<div align="center">

# 🧩 GJC マルチベンダー究極セットアップ

### claude · gpt · grok · gemini · opencode go — 5つの契約を*役割ごと*に振り分ける検証済み構成

モデル選びで悩むのをやめよう。**ワンライナーでインストール**し、各役割に最適なモデルを自動で割り当てる。

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-1.10.0-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/profiles-13-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-grok%2Fopenai%2Fgemini%2Fopencode%202026--07--09-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="legend 構成 — 役割ごとの最強モデル" width="100%">

</div>

**[한국어](./README.md) · [English](./README.en.md) · [中文](./README.zh.md) · 日本語（このページ）**

> [!NOTE]
> **本ガイドの中核は GJC 公式ドキュメントに採用された** — 圧縮版が上流に [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md) としてマージ済み（[PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860)、`dev`）。役割/セレクタの概念は **GJC 公式ドキュメントを正式リファレンス**とし、本リポジトリはそこに無いもの — **ワンライナー・インストーラ**、**13プロファイル一式**（`solo-*` / `claude-codex*` / `legend` / `cyber-cop` 含む）、そして[保守・検証ツール](./MAINTAINING.md)（静的チェック CI + ライブセレクタ検証 + カタログドリフト追跡）— を提供する。

## 🚨 NEW · `cyber-cop` — 初の reviewer モードプロファイル

> これまでの 12 プロファイルはすべてコードを**書く(author)**セッション用だった。**`cyber-cop` は 13 番目のプロファイル —— GJC 初の reviewer モード**で、コードを**止める**セッション用だ：他人の PR をレビューし、却下の根拠を探し、マージゲートで判定する。

