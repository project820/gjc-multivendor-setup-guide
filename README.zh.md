<div align="center">

# 🧩 GJC 多厂商极限配置

### claude · gpt · grok · gemini · opencode go — 把 5 个订阅*按角色*拆分使用的已验证配置

不用再纠结选哪个模型。**一行安装**，让每个角色自动用上最合适的模型。

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-1.5-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/profiles-13-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/selectors-live%20tested%202026--07--02-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="legend 配置 — 各角色最强模型" width="100%">

</div>

**[한국어](./README.md) · [English](./README.en.md) · 中文（本页） · [日本語](./README.ja.md)**

> [!NOTE]
> **本指南的核心已被采纳进 GJC 官方文档** — 精简版已合并到上游 [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)（[PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860)，`dev`）。角色/选择器概念请以 **GJC 官方文档为权威参考**；本仓库提供官方文档没有的东西 —— **一行安装脚本**、**完整的 13 套配置**（含 `solo-*`、`claude-codex*`、`legend`、`cyber-cop`），以及[维护与验证工具](./MAINTAINING.md)（静态检查 CI + 实时选择器测试 + 目录漂移追踪）。

---

## ⚡ 30 秒安装（一行复制粘贴）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

这一行会**把 13 套配置安全合并进 `~/.gjc/agent/models.yml`**，并把默认配置设为 `daily`。原有配置会自动备份，重复执行也会干净地原地更新。

```bash
gjc --mpreset daily        # 仅本次会话生效
gjc                        # 新会话自动使用 daily
```

> [!IMPORTANT]
> **安装后必须登录各厂商。** GJC 使用自己的 OAuth（不与原生 `agy`/`grok` CLI 登录共享），所以打开 GJC 后各执行一次（浏览器认证）：
>
> ```text
> /login anthropic           # claude
> /login openai-codex        # gpt（ChatGPT 账号 → 提供 base GPT）
> /login google-antigravity  # gemini（Google AI Pro/Ultra 订阅）
> /login xai                 # grok 全系列 + Composer
> ```
> opencode-go 用 API key：`/provider add` 或环境变量 `OPENCODE_API_KEY`。用 `/provider` 查看认证状态。

> [!TIP]
> 指定默认配置：`curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash` · 跳过默认设置：`GJC_SETUP_DEFAULT=none`。

---

## 1. 🎯 为什么要多厂商

订阅了 claude·gpt·grok·gemini·opencode go 却只用一个模型，等于在每个角色上都用*次优*模型。已验证的基准显示**各角色的领先厂商各不相同**：

| 角色 | 做什么 | 最佳模型 |
|---|---|---|
| 🧠 **推理/规划**（planner） | 排序、验收标准 | **Gemini 3.1 Pro**（GPQA 94.3 / ARC-AGI-2 77.1）† |
| 🔨 **实现**（executor） | 真正写/改代码 | **Claude Fable 5**（SWE-bench Verified **95.0**）— 订阅内最强是 **Opus 4.8**（88.6） |
| 🔭 **代码评审**（architect） | 大型仓库导航、架构 | **Gemini 3.1 Pro**（多模态 MMMU-Pro 81%）† · 超长上下文（>200k）→ **Opus** |
| ⚖️ **独立批评**（critic） | 对抗式验证 | **跨厂商**（与主循环不同厂商） |
| 🎛️ **编排**（default） | 工具调用、路由、诚实性 | **Anthropic 旗舰** — Opus 4.8（路由质量 = 全系统上限；`legend`/`ultimate-f5` 用 Fable 5） |

> **基准日期：2026-07-02**（Claude 5 家族发布后即时复验）。† 推理与 architect 维度「继任者临近」— GPT-5.6 Sol 正在合作伙伴预览（6/26，`max` effort + `ultra` 子代理模式，数周内 GA）；Gemini 3.5 Pro（2M 上下文，Deep Think）推迟至 7 月 GA。发布后将重新验证。

