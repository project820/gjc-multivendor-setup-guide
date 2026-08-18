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
        # 여는 펜스는 ``` 또는 ~~~ 3개 이상, 닫는 펜스는 **같은 문자 · 같은 길이 이상**.
        # 단순 토글로 처리하면 긴 펜스(````) 안의 짧은 ``` 에서 상태가 뒤집힌다.
        # 펜스 줄 자체도 덮는다(info string 에 링크 모양이 들어갈 수 있다).
        # blockquote 안의 펜스(`> ```)와 리스트 안에 들여쓴 펜스도 인식해야 하므로
        # 들여쓰기 제한을 두지 않는다.
        #
        # ⚠ **들여쓰기 코드블록은 다루지 않는다.** 한때 `indent >= 4` 를 코드로 보고
        # 덮었는데, 이 문서들의 3단계 불릿과 리스트 안 문단 이어가기가 전부 4칸을 넘어서
        # **정상 링크가 통째로 검사에서 빠졌다** — 게이트가 검사한다고 말하고 안 하는,
        # 이 스크립트가 없애려던 바로 그 결함이다(cyber-cop 패널 3인 동시 지적).
        # 실제로 필요한 것은 펜스 마스킹뿐이다.
        scan = list(txt)
        fence = None          # (문자, 길이) — 열려 있으면 튜플
        pos = 0
        for line in txt.splitlines(keepends=True):
            body = re.sub(r"^[ \t]*(?:>[ \t]?)*", "", line)   # blockquote 마커 제거
            fm = re.match(r"(`{3,}|~{3,})", body.lstrip())
            covered = False
            if fence is None:
                if fm:
                    fence = (fm.group(1)[0], len(fm.group(1)))
                    covered = True
            else:
                ch, width = fence
                if fm and fm.group(1)[0] == ch and len(fm.group(1)) >= width:
                    fence = None
                covered = True
            if covered:
                for k in range(pos, pos + len(line)):
                    if scan[k] != "\n":
                        scan[k] = " "
            pos += len(line)
        # 인라인 코드 스팬(`` `…` ``)도 링크가 아니다. 문서가 링크 **문법 자체**를
        # 이야기할 때 백틱 안에 `](…)` 를 쓰는데, 마스킹하지 않으면 그걸 진짜 링크로
        # 읽고 "대상 파일 없음" 오탐을 낸다 — 이 게이트가 실제로 자기 CHANGELOG 에서
        # 그렇게 걸렸다. 여는 백틱 런과 **같은 길이**의 런이 닫는다(CommonMark).
        scan = _mask_code_spans("".join(scan))
        matches = [(m.group(1), m.start(1))
                   for m in re.finditer(r"\]\(([^)\s]+)\)", scan)]
        # 로컬 HTML: `<a href>` 뿐 아니라 `<img src>` 도 본다. README ×4 의 17행이
        # `<img src="assets/role-winners.svg">` 로 배너를 문다 — src 가 깨져도 예전
        # "링크 무결성" 게이트는 통과했다(cyber-cop critic 지적).
        matches += [(m.group(2), m.start(2))
                    for m in re.finditer(
                        r"""<(?:a\b[^>]*\bhref|img\b[^>]*\bsrc)\s*=\s*(["'])(.*?)\1""",
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
        print("%-30s 헤딩 %3d · 링크 내부 %2d/파일간 %2d · 죽은 링크 %d"
              % (name, len(headings[name]), intra, cross, bad))

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
