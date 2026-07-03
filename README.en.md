<div align="center">

# 🧩 GJC Multi-Vendor Extreme Setup

### claude · gpt · grok · gemini · opencode go — a verified setup that splits 5 subscriptions *by role*

Stop agonizing over model choice. **Install in one line** and let each role get its best-fit model automatically.

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-1.5.5-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/profiles-13-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/selectors-live%20tested%202026--07--02-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="legend setup — strongest model per role" width="100%">

</div>

**[한국어](./README.md) · English (this page) · [中文](./README.zh.md) · [日本語](./README.ja.md)**

> [!NOTE]
> **The core of this guide was adopted into the official GJC docs** — a condensed version was merged upstream as [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md) ([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev`). Treat the **official GJC docs as the canonical reference** for the role/selector concepts; this repo provides what those docs do not — the **one-line installer**, the **full set of 13 profiles** (incl. `solo-*` / `claude-codex*` / `legend` / `cyber-cop`), and [maintenance & validation tooling](./MAINTAINING.md) (static-check CI + live selector battery + catalog drift tracking).

## 🚨 NEW · `cyber-cop` — the first reviewer-mode profile

> The 12 original profiles were all for *writing* code (author mode). **`cyber-cop` is the 13th profile — GJC's first reviewer mode** — for sessions that *gate* code: review someone else's PR, hunt for reasons to block, and adjudicate at the merge gate.

**What's different**
- In PR review / security audits the role weighting **inverts** → **architect (first-pass verdict: CLEAR/WATCH/BLOCK) and critic (merge gate) lead**; executor drops to a supporting repro-PoC / failing-test role.
- The critic runs **cross-family vs the code author (assumed Claude)** (GPT-5.5) → structurally counters self-preference bias ([arXiv 2410.21819](https://arxiv.org/abs/2410.21819)).
- High-risk / security PRs convene a **3-vote parallel panel** (`gpt-5.5` · `grok-4.3` · `gemini-3.1-pro`), independent votes → 2/3 dissent or any CRITICAL/BLOCK blocks.

**Proof it works — this repo dogfooded it**
> Across PRs #4–#7 the review gate **caught multiple real defects before merge**. The review helper was BLOCKed by *its own* prompt-injection flaw (fixed, then passed), and two overclaims the Anthropic base model waved through (a relative-path injection surface and a permission overclaim) were **correctly BLOCKed by the cross-family critic (GPT-5.5)** — proving the self-preference-bias defense works in practice.

**Start in one line**
```bash
GUIDE=/path/to/gjc-multivendor-setup-guide     # this setup-guide repo
cd <repo-under-review>
gjc --mpreset cyber-cop --append-system-prompt "@$GUIDE/routing-rules.md"
# or headless 4-section verdict (set REPO to the target — defaults to this guide repo):
# REPO=owner/name "$GUIDE/scripts/cyber-cop-review.sh" <PR_NUMBER>
```

📖 Full gap argument, 3-step usage, automated review pipeline & security rules → **[cyber-cop announcement](./docs/whats-new-cyber-cop.md)** (Korean canonical)

---

## ⚡ 30-second install (one-line copy-paste)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

This single line **safely merges 13 profiles into `~/.gjc/agent/models.yml`** and sets `daily` as the default profile. Your existing config is backed up automatically, and re-running cleanly updates in place.

```bash
gjc --mpreset daily        # this session only
gjc                        # new sessions use daily automatically
```

> [!IMPORTANT]
> **You must log in to providers after installing.** GJC uses its own OAuth (not shared with the native `agy`/`grok` CLI logins), so open GJC and run each of these once (browser auth):
>
> ```text
> /login anthropic           # claude
> /login openai-codex        # gpt (ChatGPT account → serves base GPT)
> /login google-antigravity  # gemini (Google AI Pro/Ultra subscription)
> /login xai                 # grok full lineup + Composer
> ```
> opencode-go uses an API key: `/provider add`, or the `OPENCODE_API_KEY` env var. Check auth state with `/provider`.

> [!TIP]
> Pick the default profile: `curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash` · skip default-setting: `GJC_SETUP_DEFAULT=none`.

---

## 1. 🎯 Why multi-vendor

Subscribing to claude·gpt·grok·gemini·opencode go and then using only one model means running a *second-best* model in every role. Verified benchmarks show **the leading vendor differs per role**:

| Role | What it does | Best model |
|---|---|---|
| 🧠 **reasoning/planning** (planner) | sequencing, acceptance criteria | **Gemini 3.1 Pro** (GPQA 94.3 / ARC-AGI-2 77.1)† |
| 🔨 **implementation** (executor) | writing/editing real code | **Claude Fable 5** (SWE-bench Verified **95.0**) — strongest *subscription-included* is **Opus 4.8** (88.6) |
| 🔭 **code review** (architect) | large-repo navigation, architecture | **Gemini 3.1 Pro** (multimodal MMMU-Pro 81%)† · ultra-long-context (>200k) → **Opus** |
| ⚖️ **independent critique** (critic) | adversarial verification | **cross-family** (different vendor than the main loop) |
| 🎛️ **orchestration** (default) | tool-calling, routing, honesty | **Anthropic flagship** — Opus 4.8 (router quality caps the whole system; `legend`/`ultimate-f5` use Fable 5) |

> **Benchmark reference date: 2026-07-02** (re-verified right after the Claude 5 family launch). † The reasoning/architect axes have "successors imminent" — GPT-5.6 Sol is in partner preview (6/26, `max` effort + `ultra` sub-agent mode, GA weeks away), and Gemini 3.5 Pro (2M ctx, Deep Think) slipped to July GA. Will re-verify on release.

> Fill all 5 roles from one vendor and at least one role is not the best. This guide fills each of the 5 with its best-fit vendor — weighed against cost, accessibility, and reliability — into a combo that **actually works**. It cross-validates three independent deep-research passes (GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro) and **verifies every profile selector with live calls** ([§6](#6--verification-matrix)).

---

## 2. 🧭 Core design

> **One strong main loop, fixed (default = Anthropic flagship Opus/Fable) + signal-driven delegation + failure-driven effort escalation.**

The only model that runs on every turn is `default` (the main loop). executor/architect/planner/critic are sub-agents the main loop **delegates to via `task` only when warranted** (fresh context).

<div align="center">
<img src="assets/architecture.svg" alt="one main loop (default) + 4 sub-agents — signal-driven delegation" width="100%">
</div>

Three design principles:

- **The main loop is non-negotiable.** Most median tasks are handled by the main loop alone, so dropping `default` to a weak model collapses perceived quality across the board. Always the Anthropic flagship (Opus 4.8 — Fable 5 in `legend`/`ultimate-f5`).
- **Diversity pays off only in *verification*.** Keep `critic` on a different vendor for independence, but keep serial chains short (reliability decays as `0.99ⁿ`).
- **Effort is asymmetric economics.** `medium→high` is +1–2 points for ~23× the tokens. Blindly maxing is waste — escalate only "because it couldn't solve it."

---

## 3. 🔧 GJC engine facts

### 3-1. The five roles

| Role | Where it runs | Top priority |
|---|---|---|
| `default` | **main loop** | tool-calling reliability · honesty |
| `executor` | sub-agent (only on `task` delegation) | real coding (SWE-bench) |
| `architect` | sub-agent | large-ctx · multimodal code review |
| `planner` | sub-agent | top-tier reasoning · sequencing |
| `critic` | sub-agent | independent adversarial critique |

### 3-2. Effort cheatsheet

These are the **GJC 0.7.10 effective** tiers — some differ from the official API spec (footnote below):

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← all 6 tiers
Fable 5                 minimal low medium high xhigh       ← :max silently clamps to xhigh · thinking always-on
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max silently clamp to high
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 defaults to xhigh
Grok 4.x (xai)          minimal low medium high              ← grok-4.3 :xhigh silently clamps to high
grok-build/grok-4.3     ── bare selector only (effort suffixes don't resolve) ──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go others       ── omit the :effort suffix (default) ──
google-antigravity Gemini  gemini-3.1-pro-low:high (high reasoning) · gemini-3.1-pro-low (low effort)
```

> [!IMPORTANT]
> **Five hard rules**: ① Gemini Pro supports only `low`/`high` ② openai-codex ctx is **per-model** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K** (shrank from 400K; the old blanket "codex 272k" rule is retired) ③ Sonnet (4.6/5) cannot do `xhigh`/`max` in GJC · **Fable 5 cannot do `max`** (clamped to high / xhigh respectively) ④ opencode-go: omit `:effort` (only the deepseek-v4 family supports it) ⑤ xai `grok-4.3` caps at `high` (`:xhigh` silently clamps — xhigh exists only on the grok-build provider, where effort suffixes don't resolve at all). Out-of-range tiers are **clamped**, not errored.
>
> **Footnote (upstream gap)**: per the official API, both Claude 5 models support up to `max`. The GJC 0.7.10 parser doesn't know the fable family (falls back to inferred rules) and sonnet-5 inherits the 4.6 clamp — an **engine-side gap, reported upstream** with a repro. This guide records the GJC-effective tiers.

### 3-3. Subscription → provider

| Subscription | provider-id | Notes |
|---|---|---|
| claude | `anthropic` | all efforts. Includes the Claude 5 family (Fable 5 · Sonnet 5) |
| gpt | `openai-codex` | **ChatGPT account → serves base GPT (gpt-5.5/5.4)**. ctx: gpt-5.4=1M · gpt-5.5=272K |
| grok | `xai` | full lineup + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra subscription token**. Gemini + bundled Claude (Opus 4.6 — bundle composition not re-checked since the Claude 5 launch) |
| opencode go | `opencode-go` | API key (`OPENCODE_API_KEY`) |

> [!NOTE]
> **openai-codex path caveat**: logging in with a ChatGPT (Codex) account serves the **base GPT models (`gpt-5.5`, `gpt-5.4`)**. Standalone `-codex` variants (`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex-max/mini`) are **not supported** on this path (`not supported when using Codex with a ChatGPT account`), so this guide uses verified **base GPT** for coding roles too.
>
> Alternative paths: `google-vertex` (API key, paid per-token, 1M ctx) — a fallback independent of subscription/quota. Another is **DeepInfra** (new GJC provider since 0.7.9, API key): DeepSeek V4 Pro **$1.30/$2.60** (1M ctx) · V4 Flash $0.09/$0.18 — its Standard/Priority (1.5×) tiers map directly onto GJC's `service-tier` setting.

### 3-4. Selector syntax

```text
<provider-id>/<model-id>:<effort>            e.g. anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   (Gemini high reasoning — the engine's canonical path)
opencode-go/<model>                           (omit effort = model default)
```

---

## 4. 📊 Benchmark basis

**Verified per-role leader** (vals.ai independent boards · official model cards — **as of 2026-07-02**)

| Role (axis) | Leader | Figure |
|---|---|---|
| executor (SWE-bench Verified) | **Fable 5** | **95.0%** (Opus 4.8 88.6 = **strongest subscription-included** · GPT-5.5 82.6 · Gemini 3.1 Pro 80.6) |
| planner (reasoning GPQA/ARC-AGI) | **Gemini 3.1 Pro**† | GPQA 94.3 · ARC-AGI-2 77.1 (fluid reasoning: GPT-5.5 — [§6-2 (KO)](./README.md#6-2-역할-배치-최적성-검토-deep-research--실측) · standalone GPQA #1 is Sonnet 5 at 96.2) |
| architect (ctx · multimodal) | **Gemini 3.1 Pro**† | 1M ctx · MMMU-Pro 81% |
| default (tool-calling · honesty) | **Opus 4.8 / Fable 5** | router quality = whole-system ceiling (Fable carries refusal/billing caveats — [§5](#5-️-final-catalog-13-profiles)) |
| critic (independence) | **cross-family** | meta-judge > debate aggregation |

> † **Successors imminent**: on the planner axis, GPT-5.6 Sol is in partner preview (2026-06-26, `max` effort + `ultra` sub-agent mode — GA weeks away); on the architect axis, Gemini 3.5 Pro (2M ctx, Deep Think) slipped to July GA. Either release puts this table up for re-verification.

**Consensus principles**

1. **default = Anthropic flagship (Opus/Fable), fixed** (multi-vendor profiles) — router quality is the whole-system ceiling. `solo-*` use the single vendor's strongest as default.
2. **architect = Gemini 3.1 Pro (multimodal) / Opus (ultra-long-context)** — Gemini is best for vision and mid ctx; for 200k+ text retrieval use Opus (MRCR 76%@1M, where Gemini collapses to 26%).
3. **critic = cross-family** — a different vendor than the main loop/planner mitigates self-preference bias.
4. **Structure = strong main loop + signal-driven delegation + failure-driven effort escalation.**
5. **No per-query profile swapping** — cache loss > benefit. Swap only at mode boundaries.

> Benchmarks are time-sensitive → re-verify quarterly. Absolute rankings limited to vals.ai independent boards.

---

## 5. 🗂️ Final catalog (13 profiles)

<div align="center">
<img src="assets/profiles-matrix.svg" alt="profiles × roles matrix" width="100%">
</div>

> ★ = everyday recommendation. The top banner = the **`legend` setup** (sustainable strongest — only `default` on Fable 5). The everyday cost-balanced pick is **`daily`** (executor·critic swapped to cheaper). Multi-vendor profiles keep `default = Anthropic flagship (Opus/Fable)` and `critic = cross-family` (solo-* use the single vendor's strongest); all pass the engine effort hard-rules and **every selector is live-verified** ([§6](#6--verification-matrix)).

| Profile | One-liner | Use when |
|---|---|---|
| ⭐ **daily** | Opus main loop + delegation to each role's best vendor | **everyday default** |
| 🏆 **ultimate** | cost-no-object, best per role (sustainable edition) | accuracy matters more than cost |
| 🔥 **ultimate-f5** | Fable 5-centric event edition — **subscription-included through 2026-07-07** | peak accuracy during the event window |
| 👑 **legend** | only the main loop on Fable 5; the rest stays sustainable | strongest setup that stays viable after 7/7 |
| 🏎️ **coding-sprint** | executor-led + coding-aware critic | pure implementation throughput |
| 🛡️ **escalation** | Fable 5 rescue pitcher on failure signals + multi-vendor critic panel | merges · security · billing · irreversible changes |
| 🚨 **cyber-cop** | reviewer mode — architect & critic in the lead, dedicated to PR review & security audits | reviewing others' PRs · merge gates · security audits |
| 💸 **eco** | only the main loop is Opus; delegation all cheap/subscription | cost pressure · bulk work |
| 🗺️ **monorepo** | ≥1M ctx everywhere (gpt-5.5 excluded) | huge codebases |
| 🧱 **solo-anthropic** | every role on Opus (v1.4: critic on Opus too) | single-vendor operation |
| 🤖 **solo-openai** | every role on base GPT (5.5=272K · 5.4=1M) | ChatGPT-only subscriber |
| 🤝 **claude-codex** | Claude = execution/ctx, Codex = reasoning/critique | Claude + Codex (2 subs only) |
| 🥇 **claude-codex-max** | cost-no-object version of claude-codex | Claude + Codex · accuracy first |

<details>
<summary><b>📋 Expand the full YAML (identical to gjc-profiles.yml — by model mapping; only §refs in comments adapted for the README)</b></summary>

```yaml
profiles:

  daily:                               # ★ everyday default (--default daily)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # main-loop efficiency knee
      executor:  openai-codex/gpt-5.4:high                      # coding-focused · mid price ($2.5/15) · vendor spread (verified✅)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # verified #1 reasoning (GPQA 94.3 / ARC-AGI-2 77.1)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx · multimodal (MMMU-Pro 81%)
      critic:    xai/grok-4.3:medium                            # cross-family cheap independent critic ($1.25/2.5)

  ultimate:                            # cost-no-object, best per role + vendor spread (sustainable edition — event edition is ultimate-f5)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # strongest subscription-included coder (SWE-bench Verified 88.6)
      planner:   openai-codex/gpt-5.5:xhigh                     # top reasoning + OpenAI diversity
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx · multimodal
      critic:    xai/grok-4.3:high                              # cross-family independent critic

  ultimate-f5:                         # 🔥 event: Fable 5-centric — subscription-included through ~2026-07-07 (50% weekly-limit cap), then usage credits ($10/$50)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # router = quality ceiling. beware refusal (HTTP 200 + stop_reason)
      executor:  anthropic/claude-fable-5:xhigh                 # SWE-bench Verified 95.0 new #1. ⚠never :max (silently clamps to xhigh)
      planner:   openai-codex/gpt-5.5:xhigh                     # reasoning axis unproven for Fable (ARC-AGI-2 unpublished) — keep GPT
      architect: google-antigravity/gemini-3.1-pro-low:high     # keeps the verified multimodal lead (Fable vision is vendor-claimed)
      critic:    xai/grok-4.3:high                              # cross-family invariant — no Fable self-review
      # after 7/7: lower default to opus-4-8:high for the same sustainable structure as legend

  legend:                              # 👑 Ultimate Legend — strongest that stays viable after 7/7 (fable on the default seat only)
    display_name: legend5
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # router quality ceiling = Fable (minimal usage-credits exposure)
      executor:  anthropic/claude-opus-4-8:max                  # strongest subscription-included coder (88.6)
      planner:   openai-codex/gpt-5.5:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.3:high
      # to avoid credits cost: set default to opus-4-8:high — becomes identical to ultimate

  coding-sprint:                       # implementation throughput. executor-led + coding-aware critic
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # main-loop orchestration
      executor:  anthropic/claude-opus-4-8:max                  # strongest subscription-included coder (88.6)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # #1 reasoning for lightweight planning
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx review
      critic:    openai-codex/gpt-5.4:high                      # coding-aware critic (catches real bugs), cross-family vs gemini

  escalation:                          # high failure cost — on failure signals, deploy the strongest executor (Fable 5) + multi-vendor critic panel (§9)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-fable-5:xhigh                 # rescue pitcher for failed tasks (SWE-V 95.0). intermittent use also fits credits billing
      planner:   openai-codex/gpt-5.5:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.3:high                              # + 3-vote cross-vendor critic panel (independent vote → main loop tallies). ⚠xai :xhigh silently clamps to high, so unused
      # (the critic :xhigh used through v1.3 was a no-op clamp — xhigh exists only on the grok-build provider, which doesn't resolve effort suffixes)

  cyber-cop:                           # 🚨 reviewer mode — PR review & security audit (inverse of author mode)
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high                 # invariant-compliant + 1M ctx. Aggregator-only — preserve/expose raw critic verdicts (routing-rules contract)
      executor:  openai-codex/gpt-5.5:high                      # supporting role — repro PoCs, failing tests, harnesses (Terminal-Bench 82.7)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # review checklists & audit scoping (cross-family vs critic)
      architect: anthropic/claude-opus-4-8:high                 # lead #1 — primary code-review judge, 1M effective retrieval (MRCR 76% vs Gemini 26%)
      critic:    openai-codex/gpt-5.5:high                      # lead #2 — merge gate, cross-family vs Claude-authored code
      # High-risk PRs / security audits: 3-vote parallel critic panel {openai-codex/gpt-5.5:high, xai/grok-4.3:high,
      # google-antigravity/gemini-3.1-pro-low:high} — independent votes aggregated by the main loop (no debate); block on 2/3 rejection or any CRITICAL/BLOCK
      # (3rd vote (grok) requires xai login — without it, 2 votes {gpt-5.5, gemini} still meet the provenance minimum of ≥2 non-default families)

  eco:                                 # cheapest — only the main loop is Opus (effort trimmed), delegation ultra-cheap/subscription (all verified✅)
    required_providers: [anthropic, opencode-go, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:low                  # can't lower the router, only its effort
      executor:  opencode-go/deepseek-v4-flash                  # $0.14/0.28, 1M, cheapest coder (5th vendor). alt: sonnet-5:medium (≈sonnet-4-6:high, intro $2/10 thru 8/31)
      planner:   xai/grok-4-1-fast:high                         # $0.2/0.5, 2M, cheap reasoning
      architect: google-antigravity/gemini-3.1-pro-low          # subscription token, low effort, 1M ctx
      critic:    google-antigravity/gemini-3.5-flash-low        # subscription token, light, cross-family vs executor (opencode-go). literal-id pin (old 'gemini-3.5-flash' was fuzzy matching)

  monorepo:                            # huge codebases — ≥1M ctx everywhere (★gpt-5.5 272K excluded — gpt-5.4 is 1M but Opus ranks at least equal)
    required_providers: [anthropic, google-antigravity, opencode-go]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 1M
      executor:  anthropic/claude-opus-4-8:high                 # 1M
      planner:   google-antigravity/gemini-3.1-pro-low:high     # reasoning (scoped input)
      architect: anthropic/claude-opus-4-8:high                 # Opus 4.8 = GJC 1M ctx window (best multi-turn accumulation/retrieval). single-message paste cap only ~400k — for one-shot >400k use opencode-go/deepseek-v4-pro
      critic:    opencode-go/glm-5.2                            # open-weight #1 (AA 51 > V4 Pro 44), in the 0.7.10 bundled catalog, cross-family vs anthropic (alt: deepseek-v4-pro)

  solo-anthropic:                      # single-vendor operation — every role on Opus (v1.4: critic Sonnet→Opus, capability first)
    required_providers: [anthropic]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max
      planner:   anthropic/claude-opus-4-8:max
      architect: anthropic/claude-opus-4-8:high                 # 1M, Gemini replacement (fallback #1)
      critic:    anthropic/claude-opus-4-8:high                 # ⚠same-model self-review = maximal bias (research-confirmed) — the quality path is the cross-family profiles
      # Sonnet 5 critic not recommended: measured reviewer bug recall dropped (63%→50%, only precision rose)

  solo-openai:                         # ChatGPT (Codex) account only — base GPT only
    required_providers: [openai-codex]
    model_mapping:
      default:   openai-codex/gpt-5.5:high                      # router (strongest base GPT, ctx 272K)
      executor:  openai-codex/gpt-5.5:xhigh                     # this account's strongest coder
      planner:   openai-codex/gpt-5.5:xhigh                     # top reasoning
      architect: openai-codex/gpt-5.4:high                      # ★gpt-5.4 = 1M ctx — route large inputs here (5.5 is 272K)
      critic:    openai-codex/gpt-5.4:high                      # ⚠same vendor = weak independence (tradeoff)

  claude-codex:                        # ★Claude+Codex (2 subs) only — everyday balance. Anthropic = execution/ctx, Codex = reasoning/critique
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # router · tool reliability
      executor:  anthropic/claude-opus-4-8:high                 # strongest subscription-included coder (SWE-bench 88.6)
      planner:   openai-codex/gpt-5.5:high                      # OpenAI reasoning flagship
      architect: anthropic/claude-opus-4-8:high                 # 1M window (avoids gpt-5.5's 272K limit)
      critic:    openai-codex/gpt-5.4:high                      # cross-family vs Opus (executor), coding-aware

  claude-codex-max:                    # Claude+Codex (2 subs) strongest — cost-no-object
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # SWE-bench 88.6
      planner:   openai-codex/gpt-5.5:xhigh                     # top reasoning (strong ARC-AGI-2)
      architect: anthropic/claude-opus-4-8:high                 # 1M window
      critic:    openai-codex/gpt-5.5:high                      # cross-family independent critique vs Opus

# ─────────────────────────────────────────────────────────────────────────────
# Claude 5 family (2026-07-01–): Fable 5 = $10/$50 (2× Opus); subscription-included only through ~7/7 (50% of weekly limits) — NOT "free".
#   Sonnet 5 = $3/$15 (intro $2/$10 through 2026-08-31); tokenizer change makes the same text ~30% more tokens.
#   GJC-effective effort: fable-5 ≤xhigh · sonnet-5 ≤high (the API supports max on both — GJC parser gap, reported upstream).
# opencode-go: active once OPENCODE_API_KEY is set (used by eco.executor · monorepo.critic).
#   verified✅: deepseek-v4-flash/pro · glm-5.2 · minimax-m2.7 · qwen3.7-max · kimi-k2.6 · mimo-v2.5.
#   new arrivals (unverified candidates): kimi-k2.7-code (strong budget-executor candidate) · minimax-m3 (1M multimodal).
# Optional: the grok subscription's (SuperGrok OAuth) grok-build/composer also work:
#   grok-build/grok-4.3 (bare selector only; effort suffixes unsupported — verified✅ 2026-07-02).
```

</details>

For the per-profile design rationale — including the `ultimate-f5` event terms (**subscription-included through 2026-07-07**, capped at 50% of weekly limits, then usage credits $10/$50 — never "free"), the `legend` default-seat-only Fable placement, the `escalation` rescue-pitcher redesign (and the honest record that its v1.3 critic `:xhigh` was a no-op clamp), and the all-Opus `solo-anthropic` caveat (research shows **stronger models exhibit stronger self-preference bias** — arXiv [2410.21819](https://arxiv.org/abs/2410.21819) · [2604.22891](https://arxiv.org/abs/2604.22891) — so all-Opus is a capability-first choice and **cross-family profiles remain the quality path**) — plus the opencode-go extras, see the **[Korean canonical README](./README.md#5-️-최종-카탈로그-13종)** and the official **[GJC docs](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)**.

---

## 6. ✅ Verification matrix

> Every selector was **actually called** in this environment via `gjc -p --no-session --no-tools --model <sel> "..."` (**final verification 2026-07-02, gjc 0.7.10** — entries without an explicit date were verified 2026-06-18; core selectors were re-verified by the 0.7.10 regression battery (marked 07-02✅)). "Works" means a real call, not a guess.

| Provider | Verified selectors (✅ working) |
|---|---|
| `anthropic` | `claude-fable-5` (bare·low·medium·high — `:max` works but **silently clamps to xhigh**, 07-02✅) · `claude-sonnet-5` (bare·medium·high — `:max` works but **silently clamps to high**, 07-02✅) · `claude-opus-4-8` (low·medium·high·max; `:high` re-verified 07-02✅) · `claude-sonnet-4-6:high` (re-verified 07-02✅) |
| `openai-codex` | `gpt-5.5:high` (**re-verified 07-02 after re-auth✅**) · `gpt-5.5:xhigh` · `gpt-5.4:high` · `gpt-5.4-mini:high` |
| `xai` | `grok-4.3:high` (re-verified 07-02✅ — `:xhigh` silently clamps to high) · `grok-4-1-fast:high` (07-02✅) · `grok-4-fast:high` (07-02✅) · `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3` (**bare selector only** — effort suffixes don't resolve, 07-02✅. SuperGrok OAuth) |
| `google-antigravity` | `gemini-3.1-pro-low` (±`:high`, re-verified 07-02✅) · `gemini-3.5-flash-low` (**newly pinned**, 07-02✅) · `gemini-3.5-flash` (works via fuzzy matching, 07-02✅) · `gemini-3-flash` · `claude-opus-4-6-thinking` (06-18 — bundle composition not re-checked since the Claude 5 launch) |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro` (re-verified 07-02✅) · `glm-5.2` (**in the 0.7.10 bundled catalog**, 07-02✅) · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` (needs `OPENCODE_API_KEY`) |

> [!WARNING]
> **Selectors that did NOT work here** (avoid): `openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini` (unsupported on ChatGPT accounts) · `google-antigravity/gemini-3.1-pro-high` (**appears in the 0.7.10 catalog listing but calls still return 400** — the documented trap stands; the engine uses `gemini-3.1-pro-low:high`) · `gemini-3-pro` (retired) · `claude-sonnet-4-6-thinking` (404) · `gpt-oss-120b` (500). `opencode-go/*` fails **only when `OPENCODE_API_KEY` is unset** (works per the table once set). Note: `fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.3:xhigh` are not failures — they **silently clamp** ([§3-2](#3-2-effort-cheatsheet)).

> [!NOTE]
> `opencode-go/glm-5.2` joined the **bundled catalog in 0.7.10** (the old "live-catalog only" caveat is retired). Conversely, the `google-antigravity/gemini-3.5-flash` literal id is not in the catalog (only `-low`/`-extra-low` exist) and **worked only via fuzzy matching**, so the v1.4 profiles pin `gemini-3.5-flash-low`. With a stale discovery cache, activation can fail with `selector did not resolve` — re-login/retry to refresh the catalog, or substitute a bundled id (`opencode-go/deepseek-v4-pro` for the critic, or `zai/glm-5.2` — add `zai` to `required_providers`).

**Latency reference** (micro-bench 2026-07-02 — identical coding/reasoning prompts, every selector correct):

| Selector | Coding | Reasoning | Notes |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **fastest overall** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | +3~4s vs sonnet-5 on coding |
| `grok-4.3:high` | 5.6s | 4.0s | |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | coding-latency outlier |
| `glm-5.2` | **21.9s** | 4.0s | slowest at coding — fine for critic |

Reproduce:
```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.4:high" "Reply exactly: OK"
```

> **Deep role-placement review and the GJC effective-context measurements** (§6-2 / §6-3 in the Korean canonical) confirmed the skeleton and drove the v1.4 changes: the executor axis flipped to **Fable 5** (SWE-bench Verified 95.0 vs Opus 4.8 88.6 — Opus stays "strongest subscription-included"); the planner reasoning axis splits (GPQA is saturated — standalone #1 is now Sonnet 5 at 96.2 — while GPT-5.5 clearly leads ARC-AGI-2 fluid reasoning, so planner stays GPT-5.5); `gemini-3.1-pro-low:high` invokes Gemini's native high-reasoning mode (not a degraded one); Opus holds 1M-context retrieval where Gemini collapses (hence monorepo architect = Opus, and the "Grok 2M architect" swap was rejected outright); and the single-message `@file` input cap (~400k on anthropic/antigravity) is separate from the 1M context window — chunk huge inputs across turns to keep the full window. Full tables: **[Korean README §6](./README.md#6--검증-매트릭스)**.

---

## 7. 🛠️ Install / uninstall

### One-click (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

What the installer does: safely merges the 13 profiles into `~/.gjc/agent/models.yml` (auto-updates on re-run), backs up existing files, and sets `daily` as default. Needs only `curl` + `python3`.

```bash
# options
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash    # pick default profile
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash        # skip default-setting
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash    # override agent dir
```

### Provider auth (required)

Install only lays down the profiles. Open GJC and log in to each vendor once:

```text
/login anthropic           # claude
/login openai-codex        # gpt (base GPT)
/login google-antigravity  # gemini (Google AI Pro/Ultra subscription)
/login xai                 # grok full lineup + Composer
```

opencode-go: `/provider add` or the `OPENCODE_API_KEY` env var.

### Manual install / verify / uninstall

Paste the `profiles:` block from [`gjc-profiles.yml`](./gjc-profiles.yml) under `profiles:` in `~/.gjc/agent/models.yml`, then `gjc --mpreset daily --default`.

```bash
gjc --list-models daily                       # confirm
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # revert (restore backup)
```

> [!WARNING]
> **GJC 0.7.10 preset rename/delete caveat**: the engine's custom-preset rename/delete features **strip all comments** from `models.yml` — including the installer's managed-block sentinels — which degrades updates to name-based replacement, so **profiles you deleted can resurrect on reinstall** (reproduced). After using rename/delete, double-check the result when reinstalling; for guaranteed full removal, restoring a backup (`cp … .bak-*`) is the safest path.

---

## 8. 🔀 Dynamic routing

> **"Swap profile per query" ❌ / "one strong main loop + one thin rule layer" ✅.** The router is the main loop (the Anthropic flagship); profiles are the destination pool.

> [!TIP]
> To make the main loop follow the routing rules below, put [`routing-rules.md`](./routing-rules.md) (Korean; selectors are language-neutral) in your project `AGENTS.md`, or inject it via `gjc --append-system-prompt @routing-rules.md` (installed profiles + verified-selector hard-rules + GJC effective ctx caps, all in one file).

### 8-1. Work signal → delegation

<div align="center">
<img src="assets/routing-tree.svg" alt="work signal → delegation routing" width="100%">
</div>

Rule: **delegate only when the signal is clear.** If the main loop can do it directly, it does.

### 8-2. Adaptive effort escalation

<div align="center">
<img src="assets/effort-ladder.svg" alt="adaptive effort escalation" width="100%">
</div>

- ✅ Raising because it couldn't solve it is valid / ❌ "raising to be safe" is waste.
- No minimal. Floor at `low`. Gemini does a single `low↔high` jump.

### 8-3. Profile swap (mode boundaries only)

| Signal | Swap → |
|---|---|
| session start · general work | `daily` |
| pre-merge/release · security · billing | `escalation` |
| PR review / security-audit session | `cyber-cop` |
| accuracy above all (Fable 5 event through 2026-07-07) | `ultimate-f5` → afterwards `legend` |
| bulk refactor · migration | `eco` |
| entering a huge codebase | `monorepo` |
| single-vendor operation | `solo-anthropic` |

---

## 9. 🧪 Parallel agents + reliability

Serial hand-offs decay as `0.99ⁿ`, and multi-agent setups, wired wrong, harden into "false consensus." Design parallelism to defend against both.

```text
serial chain, 5 steps (0.99 each):  0.99^5 ≈ 95.1%    → collapses with length
parallel independent, 5 (OR-success): 1-(0.01)^5 ≈ 100%  → diversity raises reliability
```

**Design principles**
- critic = **different vendor from the main loop, parallel independent vote, then the main loop tallies** (no debate — meta-judge wins).
- critic panel example: `{xai/grok-4.3, openai-codex/gpt-5.4, google-antigravity/gemini-3.1-pro-low:high}` in parallel → discard if 2/3 reject.
- executor fan-out only when **the work is truly independent** (no shared state).
- keep chains short, main loop as the single source of truth (no direct sub-agent consensus).

---

## 10. 💰 Cost

Gemini (`google-antigravity`) runs on the **Google AI Pro/Ultra subscription token** (included in the subscription, not per-token billed). **Fable 5 is included in Claude subscriptions (Pro/Max/Team) through 2026-07-07** — capped at 50% of your weekly usage limits — and **billed separately via usage credits afterwards**; it is **not "free."** The rest are per-token; key model prices ($/1M, in/out):

| Model | $/1M (in/out) | Role |
|---|---|---|
| Claude Fable 5 | 10 / 50 (batch 5/25 · cache hits 1)† | ultimate-f5 default·executor · legend default · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor |
| Claude Sonnet 5 | 3 / 15 (intro 2/10 through 2026-08-31)‡ | eco executor alternative |
| GPT-5.5 | 5 / 30 | planner (ultimate) |
| GPT-5.4 | 2.5 / 15 | executor/critic (daily·sprint) |
| Grok 4.3 | 1.25 / 2.5 | critic |
| Grok 4.1 Fast | 0.2 / 0.5 | eco planner |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k single-paste fallback |
| Gemini 3.1 Pro / 3.5 Flash | subscription token | planner·architect·critic |

> † Fable 5 is exactly 2× Opus pricing. The subscription-included window (through ~7/7) still consumes your weekly limits.
> ‡ Sonnet 5's **tokenizer change makes the same text ~30% more tokens** — budget its effective cost above the sticker price.
> (Note: via the DeepInfra provider, DeepSeek V4 Pro is $1.30/$2.60 — [§3-3](#3-3-subscription--provider).)

**Relative profile cost**

| Profile | Cost | Main driver |
|---|---|---|
| ultimate-f5 | ●●●●● | default·executor Fable 5 — subscription-included through ~7/7 (50% weekly-limit cap), then credits $10/50 |
| legend | ●●●●● | default Fable 5 (credits after 7/7) + executor Opus `:max` |
| ultimate / escalation | ●●●●● | executor Opus `:max` / Fable `:xhigh` (rescue pitcher) + planner GPT-5.5 `:xhigh` |
| coding-sprint | ●●●●○ | executor Opus `:max` |
| solo-anthropic | ●●●●○ | all roles Opus (executor/planner `:max`) |
| daily | ●●●○○ | main loop Opus `:medium`, delegation mid/cheap |
| monorepo | ●●●○○ | executor/architect Opus + Gemini (subscription) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash ($0.14) + subscription Gemini |

> **Three savings levers**: ① push delegated work onto ultra-cheap models (DeepSeek V4 Flash $0.14, Grok Fast $0.2) / subscription tokens (Gemini) ② escalate effort only on failure ③ keep the main loop on the Anthropic flagship (it's the quality ceiling) but `:medium` for everyday, `:low` under cost pressure — and if the Fable default's credits (`legend`) get heavy, drop default to `opus-4-8:high`.

---

## 11. 📖 Sources

**Coding (executor)** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.0](https://www.tbench.ai/leaderboard/terminal-bench/2.0)

**Claude 5 family** · [Fable 5 redeployment announcement](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com model docs](https://platform.claude.com/docs) — pricing · subscription inclusion (~7/7) · effort specs cross-checked 2026-07-02

**Reasoning (planner)** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**ctx · multimodal (architect)** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**Tool-calling · honesty (default)** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**Independence · routing (critic + design)** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [self-preference grows with capability](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**Official models/pricing** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**Install in one line, best model per role.**

**v1.5** · [CHANGELOG](./CHANGELOG.md) · [Maintenance playbook](./MAINTAINING.md) · License [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
