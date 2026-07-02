#!/usr/bin/env bash
# Catalog drift detector — snapshots the live model catalog so future runs can diff
# against it to spot new models, retirements, and context/max-out/effort changes.
# NOTE: `gjc --list-models` output carries NO price data — price drift is not tracked here.
#
#   bash scripts/catalog-snapshot.sh                 # write evidence/<date>-catalog.txt
#   bash scripts/catalog-snapshot.sh --diff          # diff newest two snapshots
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p evidence

if [ "${1:-}" = "--diff" ]; then
  # bash-3.2 portable (macOS default bash has no `mapfile`); this branch always
  # terminates here and can never fall through into the snapshot path below.
  new="$(ls -1 evidence/*-catalog.txt 2>/dev/null | sort | tail -1)"
  old="$(ls -1 evidence/*-catalog.txt 2>/dev/null | sort | tail -2 | head -1)"
  if [ -z "$new" ] || [ -z "$old" ] || [ "$new" = "$old" ]; then
    echo "need >=2 snapshots to diff"; exit 1
  fi
  echo "diff $old  ->  $new"
  diff "$old" "$new" || true
  exit 0
fi

command -v gjc >/dev/null 2>&1 || { echo "gjc not found"; exit 2; }
DATE="$(date +%Y-%m-%d)"; OUT="evidence/${DATE}-catalog.txt"
# Per-provider model listing GJC currently resolves (bundled + live-discovered after /login).
: > "$OUT"
for q in claude-opus claude-sonnet claude-haiku claude-fable gpt-5 grok gemini deepseek glm kimi qwen mimo minimax; do
  echo "## query: $q" >> "$OUT"
  gjc --list-models "$q" 2>/dev/null | grep -vE '^\s*$' >> "$OUT" || true
  echo >> "$OUT"
done
echo "Wrote $OUT ($(wc -l <"$OUT") lines). Run with --diff to compare snapshots."
