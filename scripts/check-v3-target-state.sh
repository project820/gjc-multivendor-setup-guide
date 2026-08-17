#!/usr/bin/env bash
# 승인 계획 4b "목표 상태 게이트(v3)" — 원자 단계 직후 트리가 v3 목표 상태인지 한 번에 판정한다.
#
# 왜 필요한가: 4단계(로스터+validator 개정)는 파일 여러 개를 동시에 건드린다. 하나만 빠져도
# 개별 명령은 통과하는데 전체는 어긋난 상태가 나온다(예: 로스터는 줄었는데 개정이 안 들어감).
# 이 스크립트는 아래 축을 **한꺼번에** 보고 하나라도 어긋나면 exit 1 한다.
# (실제 출력되는 축 이름이 정본이다 — 여기 개수를 세어 적지 않는다. 세면 낡는다.)
#
#   1) 로스터가 정확히 v3 집합인가 (budget 유무는 자동 판정)
#   2) validator 개정 D-1/D-2/D-3 + D-3b(죽은 SAME_FAMILY_OK 엔트리) 가 실제로 들어갔는가
#      그리고 D-1 이 일반 gpt 룰보다 **앞**에 삽입됐는가(뒤면 :max 가 거부된다)
#   3) validate-profiles.py 가 green 인가
#   4) ci-fixture-check.sh 의 v3 fixture 가 SKIP 이 아니라 활성 상태로 통과하는가
#   5) required_providers 패리티가 맞는가
#   6) 생성 표면이 멱등인가 (sync + gen_svgs 두 번 돌려도 트리 불변)
#   `--ship` 추가 시: 퍼널 매트릭스 파싱 검증 · whats-new-v3 + 배너 · CHANGELOG/MAINTAINING · 태그 조상
#
# ⚠ 이것은 **v3 전환 1회용 게이트**다. CI 나 상시 릴리스 체크리스트에 넣지 마라 —
#   "로스터가 정확히 v3 집합인가" 를 단정하므로, v3.1 에서 번들이 정당하게 바뀌면
#   그때부터 영구히 빨간불이 된다. 상시 게이트는 validator·fixtures·parity·멱등
#   네 가지이고 그건 MAINTAINING §4 릴리스 체크리스트와 CI 가 담당한다.
#
# 사용: bash scripts/check-v3-target-state.sh          # 4b 원자 단계 게이트
#       bash scripts/check-v3-target-state.sh --ship   # + 계획 10 "출하 게이트" 축
# 종료코드: 0 전부 통과 / 1 하나라도 어긋남
set -uo pipefail
SHIP=0
for a in "$@"; do [ "$a" = "--ship" ] && SHIP=1; done
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ ! -f "$ROOT/gjc-profiles.yml" ]; then
  ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || echo "$ROOT")"
  echo "note: repo root resolved via git → $ROOT" >&2
fi
cd "$ROOT" || { echo "FATAL: cannot resolve repo root"; exit 1; }

FAIL=0
ok()   { printf 'ok   [%s] %s\n' "$1" "$2"; }
bad()  { printf 'FAIL [%s] %s\n' "$1" "$2"; FAIL=1; }

# ── 1) 로스터 ────────────────────────────────────────────────────────────────
ROSTER_OUT="$(python3 - <<'PY'
import sys, yaml
KEEP = {"daily","coding-sprint","cyber-cop","ultimate-opus","escalation","llm-council","monorepo"}
d = yaml.safe_load(open("gjc-profiles.yml"))
ps = d.get("profiles") or d.get("model_profiles")
if not isinstance(ps, dict) or not ps:
    print("NO_PROFILES"); sys.exit(0)
got = set(ps)
if got == KEEP:            print("OK 7 " + " ".join(sorted(got)))
elif got == KEEP | {"budget"}: print("OK 8 " + " ".join(sorted(got)))
else:
    print("BAD " + " ".join(sorted(got)))
    print("  extra: " + " ".join(sorted(got - (KEEP | {"budget"}))))
    print("  missing: " + " ".join(sorted(KEEP - got)))
