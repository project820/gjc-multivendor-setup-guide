#!/usr/bin/env bash
# ============================================================================
#  GJC 멀티벤더 셋업 — 원클릭 설치기
#  https://github.com/project820/gjc-multivendor-setup-guide
#
#  사용법:
#    curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
#
#  옵션(환경변수):
#    GJC_SETUP_DEFAULT=ultimate  # 기본 프로필 지정(기본값: daily). none 이면 기본설정 건너뜀
#      예) curl -fsSL <url>/install.sh | GJC_SETUP_DEFAULT=ultimate bash
#    GJC_CODING_AGENT_DIR=...    # GJC 에이전트 디렉터리 override (기본: ~/.gjc/agent)
#    GJC_SETUP_COP=1             # cyber-cop reviewer 도구 설치: routing-rules.md + 오케스트레이터 +
#                               #   trusted validator 를 ~/.gjc/agent/cyber-cop/ 에 배송하고
#                               #   `gjc-cop` 래퍼를 ~/.local/bin 에 등록 (클론 없이 PR 리뷰)
#
#  안전장치: 기존 models.yml / config.yml 자동 백업 · 관리블록 sentinel 로 재실행 시 깔끔 교체.
#  ⚠ GJC 0.7.10 의 프리셋 rename/delete 는 models.yml 주석(sentinel 포함)을 전부 제거함 —
#    sentinel 이 사라진 파일에서는 이름 기반 교체로 동작하며, GJC 에서 삭제한 가이드 프로필이
#    재설치 시 부활함(설치 전 경고 출력).
# ============================================================================
set -euo pipefail

REPO_RAW="${GJC_SETUP_REPO:-https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main}"
PROFILES_URL="$REPO_RAW/gjc-profiles.yml"
DIR="${GJC_CODING_AGENT_DIR:-$HOME/.gjc/agent}"
TARGET="$DIR/models.yml"
CONFIG="$DIR/config.yml"
DEFAULT_PROFILE="${GJC_SETUP_DEFAULT:-daily}"
SENTINEL="gjc-multivendor-setup-guide"

b(){ printf '\033[1;36m%s\033[0m\n' "$*"; }
g(){ printf '\033[32m%s\033[0m\n' "$*"; }
y(){ printf '\033[33m%s\033[0m\n' "$*"; }
die(){ printf '\033[31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

command -v python3 >/dev/null 2>&1 || die "python3 가 필요합니다 (YAML 안전 병합에 사용)."

b "▶ GJC 멀티벤더 셋업 설치"

# 1) 프로필 소스 확보 (로컬 테스트는 GJC_SETUP_SRC 로 파일 지정)
SRC="$(mktemp)"; trap 'rm -f "$SRC"' EXIT
if [ -n "${GJC_SETUP_SRC:-}" ]; then
  cp "$GJC_SETUP_SRC" "$SRC"; echo "  · 소스(로컬): $GJC_SETUP_SRC"
else
  command -v curl >/dev/null 2>&1 || die "curl 이 필요합니다."
  curl -fsSL "$PROFILES_URL" -o "$SRC" || die "프로필 다운로드 실패: $PROFILES_URL"
  echo "  · 소스: $PROFILES_URL"
fi

# 1b) 프로필 로스터/카운트를 소스에서 파생 (하드코딩 금지 — 프로필 추가 시 자동 반영)
PROFILE_NAMES="$(python3 - "$SRC" <<'PY'
import sys, re
s = open(sys.argv[1], encoding="utf-8").read().splitlines()
pi = next((i for i, l in enumerate(s) if l.rstrip() == "profiles:"), None)
if pi is None: sys.exit("소스에 profiles: 블록이 없습니다")
names = [m.group(1) for l in s[pi+1:]
         for m in [re.match(r"^  ([A-Za-z0-9_-]+):\s*(#.*)?$", l)] if m]
print(" ".join(names))
PY
)" || die "프로필 소스 파싱 실패"
PROFILE_COUNT="$(printf '%s' "$PROFILE_NAMES" | wc -w | tr -d ' ')"
[ "$PROFILE_COUNT" -gt 0 ] || die "프로필 소스에서 프로필을 찾지 못했습니다"

mkdir -p "$DIR"

