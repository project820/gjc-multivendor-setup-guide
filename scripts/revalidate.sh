#!/usr/bin/env bash
# Live re-validation battery — runs on an authenticated machine (needs /login'd providers).
# Re-confirms every selector used by the profiles via real `gjc -p` calls and records a
# dated evidence table under evidence/. Portable (macOS/Linux), per-call timeout via perl alarm.
#
#   bash scripts/revalidate.sh            # full battery → evidence/<date>-selectors.md
#   SELECTORS_ONLY=1 bash scripts/revalidate.sh   # skip the long-context probes
#
# Exit code: non-zero if any selector EXPECTED to work failed (regression).
# Credential failures (expired/unauthorized/re-login needed) are recorded as
# `blocked(creds)` and do NOT count as regressions — re-run after /login <provider>.
set -uo pipefail
cd "$(dirname "$0")/.."
DATE="$(date +%Y-%m-%d)"
mkdir -p evidence
OUT="evidence/${DATE}-selectors.md"
if [ -e "$OUT" ]; then
  n=2
  while [ -e "evidence/${DATE}-selectors-rerun-${n}.md" ]; do n=$((n+1)); done
  OUT="evidence/${DATE}-selectors-rerun-${n}.md"
fi
command -v gjc >/dev/null 2>&1 || { echo "gjc not found"; exit 2; }
command -v perl >/dev/null 2>&1 || { echo "perl not found (used for per-call timeout)"; exit 2; }

FAIL=0
{ echo "# Live selector revalidation — ${DATE}"; echo
  echo "Each row: \`gjc -p --no-session --no-tools --model <selector> \"Reply OK\"\`."; echo
  echo "| selector | expect | result |"; echo "| --- | --- | --- |"; } > "$OUT"

# P <selector> <expect: ok|ok-live|fail>
P(){ local sel="$1" expect="$2" r a
  r="$(perl -e 'alarm 100; exec @ARGV' gjc -p --no-session --no-tools --model "$sel" "Reply with exactly: OK" 2>&1)"
  if printf '%s' "$r" | grep -qw OK; then a="ok"
  elif printf '%s' "$r" | tr '\n' ' ' | grep -qiE 'credential|expired|invalidated|unauthorized|401|429|rate[_ -]?limit|login|sign|no api key'; then
    a="blocked(creds/rate-limit)"   # auth/rate-limit problem, NOT a model regression
  else
    a="fail[$(printf '%s' "$r" | tr '\n' ' ' | grep -oiE 'not supported|404|500|400|did not resolve' | head -1)]"; fi
  printf '| `%s` | %s | %s |\n' "$sel" "$expect" "$a" >> "$OUT"
  case "$expect" in
    ok)
      case "$a" in
        ok) ;;
        blocked*) echo "BLOCKED(creds/rate-limit): $sel — run /login or wait for quota reset, then re-run" ;;
        *) echo "REGRESSION: $sel expected ok, got $a"; FAIL=1 ;;
      esac ;;
    fail)
      case "$a" in
        fail*) ;;
        blocked*) echo "INCONCLUSIVE: $sel expected fail but got $a — canary not proven"; FAIL=1 ;;
        *) echo "REGRESSION: $sel expected fail, got $a"; FAIL=1 ;;
      esac ;;
  esac
}

# --- catalog selectors used by the current profiles, plus documented compatibility canaries (must stay ok) ---
for s in \
  "anthropic/claude-opus-4-8:high" "anthropic/claude-sonnet-4-6:high" \
  "anthropic/claude-fable-5:high" "anthropic/claude-fable-5:xhigh" \
  "anthropic/claude-sonnet-5:high" \
  "openai-codex/gpt-5.6-sol:high" "openai-codex/gpt-5.6-sol:xhigh" \
  "openai-codex/gpt-5.6-terra:high" "openai-codex/gpt-5.6-luna:high" \
  "openai-codex/gpt-5.5:high" "openai-codex/gpt-5.4:high" \
  "google-antigravity/gemini-3.1-pro-low" "google-antigravity/gemini-3.1-pro-low:high" \
  "google-antigravity/gemini-3-flash:low" \
  "anthropic/claude-opus-4-8:medium" \
  "openai-codex/gpt-5.6-terra:medium" "openai-codex/gpt-5.6-luna:medium" \
  "xai/grok-4.5:medium" "xai/grok-4.5:high" "xai/grok-4.3:high" "xai/grok-4-fast:high" \
  "opencode-go/deepseek-v4-flash" "opencode-go/deepseek-v4-pro" \
  "opencode-go/glm-5.2" ; do P "$s" ok; done
