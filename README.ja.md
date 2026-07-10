<div align="center">

# 🧩 GJC マルチベンダー究極セットアップ

### claude · gpt · grok · gemini · opencode go — 5つの契約を*役割ごと*に振り分ける検証済み構成

モデル選びで悩むのをやめよう。**ワンライナーでインストール**し、各役割に最適なモデルを自動で割り当てる。

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-2.0.0-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/bundles-10%20·%204%20tiers-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="dream-team 構成 — 役割ごとの最強仮説" width="100%">

</div>

**[한국어](./README.md) · [English](./README.en.md) · [中文](./README.zh.md) · 日本語（このページ）**

> [!NOTE]
> **本ガイドの中核は GJC 公式ドキュメントに採用された** — 圧縮版が上流に [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md) としてマージ済み（[PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860)、`dev`）。役割/セレクタの概念は **GJC 公式ドキュメントを正式リファレンス**とし、本リポジトリはそこに無いもの — **ワンライナー・インストーラ**、4階層 10 バンドルカタログ（`cyber-cop` reviewer モード・Council/Escalation ワークフロー契約を含む）、そして[保守・検証ツール](./MAINTAINING.md)（静的チェック CI + ライブセレクタ検証 + カタログドリフト追跡）— を提供する。

## 🚨 `cyber-cop` — reviewer モードプロファイル

> author モードのバンドルはすべてコードを**書く**セッション用。**`cyber-cop` はコードを止めるセッション**のためのバンドル — GJC 初の **reviewer モード**だ。他人の PR をレビューし、反対根拠を探し、マージゲートで判定する。

