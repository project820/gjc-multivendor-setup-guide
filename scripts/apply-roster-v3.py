#!/usr/bin/env python3
"""승인 계획의 v3 로스터 축소를 `gjc-profiles.yml` 에 적용한다.

**결정이 끝난 부분만 한다.**
  - `dream-team` · `eco` · `ultimate-sol` 프로필 블록 제거 (계획 DROP 중 실출하분)
  - `--with-budget` 을 줄 때만 budget 블록 삽입 (게이트 3조건 충족 시)
  - `daily.executor` → `openai-codex/gpt-5.6-luna:max` 교체

**하지 않는 것 — 의도적이다:**
  - **2026-08-17 갱신**: `daily.executor` 는 이제 **바꾼다**. 사용자가 결정표 #1 을
    `"luna 는 max 만 허용한다"` 로 확정했다. 그 전까지 이 스크립트는 좌석을 일부러
    건드리지 않았다(배터리 FAIL + R8 잠금 때문에 코드가 미승인 결정을 대신 내리면 안 됐다).
    같은 결정으로 `apply-validator-v3.py` 의 D-1 합법 effort 도 `{max}` 단독으로 좁혔다 —
    둘은 **같은 커밋**에 담아야 한다(좌석만 바꾸고 룰을 안 바꾸면 구 validator 가 거부한다).
  - validator 개정 — `apply-validator-v3.py` 가 한다. 둘을 **같은 커밋**에 담아야 한다
    (D-3 를 로스터 축소보다 먼저 적용하면 `ERROR [ultimate-sol]` 로 깨진다).

**왜 3개만 지우나 — 계획은 "DROP 6" 이라고 적혀 있다:**
  계획 line 32 의 DROP 6 은 `eco` · `dream-team` · `ultimate-sol` · `trio` ·
  `luna-scale` · `research-long` 이다. 그런데 뒤의 **3개는 v2.1.0 에 존재한 적이 없다**
  — 2026-08-17 실측으로 `gjc-profiles.yml` 0건, `git log -S` 커밋이력도 0건이다.
  계획의 DROP 목록은 *원안(스펙 후보) 로스터* 기준이라 출하된 적 없는 후보까지
  포함한다. 실제 YAML 에서 지울 수 있는 건 **실출하 3개뿐**이고, 그래서
  `10 → 7` 이 된다(계획 line 30 "출하 로스터 7", line 184 "4b → 7(또는 8)번들" 과 일치).

  **"6개를 지워야 하는데 3개만 지워졌다" 고 판단해 추가 삭제하지 마라.** 남은 7개는
  전부 계획이 존치하기로 한 것이다. 같은 혼동이 릴리스노트에서도 한 번 났다 —
  `whats-new-v3.md` 초안이 저 3개를 "삭제된 번들" 로 공지할 뻔했다(정정 완료).

fail-closed: 지울 프로필이 없거나 이미 지워졌으면 중단한다. 텍스트 블록 단위로
자르되, 작업 후 YAML 을 다시 파싱해 **기대한 로스터가 정확히 나왔는지** 검증한다.

사용:
  python3 scripts/apply-roster-v3.py --check                 # 판정만, 파일 미변경
  python3 scripts/apply-roster-v3.py                         # 7번들
  python3 scripts/apply-roster-v3.py --with-budget           # 7 + budget
종료코드: 0 성공 / 1 실패
"""
import argparse
import pathlib
import re
import subprocess
import sys

import yaml

DROP = ["dream-team", "eco", "ultimate-sol"]
KEEP = ["daily", "coding-sprint", "cyber-cop", "ultimate-opus", "escalation", "llm-council", "monorepo"]

# 사용자 결정 2026-08-17: "luna 는 max 만 허용한다" → daily.executor 좌석 확정.
LUNA_SEAT_TO = "openai-codex/gpt-5.6-luna:max"

BUDGET_BLOCK = """
  budget:                              # v3 게이트 — 구독 없이 저가 API 만으로 5역할
    required_providers: [openai-codex, google-antigravity, opencode-go]
    model_mapping:
      default:   openai-codex/gpt-5.6-terra:medium
      executor:  opencode-go/glm-5.2
      planner:   opencode-go/qwen3.8-max
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    google-antigravity/gemini-3.1-pro-low:high
"""

_KEY = re.compile(r"^  ([A-Za-z0-9_-]+):\s*(#.*)?$")