PY
)"
case "$ROSTER_OUT" in
  "OK 7 "*) ok roster "7 번들 (budget 미출하)" ;;
  "OK 8 "*) ok roster "8 번들 (budget 포함)" ;;
  *)        bad roster "$(printf '%s' "$ROSTER_OUT" | tr '\n' ' ')" ;;
esac

# ── 2) validator 개정 ────────────────────────────────────────────────────────
V=scripts/validate-profiles.py
[ -f "$V" ] || { bad validator "$V not found"; }
if [ -f "$V" ]; then
  grep -q 'm == "gpt-5.6-luna"' "$V"            && ok D-1 "Luna exact matcher 존재" || bad D-1 "Luna exact matcher 없음"
  grep -q 'fam\["default"\] == fam\["critic"\]' "$V" && ok D-2 "default↔critic hard 규칙 존재" || bad D-2 "default↔critic 규칙 없음"
  if grep -q '"ultimate-sol":' "$V"; then bad D-3 "NON_ANTHROPIC_DEFAULT_OK 에 ultimate-sol 잔존"; else ok D-3 "stale allowlist 엔트리 제거됨"; fi
  if grep -q '("dream-team", "exec_arch")' "$V"; then bad D-3b "SAME_FAMILY_OK 에 dream-team 잔존(죽은 엔트리)"; else ok D-3b "SAME_FAMILY_OK 죽은 엔트리 없음"; fi
  # D-1 순서: Luna 룰이 일반 gpt-5.[2-9] 룰보다 앞이어야 한다.
  # 주석 줄에도 "gpt-5.[2-9] rule" 이 나오므로 **실제 룰 줄만** 비교한다.
  # (주석까지 세면 정상 트리에서 오탐이 난다 — 2026-08-17 실측으로 확인)
  LN=$(grep -nE '^[[:space:]]*\(lambda p, m:.*gpt-5\.6-luna' "$V" | head -1 | cut -d: -f1)
  GN=$(grep -nE '^[[:space:]]*\(lambda p, m:.*gpt-5\\\.\[2-9\]' "$V" | head -1 | cut -d: -f1)
  [ -n "${GN:-}" ] || GN=$(grep -nE '^[[:space:]]*\(lambda p, m:.*startswith\("gpt-5"' "$V" | head -1 | cut -d: -f1)
  if [ -z "${LN:-}" ] || [ -z "${GN:-}" ]; then
    bad D-1-order "룰 줄을 찾지 못해 순서 판정 불가 (luna=${LN:-none} generic=${GN:-none})"
  elif [ "$LN" -lt "$GN" ]; then
    ok D-1-order "Luna 룰이 일반 gpt 룰보다 앞 (L$LN < L$GN)"
  else
    bad D-1-order "Luna 룰이 일반 gpt 룰보다 뒤 (L$LN > L$GN) — :max 가 거부된다"
  fi
fi

# 임시 파일은 mktemp 로 잡는다 — 예측 가능한 /tmp 이름은 공용 호스트에서
# 심링크·TOCTOU 로 덮어쓰기 당한다(ci-fixture-check.sh 가 이미 mktemp 를 쓴다).
TMPD="$(mktemp -d "${TMPDIR:-/tmp}/v3gate.XXXXXX")"
trap 'rm -rf "$TMPD"' EXIT

# ── 3) validator green ───────────────────────────────────────────────────────
if python3 "$V" >"$TMPD/v.txt" 2>&1; then ok invariants "$(tail -1 "$TMPD/v.txt")"
else bad invariants "$(grep -E '^  ERROR' "$TMPD/v.txt" | head -3 | tr '\n' ' ')"; fi