> 用一个厂商填满 5 个角色，必然至少有一个角色不是最强。本指南把这 5 个角色各自配上最合适的厂商，并在成本、可用性、可靠性之间权衡，整理成一个**真正能用**的组合。它交叉验证了三份独立深度调研（GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro），并**用真实调用验证了每个配置选择器**（[§6](#6--验证矩阵)）。

---

## 2. 🧭 核心设计

> **固定一个强主循环（default = Anthropic 旗舰 Opus/Fable）+ 按信号委派 + 按失败信号升档 effort。**

每一轮真正运行的只有 `default`（主循环）。executor/architect/planner/critic 是主循环**仅在必要时通过 `task` 委派**的子代理（全新上下文）。

<div align="center">
<img src="assets/architecture.svg" alt="一个主循环（default）+ 4 个子代理 — 按信号委派" width="100%">
</div>

三条设计原则：

- **主循环绝不让步。** 大多数中位任务由主循环独自处理，所以把 `default` 降成弱模型会让整体体感质量崩塌。始终用 Anthropic 旗舰（Opus 4.8 — `legend`/`ultimate-f5` 中为 Fable 5）。
- **多样性只在「验证」环节获益。** 让 `critic` 用不同厂商以保持独立，但串行链要短（可靠性按 `0.99ⁿ` 衰减）。
- **effort 是非对称经济学。** `medium→high` 只提升 1~2 分却要约 23 倍 token。无脑拉满是浪费 —— 只在「解不出来」时才升档。

---

## 3. 🔧 GJC 引擎事实

### 3-1. 五个角色

| 角色 | 运行位置 | 首要能力 |
|---|---|---|
| `default` | **主循环** | 工具调用可靠性 · 诚实性 |
| `executor` | 子代理（仅 `task` 委派时） | 真实编码（SWE-bench） |
| `architect` | 子代理 | 大上下文 · 多模态代码评审 |
| `planner` | 子代理 | 顶级推理 · 排序 |
| `critic` | 子代理 | 独立对抗式批评 |

### 3-2. Effort 速查表

以下按 **GJC 0.7.10 实际生效值**记载 —— 有些地方与 API 官方规格不同（见下方脚注）：

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← 全 6 档
Fable 5                 minimal low medium high xhigh       ← :max 被静默夹取到 xhigh · thinking 常开
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max 被静默夹取到 high
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 默认 xhigh
Grok 4.x（xai）          minimal low medium high              ← grok-4.3 :xhigh 被静默夹取到 high
grok-build/grok-4.3     ── 仅裸选择器（effort 后缀不解析）──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go 其他         ── 省略 :effort 后缀（用默认）──
google-antigravity Gemini  gemini-3.1-pro-low:high（高推理）· gemini-3.1-pro-low（低 effort）
```

> [!IMPORTANT]
> **五条硬规则**：① Gemini Pro 只支持 `low`/`high` ② openai-codex 上下文**按模型区分** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K**（从 400K 缩水到 272K；旧的「codex 272k」一刀切规则作废）③ Sonnet（4.6/5）在 GJC 中不支持 `xhigh`/`max`，**Fable 5 不支持 `max`**（分别被夹取到 high/xhigh）④ opencode-go 省略 `:effort`（仅 deepseek-v4 系列例外支持）⑤ xai `grok-4.3` 上限为 `high`（`:xhigh` 会被静默夹取 — xhigh 只存在于 grok-build 提供方，而那边根本不解析 effort 后缀）。超范围的档位不会报错，而是被**夹取（clamp）**。
>
> **脚注（上游缺口）**：按 API 官方规格，Claude 5 家族两个模型都支持到 `max`。这是 GJC 0.7.10 解析器不认识 fable 家族而回退推断、sonnet-5 继承 4.6 夹取规则的**引擎侧缺口**，已附复现材料**上报上游**。本指南按 GJC 实际生效值记载。

### 3-3. 订阅 → 提供方

| 订阅 | provider-id | 备注 |
|---|---|---|
| claude | `anthropic` | 全 effort。含 Claude 5 家族（Fable 5·Sonnet 5） |
| gpt | `openai-codex` | **ChatGPT 账号 → 提供 base GPT（gpt-5.5/5.4）**。上下文：gpt-5.4=1M · gpt-5.5=272K |
| grok | `xai` | 全系列 + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra 订阅 token**。Gemini + 捆绑的 Claude（Opus 4.6 — Claude 5 发布后捆绑构成待复核） |
| opencode go | `opencode-go` | API key（`OPENCODE_API_KEY`） |

> [!NOTE]
> **openai-codex 路径注意**：用 ChatGPT（Codex）账号登录会提供 **base GPT 模型（`gpt-5.5`、`gpt-5.4`）**。独立的 `-codex` 变体（`gpt-5.3-codex`、`gpt-5.2-codex`、`gpt-5.1-codex-max/mini`）在此路径下**不受支持**（`not supported when using Codex with a ChatGPT account`），因此本指南的编码角色也统一使用已验证的 **base GPT**。
>
> 备选路径：`google-vertex`（API key，按 token 付费，1M 上下文）— 与订阅/配额无关的兜底。另一个是 **DeepInfra**（gjc 0.7.9 新增提供方，API key）：DeepSeek V4 Pro **$1.30/$2.60**（1M 上下文）· V4 Flash $0.09/$0.18 — Standard/Priority（1.5×）层级与 GJC `service-tier` 设置直接对应。

### 3-4. 选择器语法

```text
<provider-id>/<model-id>:<effort>            例）anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   （Gemini 高推理 — 引擎的官方路径）
opencode-go/<model>                           （省略 effort = 模型默认）
```

---

## 4. 📊 基准依据

**各角色已验证的领先者**（vals.ai 独立榜单 · 官方模型卡 — **基准日 2026-07-02**）

| 角色（维度） | 领先者 | 数据 |
|---|---|---|
| executor（SWE-bench Verified） | **Fable 5** | **95.0%**（Opus 4.8 88.6 = **订阅内最强** · GPT-5.5 82.6 · Gemini 3.1 Pro 80.6） |
| planner（推理 GPQA/ARC-AGI） | **Gemini 3.1 Pro**† | GPQA 94.3 · ARC-AGI-2 77.1（流体推理是 GPT-5.5 — [韩文 §6-2](./README.md#6-2-역할-배치-최적성-검토-deep-research--실측) · GPQA 单项第一是 Sonnet 5 的 96.2） |
| architect（上下文 · 多模态） | **Gemini 3.1 Pro**† | 1M 上下文 · MMMU-Pro 81% |
| default（工具调用 · 诚实性） | **Opus 4.8 / Fable 5** | 路由质量 = 全系统上限（Fable 有 refusal·计费注意事项 — [§5](#5-️-最终目录13-套配置)） |
| critic（独立性） | **跨厂商** | 元裁判 > 辩论式聚合 |

> † **继任者临近脚注**：planner 维度 GPT-5.6 Sol 正在合作伙伴预览（2026-06-26，`max` effort + `ultra` 子代理模式 — 数周内 GA）；architect 维度 Gemini 3.5 Pro（2M 上下文，Deep Think）推迟至 7 月 GA。任一发布后本表都需重新验证。

**共识原则**

1. **default = Anthropic 旗舰（Opus/Fable）固定**（多厂商配置）— 路由质量是上限。`solo-*` 用该单厂商最强者作 default。
2. **architect = Gemini 3.1 Pro（多模态）/ Opus（超长上下文）** — Gemini 适合视觉与中等上下文；200k+ 文本检索用 Opus（MRCR 76%@1M，而 Gemini 崩到 26%）。
3. **critic = 跨厂商** — 与主循环/规划者不同厂商可缓解自我偏好偏差（self-preference bias）。
4. **结构 = 强主循环 + 按信号委派 + 按失败升档 effort。**
5. **不要逐查询切换配置** — 缓存损失 > 收益。只在模式边界切换。

> 基准对时间敏感 → 建议每季度复验。绝对排名仅限 vals.ai 独立榜单。

---

## 5. 🗂️ 最终目录（13 套配置）

<div align="center">
<img src="assets/profiles-matrix.svg" alt="配置 × 角色 矩阵" width="100%">
</div>

> ★ = 日常推荐。顶部横幅 = **`legend` 配置**（可持续最强 — 仅 default 用 Fable 5）。按成本平衡的日常推荐是 **`daily`**（executor·critic 换成低价模型）。多厂商配置保持 `default = Anthropic 旗舰（Opus/Fable）`、`critic=跨厂商`（solo-* 用单厂商最强），全部通过引擎 effort 硬规则，且**每个选择器都经真实调用验证**（[§6](#6--验证矩阵)）。

| 配置 | 一句话 | 何时用 |
|---|---|---|
| ⭐ **daily** | Opus 主循环 + 委派给各角色最佳厂商 | **日常默认** |
| 🏆 **ultimate** | 不计成本，各角色最强（可持续版） | 精度比成本更重要 |
| 🔥 **ultimate-f5** | 以 Fable 5 为核心的限时活动版 — **订阅内含至 2026-07-07** | 活动期内的最高精度 |
| 👑 **legend** | 仅主循环用 Fable 5，其余为可持续结构 | 7/7 之后也能维持的最强 |
| 🏎️ **coding-sprint** | executor 主导 + 懂代码的 critic | 纯实现吞吐 |
| 🛡️ **escalation** | 出现失败信号时投入 Fable 5 救援投手 + 多厂商 critic 评审团 | 合并·安全·支付·不可逆变更 |
| 🚨 **cyber-cop** | reviewer 模式 — architect·critic 主导，专用于 PR 审查·安全审计 | 审查他人 PR·合并门禁·安全审计 |
| 💸 **eco** | 仅主循环用 Opus，委派全用便宜/订阅模型 | 成本压力·大批量 |
| 🗺️ **monorepo** | 全局 ≥1M 上下文（排除 gpt-5.5） | 巨型代码库 |
| 🧱 **solo-anthropic** | 全角色 Opus（v1.4：critic 也用 Opus） | 仅单厂商运营 |
| 🤖 **solo-openai** | 全角色 base GPT（5.5=272K · 5.4=1M） | 只订阅 ChatGPT |
| 🤝 **claude-codex** | Claude=执行·上下文 / Codex=推理·批评 | 仅 Claude+Codex 两订阅 |
| 🥇 **claude-codex-max** | claude-codex 的不计成本最强版 | Claude+Codex · 精度优先 |

<details>
<summary><b>📋 展开完整 YAML（与 gjc-profiles.yml 一致 — 以模型映射为准，注释中的 § 引用按 README 调整）</b></summary>

```yaml
profiles:

  daily:                               # ★ 日常默认 (--default daily)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 主循环效率拐点
      executor:  openai-codex/gpt-5.4:high                      # 擅长编码·中等价位($2.5/15)·分散厂商(已验证✅)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 已验证推理第一(GPQA 94.3 / ARC-AGI-2 77.1)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M 上下文·多模态(MMMU-Pro 81%)
      critic:    xai/grok-4.3:medium                            # 跨厂商廉价独立批评($1.25/2.5)

  ultimate:                            # 不计成本，各角色最强 + 分散厂商(可持续版 — 活动版是 ultimate-f5)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # 订阅内编码最强(SWE-bench Verified 88.6)
      planner:   openai-codex/gpt-5.5:xhigh                     # 顶级推理 + OpenAI 多样性
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M 上下文·多模态
      critic:    xai/grok-4.3:high                              # 跨厂商独立批评

  ultimate-f5:                         # 🔥 限时活动：以 Fable 5 为核心 — 订阅内含至 ~2026-07-07(每周额度 50% 上限)，之后按 usage credits 计费($10/$50)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # 路由=质量上限。注意 refusal(HTTP 200+stop_reason)
      executor:  anthropic/claude-fable-5:xhigh                 # SWE-bench Verified 95.0 新科第一。⚠禁用 :max(会被静默夹取到 xhigh)
      planner:   openai-codex/gpt-5.5:xhigh                     # 推理维度 Fable 优势未证实(ARC-AGI-2 未公开) — 保留 GPT
      architect: google-antigravity/gemini-3.1-pro-low:high     # 多模态已验证优势保持(Fable 视觉仅厂商自称)
      critic:    xai/grok-4.3:high                              # 跨厂商不变 — 禁止 Fable 自我评审
      # 7/7 之后：把 default 降到 opus-4-8:high 即为与 legend 相同的可持续结构

  legend:                              # 👑 Ultimate Legend — 7/7 之后也能维持的最强(fable 仅占 default 一席)
    display_name: legend5
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # 路由质量上限 = Fable(usage credits 暴露最小的位置)
      executor:  anthropic/claude-opus-4-8:max                  # 订阅内编码最强(88.6)
      planner:   openai-codex/gpt-5.5:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.3:high
      # 想规避 credits 成本：把 default 换成 opus-4-8:high — 即与 ultimate 相同

  coding-sprint:                       # 纯实现吞吐。executor 主导 + 懂代码的 critic
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 主循环编排
      executor:  anthropic/claude-opus-4-8:max                  # 订阅内编码最强(88.6)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 推理已验证第一，用于轻量规划
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M 上下文评审
      critic:    openai-codex/gpt-5.4:high                      # 懂代码的 critic(抓真实 bug)，跨厂商 vs gemini

  escalation:                          # 高失败成本 — 出现失败信号时投入最强执行者(Fable 5) + 多厂商 critic 并行评审团(§9)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-fable-5:xhigh                 # 失败任务的救援投手(SWE-V 95.0)。间歇使用 = 与 credits 计费也契合
      planner:   openai-codex/gpt-5.5:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.3:high                              # + 3 票跨厂商 critic 评审团(独立投票→主循环汇总)。⚠xai :xhigh 会被静默夹取到 high，故不用
      # (v1.3 之前的 critic :xhigh 实为 no-op 夹取 — xhigh 仅存在于 grok-build 提供方，且那边不支持 effort 后缀)

  cyber-cop:                           # 🚨 reviewer 模式 — PR 审查·安全审计（author 模式的反相）
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high                 # 满足不变式 + 1M ctx。仅作聚合者 — 完整保留·公开 critic 原始判定（routing-rules 契约）
      executor:  openai-codex/gpt-5.5:high                      # 配角 — 复现 PoC·failing test·harness（Terminal-Bench 82.7）
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 审查清单·审计范围（与 critic cross-family）
      architect: anthropic/claude-opus-4-8:high                 # 主角1 — 一线代码审查裁定者，1M 有效检索（MRCR 76% vs Gemini 26%）
      critic:    openai-codex/gpt-5.5:high                      # 主角2 — 合并门禁，与 Claude 编写的代码 cross-family
      # 高风险 PR·安全审计：critic 三票并行评审团 {openai-codex/gpt-5.5:high, xai/grok-4.3:high,
      # google-antigravity/gemini-3.1-pro-low:high} — 独立投票后由主体聚合（禁止辩论），2/3 反对或出现任一 CRITICAL/BLOCK 即阻断

  eco:                                 # 最省 — 仅主循环用 Opus(降 effort)，委派全用超低价/订阅模型(全部已验证✅)
    required_providers: [anthropic, opencode-go, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:low                  # 路由不能降，只降 effort
      executor:  opencode-go/deepseek-v4-flash                  # $0.14/0.28, 1M, 最便宜的 coder(第 5 厂商)。备选: sonnet-5:medium(≈sonnet-4-6:high，入门价 $2/10 至 8/31)
      planner:   xai/grok-4-1-fast:high                         # $0.2/0.5, 2M, 廉价推理
      architect: google-antigravity/gemini-3.1-pro-low          # 订阅 token，低 effort，1M 上下文
      critic:    google-antigravity/gemini-3.5-flash-low        # 订阅 token，轻量，跨厂商 vs executor(opencode-go)。钉住字面 id(旧 'gemini-3.5-flash' 靠模糊匹配)

  monorepo:                            # 巨型代码库 — 全局 1M 上下文(★排除 gpt-5.5 272K — gpt-5.4 是 1M 但 Opus 至少同级)
    required_providers: [anthropic, google-antigravity, opencode-go]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 1M
      executor:  anthropic/claude-opus-4-8:high                 # 1M
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 推理(范围化输入)
      architect: anthropic/claude-opus-4-8:high                 # Opus 4.8 = GJC 支持 1M 上下文窗口(多轮累积·检索最佳)。仅单条消息粘贴限 ~400k — 一次性 >400k 用 opencode-go/deepseek-v4-pro
      critic:    opencode-go/glm-5.2                            # 开源权重第一(AA 51 > V4 Pro 44)，0.7.10 已入捆绑目录，跨厂商 vs anthropic(备选: deepseek-v4-pro)

  solo-anthropic:                      # 仅单厂商运营 — 全角色 Opus(v1.4: critic Sonnet→Opus，能力优先)
    required_providers: [anthropic]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max
      planner:   anthropic/claude-opus-4-8:max
      architect: anthropic/claude-opus-4-8:high                 # 1M，替代 Gemini(兜底第一)
      critic:    anthropic/claude-opus-4-8:high                 # ⚠同一模型自我评审=偏差最大(研究证实) — 质量路径仍是跨厂商配置
      # 不推荐 Sonnet 5 当 critic：评审者 bug 召回率实测下降(63%→50%，仅精确率上升)

  solo-openai:                         # 仅 ChatGPT(Codex) 账号 — 只用 base GPT
    required_providers: [openai-codex]
    model_mapping:
      default:   openai-codex/gpt-5.5:high                      # 路由(最强 base GPT，上下文 272K)
      executor:  openai-codex/gpt-5.5:xhigh                     # 此账号最强 coder
      planner:   openai-codex/gpt-5.5:xhigh                     # 顶级推理
      architect: openai-codex/gpt-5.4:high                      # ★gpt-5.4 = 1M 上下文 — 大输入走这边(5.5 是 272K)
      critic:    openai-codex/gpt-5.4:high                      # ⚠同厂商=独立性弱(权衡)

  claude-codex:                        # ★仅 Claude+Codex(两订阅) — 日常均衡。Anthropic=执行·上下文 / Codex=推理·批评
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 路由·工具可靠
      executor:  anthropic/claude-opus-4-8:high                 # 订阅内编码最强(SWE-bench 88.6)
      planner:   openai-codex/gpt-5.5:high                      # OpenAI 推理旗舰
      architect: anthropic/claude-opus-4-8:high                 # 1M 窗口(规避 gpt-5.5 272K 限制)
      critic:    openai-codex/gpt-5.4:high                      # 跨厂商 vs Opus(executor)，懂代码

  claude-codex-max:                    # Claude+Codex(两订阅)最强 — 不计成本
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # SWE-bench 88.6
      planner:   openai-codex/gpt-5.5:xhigh                     # 顶级推理(ARC-AGI-2 强)
      architect: anthropic/claude-opus-4-8:high                 # 1M 窗口
      critic:    openai-codex/gpt-5.5:high                      # 跨厂商独立批评 vs Opus

# ─────────────────────────────────────────────────────────────────────────────
# Claude 5 家族(2026-07-01~)：Fable 5 = $10/$50(Opus 的 2 倍)，订阅内含仅到 ~7/7(每周额度 50%) — 不是「免费」。
#   Sonnet 5 = $3/$15(入门价 $2/$10 至 2026-08-31)，tokenizer 变更使同一文本多出 ~30% token。
#   GJC 实际生效 effort：fable-5 ≤xhigh · sonnet-5 ≤high(API 两者都支持 max — GJC 解析器缺口，已上报上游)。
# opencode-go：设置 OPENCODE_API_KEY 后启用(用于 eco.executor·monorepo.critic)。
#   已验证✅：deepseek-v4-flash/pro · glm-5.2 · minimax-m2.7 · qwen3.7-max · kimi-k2.6 · mimo-v2.5。
#   新上架(未验证·候选)：kimi-k2.7-code(预算 executor 有力候选) · minimax-m3(1M 多模态)。
# 可选：grok 订阅(SuperGrok OAuth)的 grok-build/composer 也可用：
#   grok-build/grok-4.3(仅裸选择器可用，不支持 effort 后缀 — 已验证✅ 2026-07-02)。
```

</details>

各配置的详细设计依据（含 `ultimate-f5` 的活动条件与 refusal 注意事项、`legend` 的 `display_name` 保护装置、`escalation` 重新设计的诚实记录、7/7 之后的降级路径），以及完整的深度调研基准分析，见 **[韩文权威 README](./README.md#5-️-최종-카탈로그-13종)** 和官方 **[GJC 文档](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)**。特别提示：`solo-anthropic` 全 Opus 是「单厂商约束下能力优先」的选择 — 研究表明**越强的模型自我偏好偏差反而越大**（arXiv [2410.21819](https://arxiv.org/abs/2410.21819) · [2604.22891](https://arxiv.org/abs/2604.22891)），能力并不能抵消偏差；**质量路径仍是跨厂商配置**（Sonnet 5 当 critic 也不推荐 — 评审者 bug 召回率实测从 63% 降到 50%）。

---

## 6. ✅ 验证矩阵

> 每个选择器都在本环境通过 `gjc -p --no-session --no-tools --model <sel> "..."` **真实调用**确认过（**最终验证 2026-07-02，gjc 0.7.10** — 未单独标注的条目为 2026-06-18 验证；核心选择器已由 0.7.10 回归测试重新验证（标注 07-02✅））。「能用」的依据是真实调用，不是猜测。

| 提供方 | 已验证选择器（✅ 可用） |
|---|---|
| `anthropic` | `claude-fable-5`（bare·low·medium·high — `:max` 会被**静默夹取到 xhigh**后照常工作，07-02✅）· `claude-sonnet-5`（bare·medium·high — `:max` 会被**静默夹取到 high**后照常工作，07-02✅）· `claude-opus-4-8`（low·medium·high·max，`:high` 07-02 复验✅）· `claude-sonnet-4-6:high`（07-02 复验✅） |
| `openai-codex` | `gpt-5.5:high`（**07-02 重新认证后复验✅**）· `gpt-5.5:xhigh` · `gpt-5.4:high` · `gpt-5.4-mini:high` |
| `xai` | `grok-4.3:high`（07-02 复验✅ — `:xhigh` 被静默夹取到 high）· `grok-4-1-fast:high`（07-02✅）· `grok-4-fast:high`（07-02✅）· `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3`（**仅裸选择器** — effort 后缀不解析，07-02✅。SuperGrok OAuth） |
| `google-antigravity` | `gemini-3.1-pro-low`（±`:high`，07-02 复验✅）· `gemini-3.5-flash-low`（**新钉住的 id**，07-02✅）· `gemini-3.5-flash`（靠模糊匹配可用，07-02✅）· `gemini-3-flash` · `claude-opus-4-6-thinking`（06-18 — Claude 5 发布后捆绑构成待复核） |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro`（07-02 复验✅）· `glm-5.2`（**0.7.10 已入捆绑目录**，07-02✅）· `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5`（需 `OPENCODE_API_KEY`） |

> [!WARNING]
> **本环境下不可用的选择器**（避免）：`openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`（ChatGPT 账号不支持）· `google-antigravity/gemini-3.1-pro-high`（**0.7.10 的目录列表里出现，但调用仍返回 400** — 已记录的陷阱依旧，引擎请用 `gemini-3.1-pro-low:high`）· `gemini-3-pro`（已退役）· `claude-sonnet-4-6-thinking`（404）· `gpt-oss-120b`（500）。`opencode-go/*` **仅在未设 `OPENCODE_API_KEY` 时**失败（设置后按上表可用）。注意：`fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.3:xhigh` 不是失败，而是**静默夹取**（[§3-2](#3-2-effort-速查表)）。

> [!NOTE]
> `opencode-go/glm-5.2` **自 0.7.10 起进入捆绑目录**（旧「仅实时目录」注意事项作废）。相反，`google-antigravity/gemini-3.5-flash` 这个字面 id 不在目录里（只有 `-low`/`-extra-low`），**是靠模糊匹配碰巧可用**，所以 v1.4 配置改钉 `gemini-3.5-flash-low`。发现（discovery）未刷新时激活可能以 `selector did not resolve` 失败 — 重新登录/重试以刷新目录，或替换为捆绑 id（critic 用 `opencode-go/deepseek-v4-pro`，GLM 用 `zai/glm-5.2` — 把 `zai` 加入 `required_providers`）。

**延迟参考**（微基准 2026-07-02 — 同一组编码·推理提示词，全部选择器答对）：

| 选择器 | 编码 | 推理 | 备注 |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **全场最快** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | 编码比 sonnet-5 慢 +3~4s |
| `grok-4.3:high` | 5.6s | 4.0s | |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | 编码延迟离群值 |
| `glm-5.2` | **21.9s** | 4.0s | 编码最慢 — 当 critic 无妨 |

复现：
```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.4:high" "Reply exactly: OK"
```

> **深度角色配置复查与 GJC 有效上下文实测**（韩文权威版 §6-2 / §6-3）确认骨架接近最优，且 v1.4 更换了 executor 轴：**Fable 5 以 SWE-bench Verified 95.0 成为新科第一**（Opus 4.8 88.6 保持「订阅内编码最强」）；`gemini-3.1-pro-low:high` 调用的是 Gemini 原生高推理模式（非降级）；planner 推理维度分裂（GPQA 已饱和 — 单项第一是 Sonnet 5 的 96.2，而 ARC-AGI-2 流体推理 GPT-5.5 明显领先，Fable 5 未公开）；Opus 在 1M 上下文检索上保持优势而 Gemini 崩溃（因此 monorepo architect = Opus，critic 升级为 `opencode-go/glm-5.2`）；单条 `@file` 输入上限（anthropic/antigravity 约 400k）与 1M 上下文窗口是两回事（巨型输入应跨轮分块累积）。完整表格与出处见 **[韩文 README §6](./README.md#6--검증-매트릭스)**。

---

## 7. 🛠️ 安装 / 卸载

### 一键（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

安装脚本做的事：把 13 套配置安全合并进 `~/.gjc/agent/models.yml`（重复执行自动更新）、自动备份原文件、把默认配置设为 `daily`。只需 `curl` + `python3`。

```bash
# 选项
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash    # 指定默认配置
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash        # 跳过默认设置
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash    # 覆盖 agent 目录
```

### 厂商认证（必需）

安装只放置配置。打开 GJC 后给每个厂商登录一次：

```text
/login anthropic           # claude
/login openai-codex        # gpt（base GPT）
/login google-antigravity  # gemini（Google AI Pro/Ultra 订阅）
/login xai                 # grok 全系列 + Composer
```

opencode-go：`/provider add` 或环境变量 `OPENCODE_API_KEY`。

### 手动安装 / 验证 / 卸载

把 [`gjc-profiles.yml`](./gjc-profiles.yml) 的 `profiles:` 块粘贴到 `~/.gjc/agent/models.yml` 的 `profiles:` 下，然后 `gjc --mpreset daily --default`。

```bash
gjc --list-models daily                       # 确认
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # 回滚(恢复备份)
```

> [!WARNING]
> **GJC 0.7.10 预设 rename/delete 注意**：引擎的自定义预设 rename/delete 功能会**删掉 `models.yml` 里的全部注释** — 安装脚本的管理区块哨兵（注释）也会一并消失，管理区块随之降级为按名称替换，**用户删除过的配置可能在重装时复活**（已复现确认）。用过 rename/delete 之后再重装时务必检查结果；要彻底移除，最可靠的做法是恢复备份（`cp … .bak-*`）。

---

## 8. 🔀 动态路由

> **「逐查询切换配置」❌ /「一个强主循环 + 一层薄规则」✅。** 路由者是主循环（Anthropic 旗舰），配置是目的地池。

> [!TIP]
> 想让主循环遵循下面的路由规则，把 [`routing-rules.md`](./routing-rules.md)（韩文文档 — 其中的选择器/配置名与语言无关）放进项目 `AGENTS.md`，或用 `gjc --append-system-prompt @routing-rules.md` 注入（已装配置 + 已验证选择器硬规则 + GJC 有效上下文上限，全在一个文件里）。

### 8-1. 工作信号 → 委派

<div align="center">
<img src="assets/routing-tree.svg" alt="工作信号 → 委派路由" width="100%">
</div>

规则：**只在信号明确时委派。** 主循环能直接做就直接做。

### 8-2. 自适应 effort 升档

<div align="center">
<img src="assets/effort-ladder.svg" alt="自适应 effort 升档" width="100%">
</div>

- ✅ 因解不出而升档是正当的 / ❌「为了保险升档」是浪费。
- 禁用 minimal。下限到 `low`。Gemini 是 `low↔high` 单跳。

### 8-3. 配置切换（仅模式边界）

| 信号 | 切换 → |
|---|---|
| 会话开始 · 一般工作 | `daily` |
| 合并/发布前 · 安全 · 支付 | `escalation` |
| PR 审查·安全审计会话 | `cyber-cop` |
| 精度至上（Fable 5 活动期 ~2026-07-07） | `ultimate-f5` → 之后 `legend` |
| 大批量重构 · 迁移 | `eco` |
| 进入巨型代码库 | `monorepo` |
| 仅单厂商运营 | `solo-anthropic` |

---

## 9. 🧪 并行代理 + 可靠性

串行交接按 `0.99ⁿ` 衰减，多代理若连接不当会固化成「虚假共识」。并行设计要同时防住这两点。

```text
串行链 5 步(各 0.99)：  0.99^5 ≈ 95.1%    → 越长越崩
并行独立 5 个(OR 成功)： 1-(0.01)^5 ≈ 100%  → 多样性提升可靠性
```

**设计原则**
- critic = **与主循环不同厂商，并行独立投票后由主循环汇总**（禁止辩论 — 元裁判更优）。
- critic 评审团示例：`{xai/grok-4.3, openai-codex/gpt-5.4, google-antigravity/gemini-3.1-pro-low:high}` 并行 → 2/3 反对则废弃。
- executor 扇出仅在**工作真正独立**（无共享状态）时。
- 链要短，主循环作为唯一事实源（子代理之间不直接达成共识）。

---

## 10. 💰 成本

Gemini（`google-antigravity`）以 **Google AI Pro/Ultra 订阅 token** 运行（包含在订阅内，非按 token 计费）。**Fable 5 到 2026-07-07 为止包含在 Claude 订阅（Pro/Max/Team）内**，但设有每周使用额度 50% 的上限，**之后按 usage credits 单独计费** — 不是「免费」。其余按 token 计费，主要模型单价如下（$/1M，输入/输出）：

| 模型 | $/1M (in/out) | 角色 |
|---|---|---|
| Claude Fable 5 | 10 / 50（批量 5/25 · 缓存命中 1）† | ultimate-f5 default·executor · legend default · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor |
| Claude Sonnet 5 | 3 / 15（入门价 2/10 至 2026-08-31）‡ | eco executor 备选 |
| GPT-5.5 | 5 / 30 | planner(ultimate) |
| GPT-5.4 | 2.5 / 15 | executor/critic(daily·sprint) |
| Grok 4.3 | 1.25 / 2.5 | critic |
| Grok 4.1 Fast | 0.2 / 0.5 | eco planner |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 单条粘贴兜底 |
| Gemini 3.1 Pro / 3.5 Flash | 订阅 token | planner·architect·critic |

> † Fable 5 单价恰为 Opus 的 2 倍。订阅内含部分（~7/7）同样消耗每周额度。
> ‡ Sonnet 5 因 **tokenizer 变更，同一文本会多出 ~30% token** — 实际成本要按高于标价来估。
> （参考：DeepSeek 系列走 DeepInfra 提供方时 V4 Pro 为 $1.30/$2.60 — [§3-3](#3-3-订阅--提供方)。）

**配置相对成本**

| 配置 | 成本 | 主要成本来源 |
|---|---|---|
| ultimate-f5 | ●●●●● | default·executor 用 Fable 5 — ~7/7 订阅内含(每周额度 50% 上限)，之后 credits $10/50 |
| legend | ●●●●● | default Fable 5(7/7 后 credits) + executor Opus `:max` |
| ultimate / escalation | ●●●●● | executor Opus `:max`/Fable `:xhigh`(救援投手) + planner GPT-5.5 `:xhigh` |
| coding-sprint | ●●●●○ | executor Opus `:max` |
| solo-anthropic | ●●●●○ | 全角色 Opus(executor/planner `:max`) |
| daily | ●●●○○ | 主循环 Opus `:medium`，委派中/低价分散 |
| monorepo | ●●●○○ | executor/architect Opus + Gemini(订阅) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash($0.14) + 订阅 Gemini |

> **三大省钱杠杆**：① 把委派工作推给超低价模型（DeepSeek V4 Flash $0.14、Grok Fast $0.2）/ 订阅 token（Gemini）② 只在失败时升档 effort ③ 主循环（Anthropic 旗舰）是质量上限所以保留，日常用 `:medium`，成本紧张时 `:low` — 若 Fable default（`legend`）的 credits 成为负担，把 default 换成 `opus-4-8:high`。

---

## 11. 📖 来源

**编码（executor）** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.0](https://www.tbench.ai/leaderboard/terminal-bench/2.0)

**Claude 5 家族** · [Fable 5 重新发布公告](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com 模型文档](https://platform.claude.com/docs) — 价格·订阅内含（~7/7）·effort 规格交叉确认 2026-07-02

**推理（planner）** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**上下文 · 多模态（architect）** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**工具调用 · 诚实性（default）** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**独立性 · 路由（critic + 设计）** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [自我偏好随能力一同增大](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**官方模型/价格** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**一行安装，各角色用最佳模型。**

**v1.5** · [CHANGELOG](./CHANGELOG.md) · [维护与验证手册](./MAINTAINING.md) · 许可证 [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