# (glm-5.2 bundled since 0.7.10; grok-4.5 added to the catalog 2026-07-09 = xai/grok-4.5, xai API only, no grok-build variant.
#  grok-4.5 native efforts low/med/high; :xhigh/:max exit 0 but clamp to high — shipped selectors are :medium/:high only.
#  gpt-5.6-sol/terra/luna added 2026-07-10: catalog lists low..max; :max is accepted live but its depth is
#  un-benchmarked — shipped selectors cap at :xhigh. gpt-5.5 kept as a canary (retired from profiles in v1.11).
#  gemini-3-flash:low = v2 eco.critic (gemini-3.5-flash-low vanished from the live surface 07-10 PM — see below).)

# --- retired/informational selectors (not counted as regression) ---
# grok-4-1-fast: xAI retired the slug 2026-05-15 — legacy calls redirect to grok-4.3 at grok-4.3
# pricing (official migration doc). Still answers, so keep as an informational canary only;
# shipped profiles dropped it in v2 (eco.planner -> gpt-5.6-luna:medium).
for s in "xai/grok-4-1-fast:high"; do P "$s" ok-live; done

# --- antigravity fuzzy/live-surface canaries (gjc 0.9.6: fail-closed; expected to FAIL) ---
# 0.9.5 silently fuzzy-resolved unknown antigravity ids to gemini-3.1-pro-low (even -bogus).
# 0.9.6 fails closed: gemini-3.1-pro-high / gemini-3.5-flash / -bogus all return "not found".
# Also a live-surface retirement (07-10 PM): gemini-3.5-flash-low / -extra-low / gemini-pro-agent
# vanished from live calls while --list-models still printed them — live calls are the truth.
# If any of these start SUCCEEDING again, that's a resolver/surface change — re-audit the fuzzy rules.
for s in "google-antigravity/gemini-3.5-flash" "google-antigravity/gemini-3.5-flash-low" \
  "google-antigravity/gemini-3.1-pro-high" "google-antigravity/gemini-3.1-pro-bogus"; do P "$s" fail; done

# --- known rejections (documented; expected to FAIL) ---
for s in "openai-codex/gpt-5.3-codex:high" "xai/grok-4.5:bogus" "openai-codex/gpt-5.6-sol:bogus"; do P "$s" fail; done

if [ "${SELECTORS_ONLY:-0}" != 1 ]; then
  { echo; echo "## Single-message @file input limit (separate from the 1M context window)"; echo
    echo "needle answer = ZULU555"; echo
    echo "| selector | @tokens | result |"; echo "| --- | --- | --- |"; } >> "$OUT"
  gen(){ awk -v n="$1" 'BEGIN{b=int(n*0.6);for(i=1;i<=n;i++){if(i==b)printf"Record %06d: PART_X=ZULU555\n",i;else printf"Record %06d: r%d s%d\n",i,i%9,(i*7)%99999}}' > "$2"; }
  T="$(mktemp -d)"; gen 37000 "$T/350k.txt"; gen 50000 "$T/476k.txt"; gen 90000 "$T/857k.txt"
  B(){ local sel="$1" f="$2" lbl="$3" r a
    r="$(perl -e 'alarm 300; exec @ARGV' gjc -p --no-session --no-tools --model "$sel" @"$f" "Output only the PART_X value." 2>&1)"
    if printf '%s' "$r" | grep -q ZULU555; then a="found"; elif [ -z "$r" ]; then a="400/empty"; else a="resp(no-needle)"; fi
    printf '| `%s` | %s | %s |\n' "$sel" "$lbl" "$a" >> "$OUT"; }
  B "anthropic/claude-opus-4-8:high"             "$T/350k.txt" 350k
  B "anthropic/claude-opus-4-8:high"             "$T/476k.txt" 476k
  B "xai/grok-4-fast:high"                       "$T/476k.txt" 476k
  B "xai/grok-4-fast:high"                       "$T/857k.txt" 857k
  rm -rf "$T"
fi

echo >> "$OUT"; echo "_generated by scripts/revalidate.sh on ${DATE}_" >> "$OUT"
echo "Wrote $OUT"; cat "$OUT"
exit $FAIL
