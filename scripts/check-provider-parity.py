#!/usr/bin/env python3
"""README 임베드 블록의 required_providers 가 gjc-profiles.yml 과 일치하는지 검사.

왜 별도 스크립트인가:
  validate-profiles.py 의 6번 체크는 README 임베드 YAML 과 정본을 비교하지만
  `model_mapping` 만 본다. `required_providers` 가 어긋나도 통과한다.
  v2.1.0 리뷰에서 파생 표면이 정본과 조용히 어긋나는 사고가 실제로 났으므로
  이 축도 fail-closed 로 막는다.

사용:
  python3 scripts/check-provider-parity.py            # repo 루트 자동 판별
  python3 scripts/check-provider-parity.py --root DIR # 다른 트리
  (아직 scripts/ 로 옮기기 전에는 대기 위치에서 그대로 실행해도 된다)
종료코드: 0 일치 / 1 불일치 또는 구조 오류
"""
import argparse
import pathlib
import re
import subprocess
import sys

import yaml

_BLOCK = re.compile(r"```yaml\s*\n(.*?)```", re.S)


def _profiles(data, where):
    p = data.get("profiles") or data.get("model_profiles")
    if not isinstance(p, dict) or not p:
        sys.exit(f"check-provider-parity: {where} has no usable 'profiles' mapping")
    return p


def _providers(profiles, where):
    out = {}
    for name, spec in profiles.items():
        rp = (spec or {}).get("required_providers")
        if not isinstance(rp, list) or not rp:
            sys.exit(f"check-provider-parity: {where} profile {name!r} has no required_providers")
        out[name] = sorted(rp)
    return out


def _from_readme(path):
    """README 안의 첫 profiles 블록에서 required_providers 를 뽑는다."""
    text = path.read_text(encoding="utf-8")
    for m in _BLOCK.finditer(text):
        try:
            data = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and (data.get("profiles") or data.get("model_profiles")):
            return _providers(_profiles(data, str(path)), str(path))
    return None


def _default_root():
    """스크립트가 scripts/ 에 있으면 상위가 곧 루트다. 아직 대기 위치(.gjc/v3-pending-scripts/)에
    있으면 상위에 gjc-profiles.yml 이 없으므로 git 최상위로 되짚는다."""
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
    # 되짚은 경우 어느 트리를 검사하는지 보이게 한다 — 저장소 안에 만든 임시 복사본에서
    # 돌리면 조용히 실제 트리로 새어나가 오탐(false pass)이 날 수 있다.
    print(f"note: repo root resolved via git → {top}", file=sys.stderr)
    return pathlib.Path(top)


def main():
    ap = argparse.ArgumentParser(description="README required_providers parity check")
    ap.add_argument("--root", default=None)
    args = ap.parse_args()
    root = pathlib.Path(args.root) if args.root else _default_root()

    canonical_path = root / "gjc-profiles.yml"
    if not canonical_path.exists():
        sys.exit(f"check-provider-parity: {canonical_path} not found")
    canonical = _providers(
        _profiles(yaml.safe_load(canonical_path.read_text(encoding="utf-8")), str(canonical_path)),
        str(canonical_path),
    )

    readmes = sorted(root.glob("README*.md"))
    if not readmes:
        sys.exit("check-provider-parity: no README*.md found")

    # 지정된 네 README 는 전부 임베드 블록을 가져야 한다. 하나가 통째로 사라져도
    # "나머지가 일치하니 OK" 로 통과하면 안 된다 — 그게 정확히 이 스크립트가 막으려는
    # 드리프트다. 없으면 fail-closed.
    required = ["README.md", "README.en.md", "README.zh.md", "README.ja.md"]
    missing_files = [n for n in required if not (root / n).exists()]
    if missing_files:
        print(f"FAIL — expected README files are missing: {missing_files}")
        return 1

    failures = []
    checked = 0
    for r in readmes:
        embedded = _from_readme(r)
        if embedded is None:
            if r.name in required:
                failures.append(f"{r.name}: no embedded ```yaml profiles block found")
                checked += 1
            continue  # 그 외 README 변형은 대상 아님
        checked += 1
        for name in sorted(set(canonical) | set(embedded)):
            want = canonical.get(name)
            got = embedded.get(name)
            if want != got:
                failures.append(f"{r.name}: {name}: canonical={want} embedded={got}")

    if checked < len(required):
        print(f"FAIL — only {checked} of {len(required)} required READMEs were checked")
        return 1

    if failures:
        print(f"FAIL — required_providers drift in {len(failures)} place(s):")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"OK — required_providers match across {checked} README file(s), "
          f"{len(canonical)} profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
