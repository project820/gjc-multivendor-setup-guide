#!/usr/bin/env bash
# validate-profiles.py 의 fail-closed 동작을 fixture 로 증명한다.
#
# 왜 필요한가: 출하 effort 상한(fable-5 xhigh · sonnet-5 high · grok-4.6 high ·
# gpt-5.6 xhigh)과 default↔critic 계열 금지는 validator 규칙으로만 강제된다.
# 라이브 배터리는 상한 위 effort 를 호출하지 않으므로, 규칙이 조용히 느슨해져도
# 아무도 모른다. 이 스크립트가 그 음성 경로를 CI 에서 붙잡는다.
#
# fixture 는 임시 디렉터리에 만들고 실행 후 지운다 — 저장소에 커밋하지 않는다.
#
# 사용: bash scripts/ci-fixture-check.sh
#       (아직 scripts/ 로 옮기기 전에는 대기 위치에서 그대로 실행해도 된다 —
#        루트를 gjc-profiles.yml 로 식별하고, 없으면 git 최상위로 되짚는다)
# 종료코드: 0 전부 기대대로 / 1 하나라도 어긋남
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ ! -f "$ROOT/gjc-profiles.yml" ]; then
  ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || echo "$ROOT")"
  # 되짚은 경우 어느 트리를 검사하는지 반드시 보이게 한다 — 저장소 안에 만든 임시
  # 복사본에서 돌리면 조용히 실제 트리로 새어나가 오탐(false pass)이 날 수 있다.
  echo "note: repo root resolved via git → $ROOT"
fi
cd "$ROOT" || { echo "FATAL: cannot resolve repo root"; exit 1; }

VALIDATOR="scripts/validate-profiles.py"
[ -f "$VALIDATOR" ] || { echo "FATAL: $VALIDATOR not found"; exit 1; }
[ -f gjc-profiles.yml ] || { echo "FATAL: gjc-profiles.yml not found"; exit 1; }

FAIL=0
TMPROOT="$(mktemp -d)"
trap 'rm -rf "$TMPROOT"' EXIT

# make_fixture <name> <sed-expr>
make_fixture() {
  local name="$1" expr="$2" dir="$TMPROOT/$name"
  mkdir -p "$dir"
  sed "$expr" gjc-profiles.yml > "$dir/gjc-profiles.yml"
  # README 임베드 패리티 체크를 통과시키기 위해 동일 내용을 심는다
  { printf '```yaml\n'; cat "$dir/gjc-profiles.yml"; printf '\n```\n'; } > "$dir/README.md"
  printf '%s' "$dir"
}

# expect_reject <name> <sed-expr> <substring that must appear>
expect_reject() {
  local name="$1" expr="$2" needle="$3" dir out rc
  dir="$(make_fixture "$name" "$expr")"
  # sed 가 아무것도 못 바꿨으면 fixture 는 canonical 과 동일해진다. 그러면 이 검사는
  # "정상 트리를 검사해서 정상이라고 보고하는" 공허한 통과가 된다. 실패로 처리한다.
  # (2026-08-17: luna-max-pass 가 정확히 이 상태였다 — 앵커 셀렉터가 YAML 에 없어
  #  sed 무효 → 무조건 통과 → D-1 을 한 번도 검증하지 않았다.)
  if cmp -s "$dir/gjc-profiles.yml" gjc-profiles.yml; then
    echo "FAIL [$name] fixture 가 canonical 과 동일 — sed 가 아무것도 바꾸지 않았다(공허한 검증)"
    FAIL=1; return
  fi
  out="$(python3 "$VALIDATOR" --root "$dir" 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ]; then
    echo "FAIL [$name] expected rejection but validator exited 0"; FAIL=1; return
  fi
  if ! printf '%s' "$out" | grep -qF "$needle"; then
    echo "FAIL [$name] exit $rc but message missing: $needle"
    printf '%s\n' "$out" | grep -E 'ERROR' | head -3
    FAIL=1; return
  fi
  echo "ok   [$name] exit $rc · $needle"
}

# expect_accept <name> <sed-expr>  — v3 규칙이 "허용"해야 하는 경우
expect_accept() {
  local name="$1" expr="$2" dir out rc
  dir="$(make_fixture "$name" "$expr")"
  if cmp -s "$dir/gjc-profiles.yml" gjc-profiles.yml; then
    echo "FAIL [$name] fixture 가 canonical 과 동일 — sed 가 아무것도 바꾸지 않았다(공허한 검증)"
    FAIL=1; return
  fi
  out="$(python3 "$VALIDATOR" --root "$dir" 2>&1)"; rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "FAIL [$name] expected acceptance but validator exited $rc"
    printf '%s\n' "$out" | grep -E 'ERROR' | head -3
    FAIL=1; return
  fi
  echo "ok   [$name] exit 0 (accepted as designed)"
}

