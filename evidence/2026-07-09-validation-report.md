# v1.10.0 Grok 4.5 validation report — 2026-07-09

Branch: `feat/grok-4-5-critic-refresh` (tip hash intentionally omitted because this report is committed in the branch and would stale itself if it embedded its own final commit hash).

## Leader-run gates

- `python3 scripts/validate-profiles.py` — PASS.
  - 13 profiles checked.
  - Expected warnings only: documented same-family exceptions for monorepo and claude-codex profiles.
  - Result: `OK — all invariants hold`.
- `git diff --check` — PASS (no whitespace errors before commit).
- `python3 scripts/gen_svgs.py` — PASS; regenerated `assets/role-winners.svg`, `assets/profiles-matrix.svg`, `assets/effort-ladder.svg`; `architecture.svg` content unchanged in git.
- Targeted real calls:
  - `gjc -p --no-session --no-tools --model xai/grok-4.5:medium "Reply with exactly: OK"` — exit 0, `OK`.
  - `gjc -p --no-session --no-tools --model xai/grok-4.5:high "Reply with exactly: OK"` — exit 0, `OK`.
  - `gjc -p --no-session --no-tools --model xai/grok-4.5:bogus "Reply with exactly: OK"` — exit 1, model not found.
- `SELECTORS_ONLY=1 bash scripts/revalidate.sh` — PASS after rate-limit classification and expected-fail canary enforcement fixes; wrote `evidence/2026-07-09-selectors-rerun-3.md`.
  - Grok 4.5 `:medium` and `:high` OK.
  - OpenAI, Gemini, opencode rows OK.
  - Anthropic rows are `blocked(creds/rate-limit)` due 7d quota, not model regression.

## Review lanes

- Architect review `agent://13-Architect-Final-Grok45` — CLEAR/CLEAR/CLEAR, APPROVE, blockers `[]`.
- QA/red-team review `agent://14-QA-Final-Grok45` — passed/passed/passed, blockers `[]`.
  - Residual cost-table drift was fixed afterward in README x4.
  - `python3 scripts/validate-profiles.py` and `git diff --check` were rerun clean after the fix.
- PR #18 cyber-cop panel first pass returned DO-NOT-MERGE; blockers were fixed in this branch:
  - `scripts/cyber-cop-review.sh` now voids the optional Grok 4.5 panel seat when PR diff bytes exceed the documented ~400K-token exact-diff guard.
  - `scripts/revalidate.sh` now enforces expected-failure canaries: an unexpected `ok` for `xai/grok-4.5:bogus` or other fail rows is a regression.
  - README x4 effort/latency tables now state Grok 4.5 native efforts as `low/medium/high` and high-effort latency as ~50s total / ~48s TTFT from the 2026-07-09 streaming bench.
- PR #18 cyber-cop second pass cleared the high-risk panel but requested wording changes for Anthropic quota-blocked rows; README x4 badges/§6 now say the 2026-07-09 rerun covers Grok/OpenAI/Gemini/opencode and Anthropic remains 2026-07-02 last-good due rate-limit.

## Contract coverage

- Active selectors: only critic lanes changed to Grok 4.5; no default/executor/planner/architect promotion.
- Effort: no active `xai/grok-4.5:xhigh` or `xai/grok-4.5:max`; validator rejects them for profiles.
- README x4: embedded YAML parity and badges confirmed by `validate-profiles.py` plus direct badge count.
- Evidence: catalog snapshot, selector rerun, Grok 4.5 notes, and this validation report are append-only new files.
- Runtime: cyber-cop xai panel seat is optional/voidable; Gemini remains fail-closed; scripts do not merge or tag.