# 1c) sentinel 소실 감지 — GJC 0.7.10 의 프리셋 rename/delete 는 models.yml 의 모든 주석을
#     제거하므로 관리블록 sentinel 도 사라짐. 그 경우 병합은 '이름 기반 교체'로 격하됨.
if [ -f "$TARGET" ] && ! grep -q "$SENTINEL" "$TARGET"; then
  for _n in $PROFILE_NAMES; do
    if grep -qE "^  ${_n}:" "$TARGET"; then
      y "⚠ 기존 models.yml 에 관리블록 sentinel 이 없습니다 (GJC 0.7.10 프리셋 편집이 주석을 제거한 것으로 보임)."
      y "  → 이름 기반 교체로 병합합니다: 가이드와 같은 이름의 프로필은 원본으로 덮어써지고,"
      y "    GJC 에서 삭제했던 가이드 프로필도 재설치로 부활합니다. (백업: $TARGET.bak-<ts>)"
      break
    fi
  done
fi

# 2) 백업
TS="$(date +%Y%m%d-%H%M%S)"
[ -f "$TARGET" ] && { cp "$TARGET" "$TARGET.bak-$TS"; echo "  · 백업: $TARGET.bak-$TS"; }
[ -f "$CONFIG" ] && cp "$CONFIG" "$CONFIG.bak-$TS"

# 3) profiles 병합 (관리블록 sentinel — 재실행 시 자동 교체, 동일이름 기존 프로필은 교체)
python3 - "$TARGET" "$SRC" "$SENTINEL" <<'PY'
import sys, os, re
target, src, name = sys.argv[1], sys.argv[2], sys.argv[3]
START = f"  # >>> {name} (managed block — 재실행 시 자동 교체) >>>"
END   = f"  # <<< {name} <<<"

s = open(src, encoding="utf-8").read().splitlines()
pi = next((i for i, l in enumerate(s) if l.rstrip() == "profiles:"), None)
if pi is None: sys.exit("소스에 profiles: 블록이 없습니다")
children = s[pi+1:]
while children and not children[0].strip(): children.pop(0)
while children and not children[-1].strip(): children.pop()
managed = [START] + children + [END]
our = {m.group(1) for l in children for m in [re.match(r"^  ([A-Za-z0-9_-]+):\s*(#.*)?$", l)] if m}

content = open(target, encoding="utf-8").read() if os.path.exists(target) else ""
content = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", content, flags=re.S)
lines = content.splitlines()

pidx = next((i for i, l in enumerate(lines) if re.match(r"^profiles:\s*$", l)), None)
replaced = []
if pidx is None:
    base = ("\n".join(lines).rstrip() + "\n\n") if any(l.strip() for l in lines) else ""
    out = base + "profiles:\n" + "\n".join(managed) + "\n"
else:
    end = len(lines)
    for i in range(pidx+1, len(lines)):
        if lines[i] and not lines[i][0].isspace():
            end = i; break
    head, body, tail = lines[:pidx+1], lines[pidx+1:end], lines[end:]
    out_body, i = [], 0
    while i < len(body):
        m = re.match(r"^  ([A-Za-z0-9_-]+):\s*(#.*)?$", body[i])
        if m and m.group(1) in our:
            replaced.append(m.group(1)); i += 1
            while i < len(body) and (not body[i].strip() or body[i].startswith("   ")):
                i += 1
            continue
        out_body.append(body[i]); i += 1
    out = "\n".join(head + managed + out_body + tail).rstrip() + "\n"

open(target, "w", encoding="utf-8").write(out)
if replaced: print("  · 기존 동일이름 프로필 교체:", ", ".join(sorted(set(replaced))))
print(f"  · 프로필 {len(our)}종 병합 완료 →", target)
PY

# 4) 기본 프로필 설정 (config.yml). none 이면 건너뜀
if [ "$DEFAULT_PROFILE" != "none" ]; then
python3 - "$CONFIG" "$DEFAULT_PROFILE" <<'PY'
import sys, os, re
cfg, prof = sys.argv[1], sys.argv[2]
content = open(cfg, encoding="utf-8").read() if os.path.exists(cfg) else ""
lines = content.splitlines()
mi = next((i for i, l in enumerate(lines) if re.match(r"^modelProfile:\s*$", l)), None)
if mi is None:
    block = f"modelProfile:\n  default: {prof}"
    content = (content.rstrip() + "\n\n" + block + "\n") if content.strip() else (block + "\n")
else:
    j, found = mi+1, False
    while j < len(lines) and (lines[j].startswith("  ") or not lines[j].strip()):
        if re.match(r"\s+default:\s*", lines[j]):
            lines[j] = re.sub(r"(default:\s*).*", lambda m: m.group(1)+prof, lines[j]); found = True; break
        if lines[j].strip() and not lines[j].startswith("  "): break
        j += 1
    if not found: lines.insert(mi+1, f"  default: {prof}")
    content = "\n".join(lines) + "\n"
