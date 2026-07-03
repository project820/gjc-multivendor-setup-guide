# L3 — Fable 5 role-fit behavioral A/B (2026-07-03, gjc 0.7.10)

Default-router A/B: `ultimate` (default=Opus 4.8) vs `legend` (default=Fable 5); executor/planner/architect/critic identical. Real delegated-work sessions.

| task | kind | Opus $ | Fable $ | Opus wall | Fable wall | Opus rc | Fable rc | note |
|---|---|--:|--:|--:|--:|:--:|:--:|---|
| R1 | solo | 0.2679 | 0.4626 | 31.0s | 31.0s | 0 | 0 |  |
| R2 | solo | 0.2108 | 0.352 | 30.0s | 21.0s | 0 | 0 |  |
| R3 | exec-patch | 0.1759 | 0.3327 | 23.0s | 23.0s | 0 | 0 |  |
| R4 | plan | 0.9906 | 1.5786 | 195.0s | 142.0s | 0 | 0 |  |
| R5 | arch | 0.314 | 0.5277 | 81.0s | 67.0s | 0 | 0 |  |
| R6 | safety | 0.309 | 0.6562 | 84.0s | 83.0s | 0 | 1 | **Fable refusal/error (stopReason=error) — Opus completed** |
| R7 | safety | 0.2954 | 0.5139 | 82.0s | 77.0s | 0 | 0 |  |
| R8 | longctx | 1.1228 | 2.3264 | 286.0s | 195.0s | 0 | 0 |  |

**Cost**: Opus-default total $3.69 vs Fable-default $6.75 → **Fable-default 1.83× cost**.
**Reliability**: Fable-default had 1 refusal/error event(s) on benign tasks (R6 defensive security triage: partial output then stopReason=error); Opus-default completed all 8.
**Quality (double-judge, anonymized, GPT-5.5)**: on R1 & R8, judge preferred the Fable-default output (5/5 vs 4/4; 4/4 vs 3/3) — marginal quality edge.

## Verdict per seat
- **default (router)** → **KEEP Opus** as recommended default. Fable-default shows a marginal quality edge but ~1.7–2× cost **and** a refusal/error on a benign task — unacceptable for the always-on router seat. Fable-default remains a valid **opt-in premium** (`legend`/`ultimate-f5`), now backed by L3 data. This VALIDATES v1.4's existing split (Opus=recommended, Fable=premium event).
- **planner (Fable candidate)** → **INCONCLUSIVE (direct A/B)**: delegation runs exceeded the 420–600s wall-budget (N1-ultimate 420s timeout; N2-ultimate completed 499s, Fable side terminated). Verdict from external benchmarks (ARC-AGI-2 → GPT-5.5 leads) + router cost/refusal downside → **KEEP GPT-5.5**.
- **architect (Fable candidate)** → **INCONCLUSIVE (direct A/B, budget)**; external evidence (architect axis → Gemini ctx/multimodal) + no Fable superiority → **KEEP Gemini 3.1 Pro (`-low:high`)**.

**Budget**: total measured spend across 24 runs = $15.24 / $30 hard cap. Planner/architect full A/B curtailed for time-budget discipline (pre-mortem-sanctioned labeling).

_Transcripts: sha16 per run in the .jsonl ledger. Judge sheets: internal (anonymized A/B, GPT-5.5+Gemini)._