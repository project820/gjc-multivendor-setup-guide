<div align="center">

# 🧩 GJC Multi-Vendor Extreme Setup

### claude · gpt · grok · gemini · opencode go — a verified setup that splits 5 subscriptions *by role*

Stop agonizing over model choice. **Install in one line** and let each role get its best-fit model automatically.

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-2.0.0-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/bundles-10%20·%204%20tiers-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="dream-team setup — strongest hypothesis per role" width="100%">

</div>

**[한국어](./README.md) · English (this page) · [中文](./README.zh.md) · [日本語](./README.ja.md)**

> [!NOTE]
> **The core of this guide was adopted into the official GJC docs** — a condensed version was merged upstream as [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md) ([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev`). Treat the **official GJC docs as the canonical reference** for the role/selector concepts; this repo provides what those docs do not — the **one-line installer**, the **4-tier / 10-bundle catalog** (including the `cyber-cop` reviewer mode plus Council/Escalation workflow contracts), and [maintenance & validation tooling](./MAINTAINING.md) (static-check CI + live selector battery + catalog drift tracking).

## 🚨 `cyber-cop` — reviewer-mode profile

> Author-mode bundles are for sessions that **write** code. **`cyber-cop` is for sessions that stop code** — GJC's first **reviewer-mode** bundle: review someone else's PR, hunt for reasons to block, and adjudicate at the merge gate.

**What's different**
- In PR review / security audits the role weighting **inverts** → **architect (first-pass verdict: CLEAR/WATCH/BLOCK) and critic (merge gate) lead**; executor drops to a supporting repro-PoC / failing-test role.
- The critic runs **cross-family vs the code author (assumed Claude)** (GPT-5.6 Sol) → structurally counters self-preference bias ([arXiv 2410.21819](https://arxiv.org/abs/2410.21819)).
- High-risk / security PRs convene a **3-vote parallel panel** (`gpt-5.6-sol` · `grok-4.5` · `gemini-3.1-pro`), independent votes → 2/3 dissent or any CRITICAL/BLOCK blocks.

**Proof it works — this repo dogfooded it**
> Across PRs #4–#7 the review gate **blocked 10 defects before merge** (#4: 5 · #6: 5 · #7: passed on first vote). The review helper was BLOCKed by *its own* prompt-injection flaw (fixed, then passed), and two overclaims the Anthropic base model waved through (a relative-path injection surface and a permission overclaim) were **correctly BLOCKed by the cross-family critic (GPT-5.5)**. (One more was caught *after* #6 merged → fixed immediately in #7.) The self-preference-bias defense works in practice.

**Start clone-free in 2 commands (v1.6+)**
```bash
# prereqs: gh CLI installed & authed (gh auth login) + gjc provider /login done
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_COP=1 bash
export PATH="$HOME/.local/bin:$PATH"   # once, if the installer warned about PATH
cd <repo-under-review>
gjc-cop 123               # PR #123 → 4-section verdict (REPO auto-detected from cwd — never merges)
# gjc-cop --panel 123     # high-risk: 3-vote cross-family panel
# gjc-cop shell           # interactive reviewer session (trusted contract auto-injected)
# gjc-cop watch           # poll & review new PRs (humans decide merges)
```
The clone/manual path (same mechanics, no wrapper) is in the [announcement §3](./docs/whats-new-cyber-cop.md).

📖 Full gap argument, 3-step usage, automated review pipeline & security rules → **[cyber-cop announcement](./docs/whats-new-cyber-cop.md)** (Korean canonical)

---

## ⚡ 30-second install (one-line copy-paste)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

This single line **safely merges 10 bundles into `~/.gjc/agent/models.yml`** and sets `daily` as the default profile. Your existing config is backed up automatically, and re-running cleanly updates in place.

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
> Pick the default profile: `curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash` · skip default-setting: `GJC_SETUP_DEFAULT=none`.

---

## 📑 Table of contents

1. [Why multi-vendor](#1--why-multi-vendor)
2. [Core design](#2--core-design)
3. [GJC engine facts](#3--gjc-engine-facts)
4. [Benchmark basis](#4--benchmark-basis)
5. [Final catalog — 10 bundles · 4 tiers](#5-️-final-catalog--10-bundles--4-tiers)
6. [Verification matrix](#6--verification-matrix)
7. [Install / uninstall](#7-️-install--uninstall)
8. [Dynamic routing](#8--dynamic-routing)
9. [Parallel agents + reliability](#9--parallel-agents--reliability)
10. [Cost](#10--cost)
11. [Sources](#11--sources)

---

## 1. 🎯 Why multi-vendor

Subscribing to claude·gpt·grok·gemini·opencode go and then using only one model means running a *second-best* model in every role. Verified benchmarks show **the leading vendor differs per role**:

| Role | What it does | Best model |
|---|---|---|
| 🧠 **reasoning/planning** (planner) | sequencing, acceptance criteria | **Gemini 3.1 Pro** (GPQA 94.3 / ARC-AGI-2 77.1)† |
| 🔨 **implementation** (executor) | writing/editing real code | **Claude Fable 5** (SWE-bench Verified **95.0**) — strongest *subscription-included* is **Opus 4.8** (88.6) |
| 🔭 **code review** (architect) | large-repo navigation, architecture | **Gemini 3.1 Pro** (multimodal MMMU-Pro 81%)† · ultra-long-context (>200k) → **Opus** |
| ⚖️ **independent critique** (critic) | adversarial verification | **cross-family** (different vendor than the main loop) |
| 🎛️ **orchestration** (default) | tool-calling, routing, honesty | **Anthropic flagship** — Opus 4.8 (router quality caps the whole system; `dream-team` uses Fable 5, and `ultimate-sol` is the only Sol opt-in exception) |

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

- **The main loop is non-negotiable.** Most median tasks are handled by the main loop alone, so dropping `default` to a weak model collapses perceived quality across the board. Default to the Anthropic flagship (Opus 4.8 — Fable 5 in `dream-team`). The only exception is `ultimate-sol` (Sol router), an opt-in experiment listed in the validator with WARN surfaced.
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

These are the **GJC 0.9.6 effective** tiers (2026-07-10 live-call battery) — some differ from the official API spec (footnote below):

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

> [!IMPORTANT]
> **Five hard rules**: ① Gemini Pro supports only `low`/`high`; high reasoning is the literal pin `gemini-3.1-pro-low:high` (since 0.9.6 the fuzzy space is fail-closed — bad ids return "not found") ② openai-codex ctx is **per-model** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K** · the three `gpt-5.6` models=**373K** (raised in 0.9.6; separate from the 1.05M API spec usable prompt budget) ③ Sonnet (4.6/5) cannot do `xhigh`/`max` in GJC · **Fable 5 cannot do `max`** (clamped to high / xhigh respectively) ④ opencode-go: omit `:effort` (only the deepseek-v4 family supports it) ⑤ xai `grok-4.5` caps at `high` (`:xhigh` silently clamps — xhigh exists only on the grok-build provider, where effort suffixes don't resolve at all). Out-of-range tiers are **clamped**, not errored. The three gpt-5.6 models appear in the catalog up to `max` and live calls accept it (verified 07-10), but depth is unverified — this guide ships no higher than `xhigh`.
>
> **Footnote (upstream gap)**: per the official API, both Claude 5 models support up to `max`. The GJC parser (0.9.1~0.9.6) doesn't know the fable family (falls back to inferred rules) and sonnet-5 inherits the 4.6 clamp — an **engine-side gap, reported upstream** with a repro. This guide records the GJC-effective tiers.

### 3-3. Subscription → provider

| Subscription | provider-id | Notes |
|---|---|---|
| claude | `anthropic` | all efforts. Includes the Claude 5 family (Fable 5 · Sonnet 5) |
| gpt | `openai-codex` | **ChatGPT account → serves base GPT (gpt-5.6 sol/terra/luna · 5.5 · 5.4)**. ctx: gpt-5.4=1M · 5.5=272K · the three 5.6 models=373K |
| grok | `xai` | full lineup + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra subscription token**. Gemini + bundled Claude (Opus 4.6 — bundle composition not re-checked since the Claude 5 launch) |
| opencode go | `opencode-go` | API key (`OPENCODE_API_KEY`) |

> [!NOTE]
> **openai-codex path caveat**: logging in with a ChatGPT (Codex) account serves the **base GPT models (`gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5`, `gpt-5.4`)**. Standalone `-codex` variants (`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex-max/mini`) are **not supported** on this path (`not supported when using Codex with a ChatGPT account`), so this guide uses verified **base GPT** for coding roles too.
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
| default (tool-calling · honesty) | **Opus 4.8 / Fable 5** | router quality = whole-system ceiling (Fable carries refusal/billing caveats — [§5](#5-️-final-catalog--10-bundles--4-tiers)) |
| critic (independence) | **cross-family** | meta-judge > debate aggregation |

> † **Successors imminent**: on the planner axis, GPT-5.6 Sol is in partner preview (2026-06-26, `max` effort + `ultra` sub-agent mode — GA weeks away); on the architect axis, Gemini 3.5 Pro (2M ctx, Deep Think) slipped to July GA. Either release puts this table up for re-verification.

**Consensus principles**

1. **default = Anthropic flagship (Opus/Fable), fixed** — router quality is the whole-system ceiling. The only exception is `ultimate-sol`, an opt-in Sol-router experiment listed in the validator with WARN surfaced.
2. **architect = Gemini 3.1 Pro (multimodal) / Opus (ultra-long-context)** — Gemini is best for vision and mid ctx; for 200k+ text retrieval use Opus (MRCR 76%@1M, where Gemini collapses to 26%).
3. **critic = cross-family** — a different vendor than the main loop/planner mitigates self-preference bias.
4. **Structure = strong main loop + signal-driven delegation + failure-driven effort escalation.**
5. **No per-query profile swapping** — cache loss > benefit. Swap only at mode boundaries.

> Benchmarks are time-sensitive → re-verify quarterly. Absolute rankings limited to vals.ai independent boards.

---

## 5. 🗂️ Final catalog — 10 bundles · 4 tiers

<div align="center">
<img src="assets/profiles-matrix.svg" alt="profiles × roles matrix" width="100%">
</div>

> ★ = everyday recommendation. **v2.0.0 structure shift**: this is no longer "N equal profiles"; it is **10 user-facing bundles split across 4 trust tiers**. Multi-vendor invariants: every bundle has `required_providers ≥ 2` (single-vendor needs belong to built-in GJC 0.9.6 profiles) · `critic=cross-family` by default (exceptions are listed in the validator as `SAME_FAMILY_OK` with WARN permanently surfaced) · every bundle passes the engine effort hard-rules and **tracks selector verification status** ([§6](#6--verification-matrix); first 2026-07-10 gjc **0.9.6** battery — every shipped selector green).

| Tier | Bundle | One-liner | Use when |
|---|---|---|---|
| Core | ⭐ **daily** | Opus main loop + role-split delegation — **activates with subscription OAuth across 3 vendors only** | **everyday default** |
| Core | 🏎️ **coding-sprint** | implementation-throughput bundle with executor promoted to Opus | pure implementation sprint |
| Core | 🚨 **cyber-cop** | reviewer mode — architect & critic lead, dedicated to PR review and security audits | reviewing others' PRs · merge gates · security audits |
| Premium (exp) | 🏆 **ultimate-opus** | Anthropic-quality premium baseline (successor to the old cost-no-object profile) | accuracy matters more than cost |
| Premium (exp) | 🧪 **ultimate-sol** | Sol-baseline premium — agentic/terminal/browser axis. **Only non-Anthropic default** | long autonomous workflow experiments |
| Premium (exp) | 🔥 **dream-team** | strongest-per-role hypothesis — Fable default+executor | highest quality, credits accepted |
| Workflow | 🏛️ **llm-council** | 4-family council seating chart — **routing-rules executes the Council vote/quorum contract** | decisions needing multi-family consensus |
| Workflow | 🛡️ **escalation** | manual escalation — Fable rescue pitcher + 3-vote critic panel | merges · security · billing · irreversible changes |
| Specialized (exp) | 💸 **eco** | low-cost multi-vendor experiment — *not absolute cheapest* (built-in `codex-eco` is the minimal-dependency cheap path) | cost pressure · bulk work |
| Specialized (exp) | 🗺️ **monorepo** | ≥1M ctx everywhere (excludes gpt-5.5 272K / gpt-5.6 373K) | huge codebases |

**v1.11.0 → v2.0.0 migration**: `ultimate`→`ultimate-opus` · `ultimate-f5`/`legend`→`dream-team` · `solo-anthropic`/`solo-openai`/`claude-codex`/`claude-codex-max` → **removed** — single-/two-vendor needs are absorbed by built-in GJC 0.9.6 profiles (`claude-opus`/`claude-fable`/`codex-*`/`opus-codex`/`fable-opus-codex`), as use-case absorption rather than mapping equivalence. `llm-council` and `ultimate-sol` are new.

<details>
<summary><b>📋 Expand the full YAML (identical to gjc-profiles.yml — by model mapping; only §refs in comments adapted for the README)</b></summary>

```yaml
profiles:

  # ───────────────────────── Core tier ─────────────────────────

  daily:                               # ★ 평소 기본 (--default daily) — 구독 OAuth 3벤더만으로 activation
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 본체 효율 knee · 1M ctx
      executor:  openai-codex/gpt-5.6-terra:high                # 코딩특화 $2.5/15에 ≈GPT-5.5급(공식 5.6 평가표)·벤더분산
      planner:   openai-codex/gpt-5.6-sol:high                  # 장기 워크플로 완주 1위(Agents' Last Exam 52.7)·tool-heavy 분해
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx·멀티모달(MMMU-Pro)·GPQA 94.3 — Gemini 전문좌석
      critic:    google-antigravity/gemini-3.1-pro-low:high     # v2: grok→Gemini — xai 키 장벽 제거(구독-only daily) + 본체(Opus)와 cross-family 유지. PR #21 패널 지적 반영(본체=critic 동일벤더 금지). Grok critic 은 defect-recall 직접근거 0건(2축 리서치 합의)

  coding-sprint:                       # 🏎 순수 구현 처리량 — daily 대비 executor 를 Opus 로 승격
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 본체 오케스트레이션
      executor:  anthropic/claude-opus-4-8:high                 # 구독 포함 코딩 최강 계열(v2: max→high — 실패신호 시에만 max 격상, routing-rules 사다리)
      planner:   openai-codex/gpt-5.6-sol:high                  # v2: gemini→Sol — 스프린트 분해는 Sol 축(Terminal-Bench 88.8·DeepSWE 72.7)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx 리뷰
      critic:    openai-codex/gpt-5.6-terra:high                # 코딩인지 critic. ⚠planner 와 같은 gpt 계열 — 인간 판정(2026-07-10)으로 SAME_FAMILY_OK 등재(번들 전체는 3벤더 유지)

  cyber-cop:                           # 🚨 reviewer 모드 — PR 리뷰·보안 감사 (author 모드의 역상). v1.11.0 매핑 그대로(KEEP)
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high                 # 집계자 제한 — critic raw verdict 보존·노출(routing-rules 계약)
      executor:  openai-codex/gpt-5.6-sol:high                  # 조연 — 재현 PoC·failing test·harness (Terminal-Bench 2.1 88.8 SOTA)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 리뷰 체크리스트·감사 범위 (critic 과 cross-family)
      architect: anthropic/claude-opus-4-8:high                 # 주연1 — 1차 코드리뷰 판정자(CLEAR/WATCH/BLOCK)
      critic:    openai-codex/gpt-5.6-sol:high                  # 주연2 — 머지 게이트, Claude-작성 코드와 cross-family
      # 고위험 PR·보안 감사: critic 3표 병렬 패널 {openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high,
      # google-antigravity/gemini-3.1-pro-low:high} — 독립 투표 후 본체 집계(토론 금지), 2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단
      # (3표째 grok 은 xai 로그인 시 — 미보유면 2표 {gpt-5.6-sol, gemini}로도 provenance 최소치(non-default family ≥2) 충족)

  # ─────────────── Premium tier (experimental — role-fit L3 전) ───────────────

  ultimate-opus:                       # 🏆 Anthropic 품질 기저 프리미엄 (구 ultimate 후계)
    required_providers: [anthropic, openai-codex, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:high                 # ⚠architect 와 같은 claude 계열 — 인간 판정(2026-07-10) SAME_FAMILY_OK. Sol planner+Grok critic 이 교차검증 담당
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 최상위 추론 + OpenAI 다양성
      architect: anthropic/claude-opus-4-8:high                 # 1M 실효검색(MRCR 76% vs Gemini 26%) — v2: gemini→Opus
      critic:    xai/grok-4.5:high                              # 제3계열 독립 dissent seat(결함회수 최강 근거는 없음 — 명칭 주의)

  ultimate-sol:                        # 🧪 OpenAI(Sol) 기저 프리미엄 — agentic/terminal/브라우징 축. non-Anthropic default 유일 예외
    required_providers: [openai-codex, anthropic, xai]
    model_mapping:
      default:   openai-codex/gpt-5.6-sol:high                  # 라우터(장기 워크플로 완주 1위). ctx 373K(0.9.6) — 1M 아님 주의
      executor:  openai-codex/gpt-5.6-sol:xhigh                 # Terminal-Bench 88.8·DeepSWE 72.7. ⚠METR 게이밍 캐비앗 — SWE류 단독근거 금지
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # Sol 3좌석 = 의도된 정체성(자기강화 리스크는 아래 2좌석이 완충)
      architect: anthropic/claude-opus-4-8:high                 # cross-family 검증축 1 — 1M 장문
      critic:    xai/grok-4.5:high                              # cross-family 검증축 2

  dream-team:                          # 🔥 역할별 최강 가설 (구 ultimate-f5/legend 후계) — Fable 중심
    required_providers: [anthropic, openai-codex, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # 라우터=품질 상한. refusal(HTTP 200+stop_reason) 유의 · 7/12 이후 credits $10/$50 노출
      executor:  anthropic/claude-fable-5:xhigh                 # SWE-Bench Pro 80.0(공식표 자기불리)·FrontierMath T4. ⚠:max 금지(xhigh 침묵 클램프)
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 분해·tool-heavy 는 Sol 축
      architect: anthropic/claude-opus-4-8:high                 # ⚠executor 와 같은 claude 계열 — 인간 판정 SAME_FAMILY_OK(Fable≠Opus 모델 분리·1M 장문)
      critic:    xai/grok-4.5:high                              # 제3계열 dissent

  # ─────────────── Workflow bundle tier (좌석표 + 동반 워크플로) ───────────────

  llm-council:                         # 🏛 다계열 합의 리뷰 — ★프로필은 좌석표일 뿐이다. 병렬 독립호출·quorum·raw verdict 보존은
    required_providers: [anthropic, openai-codex, google-antigravity, xai]   #   routing-rules.md "Council 계약"이 실행한다(YAML 이 자동 실행하지 않음)
    model_mapping:
      default:   anthropic/claude-opus-4-8:high                 # 집계자 제한 — 요약·은폐 없이 raw verdict 보존
      executor:  openai-codex/gpt-5.6-terra:high                # 재현·검증 잡무
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 의제 분해
      architect: google-antigravity/gemini-3.1-pro-low:high     # 4계열 council 좌석 1 (Google)
      critic:    xai/grok-4.5:high                              # 4계열 council 좌석 2 (xAI)

  escalation:                          # 🚑 고실패비용 구원투수 — ★수동 에스컬레이션 번들. 실패신호 트리거·재시도 상한·human gate 는
    required_providers: [anthropic, openai-codex, google-antigravity, xai]   #   routing-rules.md 가 정의한다(프로필이 자동 감지하지 않음). v1.11.0 매핑 그대로(KEEP)
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-fable-5:xhigh                 # 실패한 작업의 구원투수. 간헐 사용 = credits 과금과도 궁합
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.5:high                              # + 3표 교차벤더 critic 패널(독립투표→본체집계)

  # ─────────────── Specialized tier (experimental) ───────────────

  eco:                                 # 💸 멀티벤더 저단가 실험 — "절대 최저비용" 아님(최소 의존 저가 경로는 GJC 내장 codex-eco).
    required_providers: [openai-codex, opencode-go, google-antigravity]      #   v2: anthropic·xai 제거 — 3벤더
    model_mapping:
      default:   openai-codex/gpt-5.6-terra:medium              # v2: opus:low→terra — 비-Anthropic default 는 anthropic 미포함 번들이라 router 불변식 비적용
      executor:  opencode-go/deepseek-v4-flash                  # $0.14/0.28, 최저가 코더(5번째 벤더)
      planner:   openai-codex/gpt-5.6-luna:medium               # v2: grok-4-1-fast(2026-05-15 retire→4.3 redirect 과금)→Luna $1/$6
      architect: google-antigravity/gemini-3.1-pro-low:high     # v2: 무핀→리터럴 -low:high 핀
      critic:    google-antigravity/gemini-3-flash:low          # v2: gemini-3.5-flash-low 07-10 오후 라이브 소멸 → gemini-3-flash:low(검증✅)·cross-family vs executor

  monorepo:                            # 🗄 거대 코드베이스 — 전역 1M ctx (★gpt-5.5(272K)/5.6(373K) 배제 — 1M 미달). v1.11.0 매핑 그대로(KEEP)
    required_providers: [anthropic, google-antigravity, opencode-go]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 1M
      executor:  anthropic/claude-opus-4-8:high                 # 1M
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 추론(스코프 입력). 1M window ≠ 완전 recall — 청크 누적 워크플로 전제
      architect: anthropic/claude-opus-4-8:high                 # 1M 멀티턴 누적·검색 최상. 단일 메시지 paste ~400k 한도(실측 350k ✅/476k 🔴) — 한 방 >400k 는 opencode-go/deepseek-v4-pro
      critic:    opencode-go/glm-5.2                            # 오픈웨이트 1위(AA 51), cross-family vs anthropic. effort 무핀(opencode-go 규칙)

# ─────────────────────────────────────────────────────────────────────────────
# v1.11.0 → v2.0.0 마이그레이션:
#   ultimate → ultimate-opus (executor max→high, architect gemini→opus) · ultimate-f5/legend → dream-team ·
#   solo-anthropic/solo-openai/claude-codex/claude-codex-max → 삭제(단일·2벤더 수요는 GJC 0.9.6 내장 claude-opus/claude-fable/codex-*/opus-codex/fable-opus-codex 프로필이 흡수 — 매핑 등가는 아니고 use-case 흡수) ·
#   daily.planner gemini→sol · daily.critic grok→gemini(구독-only 3벤더화 + 본체와 cross-family 유지) · eco 전면 재편(위 주석) · llm-council/ultimate-sol 신설.
# Claude 5 패밀리: Fable 5 = $10/$50(Opus 2배), 구독 포함 이벤트 ~7/12 23:59 PT(2차 출처 — 공식 1차 연장 페이지 미확보), 이후 usage credits.
#   Fable refusal 은 HTTP 200 + stop_reason=refusal — "빈 응답" 오인 금지. 30-day retention·ZDR 불가(민감 코드베이스 주의).
#   GJC 실효 effort: fable-5 ≤xhigh · sonnet-5 ≤high (API 는 둘 다 max — 파서 갭, 상류 제보됨).
# GPT-5.6(2026-07-09 GA): Sol $5/$30 · Terra $2.5/$15 · Luna $1/$6 — API 1.05M/128K, GJC 0.9.6 usable prompt budget 373K.
#   :max 는 수용되나 심도 미검증 — 미출하(상한 xhigh). ⚠ METR: Sol 의 SWE 평가 게이밍 적발 — SWE류 벤치 단독근거 승격 금지.
#   v2: Luna 를 eco.planner 로 채용($1/$6 — retire 된 grok-4-1-fast 대체).
# opencode-go: OPENCODE_API_KEY 필요(eco.executor·monorepo.critic). 검증✅: deepseek-v4-flash/pro · glm-5.2.
# xai: XAI_API_KEY 필요(premium 3종 + llm-council/escalation 의 critic). grok-4.5 는 grok-build/OAuth 변종 없음(07-10 재조회) —
#   grok-build 에 4.5 등장 시 xai 좌석 인증·비용 논증 전면 재계산(재평가 트리거).
# Grok 4.5 critic 좌석의 의미: "검증된 결함회수 최강"이 아니라 "제3계열 독립 dissent" — 2축 리서치 합의(critic-specific 근거 0건).
# 재평가 트리거: GJC 릴리스 diff · catalog drift(catalog-snapshot.sh --diff) · Fable 프로모션 종료/재연장 · 신모델 입점 ·
#   validator 검사범위 변경 · 가격 개정 · 독립 leaderboard 등재 — 하나라도 발화하면 profile matrix 재계산.
```

</details>

> [!TIP]
> **opencode-go** activates in `eco` (executor) and `monorepo` (critic) when `OPENCODE_API_KEY` is set (verified✅). SuperGrok's `xai/grok-composer-2.5-fast` (200k) is also verified as a throughput alternative. Other opencode-go models (qwen3.7-max · kimi-k2.6 · glm-5.1 · minimax-m2.7 · mimo-v2.5) were also confirmed working. Newly listed, still unverified candidates: **kimi-k2.7-code** (likely budget executor) · **minimax-m3** (1M multimodal).

#### Per-bundle design rationale

- **daily** — Opus `:medium` main loop (efficiency knee), implementation on coding-specialized `gpt-5.6-terra` (≈GPT-5.5 class at $2.5/15), decomposition on workflow-leading `gpt-5.6-sol:high`, design/review **and critique** on Gemini `-low:high` (v2: critic grok→gemini — drops the xai key barrier so daily activates with subscription OAuth across 3 vendors only, while keeping the critic cross-family vs the Anthropic main loop; the Grok diversity seat moved to premium bundles because there is no direct defect-recall evidence for Grok critic superiority). This is the everyday quality/cost balance point.
- **coding-sprint** — executor leads (Opus `:high`; escalate to max only on failure signals, [§8-2](#8-2-adaptive-effort-escalation)), planner is `gpt-5.6-sol:high` for sprint decomposition, and critic is coding-aware `gpt-5.6-terra` for real bug finding. ⚠ planner/critic are both GPT-family — listed as `SAME_FAMILY_OK` by human judgment (2026-07-10): Sol≠Terra and the whole bundle still uses 3 vendors.
- **cyber-cop** — 🚨 **reviewer mode**: the inverse of author mode. In review sessions role weight flips: executor drops to supporting repro PoC / failing-test work, while **architect (first-pass code-review verdict) and critic (merge gate) lead**. architect=Opus `:high` (1M effective retrieval, 76% vs Gemini collapsing to 26% for 200k+ diff reading), critic=`gpt-5.6-sol:high` (cross-family vs Claude-authored code — self-preference mitigation, arXiv [2410.21819](https://arxiv.org/abs/2410.21819)). High-risk PRs/security audits use the §9 critic panel: independent votes, no debate, 2/3 dissent or any CRITICAL/BLOCK blocks. The third Grok vote is optional when xai is logged in; without it, a 2-vote {gpt-5.6-sol, gemini} panel still preserves the minimum provenance rule (non-default family ≥2). Operational rules live in [`routing-rules.md`](./routing-rules.md). Difference from `escalation`: escalation is an author-side gate (fix until pass); cyber-cop is reviewer-side (hunt for blocking evidence).
- **ultimate-opus** — 🏆 Anthropic-quality premium baseline. default·executor·architect are Opus `:high` for stability, 1M context, and subscription marginal cost; cross-checking is handled by **Sol planner `:xhigh` + Grok critic `:high`**. ⚠ executor/architect are same Claude-family — human-judged `SAME_FAMILY_OK` with WARN surfaced. Three Opus seats are not "three independent opinions"; do not imply council quality.
- **ultimate-sol** — 🧪 Sol-baseline premium (experimental). Sol owns the axes where it is verified strong — long workflow completion (Agents' Last Exam 52.7), terminal (T-B 2.1 88.8 SOTA), browsing (BrowseComp 90.4), computer use (OSWorld 62.6) — so default/executor/planner all sit on Sol. **Only non-Anthropic default** (validator `NON_ANTHROPIC_DEFAULT_OK`; WARN surfaced). Tradeoffs are explicit: router ctx **373K** vs Opus 1M, weaker tool-use axis (Toolathlon 58 vs Fable 61.7), and ⚠METR's SWE-gaming finding, so SWE-style scores cannot be the sole promotion basis. Opus architect + Grok critic buffer the OpenAI self-reinforcement risk. Experimental until role-fit L3 is measured.
- **dream-team** — 🔥 strongest-per-role *hypothesis*. **Fable 5 = default+executor** (SWE-Bench Pro 80.0 on OpenAI's own self-disadvantaging table · FrontierMath T4 87.8), decomposition on Sol `:xhigh`, design review on Opus `:high` (1M), critique on third-family Grok. Fable caveats: ① subscription-included event through ~7/12 23:59 PT, then **usage credits $10/$50** (default+executor exposes the maximum) ② refusal returns HTTP 200 + `stop_reason:refusal` ③ 30-day retention and no ZDR. ⚠ executor(Fable)/architect(Opus) are same Claude-family — human-judged `SAME_FAMILY_OK` because models are separated and Sol/Grok cross-check.
- **llm-council** — 🏛 4-family (Anthropic·OpenAI·Google·xAI) council seating chart. **Activating the profile does not start a council** — parallel independent calls, mutual non-disclosure, raw verdict preservation, and quorum (CRITICAL/HIGH dissent is not majority-voted away) happen only when the main loop executes the **Council contract** in [`routing-rules.md`](./routing-rules.md). Seats: Opus main loop (aggregator limits), Terra (repro/verification chores), Sol `:xhigh` (agenda decomposition), Gemini (Google seat), Grok (xAI seat). Vendor count is not independent vote count; do not inflate confidence by arithmetic.
- **escalation** — 🛡 **manual** escalation (not automatic failure detection — triggers, retry budget, and human gate are the routing-rules Escalation contract). On failure signals, bring in **Fable 5 `:xhigh` as the rescue executor**; intermittent use also fits credits billing. critic uses the multi-vendor 3-vote panel ([§9](#9--parallel-agents--reliability)). On Fable refusal, fall back executor to Opus `:max` and report to the human. Reserve for irreversible/high-cost changes.
- **eco** — 💸 low-cost multi-vendor *experiment* — **not absolute cheapest** (built-in GJC 0.9.6 `codex-eco` is the minimal-dependency cheap path). v2 redesign: default `gpt-5.6-terra:medium` (non-Anthropic default invariant does not apply because no Anthropic is in the bundle), executor `deepseek-v4-flash` ($0.14/0.28), planner `gpt-5.6-luna:medium` (replaces the retired Grok fast slug: 2026-05-15 retire → legacy slug redirects to Grok 4.3 billing per xAI migration docs), architect literal Gemini `-low:high`, critic `gemini-3-flash:low` (the prior 3.5 flash live id disappeared on 07-10 afternoon — [§6](#6--verification-matrix)) and cross-family vs executor. No xai or anthropic key required.
- **monorepo** — 🗺 every role has 1M ctx. `gpt-5.5` (272K) and the three `gpt-5.6` models (373K) are excluded; gpt-5.4 has 1M, but Opus is at least as strong here. architect=**Opus** (best 1M effective retrieval, **76%@1M**; Gemini collapses to 26%), critic=**`glm-5.2`** (cross-family, alternative `deepseek-v4-pro`). **1M nominal window ≠ perfect recall** — split huge inputs into chunks and accumulate across turns ([§6-3](#6-3-remaining-gaps-gap-13--gjc-effective-context-measurement)); only use `opencode-go/deepseek-v4-pro` for rare single-message >~400k paste.

**Deleted profile destinations** — `solo-anthropic`/`solo-openai` (single vendor) and `claude-codex`/`claude-codex-max` (fixed two-vendor mixes) were removed under the v2 multi-vendor catalog principle (mixed-subscription collaboration, human judgment 2026-07-10). Built-in GJC 0.9.6 profiles absorb those use-cases: single Anthropic → built-in `claude-opus`/`claude-fable`; single Codex → built-in `codex-eco`/`codex-medium`/`codex-pro`; Claude+Codex two-vendor → built-in `opus-codex`/`fable-opus-codex` (updated to GPT-5.6 family in 0.9.6). Built-in mappings are not byte-identical to this guide's old YAML; if exact seats matter, keep the old YAML locally as a custom preset.

---

## 6. ✅ Verification matrix

> On 2026-07-10 (gjc **0.9.6** — rerun after the same-day 0.9.5→0.9.6 upgrade), the core selectors of every provider were **actually called** via `gjc -p --no-session --no-tools --model <sel> "..."` and re-verified (`evidence/2026-07-10-selectors-rerun-3.md`; rerun-2 is the 0.9.5 green record) — **every v2 shipped selector is green**. This battery caught same-day drift on the antigravity live surface (WARNING below) and replaced `eco.critic`. "Works" means a real call, not a guess.

| Provider | Verified selectors (✅ working) |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh` (**07-10 rerun✅** — `:max` silently clamps to xhigh) · `claude-sonnet-5:high` (07-10✅ — `:max` silently clamps to high) · `claude-opus-4-8:high` (07-10✅; low·medium·max 07-02✅) · `claude-sonnet-4-6:high` (07-10✅) — the 07-09 rate-limit lifted; every seat re-verified |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh` (**07-10✅**) · `gpt-5.6-terra:high`/`:xhigh` (07-10✅) · `gpt-5.6-luna:high` (07-10✅) · all 3 accept `:max` but depth is unverified (not shipped) · `gpt-5.5:high` (07-02✅, retired from v2 bundles — kept as canary) · `gpt-5.4:high` (1M ctx lane) |
| `xai` | `grok-4.5:medium`/`:high` (07-10✅ — `:xhigh`/`:max` clamp to high; xai-only, provider 500K / GJC 222K floor, $2/$6) · `grok-4-fast:high` (07-10✅) · ⚠`grok-4-1-fast:high` calls succeed but **xAI retired it on 2026-05-15 — legacy slug redirects to Grok 4.3 billing** (removed from v2) · `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3` (**bare selector only** — effort suffixes don't resolve, 07-02✅. SuperGrok OAuth) |
| `google-antigravity` | `gemini-3.1-pro-low` (±`:high`, 07-10✅) · `gemini-3-flash` (±`:low`, **07-10✅ — v2 eco.critic**) · ⚠ since 0.9.6 the fuzzy space is **fail-closed**: `gemini-3.1-pro-high`/`-bogus` return "not found" (the 0.9.5 silent `-low` interpretation trap did not reproduce — keep the pin) · ⚠ **same-day live-surface drift**: `gemini-3.5-flash-low`/`-extra-low`/`gemini-pro-agent` disappeared on 07-10 afternoon ("not found" despite `--list-models`; live calls are truth) |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro` (re-verified 07-02✅) · `glm-5.2` (**in the 0.7.10 bundled catalog**, 07-02✅) · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` (needs `OPENCODE_API_KEY`) |

> [!WARNING]
> **Selectors that did NOT work here** (avoid): `openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini` (unsupported on ChatGPT accounts) · `google-antigravity/gemini-3.1-pro-high`·`gemini-3.5-flash-low`·`gemini-3.5-flash`·`gemini-pro-agent` (**0.9.6 / 07-10 afternoon: "not found"** — high reasoning is `gemini-3.1-pro-low:high`; lightweight Gemini is `gemini-3-flash:low`) · `gemini-3-pro` (retired) · `claude-sonnet-4-6-thinking` (404) · `gpt-oss-120b` (500). `opencode-go/*` fails **only when `OPENCODE_API_KEY` is unset** (works per the table once set). Note: `fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.5:xhigh/max` are not failures — they **silently clamp** ([§3-2](#3-2-effort-cheatsheet)) — and the gpt-5.6 trio accepts `:max` but its depth is unverified (not shipped).

> [!NOTE]
> `opencode-go/glm-5.2` joined the **bundled catalog in 0.7.10** (the old "live-catalog only" caveat is retired). The antigravity live surface can drift even within a day (measured 07-10 afternoon disappearance of `gemini-3.5-flash*`) — `--list-models` can show cached listings, so **verify with a live call before adopting a seat**. With a stale discovery cache, activation can fail with `selector did not resolve`; re-login/retry to refresh the catalog, or substitute a bundled id (eco critic alternatives: `opencode-go/deepseek-v4-pro`, GLM as `zai/glm-5.2` — add `zai` to `required_providers`).

**Latency reference** (micro-bench 2026-07-02; Grok 4.5 row uses the 2026-07-09 streaming bench):

| Selector | Coding | Reasoning | Notes |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **fastest overall** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | +3~4s vs sonnet-5 on coding |
| `grok-4.5:medium` / `:high` | ~14s / ~50s | TTFT ~13s / ~48s | 2026-07-09 streaming bench; high only for high-risk critic |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | coding-latency outlier |
| `glm-5.2` | **21.9s** | 4.0s | slowest at coding — fine for critic |

Reproduce:
```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
```

---

### 6-2. Role-placement optimality review (deep research + measurements)

The early 8-profile (v1.0) role→model placement was re-reviewed through repeated deep research (independent benchmark validation) and live reasoning probes; the skeleton was confirmed near-optimal. **v2.0.0 adds a two-axis blind independent deep-research pass (Claude Fable 5 Ultracode + Parallel.ai Ultra 2x, 2026-07-10)** and restructures the result into the 10-bundle / 4-tier catalog — both axes agreed: release state and role placement are supported (SUPPORT), while profile/workflow boundaries, tier labels, and strict-provider friction needed revision (REVISE). Role-fit L3 measurements for the 3 premium bundles remain open, hence the experimental labels.

- **`gemini-3.1-pro-low:high` is not a degraded mode.** `thinkingLevel` is a per-request parameter on the same Gemini 3.1 Pro, not a separate model variant, and the model default is **HIGH**. The official model-card headline reasoning scores (GPQA 94.3 · ARC-AGI-2 77.1) were all measured under *Thinking (High)* — this selector calls the **native high-reasoning default mode**. Measurement probe: latency increased from `low` (18s) to `low:high` (22s), confirming thinking activation; standard reasoning answers matched GPT-5.5/Opus. *(Remaining: the primary-source mapping of GJC `:high` override to native HIGH is not fully confirmed → monitor reasoning quality in operation.)*
- **The planner reasoning axis splits.** GPQA Diamond (science knowledge) is saturated at the top (93–96%); standalone #1 is now **Sonnet 5 (96.2)**, with Gemini 3.1 Pro at 94.3. ARC-AGI-2 (abstract/fluid reasoning) clearly favored **GPT-5.5** in the dated analysis (0.850 vs 0.771; Fable 5 unpublished — reasoning lead unproven). For the fluid-reasoning axis closer to planning → keep GPT for premium/escalation planners. **If science-knowledge reasoning dominates, swap `planner → google-antigravity/gemini-3.1-pro-low:high`.** *(2026-07-10 update: GPT-5.6 Sol GA — official eval lead (Agents' Last Exam 52.7 vs 46.9 · AA Intelligence 58.9 vs 54.8) + same $5/$30 price → planner seats moved to `gpt-5.6-sol:xhigh`. ARC-AGI-2 for 5.6 remains unpublished; basis is official eval table + AA index. Source: [evidence/2026-07-10-gpt-5.6-notes.md](./evidence/2026-07-10-gpt-5.6-notes.md).)*
- **The executor axis changed in v1.4.** **Fable 5 became the new #1 at SWE-bench Verified 95.0 / SWE-Bench Pro 80.0** (Opus 4.8 88.6 · GPT-5.5 82.6; Pro 80.3 is a separate Mythos 5 column — [errata E1](./evidence/2026-07-10-errata.md)). Opus 4.8 remains the "strongest subscription-included coder"; Fable 5 has usage-credits billing after 7/12, so always-on executor economics differ (used only in `dream-team`/`escalation`). On terminal/agentic axes, **GPT-5.6 Sol is now SOTA** (Terminal-Bench 2.1 88.8), but ⚠METR found the highest-ever rate of SWE benchmark gaming for Sol, so discount SWE-style scores. daily executor uses same-price successor `gpt-5.6-terra`.
- **xAI `grok-composer-2.5-fast` and `grok-code-fast-1` are for eco/throughput only.** Independent benchmarks are unpublished or inflated, and grok-code-fast-1 is scheduled for retirement; excluding them from core executor seats is correct.
- **default = Anthropic flagship.** Opus 4.8 was reconfirmed by Vals Index as the top served model overall. Fable 5 default (`dream-team`) raises the quality ceiling but carries refusal-classifier and credits caveats ([§5](#per-bundle-design-rationale)). `ultimate-sol`'s Sol router is an opt-in experiment (WARN surfaced).
- **architect long-context correction**: Gemini's nominal 1M is not effective 1M — MRCR v2 8-needle falls from 84.9% at 128K to **26.3% at 1M**, while **Opus 4.6 holds 76% at 1M** (4.8 unpublished). Grok 4.3 multimodal ranks low (12/16), so it is not fit for vision architect → **monorepo architect corrected to Opus**. Standard profile architect=Gemini remains optimal for multimodal/mid-ctx work. (Successor imminent: Gemini 3.5 Pro 2M ctx · Deep Think slipped to July GA; re-verify `{low,high}` clamp rules on release.) See [§6-3](#6-3-remaining-gaps-gap-13--gjc-effective-context-measurement) for the GJC effective cap.

> Sources: [vals.ai GPQA](https://www.vals.ai/benchmarks/gpqa) · [vals.ai SWE-bench](https://www.vals.ai/benchmarks/swebench) · [vals.ai MMMU](https://www.vals.ai/benchmarks/mmmu) · [Gemini 3.1 Pro card (MRCR)](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini thinking docs](https://ai.google.dev/gemini-api/docs/thinking) · [Opus 4.6 (MRCR 76%@1M)](https://www.anthropic.com/news/claude-opus-4-6) · [long-context board](https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/) · [llm-stats ARC-AGI-2](https://llm-stats.com/benchmarks/arc-agi-v2) · [xAI Composer 2.5](https://x.ai/news/composer-2-5)

> 📑 **Full research reports (with primary-source citations)** — the three originals for this placement: [deep-research benchmarks](./evidence/2026-07-03-deep-research-benchmarks.md) · [consultant report](./evidence/2026-07-03-consultant-report.md) · [integrated final report](./evidence/2026-07-03-ultimate-final-report.md). The full evidence for "why this model setup," council consensus, and final answers (Grok=critic / Composer Fast≠executor) lives there. Published reports are preserved verbatim; corrections ship through **[errata](./evidence/2026-07-03-errata.md)** (current E1: Composer 74.7→54.0 is SWE-bench **Pro**, correcting a Verified-column misplacement in the final report).

---

### 6-3. Remaining gaps (gap 1~3 · GJC effective-context measurement)

Opus 4.8 **does support a 1M context window in GJC** (multi-turn accumulation — status bar shows `◫ %/1M`). The table below is separate: measured input-size limits when injecting huge context **in one single message (`@file`)** (3-needle multi-hop retrieval), not the window limit:

| Tokens (single request) | Opus 4.8 | Gemini 3.1 Pro | Grok 4.3 / 4-fast | DeepSeek V4 Pro |
|---|:---:|:---:|:---:|:---:|
| ~130k · 250k · 350k | ✅ | ✅ | ✅ | ✅ |
| ~476k | 🔴 400 | 🔴 400 | ✅ (89s) | ✅ (36s) |
| ~857k | 🔴 | 🔴 | 🔴 400 | — |

- **gap1 — Grok 2M architect swap: ❌ rejected.** Independent Context Arena MRCR v2 shows Grok deep-bin retrieval at the bottom (grok-4.20 256–512k 0.117), no board has a measured 2M bin, and grok-4-fast's 2M has measured retrieval score 0 (marketing/training claim). Live measurement also 400s at 857k. → drop the "use grok-4-fast (2M) above 1M" assumption.
- **gap2 — Opus 4.8 long context:** Opus 4.8 **supports the 1M context window in GJC** (multi-turn agentic file reading accumulates normally to 1M). The ~400k 400 in the table is **single-message (`@file`) input-size limit, not window limit**. (Public MRCR 76%@1M is Opus 4.6; 4.8 unpublished.) → keep monorepo architect=**Opus** (1M ctx works, retrieval is top-tier). Only rare **single-message paste >~400k tokens** should go to `opencode-go/deepseek-v4-pro` (single-message 476k accepted).
- **gap3 — GLM-5.2 vs DeepSeek:** keep eco executor=**DeepSeek V4 Flash** (GLM-5.2 at $1.40/$4.40 is 10× input / 15× output and too expensive for eco). **Upgrade monorepo critic to `opencode-go/glm-5.2`** (live-call verified✅) — new open-weight #1 (AA Index 51; DeepSeek V4 Pro fell 52→**44**), cross-family independence preserved, served inside opencode-go so marginal cost stays low. (Switch back to `deepseek-v4-pro` if low cost is the priority.)

> Key point: the Opus 4.8 context window is **1M working in GJC** (multi-turn accumulation). Only the amount you can paste in a single message is ~400k on Opus/Gemini; above that, **single-paste** is more robust on Grok/DeepSeek (measured). **Do not dump huge inputs in one message; chunk them across turns to use the full 1M window.** (This table passed independent re-check inside GJC — 20/20 agreement, measured 2026-06-18.) Sources: [Context Arena](https://contextarena.ai/) · [GLM-5.2 (AA)](https://artificialanalysis.ai/models/glm-5-2) · [Opus 4.8 what's-new](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)

---

## 7. 🛠️ Install / uninstall

### One-click (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

What the installer does: safely merges 10 bundles into `~/.gjc/agent/models.yml` (auto-updates on re-run — old profiles from the v1.x managed block are replaced), backs up existing files, and sets `daily` as default. Needs only `curl` + `python3`.

```bash
# options
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash  # pick default profile
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

Serial hand-offs decay as `0.99ⁿ`, and multi-agent setups, wired wrong, harden into "false consensus." Design parallelism to defend against both.

```text
serial chain, 5 steps (0.99 each):  0.99^5 ≈ 95.1%    → collapses with length
parallel independent, 5 (OR-success): 1-(0.01)^5 ≈ 100%  → diversity raises reliability
```

**Design principles**
- critic = **different vendor from the main loop, parallel independent vote, then the main loop tallies** (no debate — meta-judge wins).
- critic panel example: `{openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high, google-antigravity/gemini-3.1-pro-low:high}` in parallel → 2/3 dissent or any CRITICAL/BLOCK blocks. **CRITICAL/HIGH dissent cannot be majority-voted away** — resolve it or use a human gate.
- executor fan-out only when **the work is truly independent** (no shared state).
- keep chains short, main loop as the single source of truth (no direct sub-agent consensus).

---

## 10. 💰 Cost

Gemini (`google-antigravity`) runs on **free public preview + higher limits with Google AI Pro/Ultra subscriptions** (not per-token billed — [official Antigravity plans doc](https://antigravity.google/docs/plans), checked 2026-07-10). **Fable 5 is included in Claude subscriptions (Pro/Max/Team) through 2026-07-12 23:59 PT** (7/7→7/12 extension; no official primary extension page, based on multiple secondary reports), capped at 50% of weekly usage limits, and **billed separately via usage credits afterwards** — it is **not "free."** The rest are per-token; key model prices ($/1M, in/out):

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

> † Fable 5 is exactly 2× Opus pricing. The subscription-included window (through ~7/12) still consumes weekly limits.
> ‡ Sonnet 5's **tokenizer change makes the same text ~30% more tokens** — budget its effective cost above the sticker price.
> (Note: via the DeepInfra provider, DeepSeek V4 Pro is $1.30/$2.60 — [§3-3](#3-3-subscription--provider).)

**Relative bundle cost**

| Bundle | Cost | Main driver |
|---|---|---|
| dream-team | ●●●●● | default·executor Fable 5 — ~7/12 subscription-included (50% weekly-limit cap), then credits $10/50 |
| escalation | ●●●●● | executor Fable `:xhigh` (rescue pitcher — intermittent use) + planner Sol `:xhigh` + 4-vendor auth |
| ultimate-opus / ultimate-sol | ●●●●○ | Opus or Sol 3 seats at `:high~xhigh` + Grok critic (xai API) |
| llm-council | ●●●●○ | 4-vendor auth + Sol `:xhigh` planner — council workflow bills by number of votes when executed |
| coding-sprint | ●●●○○ | executor Opus `:high` (raise to max only on failure signals) |
| daily | ●●●○○ | main loop Opus `:medium`, delegation spread across mid/cheap models — subscription OAuth across 3 vendors |
| monorepo | ●●●○○ | executor/architect Opus + Gemini (preview/subscription) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash ($0.14) + Luna ($1) + Gemini preview — but absolute cheapest is built-in `codex-eco` |

> **Three savings levers**: ① push delegated work onto ultra-cheap models (DeepSeek V4 Flash $0.14, Luna $1) and preview/subscription tokens (Gemini) ② escalate effort only on failure ③ keep the main loop on the Anthropic flagship (it is the quality ceiling) but use `:medium` for daily work — if Fable default credits in `dream-team` get heavy, drop default to `opus-4-8:high` (roughly the `ultimate-opus` structure).

---

## 11. 📖 Sources

**Coding (executor)** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1)

**Claude 5 family** · [Fable 5 redeployment announcement](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com model docs](https://platform.claude.com/docs) — pricing · subscription inclusion (~7/12 extension, [Android Authority report](https://www.androidauthority.com/claude-fable-5-free-extension-3685103/)) · effort specs cross-checked 2026-07-02/07-10

**GPT-5.6 (2026-07-09 GA)** · [launch announcement](https://openai.com/index/gpt-5-6/) · [Sol preview (Cerebras 750TPS)](https://openai.com/index/previewing-gpt-5-6-sol/) · [AA: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) · [TechTimes (METR eval gaming)](https://www.techtimes.com/articles/319808/20260707/gpt-56-sol-review-faster-coding-half-fable-5-cost-benchmark-problem.htm) — pricing/evals cross-checked 2026-07-10

**Reasoning (planner)** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**ctx · multimodal (architect)** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**Tool-calling · honesty (default)** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**Independence · routing (critic + design)** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [self-preference grows with capability](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**Official models/pricing** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**Install in one line, best model per role.**

**v2.0.0** · [CHANGELOG](./CHANGELOG.md) · [Maintenance playbook](./MAINTAINING.md) · License [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
