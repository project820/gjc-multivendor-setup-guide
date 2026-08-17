#!/usr/bin/env python3
"""docs/factsheet.md §2 번들×좌석 표가 gjc-profiles.yml 과 일치하는지 검사.

**이 스크립트는 승인 계획에 없다 — 제안이다.** 채택 여부는 사람이 정한다.
`.gjc/v3-pending-scripts/README.md` 의 "제안 (계획 외)" 절을 볼 것.

왜 만들었나:
  동기화 표면 중 `gjc-profiles.yml` → README 임베드는 validator 6번 체크가,
  → SVG 는 `gen_svgs.py` 의 fail-closed 가, → revalidate 로스터는 파생이 지킨다.
  `docs/factsheet.md` §2 만 **아무 자동 가드가 없다.** v2.0.1 때 파생 표면이 정본과
  조용히 어긋나 공개 문서가 반대로 말한 사고가 있었고, factsheet 는 그 사고가
  났던 종류의 수동 표면이다.

무엇을 비교하나:
  번들 집합(양방향)과 5역할 좌석 셀. factsheet 는 축약 표기(`Opus5:high`)를 쓰므로
  모델 토큰과 effort 토큰이 셀에 들어있는지로 대조한다. 각주 위첨자(¹²³…)와
  백틱은 비교 전에 제거한다 — 표기용이지 내용이 아니다.

사용:
  python3 scripts/check-factsheet-parity.py            # repo 루트 자동 판별
  python3 scripts/check-factsheet-parity.py --root DIR # 다른 트리
종료코드: 0 일치 / 1 불일치 또는 구조 오류
"""
import argparse
import pathlib
import re
import subprocess
import sys

import yaml

_ROLES = ["default", "executor", "planner", "architect", "critic"]
_SUPERSCRIPT = "¹²³⁴⁵⁶⁷⁸⁹⁰"

# 정본 모델 id → factsheet 축약 토큰. 모르는 모델은 아래 _token() 이 fail-closed 한다.
_MODEL_TOKEN = {
    "claude-opus-5": "opus5",
    "claude-sonnet-5": "sonnet5",
    "claude-fable-5": "fable",
    "gpt-5.6-terra": "terra",
    "gpt-5.6-sol": "sol",
    "gpt-5.6-luna": "luna",
    "grok-4.6": "grok4.6",
    "glm-5.2": "glm-5.2",
    # v3 신규 — budget.planner 좌석. 2026-08-17: 이 엔트리가 없으면 가드가
    # `unknown model 'qwen3.8-max' — add it to _MODEL_TOKEN` 로 **fail-closed** 한다
    # (시뮬레이션 릴리스 트리에서 실측). gen_svgs.py 의 `_MODEL_DISPLAY` 와 같은 계열의
    # 하드코딩 테이블이고, v3 로스터에 모델이 추가되면 **두 곳을 같이** 고쳐야 한다.
    "qwen3.8-max": "qwen3.8max",
}
_EFFORT_TOKEN = {
    "minimal": "min",
    "low": "low",
    "medium": "med",
    "high": "high",
    "xhigh": "xhigh",
    "max": "max",
}


def _default_root():
    """scripts/ 에 있으면 상위가 루트. 대기 위치면 git 최상위로 되짚는다."""
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


def _clean(cell):
    return "".join(ch for ch in cell if ch not in _SUPERSCRIPT).replace("`", "").strip()


def _token(model):
    tok = _MODEL_TOKEN.get(model)
    if tok is not None:
        return tok
    if "gemini" in model:
        return "gemini"
    sys.exit(f"check-factsheet-parity: unknown model {model!r} — add it to _MODEL_TOKEN")


def _profiles(root):
    path = root / "gjc-profiles.yml"
    if not path.exists():
        sys.exit(f"check-factsheet-parity: {path} not found")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    profiles = data.get("profiles") or data.get("model_profiles")
    if not isinstance(profiles, dict) or not profiles:
        sys.exit(f"check-factsheet-parity: {path} has no usable 'profiles' mapping")
    for name, spec in profiles.items():
        mapping = (spec or {}).get("model_mapping")
        if not isinstance(mapping, dict):
            sys.exit(f"check-factsheet-parity: profile {name!r} has no model_mapping")
        missing = [r for r in _ROLES if r not in mapping]
        if missing:
            sys.exit(f"check-factsheet-parity: profile {name!r} is missing roles {missing}")
    return profiles


def _table(root):
    path = root / "docs" / "factsheet.md"
    if not path.exists():
        sys.exit(f"check-factsheet-parity: {path} not found")
    text = path.read_text(encoding="utf-8")
    parts = text.split("## 2. 번들 × 좌석")
    if len(parts) != 2:
        sys.exit("check-factsheet-parity: '## 2. 번들 × 좌석' section not found in docs/factsheet.md")
    section = parts[1].split("\n## ")[0]
    rows = [l for l in section.split("\n") if l.startswith("|") and "---" not in l]
    if len(rows) < 2:
        sys.exit("check-factsheet-parity: §2 has no bundle rows")
    out = {}
    for line in rows[1:]:                       # rows[0] 은 헤더
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 1 + len(_ROLES):
            sys.exit(f"check-factsheet-parity: malformed §2 row: {line}")
        name = re.sub(r"^[^\w]*", "", cells[0]).strip()   # 선두 이모지 제거
        out[name] = [_clean(c) for c in cells[1:1 + len(_ROLES)]]
    return out


def main():
    ap = argparse.ArgumentParser(description="docs/factsheet.md §2 ↔ gjc-profiles.yml parity")
    ap.add_argument("--root", default=None)
    args = ap.parse_args()
    root = pathlib.Path(args.root) if args.root else _default_root()

    profiles = _profiles(root)
    table = _table(root)

    problems = []
    only_yaml = sorted(set(profiles) - set(table))
    only_table = sorted(set(table) - set(profiles))
    if only_yaml:
        problems.append(f"gjc-profiles.yml 에 있는데 factsheet §2 에 없는 번들: {only_yaml}")
    if only_table:
        problems.append(f"factsheet §2 에 있는데 gjc-profiles.yml 에 없는 번들: {only_table}")

    checked = 0
    for name in sorted(set(profiles) & set(table)):
        mapping = profiles[name]["model_mapping"]
        for role, cell in zip(_ROLES, table[name]):
            selector = mapping[role]
            _, _, rest = selector.partition("/")
            model, _, effort = rest.partition(":")
            checked += 1
            low = cell.lower()
            token = _token(model)
            ok = (token in low) if token != "gemini" else ("gemini" in low)
            if effort:
                want = _EFFORT_TOKEN.get(effort, effort)
                ok = ok and re.search(re.escape(want) + r"(?![a-z])", low) is not None
            if not ok:
                problems.append(f"[{name}.{role}] yaml={selector}  factsheet={cell!r}")

    if problems:
        print(f"FAIL — factsheet §2 drift ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"OK — factsheet §2 matches gjc-profiles.yml ({len(table)} bundles, {checked} seat cells)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
