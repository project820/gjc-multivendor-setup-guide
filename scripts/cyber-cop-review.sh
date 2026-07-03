#!/usr/bin/env bash
# cyber-cop reviewer-mode review of a PR (GJC headless, cyber-cop profile).
#
# Usage:  scripts/cyber-cop-review.sh <PR_NUMBER>
# Env:    REPO=owner/name (default: project820/gjc-multivendor-setup-guide)
#         TIMEOUT=<seconds> (default: 600)
#
# Runs the review under the `cyber-cop` profile (architect+critic lead, cross-family
# vs the assumed-Claude author) and prints the verdict to stdout. It NEVER merges —
# the verdict is surfaced to a human for the merge decision (routing-rules.md contract).
set -e
REPO="${REPO:-project820/gjc-multivendor-setup-guide}"
TIMEOUT="${TIMEOUT:-600}"
PR="${1:?usage: cyber-cop-review.sh <PR_NUMBER>}"
WORK="$(mktemp -d "/tmp/cc-review-${PR}.XXXX")"

gh pr view "$PR" -R "$REPO" --json number,title,author,body,baseRefName,headRefName,additions,deletions,changedFiles > "$WORK/meta.json"
gh pr diff "$PR" -R "$REPO" > "$WORK/pr.diff"
gh pr view "$PR" -R "$REPO" --json files --jq '.files[] | "\(.additions)+ \(.deletions)- \(.path)"' > "$WORK/files.txt"

TITLE=$(python3 -c "import json;print(json.load(open('$WORK/meta.json'))['title'])")
FILES=$(tr '\n' ' ' < "$WORK/files.txt")

PROMPT="You are running under the cyber-cop reviewer profile (reviewer-mode, architect+critic lead).
Review PR #${PR} \"${TITLE}\" of ${REPO} as an INDEPENDENT reviewer. Do NOT trust claims made in the PR; re-verify them.

Reviewer contract (routing-rules.md):
- architect = first-pass code-review adjudicator: verdict CLEAR / WATCH / BLOCK with file-backed reasons.
- critic = merge gate. Each critic vote MUST cite at least one file-backed blocking issue OR an explicit no-finding rationale; unsupported verdicts are void.
- For high-risk or security PRs: convene a 3-vote cross-family panel {gpt-5.5, grok-4.3, gemini-3.1-pro}, independent votes aggregated with no debate; 2/3 dissent OR any CRITICAL/BLOCK blocks.
- No baseless LGTM: search for reasons to block FIRST.
- Repo invariants (scripts/validate-profiles.py): default=Anthropic; executor!=architect; planner!=critic; effort legality; 4-language README YAML parity.

PR metadata file: ${WORK}/meta.json
Changed files: ${FILES}
Full unified diff: ${WORK}/pr.diff  (read it before judging).

Output exactly these four sections, terse and evidence-first:
1. ARCHITECT VERDICT: CLEAR|WATCH|BLOCK + file-backed reasons.
2. CRITIC VERDICT: APPROVE|REQUEST_CHANGES|BLOCK + file-backed findings (or explicit no-finding rationale).
3. INVARIANTS: pass/fail per invariant.
4. MERGE RECOMMENDATION: MERGE | DO-NOT-MERGE + one-line why."

echo "=== cyber-cop review: PR #${PR} — ${TITLE} ==="
perl -e 'alarm shift; exec @ARGV' "$TIMEOUT" \
  gjc -p --mpreset cyber-cop --session-dir "$WORK/session" "$PROMPT"