open(cfg, "w", encoding="utf-8").write(content)
print(f"  · 기본 프로필 = {prof} (config.yml)")
PY
fi

# 5) cyber-cop reviewer 도구 (opt-in: GJC_SETUP_COP=1) — clone 없이 `gjc-cop <PR>` 리뷰
if [ "${GJC_SETUP_COP:-0}" = "1" ]; then
  b "▶ cyber-cop reviewer 도구 설치 (GJC_SETUP_COP=1)"
  COP_HOME="$DIR/cyber-cop"
  BIN_DIR="${GJC_COP_BIN_DIR:-$HOME/.local/bin}"
  mkdir -p "$COP_HOME" "$BIN_DIR"
  cop_fetch() {  # $1=repo-relative path  $2=dest ; local dir via GJC_SETUP_SRC_DIR for testing
    if [ -n "${GJC_SETUP_SRC_DIR:-}" ]; then cp "$GJC_SETUP_SRC_DIR/$1" "$2"
    else command -v curl >/dev/null 2>&1 || die "curl 필요"; curl -fsSL "$REPO_RAW/$1" -o "$2" || die "다운로드 실패: $1"; fi
  }
  cop_fetch routing-rules.md             "$COP_HOME/routing-rules.md"
  cop_fetch scripts/cyber-cop-review.sh  "$COP_HOME/cyber-cop-review.sh"
  cop_fetch scripts/validate-profiles.py "$COP_HOME/validate-profiles.py"
  cop_fetch scripts/gjc-cop              "$COP_HOME/gjc-cop"
  chmod +x "$COP_HOME/cyber-cop-review.sh" "$COP_HOME/gjc-cop"
  ln -sf "$COP_HOME/gjc-cop" "$BIN_DIR/gjc-cop"   # idempotent PATH wrapper
  g "  · cyber-cop 배송 → $COP_HOME"
  g "  · 래퍼 → $BIN_DIR/gjc-cop  (사용: gjc-cop <PR> · gjc-cop --panel <PR> · gjc-cop shell · gjc-cop watch)"
  case ":$PATH:" in
    *":$BIN_DIR:"*) : ;;
    *) y "  ⚠ $BIN_DIR 가 PATH에 없습니다 — 셸 rc에 추가: export PATH=\"$BIN_DIR:\$PATH\"" ;;
  esac
  # 배송된 validator 는 PyYAML 필요 — 없으면 가이드 PR 리뷰의 invariants 가 항상 FAIL(fail-closed).
  if ! python3 -c "import yaml" >/dev/null 2>&1; then
    y "  ⚠ PyYAML 미설치 — 가이드 레포 PR 리뷰 시 invariants 단계가 실패합니다: pip3 install pyyaml"
  fi
fi
echo
g "✓ 설치 완료"
echo
b "설치된 프로필 ${PROFILE_COUNT}종"
ROSTER=""
for _n in $PROFILE_NAMES; do
  if [ "$_n" = "$DEFAULT_PROFILE" ]; then ROSTER="$ROSTER ★$_n"; else ROSTER="$ROSTER  $_n"; fi
done
echo " $ROSTER"
echo
b "다음 단계"
echo "  gjc --mpreset daily          # 이번 세션만 적용"
echo "  gjc --list-models daily      # 적용 확인 (세션 중 Ctrl+P 로 순환)"
echo
b "⚠ 프로바이더 인증 (필수 — 안 하면 'No API key')"
echo "  GJC를 켠 뒤 아래를 한 번씩(브라우저 OAuth):"
echo "    /login anthropic           # claude"
echo "    /login openai-codex        # gpt(base GPT: gpt-5.5/5.4)"
echo "    /login google-antigravity  # gemini (Google AI Pro/Ultra 구독)"
echo "    /login xai                 # grok 전체(grok-4.3 등)"
echo "  opencode-go 는 /provider add 또는 OPENCODE_API_KEY"
[ "$DEFAULT_PROFILE" != "none" ] && y "현재 기본 프로필이 '$DEFAULT_PROFILE' 로 설정됨 (config.yml). 새 세션부터 자동 적용."
echo
echo "  되돌리기: cp \"$TARGET.bak-$TS\" \"$TARGET\"   (백업본 존재 시)"
