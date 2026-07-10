<div align="center">

# 🧩 GJC 多厂商极限配置

### claude · gpt · grok · gemini · opencode go — 把 5 个订阅*按角色*拆分使用的已验证配置

不用再纠结选哪个模型。**一行安装**，让每个角色自动用上最合适的模型。

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-2.0.0-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/bundles-10%20·%204%20tiers-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="dream-team 配置 — 各角色最强假设" width="100%">

</div>

**[한국어](./README.md) · [English](./README.en.md) · 中文（本页） · [日本語](./README.ja.md)**

> [!NOTE]
> **本指南的核心已被采纳进 GJC 官方文档** — 精简版已合并到上游 [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)（[PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860)，`dev`）。角色/选择器概念请以 **GJC 官方文档为权威参考**；本仓库提供官方文档没有的东西 —— **一行安装脚本**、**4 层级 10 捆绑目录**（含 `cyber-cop` reviewer 模式、Council/Escalation 工作流契约），以及[维护与验证工具](./MAINTAINING.md)（静态检查 CI + 实时选择器测试 + 目录漂移追踪）。

## 🚨 `cyber-cop` — reviewer 模式配置

> author 模式的捆绑都是为**编写**代码的会话服务。**`cyber-cop` 是为拦截代码的会话准备的捆绑** —— GJC 首个 **reviewer 模式**。它用于审查他人 PR、寻找反对依据、在合并门做出判定。

