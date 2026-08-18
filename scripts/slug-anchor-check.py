#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""링크 무결성 검사 — 파일 생존 + 앵커 슬러그. 예전 헤딩 → GitHub 앵커 슬러그 계산 + 문서 내 링크와 대조.

왜 필요한가
-----------
v3 는 `## 5.` 제목의 번들 개수를 바꾼다. 그 순간 GitHub 슬러그가 바뀌어 문서 안의
앵커 링크가 **에러 없이 조용히** 죽는다(2026-08-17 실측: KO 4 · EN 1 · JA 3 · ZH 3 = 11개).
손으로 새 슬러그를 적으면 틀린다 — `🗂️` 의 variation selector(U+FE0F)가 **살아남기**
때문에 슬러그에 `-️-` 가 들어간다. 이 도구로 계산해서 넣어라.

사용법
------
    python3 slug-anchor-check.py            # README 4종
    python3 slug-anchor-check.py --all      # 전수 .md (파일간 링크·퍼센트 인코딩 포함)
    python3 slug-anchor-check.py --heading '## 5. 🗂️ 최종 카탈로그 · 4계층'
종료코드: 0 = 모든 링크가 실재 헤딩을 가리킨다 / 1 = 죽은 링크 발견
"""
from __future__ import print_function
import argparse, os, re, sys, urllib.parse

READMES = ["README.md", "README.en.md", "README.ja.md", "README.zh.md"]


# reference-style 정의의 대상이 **정말 링크인지** 판정한다. `[주의]: 이건 산문이다.`
# 같은 줄을 링크로 읽으면 없는 파일로 오탐한다 — `--all` 이 evidence/·docs/ 전체를
# 훑으므로 실재하는 위험이다. 판정은 ASCII 경로/URL 모양으로만 한다(유니코드 `\w` 를
# 쓰면 한글 문장이 경로처럼 매칭된다).
_TARGET_RE = re.compile(r"^[A-Za-z0-9._~%+/#?=&:@-]+$")


def _mask_code_spans(text):
    """인라인 코드 스팬 내부를 같은 길이의 공백으로 덮는다(오프셋·줄번호 보존).

    CommonMark: N개 백틱으로 열면 **정확히 N개** 백틱 런이 닫는다. 줄바꿈은 그대로 둔다.
    """
    out = list(text)
    i, n = 0, len(text)
    while i < n:
        if text[i] != "`":
            i += 1
            continue
        j = i
        while j < n and text[j] == "`":
            j += 1
        run = j - i
        k = j
        while k < n:
            if text[k] == "`":
                e = k
                while e < n and text[e] == "`":
                    e += 1
                if e - k == run:
                    for p in range(i, e):
                        if out[p] != "\n":
                            out[p] = " "
                    i = e
                    break
                k = e
            else:
                k += 1
        else:
            i = j          # 닫는 런이 없다 — 코드 스팬이 아니다
    return "".join(out)


def _looks_like_target(raw):
    if not raw or not _TARGET_RE.match(raw):
        return False
    if raw.startswith(("http://", "https://", "mailto:", "#", "/", "./", "../")):
        return True
    # 확장자나 경로 구분자가 있어야 파일 참조로 본다
    return "/" in raw or re.search(r"\.[A-Za-z0-9]{1,8}(#|$)", raw) is not None


def slug(heading):
    t = heading.lstrip("#").strip().lower()
    out = []
    for ch in t:
        # U+FE0F(variation selector-16)는 GitHub 슬러그에서 **살아남는다**. 이 한 글자는
        # 반드시 이스케이프로 둔다 — 리터럴로 쓰면 diff 에서 보이지 않아 리뷰가 불가능하고,
        # 에디터·정규화기가 지우면 조건이 `ch == ""`(항상 False)로 바뀌어 모든 이모지 헤딩의
        # 슬러그가 조용히 달라진다. 테스트도 안 깨진다(cyber-cop 패널 지적).
        if ch.isalnum() or ch in "-_" or ch == "\ufe0f":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "#" + "".join(out)


def find_root(explicit=None):
    if explicit:
        return os.path.abspath(explicit)
    cur = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.exists(os.path.join(cur, "gjc-profiles.yml")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.getcwd()
        cur = parent


def collect_headings(root):
    """전수 .md 파일 → {상대경로: {슬러그, …}}"""
    table = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".gjc", "node_modules")]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                txt = open(full, encoding="utf-8").read()
            except Exception:
                continue
            table[rel] = {slug(l) for l in txt.split("\n") if l.startswith("#")}
    return table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--heading", default=None, help="이 헤딩의 슬러그만 계산하고 종료")
    ap.add_argument("--all", action="store_true",
                    help="README 4종이 아니라 전수 .md 를 검사(파일간 링크 포함)")
    args = ap.parse_args()

    if args.heading:
        print(slug(args.heading))
        return 0

    root = find_root(args.root)
    if not os.path.exists(os.path.join(root, "gjc-profiles.yml")):
        print("FAIL — gjc-profiles.yml 없는 트리다: %s" % root)
        return 1

    headings = collect_headings(root)
    scope = sorted(headings) if args.all else [f for f in READMES if f in headings]
    dead = []

    for name in scope:
        path = os.path.join(root, name)
        txt = open(path, encoding="utf-8").read()
        # 펜스 코드블록은 링크가 아니다. README 는 임베드 YAML 을, docs 는 HTML/markdown
        # 샘플을 펜스에 담는다 — 그 안의 상대 href 를 죽은 링크로 잡으면 CI 가 링크가
        # 아닌 것 때문에 실패한다. 오프셋을 보존해야 리포트의 줄번호가 맞으므로,
        # 펜스 구간은 지우지 말고 **같은 길이의 공백으로 덮는다.**
        #
        # 펜스 판정은 CommonMark 를 그대로 쓴다. 대충 "줄 앞이 ``` 이면 펜스" 로 잡으면
        # **산문이 펜스를 연다.** 실측: 이 레포 CHANGELOG 가 백틱 런을 문장 안에서
        # 이야기하는 순간 그 아래 링크가 통째로 미검사가 됐다(파일 링크 1 → 0).
        # 게이트가 조용히 fail-open 된 것이라 오탐보다 훨씬 나쁘다.
        #
        #   - 여는 펜스: 들여쓰기 ≤3 + ```/~~~ 3개 이상.
        #     백틱 펜스는 **info string 에 백틱이 있으면 펜스가 아니다**(CommonMark 규칙).
        #     위 CHANGELOG 문장이 정확히 이 경우다.
        #   - 닫는 펜스: 같은 문자 · 같은 길이 이상 + 뒤에 공백 말고 아무것도 없어야 한다.
        #
        # 안 맞으면 마스킹을 **덜** 하는 쪽으로 틀린다 — 오탐(시끄럽고 안전)이지
        # 미검사(조용하고 위험)가 아니다.
        #
        # ⚠ **들여쓰기 코드블록은 다루지 않는다.** 한때 `indent >= 4` 를 코드로 보고
        # 덮었는데, 이 문서들의 3단계 불릿과 리스트 안 문단 이어가기가 전부 4칸을 넘어서
        # **정상 링크가 통째로 검사에서 빠졌다** — 같은 fail-open 이다.
        scan = list(txt)
        fence = None          # (문자, 길이) — 열려 있으면 튜플
        fence_at = 0          # 열린 펜스의 시작 오프셋(미닫힘 리포트용)
        pos = 0
        for line in txt.splitlines(keepends=True):
            # blockquote 마커만 걷어낸다. **들여쓰기는 보존해야 한다** — 예전엔
            # `^[ \t]*` 로 앞 공백을 통째로 지운 뒤 ` {0,3}` 로 폭을 제한했는데, 그러면
            # 그 제한이 죽은 코드가 된다. 4칸 이상 들여쓴 ``` (CommonMark 상 들여쓰기
            # 코드블록의 *내용*)이 펜스를 열고, 닫히지 않으면 EOF 까지 마스킹돼
            # 링크가 조용히 미검사가 된다 — 이 PR 이 없앤 fail-open 이 한 줄 옆으로
            # 옮겨간 꼴이다(패널 지적). blockquote 마커 앞 공백만 CommonMark 대로 ≤3 허용.
            body = re.sub(r"^(?: {0,3}>[ \t]?)*", "", line)
            fm = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", body.rstrip("\n"))
            opener = closer = None
            if fm:
                run, rest = fm.group(1), fm.group(2)
                if fence is None:
                    if run[0] != "`" or "`" not in rest:
                        opener = (run[0], len(run))
                else:
                    ch, width = fence
                    if run[0] == ch and len(run) >= width and not rest.strip():
                        closer = True
            covered = False
            if fence is None:
                if opener:
                    fence = opener
                    fence_at = pos
                    covered = True
            else:
                if closer:
                    fence = None
                covered = True
            if covered:
                for k in range(pos, pos + len(line)):
                    if scan[k] != "\n":
                        scan[k] = " "
            pos += len(line)
        # 펜스가 EOF 까지 안 닫혔으면 그 뒤 줄이 전부 마스킹된 것이다 — 링크가 조용히
        # 미검사가 된 상태다. 카운터는 사람 눈으로 보는 완화책이지 게이트가 아니므로
        # (패널 지적) **여기서 죽인다.** 닫는 펜스가 4칸 이상 들여쓰여 있으면 이 경우가 된다.
        if fence is not None:
            dead.append("%s:%d → (열린 채 끝난 %s 펜스) : 이 줄 뒤 링크가 전부 마스킹됐다"
                        % (name, txt.count("\n", 0, fence_at) + 1, fence[0] * fence[1]))
        # 인라인 코드 스팬(`` `…` ``)도 링크가 아니다. 문서가 링크 **문법 자체**를
        # 이야기할 때 백틱 안에 `](…)` 를 쓰는데, 마스킹하지 않으면 그걸 진짜 링크로
        # 읽고 "대상 파일 없음" 오탐을 낸다.
        # 스팬 짝짓기는 **한 줄 안에서만** 한다 — 파일 전체에서 짝을 찾으면 짝 없는 런
        # 하나가 다음 같은 길이 런까지의 모든 링크를 조용히 지운다(패널 지적).
        # 줄을 넘어가는 스팬은 못 잡지만, 그건 오탐 방향이라 안전하다.
        scan = "\n".join(_mask_code_spans(l) for l in "".join(scan).split("\n"))
        matches = [(m.group(1), m.start(1))
                   for m in re.finditer(r"\]\(([^)\s]+)\)", scan)]
        # 로컬 HTML: `<a href>` 뿐 아니라 `<img src>` 도 본다. README ×4 의 17행이
        # `<img src="assets/role-winners.svg">` 로 배너를 문다 — src 가 깨져도 예전
        # "링크 무결성" 게이트는 통과했다(cyber-cop critic 지적).
        # 따옴표 없는 속성(`<img src=a.svg>`)도 유효한 HTML 이다. 따옴표를 강제하면
        # 그런 깨진 참조가 게이트를 그냥 통과한다(패널 지적).
        matches += [(m.group(2) or m.group(3), m.start(2) if m.group(2) else m.start(3))
                    for m in re.finditer(
                        r"""<(?:a\b[^>]*\bhref|img\b[^>]*\bsrc)\s*=\s*"""
                        r"""(?:(["'])(.*?)\1|([^\s"'>]+))""",
                        scan, re.IGNORECASE)]
        # reference-style 정의. 두 가지를 조심한다(패널 지적):
        #   1. `[x]: <./docs/a.md>` 의 꺾쇠는 **대상에 포함되지 않는다** — 포함하면
        #      `<./docs/a.md` 라는 없는 파일로 오탐한다.
        #   2. `[주의]: 이건 산문이다.` 같은 줄을 링크로 읽으면 안 된다. Python `\w` 는
        #      유니코드라서 한글 문장도 경로처럼 매칭된다 — 그래서 대상 판정은 정규식이
        #      아니라 아래 `_looks_like_target()` 이 **ASCII 경로/URL 모양**으로 한다.
        for m in re.finditer(r"^\[[^\]]+\]:[ \t]*<([^>\s]+)>|^\[[^\]]+\]:[ \t]*(\S+)",
                             scan, re.MULTILINE):
            raw = m.group(1) or m.group(2)
            start = m.start(1) if m.group(1) else m.start(2)
            if _looks_like_target(raw):
                matches.append((raw, start))
        links = [raw for raw, _ in matches]
        intra = cross = bad = 0
        for raw, position in matches:
            if raw.startswith(("http://", "https://", "mailto:")):
                continue
            if "#" in raw:
                target, frag = raw.split("#", 1)
                frag = "#" + urllib.parse.unquote(frag)
            else:
                target, frag = raw, None
            if target in ("", "."):
                owner = name
                intra += 1
            else:
                owner = os.path.normpath(
                    os.path.join(os.path.dirname(name), urllib.parse.unquote(target)))
                cross += 1
            if owner not in headings:
                # md 가 아니면 앵커는 못 보지만 **파일 생존**은 본다.
                if not os.path.exists(os.path.join(root, owner)):
                    bad += 1
                    dead.append("%s:%d → %s : 대상 파일 없음 (등장 %d회)"
                                % (name, txt.count("\n", 0, position) + 1, owner,
                                   links.count(raw)))
                continue
            if frag is None:
                continue          # 파일만 가리키는 링크 — 생존 확인으로 끝
            if frag not in headings[owner]:
                bad += 1
                dead.append("%s:%d → %s%s : 대상 헤딩 없음 (등장 %d회%s)"
                            % (name, txt.count("\n", 0, position) + 1, owner, frag,
                               links.count(raw),
                               ", 퍼센트 인코딩" if "%" in raw else ""))
        # 마스킹된 링크 모양 개수를 같이 찍는다. 마스킹이 과하게 먹으면 검사 건수만
        # 조용히 줄어드는데, 그 숫자를 아무도 diff 하지 않는다 — 마스킹 건수를 옆에
        # 두면 "왜 갑자기 안 세지?" 를 눈으로 잡을 수 있다(패널 제안).
        masked = len(re.findall(r"\]\(([^)\s]+)\)", txt)) - len(
            re.findall(r"\]\(([^)\s]+)\)", scan))
        print("%-30s 헤딩 %3d · 링크 내부 %2d/파일간 %2d · 마스킹 %2d · 죽은 링크 %d"
              % (name, len(headings[name]), intra, cross, masked, bad))

    if dead:
        print("\nFAIL — 죽은 링크 %d건:" % len(dead))
        for d in dead:
            print("  " + d)
        print("\n헤딩을 바꿨다면 같은 커밋에서 링크도 고쳐라. 새 슬러그는")
        print("  python3 slug-anchor-check.py --heading '<새 제목>'")
        return 1

    print("\nOK — 검사한 모든 링크가 실재 헤딩을 가리킨다"
          " (%s)" % ("전수 .md" if args.all else "README 4종"))
    print("root: %s" % root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
