#!/usr/bin/env bash
# Catalog drift detector — snapshots the live model catalog so future runs can diff
# against it to spot new models, retirements, and context/max-out/effort changes.
# NOTE: `gjc --list-models` output carries NO price data — price drift is not tracked here.
#
#   bash scripts/catalog-snapshot.sh                 # write evidence/<date>-catalog.txt
#   bash scripts/catalog-snapshot.sh --diff          # diff newest two snapshots
# 아직 scripts/ 로 옮기기 전에는 대기 위치에서 그대로 실행해도 된다 —
# 루트를 gjc-profiles.yml 로 식별하고, 없으면 git 최상위로 되짚는다.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ ! -f "$ROOT/gjc-profiles.yml" ]; then
  ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || echo "$ROOT")"
  echo "note: repo root resolved via git → $ROOT" >&2
fi
cd "$ROOT" || { echo "FATAL: cannot resolve repo root"; exit 1; }
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
# v3: daybreak 추가. Daybreak Blue 가 cyber-cop 의 opt-in 수동 교차확인 핀으로 문서에
# 오르므로 드리프트 감시가 그 계열에 눈먼 채로 남으면 안 된다(승인된 post-interview R2).
# cyber 도 함께 넣는다 — gpt-5.6-cyber 는 미출하지만 카탈로그 등장 여부가 재평가 트리거다.
for q in claude-opus claude-sonnet claude-haiku claude-fable gpt-5 daybreak cyber grok gemini deepseek glm kimi qwen mimo minimax; do
  echo "## query: $q" >> "$OUT"
  gjc --list-models "$q" 2>/dev/null | grep -vE '^\s*$' >> "$OUT" || true
  echo >> "$OUT"
done
echo "Wrote $OUT ($(wc -l <"$OUT") lines). Run with --diff to compare snapshots."