**何が違うか**
- PR レビュー・セキュリティ監査では役割の重みが**反転** → **architect（一次判定：CLEAR/WATCH/BLOCK）と critic（マージゲート）が主役**、executor は再現 PoC・failing test の脇役に下がる。
- critic が**コード作成者（Claude 想定）に対して cross-family**（GPT-5.6 Sol）→ 自己選好バイアスを構造的に抑制（[arXiv 2410.21819](https://arxiv.org/abs/2410.21819)）。
- 高リスク PR・セキュリティ監査は**3票並列パネル**（`gpt-5.6-sol` · `grok-4.5` · `gemini-3.1-pro`）を招集し、独立投票 → 2/3 反対または CRITICAL/BLOCK 1 件で遮断。

**実証済み — 本リポジトリが自己検証した**
> PR #4〜#7 でレビューゲートがマージ前に**欠陥 10 件を遮断**した（#4：5 · #6：5 · #7：初回投票で通過）。レビュー補助スクリプトは*自身の* prompt-injection 欠陥で BLOCK され（修正後に通過）、本体（Anthropic）が自家系統の文書を甘く通した 2 点（相対パス注入面・権限の過大表示）を **cross-family critic（GPT-5.5）が正確に BLOCK**。（さらに 1 件が #6 マージ**後**に検出 → #7 で即修正。）自己選好バイアス防御が実戦で機能することを証明した。

**クローン不要、2 コマンドで開始（v1.6+）**
```bash
# 前提：gh CLI インストール・認証済み（gh auth login）+ gjc プロバイダ /login 完了
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_COP=1 bash
export PATH="$HOME/.local/bin:$PATH"   # インストーラが PATH 警告を出した場合は一度実行
cd <レビュー対象リポジトリ>
gjc-cop 123               # PR #123 → 4 セクション判定（REPO は cwd から自動検出 — マージは絶対しない）
# gjc-cop --panel 123     # 高リスク：3 票 cross-family パネル
# gjc-cop shell           # 対話型レビューアセッション（信頼契約を自動注入）
# gjc-cop watch           # 新規 PR をポーリング・レビュー（マージは人間が決定）
```
クローン/手動パス（同じ仕組み、ラッパーなし）は[アナウンス文書 §3](./docs/whats-new-cyber-cop.md)を参照。

📖 ギャップ論証・3 段階の使い方・自動レビューパイプライン・セキュリティ規則の全体 → **[cyber-cop アナウンス文書](./docs/whats-new-cyber-cop.md)**（韓国語正本）

### Extragoal — GPT-5.5 Pro 最終レビューレーン（opt-in, v1.9+）

GPT-5.5 **Pro** 契約者が Pro の深い推論を開発・QA・セキュリティ点検の最終判定席に投入する別レーン。上流 gajae-code の extragoal 外部レビューゲートをインストール可能な体験として包んでいる — **上流の基本レーンはこれ無しでも常に動き、Pro レーンはいかなる段階でも前提条件ではない。**

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_EXTRAGOAL=1 bash
```

extragoal スキル（上流 SHA ピン fetch）+ courier ツール 4 種（無インストール手動 courier → `--check-env` 半自動 → 常駐ブラウザの 3 段ラダー）を配送する。3 段ラダー・契約マッピング・地雷リストの全体 → **[Extragoal Maximalist 文書](./docs/extragoal-maximalist.md)**

---

## ⚡ 30秒インストール（ワンライナーをコピペ）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

この1行で **10 個のバンドルを `~/.gjc/agent/models.yml` に安全にマージ**し、既定プロファイルを `daily` に設定する。既存設定は自動バックアップされ、再実行してもクリーンに更新される。

```bash
gjc --mpreset daily        # このセッションのみ
gjc                        # 新規セッションは自動で daily
```

> [!IMPORTANT]
> **インストール後、各プロバイダへのログインが必要。** GJC は独自の OAuth を使う（ネイティブ `agy`/`grok` CLI のログインとは共有されない）ので、GJC を起動して各コマンドを一度ずつ実行（ブラウザ認証）：
>
> ```text
> /login anthropic           # claude
> /login openai-codex        # gpt（ChatGPT アカウント → base GPT を提供）
> /login google-antigravity  # gemini（Google AI Pro/Ultra サブスク）
> /login xai                 # grok 全ラインナップ + Composer
> ```
> opencode-go は API キー方式：`/provider add` または環境変数 `OPENCODE_API_KEY`。認証状態は `/provider` で確認。

> [!TIP]
> 既定プロファイル指定：`curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash` · 既定設定をスキップ：`GJC_SETUP_DEFAULT=none`。

---

## 📑 目次

1. [なぜマルチベンダーか](#1--なぜマルチベンダーか)
2. [コア設計](#2--コア設計)
3. [GJC エンジンの事実](#3--gjc-エンジンの事実)
4. [ベンチマーク根拠](#4--ベンチマーク根拠)
5. [最終カタログ — 10 バンドル · 4階層](#5-️-最終カタログ--10-バンドル--4階層)
6. [検証マトリクス](#6--検証マトリクス)
7. [インストール / アンインストール](#7-️-インストール--アンインストール)
8. [動的ルーティング](#8--動的ルーティング)
9. [並列エージェント + 信頼性](#9--並列エージェント--信頼性)
10. [コスト](#10--コスト)
11. [出典](#11--出典)

---

## 1. 🎯 なぜマルチベンダーか

claude·gpt·grok·gemini·opencode go を契約しておきながら1モデルしか使わないのは、すべての役割で*次善*モデルを使うのと同じ。検証済みベンチマークは**役割ごとに首位ベンダーが異なる**ことを示す：

| 役割 | 何をするか | 最適モデル |
|---|---|---|
| 🧠 **推論・設計**（planner） | 手順・受け入れ基準 | **Gemini 3.1 Pro**（GPQA 94.3 / ARC-AGI-2 77.1）† |
| 🔨 **実装**（executor） | 実際のコード作成・修正 | **Claude Fable 5**（SWE-bench Verified **95.0**）— サブスク込みの最強は **Opus 4.8**（88.6） |
| 🔭 **コードレビュー**（architect） | 大規模リポ探索・アーキ | **Gemini 3.1 Pro**（マルチモーダル MMMU-Pro 81%）† · 超長文脈（>200k）→ **Opus** |
| ⚖️ **独立批評**（critic） | 敵対的検証 | **クロスファミリー**（メインループと別ベンダー） |
| 🎛️ **オーケストレーション**（default） | ツール呼び出し・ルーティング・誠実性 | **Anthropic フラッグシップ** — Opus 4.8（ルータ品質 = 全体の上限；`dream-team` は Fable 5。非 Anthropic ルータは opt-in `ultimate-sol`（Sol）と Anthropic 非搭載 `eco`（Terra）の 2 つだけ） |

> **ベンチマーク基準日：2026-07-02**（Claude 5 ファミリーのリリース直後に再検証）。† 推論軸の更新：**GPT-5.6 Sol は 2026-07-09 に GA** — v2 カタログで planner 軸の世代交代は反映済み（[§6-2](#6-2-役割配置の最適性検討deep-research--実測)）。architect 軸は Gemini 3.5 Pro（2M 文脈、Deep Think）が 7月 GA に延期 — リリース時に再検証予定。

> 1ベンダーで5役割を埋めると、必ずどこかが最強でなくなる。本ガイドはその5枠を各々の最適ベンダーで埋め、コスト・アクセス性・信頼性まで勘案して**実際に動く**組み合わせにまとめた。3本の独立ディープリサーチ（GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro）を相互検証し、セレクタ検証状態を[§6](#6--検証マトリクス)に明記している。

---

## 2. 🧭 コア設計

> **強いメインループを1つ固定（default = Anthropic フラッグシップ Opus/Fable）+ シグナル駆動の委譲 + 失敗駆動の effort エスカレーション。**

毎ターン実際に走るのは `default`（メインループ）だけ。executor/architect/planner/critic は、メインループが**必要なときだけ `task` で委譲**するサブエージェント（新規コンテキスト）。

<div align="center">
<img src="assets/architecture.svg" alt="1メインループ(default) + 4サブエージェント — シグナル駆動委譲" width="100%">
</div>

3つの設計原則：

- **メインループは絶対に譲らない。** 中央値のタスクはほぼメインループが単独処理するため、`default` を弱モデルに落とすと体感品質が全面崩壊する。基本は Anthropic フラッグシップ（Opus 4.8 — `dream-team` は Fable 5）。非 Anthropic ルータは 2 つだけ：opt-in 実験 `ultimate-sol`（Sol — validator 登載+WARN）と Anthropic 非搭載の低単価実験 `eco`（Terra — ルータ不変式は非適用）。
- **多様性は「検証」でのみ効く。** 独立性のため `critic` は別ベンダーに。ただし直列チェーンは短く（信頼性は `0.99ⁿ` で減衰）。
- **effort は非対称な経済学。** `medium→high` は +1〜2点のためにトークン約23倍。無条件 `max` は無駄 — 「解けなかったとき」だけ上げる。

---

## 3. 🔧 GJC エンジンの事実

### 3-1. 5つの役割

| 役割 | 実行場所 | 最優先能力 |
|---|---|---|
| `default` | **メインループ** | ツール呼び出し信頼性 · 誠実性 |
| `executor` | サブエージェント（`task` 委譲時のみ） | 実コーディング（SWE-bench） |
| `architect` | サブエージェント | 大文脈 · マルチモーダルレビュー |
| `planner` | サブエージェント | 最上位の推論 · 手順化 |
| `critic` | サブエージェント | 独立した敵対的批評 |

### 3-2. Effort チートシート

**GJC 0.9.6 の実効値**である（2026-07-10 実呼び出しバッテリー）— API 公式仕様と異なる箇所がある（下の脚注）：

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← 全6段
Fable 5                 minimal low medium high xhigh       ← :max は xhigh へサイレントクランプ · thinking 常時オン
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max は high へサイレントクランプ
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 既定 xhigh
GPT 5.6 Sol/Terra/Luna  low medium high xhigh (max)          ← :max は受理されるが深度未検証 — 出荷上限 xhigh
Grok 4.5（xai）          low medium high                      ← :xhigh/:max は high へサイレントクランプ · minimal はネイティブ effort ではない
grok-build/grok-4.3     ── bare セレクタのみ（effort サフィックス非解釈）──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go その他       ── effort サフィックス省略（既定）──
google-antigravity Gemini  gemini-3.1-pro-low:high（高推論）· gemini-3.1-pro-low（低 effort）
```

> [!IMPORTANT]
> **5つのハードルール**：① Gemini Pro は `low`/`high` のみ — 高推論は `gemini-3.1-pro-low:high` をリテラルにピン（0.9.6 からファジー空間は fail-closed、誤った id は `not found`） ② openai-codex の文脈は**モデル別** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K** · `gpt-5.6 3種`=**373K**（0.9.6 で引き上げ。API 仕様 1.05M とは別の usable prompt budget）③ Sonnet（4.6/5）は GJC で `xhigh`/`max` 不可 · **Fable 5 は `max` 不可**（それぞれ high/xhigh にクランプ）④ opencode-go は `:effort` 省略（deepseek-v4 系のみ例外的に対応）⑤ xai `grok-4.5` の上限は `high`（`:xhigh` はサイレントクランプ — xhigh は grok-build プロバイダ専用だが、そちらは effort サフィックス自体が解釈されない）。範囲外の段はエラーではなく**クランプ**される。gpt-5.6 3種はカタログに `max` まで表示され、実呼び出しも受理されるが（07-10 検証）、**深度未検証 — 本ガイドの出荷上限は `xhigh`**。
>
> **脚注（上流ギャップ）**：Claude 5 ファミリーは API 公式には両方とも `max` まで対応する。GJC パーサ（0.9.1~0.9.6）が fable ファミリーを知らずフォールバック推論し、sonnet-5 が 4.6 のクランプを継承する**エンジン側のギャップ**であり、再現資料と共に**上流へ報告済み**。本ガイドは GJC 実効値で記載する。

### 3-3. 契約 → プロバイダ

| 契約 | provider-id | 備考 |
|---|---|---|
| claude | `anthropic` | 全 effort。Claude 5 ファミリー（Fable 5·Sonnet 5）を含む |
| gpt | `openai-codex` | **ChatGPT アカウント → base GPT を提供**。ctx: gpt-5.4=1M · gpt-5.5=272K · gpt-5.6 3種=373K。対象モデルは gpt-5.4 · gpt-5.5 · gpt-5.6 sol/terra/luna |
| grok | `xai` | 全ラインナップ + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra サブスクトークン**。Gemini + 同梱 Claude（Opus 4.6 — Claude 5 リリース後の同梱構成は再確認前） |
| opencode go | `opencode-go` | API キー（`OPENCODE_API_KEY`） |

> [!NOTE]
> **openai-codex 経路の注意**：ChatGPT（Codex）アカウントでログインすると **base GPT モデル（`gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna`、`gpt-5.5`、`gpt-5.4`）** が提供される。単体の `-codex` 派生（`gpt-5.3-codex`、`gpt-5.2-codex`、`gpt-5.1-codex-max/mini`）はこの経路では**非対応**（`not supported when using Codex with a ChatGPT account`）なので、本ガイドはコーディング役も検証済みの **base GPT** に統一している。
>
> 代替経路：`google-vertex`（API キー、トークン従量課金、1M 文脈）— サブスク/クォータに依存しないフォールバック。もう一つは **DeepInfra**（gjc 0.7.9 の新プロバイダ、API キー）：DeepSeek V4 Pro **$1.30/$2.60**（1M 文脈）· V4 Flash $0.09/$0.18 — Standard/Priority（1.5×）ティアが GJC の `service-tier` 設定と直結する。

### 3-4. セレクタ構文

```text
<provider-id>/<model-id>:<effort>            例）anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   （Gemini 高推論 — エンジン公式経路）
opencode-go/<model>                           （effort 省略 = モデル既定）
```

---

## 4. 📊 ベンチマーク根拠

**役割ごとの検証済み首位**（vals.ai 独立ボード · 公式モデルカード — **基準日 2026-07-02**）

| 役割（軸） | 首位 | 数値 |
|---|---|---|
| executor（SWE-bench Verified） | **Fable 5** | **95.0%**（Opus 4.8 88.6 = **サブスク込み最強** · GPT-5.5 82.6 · Gemini 3.1 Pro 80.6） |
| planner（推論 GPQA/ARC-AGI） | **Gemini 3.1 Pro**† | GPQA 94.3 · ARC-AGI-2 77.1（流動推論は GPT-5.5 — [§6-2](#6-2-役割配置の最適性レビューdeep-research--実測) · GPQA 単独首位は Sonnet 5 の 96.2） |
| architect（文脈 · マルチモーダル） | **Gemini 3.1 Pro**† | 1M 文脈 · MMMU-Pro 81% |
| default（ツール呼び出し · 誠実性） | **Opus 4.8 / Fable 5** | ルータ品質 = 全体の上限（Fable は refusal・課金のキャベアット — [§5](#5-️-最終カタログ--10-バンドル--4階層)） |
| critic（独立性） | **クロスファミリー** | メタ審判 > 討論型集計 |

> † **更新脚注**：planner 軸は **GPT-5.6 Sol の 2026-07-09 GA** で世代交代済み（v2 カタログに反映 — 上表の planner/architect 行は 2026-07-02 時点のスナップショット）。architect 軸は Gemini 3.5 Pro（2M 文脈、Deep Think）が 7月 GA に延期 — リリース時にこの表は再検証対象。

**合意原則**

1. **default = Anthropic フラッグシップ（Opus/Fable）固定** — ルータ品質が全体の上限。例外は 2 つ：`ultimate-sol`（Sol ルータ — validator 登載 + WARN 表面化の opt-in 実験）· `eco`（Anthropic 非搭載バンドル — Terra ルータ、不変式は非適用）。
2. **architect = Gemini 3.1 Pro（マルチモーダル）/ Opus（超長文脈）** — Gemini はビジョンと中程度文脈に最適。200k+ のテキスト検索は Opus（MRCR 76%@1M、Gemini は 26% に崩壊）。
3. **critic = クロスファミリー** — メインループ/プランナーと別ベンダーで自己選好バイアスを緩和。
4. **構造 = 強メインループ + シグナル駆動委譲 + 失敗駆動 effort エスカレーション。**
5. **クエリ毎のプロファイル切替 ❌** — キャッシュ損失 > 利得。モード境界でのみ切替。

> ベンチマークは時点依存 → 四半期ごとに再検証推奨。絶対順位は vals.ai 独立ボードに限定。

---

## 5. 🗂️ 最終カタログ — 10 バンドル · 4階層

<div align="center">
<img src="assets/profiles-matrix.svg" alt="プロファイル × 役割 マトリクス" width="100%">
</div>

> ★ = 日常推奨。**v2.0.0 構造転換**：「同等のプロファイル N 個」ではなく **user-facing バンドル 10 個を 4 階層（tier）** に分ける — 信頼等級は同じではない。マルチベンダー不変式：全バンドル `required_providers ≥ 2`（単一ベンダー需要は GJC 0.9.6 内蔵プロファイルの担当）· `critic=cross-family` が基本（例外は validator `SAME_FAMILY_OK` 登載 + WARN 永続表面化）· すべてエンジン effort ハードルールを通過 + **セレクタ検証状態を追跡**（[§6](#6--検証マトリクス)。2026-07-10 gjc **0.9.6** 初回バッテリー — 出荷セレクタ全席グリーン）。

| Tier | バンドル | 一言定義 | こんな時 |
|---|---|---|---|
| Core | ⭐ **daily** | 本体 Opus + 委譲役割別に分散 — **サブスク OAuth 3 ベンダーだけで activation** | **日常の既定** |
| Core | 🏎️ **coding-sprint** | executor を Opus に昇格した実装スループット特化 | 純粋な実装スプリント |
| Core | 🚨 **cyber-cop** | reviewer モード — architect·critic が主役、PRレビュー・セキュリティ監査専用 | 他人の PR レビュー・マージゲート・セキュリティ監査 |
| Premium (exp) | 🏆 **ultimate-opus** | Anthropic 品質基盤のプレミアム（旧 `ultimate` 後継） | 正確性がコストより重要 |
| Premium (exp) | 🧪 **ultimate-sol** | Sol 基盤のプレミアム — agentic/terminal/browser 軸。**Anthropic 搭載バンドル中で唯一の非 Anthropic default**（validator 例外；`eco` は Anthropic 自体が無い） | 長期自律ワークフロー実験 |
| Premium (exp) | 🔥 **dream-team** | 役割別最強仮説 — Fable default+executor（旧 `ultimate-f5`/`legend` 後継） | 最高品質、credits 覚悟 |
| Workflow | 🏛️ **llm-council** | 4 系列の座席表（判定席は Google·xAI·OpenAI の 3 系列 — **本体 Anthropic は集計者制限**）— 投票・quorum は routing-rules の Council 契約が実行 | 多系列合意が必要な決定 |
| Workflow | 🛡️ **escalation** | 手動エスカレーション — Fable 救援投手 + critic 3 票パネル | マージ・セキュリティ・決済・不可逆変更 |
| Specialized (exp) | 💸 **eco** | マルチベンダー低単価実験 — *絶対最安ではない*（最小依存の低価格は内蔵 `codex-eco`） | コスト圧・大量作業 |
| Specialized (exp) | 🗺️ **monorepo** | 全域 ≥1M ctx（gpt-5.5 272K/5.6 373K は除外） | 巨大コードベース |

**v1.11.0 → v2.0.0 マイグレーション**：`ultimate`→`ultimate-opus` · `ultimate-f5`/`legend`→`dream-team` · `solo-anthropic`/`solo-openai`/`claude-codex`/`claude-codex-max` → **削除** — 単一・2ベンダー需要は GJC 0.9.6 内蔵プロファイル（`claude-opus`/`claude-fable`/`codex-*`/`opus-codex`/`fable-opus-codex`）が吸収する（マッピング等価ではなく use-case 吸収）。`llm-council`・`ultimate-sol` を新設。

<details>
<summary><b>📋 完全な YAML を展開（モデルマッピングは gjc-profiles.yml と同一 — コメントは除去済み。注釈付きの韓国語正本は <a href="./gjc-profiles.yml">gjc-profiles.yml</a>）</b></summary>

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

> [!TIP]
> **opencode-go** は `OPENCODE_API_KEY` 設定時に `eco`（executor）・`monorepo`（critic）で有効になる（検証✅）。grok 契約（SuperGrok）の `xai/grok-composer-2.5-fast`（200k）も検証済み — throughput 用の代替。他の opencode-go モデル（qwen3.7-max・kimi-k2.6・glm-5.1・minimax-m2.7・mimo-v2.5）も全て動作確認済み。新規入庫（未検証候補）：**kimi-k2.7-code**（budget executor 有力）· **minimax-m3**（512K マルチモーダル — カタログ実測値、`2026-07-10-catalog-gjc096.txt`）。

#### プロファイル別の設計理由

- **daily** — 本体 Opus `:medium`（効率 knee）、実装はコーディング特化 `gpt-5.6-terra`（$2.5/15 で ≈GPT-5.5 級）、分解は長期ワークフロー 1 位 `gpt-5.6-sol:high`（v2: gemini→sol — Agents' Last Exam 52.7）、設計・レビュー**と批評**は Gemini `-low:high`（v2: critic grok→gemini — **xai キー障壁を消し、サブスク OAuth 3 ベンダーだけで activation**、かつ critic は Anthropic 本体と cross-family を維持；Grok critic に defect-recall の直接根拠は 0 件のため diversity 席は premium 系へ移動）。日常作業の品質/コストの均衡点。
- **coding-sprint** — executor 主役（Opus `:high` — v2 では `:max` 常時ではなく失敗シグナル時だけ昇格、[§8-2](#8-2-適応的-effort-エスカレーション)）、planner は `gpt-5.6-sol:high`、critic は*コードを知る* `gpt-5.6-terra`で実バグを拾う。⚠planner/critic が同じ gpt 系列 — 人間判定（2026-07-10）で `SAME_FAMILY_OK` 登載（Sol≠Terra、バンドル全体は 3 ベンダー）。
- **cyber-cop** — 🚨 **reviewer モード**：author モード（default+executor 重視）の逆相。レビューセッションでは役割の重みが反転し、executor は再現 PoC・failing test の脇役、**architect（一次コードレビュー判定者）と critic（マージゲート）が主役**になる。architect=Opus `:high`（1M 実効検索 76% vs Gemini 26% 崩壊）、critic=`gpt-5.6-sol:high`（Claude 作成コードと cross-family）。高リスク PR・セキュリティ監査は critic 3 票パネル（§9 規則 — 独立投票、討論禁止、2/3 反対または CRITICAL/BLOCK 1 件なら遮断）。運用規則は [`routing-rules.md`](./routing-rules.md) の reviewer 契約を参照。
- **ultimate-opus** — 🏆 Anthropic 品質基盤プレミアム（旧 `ultimate` 後継）。default·executor·architect を Opus `:high` で統一し、安定性・1M・サブスク限界費用を取る。交差検証は **Sol planner `:xhigh` + Grok critic `:high`** が担当。⚠executor/architect 同一 claude 系列 — 人間判定 `SAME_FAMILY_OK`（WARN 永続表面化）。Opus 3 席は「3つの独立意見」ではない — council 品質を示唆しないこと。
- **ultimate-sol** — 🧪 Sol 基盤プレミアム（experimental）。Sol が優位な軸 — 長期ワークフロー完走（Agents' Last Exam 52.7）・terminal（T-B 2.1 88.8 SOTA）・browsing（BrowseComp 90.4）・computer use（OSWorld 62.6）— に default/executor/planner 3 席を寄せる。**Anthropic 搭載バンドル中で唯一の非 Anthropic default**（validator `NON_ANTHROPIC_DEFAULT_OK` 登載 — WARN 表面化；Anthropic 非搭載 `eco` の Terra ルータは不変式自体が非適用）。トレードオフ：ルータ ctx **373K**（Opus 1M 比）・Toolathlon 58 vs Fable 61.7・⚠METR の SWE ゲーミング指摘。OpenAI 3 席の自己強化は Opus architect + Grok critic が緩衝する。role-fit L3 前までは experimental。
- **dream-team** — 🔥 役割別最強*仮説*（旧 `ultimate-f5`/`legend` 後継）。**Fable 5 = default+executor**（SWE-Bench Pro 80.0 — OpenAI 自社表の自己不利承認 · FrontierMath T4 87.8）、分解は Sol `:xhigh`、設計レビューは Opus `:high`（1M）、批評は第三系列 Grok。Fable のキャベアット 3 点：①サブスク込みイベント ~7/12 23:59 PT（以後 **usage credits $10/$50** — default+executor 2 席で露出最大）②refusal が HTTP 200+`stop_reason:refusal` で来る ③30-day retention・ZDR 不可。⚠executor(Fable)/architect(Opus) 同一 claude 系列 — 人間判定 `SAME_FAMILY_OK`。
- **llm-council** — 🏛 4 系列の座席表（Anthropic·OpenAI·Google·xAI）。**判定席は Google（Gemini）・xAI（Grok）・OpenAI（Sol/Terra）の 3 系列で、本体 Anthropic（Opus）は集計者制限** — 自己選好バイアス隔離のため本体は判定に参加せず、raw verdict の保存・開示のみ行う（4 系列の「合意」ではなく「3 系列判定 + 第 4 系列集計」）。**プロファイルを有効化するだけでは council は始まらない** — 並列独立呼び出し・相互非公開・raw verdict 保存・quorum（CRITICAL/HIGH dissent は多数決で棄却不可）は [`routing-rules.md`](./routing-rules.md) の **Council 契約**を本体が実行して初めて発生する。ベンダー数 ≠ 独立票数 — 算術で確信を膨らませない。
- **escalation** — 🛡 **手動**エスカレーション（失敗自動検知ではない — トリガー・再試行予算・human gate は routing-rules の Escalation 契約）。失敗シグナルが出た作業に**最強実行者 Fable 5 `:xhigh`を救援投手として投入**。間欠使用なので credits 課金とも相性が良い。critic はマルチベンダー 3 票パネル（[§9](#9--並列エージェント--信頼性)）。Fable refusal 時は executor を Opus `:max` に降格し、人間に報告。不可逆変更専用。
- **eco** — 💸 マルチベンダー低単価*実験* — **絶対最安ではない**（最小依存の低価格経路は GJC 0.9.6 内蔵 `codex-eco`）。v2 で全面再編：default `gpt-5.6-terra:medium`、executor 最安 `deepseek-v4-flash`（$0.14/0.28）、planner `gpt-5.6-luna:medium`（v2: `grok-4-1-fast` は **2026-05-15 retire — legacy slug は grok-4.3 料金へ redirect 課金**のため退場）、architect は Gemini `-low:high` リテラルピン、critic は `gemini-3-flash:low`（v2: `gemini-3.5-flash-low` が 07-10 午後ライブで消滅 — [§6](#6--検証マトリクス)）。xai・anthropic キー不要（3 ベンダー）。
- **monorepo** — 🗺 全役割が 1M ctx。`gpt-5.5`（272K）・`gpt-5.6 3種`（373K）は除外 — gpt-5.4 は 1M だが Opus が同等以上。architect=**Opus**（1M 実効検索 1 位 **76%@1M** — Gemini は 26% に崩壊）、critic=**`glm-5.2`**（cross-family、代替 `deepseek-v4-pro`）。**1M nominal window ≠ 完全 recall** — 巨大入力は一発で貼らず**チャンクに分けてマルチターン累積**（[§6-3](#6-3-残余ギャップ検討gap-13--gjc-実効コンテキスト実測)）— 単一メッセージ >~400k paste だけ `opencode-go/deepseek-v4-pro`へ。

**削除されたプロファイルの行き先** — `solo-anthropic`/`solo-openai`（単一ベンダー）と `claude-codex`/`claude-codex-max`（2ベンダー固定ミックス）は、v2 のマルチベンダーカタログ原則（混合サブスクのコラボレーション — 人間判定 2026-07-10）により退場。GJC 0.9.6 内蔵プロファイルが該当 use-case を吸収する：単一 Anthropic → 内蔵 `claude-opus`/`claude-fable`、単一 Codex → 内蔵 `codex-eco`/`codex-medium`/`codex-pro`、Claude+Codex 2ベンダー → 内蔵 `opus-codex`/`fable-opus-codex`（0.9.6 で GPT-5.6 系に更新済み）。内蔵マッピングは本ガイド旧版と byte-identical ではない — 席の詳細が重要なら旧版 YAML（`git show v1.11.0:gjc-profiles.yml`）をローカルカスタムで維持する。

---

## 6. ✅ 検証マトリクス

> 2026-07-10（gjc **0.9.6** — 当日 0.9.5→0.9.6 アップグレード後の再バッテリー）に全プロバイダの核心セレクタを `gjc -p --no-session --no-tools --model <sel> "..."` で**実呼び出し**して再検証した（`evidence/2026-07-10-selectors-rerun-3.md`；0.9.5 グリーン記録は rerun-2）— **v2 出荷セレクタ全席グリーン**。このバッテリーで antigravity ライブ面の当日ドリフト（下の WARNING）を捕捉し、eco.critic を差し替えた。「動く」は推測ではなく実呼び出しに基づく。

| プロバイダ | 検証済みセレクタ（✅ 動作） |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh`（**07-10 rerun✅** — `:max` は xhigh へサイレントクランプ）· `claude-sonnet-5:high`（07-10✅ — `:max` は high へサイレントクランプ）· `claude-opus-4-8:high`（07-10✅；low·medium·max 07-02✅）· `claude-sonnet-4-6:high`（07-10✅）— 07-09 の rate-limit 解除、全席再検証完了 |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh`（**07-10✅**）· `gpt-5.6-terra:high`/`:xhigh`（07-10✅）· `gpt-5.6-luna:high`（07-10✅）· 3種 `:max` は受理されるが深度未検証（未出荷）· `gpt-5.5:high`（07-02✅、v1.11 でプロファイルから退役—カナリア維持）· `gpt-5.4:high`（1M ctx レーン） |
| `xai` | `grok-4.5:medium`/`:high`（07-10✅ — `:xhigh`/`:max` は high へサイレントクランプ；xai 専用、provider 500K/GJC 222K floor、$2/$6）· `grok-4-fast:high`（07-10✅）· ⚠`grok-4-1-fast:high` は呼び出し自体は成功するが **xAI が 2026-05-15 retire — grok-4.3 料金へ redirect 課金**（v2 で退場）· `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3`（**bare セレクタのみ** — effort サフィックス非解釈、07-02✅。SuperGrok OAuth） |
| `google-antigravity` | `gemini-3.1-pro-low`（±`:high`、07-10✅）· `gemini-3-flash`（±`:low`、**07-10✅ — v2 eco.critic**）· ⚠0.9.6 からファジー空間は **fail-closed**：`gemini-3.1-pro-high`/`-bogus` は `not found`（0.9.5 のサイレント `-low` 解釈罠は再現せず — ピンは維持）· ⚠**ライブ面の当日ドリフト**：`gemini-3.5-flash-low`/`-extra-low`/`gemini-pro-agent` は 07-10 午後に消滅（`not found` — `--list-models` 表記と不一致、実呼び出しが真実） |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro`（07-02 再検証✅）· `glm-5.2`（**0.7.10 バンドル入り**、07-02✅）· `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5`（`OPENCODE_API_KEY` 必要） |

> [!WARNING]
> **本環境で動かなかったセレクタ**（回避）：`openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`（ChatGPT アカウント非対応）· `google-antigravity/gemini-3.1-pro-high`·`gemini-3.5-flash-low`·`gemini-3.5-flash`·`gemini-pro-agent`（**0.9.6/07-10 午後基準 `not found`** — 高推論は `gemini-3.1-pro-low:high`、軽量 Gemini は `gemini-3-flash:low`）· `gemini-3-pro`（廃止）· `claude-sonnet-4-6-thinking`（404）· `gpt-oss-120b`（500）。`opencode-go/*` は **`OPENCODE_API_KEY` 未設定時のみ**失敗（設定後は上表どおり動作）。参考：`fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.5:xhigh/max` は失敗ではなく**サイレントクランプ**（[§3-2](#3-2-effort-チートシート)）— gpt-5.6 3種は `:max` を受理するが深度未検証（未出荷）。

> [!NOTE]
> `opencode-go/glm-5.2` は **0.7.10 からバンドルカタログ入り**した（旧「ライブカタログ専用」のキャベアットは廃止）。antigravity のライブ面は当日中にも変わる（07-10 午後 `gemini-3.5-flash*` 消滅実測）— `--list-models` はキャッシュされた表記を見せることがあるため、**席に採用する前に実呼び出しで確認**する。ディスカバリ未更新の状態では `selector did not resolve` で有効化に失敗しうる — 再ログイン/リトライでカタログを更新するか、バンドル id に置換する（eco critic 代替：`opencode-go/deepseek-v4-pro`、GLM は `zai/glm-5.2` — `zai` を `required_providers` に追加）。

**レイテンシ参考**（マイクロベンチ 2026-07-02；Grok 4.5 行のみ 2026-07-09 streaming bench）：

| セレクタ | コーディング | 推論 | 備考 |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **全体最速** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | コーディングで sonnet-5 比 +3~4s |
| `grok-4.5:medium` / `:high` | ~14s / ~50s | TTFT ~13s / ~48s | 2026-07-09 streaming bench；high は高リスク critic 専用 |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | コーディング遅延の外れ値 |
| `glm-5.2` | **21.9s** | 4.0s | コーディング最遅 — critic には支障なし |

再現：
```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
```

---

### 6-2. 役割配置の最適性レビュー（deep-research + 実測）

初期 8 プロファイル（v1.0 基準）の役割→モデル配置を多回 deep-research（独立ベンチ検証）とライブ推論プローブで再点検した結果、骨格は near-optimal と確認された。**v2.0.0 はここに 2 軸ブラインド独立ディープリサーチ（Claude Fable 5 Ultracode + Parallel.ai Ultra 2x、2026-07-10）を追加**し、10-bundle 4階層構造に再編した — 2 軸の共通結論：発売状態・役割軸配置は支持（SUPPORT）、profile/workflow 境界・tier ラベル・strict provider 摩擦は修正（REVISE）。Premium 3種の role-fit L3 実測は残課題（experimental ラベルの理由）。

- **`gemini-3.1-pro-low:high` は劣化モードではない。** `thinkingLevel` は別モデル変種ではなく同じ Gemini 3.1 Pro にかかる per-request パラメータで、モデル既定値は **HIGH**。公式モデルカードのヘッドライン推論点（GPQA 94.3 · ARC-AGI-2 77.1）は全て *Thinking (High)* で測定された — このセレクタは**ネイティブ高推論の既定モード**を呼ぶ。実測プローブ：`low`（18s）→ `low:high`（22s）で遅延増、thinking 有効を確認。
- **planner 推論軸は分裂する。** GPQA Diamond（科学知識）は上位が 93〜96% で飽和 — 単独首位は **Sonnet 5（96.2）**、Gemini 3.1 Pro 94.3。ARC-AGI-2（抽象・流動推論）は **GPT-5.5 が明確に上**（0.850 vs 0.771、Fable 5 は未公開）。プランニングに直結する流動推論（ARC）基準 → planner は GPT 系を維持。**科学知識推論比重が大きければ `planner → google-antigravity/gemini-3.1-pro-low:high` へ swap。**（更新 2026-07-10：GPT-5.6 Sol GA — 公式評価で全面優位 + 同価 $5/$30 → v1.11 で planner を `gpt-5.6-sol:xhigh` に世代交代。）
- **executor 軸は v1.4 で交代した。** **Fable 5 が SWE-bench Verified 95.0 / SWE-Bench Pro 80.0 で新 1 位**（Opus 4.8 88.6 · GPT-5.5 82.6；Pro 80.3 は別列の Mythos 5 — [errata E1](./evidence/2026-07-10-errata.md)）。Opus 4.8 は「サブスク込みコーディング最強」として維持 — Fable 5 は 7/12 以後 usage credits 課金なので常時 executor とは費用構造が異なる（`dream-team`/`escalation` のみ採用）。terminal・agentic 軸は **GPT-5.6 Sol が SOTA**（Terminal-Bench 2.1 88.8）— ただし ⚠METR が Sol の SWE 評価ゲーミング（過去最高比率）を指摘しており、SWE 系点数は割り引いて読むこと。daily executor は同価後継 `gpt-5.6-terra`。
- **xAI `grok-composer-2.5-fast`・`grok-code-fast-1` は eco/throughput 専用。** 独立ベンチ非公開/インフレのためフロンティア coder ではなく、core executor に含めない判断が正しい。
- **default = Anthropic フラッグシップ。** Opus 4.8 は Vals Index 総合（提供中モデル 1 位）で再確認。Fable 5 default（`dream-team`）は品質上限を一段上げるが、refusal 分類器・credits 課金キャベアットを伴う（[§5](#プロファイル別の設計理由)）。`ultimate-sol` の Sol ルータは opt-in 実験（WARN 表面化）。
- **architect 長文脈の訂正**：Gemini の名目 1M は実効 1M ではない — MRCR v2 8-needle 128K 84.9% → 1M **26.3%** 崩壊、一方 **Opus 4.6 は 1M 76% 維持**（4.8 数値は未公開）。Grok 4.3 multimodal は 12/16 の下位なので vision architect には不適。→ **monorepo architect を Grok→Opus に修正**。標準プロファイル architect=Gemini はマルチモーダル・中程度 ctx 限定で最適。

> 出典： [vals.ai GPQA](https://www.vals.ai/benchmarks/gpqa) · [vals.ai SWE-bench](https://www.vals.ai/benchmarks/swebench) · [vals.ai MMMU](https://www.vals.ai/benchmarks/mmmu) · [Gemini 3.1 Pro card (MRCR)](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini thinking docs](https://ai.google.dev/gemini-api/docs/thinking) · [Opus 4.6 (MRCR 76%@1M)](https://www.anthropic.com/news/claude-opus-4-6) · [long-context ボード](https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/) · [llm-stats ARC-AGI-2](https://llm-stats.com/benchmarks/arc-agi-v2) · [xAI Composer 2.5](https://x.ai/news/composer-2-5)

> 📑 **完全リサーチレポート（一次出典引用込み）** — この配置根拠の原文 3 本： [ディープリサーチベンチマーク](./evidence/2026-07-03-deep-research-benchmarks.md) · [コンサルタントレポート](./evidence/2026-07-03-consultant-report.md) · [統合最終レポート](./evidence/2026-07-03-ultimate-final-report.md)。発行レポートは verbatim 保存され、訂正は **[errata](./evidence/2026-07-03-errata.md)** で配送される。

---

### 6-3. 残余ギャップ検討（gap 1〜3 · GJC 実効コンテキスト実測）

Opus 4.8 は GJC で **1M コンテキストウィンドウを正常サポート**する（マルチターン累積 — 状態バー `◫ %/1M` を確認）。下表はそれとは**別に**、巨大コンテキストを**単一メッセージ（`@ファイル`）で一発注入**するときの入力サイズ上限実測（3-needle マルチホップ検索基準）— ウィンドウ上限ではない：

| トークン（単一リクエスト） | Opus 4.8 | Gemini 3.1 Pro | Grok 4.3 / 4-fast | DeepSeek V4 Pro |
|---|:---:|:---:|:---:|:---:|
| ~130k · 250k · 350k | ✅ | ✅ | ✅ | ✅ |
| ~476k | 🔴 400 | 🔴 400 | ✅ (89s) | ✅ (36s) |
| ~857k | 🔴 | 🔴 | 🔴 400 | — |

- **gap1 — Grok 2M architect swap：❌ 棄却。** 独立ベンチ（Context Arena MRCR v2）で Grok は deep-bin 検索が**最下位**、2M bin はどのボードにも無く、grok-4-fast の 2M は測定済み検索点が 0。実測も 857k で 400。→ 「1M 超は grok-4-fast（2M）」仮定を破棄。
- **gap2 — Opus 4.8 長文脈：** Opus 4.8 は **GJC で 1M コンテキストウィンドウをサポート**する（マルチターン agentic ファイル読みで 1M まで正常累積）。上表の ~400k 400 は**ウィンドウ上限ではなく単一メッセージ（`@ファイル`）入力サイズ上限**。→ monorepo architect=**Opus 維持**。ただし**一つのメッセージに >~400k トークンを丸ごと paste**する稀な場合だけ `opencode-go/deepseek-v4-pro`へ。
- **gap3 — GLM-5.2 vs DeepSeek：** eco executor=**DeepSeek V4 Flash 維持**（GLM-5.2 $1.40/$4.40 = 入力 10×・出力 15×で eco には重い）。**monorepo critic は `opencode-go/glm-5.2` へアップグレード**（実呼び出し検証✅）— 新 open-weight 1 位（AA Index 51、DeepSeek V4 Pro は 52→**44 下落**）、cross-family 独立性を維持。

> 核心：Opus 4.8 のコンテキストウィンドウは GJC で **1M 正常**（マルチターン累積）。単一メッセージで一発注入できる量だけが ~400k（Opus/Gemini）— それ以上の**単一 paste**は Grok/DeepSeek が堅い（実測）。**巨大入力は一発で流し込まず、チャンクに分けて累積すれば 1M ウィンドウをそのまま活用**できる。出典： [Context Arena](https://contextarena.ai/) · [GLM-5.2 (AA)](https://artificialanalysis.ai/models/glm-5-2) · [Opus 4.8 what's-new](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)

---

## 7. 🛠️ インストール / アンインストール

### ワンクリック（推奨）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

インストーラの動作：`~/.gjc/agent/models.yml` に 10 個のバンドルを安全マージ（再実行で自動更新 — v1.x 管理ブロックの旧プロファイルは置換される）· 既存ファイルを自動バックアップ · 既定プロファイルを `daily` に設定。`curl` + `python3` だけで動く。

```bash
# オプション
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash  # 既定プロファイル指定
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash        # 既定設定をスキップ
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash    # agent ディレクトリ上書き
```

### プロバイダ認証（必須）

インストールはプロファイルを置くだけ。GJC を起動し各ベンダーに一度ログイン：

```text
/login anthropic           # claude
/login openai-codex        # gpt（base GPT）
/login google-antigravity  # gemini（Google AI Pro/Ultra サブスク）
/login xai                 # grok 全ラインナップ + Composer
```

opencode-go は `/provider add` または環境変数 `OPENCODE_API_KEY`。

### 手動インストール / 検証 / アンインストール

[`gjc-profiles.yml`](./gjc-profiles.yml) の `profiles:` ブロックを `~/.gjc/agent/models.yml` の `profiles:` 配下に貼り付け、`gjc --mpreset daily --default`。

```bash
gjc --list-models daily                       # 確認
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # 巻き戻し(バックアップ復元)
```

> [!WARNING]
> **GJC 0.7.10 のプリセット rename/delete に注意**：エンジンのカスタムプリセット rename/delete 機能は `models.yml` の**コメントを全て除去**する — インストーラの管理ブロックのセンチネル（コメント）も一緒に消えて名前ベースの置換に格下げされ、**ユーザーが削除したプロファイルが再インストール時に復活**しうる（再現確認済み）。rename/delete を使った後に再インストールする際は結果を必ず確認すること。完全な除去はバックアップ復元（`cp … .bak-*`）が最も確実。

---

## 8. 🔀 動的ルーティング

> **「クエリ毎にプロファイル切替」❌ /「強メインループ1つ + 薄いルール1層」✅。** ルータはメインループ（Anthropic フラッグシップ）、プロファイルは行き先プール。

> [!TIP]
> 下のルーティングルールをメインループに従わせるには、[`routing-rules.md`](./routing-rules.md)（韓国語 — セレクタ/プロファイル名は言語非依存）をプロジェクトの `AGENTS.md` に入れるか、`gjc --append-system-prompt @routing-rules.md` で注入する（導入プロファイル + 検証済みセレクタのハードルール + GJC 実効 ctx 上限を1ファイルに同梱）。

### 8-1. 作業シグナル → 委譲

<div align="center">
<img src="assets/routing-tree.svg" alt="作業シグナル → 委譲ルーティング" width="100%">
</div>

ルール：**委譲はシグナルが明確なときだけ。** メインループが直接できるなら直接やる。

### 8-2. 適応的 effort エスカレーション

<div align="center">
<img src="assets/effort-ladder.svg" alt="適応的 effort エスカレーション" width="100%">
</div>

- ✅ 解けなかったから上げるのは正当 / ❌「念のため上げる」は無駄。
- minimal 禁止。下限は `low`。Gemini は `low↔high` の単一ジャンプ。

### 8-3. プロファイル切替（モード境界のみ）

| シグナル | 切替 → |
|---|---|
| セッション開始 · 一般作業 | `daily` |
| 純粋な実装スプリント | `coding-sprint` |
| マージ/リリース前 · セキュリティ · 決済 | `escalation`（手動トリガー — routing-rules の Escalation 契約） |
| PR レビュー · セキュリティ監査セッション | `cyber-cop` |
| 多系列合意が必要な決定 | `llm-council`（+ routing-rules の Council 契約） |
| 精度最優先（opt-in premium） | `ultimate-opus` / `ultimate-sol`（Sol 軸実験） / `dream-team`（Fable・credits 覚悟） |
| 大量リファクタ · マイグレーション | `eco` |
| 巨大コードベースへ突入 | `monorepo` |
| 単一ベンダーのみで運用 | GJC 内蔵プロファイル（`claude-opus`·`codex-*` など — このカタログ外） |

---

## 9. 🧪 並列エージェント + 信頼性

直列の引き継ぎは `0.99ⁿ` で減衰し、マルチエージェントは繋ぎ方を誤ると「偽の合意」に固まる。並列設計はこの2つを防ぐように組む。

```text
直列チェーン 5段(各 0.99)：  0.99^5 ≈ 95.1%    → 長いほど崩壊
並列独立 5個(OR 成功)：      1-(0.01)^5 ≈ 100%  → 多様性が信頼性を高める
```

**設計原則**
- critic は**メインループと別ベンダー、並列で独立投票しメインループが集計**（討論禁止 — メタ審判が優位）。
- critic パネル例：`{openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high, google-antigravity/gemini-3.1-pro-low:high}` を同時実行 → 2/3 反対または CRITICAL/BLOCK 1 件なら遮断。**CRITICAL/HIGH dissent は多数決で棄却不可** — 解消または human gate。
- executor の fan-out は**作業が真に独立**（共有状態なし）なときだけ。
- チェーンは短く、メインループを単一の真実源に（サブ同士で直接合意させない）。

---

## 10. 💰 コスト

Gemini（`google-antigravity`）は **無料公開プレビュー + Google AI Pro/Ultra 契約時の上限引き上げ**で動く（per-token 請求ではない — [Antigravity plans 公式ドキュメント](https://antigravity.google/docs/plans)、2026-07-10 確認）。**Fable 5 は 2026-07-12 23:59 PT まで Claude サブスク（Pro/Max/Team）に含まれる**（7/7→7/12 延長 — 公式一次延長ページは未確保、複数二次報道基準）が、週次使用上限の 50% までという制限があり、**以後は usage credits の別課金**になる — 「無料」ではない。他は従量課金で、主要モデル単価は以下（$/1M、入力/出力）：

| モデル | $/1M (in/out) | 役割 |
|---|---|---|
| Claude Fable 5 | 10 / 50（バッチ 5/25 · キャッシュヒット 1）† | dream-team default·executor · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor の基幹 |
| Claude Sonnet 5 | 3 / 15（イントロ 2/10 ~2026-08-31）‡ | eco executor 代替 |
| GPT-5.6 Sol | 5 / 30（Fast モードは 12.5/75） | planner（daily·sprint·ultimate-opus·dream-team·council·escalation）· ultimate-sol 3 席 · cyber-cop executor·critic |
| GPT-5.6 Terra | 2.5 / 15 | daily executor · coding-sprint critic · llm-council executor · eco default |
| GPT-5.6 Luna | 1 / 6 | eco planner（v2 新規採用） |
| Grok 4.5 | 2 / 6（実効入力約 $0.84 @88% cache） | critic（premium 3種·llm-council·escalation）— xai API キー |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 単一 paste フォールバック |
| Gemini 3.1 Pro / 3-flash | プレビュー/サブスクトークン | planner·architect·critic |

> † Fable 5 は Opus のちょうど2倍の単価。サブスク込み分（~7/12）も週次上限を消費する。
> ‡ Sonnet 5 は**トークナイザ変更で同一テキストが約 30% 多くトークン化**される — 実効コストは表示単価より高く見積もること。
> （参考：DeepSeek 系は DeepInfra プロバイダ経由なら V4 Pro $1.30/$2.60 — [§3-3](#3-3-契約--プロバイダ)。）

**プロファイル相対コスト**

| プロファイル | コスト | 主因 |
|---|---|---|
| dream-team | ●●●●● | default·executor Fable 5 — ~7/12 サブスク込み（週次上限 50%）、以後 credits $10/50 |
| escalation | ●●●●● | executor Fable `:xhigh`（救援投手 — 間欠使用）+ planner Sol `:xhigh` + 4 ベンダー認証 |
| ultimate-opus / ultimate-sol | ●●●●○ | Opus または Sol 3 席 `:high~xhigh` + Grok critic（xai API） |
| llm-council | ●●●●○ | 4 ベンダー認証 + Sol `:xhigh` planner — council ワークフロー実行時は票数分課金 |
| coding-sprint | ●●●○○ | executor Opus `:high`（失敗シグナル時のみ max 昇格） |
| daily | ●●●○○ | 本体 Opus `:medium`、委譲は中・低価格へ分散 — サブスク OAuth 3 ベンダー |
| monorepo | ●●●○○ | executor/architect Opus + Gemini（プレビュー/サブスク）+ GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash（$0.14）+ Luna（$1）+ Gemini プレビュー — ただし*絶対最安は内蔵 `codex-eco`* |

> **3つの節約レバー**：① 委譲作業を超安価モデル（DeepSeek V4 Flash $0.14、Luna $1）・プレビュー/サブスクトークン（Gemini）へ ② 失敗時のみ effort を上げる ③ メインループ（Anthropic フラッグシップ）は品質の上限なので維持しつつ、日常は `:medium` — Fable default（`dream-team`）の credits が負担なら default を `opus-4-8:high` へ（≈`ultimate-opus` 構造）。

---

## 11. 📖 出典

**コーディング（executor）** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1)

**Claude 5 ファミリー** · [Fable 5 再デプロイ告知](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com モデルドキュメント](https://platform.claude.com/docs) — 価格・サブスク込み（~7/12 延長、[Android Authority 報道](https://www.androidauthority.com/claude-fable-5-free-extension-3685103/)）・effort 仕様を 2026-07-02/07-10 に相互確認

**GPT-5.6 (2026-07-09 GA)** · [リリース発表](https://openai.com/index/gpt-5-6/) · [Sol プレビュー(Cerebras 750TPS)](https://openai.com/index/previewing-gpt-5-6-sol/) · [AA: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) · [TechTimes(METR 評価ゲーミング)](https://www.techtimes.com/articles/319808/20260707/gpt-56-sol-review-faster-coding-half-fable-5-cost-benchmark-problem.htm) — 価格・評価を 2026-07-10 に相互確認

**推論（planner）** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**文脈 · マルチモーダル（architect）** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**ツール呼び出し · 誠実性（default）** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**独立性 · ルーティング（critic + 設計）** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [自己選好は能力とともに強まる](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**公式モデル/価格** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**ワンライナーで導入、役割ごとに最適モデル。**

**v2.0.0** · [CHANGELOG](./CHANGELOG.md) · [保守プレイブック](./MAINTAINING.md) · ライセンス [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