def _default_root():
    parent = pathlib.Path(__file__).resolve().parent.parent
    if (parent / "gjc-profiles.yml").exists():
        return parent
    try:
        top = subprocess.run(
            ["git", "-C", str(pathlib.Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return parent
    if not top:
        return parent
    print(f"note: repo root resolved via git → {top}", file=sys.stderr)
    return pathlib.Path(top)


def _roster(text):
    data = yaml.safe_load(text)
    profiles = data.get("profiles") or data.get("model_profiles")
    if not isinstance(profiles, dict) or not profiles:
        sys.exit("apply-roster-v3: 'profiles' 매핑을 찾지 못했다")
    return profiles


def main():
    ap = argparse.ArgumentParser(description="apply v3 roster reduction")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--with-budget", action="store_true",
                    help="게이트 3조건 충족을 확인한 뒤에만 쓴다")
    args = ap.parse_args()
    root = pathlib.Path(args.root) if args.root else _default_root()

    path = root / "gjc-profiles.yml"
    if not path.exists():
        sys.exit(f"apply-roster-v3: {path} not found")
    src = path.read_text(encoding="utf-8")
    before = _roster(src)

    missing = [n for n in DROP if n not in before]
    if missing:
        sys.exit(f"apply-roster-v3: 지울 프로필이 이미 없다 {missing} — 중복 적용이거나 예상과 다른 트리다")
    absent_keep = [n for n in KEEP if n not in before]
    if absent_keep:
        sys.exit(f"apply-roster-v3: 남겨야 할 프로필이 없다 {absent_keep} — 예상과 다른 트리다")
    if "budget" in before:
        sys.exit("apply-roster-v3: budget 이 이미 있다 — 중복 적용")

    # 프로필 블록 제거 (2칸 들여쓰기 키 기준)
    out, skip = [], False
    for line in src.split("\n"):
        m = _KEY.match(line)
        if m:
            skip = m.group(1) in DROP
        elif skip and (line.startswith("  ") or line.strip() == ""):
            pass
        elif skip:
            skip = False
        if not skip:
            out.append(line)
    text = "\n".join(out)

    # daily.executor → Luna :max  (사용자 결정 2026-08-17: "luna 는 max 만 허용한다")
    # 같은 셀렉터가 다른 번들에도 있으므로 **번들 인식**으로 바꾼다 —
    # 첫 등장 치환은 daily 가 파일 첫 번들이라는 가정에 의존해서 취약하다.
    lines, cur, hit = text.split("\n"), None, 0
    for i, line in enumerate(lines):
        m = _KEY.match(line)
        if m:
            cur = m.group(1)
            continue
        if cur == "daily" and re.match(r'^\s+executor:\s', line):
            new = re.sub(r'(^\s+executor:\s+)\S+', r'\1' + LUNA_SEAT_TO, line, count=1)
            if new != line:
                lines[i], hit = new, hit + 1
    if hit != 1:
        sys.exit(f"apply-roster-v3: daily.executor 줄을 정확히 1개 찾지 못했다 (found {hit})")
    text = "\n".join(lines)

    if args.with_budget:
        marker = "\n# ─────"
        try:
            i = text.index(marker, text.index("  monorepo:"))
        except ValueError:
            sys.exit("apply-roster-v3: budget 삽입 지점(monorepo 뒤 구분선)을 찾지 못했다")
        text = text[:i] + BUDGET_BLOCK + text[i:]

    after = _roster(text)
    expected = set(KEEP) | ({"budget"} if args.with_budget else set())
    if set(after) != expected:
        sys.exit(f"apply-roster-v3: 결과 로스터가 기대와 다르다\n  기대: {sorted(expected)}\n  실제: {sorted(after)}")

    # daily.executor 는 Luna :max 여야 한다 (사용자 결정)
    got = after["daily"]["model_mapping"]["executor"]
    if got != "openai-codex/gpt-5.6-luna:max":
        sys.exit(f"apply-roster-v3: daily.executor 가 기대와 다르다 — got {got}")

    print(f"로스터 {len(before)} → {len(after)}: {sorted(after)}")
    print(f"daily.executor: {before['daily']['model_mapping']['executor']} → {got}")
    if args.check:
        print("OK — 적용 가능(파일 미변경).")
        return 0

    path.write_text(text, encoding="utf-8")
    print(f"OK — 적용 완료: {path}")
    print("다음(같은 커밋에서): python3 scripts/apply-validator-v3.py")
    print("                    python3 scripts/sync-readme-yaml.py && python3 scripts/gen_svgs.py")
    print("                    python3 scripts/validate-profiles.py && bash scripts/ci-fixture-check.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
