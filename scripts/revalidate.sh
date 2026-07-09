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
  if [ "$expect" = ok ]; then
    case "$a" in
      ok) ;;
      blocked*) echo "BLOCKED(creds/rate-limit): $sel — run /login or wait for quota reset, then re-run" ;;
      *) echo "REGRESSION: $sel expected ok, got $a"; FAIL=1;;
    esac
  fi
}

# --- catalog selectors used by the current profiles, plus documented compatibility canaries (must stay ok) ---
for s in \
  "anthropic/claude-opus-4-8:high" "anthropic/claude-sonnet-4-6:high" \
  "anthropic/claude-fable-5:high" "anthropic/claude-fable-5:xhigh" \
  "anthropic/claude-sonnet-5:high" \
  "openai-codex/gpt-5.5:high" "openai-codex/gpt-5.4:high" \
  "google-antigravity/gemini-3.1-pro-low" "google-antigravity/gemini-3.1-pro-low:high" \
  "google-antigravity/gemini-3.5-flash-low" \
  "xai/grok-4.5:medium" "xai/grok-4.5:high" "xai/grok-4.3:high" "xai/grok-4-1-fast:high" "xai/grok-4-fast:high" \
  "opencode-go/deepseek-v4-flash" "opencode-go/deepseek-v4-pro" \
  "opencode-go/glm-5.2" ; do P "$s" ok; done
# (glm-5.2 bundled since 0.7.10; grok-4.5 added to the catalog 2026-07-09 = xai/grok-4.5, xai API only, no grok-build variant.
#  grok-4.5 native efforts low/med/high; :xhigh/:max exit 0 but clamp to high — shipped selectors are :medium/:high only.)

# --- fuzzy/dynamic selectors (informational; not counted as regression) ---
# bare gemini-3.5-flash is NOT a literal catalog id — resolves via fuzzy match to -low today;
# kept as a canary for fuzzy-resolution changes. Profiles pin gemini-3.5-flash-low (above).
for s in "google-antigravity/gemini-3.5-flash"; do P "$s" ok-live; done

# --- known rejections (documented; expected to FAIL) ---
# gemini-3.1-pro-high: appears in the catalog LISTING since 0.7.10 but the live call still 400s (trap).
for s in "google-antigravity/gemini-3.1-pro-high" "openai-codex/gpt-5.3-codex:high" "xai/grok-4.5:bogus"; do P "$s" fail; done

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
