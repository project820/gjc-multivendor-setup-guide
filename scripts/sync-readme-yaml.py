#!/usr/bin/env python3
"""Sync the embedded ```yaml profiles block in every README*.md from gjc-profiles.yml.

- README.md (Korean canonical) gets the full annotated block verbatim.
- README.{en,ja,zh}.md get a comment-stripped block: identical mappings, no Korean
  comments (avoids shipping wrong-language prose inside localized docs — PR #21 panel).
  The annotated canonical always lives in gjc-profiles.yml.

The drift guard (`scripts/validate-profiles.py` check #7) parses the YAML, so both
variants stay parity-green. Run after ANY change to gjc-profiles.yml:

    python3 scripts/sync-readme-yaml.py
"""
from __future__ import annotations
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCK_RE = re.compile(r"(```yaml\n)profiles:.*?(\n```)", re.S)
TRAILING_COMMENT_RE = re.compile(r"\s+#.*$")


def strip_comments(block: str) -> str:
    out: list[str] = []
    for line in block.splitlines():
        if line.lstrip().startswith("#"):
            continue
        line = TRAILING_COMMENT_RE.sub("", line).rstrip()
        out.append(line)
    # collapse runs of blank lines left behind by removed comment banners
    collapsed: list[str] = []
    for line in out:
        if line == "" and collapsed and collapsed[-1] == "":
            continue
        collapsed.append(line)
    while collapsed and collapsed[-1] == "":
        collapsed.pop()
    return "\n".join(collapsed)


def main() -> int:
    src = (ROOT / "gjc-profiles.yml").read_text(encoding="utf-8")
    full = src[src.index("profiles:"):].rstrip("\n")
    stripped = strip_comments(full)
    for rf in sorted(ROOT.glob("README*.md")):
        block = full if rf.name == "README.md" else stripped
        text = rf.read_text(encoding="utf-8")
        if not BLOCK_RE.search(text):
            print(f"{rf.name}: no embedded yaml block — skipped")
            continue
        rf.write_text(BLOCK_RE.sub(lambda m: m.group(1) + block + m.group(2), text, count=1), encoding="utf-8")
        print(f"{rf.name}: synced ({'full' if block is full else 'comment-stripped'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