# ── 4) fixtures (SKIP 이면 실패로 본다 — 개정이 안 들어간 것) ──────────────────
if [ -f scripts/ci-fixture-check.sh ]; then
  if bash scripts/ci-fixture-check.sh >"$TMPD/f.txt" 2>&1; then
    if grep -q 'SKIP' "$TMPD/f.txt"; then bad fixtures "v3 fixture 가 SKIP 상태 — validator 개정 미적용"
    else ok fixtures "v3 fixture 활성 + 전부 통과"; fi
  else bad fixtures "$(tail -1 "$TMPD/f.txt")"; fi
else bad fixtures "scripts/ci-fixture-check.sh not found"; fi

# ── 5) provider parity ───────────────────────────────────────────────────────
if [ -f scripts/check-provider-parity.py ]; then
  if python3 scripts/check-provider-parity.py >"$TMPD/p.txt" 2>&1; then ok parity "$(tail -1 "$TMPD/p.txt")"
  else bad parity "$(tail -1 "$TMPD/p.txt")"; fi
else bad parity "scripts/check-provider-parity.py not found"; fi

# ── 6) 생성 표면 멱등 ────────────────────────────────────────────────────────
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
  python3 scripts/sync-readme-yaml.py >/dev/null 2>&1
  # gen_svgs.py 가 실패하면 멱등 검사를 **건너뛴다**. 돌리면 "실패한 두 상태가 서로
  # 같다" 를 보고 `ok generators 멱등` 을 찍어버려서, 같은 축에 FAIL 과 ok 가 동시에
  # 나온다(2026-08-17 시뮬레이션 릴리스 트리에서 실측). 생성기가 돌지도 않았는데
  # 멱등을 통과했다고 적는 것은 공허한 ok 다.
  #
  # 해시 대상은 **생성물 내용**이다. 예전엔 `git status --porcelain` 을 해시했는데
  # 그건 파일 이름과 상태 플래그만 담는다 — 이미 ` M` 인 파일이 2차 실행에서 내용만
  # 또 바뀌면 porcelain 출력은 똑같아서 "멱등" 으로 오판한다(cyber-cop 패널 지적).
  if python3 scripts/gen_svgs.py >/dev/null 2>&1; then
    _gen_hash() { shasum -a 256 assets/*.svg README.md README.en.md README.ja.md README.zh.md | shasum -a 256 | cut -d' ' -f1; }
    H1="$(_gen_hash)"
    python3 scripts/sync-readme-yaml.py >/dev/null 2>&1
    python3 scripts/gen_svgs.py >/dev/null 2>&1
    H2="$(_gen_hash)"
    [ "$H1" = "$H2" ] && ok generators "sync+gen_svgs 멱등 (생성물 내용 해시)" || bad generators "재실행 시 생성물 내용이 또 바뀐다"
  else
    bad generators "gen_svgs.py 실패 — _PROFILE_CHROME/_MODEL_DISPLAY 편집 필요 (멱등 검사 건너뜀)"
  fi
else
  echo "skip [generators] git 트리가 아니라 멱등 검사 생략" >&2
fi

# ── 7) 정본 YAML 헤더 주석 (2026-08-17 추가 — MAINTAINING-v3-updates.md §10) ──
# v3 로스터 축소는 프로필 **블록**만 지웠다. 헤더 주석은 현행 상태 서술이라
# 번들이 사라지면 그 자리에서 거짓이 되는데, 여기 오기 전까지 **어떤 가드도 안 봤다.**
#
# 오탐 방지 — 검사 구간을 `profiles:` 앞(헤더)으로 한정한다. 본문 아래쪽의
#   `#   ultimate → ultimate-opus … dream-team ·`  /  `… eco 전면 재편 …`
# 두 줄은 **v2.0 이행 이력**이고 삭제된 번들 이름이 나오는 것이 정상이다.
# 파일 전체를 훑으면 이 두 줄에서 반드시 오탐이 난다.
#
# 무엇으로 바꿀지는 검사하지 않는다 — `budget` 의 tier 는 결정 #6 이라 정답이 아직 없다.
# 여기서는 **낡은 토큰이 남아 있지 않은지**만 본다(fail-closed 하되 결정은 침범 안 함).
HDR="$(awk '/^profiles:/{exit} {print}' gjc-profiles.yml)"
HDR_BAD=""
for t in eco dream-team ultimate-sol; do
  printf '%s\n' "$HDR" | grep -q -- "$t" && HDR_BAD="$HDR_BAD $t"
done
printf '%s\n' "$HDR" | grep -q "v2\.1\.0"  && HDR_BAD="$HDR_BAD v2.1.0"
printf '%s\n' "$HDR" | grep -q "10 번들"   && HDR_BAD="$HDR_BAD 10번들"
printf '%s\n' "$HDR" | grep -q "출하 상한은 xhigh" && HDR_BAD="$HDR_BAD 출하상한xhigh(Luna:max 미반영)"
if [ -z "$HDR_BAD" ]; then
  ok yaml-header "헤더 주석에 낡은 토큰 없음"
else
  bad yaml-header "헤더 주석이 아직 v2.1.0 을 말한다 —$HDR_BAD (§10 참조)"
fi

# opencode-go 좌석 안내 줄 — 본문이지만 이력이 아니라 **현행 안내**다.
if grep -q "^# opencode-go:.*eco\.executor" gjc-profiles.yml; then
  bad yaml-provider-note "opencode-go 줄이 아직 eco.executor 를 가리킨다 (§10 #5)"
else
  ok yaml-provider-note "opencode-go 좌석 안내 갱신됨"
fi

# ── 8) README §5 번들 카드 ↔ 로스터 1:1 (2026-08-17 추가) ────────────────────
# `README.md` §5 는 번들마다 `- **name** — 설명` 카드를 하나씩 갖는다(v2.1.0 에서 10/10
# 일치 실측). 이 카드가 **번들 설명의 유일한 출처**다 — 퍼널 tier 표를 v3 매트릭스로
# 교체하면 `한 줄 정의`·`이럴 때` 열이 사라지므로(7×2=14셀), §5 카드만 남는다.
#
# 2026-08-17 실측: 시뮬레이션 릴리스 트리에서 `budget` 카드가 **없고**
# `dream-team`·`eco`·`ultimate-sol` 죽은 카드가 **남아 있는데** 모든 게이트가 통과했다.
# 즉 "설명 없는 번들이 출하되고, 없는 번들이 설명을 갖는" 상태를 아무도 안 봤다.
CARD_BAD="$(python3 - <<'PY'
import re, yaml
d = yaml.safe_load(open('gjc-profiles.yml', encoding='utf-8'))
roster = sorted((d.get('profiles') or {}))
txt = open('README.md', encoding='utf-8').read()
cards = re.findall(r'^- \*\*([a-z0-9-]+)\*\*\s*[\u2014-]', txt, re.M)
miss = [b for b in roster if b not in cards]
dead = [c for c in sorted(set(cards)) if c not in roster]
dup = sorted({c for c in cards if cards.count(c) > 1})
out = []
if miss: out.append('\uc124\uba85\uc5c6\ub294\ubc88\ub4e4=' + ','.join(miss))
if dead: out.append('\uc8fd\uc740\uce74\ub4dc=' + ','.join(dead))
if dup:  out.append('\uc911\ubcf5\uce74\ub4dc=' + ','.join(dup))
print(' '.join(out))
PY
)"
if [ -z "$CARD_BAD" ]; then
  ok readme-cards "§5 번들 카드 ↔ 로스터 1:1"
else
  bad readme-cards "§5 카드가 로스터와 어긋난다 — $CARD_BAD · 문구 원문은 .gjc/v3-pending-docs/bundle-blurbs-v3.md (결정 #2)"
fi

# ── 9) routing-rules.md 에 삭제 번들 잔존 (2026-08-17 추가) ──────────────────
# 이 파일은 **전부 현행 서술**이다 — 역사 절이 없다(2026-08-17 구조 확인).
# 그래서 삭제 번들 이름이 남아 있으면 예외 없이 결함이다. 실측 잔존 7행/10건:
#   1행 문서 제목(§8 불변식의 9번째 인스턴스) · 35·39·46행 tier·용도 목록
#   43행 "대량·비용압박: eco" · 85행 정책 경고 · 94행 Luna 단가 각주(eco.planner)
#
# `codex-eco` 는 **GJC 내장 프로필**이고 삭제 대상이 아니다(39행에 실재).
# 그래서 경계에 `-` 를 포함시켜야 한다 — 안 그러면 그 문장을 파괴한다(§26).
RR_BAD="$(python3 - <<'PY'
import re, os
p = 'routing-rules.md'
if not os.path.exists(p):
    print('routing-rules.md \uc5c6\uc74c'); raise SystemExit
txt = open(p, encoding='utf-8').read()
pat = re.compile(r'(?<![A-Za-z0-9-])(eco|dream-team|ultimate-sol)(?![A-Za-z0-9-])')
hits = {}
for i, line in enumerate(txt.split('\n'), 1):
    n = len(pat.findall(line))
    if n:
        hits[i] = n
if hits:
    print('%d\ud589/%d\uac74 \u2014 \ud589: %s'
          % (len(hits), sum(hits.values()), ','.join(str(k) for k in sorted(hits))))
PY
)"
if [ -z "$RR_BAD" ]; then
  ok routing-rules "routing-rules.md 에 삭제 번들 없음"
else
  bad routing-rules "routing-rules.md 에 삭제 번들 잔존 — $RR_BAD (§12·§26 · codex-eco 는 건드리지 마라)"
fi

# ── 10) docs/factsheet.md — §2 밖 4건 (2026-08-17 추가) ──────────────────────
# `check-factsheet-parity.py`(결정 #4 제안)는 **§2 표만** 파싱한다. §16 이 확정한
# 편집 10건 중 6~10번(§1 버전 · §3 Luna 상한 · §3 Qwen 행 · §5 불변식)은
# 채택하든 안 하든 **무가드**였다. 여기서 그 4건만 좁게 본다 — §3 전체를 파싱하는
# 계약을 새로 만들지 않는다(가격·ctx·검증일이 섞인 사람용 표다).
#
# Sol·Terra 행의 `xhigh 출하상한` 은 **v3 에서도 참**이므로 건드리지 않는다.
# Luna 행만 결정 #1 로 거짓이 된다(§17).
FS_BAD="$(python3 - <<'PY'
import os, re, yaml

p = 'docs/factsheet.md'
if not os.path.exists(p):
    print('factsheet \uc5c6\uc74c'); raise SystemExit
txt = open(p, encoding='utf-8').read()
prof = (yaml.safe_load(open('gjc-profiles.yml', encoding='utf-8')).get('profiles') or {})
sels = {v for s in prof.values() for v in (s.get('model_mapping') or {}).values()}
dead = re.compile(r'ultimate-sol|dream-team|(?<![A-Za-z0-9-])eco(?![A-Za-z0-9-])')
out = []

# 6) \u00a71 \ub9b4\ub9ac\uc2a4 \ud589 \u2014 \uad6c \ubc84\uc804\u00b7\uad6c \uac1c\uc218
for line in txt.split('\n'):
    if line.startswith('| \uac00\uc774\ub4dc \ubc84\uc804'):
        if 'v2.1.0' in line or '10\ubc88\ub4e4' in line:
            out.append('\u00a71\ubc84\uc804\ud589')
        break

# 9) \u00a73 Luna \ud589 \u2014 \uacb0\uc815 #1 \ub85c \uac70\uc9d3
if any(v.endswith('gpt-5.6-luna:max') for v in sels):
    for line in txt.split('\n'):
        if line.startswith('| GPT-5.6 Luna') and 'xhigh' in line:
            out.append('\u00a73Luna\uc0c1\ud55c')
            break

# 10) \u00a73 \ucd9c\ud558 \uc140\ub809\ud130\uc5d0 qwen \uc774 \uc788\uc73c\uba74 \ud589\ub3c4 \uc788\uc5b4\uc57c \ud55c\ub2e4
if any('qwen' in v for v in sels) and 'qwen' not in txt.lower():
    out.append('\u00a73Qwen\ud589\uc5c6\uc74c')

# 8) \u00a75 \ubd88\ubcc0\uc2dd \ubaa9\ub85d\uc5d0 \uc0ad\uc81c \ubc88\ub4e4
for line in txt.split('\n'):
    if line.lstrip().startswith('2. default = Anthropic') and dead.search(line):
        out.append('\u00a75\ubd88\ubcc0\uc2dd')
        break

print(','.join(out))
PY
)"
if [ -z "$FS_BAD" ]; then
  ok factsheet-prose "factsheet §2 밖 4건 갱신됨"
else
  bad factsheet-prose "factsheet §2 밖이 낡았다 — $FS_BAD (§16 6~10번 · 가드 채택과 무관하게 손 편집 대상)"
fi

# ── 출하 게이트 (--ship) — 계획 "수용 기준" 중 기계 검증 가능한 것 ─────────────
if [ "$SHIP" = 1 ]; then
  echo
  echo "## 출하 게이트 (계획 10단계)"

  # `check-funnel-parity.py` 는 실패 시 **exit 1** 을 낸다(CI 스텝이 그 코드로 판정한다).
  # 이 스크립트는 26행에서 `set -uo pipefail` 만 켠다 — `-e` 는 **의도적으로 없다.**
  # `-e` 를 켜면 아래 명령치환의 비영 종료가 25축 순회를 중간에 끊어버려서 `bad funnel`
  # 을 기록하지 못한다. 축 하나가 실패해도 나머지 축은 계속 재야 한다.
  # #5 퍼널 매트릭스: 각 shipped 번들의 required_providers 가 정확히 하나의 최소행과 집합 동일
  FUNNEL="$(python3 scripts/check-funnel-parity.py 2>&1)"
  case "$FUNNEL" in
    OK*)  ok funnel "$FUNNEL" ;;
    *)    bad funnel "$FUNNEL" ;;
  esac

  # #8 whats-new-v3 존재 + 구 공지 배너 + CHANGELOG 에는 배너 없음
  #
  # 계획이 금지한 것은 CHANGELOG **최상단의 공지 배너**(`> … whats-new-v3.md` 인용줄)다.
  # 파일명 언급 자체가 아니다 — CHANGELOG 항목이 "whats-new-v3.md 의 이 문장을 고쳤다"
  # 라고 쓰는 것은 정상이고 오히려 권장된다. 예전 검사는 파일 전체를 `grep -q
  # "whats-new-v3.md"` 로 훑어서 그런 정상 항목에 FAIL 을 냈다(#27 머지 직후 실측).
  # 크루드한 검사가 오탐을 내면 사람은 문서를 약하게 고치거나 게이트를 무시한다 —
  # 둘 다 나쁘다.
  #
  # 판정식은 **양방향이 같은 모양**을 써야 한다(cyber-cop 패널 지적). 예전엔 음성만
  # `^>` 로 좁혀서, 구 공지 파일 쪽은 배너가 아니라 단순 파일명 언급만 있어도 "배너 존재"
  # 로 통과했다. 아래 `_has_banner` 하나를 양쪽이 공유한다.
  #
  # 범위도 좁힌다 — CHANGELOG 는 **첫 릴리스 헤딩(`## v…`) 앞**까지가 배너 자리다.
  # 그 아래 항목 본문의 인용문이 파일명을 언급하는 것은 배너가 아니다.
  # `$2` 는 **명시적 센티널**을 쓴다: `all` = 파일 전체, 숫자 = 그 줄수까지.
  # 예전엔 `0` 을 "전체" 로 썼는데, CHANGELOG 가 곧바로 `## v…` 로 시작하면 배너 영역이
  # 0줄이고 awk 도 `0` 을 돌려준다. 그러면 "전체 스캔" 으로 조용히 되돌아가 이 hunk 가
  # 없애려던 #27 오탐이 다시 살아난다(cyber-cop 패널 지적). awk 실패·파일 부재도 같다.
  _has_banner() {  # $1=file  $2=all | <줄수>
    [ -f "$1" ] || return 1
    if [ "$2" = "all" ]; then cat "$1"; else head -n "$2" "$1"; fi \
      | grep -qE '^[[:space:]]*>.*whats-new-v3\.md'
  }
  if [ -f docs/whats-new-v3.md ]; then ok whats-new "docs/whats-new-v3.md 존재"; else bad whats-new "docs/whats-new-v3.md 없음"; fi
  for f in docs/whats-new-v2.md docs/whats-new-cyber-cop.md; do
    if _has_banner "$f" all; then ok banner "$f 배너 존재(인용줄 모양)"; else bad banner "$f 배너 없음 — 파일명만 언급된 것은 배너가 아니다"; fi
  done
  # CHANGELOG 의 배너 자리 = 첫 `## v…` 헤딩 앞. awk 가 실패하면 0줄(= 검사 안 함)이 아니라
  # **실패로 본다** — 범위를 못 정한 채 통과시키면 그게 무가드다.
  if ! CL_HEAD="$(awk '/^## v/{exit} {n++} END{print n+0}' CHANGELOG.md 2>/dev/null)"; then
    bad banner "CHANGELOG.md 배너 영역을 계산하지 못했다(awk 실패)"
  elif _has_banner CHANGELOG.md "$CL_HEAD"; then
    bad banner "CHANGELOG.md 머리 ${CL_HEAD}줄에 공지 배너가 들어갔다(계획상 제외 대상)"
  else
    ok banner "CHANGELOG.md 머리 ${CL_HEAD}줄에 공지 배너 없음(의도대로 — 항목 내 파일명 언급은 정상)"
  fi

  # #11 CHANGELOG v3.0.0 + MAINTAINING MAJOR 사례
  if grep -qE '^#+ .*v?3\.0\.0' CHANGELOG.md 2>/dev/null; then ok changelog "v3.0.0 항목 존재"; else bad changelog "CHANGELOG 에 v3.0.0 항목 없음"; fi
  if grep -q "Worked example" MAINTAINING.md 2>/dev/null; then ok maintaining "MAJOR 사례 기재됨"; else bad maintaining "MAINTAINING 에 MAJOR 사례 없음"; fi

  # #10 태그가 분기점보다 앞서는가
  if git rev-parse "v2.1.0^{commit}" >/dev/null 2>&1; then
    if git merge-base --is-ancestor "v2.1.0^{commit}" HEAD 2>/dev/null; then ok tag "v2.1.0 이 HEAD 의 조상"
    else bad tag "v2.1.0 이 HEAD 의 조상이 아니다 — 분기점 확인 필요"; fi
  else bad tag "v2.1.0 태그 없음"; fi

  # 출하 SVG 에 **삭제된 번들 이름**이 남아 있는가 (2026-08-17 추가)
  #
  # gen_svgs 의 fail-closed 는 `_PROFILE_CHROME` **키**만 로스터와 대조한다. 제목·푸터의
  # **하드코딩 산문**은 안 본다. 2026-08-17 시뮬레이션 릴리스 트리 실측 — 런북을 전부
  # 올바르게 수행하고 SVG 를 재생성했는데도 이렇게 남았다:
  #   profiles-matrix.svg 푸터  "예외: opt-in ultimate-sol=Sol · anthropic 미포함 eco=Terra"
  #                             "🔥 dream-team = Fable 5 (…)"
  #   role-winners.svg   제목   "🔥 dream-team 셋업 — 역할별 최강 가설"
  # 즉 **없는 번들을 광고하는 SVG 가 출하된다.** 이 저장소가 이미 겪은 사고와 같은 계열
  # (좌석 교체가 SVG 에 반영되지 않아 공개 문서가 정본과 반대로 말했다).
  SVG_BAD=""
  ROSTER="$(python3 - <<'PY'
import yaml
d=yaml.safe_load(open('gjc-profiles.yml',encoding='utf-8'))
print(' '.join(sorted((d.get('profiles') or {}).keys())))
PY
)"
  for f in assets/*.svg; do
    [ -f "$f" ] || continue
    [ "$f" = "assets/routing-tree.svg" ] && continue   # 생성 대상이 아니다
    for dead in dream-team eco ultimate-sol trio luna-scale research-long; do
      case " $ROSTER " in *" $dead "*) continue ;; esac
      grep -q -- "$dead" "$f" && SVG_BAD="$SVG_BAD ${f##*/}:$dead"
    done
  done
  if [ -z "$SVG_BAD" ]; then
    ok svg-prose "출하 SVG 에 삭제 번들 이름 없음"
  else
    bad svg-prose "SVG 가 없는 번들을 광고한다 —$SVG_BAD · profiles-matrix 푸터는 MAINTAINING-v3-updates §6/§8, role-winners 는 결정 #7"
  fi

  # README ×4 의 `## 5.` 제목에 박힌 **번들 개수**가 실제 로스터와 맞나 (2026-08-17 추가)
  #
  # 2026-08-17 실측 — 시뮬레이션 릴리스 트리에서 로스터는 8인데 네 README 의 §5 제목이
  # 전부 "10 번들/10 bundles/10 バンドル/10 个捆绑" 이었고 `--ship` 이 **통과했다.**
  # 개수가 제목에 박혀 있어 사람 눈에만 보이고 어떤 가드도 안 봤다.
  #
  # 제목을 고치면 GitHub 앵커 슬러그가 바뀌어 링크 17건이 조용히 죽는다 →
  # 같은 커밋에서 `slug-anchor-check.py` 를 함께 돌려라(MAINTAINING-v3-updates §18·§20·§21).
  N_BUNDLES="$(python3 - <<'PY'
