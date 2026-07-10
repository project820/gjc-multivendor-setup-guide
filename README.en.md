<div align="center">

# 🧩 GJC Multi-Vendor Extreme Setup

### claude · gpt · grok · gemini · opencode go — a verified setup that splits 5 subscriptions *by role*

Stop agonizing over model choice. **Install in one line** and let each role get its best-fit model automatically.

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-2.0.1-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/bundles-10%20·%204%20tiers-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="dream-team setup — strongest hypothesis per role" width="100%">

</div>

**[한국어](./README.md) · English (this page) · [中文](./README.zh.md) · [日本語](./README.ja.md)**

> [!NOTE]
> The role and selector concepts were merged into the [official GJC docs](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md) ([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev`). This repo provides the one-line installer, the 4-tier 10-bundle catalog, and [maintenance and validation tools](./MAINTAINING.md).

---

## ⚡ 30-second install

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

This one line **safely merges 10 bundles into `~/.gjc/agent/models.yml`** and sets `daily` as the default profile. Existing settings are backed up automatically; re-running updates cleanly.

```bash
gjc --mpreset daily        # this session only
gjc                        # new sessions use daily automatically
```

> [!IMPORTANT]
> **Log in to providers after installing.** GJC OAuth is separate from native `agy`/`grok` CLI logins. Run these once in GJC:
>
> ```text
> /login anthropic           # claude
> /login openai-codex        # gpt (ChatGPT account → base GPT)
> /login google-antigravity  # gemini (Google AI Pro/Ultra subscription)
> /login xai                 # grok full lineup + Composer
> ```
> opencode-go uses an API key: `/provider add` or `OPENCODE_API_KEY`. Check auth with `/provider`.

> [!TIP]
> Pick the default profile: `curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash` · skip default-setting: `GJC_SETUP_DEFAULT=none`.

---

## 🧭 Which bundle?

| Tier | Bundle | One-liner | Use when |
|---|---|---|---|
| Core | ⭐ **daily** | Opus main loop + role-split delegation — **activates with subscription OAuth across 3 vendors only** | **everyday default** |
| Core | 🏎️ **coding-sprint** | implementation-throughput bundle with executor promoted to Opus | pure implementation sprint |
| Core | 🚨 **cyber-cop** | reviewer mode — architect and critic lead, dedicated to PR review and security audits | reviewing others' PRs · merge gates · security audits |
| Premium (exp) | 🏆 **ultimate-opus** | Anthropic-quality premium baseline | accuracy matters more than cost |
| Premium (exp) | 🧪 **ultimate-sol** | Sol-baseline premium — agentic/terminal/browser axis | long autonomous workflow experiments |
| Premium (exp) | 🔥 **dream-team** | strongest-per-role hypothesis — Fable default+executor | highest quality, credits accepted |
| Workflow | 🏛️ **llm-council** | 4-family seating chart and Council contract | decisions needing multi-family consensus |
| Workflow | 🛡️ **escalation** | manual escalation — Fable rescue pitcher + 3-vote critic panel | merges · security · billing · irreversible changes |
| Specialized (exp) | 💸 **eco** | low-cost multi-vendor experiment — *not absolute cheapest* | cost pressure · bulk work |
| Specialized (exp) | 🗺️ **monorepo** | ≥1M ctx everywhere | huge codebases |

Full catalog: [§5](#5-️-final-catalog--10-bundles--4-tiers) · reviewer mode and teasers below.

> **🚨 cyber-cop** — GJC's first reviewer mode: architect and critic lead while executor supports reproduction. High-risk PRs use a 3-vote panel; it blocked 10 defects before merge across PRs #4–#7.
> `gjc-cop 123`
> → [Announcement](./docs/whats-new-cyber-cop.md)

> **Extragoal — GPT-5.5 Pro final-review lane (opt-in)** — Put Pro deep reasoning in the final, round-one decision seat for development, QA, and security review. The upstream default lane works without it; install it with `GJC_SETUP_EXTRAGOAL=1`.
> → [Extragoal Maximalist](./docs/extragoal-maximalist.md)

---

## 1. 🎯 Why multi-vendor

| Role | What it does | Best model |
|---|---|---|
| 🧠 **reasoning/planning** (planner) | sequencing, acceptance criteria | **GPT-5.6 Sol** (Agents' Last Exam 52.7 · GA 2026-07-09)† — bundle-specific seats: see §5 (exceptions: cyber-cop/monorepo=Gemini, eco=Luna) |
| 🔨 **implementation** (executor) | writing/editing real code | **Claude Fable 5** (SWE-bench Verified **95.0**) — strongest *subscription-included* is **Opus 4.8** (88.6) |
| 🔭 **code review** (architect) | large-repo navigation, architecture | **Gemini 3.1 Pro** (multimodal MMMU-Pro 81%)† · ultra-long-context (>200k) → **Opus** |
| ⚖️ **independent critique** (critic) | adversarial verification | **cross-family** (different vendor than the main loop) |
| 🎛️ **orchestration** (default) | tool-calling, routing, honesty | **Anthropic flagship** — Opus 4.8 (router quality caps the whole system; `dream-team` uses Fable 5. The only non-Anthropic routers are opt-in `ultimate-sol` (Sol) and Anthropic-free `eco` (Terra)) |

---

## 2. 🧭 Core design

> **One strong main loop, fixed (default = Anthropic flagship Opus/Fable) + signal-driven delegation + failure-driven effort escalation.**

<div align="center">

<img src="assets/architecture.svg" alt="one main loop (default) + 4 sub-agents — signal-driven delegation" width="100%">

</div>

Three design principles:

- **The main loop is non-negotiable.** Most median tasks are handled by the main loop alone, so dropping `default` to a weak model collapses perceived quality across the board. Default to the Anthropic flagship (Opus 4.8 — Fable 5 in `dream-team`). Only two non-Anthropic routers exist: the opt-in `ultimate-sol` experiment (Sol — validator-listed, WARN surfaced) and the Anthropic-free `eco` (Terra — the router invariant does not apply).
- **Diversity pays off only in *verification*.** Keep `critic` on a different vendor for independence, but keep serial chains short (reliability decays as `0.99ⁿ`).
- **Effort is asymmetric economics.** `medium→high` is +1–2 points for ~23× the tokens. Blindly maxing is waste — escalate only because it could not solve the work.

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

These are the **GJC 0.9.6 effective** tiers (2026-07-10 live-call battery) — some differ from the official API specification:

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← all 6 tiers
Fable 5                 minimal low medium high xhigh       ← :max silently clamps to xhigh · thinking always-on
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max silently clamp to high
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 defaults to xhigh
GPT 5.6 Sol/Terra/Luna  low medium high xhigh (max)          ← :max accepted, depth unverified — shipped cap is xhigh
Grok 4.5 (xai)          low medium high                      ← :xhigh/:max silently clamps to high · minimal is not a native effort
grok-build/grok-4.3     ── bare selector only (effort suffixes don't resolve) ──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go others       ── omit the :effort suffix (default) ──
google-antigravity Gemini  gemini-3.1-pro-low:high (high reasoning) · gemini-3.1-pro-low (low effort)
```

### Five hard rules

1. Gemini Pro supports only `low`/`high`; high reasoning is the literal pin `gemini-3.1-pro-low:high` (since 0.9.6 the fuzzy space is fail-closed — bad ids return “not found”).
2. openai-codex ctx is **per-model** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K** · the three `gpt-5.6` models=**373K** (raised from 272K in 0.9.6; separate from the 1.05M API specification usable prompt budget).
3. Sonnet (4.6/5) cannot do `xhigh`/`max` in GJC; **Fable 5 cannot do `max`** (clamped to high / xhigh respectively).
4. opencode-go omits `:effort` (only the deepseek-v4 family supports it).
5. xai `grok-4.5` caps at `high` (`:xhigh` silently clamps; xhigh exists only on grok-build, where effort suffixes do not resolve). Out-of-range tiers clamp rather than error; the gpt-5.6 trio accepts `:max`, but its depth is unverified, so the shipped cap is `xhigh`.

> **Footnote (upstream gap):** Both Claude 5 models support up to `max` in the official API. The GJC parser (0.9.1–0.9.6) fable fallback and sonnet-5 inherited clamp are **engine-side gaps** reported upstream with reproductions.

### 3-3. Subscription → provider

| Subscription | provider-id | Notes |
|---|---|---|
| claude | `anthropic` | all efforts. Includes the Claude 5 family (Fable 5 · Sonnet 5) |
| gpt | `openai-codex` | **ChatGPT account → base GPT (gpt-5.6 sol/terra/luna · 5.5 · 5.4)**. ctx: gpt-5.4=1M · 5.5=272K · 5.6 trio=373K |
| grok | `xai` | full lineup + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra subscription token**. Gemini + bundled Claude (Opus 4.6 — as of 2026-07-02; bundle composition has not been re-checked afterward) |
| opencode go | `opencode-go` | API key (`OPENCODE_API_KEY`) |

> [!NOTE]
> ChatGPT (Codex) serves base GPT, not standalone `-codex` variants. `google-vertex` and DeepInfra are paid API-key alternatives.

### 3-4. Selector syntax

```text
<provider-id>/<model-id>:<effort>            e.g. anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   (Gemini high reasoning — the engine's canonical path)
opencode-go/<model>                           (omit effort = model default)
```

---

## 4. 📊 Benchmark basis

| Role (axis) | Leader | Figure |
|---|---|---|
| executor (SWE-bench Verified) | **Fable 5** | **95.0%** (Opus 4.8 88.6 = **strongest subscription-included** · GPT-5.5 82.6 · Gemini 3.1 Pro 80.6) |
| planner (long-horizon workflow · reasoning) | **GPT-5.6 Sol**† | Agents' Last Exam 52.7 (5.5: 46.9) · AA Intelligence 58.9 — standalone GPQA #1 is Sonnet 5 at 96.2 · Gemini 3.1 Pro is specialized for scientific knowledge at 94.3 ([deep dive](./docs/deep-dive-role-fit.md#6-2-역할-배치-최적성-검토-deep-research--실측)) |
| architect (ctx · multimodal) | **Gemini 3.1 Pro**† | 1M ctx · MMMU-Pro 81% |
| default (tool-calling · honesty) | **Opus 4.8 / Fable 5** | router quality = whole-system ceiling (Fable carries refusal/billing caveats — see §5) |
| critic (independence) | **cross-family** | meta-judge > debate aggregation |

**Consensus principles** — † The planner row reflects the 2026-07-10 Sol GA replacing the 2026-07-02 Gemini 3.1 Pro snapshot; re-verify the architect axis when Gemini 3.5 Pro ships.

1. **default = Anthropic flagship (Opus/Fable), fixed** — router quality is the whole-system ceiling. Exceptions: `ultimate-sol` (Sol router — validator-listed opt-in experiment) and `eco` (Anthropic-free bundle — Terra router).
2. **architect = Gemini 3.1 Pro (multimodal) / Opus (ultra-long-context)** — Gemini is best for vision and mid ctx; for 200k+ text retrieval use Opus (MRCR 76%@1M; Gemini 26%).
3. **critic = cross-family** — a different vendor than the main loop/planner mitigates self-preference bias.
4. **Structure = strong main loop + signal-driven delegation + failure-driven effort escalation.**
5. **No per-query profile swapping** — cache loss exceeds benefit. Swap only at mode boundaries.

---

## 5. 🗂️ Final catalog — 10 bundles · 4 tiers

<div align="center">

<img src="assets/profiles-matrix.svg" alt="profiles × roles matrix" width="100%">

</div>

> ★ = everyday recommendation. v2.0.0 is not a set of equal profiles but 10 bundles across 4 tiers. Every bundle has `required_providers ≥ 2`; `critic=cross-family` by default (exceptions are `SAME_FAMILY_OK` with WARN); it follows engine effort hard-rules and selector verification ([§6](#6--verification-matrix)). Every shipped seat was green in the 2026-07-10 gjc **0.9.6** battery.

<details>
<summary><b>📋 Expand the full YAML (identical to gjc-profiles.yml by model mapping — comments stripped; the annotated Korean canonical lives in <a href="./gjc-profiles.yml">gjc-profiles.yml</a>)</b></summary>

```yaml
profiles:

  daily:
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium
      executor:  openai-codex/gpt-5.6-terra:high
      planner:   openai-codex/gpt-5.6-sol:high
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    google-antigravity/gemini-3.1-pro-low:high

  coding-sprint:
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium
      executor:  anthropic/claude-opus-4-8:high
      planner:   openai-codex/gpt-5.6-sol:high
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    openai-codex/gpt-5.6-terra:high

  cyber-cop:
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  openai-codex/gpt-5.6-sol:high
      planner:   google-antigravity/gemini-3.1-pro-low:high
      architect: anthropic/claude-opus-4-8:high
      critic:    openai-codex/gpt-5.6-sol:high

  ultimate-opus:
    required_providers: [anthropic, openai-codex, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:high
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: anthropic/claude-opus-4-8:high
      critic:    xai/grok-4.5:high

  ultimate-sol:
    required_providers: [openai-codex, anthropic, xai]
    model_mapping:
      default:   openai-codex/gpt-5.6-sol:high
      executor:  openai-codex/gpt-5.6-sol:xhigh
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: anthropic/claude-opus-4-8:high
      critic:    xai/grok-4.5:high

  dream-team:
    required_providers: [anthropic, openai-codex, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high
      executor:  anthropic/claude-fable-5:xhigh
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: anthropic/claude-opus-4-8:high
      critic:    xai/grok-4.5:high

  llm-council:
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  openai-codex/gpt-5.6-terra:high
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.5:high

  escalation:
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-fable-5:xhigh
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.5:high

  eco:
    required_providers: [openai-codex, opencode-go, google-antigravity]
    model_mapping:
      default:   openai-codex/gpt-5.6-terra:medium
      executor:  opencode-go/deepseek-v4-flash
      planner:   openai-codex/gpt-5.6-luna:medium
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    google-antigravity/gemini-3-flash:low

  monorepo:
    required_providers: [anthropic, google-antigravity, opencode-go]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium
      executor:  anthropic/claude-opus-4-8:high
      planner:   google-antigravity/gemini-3.1-pro-low:high
      architect: anthropic/claude-opus-4-8:high
      critic:    opencode-go/glm-5.2
```

</details>

<details>
<summary><b>v1.11 → v2 migration</b></summary>

`ultimate`→`ultimate-opus`, `ultimate-f5`/`legend`→`dream-team`; `llm-council` and `ultimate-sol` are new. v2 removes `solo-anthropic`/`solo-openai`/`claude-codex`/`claude-codex-max` under its multi-vendor principle; built-in GJC 0.9.6 `claude-*`, `codex-*`, `opus-codex`, and `fable-opus-codex` absorb those use cases (not as mapping equivalents). See [CHANGELOG](./CHANGELOG.md) and [the v2 announcement](./docs/whats-new-v2.md) for the detailed diff.

</details>

**Bundle rationale:** Each bundle trades role fit, vendor independence, access, and cost differently. See the Korean canonical [§5 catalog](./README.md#5-️-최종-카탈로그--10-번들--4계층) and [per-bundle rationale](./README.md#프로필별-설계-근거).

---

## 6. ✅ Verification matrix

> Legend: ✅ live-call green (date in parentheses) · 🔴 failure · ⚠ caveat/clamp · †‡ footnotes · ●○ relative cost.
> On 2026-07-10, gjc **0.9.6** called every provider’s core selector with `gjc -p --no-session --no-tools --model <sel> "..."` ([rerun-3](./evidence/2026-07-10-selectors-rerun-3.md); rerun-2 is the 0.9.5 green record). Every v2 shipped selector was green; same-day antigravity drift replaced `eco.critic`.

| Provider | Verified selectors |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh` · `claude-sonnet-5:high` · `claude-opus-4-8:high` · `claude-sonnet-4-6:high` — sel ✅(07-10) |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh` · `gpt-5.6-terra:high`/`:xhigh` · `gpt-5.6-luna:high` · `gpt-5.5:high` · `gpt-5.4:high` — sel ✅(07-10; 5.5=07-02) |
| `xai` | `grok-4.5:medium`/`:high` · `grok-4-fast:high` · `grok-4-1-fast:high` · `grok-code-fast-1` · `xai/grok-composer-2.5-fast` — sel ✅(07-10; 4-1 retired) |
| `grok-build` | `grok-4.3` (bare) — sel ✅(07-02) |
| `google-antigravity` | `gemini-3.1-pro-low`/`:high` · `gemini-3-flash`/`:low` — sel ✅(07-10) |
| `opencode-go` | `deepseek-v4-flash` · `deepseek-v4-pro` · `glm-5.2` · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` — sel ✅(07-02) |

- `fable-5:max`→xhigh, `sonnet-5:xhigh/max`→high, and `grok-4.5:xhigh/max`→high are silent clamps, not failures.
- The gpt-5.6 trio accepts `:max`, but its depth is unverified and it is not shipped; `gpt-5.5:high` is a 07-02 green canary.
- `grok-4-1-fast` still calls but redirects to Grok 4.3 billing after its 2026-05-15 retirement, so v2 excludes it.
- Since 0.9.6 Gemini’s fuzzy space is fail-closed; the 0.9.5 silent `gemini-3.1-pro-high` → `-low` interpretation no longer reproduces.
- `glm-5.2` entered the bundled catalog in 0.7.10 and needs `OPENCODE_API_KEY`.

<details>
<summary><b>Failed selectors (avoid)</b></summary>

- `openai-codex/gpt-5.3-codex` · `gpt-5.2-codex` · `gpt-5.1-codex-max/mini` — unsupported on ChatGPT accounts.
- `google-antigravity/gemini-3.1-pro-high` — not found in 0.9.6; high reasoning is `gemini-3.1-pro-low:high`.
- `gemini-3.5-flash-low` · `gemini-3.5-flash` · `gemini-pro-agent` — not found on 2026-07-10 afternoon.
- `gemini-3-pro` — retired.
- `claude-sonnet-4-6-thinking` — 404.
- `gpt-oss-120b` — 500.
- `opencode-go/*` — fails when `OPENCODE_API_KEY` is unset.

</details>

> [!NOTE]
> The antigravity live surface can change within a day and `--list-models` can be cached. Live-call before adopting a seat; re-login/retry when discovery is stale, or use the bundle id (eco critic alternative: `opencode-go/deepseek-v4-pro`; add the `zai` provider for GLM).

<details>
<summary><b>Latency reference (micro-bench 2026-07-02; Grok 4.5 streaming on 2026-07-09)</b></summary>

| Selector | Coding | Reasoning | Notes |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **fastest overall** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | +3~4s vs sonnet-5 on coding |
| `grok-4.5:medium` / `:high` | ~14s / ~50s | TTFT ~13s / ~48s | high only for high-risk critic |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | coding-latency outlier |
| `glm-5.2` | **21.9s** | 4.0s | slowest at coding — fine for critic |

</details>

```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
```

### 6-2·6-3. Role-fit deep dive (moved)

Repeated deep research and measurement found the role-to-model placement near-optimal: the 07-10 Sol generation change updated planner, Gemini’s nominal 1M is not effective 1M (MRCR 26%@1M versus Opus 76%), and a ~400k single-message limit is not the context-window limit, so chunk accumulation is required. Full details: [docs/deep-dive-role-fit.md](./docs/deep-dive-role-fit.md) (Korean-only deep-dive).

---

## 7. 🛠️ Install / uninstall

Follow the 30-second install and provider login instructions above.

```bash
# options
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash  # pick default profile
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash           # skip default-setting
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash       # override agent directory
```

### Manual install / verify / uninstall

Paste the `profiles:` block from [`gjc-profiles.yml`](./gjc-profiles.yml) under `profiles:` in `~/.gjc/agent/models.yml`, then run `gjc --mpreset daily --default`.

```bash
gjc --list-models daily                       # confirm
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # revert (restore backup)
```

> [!WARNING]
> **GJC 0.7.10–0.9.1 preset rename/delete caveat:** custom-preset rename/delete strips all comments from `models.yml`, including the installer’s managed-block sentinels. Deleted profiles can therefore return on reinstall; check the result, and restore a backup (`cp … .bak-*`) for guaranteed removal. Unverified on 0.9.6.

---

## 8. 🔀 Dynamic routing

> Put [`routing-rules.md`](./routing-rules.md) (Korean-only; selectors are language-neutral) in the project `AGENTS.md`, or inject it with `gjc --append-system-prompt @routing-rules.md`.

<div align="center">

<img src="assets/routing-tree.svg" alt="work signal → delegation routing" width="100%">

</div>

**Work signal → delegation** — delegate only when the signal is clear; if the main loop can do it directly, it does.

<div align="center">

<img src="assets/effort-ladder.svg" alt="adaptive effort escalation" width="100%">

</div>

**Effort ladder** — escalation is justified only when it could not solve the work; the floor is low; Gemini makes one low↔high jump.

| Signal | Swap → |
|---|---|
| session start · general work | `daily` |
| pure implementation sprint | `coding-sprint` |
| pre-merge/release · security · billing | `escalation` (manual trigger — routing-rules Escalation contract) |
| PR review / security-audit session | `cyber-cop` |
| decision needing multi-family consensus | `llm-council` (+ routing-rules Council contract) |
| accuracy above all (opt-in premium) | `ultimate-opus` / `ultimate-sol` (Sol-axis experiment) / `dream-team` (Fable · credits accepted) |
| bulk refactor · migration | `eco` |
| entering a huge codebase | `monorepo` |
| single-vendor operation | built-in GJC profiles (`claude-opus` · `codex-*` etc. — outside this catalog) |

---

## 9. 🧪 Parallel agents + reliability

```text
serial chain, 5 steps (0.99 each):  0.99^5 ≈ 95.1%    /    parallel independent, 5 (OR-success): 1-(0.01)^5 ≈ 100%
```

- critic = **different vendor from the main loop, parallel independent vote, then the main loop tallies** (no debate — meta-judge wins).
- critic panel example: `{openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high, google-antigravity/gemini-3.1-pro-low:high}` in parallel → 2/3 dissent or any CRITICAL/BLOCK blocks. **CRITICAL/HIGH dissent cannot be majority-voted away** — resolve it or use a human gate.
- executor fan-out only when **the work is truly independent** (no shared state).
- keep chains short, with the main loop as the single source of truth (no direct sub-agent consensus).

---

## 10. 💰 Cost

Gemini uses [Google AI Pro/Ultra](https://antigravity.google/docs/plans) subscription tokens; the rest are per-token ($/1M, input/output). Follow §5 for Fable inclusion and credits caveats.

| Model | $/1M (in/out) | Role |
|---|---|---|
| Claude Fable 5 | 10 / 50 (batch 5/25 · cache hits 1)† | dream-team default·executor · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor backbone |
| Claude Sonnet 5 | 3 / 15 (intro 2/10 through 2026-08-31)‡ | eco executor alternative |
| GPT-5.6 Sol | 5 / 30 (Fast mode is 12.5/75) | planner (daily·sprint·ultimate-opus·dream-team·council·escalation) · ultimate-sol 3 seats · cyber-cop executor·critic |
| GPT-5.6 Terra | 2.5 / 15 | daily executor · coding-sprint critic · llm-council executor · eco default |
| GPT-5.6 Luna | 1 / 6 | eco planner (new in v2) |
| Grok 4.5 | 2 / 6 (effective input ~$0.84 @88% cache) | critic (premium 3 bundles · llm-council · escalation) — xai API key |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k single-paste fallback |
| Gemini 3.1 Pro / 3-flash | preview/subscription token | planner·architect·critic |

> † Fable 5 is exactly 2× Opus pricing. The subscription-included window (~7/12) still consumes weekly limits.
> ‡ Sonnet 5’s tokenizer change makes the same text ~30% more tokens — budget its effective cost above the sticker price.
> (Note: via the DeepInfra provider, DeepSeek V4 Pro is $1.30/$2.60 — see the provider section above.)

**Relative bundle cost**

| Bundle | Cost | Main driver |
|---|---|---|
| dream-team | ●●●●● | default·executor Fable 5 — ~7/12 subscription-included (50% weekly-limit cap), then credits $10/50 |
| escalation | ●●●●● | executor Fable `:xhigh` (rescue pitcher — intermittent use) + planner Sol `:xhigh` + 4-vendor auth |
| ultimate-opus / ultimate-sol | ●●●●○ | Opus or Sol 3 seats at `:high~xhigh` + Grok critic (xai API) |
| llm-council | ●●●●○ | 4-vendor auth + Sol `:xhigh` planner — council workflow bills by vote count when executed |
| coding-sprint | ●●●○○ | executor Opus `:high` (raise to max only on failure signals) |
| daily | ●●●○○ | main loop Opus `:medium`, delegation spread across mid/cheap models — subscription OAuth across 3 vendors |
| monorepo | ●●●○○ | executor/architect Opus + Gemini (preview/subscription) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash ($0.14) + Luna ($1) + Gemini preview — not absolute cheapest; built-in `codex-eco` is |

---

## 11. 📖 Sources

**Coding (executor)** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1)
**Claude 5 family** · [Fable 5 redeployment announcement](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com model docs](https://platform.claude.com/docs) — pricing, subscription inclusion (~7/12 extension, [Android Authority report](https://www.androidauthority.com/claude-fable-5-free-extension-3685103/)), and effort specs cross-checked 2026-07-02/07-10
**GPT-5.6 (2026-07-09 GA)** · [launch announcement](https://openai.com/index/gpt-5-6/) · [Sol preview (Cerebras 750TPS)](https://openai.com/index/previewing-gpt-5-6-sol/) · [AA: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) · [TechTimes (METR eval gaming)](https://www.techtimes.com/articles/319808/20260707/gpt-56-sol-review-faster-coding-half-fable-5-cost-benchmark-problem.htm) — pricing/evals cross-checked 2026-07-10
**Role and routing** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [self-preference bias](https://arxiv.org/abs/2410.21819) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)
**Official models/pricing** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

<div align="center">

**Install in one line, best model per role.**
**v2.0.1** · [CHANGELOG](./CHANGELOG.md) · [Maintenance playbook](./MAINTAINING.md) · License [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