echo "## validator fail-closed fixtures"

# 1. shipped-ceiling 위반 4종
expect_reject grok-xhigh   's|xai/grok-4.6:high|xai/grok-4.6:xhigh|g' \
  "illegal effort 'xhigh' for grok-4.6"
expect_reject sol-max      's|gpt-5.6-sol:xhigh|gpt-5.6-sol:max|g' \
  "illegal effort 'max' for gpt-5.6-sol"
expect_reject terra-max    's|gpt-5.6-terra:high|gpt-5.6-terra:max|g' \
  "illegal effort 'max' for gpt-5.6-terra"
expect_reject fable-max    's|claude-fable-5:xhigh|claude-fable-5:max|g' \
  "illegal effort 'max' for claude-fable-5"

# 2. 정상 트리는 통과해야 한다 (가드가 과하게 잡지 않는지)
out="$(python3 "$VALIDATOR" 2>&1)"; rc=$?
if [ "$rc" -ne 0 ]; then
  echo "FAIL [canonical] real tree should pass but exited $rc"; FAIL=1
else
  echo "ok   [canonical] real tree exits 0"
fi

# 3. v3 validator 개정이 실제로 적용됐는지 (계획 D-1 · D-2)
#    v2.1.0 validator 에서는 두 케이스가 반대로 나온다 — 그래서 v3 브랜치 전에는
#    SKIP 하고, v3 규칙이 들어온 뒤에만 검사한다.
if grep -q 'gpt-5.6-luna' "$VALIDATOR" && grep -q 'max' "$VALIDATOR" \
   && python3 - "$VALIDATOR" <<'PYEOF'
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
# Luna 전용 max 허용 규칙이 일반 gpt-5.x 규칙보다 앞에 있는가
luna = src.find('gpt-5.6-luna"')
gen  = src.find('gpt-5\\.[2-9]')
sys.exit(0 if (luna != -1 and gen != -1 and luna < gen) else 1)
PYEOF
then
  echo "## v3 validator 개정 fixtures (D-1 Luna exact · D-2 default↔critic)"
  # D-1 수용(accept) 케이스는 **canonical 검사가 담당한다** — 사용자 결정
  # ("luna 는 max 만 허용한다", 2026-08-17)으로 출하 트리의 `daily.executor` 가
  # 이미 `gpt-5.6-luna:max` 다. 즉 `[canonical] real tree exits 0` 이 곧
  # "Luna:max 가 합법" 의 증거다. 따로 accept fixture 를 만들면 canonical 을
  # 한 번 더 검사하는 셈이라 공허해진다.
  #
  # 대신 **좁혀진 규칙**을 행동으로 검증한다: Luna 는 `{max}` 단독이므로
  # 다른 effort 는 거부돼야 한다. v2.1.0 에서는 `luna:medium` 이 합법이었고
  # (`eco.planner`) 지금은 아니다 — 규칙이 실제로 좁아졌는지 이걸로 잡는다.
  expect_reject luna-xhigh-fail \
    's|openai-codex/gpt-5.6-luna:max|openai-codex/gpt-5.6-luna:xhigh|' \
    "illegal effort 'xhigh' for gpt-5.6-luna"
  expect_reject luna-medium-fail \
    's|openai-codex/gpt-5.6-luna:max|openai-codex/gpt-5.6-luna:medium|' \
    "illegal effort 'medium' for gpt-5.6-luna"
  expect_reject sol-max-fail 's|gpt-5.6-sol:xhigh|gpt-5.6-sol:max|g' \
    "illegal effort 'max' for gpt-5.6-sol"
  expect_reject terra-max-fail 's|gpt-5.6-terra:high|gpt-5.6-terra:max|g' \
    "illegal effort 'max' for gpt-5.6-terra"
  expect_reject default-critic-fail \
    's|      critic:    xai/grok-4.6:high|      critic:    anthropic/claude-opus-5:high|' \
    "default/critic"
else
  echo "## v3 validator 개정 fixtures — SKIP (Luna exact matcher 미적용 = v2.1.0 validator)"
  echo "     v3 브랜치에서 D-1/D-2 가 들어오면 자동으로 검사된다."
fi

if [ "$FAIL" -eq 0 ]; then
  echo; echo "OK — every fixture behaved as expected"
else
  echo; echo "FAILED — validator fail-closed behaviour regressed"
fi
exit $FAIL
