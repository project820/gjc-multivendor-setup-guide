#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""링킬 무결성 검사 — 파일 생존 + 앵커 슬러그. 예전 헤딩 → GitHub 앵커 슬러그 계산 + 문서 내 링크와 대조.

왜 필요한가
-----------
v3 는 `## 5.` 제목의 번들 개수를 바꾼다. 그 순간 GitHub 슬러그가 바뀌어 문서 안의
앵커 링크가 **에러 없이 조용히** 죽는다(2026-08-18 실측: KO 4 · EN 1 · JA 3 · ZH 3 = 11개).
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


def slug(heading):
    t = heading.lstrip("#").strip().lower()
    out = []
    for ch in t:
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
    """\uc804\uc218 .md \ud30c\uc77c \u2192 {\uc0c1\ub300\uacbd\ub85c: {\uc2ac\ub7ec\uadf8, \u2026}}"""
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
    ap.add_argument("--heading", default=None, help="\uc774 \ud5e4\ub529\uc758 \uc2ac\ub7ec\uadf8\ub9cc \uacc4\uc0b0\ud558\uace0 \uc885\ub8cc")
    ap.add_argument("--all", action="store_true",
                    help="README 4\uc885\uc774 \uc544\ub2c8\ub77c \uc804\uc218 .md \ub97c \uac80\uc0ac(\ud30c\uc77c\uac04 \ub9c1\ud06c \ud3ec\ud568)")
    args = ap.parse_args()

    if args.heading:
        print(slug(args.heading))
        return 0

    root = find_root(args.root)
    if not os.path.exists(os.path.join(root, "gjc-profiles.yml")):
        print("FAIL \u2014 gjc-profiles.yml \uc5c6\ub294 \ud2b8\ub9ac\ub2e4: %s" % root)
        return 1

    headings = collect_headings(root)
    scope = sorted(headings) if args.all else [f for f in READMES if f in headings]
    dead = []

    for name in scope:
        path = os.path.join(root, name)
        txt = open(path, encoding="utf-8").read()
        links = re.findall(r"\]\(([^)\s]+)\)", txt)
        intra = cross = bad = 0
        for raw in links:
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
                # md \uac00 \uc544\ub2c8\uba74 \uc575\ucee4\ub294 \ubabb \ubcf4\uc9c0\ub9cc **\ud30c\uc77c \uc0dd\uc874**\uc740 \ubcf8\ub2e4.
                if not os.path.exists(os.path.join(root, owner)):
                    bad += 1
                    dead.append("%s \u2192 %s : \ub300\uc0c1 \ud30c\uc77c \uc5c6\uc74c (\ub4f1\uc7a5 %d\ud68c)"
                                % (name, owner, links.count(raw)))
                continue
            if frag is None:
                continue          # \ud30c\uc77c\ub9cc \uac00\ub9ac\ud0a4\ub294 \ub9c1\ud06c \u2014 \uc0dd\uc874 \ud655\uc778\uc73c\ub85c \ub05d
            if frag not in headings[owner]:
                bad += 1
                dead.append("%s \u2192 %s%s : \ub300\uc0c1 \ud5e4\ub529 \uc5c6\uc74c (\ub4f1\uc7a5 %d\ud68c%s)"
                            % (name, owner, frag, links.count(raw),
                               ", \ud4fc\uc13c\ud2b8 \uc778\ucf54\ub529" if "%" in raw else ""))
        print("%-30s \ud5e4\ub529 %3d \u00b7 \ub9c1\ud06c \ub0b4\ubd80 %2d/\ud30c\uc77c\uac04 %2d \u00b7 \uc8fd\uc740 \ub9c1\ud06c %d"
              % (name, len(headings[name]), intra, cross, bad))

    if dead:
        print("\nFAIL \u2014 \uc8fd\uc740 \ub9c1\ud06c %d\uac74:" % len(dead))
        for d in dead:
            print("  " + d)
        print("\n\ud5e4\ub529\uc744 \ubc14\uafe8\ub2e4\uba74 \uac19\uc740 \ucee4\ubc0b\uc5d0\uc11c \ub9c1\ud06c\ub3c4 \uace0\uccd0\ub77c. \uc0c8 \uc2ac\ub7ec\uadf8\ub294")
        print("  python3 slug-anchor-check.py --heading '<\uc0c8 \uc81c\ubaa9>'")
        return 1

    print("\nOK \u2014 \uac80\uc0ac\ud55c \ubaa8\ub4e0 \ub9c1\ud06c\uac00 \uc2e4\uc7ac \ud5e4\ub529\uc744 \uac00\ub9ac\ud0a8\ub2e4"
          " (%s)" % ("\uc804\uc218 .md" if args.all else "README 4\uc885"))
    print("root: %s" % root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