**何が違うか**
- PR レビュー·セキュリティ監査では役割の重みが**反転** → **architect(一次判定：CLEAR/WATCH/BLOCK)と critic(マージゲート)が主役**、executor は再現 PoC·failing test の脇役に下がる。
- critic が**コード作成者(Claude 想定)に対して cross-family**(GPT-5.5) → 自己選好バイアスを構造的に抑制([arXiv 2410.21819](https://arxiv.org/abs/2410.21819))。
- 高リスク PR·セキュリティ監査は**3 票並列パネル**(`gpt-5.5` · `grok-4.5` · `gemini-3.1-pro`)を招集し、独立投票 → 2/3 反対または CRITICAL/BLOCK 1 件で遮断。

**実証済み —— 本リポジトリが自己検証した**
> PR #4〜#7 でレビューゲートがマージ前に**欠陥 10 件を遮断**した（#4：5 · #6：5 · #7：初回投票で通過）。レビュー補助スクリプトは*自身の* prompt-injection 欠陥で BLOCK され(修正後に通過)、本体(Anthropic)が自家系統の文書を甘く通した 2 点(相対パス注入面·権限の過大表示)を**cross-family critic(GPT-5.5)が正確に BLOCK**。（さらに 1 件が #6 マージ**後**に検出 → #7 で即修正。）自己選好バイアス防御が実戦で機能することを証明した。

**クローン不要、2 コマンドで開始（v1.6+）**
```bash
# 前提：gh CLI インストール·認証済み（gh auth login）+ gjc プロバイダ /login 完了
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_COP=1 bash
export PATH="$HOME/.local/bin:$PATH"   # インストーラが PATH 警告を出した場合は一度実行
cd <レビュー対象リポジトリ>
gjc-cop 123               # PR #123 → 4 セクション判定（REPO は cwd から自動検出 —— マージは絶対しない）
# gjc-cop --panel 123     # 高リスク：3 票 cross-family パネル
# gjc-cop shell           # 対話型レビューアセッション（信頼契約を自動注入）
# gjc-cop watch           # 新規 PR をポーリング·レビュー（マージは人間が決定）
```
クローン/手動パス（同じ仕組み、ラッパーなし）は[アナウンス文書 §3](./docs/whats-new-cyber-cop.md)を参照。

📖 ギャップ論証·3 段階の使い方·自動レビューパイプライン·セキュリティ規則の全体 → **[cyber-cop アナウンス文書](./docs/whats-new-cyber-cop.md)**（韓国語正本）

---

## ⚡ 30秒インストール（ワンライナーをコピペ）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

この1行で **13個のプロファイルを `~/.gjc/agent/models.yml` に安全にマージ**し、既定プロファイルを `daily` に設定する。既存設定は自動バックアップされ、再実行してもクリーンに更新される。

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
> 既定プロファイル指定：`curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash` · 既定設定をスキップ：`GJC_SETUP_DEFAULT=none`。

---

## 1. 🎯 なぜマルチベンダーか

claude·gpt·grok·gemini·opencode go を契約しておきながら1モデルしか使わないのは、すべての役割で*次善*モデルを使うのと同じ。検証済みベンチマークは**役割ごとに首位ベンダーが異なる**ことを示す：

| 役割 | 何をするか | 最適モデル |
|---|---|---|
| 🧠 **推論・設計**（planner） | 手順・受け入れ基準 | **Gemini 3.1 Pro**（GPQA 94.3 / ARC-AGI-2 77.1）† |
| 🔨 **実装**（executor） | 実際のコード作成・修正 | **Claude Fable 5**（SWE-bench Verified **95.0**）— サブスク込みの最強は **Opus 4.8**（88.6） |
| 🔭 **コードレビュー**（architect） | 大規模リポ探索・アーキ | **Gemini 3.1 Pro**（マルチモーダル MMMU-Pro 81%）† · 超長文脈（>200k）→ **Opus** |
| ⚖️ **独立批評**（critic） | 敵対的検証 | **クロスファミリー**（メインループと別ベンダー） |
| 🎛️ **オーケストレーション**（default） | ツール呼び出し・ルーティング・誠実性 | **Anthropic フラッグシップ** — Opus 4.8（ルータ品質 = 全体の上限；`legend`/`ultimate-f5` は Fable 5） |

> **ベンチマーク基準日：2026-07-02**（Claude 5 ファミリーのリリース直後に再検証）。† 推論・architect 軸は「後継が目前」— GPT-5.6 Sol がパートナー限定プレビュー中（6/26、`max` effort + `ultra` サブエージェントモード、GA まで数週間）、Gemini 3.5 Pro（2M 文脈、Deep Think）は 7月 GA に延期。リリース時に再検証予定。

> 1ベンダーで5役割を埋めると、必ずどこかが最強でなくなる。本ガイドはその5枠を各々の最適ベンダーで埋め、コスト・アクセス性・信頼性まで勘案して**実際に動く**組み合わせにまとめた。3本の独立ディープリサーチ（GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro）を相互検証し、セレクタ検証状態を[§6](#6--検証マトリクス)に明記している。

---

## 2. 🧭 コア設計

> **強いメインループを1つ固定（default = Anthropic フラッグシップ Opus/Fable）+ シグナル駆動の委譲 + 失敗駆動の effort エスカレーション。**

毎ターン実際に走るのは `default`（メインループ）だけ。executor/architect/planner/critic は、メインループが**必要なときだけ `task` で委譲**するサブエージェント（新規コンテキスト）。

<div align="center">
<img src="assets/architecture.svg" alt="1メインループ(default) + 4サブエージェント — シグナル駆動委譲" width="100%">
</div>

3つの設計原則：

- **メインループは絶対に譲らない。** 中央値のタスクはほぼメインループが単独処理するため、`default` を弱モデルに落とすと体感品質が全面崩壊する。常に Anthropic フラッグシップ（Opus 4.8 — `legend`/`ultimate-f5` では Fable 5）。
- **多様性は「検証」でのみ効く。** 独立性のため `critic` は別ベンダーに。ただし直列チェーンは短く（信頼性は `0.99ⁿ` で減衰）。
- **effort は非対称な経済学。** `medium→high` は +1〜2点のためにトークン約23倍。無条件 max は無駄 — 「解けなかったとき」だけ上げる。

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

**GJC 0.9.1 の実効値**である — API 公式仕様と異なる箇所がある（下の脚注）：

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← 全6段
Fable 5                 minimal low medium high xhigh       ← :max は xhigh へサイレントクランプ · thinking 常時オン
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max は high へサイレントクランプ
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 は既定 xhigh
Grok 4.5（xai）          low medium high                      ← :xhigh/:max は high へサイレントクランプ · minimal はネイティブ effort ではない
grok-build/grok-4.3     ── bare セレクタのみ（effort サフィックス非解釈）──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go その他       ── effort サフィックス省略（既定）──
google-antigravity Gemini  gemini-3.1-pro-low:high（高推論）· gemini-3.1-pro-low（低 effort）
```

> [!IMPORTANT]
> **5つのハードルール**：① Gemini Pro は `low`/`high` のみ ② openai-codex の文脈は**モデル別** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K**（400K→272K に縮小；旧「codex 272k」一括ルールは廃止）③ Sonnet（4.6/5）は GJC で `xhigh`/`max` 不可 · **Fable 5 は `max` 不可**（それぞれ high/xhigh にクランプ）④ opencode-go は `:effort` 省略（deepseek-v4 系のみ例外的に対応）⑤ xai `grok-4.5` の上限は `high`（`:xhigh` はサイレントクランプ — xhigh は grok-build プロバイダ専用だが、そちらは effort サフィックス自体が解釈されない）。範囲外の段はエラーではなく**クランプ**される。
>
> **脚注（上流ギャップ）**：Claude 5 ファミリーは API 公式には両方とも `max` まで対応する。GJC 0.9.1 のパーサが fable ファミリーを知らずフォールバック推論し、sonnet-5 が 4.6 のクランプを継承する**エンジン側のギャップ**であり、再現資料と共に**上流へ報告済み**。本ガイドは GJC 実効値で記載する。

### 3-3. 契約 → プロバイダ

| 契約 | provider-id | 備考 |
|---|---|---|
| claude | `anthropic` | 全 effort。Claude 5 ファミリー（Fable 5·Sonnet 5）を含む |
| gpt | `openai-codex` | **ChatGPT アカウント → base GPT（gpt-5.5/5.4）を提供**。文脈：gpt-5.4=1M · gpt-5.5=272K |
| grok | `xai` | 全ラインナップ + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra サブスクトークン**。Gemini + 同梱 Claude（Opus 4.6 — Claude 5 リリース後の同梱構成は再確認前） |
| opencode go | `opencode-go` | API キー（`OPENCODE_API_KEY`） |

> [!NOTE]
> **openai-codex 経路の注意**：ChatGPT（Codex）アカウントでログインすると **base GPT モデル（`gpt-5.5`、`gpt-5.4`）** が提供される。単体の `-codex` 派生（`gpt-5.3-codex`、`gpt-5.2-codex`、`gpt-5.1-codex-max/mini`）はこの経路では**非対応**（`not supported when using Codex with a ChatGPT account`）なので、本ガイドはコーディング役も検証済みの **base GPT** に統一している。
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
| planner（推論 GPQA/ARC-AGI） | **Gemini 3.1 Pro**† | GPQA 94.3 · ARC-AGI-2 77.1（流動推論は GPT-5.5 — [KO 正本 §6-2](./README.md#6-2-역할-배치-최적성-검토-deep-research--실측) · GPQA 単独首位は Sonnet 5 の 96.2） |
| architect（文脈 · マルチモーダル） | **Gemini 3.1 Pro**† | 1M 文脈 · MMMU-Pro 81% |
| default（ツール呼び出し · 誠実性） | **Opus 4.8 / Fable 5** | ルータ品質 = 全体の上限（Fable は refusal・課金のキャベアット — [§5](#5-️-最終カタログ13プロファイル)） |
| critic（独立性） | **クロスファミリー** | メタ審判 > 討論型集計 |

> † **後継目前の脚注**：planner 軸は GPT-5.6 Sol がパートナー限定プレビュー中（2026-06-26、`max` effort + `ultra` サブエージェントモード — GA まで数週間）、architect 軸は Gemini 3.5 Pro（2M 文脈、Deep Think）が 7月 GA に延期。いずれもリリース時にこの表は再検証対象。

**合意原則**

1. **default = Anthropic フラッグシップ（Opus/Fable）固定**（マルチベンダー構成）— ルータ品質が全体の上限。`solo-*` は単一ベンダーの最強を default に。
2. **architect = Gemini 3.1 Pro（マルチモーダル）/ Opus（超長文脈）** — Gemini はビジョンと中程度文脈に最適。200k+ のテキスト検索は Opus（MRCR 76%@1M、Gemini は 26% に崩壊）。
3. **critic = クロスファミリー** — メインループ/プランナーと別ベンダーで自己選好バイアスを緩和。
4. **構造 = 強メインループ + シグナル駆動委譲 + 失敗駆動 effort エスカレーション。**
5. **クエリ毎のプロファイル切替 ❌** — キャッシュ損失 > 利得。モード境界でのみ切替。

> ベンチマークは時点依存 → 四半期ごとに再検証推奨。絶対順位は vals.ai 独立ボードに限定。

---

## 5. 🗂️ 最終カタログ（13プロファイル）

<div align="center">
<img src="assets/profiles-matrix.svg" alt="プロファイル × 役割 マトリクス" width="100%">
</div>

> ★ = 日常推奨。上部バナー = **`legend` 構成**（持続可能な最強 — default のみ Fable 5）。コスト均衡の日常推奨は **`daily`**（executor·critic のみ安価に置換）。マルチベンダー構成は `default = Anthropic フラッグシップ（Opus/Fable）`·`critic=クロスファミリー`（solo-* は単一ベンダー最強）を維持し、全てエンジンの effort ハードルールを通過、**セレクタ検証状態を追跡**（[§6](#6--検証マトリクス)。2026-07-09 rerun は Grok/OpenAI/Gemini/opencode、Anthropic は quota により 2026-07-02 last-good 維持）。

| プロファイル | 一言 | こんな時 |
|---|---|---|
| ⭐ **daily** | Opus メインループ + 各役割の最適ベンダーへ委譲 | **日常の既定** |
| 🏆 **ultimate** | コスト度外視、役割ごと最強（持続可能版） | 精度がコストより重要 |
| 🔥 **ultimate-f5** | Fable 5 中心のイベント版 — **サブスク込み ~2026-07-07** | イベント期間の最高精度 |
| 👑 **legend** | メインループのみ Fable 5、他は持続構造 | 7/7 以後も維持できる最強 |
| 🏎️ **coding-sprint** | executor 主役 + コード理解 critic | 純粋な実装スループット |
| 🛡️ **escalation** | 失敗シグナル時に Fable 5 を救援投入 + critic マルチベンダーパネル | マージ・セキュリティ・決済・不可逆変更 |
| 🚨 **cyber-cop** | reviewer モード — architect·critic が主役、PRレビュー·セキュリティ監査専用 | 他人の PR レビュー·マージゲート·セキュリティ監査 |
| 💸 **eco** | メインループのみ Opus、委譲は全て安価/サブスク | コスト圧・大量作業 |
| 🗺️ **monorepo** | 全域 ≥1M 文脈（gpt-5.5 除外） | 巨大コードベース |
| 🧱 **solo-anthropic** | 全役割 Opus（v1.4: critic も Opus） | 単一ベンダー運用 |
| 🤖 **solo-openai** | 全役割 base GPT（5.5=272K · 5.4=1M） | ChatGPT のみ契約 |
| 🤝 **claude-codex** | Claude=実行・文脈 / Codex=推論・批評 | Claude+Codex の2契約のみ |
| 🥇 **claude-codex-max** | claude-codex のコスト度外視最強版 | Claude+Codex · 精度優先 |

<details>
<summary><b>📋 完全な YAML を展開（gjc-profiles.yml と同一 — モデルマッピング基準、コメントの§参照のみ README に合わせて調整）</b></summary>

```yaml
profiles:

  daily:                               # ★ 日常の既定 (--default daily)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # メインループの効率ニー
      executor:  openai-codex/gpt-5.4:high                      # コーディング特化・中価格($2.5/15)・ベンダー分散(検証✅)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 検証済み推論1位(GPQA 94.3 / ARC-AGI-2 77.1)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M 文脈・マルチモーダル(MMMU-Pro 81%)
      critic:    xai/grok-4.5:medium                            # クロスファミリーの独立批評。grok-4.5 $2/$6（実効約 $0.84/$6.2）；medium≈1.7k reasoning/~14s

  ultimate:                            # コスト度外視、役割ごと最強 + ベンダー分散（持続可能版 — イベント版は ultimate-f5）
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # サブスク込みコーディング最強(SWE-bench Verified 88.6)
      planner:   openai-codex/gpt-5.5:xhigh                     # 最上位推論 + OpenAI の多様性
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M 文脈・マルチモーダル
      critic:    xai/grok-4.5:high                              # クロスファミリーの独立批評

  ultimate-f5:                         # 🔥 イベント: Fable 5 中心 — サブスク込み ~2026-07-07(週次上限の50%まで)、以後 usage credits($10/$50)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # ルータ=品質上限。refusal(HTTP 200+stop_reason)に注意
      executor:  anthropic/claude-fable-5:xhigh                 # SWE-bench Verified 95.0 の新1位。⚠:max 禁止(xhigh へサイレントクランプ)
      planner:   openai-codex/gpt-5.5:xhigh                     # 推論軸は Fable 優位未証明(ARC-AGI-2 未公開) — GPT を維持
      architect: google-antigravity/gemini-3.1-pro-low:high     # マルチモーダルの検証済み優位を維持(Fable のビジョンは vendor-claimed)
      critic:    xai/grok-4.5:high                              # クロスファミリー不変 — Fable の自己評価は禁止
      # 7/7 以後: default を opus-4-8:high に下げれば legend と同一の持続構造

  legend:                              # 👑 Ultimate Legend — 7/7 以後も維持できる最強 (fable は default の1枠のみ)
    display_name: legend5
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # ルータ品質の上限 = Fable (usage credits 露出が最小の枠)
      executor:  anthropic/claude-opus-4-8:max                  # サブスク込みコーディング最強(88.6)
      planner:   openai-codex/gpt-5.5:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.5:high
      # credits 費用を回避するなら: default を opus-4-8:high に — ultimate と同一になる

  coding-sprint:                       # 純粋な実装スループット。executor 主役 + コード理解 critic
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # メインループのオーケストレーション
      executor:  anthropic/claude-opus-4-8:max                  # サブスク込みコーディング最強(88.6)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 推論検証1位で軽量プランニング
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M 文脈レビュー
      critic:    openai-codex/gpt-5.4:high                      # コード理解 critic(実バグ検出)、クロスファミリー vs gemini

  escalation:                          # 高失敗コスト — 失敗シグナル時に最強実行者(Fable 5)を投入 + critic マルチベンダー並列パネル(§9)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-fable-5:xhigh                 # 失敗したタスクの救援投手(SWE-V 95.0)。間欠使用 = credits 課金とも好相性
      planner:   openai-codex/gpt-5.5:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.5:high                              # + 3票クロスベンダー critic パネル(独立投票→メインループ集計)。grok-4.5 :xhigh/:max は high へサイレントクランプのため不使用
      # (v1.3 までの critic :xhigh は no-op クランプだった — xhigh は grok-build プロバイダ専用で、そちらは effort サフィックス非対応)

  cyber-cop:                           # 🚨 reviewer モード — PRレビュー·セキュリティ監査（author モードの逆相）
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high                 # 不変条件遵守 + 1M ctx。集計者に限定 — critic の raw verdict を保持·公開（routing-rules 契約）
      executor:  openai-codex/gpt-5.5:high                      # 脇役 — 再現 PoC·failing test·harness（Terminal-Bench 82.7）
      planner:   google-antigravity/gemini-3.1-pro-low:high     # レビューチェックリスト·監査範囲（critic と cross-family）
      architect: anthropic/claude-opus-4-8:high                 # 主役1 — 一次コードレビュー判定者、1M 実効検索（MRCR 76% vs Gemini 26%）
      critic:    openai-codex/gpt-5.5:high                      # 主役2 — マージゲート、Claude 作成コードと cross-family
      # 高リスク PR·セキュリティ監査：critic 3票並列パネル {openai-codex/gpt-5.5:high, xai/grok-4.5:high,
      # google-antigravity/gemini-3.1-pro-low:high} — 独立投票後に本体が集計（議論禁止）、2/3 反対または CRITICAL/BLOCK 1件で遮断
      # (3票目の grok は xai ログイン時 — 未保有でも 2票 {gpt-5.5, gemini} で provenance 最低条件(non-default family ≥2)を充足)

  eco:                                 # 最安 — メインループのみ Opus(effort 抑制)、委譲は超安価/サブスクモデル(検証表で追跡✅)
    required_providers: [anthropic, opencode-go, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:low                  # ルータは下げられない、effort のみ削減
      executor:  opencode-go/deepseek-v4-flash                  # $0.14/0.28, 1M, 最安コーダー(5番目のベンダー)。代替: sonnet-5:medium(≈sonnet-4-6:high、イントロ $2/10 ~8/31)
      planner:   xai/grok-4-1-fast:high                         # $0.2/0.5, 2M, 安価な推論
      architect: google-antigravity/gemini-3.1-pro-low          # サブスクトークン、低 effort、1M 文脈
      critic:    google-antigravity/gemini-3.5-flash-low        # サブスクトークン、軽量、クロスファミリー vs executor(opencode-go)。リテラル id にピン(旧 'gemini-3.5-flash' はファジーマッチ)

  monorepo:                            # 巨大コードベース — 全域 1M 文脈 (★gpt-5.5 272K 除外 — gpt-5.4 は 1M だが Opus が同等以上)
    required_providers: [anthropic, google-antigravity, opencode-go]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 1M
      executor:  anthropic/claude-opus-4-8:high                 # 1M
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 推論(スコープ入力)
      architect: anthropic/claude-opus-4-8:high                 # Opus 4.8 = GJC 1M 文脈ウィンドウ対応(マルチターン蓄積・検索が最良)。単一メッセージ貼付けのみ約400k 上限 — 一括 >400k は opencode-go/deepseek-v4-pro
      critic:    opencode-go/glm-5.2                            # オープンウェイト1位(AA 51 > V4 Pro 44)、0.7.10 バンドルカタログ入り、クロスファミリー vs anthropic (代替: deepseek-v4-pro)

  solo-anthropic:                      # 単一ベンダー運用 — 全役割 Opus (v1.4: critic Sonnet→Opus、能力優先)
    required_providers: [anthropic]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max
      planner:   anthropic/claude-opus-4-8:max
      architect: anthropic/claude-opus-4-8:high                 # 1M, Gemini 代替(フォールバック1位)
      critic:    anthropic/claude-opus-4-8:high                 # ⚠同一モデルの自己評価=バイアス最大(研究で確認) — 品質経路はクロスファミリー構成
      # Sonnet 5 critic は非推奨: レビューアのバグ再現率が実測で低下(63%→50%、適合率のみ上昇)

  solo-openai:                         # ChatGPT(Codex)アカウントのみ — base GPT 専用
    required_providers: [openai-codex]
    model_mapping:
      default:   openai-codex/gpt-5.5:high                      # ルータ(base GPT 最強、文脈 272K)
      executor:  openai-codex/gpt-5.5:xhigh                     # このアカウント最強のコーダー
      planner:   openai-codex/gpt-5.5:xhigh                     # 最上位推論
      architect: openai-codex/gpt-5.4:high                      # ★gpt-5.4 = 1M 文脈 — 大容量入力はこちら(5.5 は 272K)
      critic:    openai-codex/gpt-5.4:high                      # ⚠同一ベンダー=独立性が弱い(トレードオフ)

  claude-codex:                        # ★2ベンダー(Claude+Codex)のみ — 日常均衡。Anthropic=実行・文脈 / Codex=推論・批評
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # ルータ・ツール信頼
      executor:  anthropic/claude-opus-4-8:high                 # サブスク込みコーディング最強(SWE-bench 88.6)
      planner:   openai-codex/gpt-5.5:high                      # OpenAI 推論フラッグシップ
      architect: anthropic/claude-opus-4-8:high                 # 1M ウィンドウ(gpt-5.5 272K 制限を回避)
      critic:    openai-codex/gpt-5.4:high                      # クロスファミリー vs Opus(executor)、コード理解

  claude-codex-max:                    # 2ベンダー(Claude+Codex)最強 — コスト度外視
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # SWE-bench 88.6
      planner:   openai-codex/gpt-5.5:xhigh                     # 最上位推論(ARC-AGI-2 強)
      architect: anthropic/claude-opus-4-8:high                 # 1M ウィンドウ
      critic:    openai-codex/gpt-5.5:high                      # クロスファミリーの独立批評 vs Opus

# ─────────────────────────────────────────────────────────────────────────────
# Claude 5 ファミリー(2026-07-01~): Fable 5 = $10/$50(Opus の2倍)。サブスク込みは ~7/7(週次上限の50%)のみ — 「無料」ではない。
#   Sonnet 5 = $3/$15(イントロ $2/$10 ~2026-08-31)、トークナイザ変更で同一テキストが約30% トークン増。
#   GJC 実効 effort: fable-5 ≤xhigh · sonnet-5 ≤high (API は両方 max 対応 — GJC パーサのギャップ、上流へ報告済み)。
# opencode-go: OPENCODE_API_KEY 設定で有効(eco.executor·monorepo.critic で使用)。
#   検証✅: deepseek-v4-flash/pro · glm-5.2 · minimax-m2.7 · qwen3.7-max · kimi-k2.6 · mimo-v2.5。
#   新規入荷(未検証・候補): kimi-k2.7-code(バジェット executor の有力候補) · minimax-m3(1M マルチモーダル)。
# 任意: grok サブスク(SuperGrok OAuth)の grok-build/composer も使用可:
#   grok-build/grok-4.3 (bare セレクタのみ動作、effort サフィックス非対応 — 検証✅ 2026-07-02)。
```

</details>

各プロファイルの設計理由（v1.4 新規：`ultimate-f5` のイベント条件 — **サブスク込みは ~2026-07-07・週次上限の 50% までで「無料」ではない** — と refusal（HTTP 200 + `stop_reason: refusal`）への注意、`legend` の持続構造と `display_name: legend5` の保護、`escalation` の「Fable 5 救援投手」再設計と旧 critic `:xhigh` no-op の訂正、`solo-anthropic` 全 Opus 化 — 研究上、**強いモデルほど自己選好バイアスはむしろ強く**（arXiv [2410.21819](https://arxiv.org/abs/2410.21819) · [2604.22891](https://arxiv.org/abs/2604.22891)）、能力はバイアスを相殺しない。全 Opus は「能力優先」の選択であり、**品質経路はあくまでクロスファミリー構成**）、ニーズ別チートシート、完全なディープリサーチ分析は、**[韓国語の正本 README](./README.md#5-️-최종-카탈로그-13종)** と公式 **[GJC ドキュメント](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)** を参照。

---

## 6. ✅ 検証マトリクス

> 2026-07-09（gjc 0.9.1）rerun では、Grok/OpenAI/Gemini/opencode の核心セレクタを `gjc -p --no-session --no-tools --model <sel> "..."` で**実呼び出し**して再検証した。Anthropic 席は 7日 quota/rate-limit により `blocked(creds/rate-limit)` のため、2026-07-02 last-good 証拠を維持する。「動く」は推測ではなく、実呼び出しまたは明記された last-good 証拠に基づく。

| プロバイダ | 検証済みセレクタ（✅ 動作） |
|---|---|
| `anthropic` | `claude-fable-5`（bare·low·medium·high — `:max` は **xhigh へサイレントクランプ**され動作、07-02✅）· `claude-sonnet-5`（bare·medium·high — `:max` は **high へサイレントクランプ**され動作、07-02✅）· `claude-opus-4-8`（low·medium·high·max、`:high` は 07-02 再検証✅）· `claude-sonnet-4-6:high`（07-02 再検証✅）· 07-09 rerun はアカウント rate-limit で blocked（モデル回帰ではない） |
| `openai-codex` | `gpt-5.5:high`（**07-02 再認証後に再検証✅**）· `gpt-5.5:xhigh` · `gpt-5.4:high` · `gpt-5.4-mini:high` |
| `xai` | `grok-4.5:medium`/`:high`（07-09✅ — `:xhigh`/`:max` は high へクランプ；xai 専用、provider 500K / GJC 222K floor、$2/$6）· `grok-4-1-fast:high`（07-02✅）· `grok-4-fast:high`（07-02✅）· `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3`（**bare セレクタのみ** — effort サフィックス非解釈、07-02✅。SuperGrok OAuth） |
| `google-antigravity` | `gemini-3.1-pro-low`（±`:high`、07-02 再検証✅）· `gemini-3.5-flash-low`（**新規ピン**、07-02✅）· `gemini-3.5-flash`（ファジーマッチで動作、07-02✅）· `gemini-3-flash` · `claude-opus-4-6-thinking`（06-18 — Claude 5 リリース後の同梱構成は再確認前） |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro`（07-02 再検証✅）· `glm-5.2`（**0.7.10 バンドル入り**、07-02✅）· `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5`（`OPENCODE_API_KEY` 必要） |

> [!WARNING]
> **本環境で動かなかったセレクタ**（回避）：`openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`（ChatGPT アカウント非対応）· `google-antigravity/gemini-3.1-pro-high`（**0.7.10 のカタログ一覧には現れるが呼び出しは依然 400** — 文書化済みの罠は健在、エンジンは `gemini-3.1-pro-low:high` を使用）· `gemini-3-pro`（廃止）· `claude-sonnet-4-6-thinking`（404）· `gpt-oss-120b`（500）。`opencode-go/*` は **`OPENCODE_API_KEY` 未設定時のみ**失敗（設定後は上表どおり動作）。参考：`fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.5:xhigh/max` は失敗ではなく**サイレントクランプ**（[§3-2](#3-2-effort-チートシート)）。

> [!NOTE]
> `opencode-go/glm-5.2` は **0.7.10 からバンドルカタログ入り**した（旧「ライブカタログ専用」のキャベアットは廃止）。一方 `google-antigravity/gemini-3.5-flash` のリテラル id はカタログに無く（`-low`/`-extra-low` のみ存在）、**ファジーマッチで偶然動いている**だけなので、v1.4 のプロファイルは `gemini-3.5-flash-low` にピンした。ディスカバリ未更新の状態では `selector did not resolve` で有効化に失敗しうる — 再ログイン/リトライでカタログを更新するか、バンドル id に置換する（critic は `opencode-go/deepseek-v4-pro`、GLM は `zai/glm-5.2` — `zai` を `required_providers` に追加）。

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
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.4:high" "Reply exactly: OK"
```

> **役割配置の詳細レビューと GJC 実効コンテキスト実測**（韓国語正本の §6-2 / §6-3）— 骨格はほぼ最適と再確認：executor 軸は v1.4 で **Fable 5**（SWE-bench Verified 95.0 / SWE-bench Pro 80.3）に交代し、Opus 4.8 は「サブスク込み最強（88.6）」として維持；planner の推論軸は分裂（GPQA は飽和し単独首位は Sonnet 5 の 96.2、流動推論 ARC-AGI-2 は GPT-5.5 が明確に優位 0.850 vs 0.771 — Fable は未公開で優位未証明）；`gemini-3.1-pro-low:high` は Gemini のネイティブ高推論モードを呼ぶ（劣化版ではない）；Opus は 1M 文脈の実効検索で優位を保つ一方 Gemini は崩壊（MRCR 76%@1M vs 26% — ゆえに monorepo architect = Opus）；単一メッセージ `@file` 入力上限（anthropic/antigravity で約 400k）は 1M 文脈ウィンドウとは別物（巨大入力はターン分割で 1M を活用；grok 2M への swap は棄却）。完全な表と出典は **[韓国語 README §6](./README.md#6--검증-매트릭스)** を参照。

---

## 7. 🛠️ インストール / アンインストール

### ワンクリック（推奨）

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

インストーラの動作：13プロファイルを `~/.gjc/agent/models.yml` に安全マージ（再実行で自動更新）・既存ファイルを自動バックアップ・既定プロファイルを `daily` に設定。`curl` + `python3` だけで動く。

```bash
# オプション
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash    # 既定プロファイル指定
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
| マージ/リリース前 · セキュリティ · 決済 | `escalation` |
| PR レビュー · セキュリティ監査セッション | `cyber-cop` |
| 精度最優先（Fable 5 イベント ~2026-07-07） | `ultimate-f5` → 以後は `legend` |
| 大量リファクタ · マイグレーション | `eco` |
| 巨大コードベースへ突入 | `monorepo` |
| 単一ベンダー運用 | `solo-anthropic` |

---

## 9. 🧪 並列エージェント + 信頼性

直列の引き継ぎは `0.99ⁿ` で減衰し、マルチエージェントは繋ぎ方を誤ると「偽の合意」に固まる。並列設計はこの2つを防ぐように組む。

```text
直列チェーン 5段(各 0.99)：  0.99^5 ≈ 95.1%    → 長いほど崩壊
並列独立 5個(OR 成功)：      1-(0.01)^5 ≈ 100%  → 多様性が信頼性を高める
```

**設計原則**
- critic = **メインループと別ベンダー、並列で独立投票しメインループが集計**（討論禁止 — メタ審判が優位）。
- critic パネル例：`{xai/grok-4.5:high, openai-codex/gpt-5.4, google-antigravity/gemini-3.1-pro-low:high}` を並列 → 2/3 が否なら破棄。
- executor のファンアウトは**作業が真に独立**（共有状態なし）なときだけ。
- チェーンは短く、メインループを単一の真実源に（サブ同士で直接合意させない）。

---

## 10. 💰 コスト

Gemini（`google-antigravity`）は **Google AI Pro/Ultra のサブスクトークン**で動く（トークン従量ではなくサブスクに含まれる）。**Fable 5 は 2026-07-07 まで Claude サブスク（Pro/Max/Team）に含まれる**が、週次使用上限の 50% までという制限があり、**以後は usage credits の別課金**になる — 「無料」ではない。他は従量課金で、主要モデル単価は以下（$/1M、入力/出力）：

| モデル | $/1M (in/out) | 役割 |
|---|---|---|
| Claude Fable 5 | 10 / 50（バッチ 5/25 · キャッシュヒット 1）† | ultimate-f5 default·executor · legend default · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor |
| Claude Sonnet 5 | 3 / 15（イントロ 2/10 ~2026-08-31）‡ | eco executor 代替 |
| GPT-5.5 | 5 / 30 | planner(ultimate) |
| GPT-5.4 | 2.5 / 15 | executor/critic(daily·sprint) |
| Grok 4.5 | 2 / 6（実効入力約 $0.84 @88% cache） | critic(v1.10) |
| Grok 4.1 Fast | 0.2 / 0.5 | eco planner |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 単一貼付けのフォールバック |
| Gemini 3.1 Pro / 3.5 Flash | サブスクトークン | planner·architect·critic |

> † Fable 5 は Opus のちょうど2倍の単価。サブスク込み分（~7/7）も週次上限を消費する。
> ‡ Sonnet 5 は**トークナイザ変更で同一テキストが約 30% 多くトークン化**される — 実効コストは表示単価より高く見積もること。
> （参考：DeepSeek 系は DeepInfra プロバイダ経由なら V4 Pro $1.30/$2.60 — [§3-3](#3-3-契約--プロバイダ)。）

**プロファイル相対コスト**

| プロファイル | コスト | 主因 |
|---|---|---|
| ultimate-f5 | ●●●●● | default·executor Fable 5 — ~7/7 サブスク込み(週次上限の50%)、以後 credits $10/50 |
| legend | ●●●●● | default Fable 5(7/7 後は credits) + executor Opus `:max` |
| ultimate / escalation | ●●●●● | executor Opus `:max`/Fable `:xhigh`(救援) + planner GPT-5.5 `:xhigh` |
| coding-sprint | ●●●●○ | executor Opus `:max` |
| solo-anthropic | ●●●●○ | 全役割 Opus (executor/planner `:max`) |
| daily | ●●●○○ | メインループ Opus `:medium`、委譲は中/低価格に分散 |
| monorepo | ●●●○○ | executor/architect Opus + Gemini(サブスク) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash($0.14) + サブスク Gemini |

> **3つの節約レバー**：① 委譲作業を超安価モデル（DeepSeek V4 Flash $0.14、Grok Fast $0.2）/ サブスクトークン（Gemini）へ ② 失敗時のみ effort を上げる ③ メインループ（Anthropic フラッグシップ）は品質の上限なので維持しつつ、日常は `:medium`、コスト逼迫時は `:low` — Fable default（`legend`）の credits が負担なら default を `opus-4-8:high` へ。

---

## 11. 📖 出典

**コーディング（executor）** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.0](https://www.tbench.ai/leaderboard/terminal-bench/2.0)

**Claude 5 ファミリー** · [Fable 5 再デプロイ告知](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com モデルドキュメント](https://platform.claude.com/docs) — 価格・サブスク込み（~7/7）・effort 仕様を 2026-07-02 に相互確認

**推論（planner）** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**文脈 · マルチモーダル（architect）** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**ツール呼び出し · 誠実性（default）** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**独立性 · ルーティング（critic + 設計）** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [自己選好は能力とともに強まる](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**公式モデル/価格** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**ワンライナーで導入、役割ごとに最適モデル。**

**v1.5** · [CHANGELOG](./CHANGELOG.md) · [保守プレイブック](./MAINTAINING.md) · ライセンス [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
