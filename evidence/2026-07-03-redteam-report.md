# Red-Team Review — v1.4 12-profile role assignment (2026-07-03)

> Method: deep-interview(9 rounds) → ralplan consensus(Architect WATCH / Critic OKAY) → ultragoal execution. Evidence tiers: **L3** behavioral A/B (real `gjc -p` delegated sessions) · **L2** literature + live probe · **L1** literature only. Change proposals require L3; "keep" confirmations require L2. Machine: gjc 0.7.10, 5 vendors authed. Inputs: this session's L3 ledger + 3 external council reports (Perplexity deep-research / consultant / final) dated 2026-07-03.

## 0. Headline

The community's two loud questions ("is Grok right as critic", "should Composer replace executor") are **both lower-leverage than they look**, and v1.4's premium-line architecture is **largely validated** — with one genuinely new, L3-backed nuance about the Fable-5 default seat.

| Question | Verdict | Tier | 1-line reason |
|---|---|:--:|---|
| default (router) = Fable 5? | **KEEP Opus as recommended default; Fable-default = opt-in premium only** | **L3** | Fable-default: marginal quality edge but **1.83× cost + 1 refusal/error on a benign task** — bad for the always-on router |
| critic = Grok 4.3? | **KEEP** (+ optional GPT-5.5 2nd-pass on merge-critical) | L2 | cross-family independence + cheapest seat; council 3/3 KEEP |
| executor = Composer 2.5 Fast? | **REJECT Fast; Composer *Standard* only as optional `ultimate-fast` lane** | L2 | Fast=Standard at 6× price, no reasoning-effort knob (breaks executor self-verify), 200k ctx, reward-hacking collapse 74.7→54.0 |
| planner = Fable 5? | **KEEP GPT-5.5** | L2 (A/B budget-curtailed) | no Fable superiority on ARC-AGI-2 (planner axis); router cost/refusal downside |
| architect = Fable 5? | **KEEP Gemini 3.1 Pro `-low:high`** | L2 | architect axis = ctx/multimodal (Gemini); Fable vision vendor-claimed |

## 1. L3 evidence — Fable-5 default router A/B (the one thing external councils could not measure)

`ultimate` (default=Opus 4.8) vs `legend` (default=Fable 5), 8 paired real delegated tasks, other 4 seats identical. Full ledger: [`2026-07-03-l3-fable-rolefit.jsonl`](./2026-07-03-l3-fable-rolefit.jsonl) + [summary](./2026-07-03-l3-fable-rolefit.md).

- **Cost**: Opus-default $3.69 vs Fable-default $6.75 → **1.83×**.
- **Reliability**: Fable-default hit a **refusal/error (`stopReason=error`) on R6** (a *benign* defensive install.sh security triage) after partial output; Opus-default completed all 8. 1/8 observed — vendor's "<5% safety-router" is L1 background, but the router seat is exactly where a mid-orchestration refusal is most damaging.
- **Quality**: anonymized double-judge (GPT-5.5 + Gemini 3.1 Pro) — R1: both judges preferred Fable-default (5/5 vs 4/4); R8: **split** (GPT-5.5 → Fable 4/4 vs 3/3; Gemini → Opus, flagging Output-A truncation). Net a *marginal, non-counterbalanced* edge (A=legend in both judged pairs, n=2 → position-bias confound not excluded).
- **Net**: quality edge does not clear the cost-adjusted + reliability bar for an always-on router → **KEEP Opus default; Fable-default stays premium/opt-in** (`legend`, `ultimate-f5`). This directly **validates v1.4's existing recommended=Opus / premium=Fable split** with behavioral data.

Planner/architect Fable candidates: direct A/B **curtailed** (delegation runs exceeded 420–600s wall budget — N1-ultimate timed out at 420s, N2-ultimate completed at 499s, Fable sides terminated). Verdict falls back to external benchmark + router evidence (KEEP incumbents). Labeled INCONCLUSIVE on direct A/B, per plan pre-mortem.

## 2. 12-profile L2 audit

