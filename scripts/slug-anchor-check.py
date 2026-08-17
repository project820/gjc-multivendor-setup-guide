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


def slug(heading):
    t = heading.lstrip("#").strip().lower()
    out = []
    for ch in t:
        if ch.isalnum() or ch in "-_" or ch == "️":
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
        # 아닌 것 때문에 실패한다(cyber-cop 패널 지적). 오프셋을 보존해야 리포트의
        # 줄번호가 맞으므로, 펜스 구간은 지우지 말고 **같은 길이의 공백으로 덮는다.**
        scan = list(txt)
        in_fence = False
        pos = 0
        for line in txt.splitlines(keepends=True):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            elif in_fence:
                for k in range(pos, pos + len(line)):
                    if scan[k] != "\n":
                        scan[k] = " "
            pos += len(line)
        scan = "".join(scan)
        matches = [(m.group(1), m.start(1))
                   for m in re.finditer(r"\]\(([^)\s]+)\)", scan)]
        matches += [(m.group(2), m.start(2))
                    for m in re.finditer(r"""<a\b[^>]*\bhref\s*=\s*(["'])(.*?)\1""",
                                        scan, re.IGNORECASE)]
        matches += [(m.group(1), m.start(1))
                    for m in re.finditer(r"^\[[^\]]+\]:\s*(\S+)", scan, re.MULTILINE)]
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
