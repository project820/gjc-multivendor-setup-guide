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

# --- shipped selectors: derived from gjc-profiles.yml, NOT hand-listed ---
# 손으로 적은 로스터는 정본과 조용히 어긋난다. gen_svgs.py 가 같은 결함으로 공개 SVG 를
# 정본과 반대로 렌더한 사고가 있었다(v2.1.0 리뷰). 여기서는 yml 에서 출하 셀렉터를 뽑고,
# 아래 카나리는 "출하 아님"을 명시한 채 별도로 더한다.
_REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SHIPPED_SELECTORS="$(python3 - "$_REPO_ROOT/gjc-profiles.yml" <<'PYEOF'
import sys, yaml
with open(sys.argv[1], encoding="utf-8") as fh:
    data = yaml.safe_load(fh)
profiles = data.get("profiles") or data.get("model_profiles") or {}
seen = []
for spec in profiles.values():
    for sel in spec["model_mapping"].values():
        if sel not in seen:
            seen.append(sel)
print("\n".join(seen))
PYEOF
)"
if [ -z "$SHIPPED_SELECTORS" ]; then
  echo "FATAL: could not derive shipped selectors from gjc-profiles.yml"; exit 1
fi
echo "## Shipped selectors (derived from gjc-profiles.yml: $(echo "$SHIPPED_SELECTORS" | wc -l | tr -d ' ') unique)"
# 파이프라인 대신 here-string 을 쓴다. `printf | while` 은 서브셸이라 P() 안의
# FAIL=1 이 부모로 안 올라오고, 회귀가 나도 마지막 `exit $FAIL` 이 0 이 된다.
while IFS= read -r s; do
  [ -n "$s" ] && P "$s" ok
done <<< "$SHIPPED_SELECTORS"

# --- documented compatibility canaries (NOT shipped seats; must still resolve) ---
# 여기 있는 셀렉터는 위 파생 목록과 겹치면 안 된다. 겹치면 "출하 아님" 라벨이 거짓이 되고
# 같은 셀렉터를 두 번 호출하게 된다. 아래 CANARY_OVERLAP 가드가 그걸 잡는다.
CANARIES="
anthropic/claude-opus-4-8:high
anthropic/claude-sonnet-4-6:high
anthropic/claude-sonnet-5:high
openai-codex/gpt-5.6-luna:high
openai-codex/gpt-5.5:high
openai-codex/gpt-5.4:high
google-antigravity/gemini-3.1-pro-low
xai/grok-4.6:medium
xai/grok-4.5:medium
xai/grok-4.5:high
xai/grok-4.3:high
xai/grok-4-fast:high
"
CANARY_OVERLAP="$(printf '%s\n' "$SHIPPED_SELECTORS" "$CANARIES" | sed '/^$/d' | sort | uniq -d)"
if [ -n "$CANARY_OVERLAP" ]; then
  echo "FATAL: canary list overlaps shipped selectors (label says NOT shipped):"
  printf '  %s\n' $CANARY_OVERLAP
  exit 1
fi
while IFS= read -r s; do
  [ -n "$s" ] && P "$s" ok
done <<< "$CANARIES"
# (v2.1.0 / gjc 0.13.3 / 2026-08-16: opus-5 + grok-4.6 added as shipped successors.
#  grok-4.5 kept as a legacy canary. gpt-5.6 :max still un-benchmarked — shipped cap xhigh.
#  gemini-3-flash:low stays eco.critic (3.5-flash-low resurrected 08-16 but live-surface flaps).
#  deepseek-v4-flash/pro are catalog-live but this account 403s China-opt-in — informational below.)

# --- retired/informational selectors (not counted as regression) ---
# grok-4-1-fast: xAI retired the slug 2026-05-15 — legacy calls redirect to grok-4.3 at grok-4.3
# pricing (official migration doc). Still answers, so keep as an informational canary only.
# deepseek-v4-*: catalog id lives; 2026-08-16 this account 403s "China hosted / explicit opt-in".
#   NOT a shipped seat anymore — eco.executor moved to opencode-go/glm-5.2 in v2.1.0 precisely so
#   that no shipped seat depends on an entitlement this account lacks. Informational canary only;
#   if the region policy lifts, re-probe and re-evaluate as a candidate.
# grok-build/grok-4.6 (bare) resolves; :high does not — bare is informational only.
# gemini-3.5-flash-low resurrected 08-16 after the 07-10 PM vanishing — flap, not a seat.
for s in "xai/grok-4-1-fast:high" "opencode-go/deepseek-v4-flash" "opencode-go/deepseek-v4-pro" \
  "grok-build/grok-4.6" "google-antigravity/gemini-3.5-flash-low"; do P "$s" ok-live; done

# --- antigravity fuzzy/live-surface canaries (fail-closed; expected to FAIL) ---
# 0.9.6+ fails closed: gemini-3.1-pro-high / bare gemini-3.5-flash / -bogus all return "not found".
# If any of these start SUCCEEDING again, that's a resolver/surface change — re-audit the fuzzy rules.
for s in "google-antigravity/gemini-3.5-flash" \
  "google-antigravity/gemini-3.1-pro-high" "google-antigravity/gemini-3.1-pro-bogus"; do P "$s" fail; done

# --- known rejections (documented; expected to FAIL) ---
for s in "openai-codex/gpt-5.3-codex:high" "xai/grok-4.6:bogus" "openai-codex/gpt-5.6-sol:bogus" \
  "grok-build/grok-4.6:high"; do P "$s" fail; done

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
  B "anthropic/claude-opus-5:high"             "$T/350k.txt" 350k
  B "anthropic/claude-opus-5:high"             "$T/476k.txt" 476k
  B "xai/grok-4-fast:high"                       "$T/476k.txt" 476k
  B "xai/grok-4-fast:high"                       "$T/857k.txt" 857k
  rm -rf "$T"
fi

echo >> "$OUT"; echo "_generated by scripts/revalidate.sh on ${DATE}_" >> "$OUT"
echo "Wrote $OUT"; cat "$OUT"
exit $FAIL