Every selector in all 12 profiles was OK in the 2026-07-02 live matrix (re-confirmed 2026-07-03 for fable/sonnet-5). Role-family check: `critic` is cross-family with `executor` in **10/12**; the 2 same-family cases (`solo-anthropic`, `solo-openai`) are **intentional single-vendor** profiles (documented independence tradeoff). No accidental same-family critic found.

| Profile | verdict | note |
|---|:--:|---|
| daily | **KEEP** (+effort-ladder) | Opus:med router + gpt-5.4 exec + Gemini plan/arch + Grok critic; well-balanced. Adopt council effort-ladder wording. |
| ultimate | **KEEP** | recommended premium; Opus default validated by §1 L3. |
| ultimate-f5 | **KEEP (relabel)** | Fable default+exec = quality-max **premium/opt-in**; annotate 1.83× cost + refusal-risk from §1. |
| legend | **KEEP (relabel)** | Fable default only; same annotation. Not the recommended daily default. |
| coding-sprint | KEEP | exec Opus:max + coding-aware GPT critic (cross-family vs gemini). |
| escalation | KEEP | v1.4 already moved exec→fable-5:xhigh as rescue; §1 supports intermittent Fable use. critic Grok:xhigh silently clamps to high (documented). |
| eco | KEEP | cheap delegation; critic gemini-3.5-flash-low cross-family vs opencode-go exec. |
| monorepo | KEEP | all-1M seats; critic opencode-go/glm-5.2 (cross-family vs anthropic exec; deepseek-v4-pro documented alt). |
| solo-anthropic | KEEP | single-vendor; same-family critic = documented tradeoff. |
| solo-openai | KEEP | single-vendor base-GPT; same-family critic tradeoff. |
| claude-codex | KEEP | 2-vendor; Anthropic exec / GPT critic cross-family. |
| claude-codex-max | KEEP | cost-no-object 2-vendor. |

**Audit result: 12/12 KEEP** (2 with premium-relabel annotations). No role swap warranted by evidence. The architecture is merit-driven, not diversity theater.

## 3. Composer 2.5 (community "why not Composer" question)

- **grok-build Standard access on this machine: NOT verified** — the `grok-build` provider requires `GROK_CLI_OAUTH_TOKEN` wiring that is not present; `xai/grok-composer-2.5-fast` resolves but Standard-tier routing via grok-build is unconfirmed here. Marked **vendor/route-unverified**.
- Evidence (external, corroborated): Composer 2.5 = Cursor fine-tune on Kimi K2.5; **Fast = Standard intelligence at ~6× price** (pure latency purchase); `supportsReasoningEffort:false` on the grok-build composer route breaks GJC executor self-verify contract (note: the `xai/grok-composer-2.5-fast` catalog row does expose effort levels — the property is route-variant-dependent); 200k ctx vs Claude 1M; SWE-bench Pro **74.7→54.0 collapse** under stricter harness.
- **Verdict**: REJECT Composer Fast as executor. If throughput is genuinely needed, an optional **`ultimate-fast`** lane on Composer **Standard** (never Fast) is defensible — gated on verifying grok-build Standard access first.

## 4. External council 4-recommendation verdict table

| Rec | Verdict | Basis |
|---|:--:|---|
| Effort ladder (`:max`/`:xhigh`→`:high`, escalate on Critic ITERATE/Architect BLOCK) | **ACCEPT** | L3 cost data: premium seats at max are the dominant cost driver ($3.69–6.75/8-task). Add as guidance + optional lower-effort variant; keep `:max` in `ultimate`/`escalation` where accuracy-first. |
| Verify `gemini-3.1-pro-low:high` architect selector (A/B vs `gemini-3.1-pro:high`) | **PARTIAL/RESOLVED** | Our engine check is decisive (externals only recommended verifying — did not themselves conclude non-degraded): bare `gemini-3.1-pro-high` 400s; `-low:high` is the engine's canonical high path (thinking_level HIGH), NOT degraded. KEEP `-low:high`; no `gemini-3.1-pro:high` public slug on this provider. |
| GPT-5.5 second-pass critic (meta-judge) for merge-critical | **ACCEPT (doc-only)** | Judging-with-Many-Minds: meta-judge > debate. Add as workflow note for `escalation`, not a YAML seat change (single YAML critic stays Grok). |
| `ultimate-fast` throughput profile (Composer **Standard**) | **CONDITIONAL ACCEPT** | Only after grok-build Standard access is verified (see §3). Ship as opt-in, never Fast. |