import yaml
d = yaml.safe_load(open('gjc-profiles.yml', encoding='utf-8'))
print(len((d.get('profiles') or {})))
PY
)"
  HEAD_BAD=""
  for rf in README.md README.en.md README.ja.md README.zh.md; do
    [ -f "$rf" ] || continue
    H="$(grep -m1 '^## 5\.' "$rf" || true)"
    [ -n "$H" ] || { HEAD_BAD="$HEAD_BAD $rf:§5제목없음"; continue; }
    # 제목에서 첫 정수만 뽑는다(절 번호 `5.` 는 건너뛴다)
    CNT="$(printf '%s\n' "$H" | sed 's/^## 5\.//' | grep -oE '[0-9]+' | head -1 || true)"
    if [ -z "$CNT" ]; then
      continue        # 개수를 제목에서 뺐다면(§20 권고안 B) 검사 대상 아님 — 정상
    fi
    [ "$CNT" = "$N_BUNDLES" ] || HEAD_BAD="$HEAD_BAD ${rf}:${CNT}"
  done
  if [ -z "$HEAD_BAD" ]; then
    ok readme-count "§5 제목 개수 = 로스터 $N_BUNDLES (또는 제목에서 개수 제거됨)"
  else
    bad readme-count "§5 제목이 로스터($N_BUNDLES)와 다르다 —$HEAD_BAD · 고치면 앵커 링크 17건도 함께(§21)"
  fi
fi

echo
if [ "$FAIL" = 0 ]; then echo "OK — v3 게이트 통과$([ "$SHIP" = 1 ] && echo ' (출하 게이트 포함)')"; else echo "FAILED — v3 게이트 미통과"; fi
exit "$FAIL"
