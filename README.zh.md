<div align="center">

# 🧩 GJC 多厂商极限配置

### claude · gpt · grok · gemini · opencode go — 把 5 个订阅*按角色*拆分使用的已验证配置

不用再纠结选哪个模型。**一行安装**，让每个角色自动用上最合适的模型。

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-2.0.1-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/bundles-10%20·%204%20tiers-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="dream-team 配置 — 各角色最强假设" width="100%">

</div>

**[한국어](./README.md) · [English](./README.en.md) · 中文（本页） · [日本語](./README.ja.md)**

> [!NOTE]
> 核心角色与选择器概念已合并至 [GJC 官方文档](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)（[PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860)，`dev`）。本仓库提供一键安装、4 层级 10 捆绑目录和[维护与验证工具](./MAINTAINING.md)。

---

## ⚡ 30 秒安装

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

这一行会**把 10 个捆绑安全合并进 `~/.gjc/agent/models.yml`**，并把默认配置设为 `daily`。原有配置会自动备份，重复执行也会干净更新。

```bash
gjc --mpreset daily        # 仅本次会话生效
gjc                        # 新会话自动使用 daily
```

> [!IMPORTANT]
> **安装后必须登录各提供方。** GJC OAuth 不与原生 `agy`/`grok` CLI 登录共享；请在 GJC 中各执行一次：
>
> ```text
> /login anthropic           # claude
> /login openai-codex        # gpt（ChatGPT 账号 → 提供 base GPT）
> /login google-antigravity  # gemini（Google AI Pro/Ultra 订阅）
> /login xai                 # grok 全系列 + Composer
> ```
> opencode-go 使用 API key：`/provider add` 或环境变量 `OPENCODE_API_KEY`；用 `/provider` 查看认证状态。

> [!TIP]
> 指定默认配置：`curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash` · 跳过默认设置：`GJC_SETUP_DEFAULT=none`。

---

## 🧭 该用哪个捆绑？

| Tier | 捆绑 | 一句话定义 | 何时用 |
|---|---|---|---|
| Core | ⭐ **daily** | Opus 主循环 + 各角色分散委派 — **仅订阅 OAuth 3 厂商即可激活** | **日常默认** |
| Core | 🏎️ **coding-sprint** | 把 executor 升到 Opus 的实现吞吐特化 | 纯实现冲刺 |
| Core | 🚨 **cyber-cop** | reviewer 模式 — architect·critic 主导，专用于 PR 审查·安全审计 | 审查他人 PR·合并门禁·安全审计 |
| Premium (exp) | 🏆 **ultimate-opus** | Anthropic 质量基底 premium | 精度比成本更重要 |
| Premium (exp) | 🧪 **ultimate-sol** | Sol 基底 premium — agentic/终端/浏览轴 | 长程自治 workflow 实验 |
| Premium (exp) | 🔥 **dream-team** | 角色最强假设 — Fable default+executor | 最高质量，接受 credits 成本 |
| Workflow | 🏛️ **llm-council** | 4 系列座位表与 Council 契约 | 需要多系列共识的决策 |
| Workflow | 🛡️ **escalation** | 手动升级 — Fable 救援投手 + critic 3 票评审团 | 合并·安全·支付·不可逆变更 |
| Specialized (exp) | 💸 **eco** | 多厂商低价实验 — *不是绝对最低价* | 成本压力·大批量 |
| Specialized (exp) | 🗺️ **monorepo** | 全局 ≥1M ctx | 巨型代码库 |

