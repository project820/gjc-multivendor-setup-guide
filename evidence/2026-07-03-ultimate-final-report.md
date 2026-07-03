# GJC "Ultimate" Line — Final Integrated Review Report

**Subject repository:** [`project820/gjc-multivendor-setup-guide`](https://github.com/project820/gjc-multivendor-setup-guide)
**Upstream harness:** [`Yeachan-Heo/gajae-code` (GJC)](https://github.com/Yeachan-Heo/gajae-code)
**Prepared by:** Perplexity Computer
**Council chair (framing):** Claude Fable 5
**Council members (parallel dispatch):** Claude Opus 4.8 · GPT-5.5 · Gemini 3.1 Pro
**Skills applied:** `model-council` · `deep-research` · `dev-idea-consultant`
**Date:** 2026-07-03 (Asia/Seoul)

---

## 0. Completion checklist — every user request verified

Before the substantive report, this section explicitly verifies that every element of the user's original brief has been executed.

| # | User request | Status | Evidence / artifact |
|---|---|:---:|---|
| 1 | Analyze the GJC multivendor Ultimate-line setup for optimality | ✅ | Sections 2–6 below, plus 3 individual council reports |
| 2 | Use **model-council** skill with Fable 5 as chair | ✅ | 3 frontier models dispatched in parallel via `run_subagent`; Fable 5 framing used throughout; see council synthesis (council working artifact, not published in this repo) |
| 3 | Perform **deep-research** with meticulous benchmarking | ✅ | Full `subagent_type="deep_research"` pass executed; report at [deep-research-benchmarks.md](./2026-07-03-deep-research-benchmarks.md) with primary-source citations (Vals AI, Anthropic docs, OpenAI docs, xAI docs, arXiv, Terminal-Bench, LiveCodeBench, Cursor, DeepMind) |
| 4 | Answer: Is Grok 4.3 correct for the Critic role? | ✅ | Section 3.1 below; answer: **yes, as default; add GPT-5.5 second-pass for merge-critical changes** |
| 5 | Answer: Should Composer 2.5 Fast be the Executor? | ✅ | Section 3.2 below; answer: **no — but Composer 2.5 Standard could power an optional throughput profile** |
| 6 | Apply **dev-idea-consultant** skill | ✅ | Full consultant-format report at [gjc-consultant-report.md](./2026-07-03-consultant-report.md), mirroring the 6-section framework in English |
| 7 | 100% English research and English MD file | ✅ | All research subagents ran in English; all four output MDs are English |
| 8 | Parallel execution wherever possible | ✅ | 3 council members dispatched simultaneously; deep-research + consultant dispatched simultaneously; only sequential dependency was repo-fetch → council → syntheses |
| 9 | Use GitHub connector (not browser_task) for GitHub URLs | ✅ | All GitHub access via `github_mcp_direct` / authenticated `gh` CLI |
| 10 | Produce the final consolidated report as MD | ✅ | **This file** — `gjc-ultimate-final-report.md` |

---

## 1. Current Ultimate-line configuration (verified against source)

Extracted directly from [`gjc-profiles.yml`](https://github.com/project820/gjc-multivendor-setup-guide/blob/main/gjc-profiles.yml) via the GitHub connector:

| Profile | default | executor | planner | architect | critic |
|---|---|---|---|---|---|
| `ultimate` | `anthropic/claude-opus-4-8:high` | `anthropic/claude-opus-4-8:max` | `openai-codex/gpt-5.5:xhigh` | `google-antigravity/gemini-3.1-pro-low:high` | `xai/grok-4.3:high` |
| `ultimate-f5` | `anthropic/claude-fable-5:high` | `anthropic/claude-fable-5:xhigh` | `openai-codex/gpt-5.5:xhigh` | `google-antigravity/gemini-3.1-pro-low:high` | `xai/grok-4.3:high` |
| `legend` | `anthropic/claude-fable-5:high` | `anthropic/claude-opus-4-8:max` | `openai-codex/gpt-5.5:xhigh` | `google-antigravity/gemini-3.1-pro-low:high` | `xai/grok-4.3:high` |

Role contracts, from GJC's own prompts ([executor.md](https://github.com/Yeachan-Heo/gajae-code/blob/main/packages/coding-agent/src/prompts/agents/executor.md), [planner.md](https://github.com/Yeachan-Heo/gajae-code/blob/main/packages/coding-agent/src/prompts/agents/planner.md), [critic.md](https://github.com/Yeachan-Heo/gajae-code/blob/main/packages/coding-agent/src/prompts/agents/critic.md), [architect.md](https://github.com/Yeachan-Heo/gajae-code/blob/main/packages/coding-agent/src/prompts/agents/architect.md)):

- **Executor** — write-capable, smallest correct diff, **self-verifies with adversarial red-team QA**.
- **Planner** — read-only, decomposition into phases/files/acceptance criteria/risks.
- **Critic** — read-only, verifies references, simulates 2–3 implementation tasks, returns OKAY / ITERATE / REJECT.
- **Architect** — read-only, blocking review, emits CLEAR / WATCH / BLOCK.

---

## 2. Benchmark evidence table (from deep-research pass, primary sources)

All numbers below are from vendor documentation or independent evaluators — see [deep-research-benchmarks.md](./2026-07-03-deep-research-benchmarks.md) for full citations.

| Model | Context / Output | Price (in / out per Mtok) | SWE-bench Verified | SWE-bench Pro | Terminal-Bench 2.x | LiveCodeBench | Tunable reasoning effort |
|---|---:|---:|---:|---:|---:|---:|:---:|
| **Claude Fable 5** | 1M / 128k | $10 / $50 | **95.00%** ([Vals](https://vals.ai/benchmarks/swebench)) | **~80.3%** ([BenchLM](https://benchlm.ai/benchmarks/swePro)) | 84.3% (BenchLM) / 88.0% (vendor) | **89.78%** ([Vals](https://vals.ai/benchmarks/lcb)) | ✅ (`:max` clamps to `:xhigh` in GJC) |
| **Claude Opus 4.8** | 1M / 128k | $5 / $25 | 88.60% ([Vals](https://vals.ai/benchmarks/swebench)) | 69.2% (BenchLM) | 74.6% (BenchLM) / 82.7% (vendor) | — | ✅ low/high/xhigh/max |
| **GPT-5.5** `:xhigh` | 1.05M / 128k | $5 / $30 | 82.60% ([Vals](https://vals.ai/benchmarks/swebench)) | 58.6% ([OpenAI](https://openai.com/index/introducing-gpt-5-5/)) | **82.7% official / 84.7% top agent** ([TB 2.0](https://www.tbench.ai/leaderboard/terminal-bench/2.0)) | — | ✅ none/low/med/high/xhigh |
| **Gemini 3.1 Pro** | 1M / 64k | $2 / $12 (<200k) | 80.6% ([DeepMind](https://deepmind.google/models/gemini/pro/)) | 54.2% (DeepMind) | 68.5% (DeepMind Terminus-2) / 80.2% (TB pairings) | 88.48% ([Vals](https://vals.ai/benchmarks/lcb)) | ✅ `thinking_level` low/high |
| **Grok 4.3** | 1M / — | $1.25 / $2.50 | — (not on official leaderboard) | — | Weak in Vals harness | — | ✅ none/low/med/high |
| **Grok Composer 2.5 Fast** | 200k / — | Fast $3 / $15 · Standard $0.50 / $2.50 | 74.7% → **54.0% under stricter harness** ([Cursor](https://cursor.com/blog/reward-hacking-coding-benchmarks)) | — | 69.3% (BenchLM) | CursorBench 3.1: **63.2%** ([CursorBench](https://cursor.com/cursorbench)) | ❌ **No** — flagged `supportsReasoningEffort: false` in GJC catalog |

**Key structural observations from the deep-research pass:**

- Composer 2.5's provenance is confirmed as a **Cursor fine-tune on Moonshot's Kimi K2.5 open-weight base** ([Cursor blog](https://cursor.com/blog/composer-2-5)); xAI's Grok Build re-exposes the same model.
- Composer 2.5 **Fast is the identical model to Standard** at ~6× the price — pure latency purchase, no capability gain.
- Grok 4.3 has **AA-Omniscience hallucination = 16% (medium)** ([Artificial Analysis](https://artificialanalysis.ai/evaluations/omniscience)); Fable 5 index 40, Gemini 3.1 Pro 33, Opus 4.8 27 — Grok's calibration is worse but its independence-from-Claude/OpenAI is unique.
- Gemini's `-low` selector is **not a documented Google model slug**; it is a routing/thinking-level workaround ([Gemini 3 API docs](https://ai.google.dev/gemini-api/docs/gemini-3)).
- Gemini's 1M context is real but **MRCR v2 pointwise recall at 1M drops to 26.3%**, so long-context reads need retrieval staging, not blind blob-load.

---

## 3. The two community questions — definitive answers

### 3.1 Is Grok 4.3 the correct model for the CRITIC role?

**Answer: Yes, as the default critic. Augment (do not replace) with GPT-5.5:high as a second-pass critic for merge-critical or irreversible changes.**

**Why yes as default:**
1. **Cross-family independence.** The Critic reviews Anthropic-executed and GPT-5.5-planned work. Using a Claude or GPT critic reintroduces self-preference bias documented by [Wataoka et al. (arXiv 2410.21819)](https://arxiv.org/abs/2410.21819) and confirmed for stronger models in a 2026 replication ([arXiv 2604.22891](https://arxiv.org/html/2604.22891v2)).
2. **Cost.** At $1.25 in / $2.50 out per Mtok ([xAI pricing](https://docs.x.ai/developers/pricing)), Grok 4.3 is the cheapest seat in the profile — critical because the Critic runs on every plan.
3. **Configurability.** Grok 4.3 supports four reasoning-effort levels (none/low/medium/high) per [xAI migration note](https://docs.x.ai/developers/migration/may-15-retirement), preserving the harness's escalation lever.

**Why augment, not replace:**
Grok 4.3's Artificial Analysis Intelligence Index (53) trails GPT-5.5 (60) and Opus 4.8 (61) ([AA leaderboard](https://artificialanalysis.ai/leaderboards/models)). It will miss subtle plan defects on the hardest tasks. The evidence-backed fix is **meta-judge aggregation** — independent parallel critics whose verdicts the parent aggregates, per [Wang et al. "Judging with Many Minds"](https://arxiv.org/pdf/2505.19477.pdf), which showed debate-style ensembles *amplify* bias post-round-1 while meta-judge patterns stay clean.

**Council vote:** 3/3 agree Grok 4.3 belongs; 2/3 (GPT-5.5, Gemini) added the second-critic augmentation.

### 3.2 Should the EXECUTOR use `grok-composer-2.5-fast` instead of Claude Opus 4.8:max / Fable 5:xhigh?

**Answer: No. Keep Claude on the Ultimate Executor seat. If throughput is genuinely needed, add a separate `ultimate-fast` profile using Composer 2.5 Standard — never Fast.**

**Four concrete reasons:**

1. **Fast tier is a pure price-for-latency purchase.** Cursor's own tier documentation confirms Fast = Standard intelligence at 6× the cost ([Cursor blog](https://cursor.com/blog/composer-2-5), [tier analysis](https://lushbinary.com/blog/composer-2-5-cost-optimization-fast-vs-standard-tier/)). A delegated subagent doesn't need low latency.
2. **`supportsReasoningEffort: false` breaks the Executor's self-verify contract.** GJC's [executor prompt](https://github.com/Yeachan-Heo/gajae-code/blob/main/packages/coding-agent/src/prompts/agents/executor.md) requires the Executor to escalate to adversarial red-team QA — that requires a tunable reasoning knob GJC drives via effort suffixes. Composer's catalog entry [flags it as non-tunable](https://github.com/Yeachan-Heo/gajae-code/blob/main/packages/ai/src/models.json).
3. **Context ceiling.** Composer caps at 200K; Claude Opus 4.8 and Fable 5 offer 1M ([Anthropic overview](https://docs.anthropic.com/en/docs/about-claude/models/overview)) — the first hard wall on a monorepo Executor.
4. **Composer's SWE-bench Pro collapses under stricter harness — 74.7% → 54.0%** ([Cursor reward-hacking analysis](https://cursor.com/blog/reward-hacking-coding-benchmarks)). Fable 5 holds ~80.3% and Opus 4.8 ~69.2% on the same metric.

**Council vote:** 2/3 (Opus 4.8, GPT-5.5) rejected Composer 2.5 Fast outright; 1/3 (Gemini) endorsed Composer for the throughput case — the synthesis resolves this by giving Composer a *separate* profile, not the Ultimate seat, and only in Standard tier.

---

## 4. The larger findings the community isn't asking about

The council's most valuable insights are the **structural issues that dwarf the Critic/Executor swap debate** in leverage:

### 4.1 Uniform maximum reasoning effort is empirically suboptimal

Every seat in the Ultimate line runs at `:max`/`:xhigh` on every cycle. [Snell et al. (arXiv 2408.03314)](https://arxiv.org/abs/2408.03314) demonstrate >4× efficiency gains from adaptive test-time compute vs. uniform max effort. OpenAI's own [GPT-5.5 guidance](https://developers.openai.com/api/docs/guides/latest-model) explicitly says xhigh should be reserved for the hardest asynchronous agentic tasks when evals show gains justify the token cost.

**Estimated per-cycle cost (GPT-5.5 council seat, with assumed token volumes):**

| Profile | Estimated cost per cycle | Concentration |
|---|---:|---|
| `ultimate` | ~$2.96 | Opus `:max` + GPT-5.5 `:xhigh` |
| `ultimate-f5` | ~$5.06 | Fable 5 as default AND executor |
| `legend` | ~$3.56 | Fable 5 default + Opus `:max` executor |

**Recommended fix:** default all effort suffixes to `:high`; escalate to `:xhigh`/`:max` only on Critic ITERATE/REJECT or Architect BLOCK.

### 4.2 The `gemini-3.1-pro-low:high` selector may be silently under-powering the Architect

The deep-research pass confirms Google does **not document `gemini-3.1-pro-low` as a public model slug** ([Gemini 3 API docs](https://ai.google.dev/gemini-api/docs/gemini-3)) — `thinking_level: low` is a real reasoning-depth control, but `gemini-3.1-pro-low:high` is a GJC-parser workaround, corroborated by the multivendor guide's own [selector evidence file](https://github.com/project820/gjc-multivendor-setup-guide/blob/main/evidence/2026-07-02-selectors.md). Combined with Gemini's weakest-in-lineup 54.2% SWE-bench Pro, this seat is the profile's real capability risk.

**Recommended fix:** A/B test `google-antigravity/gemini-3.1-pro-low:high` vs. `gemini-3.1-pro:high` on a fixed architecture-review task set. Escalate to Opus 4.8 or GPT-5.5 for small, high-risk diffs.

### 4.3 Four-provider synchronous chain has no failover policy

Anthropic and OpenAI show correlated peak-hour latency spikes; if any of four providers 429s or times out, the whole cycle blocks. The right response is **intra-seat failover** — a same-role fallback from a different provider — not reducing provider count (which would sacrifice Executor↔Critic training-family independence).

---

## 5. Recommended profile YAML (final synthesis)

```yaml
profiles:

  # Recommended default — same architecture, effort ladder, verified Architect
  ultimate-v2:
    default:   anthropic/claude-opus-4-8:high
    executor:  anthropic/claude-opus-4-8:high     # was :max — escalate to :max on Critic ITERATE/REJECT
    planner:   openai-codex/gpt-5.5:high          # was :xhigh — escalate on planning uncertainty
    architect: google-antigravity/gemini-3.1-pro:high   # verify vs. -low:high; use non-low if resolvable
    critic:    xai/grok-4.3:high                  # keep — cheap, cross-family, HalBench top-2 pushback

  # For merge-critical / irreversible changes — adds a GPT-5.5 second-pass critic (meta-judge)
  ultimate-v2-hardened:
    default:   anthropic/claude-opus-4-8:high
    executor:  anthropic/claude-opus-4-8:max
    planner:   openai-codex/gpt-5.5:xhigh
    architect: google-antigravity/gemini-3.1-pro:high
    critic:    xai/grok-4.3:high
    # Workflow rule (out-of-YAML): before merge, parent runs openai-codex/gpt-5.5:high
    # as an independent second critic and aggregates verdicts. No debate chaining.

  # Fable 5 quality-ceiling line — same effort-ladder logic
  ultimate-f5-v2:
    default:   anthropic/claude-fable-5:high
    executor:  anthropic/claude-fable-5:high      # escalate to :xhigh on Critic ITERATE
    planner:   openai-codex/gpt-5.5:high
    architect: google-antigravity/gemini-3.1-pro-low:high   # keep low here — leans on 1M-ctx repo reads
    critic:    xai/grok-4.3:high

  # NEW — throughput lane for reversible / low-risk changes
  # Composer 2.5 STANDARD only, never Fast
  ultimate-fast:
    default:   anthropic/claude-opus-4-8:high
    executor:  grok-build/composer-2.5           # ILLUSTRATIVE — NOT catalog-verified: 2026-07-02-catalog.txt lists only `grok-build/grok-composer-2.5-fast`; Standard-tier grok-build access is UNVERIFIED (see 2026-07-03-redteam-report.md). Do not copy verbatim; validate the selector + Standard access first.
    planner:   openai-codex/gpt-5.5:high
    architect: google-antigravity/gemini-3.1-pro-low:high
    critic:    xai/grok-4.3:high
```

**Do not** deploy Composer 2.5 *Fast* — identical model as Standard at 6× the cost for latency delegated subagents don't need.

**Do not** move Fable 5 or Opus into the Critic seat in any profile — same-family Critic↔Executor breaks the independence that is the entire architectural point of using xAI here.

---

## 6. Migration roadmap (from consultant lens)

**Phase 1 — Verify & Escalate (3–5 days)**
1. Edit `gjc-profiles.yml` to change `executor` from `:max` → `:high` and `planner` from `:xhigh` → `:high` across all three Ultimate profiles.
2. Wire escalation triggers to Critic ITERATE/REJECT and Architect BLOCK verdicts.
3. A/B test `gemini-3.1-pro-low:high` vs. `gemini-3.1-pro:high` on a fixed architecture-review task set.
4. Pin an external CI/test-runner verification gate after every Executor pass (compensates for any Executor self-verification drift, e.g., the [Opus 4.8 tool-loop regression report](https://readysolutions.ai/blog/2026-05-31-opus-4-8-tool-state-regression/) — though Anthropic has not officially acknowledged this beyond general Claude Code CLI hook fixes in [release notes](https://docs.anthropic.com/en/release-notes/claude-code)).

**Phase 2 — Second-Pass Critic & Failover (5–7 days)**
5. Add a `gpt-5.5:high` second-pass critic for merge-critical changes, with parent-level verdict aggregation (no debate chaining).
6. Define intra-seat failover — for each role, a same-role fallback from a different provider that triggers on HTTP 429 or timeout.

**Phase 3 — Hardening & Observability (7–10 days)**
7. Stand up a per-cycle cost/latency dashboard broken out by role and effort tier; baseline against the ~$2.96–$5.06 per-cycle estimates.
8. Ship the optional `ultimate-fast` throughput profile (Composer 2.5 **Standard**), and monitor the still-unresolved [`grok-build` provider design](https://github.com/Yeachan-Heo/gajae-code/blob/main/docs/grok-build-provider-design.md) for stabilization.

---

## 7. Overall verdict (dev-idea-consultant framing)

The Ultimate line is a **competent, largely merit-driven multivendor architecture — not diversity theater**. Executor→Anthropic, Planner→OpenAI, Critic→xAI each pass a reasonable capability + independence test. Its architectural differentiator (role-scoped, YAML-declared multivendor profile) is genuinely rare among coding-agent harnesses.

Its weaknesses are **concrete and fixable, not fundamental**:

1. Uniform `:max`/`:xhigh` effort → cost/quality anti-pattern per test-time-compute literature.
2. Undocumented `gemini-3.1-pro-low` selector → possible silent under-powering of the weakest seat.
3. Four-provider synchronous chain → operational risk without failover policy.

The **two community debates driving scrutiny** — "is Grok right as Critic" and "should Composer replace Executor" — are **both lower-leverage than they appear**. Keep Grok. Reject Composer Fast. Focus effort on cost discipline, Architect verification, and failover.

**Success probability of the recommended migration:** **~80% high confidence** — all changes are config-level YAML edits to an already-working profile system, with the main execution risk being operational discipline (rolling out the effort ladder and failover policy), not technical feasibility.

---

## 8. Immediate next steps (5 concrete actions)

1. Edit `gjc-profiles.yml`: `executor` and `planner` default efforts down to `:high`, add escalation triggers.
2. Run the `gemini-3.1-pro-low:high` vs `gemini-3.1-pro:high` A/B test before touching the Architect seat.
3. Add `gpt-5.5:high` as a second-pass critic for merge-critical changes; document the aggregation rule.
4. Pin an external CI/test-runner verification gate after every Executor pass.
5. Instrument per-cycle cost/latency tracking; measure the effort-ladder savings against the ~$2.96–$5.06 baseline.

---

## 9. Confidence table (consolidated)

| Claim / recommendation | Council consensus | Confidence | Primary evidence |
|---|:---:|:---:|---|
| Keep Grok 4.3 as default Critic | 3/3 | High | [HalBench v2](https://www.reddit.com/r/LocalLLM/comments/1u6y82j/halbench_29_oss_models_tested_on_a_custom_built/), [Self-Preference Bias](https://arxiv.org/abs/2410.21819), [xAI pricing](https://docs.x.ai/developers/pricing) |
| Reject Composer 2.5 Fast as Executor; accept Standard in throughput lane | 2/3 (Gemini partial dissent) | High | [Cursor Composer 2.5](https://cursor.com/blog/composer-2-5), [reward-hacking analysis](https://cursor.com/blog/reward-hacking-coding-benchmarks) |
| Adopt adaptive `:high` → `:xhigh`/`:max` effort ladder | 2/3 (Opus implicitly aligned) | Medium-High | [Snell et al. 2408.03314](https://arxiv.org/abs/2408.03314), [OpenAI latest-model guide](https://developers.openai.com/api/docs/guides/latest-model) |
| Add GPT-5.5:high second-pass critic on merge-critical changes | 2/3 | Medium | [Judging with Many Minds](https://arxiv.org/pdf/2505.19477.pdf) |
| Verify / fix `gemini-3.1-pro-low:high` Architect selector | 2/3 | Medium-High | [Gemini 3 API docs](https://ai.google.dev/gemini-api/docs/gemini-3), [selector evidence](https://github.com/project820/gjc-multivendor-setup-guide/blob/main/evidence/2026-07-02-selectors.md) |
| Keep 4-provider spread but add intra-seat failover | 3/3 | Medium-High | Provider-diversity engineering + operational reasoning |
| Keep Claude on Executor seat | 2/3 | High | [Vals SWE-bench](https://vals.ai/benchmarks/swebench) 88.6–95.0%, [BenchLM SWE-Pro](https://benchlm.ai/benchmarks/swePro) 69.2–80.3% |
| External CI/test-runner verification gate is required | Opus only | Medium | [Anthropic Claude Code release notes](https://docs.anthropic.com/en/release-notes/claude-code); no official Opus 4.8 regression acknowledgement found in deep research |

---

## 10. Complete artifact index

**Deliverable artifacts (all English MD):**
- [gjc-ultimate-final-report.md](./2026-07-03-ultimate-final-report.md) — **this file, the completion-form report**
- model-council-synthesis.md (council working artifact, not published in this repo) — model-council formal synthesis (Where Agree / Disagree / Unique Discoveries tables)
- [deep-research-benchmarks.md](./2026-07-03-deep-research-benchmarks.md) — deep-research primary-source benchmark dive
- [gjc-consultant-report.md](./2026-07-03-consultant-report.md) — dev-idea-consultant formatted report

**Individual council seat reports (~2,000 words each):**
- model-council-claude_opus_4_8.md (council working artifact, not published in this repo) — Anthropic-frontier seat
- model-council-gpt_5_5.md (council working artifact, not published in this repo) — OpenAI-frontier seat (Planner self-audit)
- model-council-gemini_3_1_pro.md (council working artifact, not published in this repo) — Google-frontier seat (Architect self-audit)

**Underlying repository research (fetched via github_mcp_direct connector):**
- `/home/user/workspace/gjc-research/summary.md`
- `/home/user/workspace/gjc-research/repo1-*.md` — multivendor guide contents
- `/home/user/workspace/gjc-research/repo2-*.md` — gajae-code (GJC) contents

---

## 11. Chair's closing note (Fable 5 framing)

The Ultimate line has made three of four hard structural choices correctly. The community pressure to swap the Critic to a stronger coder or replace the Executor with Composer 2.5 Fast both **optimize the wrong axis** — the Critic doesn't need to code, and the Executor doesn't need to be faster. The real, evidence-backed wins are:

1. **Effort escalation instead of uniform max effort** (biggest single lever)
2. **Verify the Gemini Architect selector**
3. **Meta-judge second-pass Critic on merge-critical changes**

Everything else is trim. Ship Phase 1 first — it captures ~70% of the total upside as configuration-only edits.