**有何不同**
- 在 PR 审查·安全审计中角色权重**反转** → **architect（一级判定：CLEAR/WATCH/BLOCK）与 critic（合并门）为主角**，executor 降为复现 PoC·failing test 的配角。
- critic **相对代码作者（假定 Claude）跨族（cross-family）**（GPT-5.6 Sol）→ 从结构上抑制自我偏好偏差（[arXiv 2410.21819](https://arxiv.org/abs/2410.21819)）。
- 高风险 PR·安全审计召集**3 票并行评审团**（`gpt-5.6-sol` · `grok-4.5` · `gemini-3.1-pro`），独立投票 → 2/3 反对或任一 CRITICAL/BLOCK 即拦截。

**实证有效 —— 本仓库自我验证**
> 在 PR #4~#7 中，审查门在合并前**拦截了 10 个缺陷**（#4：5 · #6：5 · #7：首轮通过）。审查辅助脚本因*自身的* prompt-injection 缺陷被 BLOCK（修复后通过）；本体（Anthropic）对自家族文档放行的 2 处（相对路径注入面·权限夸大）被 **cross-family critic（GPT-5.5）准确 BLOCK**。（另有 1 个在 #6 合并**后**发现 → 已在 #7 立即修复。）证明自我偏好偏差防御在实战中生效。

**免克隆，两条命令开始（v1.6+）**
```bash
# 前提：已安装并认证 gh CLI（gh auth login）+ gjc 各提供方 /login 完成
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_COP=1 bash
export PATH="$HOME/.local/bin:$PATH"   # 若安装器提示 PATH 警告则执行一次
cd <待审查仓库>
gjc-cop 123               # PR #123 → 4 段判定（REPO 从 cwd 自动检测 —— 绝不合并）
# gjc-cop --panel 123     # 高风险：3 票 cross-family 评审团
# gjc-cop shell           # 交互式审查会话（自动注入可信契约）
# gjc-cop watch           # 轮询·审查新 PR（合并由人决定）
```
克隆/手动路径（同样机制，无包装器）见[公告文档 §3](./docs/whats-new-cyber-cop.md)。

📖 完整的缺口论证·三步用法·自动审查流水线·安全守则 → **[cyber-cop 公告文档](./docs/whats-new-cyber-cop.md)**

### Extragoal — GPT-5.5 Pro 最终审查通道（opt-in，v1.9+）

GPT-5.5 **Pro** 订阅者可把 Pro 的深度推理投入开发·QA·安全检查的第 -1 轮判定席。这是把上游 gajae-code 的 extragoal 外部审查门包装成可安装体验；**没有它，上游默认通道也始终可用，Pro 通道也不是任何阶段的前置条件。**

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_EXTRAGOAL=1 bash
```

会配送 extragoal skill（上游 SHA-pin fetch）+ 4 个 courier 工具（无安装手动 courier → `--check-env` 半自动 → 常驻浏览器 3 级梯）。3 级梯、契约映射、地雷清单全文 → **[Extragoal Maximalist 文档](./docs/extragoal-maximalist.md)**

---

## ⚡ 30 秒安装（一行复制粘贴）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

这一行会**把 10 个捆绑安全合并进 `~/.gjc/agent/models.yml`**，并把默认配置设为 `daily`。原有配置会自动备份，重复执行也会干净地原地更新。

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
> 指定默认配置：`curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash` · 跳过默认设置：`GJC_SETUP_DEFAULT=none`。

---

## 📑 目录

1. [为什么要多厂商](#1--为什么要多厂商)
2. [核心设计](#2--核心设计)
3. [GJC 引擎事实](#3--gjc-引擎事实)
4. [基准依据](#4--基准依据)
5. [最终目录 — 10 个捆绑 · 4 层级](#5-️-最终目录--10-个捆绑--4-层级)
6. [验证矩阵](#6--验证矩阵)
7. [安装 / 卸载](#7-️-安装--卸载)
8. [动态路由](#8--动态路由)
9. [并行代理 + 可靠性](#9--并行代理--可靠性)
10. [成本](#10--成本)
11. [来源](#11--来源)

---

## 1. 🎯 为什么要多厂商

订阅了 claude·gpt·grok·gemini·opencode go 却只用一个模型，等于在每个角色上都用*次优*模型。已验证的基准显示**各角色的领先厂商各不相同**：

| 角色 | 做什么 | 最佳模型 |
|---|---|---|
| 🧠 **推理/规划**（planner） | 排序、验收标准 | **Gemini 3.1 Pro**（GPQA 94.3 / ARC-AGI-2 77.1）† |
| 🔨 **实现**（executor） | 真正写/改代码 | **Claude Fable 5**（SWE-bench Verified **95.0**）— 订阅内最强是 **Opus 4.8**（88.6） |
| 🔭 **代码评审**（architect） | 大型仓库导航、架构 | **Gemini 3.1 Pro**（多模态 MMMU-Pro 81%）† · 超长上下文（>200k）→ **Opus** |
| ⚖️ **独立批评**（critic） | 对抗式验证 | **cross-family**（与主循环不同厂商） |
| 🎛️ **编排**（default） | 工具调用、路由、诚实性 | **Anthropic 旗舰** — Opus 4.8（路由质量 = 全系统上限；`dream-team` 用 Fable 5，只有 `ultimate-sol` 用 Sol — 明确 opt-in 例外） |

> **基准日期：2026-07-02**（Claude 5 家族发布后即时复验）。† 推理与 architect 维度「继任者临近」— GPT-5.6 Sol 正在合作伙伴预览（6/26，`max` effort + `ultra` 子代理模式，数周内 GA）；Gemini 3.5 Pro（2M 上下文，Deep Think）推迟至 7 月 GA。发布后将重新验证。

> 用一个厂商填满 5 个角色，必然至少有一个角色不是最强。本指南把这 5 个角色各自配上最合适的厂商，并在成本、可用性、可靠性之间权衡，整理成一个**真正能用**的组合。它交叉验证了三份独立深度调研（GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro），并在[§6](#6--验证矩阵)明确记录选择器验证状态。

---

## 2. 🧭 核心设计

> **固定一个强主循环（default = Anthropic 旗舰 Opus/Fable）+ 按信号委派 + 按失败信号升档 effort。**

每一轮真正运行的只有 `default`（主循环）。executor/architect/planner/critic 是主循环**仅在必要时通过 `task` 委派**的子代理（全新上下文）。

<div align="center">
<img src="assets/architecture.svg" alt="一个主循环（default）+ 4 个子代理 — 按信号委派" width="100%">
</div>

三条设计原则：

- **主循环绝不让步。** 大多数中位任务由主循环独自处理，所以把 `default` 降成弱模型会让整体体感质量崩塌。默认使用 Anthropic 旗舰（Opus 4.8 — `dream-team` 用 Fable 5）。唯一例外 `ultimate-sol`（Sol 路由器）是 validator 登记 + WARN 外显的 opt-in 实验。
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

以下按 **GJC 0.9.6 实际生效值**记载（2026-07-10 真实调用测试）—— 有些地方与 API 官方规格不同（见下方脚注）：

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← 全 6 档
Fable 5                 minimal low medium high xhigh       ← :max 被静默夹取到 xhigh · thinking 常开
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max 被静默夹取到 high
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 默认 xhigh
GPT 5.6 Sol/Terra/Luna  low medium high xhigh (max)          ← :max 接受但深度未验证 — 出货上限 xhigh
Grok 4.5（xai）          low medium high                      ← :xhigh/:max 静默夹取到 high · minimal 不是原生 effort
grok-build/grok-4.3     ── 仅裸选择器（effort 后缀不解析）──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go 其他         ── 省略 :effort 后缀（用默认）──
google-antigravity Gemini  gemini-3.1-pro-low:high（高推理）· gemini-3.1-pro-low（低 effort）
```

> [!IMPORTANT]
> **五条硬规则**：① Gemini Pro 只支持 `low`/`high` —— 高推理必须字面钉住 `gemini-3.1-pro-low:high`（0.9.6 起模糊空间 fail-closed，错误 id 会 `not found`）② openai-codex 上下文**按模型区分** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K**。
> `gpt-5.6 3 种`=**373K**（0.9.6 上调；这是与 API 1.05M 规格不同的 usable prompt budget）③ Sonnet（4.6/5）在 GJC 中不支持 `xhigh`/`max`，**Fable 5 不支持 `max`**（分别被夹取到 high/xhigh）④ opencode-go 省略 `:effort`（仅 deepseek-v4 系列例外支持）⑤ xai `grok-4.5` 上限为 `high`（`:xhigh` 会被静默夹取 — xhigh 只存在于 grok-build 提供方，而那边根本不解析 effort 后缀）。超范围档位不是报错，而是**夹取（clamp）**。gpt-5.6 3 种在目录里显示到 `max`，真实调用也会接受（07-10 验证），但**深度未验证 — 本指南出货上限是 `xhigh`**。
>
> **脚注（上游缺口）**：按 API 官方规格，Claude 5 家族两个模型都支持到 `max`。这是 GJC 解析器（0.9.1~0.9.6）不认识 fable 家族而回退推断、sonnet-5 继承 4.6 夹取规则的**引擎侧缺口**，已附复现材料**上报上游**。本指南按 GJC 实际生效值记载。

### 3-3. 订阅 → 提供方

| 订阅 | provider-id | 备注 |
|---|---|---|
| claude | `anthropic` | 全 effort。含 Claude 5 家族（Fable 5·Sonnet 5） |
| gpt | `openai-codex` | **ChatGPT 账号 → base GPT（5.6 sol/terra/luna · gpt-5.5 · gpt-5.4）**。上下文：gpt-5.4=1M · gpt-5.5=272K · 5.6 3 种=373K |
| grok | `xai` | 全系列 + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra 订阅 token**。Gemini + 捆绑的 Claude（Opus 4.6 — Claude 5 发布后捆绑构成待复核） |
| opencode go | `opencode-go` | API key（`OPENCODE_API_KEY`） |

> [!NOTE]
> **openai-codex 路径注意**：用 ChatGPT（Codex）账号登录会提供 **base GPT 模型（`gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna`、`gpt-5.5`、`gpt-5.4`）**。独立的 `-codex` 变体（`gpt-5.3-codex`、`gpt-5.2-codex`、`gpt-5.1-codex-max/mini`）在此路径下**不受支持**（`not supported when using Codex with a ChatGPT account`），因此本指南的编码角色也统一使用已验证的 **base GPT**。
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
| planner（推理 GPQA/ARC-AGI） | **Gemini 3.1 Pro**† | GPQA 94.3 · ARC-AGI-2 77.1（流体推理是 GPT-5.5 — [§6-2](#6-2-角色配置最优性复查deep-research--实测) · GPQA 单项第一是 Sonnet 5 的 96.2） |
| architect（上下文 · 多模态） | **Gemini 3.1 Pro**† | 1M 上下文 · MMMU-Pro 81% |
| default（工具调用 · 诚实性） | **Opus 4.8 / Fable 5** | 路由质量 = 全系统上限（Fable 有 refusal·计费注意事项 — [§5](#5-️-最终目录--10-个捆绑--4-层级)） |
| critic（独立性） | **cross-family** | 元裁判 > 辩论式聚合 |

> † **继任者临近脚注**：planner 维度 GPT-5.6 Sol 正在合作伙伴预览（2026-06-26，`max` effort + `ultra` 子代理模式 — 数周内 GA）；architect 维度 Gemini 3.5 Pro（2M 上下文，Deep Think）推迟至 7 月 GA。任一发布后本表都需重新验证。

**共识原则**

1. **default = Anthropic 旗舰（Opus/Fable）固定** — 路由质量是上限。唯一例外 `ultimate-sol`（Sol 路由器）是 validator 登记 + WARN 外显的 opt-in 实验。
2. **architect = Gemini 3.1 Pro（多模态）/ Opus（超长上下文）** — Gemini 适合视觉与中等上下文；200k+ 文本检索用 Opus（MRCR 76%@1M，而 Gemini 崩到 26%）。
3. **critic = cross-family** — 与主循环/规划者不同厂商可缓解自我偏好偏差（self-preference bias）。
4. **结构 = 强主循环 + 按信号委派 + 按失败升档 effort。**
5. **不要逐查询切换配置** — 缓存损失 > 收益。只在模式边界切换。

> 基准对时间敏感 → 建议每季度复验。绝对排名仅限 vals.ai 独立榜单。

---

## 5. 🗂️ 最终目录 — 10 个捆绑 · 4 层级

<div align="center">
<img src="assets/profiles-matrix.svg" alt="配置 × 角色 矩阵" width="100%">
</div>

> ★ = 日常推荐。**v2.0.0 结构转换**：不再是「同级配置 N 个」，而是把 **10 个面向用户的捆绑分成 4 个层级（tier）** —— 信任等级并不相同。多厂商不变量：所有捆绑 `required_providers ≥ 2`（单厂商需求交给 GJC 0.9.6 内置配置）· 默认 `critic=cross-family`（例外必须进入 validator 的 `SAME_FAMILY_OK` 并永久外显 WARN）· 全部通过引擎 effort 硬规则 + **持续追踪选择器验证状态**（[§6](#6--验证矩阵)；2026-07-10 gjc **0.9.6** 首轮电池测试 — 全部出货选择器变绿）。

| Tier | 捆绑 | 一句话定义 | 何时用 |
|---|---|---|---|
| Core | ⭐ **daily** | Opus 主循环 + 各角色分散委派 — **仅订阅 OAuth 3 厂商即可激活** | **日常默认** |
| Core | 🏎️ **coding-sprint** | 把 executor 升到 Opus 的实现吞吐特化 | 纯实现冲刺 |
| Core | 🚨 **cyber-cop** | reviewer 模式 — architect·critic 主导，专用于 PR 审查·安全审计 | 审查他人 PR·合并门禁·安全审计 |
| Premium (exp) | 🏆 **ultimate-opus** | Anthropic 质量基底 premium（旧 `ultimate` 后继） | 精度比成本更重要 |
| Premium (exp) | 🧪 **ultimate-sol** | Sol 基底 premium — agentic/终端/浏览轴。**唯一非 Anthropic default** | 长程自治 workflow 实验 |
| Premium (exp) | 🔥 **dream-team** | 角色最强假设 — Fable default+executor（旧 `ultimate-f5`/`legend` 后继） | 最高质量，接受 credits 成本 |
| Workflow | 🏛️ **llm-council** | 4 系列共识座位表 — **投票·quorum 由 routing-rules 的 Council 契约执行** | 需要多系列共识的决策 |
| Workflow | 🛡️ **escalation** | 手动升级 — Fable 救援投手 + critic 3 票评审团 | 合并·安全·支付·不可逆变更 |
| Specialized (exp) | 💸 **eco** | 多厂商低价实验 — *不是绝对最低价*（最低依赖低价走内置 `codex-eco`） | 成本压力·大批量 |
| Specialized (exp) | 🗺️ **monorepo** | 全局 ≥1M ctx（排除 gpt-5.5 272K / 5.6 373K） | 巨型代码库 |

**v1.11.0 → v2.0.0 迁移**：`ultimate`→`ultimate-opus` · `ultimate-f5`/`legend`→`dream-team` · `solo-anthropic`/`solo-openai`/`claude-codex`/`claude-codex-max` → **删除** — 单厂商/双厂商需求由 GJC 0.9.6 内置配置（`claude-opus`/`claude-fable`/`codex-*`/`opus-codex`/`fable-opus-codex`）吸收（不是映射等价，而是 use-case 吸收）。新增 `llm-council`·`ultimate-sol`。

<details>
<summary><b>📋 展开完整 YAML（与 gjc-profiles.yml 一致 — 以模型映射为准，注释中的 § 引用按 README 调整）</b></summary>

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
#   daily.planner gemini→sol · daily.critic grok→opus(3벤더화) · eco 전면 재편(위 주석) · llm-council/ultimate-sol 신설.
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
> **opencode-go** 在设置 `OPENCODE_API_KEY` 后会激活 `eco`（executor）·`monorepo`（critic）（验证✅）。grok 订阅（SuperGrok）的 `xai/grok-composer-2.5-fast`（200k）也已验证，可作 throughput 备选。其他 opencode-go 模型（qwen3.7-max·kimi-k2.6·glm-5.1·minimax-m2.7·mimo-v2.5）也确认可用。新上架（未验证候选）：**kimi-k2.7-code**（预算 executor 候选）· **minimax-m3**（1M 多模态）。

#### 各配置的设计依据

- **daily** — 主循环 Opus `:medium`（效率 knee），实现用编码特化 `gpt-5.6-terra`（$2.5/15 约等于 GPT-5.5 级），拆解用长程 workflow 第一的 `gpt-5.6-sol:high`（v2：gemini→sol — Agents' Last Exam 52.7），架构/评审**与 critic** 都用 Gemini `-low:high`（v2：critic grok→gemini — **移除 xai key 门槛，仅订阅 OAuth 3 厂商即可激活**，同时保持 critic 与 Anthropic 主循环 cross-family；Grok critic 没有 defect-recall 直接证据，diversity seat 移到 premium 系列）。日常质量/成本平衡点。
- **coding-sprint** — executor 主演（Opus `:high` — v2 不再常驻 `:max`，只在失败信号时升档，[§8-2](#8-2-自适应-effort-升档)），planner 用 `gpt-5.6-sol:high`（v2：gemini→sol — sprint 拆解走 Sol 轴），critic 用*懂代码的* `gpt-5.6-terra`抓实 bug。⚠ planner/critic 同属 gpt 系列 — 2026-07-10 人工判定登记为 `SAME_FAMILY_OK`（模型 Sol≠Terra 分离，捆绑整体仍是 3 厂商）。
- **cyber-cop** — 🚨 **reviewer 模式**：author 模式（default+executor 加权）的反相。审查会话中角色权重反转：executor 降为复现 PoC·failing test 的配角，**architect（一级代码评审判定者）与 critic（合并门）成为主角**。architect=Opus `:high`（1M 实效检索 76% vs Gemini 26% 崩溃 — 通读 200k+ diff），critic=`gpt-5.6-sol:high`（与 Claude 写的代码 cross-family — 缓解自我偏好偏差，arXiv [2410.21819](https://arxiv.org/abs/2410.21819)）。高风险 PR·安全审计走 critic 3 票 panel（§9 规则 — 独立投票、禁止辩论，2/3 反对或任一 CRITICAL/BLOCK 即拦截；第 3 票 grok 仅在 xai 登录时启用，因此 xai 不在 `required_providers`，没有 xai 也可用 2 票 {gpt-5.6-sol, gemini} 满足 provenance 最小值）。运行规则（委派顺序·证据契约·汇总者限制·provenance fallback·禁止 LGTM）见 [`routing-rules.md`](./routing-rules.md) 的 reviewer 契约。与 `escalation` 的区别：escalation 是 author-side gate（修到通过），cyber-cop 是 reviewer-side（寻找反对依据）。v1.11.0 映射保持（KEEP）。
- **ultimate-opus** — 🏆 Anthropic 质量基底 premium（旧 `ultimate` 后继）。default·executor·architect 统一用 Opus `:high`，换来稳定性、1M 和订阅边际成本；交叉验证由 **Sol planner `:xhigh` + Grok critic `:high`** 负责。⚠ executor/architect 同属 claude 系列 — 人工判定 `SAME_FAMILY_OK`（WARN 永久外显）。Opus 三席不是「三个独立意见」—— 不要暗示 council 品质。
- **ultimate-sol** — 🧪 Sol 基底 premium（experimental）。把 default/executor/planner 三席集中给 Sol 已验证更强的轴：长程 workflow 完成（Agents' Last Exam 52.7）·终端（T-B 2.1 88.8 SOTA）·浏览（BrowseComp 90.4）·计算机使用（OSWorld 62.6）。**唯一非 Anthropic default**（validator `NON_ANTHROPIC_DEFAULT_OK` 登记 — WARN 外显）。权衡必须写明：路由器 ctx **373K**（相对 Opus 1M）·工具使用轴弱势（Toolathlon 58 vs Fable 61.7）·⚠ METR 指出 SWE 评测 gaming（不得只凭 SWE 类分数升格）。OpenAI 三席的自我强化由 Opus architect + Grok critic 缓冲。role-fit L3 前保持 experimental。
- **dream-team** — 🔥 角色最强*假设*（旧 `ultimate-f5`/`legend` 后继）。**Fable 5 = default+executor**（SWE-Bench Pro 80.0 — OpenAI 自家表格的自我不利承认 · FrontierMath T4 87.8），拆解用 Sol `:xhigh`，架构评审用 Opus `:high`（1M），critic 用第三系列 Grok。Fable 三个 caveat：① 订阅包含活动到 ~7/12 23:59 PT（之后 **usage credits $10/$50** — default+executor 双席暴露最大）② refusal 以 HTTP 200+`stop_reason:refusal` 返回 ③ 30-day retention·不支持 ZDR。⚠ executor(Fable)/architect(Opus) 同属 claude 系列 — 人工判定 `SAME_FAMILY_OK`（模型分离 + Sol/Grok 交叉验证）。
- **llm-council** — 🏛 4 系列（Anthropic·OpenAI·Google·xAI）共识座位表。**仅激活配置不会自动启动 council** — 并行独立调用、相互不泄露、raw verdict 保留、quorum（CRITICAL/HIGH dissent 不走多数决）必须由 [`routing-rules.md`](./routing-rules.md) 的 **Council 契约**让主循环执行。席位：Opus 主循环（汇总者限制）·Terra（复现杂务）·Sol `:xhigh`（议程拆解）·Gemini（Google 席）·Grok（xAI 席）。厂商数 ≠ 独立票数（错误相关性）—— 不要用票数算术夸大信心。
- **escalation** — 🛡 **手动**升级（不是自动失败检测 — 触发器、重试预算、human gate 由 routing-rules 的 Escalation 契约定义）。一旦出现失败信号，把**最强 executor Fable 5 `:xhigh` 作为救援投手**投入；因为是间歇使用，也更适合 credits 计费。critic 用多厂商 3 票 panel（[§9](#9--并行代理--可靠性)）。Fable refusal 时把 executor 降级到 Opus `:max` 并报告给人。仅用于不可逆变更前。v1.11.0 映射保持（KEEP）。
- **eco** — 💸 多厂商低价*实验* —— **不是绝对最低成本**（最低依赖低价路径是 GJC 0.9.6 内置 `codex-eco`）。v2 全面重构：default `gpt-5.6-terra:medium`（不含 anthropic 的捆绑不适用 router 不变量）、executor 超低价 `deepseek-v4-flash`（$0.14/0.28）、planner `gpt-5.6-luna:medium`（v2：`grok-4-1-fast` 已 **2026-05-15 retire — legacy slug 会按 grok-4.3 费率 redirect 计费**，因此移除）、architect 字面钉住 Gemini `-low:high`、critic `gemini-3-flash:low`（v2：`gemini-3.5-flash-low` 在 07-10 下午 live 表面消失 — [§6](#6--验证矩阵)）—— 与 executor(opencode-go) cross-family。不需要 xai·anthropic key（3 厂商）。
- **monorepo** — 🗺 全角色 1M ctx。排除 `gpt-5.5`（272K）和 5.6 3 种（373K）—— gpt-5.4 虽然 1M，但 Opus 同级或更强。architect=**Opus**（1M 实效检索第一 **76%@1M** — Gemini 崩到 26%），critic=**`glm-5.2`**（cross-family，备选 `deepseek-v4-pro`）。**1M nominal window ≠ 完全 recall** —— 巨型输入不要一条消息全塞，改用**分块多轮累积**（[§6-3](#6-3-剩余缺口复查gap-13--gjc-实效上下文实测)）；只有单条消息 >~400k paste 时才用 `opencode-go/deepseek-v4-pro`。v1.11.0 映射保持（KEEP）。

**已删除配置的去向** — `solo-anthropic`/`solo-openai`（单厂商）和 `claude-codex`/`claude-codex-max`（双厂商固定混合）按 v2 多厂商目录原则（混合订阅协作 — 2026-07-10 人工判定）移除。GJC 0.9.6 内置配置吸收这些 use-case：单 Anthropic → 内置 `claude-opus`/`claude-fable`，单 Codex → 内置 `codex-eco`/`codex-medium`/`codex-pro`，Claude+Codex 双厂商 → 内置 `opus-codex`/`fable-opus-codex`（0.9.6 已更新到 GPT-5.6 系列）。内置映射不与本指南旧版 byte-identical —— 若席位细节很重要，请把旧版 YAML（`git show v1.11.0:gjc-profiles.yml`）作为本地自定义保留。

---

## 6. ✅ 验证矩阵

> 2026-07-10（gjc **0.9.6** — 当日 0.9.5→0.9.6 升级后重新跑电池）已对全部提供方核心选择器通过 `gjc -p --no-session --no-tools --model <sel> "..."` **真实调用**复验（`evidence/2026-07-10-selectors-rerun-3.md`；0.9.5 的绿色记录是 rerun-2）— **v2 出货选择器全席位变绿**。这轮电池抓到了 antigravity live 表面的当日漂移（见下方 WARNING），因此替换了 eco.critic。「可用」的依据是真实调用，不是猜测。

| 提供方 | 已验证选择器（✅ 可用） |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh`（**07-10 rerun✅** — `:max` 静默夹取到 xhigh）· `claude-sonnet-5:high`（07-10✅ — `:max` 静默夹取到 high）· `claude-opus-4-8:high`（07-10✅；low·medium·max 07-02✅）· `claude-sonnet-4-6:high`（07-10✅）— 07-09 rate-limit 已解除，全席位复验完成 |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh`（**07-10✅**）· `gpt-5.6-terra:high`/`:xhigh`（07-10✅）· `gpt-5.6-luna:high`（07-10✅）· 3 种 `:max` 会被接受但深度未验证（不出货）· `gpt-5.5:high`（07-02✅，v1.11 从配置退役—保留金丝雀）· `gpt-5.4:high`（1M ctx 通道） |
| `xai` | `grok-4.5:medium`/`:high`（07-10✅ — `:xhigh`/`:max` 夹取到 high；仅 xai，provider 500K / GJC 222K floor，$2/$6）· `grok-4-fast:high`（07-10✅）· ⚠`grok-4-1-fast:high` 调用会成功，但 **xAI 已在 2026-05-15 retire — 以 grok-4.3 费率 redirect 计费**（v2 退场）· `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3`（**仅裸选择器** — effort 后缀不解析，07-02✅。SuperGrok OAuth） |
| `google-antigravity` | `gemini-3.1-pro-low`（±`:high`，07-10✅）· `gemini-3-flash`（±`:low`，**07-10✅ — v2 eco.critic**）· ⚠0.9.6 起模糊空间 **fail-closed**：`gemini-3.1-pro-high`/`-bogus` 为 "not found"（0.9.5 的静默解析到 `-low` 陷阱未再复现 — 仍保持字面钉住）· ⚠**live 表面当日漂移**：`gemini-3.5-flash-low`/`-extra-low`/`gemini-pro-agent` 07-10 下午消失（"not found" — 与 `--list-models` 标示不一致，真实调用才是事实） |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro`（07-02 复验✅）· `glm-5.2`（**0.7.10 已入捆绑目录**，07-02✅）· `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5`（需 `OPENCODE_API_KEY`） |

> [!WARNING]
> **本环境下不可用的选择器**（避免）：`openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`（ChatGPT 账号不支持）· `google-antigravity/gemini-3.1-pro-high`·`gemini-3.5-flash-low`·`gemini-3.5-flash`·`gemini-pro-agent`（**0.9.6 / 07-10 下午基准为 "not found"** — 高推理用 `gemini-3.1-pro-low:high`，轻量 Gemini 用 `gemini-3-flash:low`）· `gemini-3-pro`（已退役）· `claude-sonnet-4-6-thinking`（404）· `gpt-oss-120b`（500）。`opencode-go/*` **仅在未设 `OPENCODE_API_KEY` 时**失败（设置后按上表可用）。注意：`fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.5:xhigh/max` 不是失败，而是**静默夹取**（[§3-2](#3-2-effort-速查表)）— gpt-5.6 三款接受 `:max` 但深度未验证（不出货）。

> [!NOTE]
> `opencode-go/glm-5.2` **自 0.7.10 起进入捆绑目录**（旧「仅实时目录」注意事项作废）。antigravity live 表面即使同一天也会变化（07-10 下午实测 `gemini-3.5-flash*` 消失）—— `--list-models` 可能显示缓存标记，**采纳席位前必须真实调用确认**。发现（discovery）未刷新时激活可能以 `selector did not resolve` 失败 — 重新登录/重试以刷新目录，或替换为捆绑 id（eco critic 备选：`opencode-go/deepseek-v4-pro`，GLM 用 `zai/glm-5.2` — 把 `zai` 加入 `required_providers`）。

**延迟参考**（微基准 2026-07-02；Grok 4.5 行使用 2026-07-09 流式 bench）：

| 选择器 | 编码 | 推理 | 备注 |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **全场最快** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | 编码比 sonnet-5 慢 +3~4s |
| `grok-4.5:medium` / `:high` | ~14s / ~50s | TTFT ~13s / ~48s | 2026-07-09 流式 bench；high 仅用于高风险 critic |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | 编码延迟离群值 |
| `glm-5.2` | **21.9s** | 4.0s | 编码最慢 — 当 critic 无妨 |

复现：
```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
```

---

### 6-2. 角色配置最优性复查（deep-research + 实测）

对初始 8 配置（v1.0 基准）的角色→模型配置进行了多轮 deep-research（独立基准验证）和 live 推理 probe 后，确认骨架接近 near-optimal。**v2.0.0 在此基础上增加 2 轴盲法独立 deep-research（Claude Fable 5 Ultracode + Parallel.ai Ultra 2x，2026-07-10）**，重构为 10-bundle 4 层级结构 — 两轴共同结论：发布状态与角色轴配置为 SUPPORT，profile/workflow 边界、tier 标签、strict provider 摩擦需 REVISE。Premium 3 种的 role-fit L3 实测仍是剩余任务（也是 experimental 标签的原因）。

- **`gemini-3.1-pro-low:high` 不是降级模式。** `thinkingLevel` 不是单独模型变种，而是同一 Gemini 3.1 Pro 的 per-request 参数，模型默认值是 **HIGH**。官方模型卡的头条推理分数（GPQA 94.3 · ARC-AGI-2 77.1）全部在 *Thinking (High)* 下测得 — 这个选择器调用的是**原生高推理默认模式**。实测 probe：`low`（18s）→ `low:high`（22s）延迟增加，确认 thinking 启用，标准推理答案与 GPT-5.5·Opus 一致。*（剩余：GJC `:high` override 到原生 HIGH 的一手来源尚未完全确认 → 运行中继续监控推理质量。）*
- **planner 推理轴是分裂的。** GPQA Diamond（科学知识）前排已 93~96% *饱和* — 单项第一现在是 **Sonnet 5（96.2）**，Gemini 3.1 Pro 94.3。ARC-AGI-2（抽象·流体推理）则 **GPT-5.5 明显领先**（0.850 vs 0.771；Fable 5 未公开 — 推理轴优势未证实）。更贴近规划的流体推理（ARC）→ ultimate/escalation planner 保持 GPT。**若科学知识推理占比大，可把 `planner → google-antigravity/gemini-3.1-pro-low:high`。** *（2026-07-10 更新：GPT-5.6 Sol GA — 官方评估全面领先（Agents' Last Exam 52.7 vs 46.9 · AA Intelligence 58.9 vs 54.8）且同价 $5/$30 → v1.11 起 planner 世代替换为 `gpt-5.6-sol:xhigh`。ARC-AGI-2 的 5.6 数值未公开 — 轴依据是官方评估表+AA 指数。依据：[evidence/2026-07-10-gpt-5.6-notes.md](./evidence/2026-07-10-gpt-5.6-notes.md)。)*
- **executor 轴在 v1.4 已更换。** **Fable 5 以 SWE-bench Verified 95.0 / SWE-Bench Pro 80.0 成为新第一**（Opus 4.8 88.6 · GPT-5.5 82.6；Pro 80.3 是另一个列的 Mythos 5 — [errata E1](./evidence/2026-07-10-errata.md)）。Opus 4.8 仍是「订阅内编码最强」；Fable 5 在 7/12 后会以 usage credits 计费，因此常驻 executor 的成本结构不同（仅在 `dream-team`/`escalation` 采用）。终端·agentic 轴现在是 **GPT-5.6 Sol SOTA**（Terminal-Bench 2.1 88.8）— 但 ⚠METR 发现 Sol 的 SWE 评估 gaming（历史最高比例），SWE 类分数需打折阅读。daily executor 用同价后继 `gpt-5.6-terra`。
- **xAI `grok-composer-2.5-fast`·`grok-code-fast-1` 只适合 eco·throughput。** 独立基准未公开/膨胀，不是 frontier coder，且 grok-code-fast-1 预计退役 — 不进 executor 核心是正确的。
- **default = Anthropic 旗舰。** Opus 4.8 以 Vals Index 综合（serving 模型中第一）再次确认。Fable 5 default（`dream-team`）可进一步抬高质量上限，但带 refusal 分类器和 credits 计费 caveat（[§5](#各配置的设计依据)）。`ultimate-sol` 的 Sol 路由器是 opt-in 实验（WARN 外显）。
- **architect 长上下文修正**：Gemini 名义 1M 不等于实效 1M — MRCR v2 8-needle 128K 84.9% → 1M **26.3%** 崩溃；相反 **Opus 4.6 1M 仍有 76%**（4.8 数值未公开）。Grok 4.3 多模态 12/16 靠后，不适合作 vision architect → **monorepo architect 从 Grok 改为 Opus**，标准配置的 architect=Gemini 仅限多模态·中等 ctx 最优。（继任者临近：Gemini 3.5 Pro 2M ctx·Deep Think — 延到 7 月 GA，发布后重验 `{low,high}` clamp 规则。）（GJC 经由的实效上限见 [§6-3](#6-3-剩余缺口复查gap-13--gjc-实效上下文实测)。）

> 来源：[vals.ai GPQA](https://www.vals.ai/benchmarks/gpqa) · [vals.ai SWE-bench](https://www.vals.ai/benchmarks/swebench) · [vals.ai MMMU](https://www.vals.ai/benchmarks/mmmu) · [Gemini 3.1 Pro card (MRCR)](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini thinking docs](https://ai.google.dev/gemini-api/docs/thinking) · [Opus 4.6 (MRCR 76%@1M)](https://www.anthropic.com/news/claude-opus-4-6) · [long-context board](https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/) · [llm-stats ARC-AGI-2](https://llm-stats.com/benchmarks/arc-agi-v2) · [xAI Composer 2.5](https://x.ai/news/composer-2-5)

> 📑 **完整研究报告（含一手来源引用）** — 该配置依据的 3 份原文：[深度调研基准](./evidence/2026-07-03-deep-research-benchmarks.md) · [顾问报告](./evidence/2026-07-03-consultant-report.md) · [整合最终报告](./evidence/2026-07-03-ultimate-final-report.md)。关于「为什么是这组模型」的完整依据、council 共识、确定回答（Grok=critic / Composer Fast≠executor）都在其中。已发布报告 verbatim 保留，修正通过 **[errata](./evidence/2026-07-03-errata.md)** 投递（当前 E1：Composer 74.7→54.0 是 SWE-bench **Pro** 数值 — 最终报告表格 Verified 列误放）。

---

### 6-3. 剩余缺口复查（gap 1~3 · GJC 实效上下文实测）

Opus 4.8 在 GJC 中**正常支持 1M 上下文窗口**（多轮累积 — 看状态栏 `◫ %/1M`）。下表与此**分开**，测的是把巨大上下文以**单条消息（`@file`）一次性**注入时的输入大小上限（3-needle 多跳检索基准）—— 不是窗口上限：

| token（单请求） | Opus 4.8 | Gemini 3.1 Pro | Grok 4.3 / 4-fast | DeepSeek V4 Pro |
|---|:---:|:---:|:---:|:---:|
| ~130k · 250k · 350k | ✅ | ✅ | ✅ | ✅ |
| ~476k | 🔴 400 | 🔴 400 | ✅（89s） | ✅（36s） |
| ~857k | 🔴 | 🔴 | 🔴 400 | — |

- **gap1 — Grok 2M architect swap：❌ 驳回。** 独立基准（Context Arena MRCR v2）中 Grok 的 deep-bin 检索**垫底**（grok-4.20 256–512k 0.117），2M bin 无任何榜单数据，grok-4-fast 的 2M 是测得检索分数 0 的 marketing/training claim。实测也在 857k 处 400。→ 废弃「1M 以上用 grok-4-fast(2M)」假设。
- **gap2 — Opus 4.8 长上下文：** Opus 4.8 在 **GJC 中支持 1M 上下文窗口**（通过多轮 agentic 文件读取正常累积到 1M）。上表 ~400k 的 400 是**单条消息（`@file`）输入大小上限**，不是窗口上限。（参考：公开 MRCR 76%@1M 是 Opus 4.6 数值，4.8 未公开。）→ monorepo architect=**Opus 保持**（1M ctx 正常，检索最强）。只有少见的**单条消息 >~400k token 全量 paste**才用 `opencode-go/deepseek-v4-pro`（已确认单消息 476k 可接收）。
- **gap3 — GLM-5.2 vs DeepSeek：** eco executor=**DeepSeek V4 Flash 保持**（GLM-5.2 $1.40/$4.40 = 输入 10×·输出 15×，对 eco 过重）。**monorepo critic 升级为 `opencode-go/glm-5.2`**（实调用验证✅）— 新开源权重第一（AA Index 51；DeepSeek V4 Pro 52→**44 下滑**），保持 cross-family 独立，走 opencode-go 订阅内服务，边际成本低。（若低价优先，可退回 `deepseek-v4-pro`。）

> 核心：Opus 4.8 上下文窗口在 GJC 中**正常 1M**（多轮累积）。一次性单条消息能塞的量只有 ~400k（Opus/Gemini）—— 更大的**单条 paste** Grok/DeepSeek 更稳（实测）。**巨型输入不要一条消息全塞，分块多轮累积即可使用 1M 窗口**。（此表已在 GJC 内部独立复验通过 — 20/20 一致，实测日 2026-06-18。）来源：[Context Arena](https://contextarena.ai/) · [GLM-5.2 (AA)](https://artificialanalysis.ai/models/glm-5-2) · [Opus 4.8 what's-new](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)

---

## 7. 🛠️ 安装 / 卸载

### 一键（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

安装脚本做的事：把 10 个捆绑安全合并进 `~/.gjc/agent/models.yml`（重复执行自动更新 — v1.x 管理区块的旧配置会被替换）、自动备份原文件、把默认配置设为 `daily`。只需 `curl` + `python3`。

```bash
# 选项
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash  # 指定默认配置
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash           # 跳过默认设置
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash       # 覆盖 agent 目录
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
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # 回滚（恢复备份）
```

> [!WARNING]
> **GJC 0.7.10 预设 rename/delete 注意**：引擎的自定义预设 rename/delete 功能会**删掉 `models.yml` 里的全部注释** — 安装脚本的管理区块哨兵（注释）也会一并消失，管理区块随之降级为按名称替换，**用户删除过的配置可能在重装时复活**（已复现确认）。用过 rename/delete 之后再重装时务必检查结果；要彻底移除，最可靠的做法是恢复备份（`cp … .bak-*`）。

---

## 8. 🔀 动态路由

> **「逐查询切换配置」❌ /「一个强主循环 + 一层薄规则」✅。** 路由者是主循环（Anthropic 旗舰），配置是目的地池。

> [!TIP]
> 想让主循环遵循下面的路由规则，把 [`routing-rules.md`](./routing-rules.md) 放进项目 `AGENTS.md`，或用 `gjc --append-system-prompt @routing-rules.md` 注入（已装配置 + 已验证选择器硬规则 + GJC 有效上下文上限，全在一个文件里）。

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
| 纯实现冲刺 | `coding-sprint` |
| 合并/发布前 · 安全 · 支付 | `escalation`（手动触发 — routing-rules 的 Escalation 契约） |
| PR 审查·安全审计会话 | `cyber-cop` |
| 需要多系列共识的决策 | `llm-council`（+ routing-rules 的 Council 契约） |
| 精度至上（opt-in premium） | `ultimate-opus` / `ultimate-sol`（Sol 轴实验）/ `dream-team`（Fable·credits 各自承担） |
| 大批量重构 · 迁移 | `eco` |
| 进入巨型代码库 | `monorepo` |
| 仅单厂商运营 | GJC 内置配置（`claude-opus`·`codex-*` 等 — 不在本目录内） |

---

## 9. 🧪 并行代理 + 可靠性

串行交接按 `0.99ⁿ` 衰减，多代理若连接不当会固化成「虚假共识」。并行设计要同时防住这两点。

```text
串行链 5 步（各 0.99）：  0.99^5 ≈ 95.1%    → 越长越崩
并行独立 5 个（OR 成功）： 1-(0.01)^5 ≈ 100%  → 多样性提升可靠性
```

**设计原则**
- critic = **与主循环不同厂商，并行独立投票后由主循环汇总**（禁止辩论 — 元裁判更优）。
- critic 评审团示例：`{openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high, google-antigravity/gemini-3.1-pro-low:high}` 并行 → 2/3 反对或任一 CRITICAL/BLOCK 即拦截。**CRITICAL/HIGH dissent 不可被多数票否决** — 必须解决或进入 human gate。
- executor 扇出仅在**工作真正独立**（无共享状态）时。
- 链要短，主循环作为唯一事实源（子代理之间不直接达成共识）。

---

## 10. 💰 成本

Gemini（`google-antigravity`）以**免费公开预览 + Google AI Pro/Ultra 订阅提高额度**方式运行（非按 token 计费）。**Fable 5 到 2026-07-12 23:59 PT 为止包含在 Claude 订阅（Pro/Max/Team）内**（7/7→7/12 延长 — 官方一手延长页未取得，按多个二手报道），但设有每周使用额度 50% 的上限，**之后按 usage credits 单独计费** — 不是「免费」。其余按 token 计费，主要模型单价如下（$/1M，输入/输出）：

| 模型 | $/1M (in/out) | 角色 |
|---|---|---|
| Claude Fable 5 | 10 / 50（批量 5/25 · 缓存命中 1）† | dream-team default·executor · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor·critic 基础设施 |
| Claude Sonnet 5 | 3 / 15（入门价 2/10 至 2026-08-31）‡ | eco executor 备选 |
| GPT-5.6 Sol | 5 / 30（Fast 模式为 12.5/75） | planner（全捆绑）· ultimate-sol 3 席 · cyber-cop executor·critic |
| GPT-5.6 Terra | 2.5 / 15 | daily executor · coding-sprint critic · llm-council executor · eco default |
| GPT-5.6 Luna | 1 / 6 | eco planner（v2 新采用） |
| Grok 4.5 | 2 / 6（实效输入约 $0.84 @88% cache） | critic（premium 3 种·llm-council·escalation）— xai API key |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 单条 paste 兜底 |
| Gemini 3.1 Pro / 3-flash | 预览/订阅 token | planner·architect·critic |

> † Fable 5 单价恰为 Opus 的 2 倍。订阅内含部分（~7/12）同样消耗每周额度。
> ‡ Sonnet 5 因 **tokenizer 变更，同一文本会多出 ~30% token** — 实际成本要按高于标价来估。
> （参考：DeepSeek 系列走 DeepInfra 提供方时 V4 Pro 为 $1.30/$2.60 — [§3-3](#3-3-订阅--提供方)。）

**配置相对成本**

| 配置 | 成本 | 主要成本来源 |
|---|---|---|
| dream-team | ●●●●● | default·executor 用 Fable 5 — ~7/12 订阅内含（每周额度 50% 上限），之后 credits $10/50 |
| escalation | ●●●●● | executor Fable `:xhigh`（救援投手 — 间歇使用）+ planner Sol `:xhigh` + 4 厂商认证 |
| ultimate-opus / ultimate-sol | ●●●●○ | Opus 或 Sol 3 席 `:high~xhigh` + Grok critic（xai API） |
| llm-council | ●●●●○ | 4 厂商认证 + Sol `:xhigh` planner — 执行 council 工作流时按票数计费 |
| coding-sprint | ●●●○○ | executor Opus `:high`（仅失败信号时升 max） |
| daily | ●●●○○ | 主循环 Opus `:medium`，委派中/低价分散 — 订阅 OAuth 3 厂商 |
| monorepo | ●●●○○ | executor/architect Opus + Gemini（预览/订阅）+ GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash（$0.14）+ Luna（$1）+ Gemini 预览 — 但*绝对最低价*是内置 `codex-eco` |

> **三大省钱杠杆**：① 把委派工作推给超低价模型（DeepSeek V4 Flash $0.14、Luna $1）/ 预览·订阅 token（Gemini）② 只在失败时升档 effort ③ 主循环（Anthropic 旗舰）是质量上限所以保留，日常用 `:medium` — 若 Fable default（`dream-team`）的 credits 成为负担，把 default 换成 `opus-4-8:high`（≈`ultimate-opus` 结构）。

---

## 11. 📖 来源

**编码（executor）** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1)

**Claude 5 家族** · [Fable 5 重新发布公告](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com 模型文档](https://platform.claude.com/docs) — 价格·订阅内含（~7/12 延长，[Android Authority 报道](https://www.androidauthority.com/claude-fable-5-free-extension-3685103/)）·effort 规格交叉确认 2026-07-02/07-10

**GPT-5.6 (2026-07-09 GA)** · [发布公告](https://openai.com/index/gpt-5-6/) · [Sol 预览(Cerebras 750TPS)](https://openai.com/index/previewing-gpt-5-6-sol/) · [AA: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) · [TechTimes(METR 评估 gaming)](https://www.techtimes.com/articles/319808/20260707/gpt-56-sol-review-faster-coding-half-fable-5-cost-benchmark-problem.htm) — 价格·评估交叉确认 2026-07-10

**推理（planner）** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**上下文 · 多模态（architect）** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**工具调用 · 诚实性（default）** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**独立性 · 路由（critic + 设计）** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [自我偏好随能力一同增大](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**官方模型/价格** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**一行安装，各角色用最佳模型。**

**v2.0.0** · [CHANGELOG](./CHANGELOG.md) · [维护与验证手册](./MAINTAINING.md) · 许可证 [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