## 5. Invariant red-team result

- **default=Anthropic-flagship** invariant: **HELD** — L3 shows Fable(also Anthropic) default is quality-viable but cost/reliability-worse; Opus remains best router. Invariant not broken, refined to "Opus recommended / Fable premium".
- **critic=cross-family** invariant: **HELD** — no evidence to drop it; single-vendor exceptions already documented.

## 6. Confidence & gaps
- **High**: default-router cost 1.83× (measured), Composer economics (external primary), 12-profile selector validity (live).
- **Medium**: Fable refusal rate (1/8 observed; not a rate claim), quality edge (2 judged pairs).
- **Curtailed**: planner/architect direct A/B (time budget) — verdict leans on external benchmarks.
- **Unverified**: grok-build Composer Standard access on this machine.
- Total L3 spend: $15.24 / $30 cap (24 runs; planner/arch full A/B intentionally not exhausted).
## 7. Capability / cost-normalized dual ranking (7/7 two-phase)

Two rankings for the **default-router / premium-executor seat** (the seat where the Opus-vs-Fable decision bites): **capability** (ordinal, from external council benchmarks + our L3 quality judge) and **cost-normalized value** (capability per measured $). Costs are the L3-measured router battery (`ultimate`=Opus-default $0.461/task; `legend`=Fable-default $0.844/task, R1–R8 mean). Two phases because Fable 5's price model flips on **7/7**: pre-7/7 Fable is bundled in the Anthropic Max subscription (near-zero marginal), post-7/7 it is credit-metered ($10 / $50 tiers) and its true per-token cost surfaces.

**Capability rank (phase-invariant — capability doesn't change with billing):**

| Rank | Seat model | Capability basis |
|:--:|---|---|
| 1 | Fable 5 (`legend`/`ultimate-f5`) | marginal quality edge in L3 double-judge (R1 both judges; R8 GPT only) + vendor frontier claims |
| 1 | Opus 4.8 (`ultimate`/`daily`) | tied top; **only seat with 8/8 reliability** (Fable refused R6) — reliability breaks the tie for an always-on router |
| 3 | Sonnet-5 (`eco` exec tier) | strong, cheaper, lower ceiling |

**Cost-normalized value rank (capability ÷ measured $/task):**

| Rank | Phase A — **pre-7/7** (Fable subscription-bundled) | Phase B — **post-7/7** (Fable credits $10/$50) |
|:--:|---|---|
| 1 | **Opus 4.8** — $0.461/task, top-tier, 8/8 reliable | **Opus 4.8** — $0.461/task; gap over Fable *widens* |
| 2 | Fable 5 — marginal quality edge, subscription hides the 1.83× marginal cost; still loses on reliability | Sonnet-5 — cheaper strong tier becomes the value pick for non-critical throughput |
| 3 | Sonnet-5 — cheapest strong tier | Fable 5 — 1.83× measured cost now **explicit + credit-metered**; premium-only, worst value |

**Reading**: Opus 4.8 is the cost-normalized #1 in *both* phases; Fable's only ranking argument (marginal capability) never overcomes its 1.83× cost + R6 reliability failure, and post-7/7 its value rank *drops* as the subscription no longer masks marginal cost. This is the quantitative backing for **KEEP Opus recommended default; Fable = opt-in premium** — and it means the v1.4 split gets *more* defensible after 7/7, not less. (Capability ordering is L1/L2 ordinal — external benchmarks + 2 judged pairs; cost figures are L3-measured.)