完整目录 ↓ [§5](#5-️-最终目录--10-个捆绑--4-层级)；reviewer 模式与预告见下方。

> **🚨 cyber-cop** — GJC 首个 reviewer 模式：architect·critic 是主角，executor 是复现配角。高风险 PR 使用三票评审团；PR #4~#7 曾在合并前拦截 10 个缺陷。
> `gjc-cop 123`
> → [公告文档](./docs/whats-new-cyber-cop.md)

> **Extragoal — GPT-5.5 Pro 最终审查通道（opt-in）** — 将 Pro 深度推理投入开发、QA 与安全检查的第 -1 轮判定席；上游默认通道不依赖它，以 `GJC_SETUP_EXTRAGOAL=1` 安装。
> → [Extragoal Maximalist 文档](./docs/extragoal-maximalist.md)

---

## 1. 🎯 为什么要多厂商

| 角色 | 做什么 | 最佳模型 |
|---|---|---|
| 🧠 **推理/规划**（planner） | 排序、验收标准 | **GPT-5.6 Sol**（Agents' Last Exam 52.7 · 2026-07-09 GA）† — 各捆绑席位见[§5](#5-️-最终目录--10-个捆绑--4-层级)（例外：cyber-cop·monorepo=Gemini，eco=Luna） |
| 🔨 **实现**（executor） | 真正写/改代码 | **Claude Fable 5**（SWE-bench Verified **95.0**）— 订阅内最强是 **Opus 4.8**（88.6） |
| 🔭 **代码评审**（architect） | 大型仓库导航、架构 | **Gemini 3.1 Pro**（多模态 MMMU-Pro 81%）† · 超长上下文（>200k）→ **Opus** |
| ⚖️ **独立批评**（critic） | 对抗式验证 | **cross-family**（与主循环不同厂商） |
| 🎛️ **编排**（default） | 工具调用、路由、诚实性 | **Anthropic 旗舰** — Opus 4.8（路由质量 = 全系统上限；`dream-team` 用 Fable 5。非 Anthropic 路由只有 opt-in `ultimate-sol`（Sol）与不含 Anthropic 的 `eco`（Terra）） |

---

## 2. 🧭 核心设计

> **固定一个强主循环（default = Anthropic 旗舰 Opus/Fable）+ 按信号委派 + 按失败信号升档 effort。**

<div align="center">
<img src="assets/architecture.svg" alt="一个主循环（default）+ 4 个子代理 — 按信号委派" width="100%">
</div>

三条设计原则：

- **主循环绝不让步。** 默认使用 Anthropic 旗舰（Opus 4.8 — `dream-team` 用 Fable 5）；例外仅为 opt-in `ultimate-sol`（Sol）与不含 Anthropic 的 `eco`（Terra）。
- **多样性只在「验证」环节获益。** 让 `critic` 用不同厂商以保持独立，但串行链要短（可靠性按 `0.99ⁿ` 衰减）。
- **effort 是非对称经济学。** `medium→high` 只提升 1~2 分却要约 23 倍 token；只在解不出来时才升档。

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

**GJC 0.9.6 实际生效值**（2026-07-10 真实调用测试；与 API 官方规格存在差异）：

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

### 五条硬规则

1. Gemini Pro 只支持 `low`/`high`；高推理必须字面钉住 `gemini-3.1-pro-low:high`（0.9.6 起模糊空间 fail-closed，错误 id 会 `not found`）。
2. openai-codex 上下文**按模型区分**：`gpt-5.4`=**1M** · `gpt-5.5`=**272K** · `gpt-5.6 3 种`=**373K**（0.9.6 上调；与 API 1.05M 规格不同的 usable prompt budget）。
3. Sonnet（4.6/5）在 GJC 中不支持 `xhigh`/`max`；**Fable 5 不支持 `max`**（分别被夹取到 high/xhigh）。
4. opencode-go 省略 `:effort`（仅 deepseek-v4 系列例外支持）。
5. xai `grok-4.5` 上限为 `high`；范围外静默夹取。gpt-5.6 三款接受 `:max`，但深度未验证，出货上限仍是 `xhigh`。

> **脚注（上游缺口）**：Claude 5 家族按 API 官方规格都支持到 `max`；GJC 0.9.1~0.9.6 的 fable 回退与 sonnet-5 夹取是引擎侧缺口，已上报上游。

### 3-3. 订阅 → 提供方

| 订阅 | provider-id | 备注 |
|---|---|---|
| claude | `anthropic` | 全 effort；含 Claude 5 家族（Fable 5·Sonnet 5） |
| gpt | `openai-codex` | **ChatGPT 账号 → base GPT（gpt-5.6 sol/terra/luna · 5.5 · 5.4）**；ctx：5.4=1M · 5.5=272K · 5.6=373K |
| grok | `xai` | 全系列 + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra 订阅 token**；Gemini + 捆绑 Claude（Opus 4.6 — 截至 2026-07-02，之后未确认） |
| opencode go | `opencode-go` | API key（`OPENCODE_API_KEY`） |

> [!NOTE]
> ChatGPT（Codex）仅提供 base GPT，不支持独立 `-codex` 变体；`google-vertex` 与 DeepInfra 是 API key 的付费替代路径。

### 3-4. 选择器语法

```text
<provider-id>/<model-id>:<effort>            例）anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   （Gemini 高推理 — 引擎的官方路径）
opencode-go/<model>                           （省略 effort = 模型默认）
```

---

## 4. 📊 基准依据

| 角色（维度） | 领先者 | 数据 |
|---|---|---|
| executor（SWE-bench Verified） | **Fable 5** | **95.0%**（Opus 4.8 88.6 = **订阅内最强** · GPT-5.5 82.6 · Gemini 3.1 Pro 80.6） |
| planner（长周期工作流·推理） | **GPT-5.6 Sol**† | Agents' Last Exam 52.7（5.5：46.9）· AA Intelligence 58.9 — GPQA 单项第一 Sonnet 5 96.2 · 科学知识 Gemini 3.1 Pro 94.3（[深度解读](./docs/deep-dive-role-fit.md#6-2-역할-배치-최적성-검토-deep-research--실측)） |
| architect（上下文·多模态） | **Gemini 3.1 Pro**† | 1M 上下文 · MMMU-Pro 81% |
| default（工具调用·诚实性） | **Opus 4.8 / Fable 5** | 路由质量 = 全系统上限（Fable 有 refusal·计费注意事项 — [§5](#5-️-最终目录--10-个捆绑--4-层级)） |
| critic（独立性） | **cross-family** | 元裁判 > 辩论式聚合 |

**核心共识原则** — † planner 已以 2026-07-10 Sol GA 取代 2026-07-02 Gemini 3.1 Pro 快照；architect 轴在 Gemini 3.5 Pro 发布时重新验证。

1. **default = Anthropic 旗舰（Opus/Fable）固定**；例外为 `ultimate-sol`（Sol）及不含 Anthropic 的 `eco`（Terra）。
2. **architect = Gemini 3.1 Pro（多模态）/ Opus（超长上下文）**；200k+ 文本有效检索用 Opus。
3. **critic = cross-family**，以缓解 self-preference bias。
4. **结构 = 强主循环 + 按信号委派 + 按失败升档 effort。**
5. **不要逐查询切换配置**；只在模式边界切换。

---

## 5. 🗂️ 最终目录 — 10 个捆绑 · 4 层级

<div align="center">
<img src="assets/profiles-matrix.svg" alt="配置 × 角色矩阵" width="100%">
</div>

> ★ = 日常推荐。v2.0.0 是 4 层级的 10 个捆绑：全部 `required_providers ≥ 2`，默认 `critic=cross-family`（例外为 `SAME_FAMILY_OK`+WARN），并遵循引擎 effort 硬规则及[§6](#6--验证矩阵)选择器验证；2026-07-10 gjc **0.9.6** 电池中的出货席位均为绿色。

<details>
<summary><b>📋 展开完整 YAML（模型映射与 gjc-profiles.yml 一致 — 已去除注释）</b></summary>

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
<summary><b>v1.11 → v2 迁移</b></summary>

`ultimate`→`ultimate-opus`，`ultimate-f5`/`legend`→`dream-team`；新增 `llm-council`·`ultimate-sol`。`solo-anthropic`/`solo-openai`/`claude-codex`/`claude-codex-max` 按多厂商原则移除，对应需求由 GJC 0.9.6 内置 `claude-*`、`codex-*`、`opus-codex`、`fable-opus-codex` 吸收（并非映射等价）。详见 [CHANGELOG](./CHANGELOG.md) 与 [v2 说明](./docs/whats-new-v2.md)。

</details>

> [!TIP]
> `opencode-go` 以 `OPENCODE_API_KEY` 激活 `eco` executor 与 `monorepo` critic；验证与候选详情见[韩文正本 §5](./README.md#프로필별-설계-근거)。

各捆绑的设计理由与 caveat 已浓缩；完整目录见[韩文正本 §5](./README.md#5-️-최종-카탈로그--10-번들--4계층)，逐捆绑说明见[设计依据](./README.md#프로필별-설계-근거)。

---

## 6. ✅ 验证矩阵

> 图例：✅ 真实调用绿色（括号为验证日）· 🔴 失败 · ⚠ 注意/夹取 · †‡ 脚注 · ●○ 相对成本。
> 2026-07-10 gjc **0.9.6** 对各提供方核心选择器以 `gjc -p --no-session --no-tools --model <sel> "..."` 真实调用（[rerun-3](./evidence/2026-07-10-selectors-rerun-3.md)；0.9.5 为 rerun-2）；出货席位均为绿色，且当日 antigravity 漂移促成 eco.critic 替换。

| 提供方 | 已验证选择器 |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh` · `claude-sonnet-5:high` · `claude-opus-4-8:high` · `claude-sonnet-4-6:high` — sel ✅（07-10） |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh` · `gpt-5.6-terra:high`/`:xhigh` · `gpt-5.6-luna:high` · `gpt-5.5:high` · `gpt-5.4:high` — sel ✅（07-10；5.5=07-02） |
| `xai` | `grok-4.5:medium`/`:high` · `grok-4-fast:high` · `grok-4-1-fast:high` · `grok-code-fast-1` · `grok-composer-2.5-fast` — sel ✅（07-10；4-1 已退役） |
| `grok-build` | `grok-4.3`（裸选择器）— sel ✅（07-02） |
| `google-antigravity` | `gemini-3.1-pro-low`/`:high` · `gemini-3-flash`/`:low` — sel ✅（07-10） |
| `opencode-go` | `deepseek-v4-flash` · `deepseek-v4-pro` · `glm-5.2` · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` — sel ✅（07-02） |

- `fable-5:max`→xhigh、`sonnet-5:xhigh/max`→high、`grok-4.5:xhigh/max`→high 是静默夹取，不是失败。
- GPT-5.6 三款 `:max` 被接受但深度未验证，故未出货；`gpt-5.5:high` 是 07-02 绿色金丝雀。
- `grok-4-1-fast` 即使能调用，也在 2026-05-15 retire 后按 grok-4.3 费率 redirect 计费，故 v2 排除。
- 0.9.6 起 Gemini 模糊空间 fail-closed；`gemini-3.1-pro-high` 的 0.9.5 静默 `-low` 解析不再复现。
- `glm-5.2` 自 0.7.10 起在捆绑目录中，且需要 `OPENCODE_API_KEY`。

<details>
<summary><b>失败的选择器（请避免）</b></summary>

- `openai-codex/gpt-5.3-codex` · `gpt-5.2-codex` · `gpt-5.1-codex-max/mini` — ChatGPT 账号不支持。
- `google-antigravity/gemini-3.1-pro-high` — 0.9.6 为 not found；高推理使用 `gemini-3.1-pro-low:high`。
- `gemini-3.5-flash-low` · `gemini-3.5-flash` · `gemini-pro-agent` — 2026-07-10 下午 not found。
- `gemini-3-pro` — 已退役。
- `claude-sonnet-4-6-thinking` — 404。
- `gpt-oss-120b` — 500。
- `opencode-go/*` — 未设置 `OPENCODE_API_KEY` 时失败。

</details>

> [!NOTE]
> antigravity 的 live 表面当日也会变化，`--list-models` 标示可能是缓存；采纳席位前真实调用。发现未刷新时重新登录/重试，或使用捆绑 id（eco critic 备选 `opencode-go/deepseek-v4-pro`；GLM 使用 `zai/glm-5.2` 并加入 `zai` provider）。

<details>
<summary><b>延迟参考（微基准 2026-07-02；仅 Grok 4.5 为 2026-07-09 streaming）</b></summary>

| 选择器 | 编码 | 推理 | 备注 |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **全场最快** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | 编码比 sonnet-5 慢 +3~4s |
| `grok-4.5:medium` / `:high` | ~14s / ~50s | TTFT ~13s / ~48s | high 仅用于高风险 critic |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | 编码延迟离群值 |
| `glm-5.2` | **21.9s** | 4.0s | 编码最慢 — 当 critic 无妨 |

</details>

```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
```

角色→模型的深度研究与实测分析已移至[docs/deep-dive-role-fit.md](./docs/deep-dive-role-fit.md)（仅韩文）；其中涵盖 Sol planner 世代替换、Gemini 名义 1M 与有效检索的差异，以及单条消息约 400k 限制不等于上下文窗口、需要分块累积的结论。

---

## 7. 🛠️ 安装 / 卸载

按[§30 秒安装](#-30-秒安装)完成安装与登录。

```bash
# 选项
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash  # 指定默认配置
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash           # 跳过默认设置
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash       # 覆盖 agent 目录
```

### 手动安装 / 验证 / 卸载

把 [`gjc-profiles.yml`](./gjc-profiles.yml) 的 `profiles:` 块粘贴到 `~/.gjc/agent/models.yml` 下，然后 `gjc --mpreset daily --default`。

```bash
gjc --list-models daily                       # 确认
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # 回滚（恢复备份）
```

> [!WARNING]
> **GJC 0.7.10~0.9.1 预设 rename/delete 注意**：会删除 `models.yml` 的全部注释，包括安装器管理区块哨兵；删除的配置可能在重装时复活。请检查结果；彻底移除以恢复备份（`cp … .bak-*`）最可靠。0.9.6 尚未复验。

---

## 8. 🔀 动态路由

> [`routing-rules.md`](./routing-rules.md) 是仅韩文文档；将其放入项目 `AGENTS.md`，或以 `gjc --append-system-prompt @routing-rules.md` 注入。

<div align="center">
<img src="assets/routing-tree.svg" alt="工作信号 → 委派路由" width="100%">
</div>

**工作信号 → 委派** — 只在信号明确时委派；主循环能直接做就直接做。

<div align="center">
<img src="assets/effort-ladder.svg" alt="自适应 effort 升档" width="100%">
</div>

**effort 阶梯** — 只因解不出而升档；下限为 low；Gemini 是 low↔high 单跳。

| 信号 | 切换 → |
|---|---|
| 会话开始·一般工作 | `daily` |
| 纯实现冲刺 | `coding-sprint` |
| 合并/发布前·安全·支付 | `escalation`（手动触发 — routing-rules 的 Escalation 契约） |
| PR 审查·安全审计会话 | `cyber-cop` |
| 需要多系列共识的决策 | `llm-council`（+ routing-rules 的 Council 契约） |
| 精度至上（opt-in premium） | `ultimate-opus` / `ultimate-sol`（Sol 轴实验）/ `dream-team`（Fable·credits） |
| 大批量重构·迁移 | `eco` |
| 进入巨型代码库 | `monorepo` |
| 仅单厂商运营 | GJC 内置配置（`claude-opus`·`codex-*` 等 — 不在本目录内） |

---

## 9. 🧪 并行代理 + 可靠性

```text
串行 5 步（各 0.99）：0.99^5 ≈ 95.1%   /   并行独立 5 个（OR 成功）：1-(0.01)^5 ≈ 100%
```

- critic 必须**与主循环不同厂商，先并行独立投票、再由主循环汇总**（禁止辩论 — 元裁判更优）。
- critic 评审团示例：`{openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high, google-antigravity/gemini-3.1-pro-low:high}` 并行 → 2/3 反对或任一 CRITICAL/BLOCK 即拦截；**CRITICAL/HIGH dissent 不可由多数票否决**，必须解决或进入 human gate。
- executor 扇出仅在工作真正独立（无共享状态）时。
- 链要短，主循环作为唯一事实源（子代理之间不直接达成共识）。

---

## 10. 💰 成本

Gemini 使用 [Google AI Pro/Ultra](https://antigravity.google/docs/plans) 订阅 token；其余按 token 计费（$/1M，输入/输出）。Fable 的内含与 credits 注意事项见 §5。

| 模型 | $/1M (in/out) | 角色 |
|---|---|---|
| Claude Fable 5 | 10 / 50（批量 5/25 · 缓存命中 1）† | dream-team default·executor · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor 基础设施 |
| Claude Sonnet 5 | 3 / 15（入门价 2/10 至 2026-08-31）‡ | eco executor 备选 |
| GPT-5.6 Sol | 5 / 30（Fast 模式为 12.5/75） | planner（daily·sprint·ultimate-opus·dream-team·council·escalation）·ultimate-sol 3 席·cyber-cop executor·critic |
| GPT-5.6 Terra | 2.5 / 15 | daily executor · coding-sprint critic · llm-council executor · eco default |
| GPT-5.6 Luna | 1 / 6 | eco planner（v2 新采用） |
| Grok 4.5 | 2 / 6（实效输入约 $0.84 @88% cache） | critic（premium 3 种·llm-council·escalation）— xai API key |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 单条 paste 兜底 |
| Gemini 3.1 Pro / 3-flash | 预览/订阅 token | planner·architect·critic |

> † Fable 5 单价恰为 Opus 的 2 倍；订阅内含部分（~7/12）同样消耗每周额度。
> ‡ Sonnet 5 因 tokenizer 变更，同一文本会多出 ~30% token；实际成本应高于标价估算。
> （参考：DeepSeek 走 DeepInfra 提供方时 V4 Pro 为 $1.30/$2.60 — [§3-3](#3-3-订阅--提供方)。）

**配置相对成本**

| 配置 | 成本 | 主要成本来源 |
|---|---|---|
| dream-team | ●●●●● | default·executor Fable 5 — ~7/12 订阅内含（每周额度 50% 上限），之后 credits $10/50 |
| escalation | ●●●●● | executor Fable `:xhigh`（救援投手 — 间歇使用）+ planner Sol `:xhigh` + 4 厂商认证 |
| ultimate-opus / ultimate-sol | ●●●●○ | Opus 或 Sol 3 席 `:high~xhigh` + Grok critic（xai API） |
| llm-council | ●●●●○ | 4 厂商认证 + Sol `:xhigh` planner — 执行 Council 工作流时按票数计费 |
| coding-sprint | ●●●○○ | executor Opus `:high`（仅失败信号时升 max） |
| daily | ●●●○○ | 主循环 Opus `:medium`，委派中低价分散 — 订阅 OAuth 3 厂商 |
| monorepo | ●●●○○ | executor/architect Opus + Gemini（预览/订阅）+ GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash（$0.14）+ Luna（$1）+ Gemini 预览；*绝对最低价*是内置 `codex-eco` |

---

## 11. 📖 来源

**编码（executor）** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1)
**Claude 5 家族** · [Fable 5 重新发布公告](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com 模型文档](https://platform.claude.com/docs) — 价格、订阅内含（[Android Authority 报道](https://www.androidauthority.com/claude-fable-5-free-extension-3685103/)）与 effort 规格交叉确认 2026-07-02/07-10
**GPT-5.6 (2026-07-09 GA)** · [发布公告](https://openai.com/index/gpt-5-6/) · [Sol 预览(Cerebras 750TPS)](https://openai.com/index/previewing-gpt-5-6-sol/) · [AA: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) · [TechTimes(METR 评估 gaming)](https://www.techtimes.com/articles/319808/20260707/gpt-56-sol-review-faster-coding-half-fable-5-cost-benchmark-problem.htm)
**推理·上下文·路由** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982) · [self-preference bias](https://arxiv.org/abs/2410.21819) · [自我偏好随能力一同增大](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)
**官方模型/价格** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

<div align="center">

**一行安装，各角色用最佳模型。**
**v2.0.1** · [CHANGELOG](./CHANGELOG.md) · [维护与验证手册](./MAINTAINING.md) · 许可证 [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
