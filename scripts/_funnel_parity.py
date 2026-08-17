#!/usr/bin/env python3
"""계획 수용기준 #5 — 퍼널 매트릭스 파싱 검증.

각 shipped 번들의 `required_providers` 가 README 퍼널 표의 **정확히 하나의 최소행**과
집합으로 동일해야 한다. 0개면 그 번들이 퍼널에서 빠진 것이고, 2개 이상이면 표가
중복 행을 가진 것이다(사용자가 어느 행을 봐야 할지 모른다).

`check-v3-target-state.sh --ship` 이 호출한다. 단독 실행도 된다.
출력: `OK …` 또는 `BAD …` 한 줄. 종료코드는 항상 0(호출부가 문자열로 판정).
"""
import pathlib
import re
import subprocess
import sys

import yaml


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
    return pathlib.Path(top) if top else parent


def main():
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else _default_root()

    data = yaml.safe_load((root / "gjc-profiles.yml").read_text(encoding="utf-8"))
    profiles = data.get("profiles") or data.get("model_profiles")
    if not isinstance(profiles, dict) or not profiles:
        print("BAD gjc-profiles.yml 에서 profiles 를 읽지 못함")
        return 1

    txt = (root / "README.md").read_text(encoding="utf-8")
    m = re.search(r"^## .*어떤 번들을 쓸까.*$", txt, re.M)
    if not m:
        print("BAD README 에서 퍼널 절 헤딩을 찾지 못함")
        return 1
    seg = txt[m.end():]
    nxt = re.search(r"^## ", seg, re.M)
    if nxt:
        seg = seg[:nxt.start()]

    # 퍼널 절에는 표가 둘 이상 있다(최소조합 매트릭스 + "인증 방식" 표). 인증 표의 첫 행도
    # 같은 프로바이더 3종을 나열하므로, 절 전체를 긁으면 같은 집합이 2회 잡혀 오탐이 난다.
    # → **첫 번째 연속 표 블록만** 읽는다.
    rows = []
    started = False
    for line in seg.split("\n"):
        if line.startswith("|"):
            started = True
            if "---" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            provs = set(re.findall(r"`([a-z0-9-]+)`", cells[0]))
            if provs:
                # 오른쪽 열도 읽는다. 예전엔 provider 집합만 봤고 "쓸 수 있는 번들" 열은
                # 아예 파싱하지 않았다 — 번들이 빠지거나 엉뚱한 행에 실려도 통과했다
                # (cyber-cop 패널 지적). 계약의 절반을 검사하지 않은 것이다.
                names = set(re.findall(r"\*\*([a-z0-9-]+)\*\*", cells[1] if len(cells) > 1 else ""))
                rows.append((provs, names))
        elif started and line.strip() == "":
            break          # 첫 표 블록이 끝났다
    if not rows:
        print("BAD 퍼널 표에서 최소 credential 행을 찾지 못함")
        return 1

    problems = []
    for name, spec in profiles.items():
        req = set((spec or {}).get("required_providers") or [])
        if not req:
            problems.append(f"{name}: required_providers 없음")
            continue
        set_hits = [provs for provs, _ in rows if provs == req]
        if len(set_hits) != 1:
            problems.append(f"{name}: {sorted(req)} 와 집합 동일한 행이 {len(set_hits)}개")
        # 번들이 실제로 그 행에 실려 있는가
        listed = [provs for provs, names in rows if name in names]
        if len(listed) != 1:
            problems.append(f"{name}: 퍼널 표에 실린 행이 {len(listed)}개 (정확히 1개여야 한다)")
        elif listed[0] != req:
            problems.append(
                f"{name}: 실린 행의 조합 {sorted(listed[0])} != required_providers {sorted(req)}"
            )

    # 반대 방향 — 표에만 있고 로스터에 없는 이름(삭제된 번들 잔존)
    for provs, names in rows:
        for ghost in sorted(names - set(profiles)):
            problems.append(f"{ghost}: 퍼널 표에 있으나 로스터에 없음 ({sorted(provs)})")

    if problems:
        print("BAD " + " | ".join(problems))
        return 1
    total = sum(len(names) for _, names in rows)
    print(
        f"OK 퍼널 {len(rows)}행 · {len(profiles)}번들 — 각 번들이 정확히 한 최소행과 일치, "
        f"표에 실린 번들 {total}개 전부 로스터와 양방향 일치"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
