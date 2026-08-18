#!/usr/bin/env python3
"""계획 수용기준 #5 — 퍼널 매트릭스 파싱 검증.

각 shipped 번들의 `required_providers` 가 README 퍼널 표의 **정확히 하나의 최소행**과
집합으로 동일해야 한다. 0개면 그 번들이 퍼널에서 빠진 것이고, 2개 이상이면 표가
중복 행을 가진 것이다(사용자가 어느 행을 봐야 할지 모른다).

`.github/workflows/validate.yml` 의 상시 CI 스텝이 호출하고, `check-v3-target-state.sh
--ship` 도 호출한다. 단독 실행도 된다.
출력: `OK …` 또는 `BAD …`로 시작한다. 종료코드는 성공 시 0, 실패 시 1이다.
검사 대상은 **네 언어 README 전부**다(KO 정본 + EN/ZH/JA 미러).
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


def _funnel_rows(readme):
    try:
        txt = readme.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"읽지 못함 ({exc})"

    # 펜스 코드블록 안의 `## 🧭 …` 는 헤딩이 아니라 샘플이다. 마스킹하지 않으면 그런
    # 샘플 하나가 헤딩 개수를 2로 만들어 **네 README 전부에서 CI 를 깨뜨린다**
    # (fail-closed 라 위험하진 않지만 링크 게이트가 이미 하는 일을 여기서 안 하면
    # 게이트끼리 규칙이 어긋난다 — 패널 지적).
    #
    # 정규식 역참조(`\1`)로 짝을 맞추면 **닫는 펜스 길이가 정확히 같아야만** 매칭된다.
    # CommonMark 은 `~~~~` 가 `~~~` 를 닫는 것을 허용하므로 그런 문서에서는 아무것도
    # 마스킹되지 않는다 — `slug-anchor-check.py` 는 `>=` 규칙을 쓴다. 두 게이트가
    # 마크다운을 다르게 읽으면 안 되므로(이 PR 이 `_has_banner` 에서 편 논리 그대로)
    # 같은 규칙을 줄 단위로 구현한다.
    masked, fence = [], None
    for line in txt.split("\n"):
        body = re.sub(r"^(?: {0,3}>[ \t]?)*", "", line)
        fm = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", body)
        cover = False
        if fence is None:
            if fm and (fm.group(1)[0] != "`" or "`" not in fm.group(2)):
                fence = (fm.group(1)[0], len(fm.group(1)))
                cover = True
        else:
            ch, width = fence
            if fm and fm.group(1)[0] == ch and len(fm.group(1)) >= width \
                    and not fm.group(2).strip():
                fence = None
            cover = True
        masked.append(" " * len(line) if cover else line)
    txt = "\n".join(masked)

    # 헤딩은 언어별로 다르므로 🧭 로 찾는다. 그런데 🧭 는 퍼널 절에만 있는 게 아니다 —
    # `## 2. 🧭 핵심 설계`(§2)도 같은 이모지를 쓴다. 예전 코드는 첫 매치를 집어서 우연히
    # 맞았을 뿐이고, 절 순서가 바뀌면 조용히 다른 절을 파싱했다(cyber-cop 패널 지적).
    #
    # 판별식: 퍼널 절은 **번호 없는** 절이다. §1~§11 은 전부 `## <숫자>.` 로 시작한다.
    # 번호 없는 🧭 헤딩이 정확히 하나여야 하고, 아니면 코드가 대상을 정할 수 없으니 BAD.
    # 헤딩 **매치 객체를 그대로 들고 간다.** 예전엔 `^## …$` 로 찾아놓고 그 문자열을
    # `re.search(re.escape(...))` 로 다시 찾았는데, 같은 문장이 앞쪽 펜스 샘플이나
    # 인용문에 있으면 그쪽이 먼저 걸려 파서가 엉뚱한 위치에서 시작한다(패널 지적).
    hits = [m for m in re.finditer(r"^## .*🧭.*$", txt, re.M)
            if not re.match(r"^## \d", m.group(0))]
    if len(hits) != 1:
        return None, f"번호 없는 퍼널 헤딩(🧭)이 {len(hits)}개 — 정확히 1개여야 한다"
    m = hits[0]
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
        elif started:
            # 표 블록은 `|` 아닌 첫 줄에서 끝난다. 표 중간에 주석줄(`<!-- -->`)이나 빈 줄을
            # 끼우면 그 뒤 행이 조용히 빠진다 — 지금 레이아웃엔 그런 게 없고, 행이 하나도
            # 안 잡히면 아래에서 BAD 로 떨어진다. 표 안에 뭘 끼우려면 이 조건을 먼저 봐라.
            break
    if not rows:
        return None, "퍼널 표에서 최소 credential 행을 찾지 못함"
    return rows, None


def _problems(profiles, rows):
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
    return problems


def main():
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else _default_root()

    data = yaml.safe_load((root / "gjc-profiles.yml").read_text(encoding="utf-8"))
    profiles = data.get("profiles") or data.get("model_profiles")
    if not isinstance(profiles, dict) or not profiles:
        print("BAD gjc-profiles.yml 에서 profiles 를 읽지 못함")
        return 1

    results = []
    failures = []
    for filename in ("README.md", "README.en.md", "README.zh.md", "README.ja.md"):
        rows, error = _funnel_rows(root / filename)
        if error:
            failures.append(f"{filename}: {error}")
            results.append(f"{filename} BAD")
            continue
        problems = _problems(profiles, rows)
        if problems:
            failures.append(f"{filename}: " + "; ".join(problems))
            results.append(f"{filename} BAD")
            continue
        total = sum(len(names) for _, names in rows)
        results.append(f"{filename} OK {len(rows)}행·{total}번들")

    if failures:
        # `results` 는 파일별 OK/BAD 한 줄 요약, `failures` 는 사유다. 예전엔 실패
        # 파일명이 양쪽에 다 찍혀 중복됐다 — 요약에서는 상태만, 사유에서만 이름을 쓴다.
        print("BAD " + " | ".join(results) + " || " + " | ".join(failures))
        return 1
    print(
        f"OK 퍼널 4개 README · {len(profiles)}번들 — " + " | ".join(results)
        + " · 각 번들이 정확히 한 최소행과 일치, 표의 번들 전부 로스터와 양방향 일치"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
