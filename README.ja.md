<div align="center">

# 🧩 GJC マルチベンダー究極セットアップ

### claude · gpt · grok · gemini · opencode go — 5つの契約を*役割ごと*に振り分ける検証済み構成

モデル選びで悩むのをやめよう。**ワンライナーでインストール**し、各役割に最適なモデルを自動で割り当てる。

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-1.11.0-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/profiles-13-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
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
- critic が**コード作成者(Claude 想定)に対して cross-family**(GPT-5.6 Sol — v1.11 で gpt-5.5 と同価格の世代交代) → 自己選好バイアスを構造的に抑制([arXiv 2410.21819](https://arxiv.org/abs/2410.21819))。
- 高リスク PR·セキュリティ監査は**3 票並列パネル**(`gpt-5.6-sol` · `grok-4.5` · `gemini-3.1-pro`)を招集し、独立投票 → 2/3 反対または CRITICAL/BLOCK 1 件で遮断。

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

**GJC 0.9.1~0.9.5 の実効値**である — API 公式仕様と異なる箇所がある（下の脚注）：

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← 全6段
Fable 5                 minimal low medium high xhigh       ← :max は xhigh へサイレントクランプ · thinking 常時オン
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max は high へサイレントクランプ
GPT 5.4 / 5.5 / 5.6 (base)  low medium high xhigh                ← 5.6 の出荷上限は xhigh
Grok 4.5（xai）          low medium high                      ← :xhigh/:max は high へサイレントクランプ · minimal はネイティブ effort ではない
grok-build/grok-4.3     ── bare セレクタのみ（effort サフィックス非解釈）──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go その他       ── effort サフィックス省略（既定）──
google-antigravity Gemini  gemini-3.1-pro-low:high（高推論）· gemini-3.1-pro-low（低 effort）
```

> [!IMPORTANT]
> **5つのハードルール**：① Gemini Pro は `low`/`high` のみ ② openai-codex の文脈は**モデル別** — `gpt-5.4`=**1M** · `gpt-5.5`·`gpt-5.6 3種`=**272K**（5.6 の API 仕様は 1.05M — codex 表記の下限）③ Sonnet（4.6/5）は GJC で `xhigh`/`max` 不可 · **Fable 5 は `max` 不可**（それぞれ high/xhigh にクランプ）④ opencode-go は `:effort` 省略（deepseek-v4 系のみ例外的に対応）⑤ xai `grok-4.5` の上限は `high`（`:xhigh` はサイレントクランプ — xhigh は grok-build プロバイダ専用だが、そちらは effort サフィックス自体が解釈されない）。範囲外の段はエラーではなく**クランプ**される。gpt-5.6 3種はカタログに `max` まで表示され、実呼び出しも受理されるが（07-10 検証）、**深度未検証 — 本ガイドの出荷上限は `xhigh`**。
>
> **脚注（上流ギャップ）**：Claude 5 ファミリーは API 公式には両方とも `max` まで対応する。GJC パーサ（0.9.1~0.9.5）が fable ファミリーを知らずフォールバック推論し、sonnet-5 が 4.6 のクランプを継承する**エンジン側のギャップ**であり、再現資料と共に**上流へ報告済み**。本ガイドは GJC 実効値で記載する。

### 3-3. 契約 → プロバイダ

| 契約 | provider-id | 備考 |
|---|---|---|
| claude | `anthropic` | 全 effort。Claude 5 ファミリー（Fable 5·Sonnet 5）を含む |
| gpt | `openai-codex` | **ChatGPT アカウント → base GPT（gpt-5.6 sol/terra/luna · 5.5 · 5.4）を提供**。ctx: gpt-5.4=1M · 5.5/5.6 3種=272K |
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

> ★ = 日常推奨。上部バナー = **`legend` 構成**（持続可能な最強 — default のみ Fable 5）。コスト均衡の日常推奨は **`daily`**（executor·critic のみ安価に置換）。マルチベンダー構成は `default = Anthropic フラッグシップ（Opus/Fable）`·`critic=クロスファミリー`（solo-* は単一ベンダー最強）を維持し、全てエンジンの effort ハードルールを通過、**セレクタ検証状態を追跡**（[§6](#6--検証マトリクス)。2026-07-10 rerun で**全プロバイダ**を再検証 — gpt-5.6 3種を新規検証、Anthropic の rate-limit も解除）。

| プロファイル | 一言 | こんな時 |
|---|---|---|
| ⭐ **daily** | Opus メインループ + 各役割の最適ベンダーへ委譲 | **日常の既定** |
| 🏆 **ultimate** | コスト度外視、役割ごと最強（持続可能版） | 精度がコストより重要 |
| 🔥 **ultimate-f5** | Fable 5 中心のイベント版 — **サブスク込み ~2026-07-12 23:59 PT（延長確定）** | イベント期間の最高精度 |
| 👑 **legend** | メインループのみ Fable 5、他は持続構造 | 7/12 以後も維持できる最強 |
| 🏎️ **coding-sprint** | executor 主役 + コード理解 critic | 純粋な実装スループット |
| 🛡️ **escalation** | 失敗シグナル時に Fable 5 を救援投入 + critic マルチベンダーパネル | マージ・セキュリティ・決済・不可逆変更 |
| 🚨 **cyber-cop** | reviewer モード — architect·critic が主役、PRレビュー·セキュリティ監査専用 | 他人の PR レビュー·マージゲート·セキュリティ監査 |
| 💸 **eco** | メインループのみ Opus、委譲は全て安価/サブスク | コスト圧・大量作業 |
| 🗺️ **monorepo** | 全域 ≥1M 文脈（gpt-5.5/5.6 除外） | 巨大コードベース |
| 🧱 **solo-anthropic** | 全役割 Opus（v1.4: critic も Opus） | 単一ベンダー運用 |
| 🤖 **solo-openai** | 全役割 base GPT（5.6 Sol 主力 · 5.4=1M レーン） | ChatGPT のみ契約 |
| 🤝 **claude-codex** | Claude=実行・文脈 / Codex=推論・批評 | Claude+Codex の2契約のみ |
| 🥇 **claude-codex-max** | claude-codex のコスト度外視最強版 | Claude+Codex · 精度優先 |

<details>
<summary><b>📋 完全な YAML を展開（gjc-profiles.yml と同一 — モデルマッピング基準、コメントの§参照のみ README に合わせて調整）</b></summary>

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
      critic:    anthropic/claude-opus-4-8:high                 # v2: grok→Opus 교체 — xai 키 장벽 제거(구독-only daily), Grok critic 은 defect-recall 직접근거 0건(2축 리서치 합의)

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
      architect: anthropic/claude-opus-4-8:high                 # 1M 멀티턴 누적·검색 최상. 단일 메시지 paste ~350-400k 한도 — 한 방 >400k 는 opencode-go/deepseek-v4-pro
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

各プロファイルの設計理由（v1.4 新規：`ultimate-f5` のイベント条件 — **サブスク込みは ~2026-07-12 23:59 PT・週次上限の 50% までで「無料」ではない** — と refusal（HTTP 200 + `stop_reason: refusal`）への注意、`legend` の持続構造と `display_name: legend5` の保護、`escalation` の「Fable 5 救援投手」再設計と旧 critic `:xhigh` no-op の訂正、`solo-anthropic` 全 Opus 化 — 研究上、**強いモデルほど自己選好バイアスはむしろ強く**（arXiv [2410.21819](https://arxiv.org/abs/2410.21819) · [2604.22891](https://arxiv.org/abs/2604.22891)）、能力はバイアスを相殺しない。全 Opus は「能力優先」の選択であり、**品質経路はあくまでクロスファミリー構成**）、ニーズ別チートシート、完全なディープリサーチ分析は、**[韓国語の正本 README](./README.md#5-️-최종-카탈로그-13종)** と公式 **[GJC ドキュメント](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)** を参照。

---

## 6. ✅ 検証マトリクス

> 2026-07-10（gjc 0.9.5）に**全プロバイダ**の核心セレクタを `gjc -p --no-session --no-tools --model <sel> "..."` で**実呼び出し**して再検証した（`evidence/2026-07-10-selectors-rerun-2.md`）— Anthropic の rate-limit が解除され全席グリーン、gpt-5.6 3種は初検証。「動く」は推測ではなく実呼び出しに基づく。

| プロバイダ | 検証済みセレクタ（✅ 動作） |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh`（**07-10 rerun✅** — `:max` は xhigh へサイレントクランプ）· `claude-sonnet-5:high`（07-10✅ — `:max` は high へサイレントクランプ）· `claude-opus-4-8:high`（07-10✅；low·medium·max 07-02✅）· `claude-sonnet-4-6:high`（07-10✅）— 07-09 の rate-limit 解除、全席再検証完了 |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh`（07-10✅）· `gpt-5.6-terra:high`/`:xhigh`（07-10✅）· `gpt-5.6-luna:high`（07-10✅）· 3種 `:max` は受理されるが深度未検証（未出荷）· `gpt-5.5:high`（07-02✅、v1.11 でプロファイルから退役—カナリア維持）· `gpt-5.4:high`（1M ctx レーン） |
| `xai` | `grok-4.5:medium`/`:high`（07-09✅ — `:xhigh`/`:max` は high へクランプ；xai 専用、provider 500K / GJC 222K floor、$2/$6）· `grok-4-1-fast:high`（07-02✅）· `grok-4-fast:high`（07-02✅）· `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3`（**bare セレクタのみ** — effort サフィックス非解釈、07-02✅。SuperGrok OAuth） |
| `google-antigravity` | `gemini-3.1-pro-low`（±`:high`、07-10✅）· `gemini-3.5-flash-low`（**リテラルピン**、07-10✅）· `gemini-3.5-flash`（ファジーマッチで動作）· ⚠`gemini-3.1-pro-high` は 0.9.5 から 400 ではなく **`-low` のデフォルト effort へサイレントにファジー解決**される（高推論ではない — 罠）· `gemini-3-flash` · `claude-opus-4-6-thinking`（06-18 — Claude 5 リリース後の同梱構成は再確認前） |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro`（07-02 再検証✅）· `glm-5.2`（**0.7.10 バンドル入り**、07-02✅）· `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5`（`OPENCODE_API_KEY` 必要） |

> [!WARNING]
> **本環境で動かなかったセレクタ**（回避）：`openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`（ChatGPT アカウント非対応）· `google-antigravity/gemini-3.1-pro-high`（**0.9.5 から 400 ではなく `-low` デフォルト effort へサイレントにファジー解決 — 「動く」が高推論ではない罠**、エンジンは `gemini-3.1-pro-low:high` を使用）· `gemini-3-pro`（廃止）· `claude-sonnet-4-6-thinking`（404）· `gpt-oss-120b`（500）。`opencode-go/*` は **`OPENCODE_API_KEY` 未設定時のみ**失敗（設定後は上表どおり動作）。参考：`fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.5:xhigh/max` は失敗ではなく**サイレントクランプ**（[§3-2](#3-2-effort-チートシート)）— gpt-5.6 3種は `:max` を受理するが深度未検証（未出荷）。

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
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
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
| 精度最優先（Fable 5 イベント ~2026-07-12） | `ultimate-f5` → 以後は `legend` |
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
- critic パネル例：`{xai/grok-4.5:high, openai-codex/gpt-5.6-terra, google-antigravity/gemini-3.1-pro-low:high}` を並列 → 2/3 が否なら破棄。
- executor のファンアウトは**作業が真に独立**（共有状態なし）なときだけ。
- チェーンは短く、メインループを単一の真実源に（サブ同士で直接合意させない）。

---

## 10. 💰 コスト

Gemini（`google-antigravity`）は **Google AI Pro/Ultra のサブスクトークン**で動く（トークン従量ではなくサブスクに含まれる）。**Fable 5 は 2026-07-12 23:59 PT まで Claude サブスク（Pro/Max/Team）に含まれる**（7/7 終了予定が 5 日延長確定）が、週次使用上限の 50% までという制限があり、**以後は usage credits の別課金**になる — 「無料」ではない。他は従量課金で、主要モデル単価は以下（$/1M、入力/出力）：

| モデル | $/1M (in/out) | 役割 |
|---|---|---|
| Claude Fable 5 | 10 / 50（バッチ 5/25 · キャッシュヒット 1）† | ultimate-f5 default·executor · legend default · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor |
| Claude Sonnet 5 | 3 / 15（イントロ 2/10 ~2026-08-31）‡ | eco executor 代替 |
| GPT-5.6 Sol | 5 / 30（Fast モードは 12.5/75） | planner(ultimate·legend·escalation)·cyber-cop critic·executor·solo-openai |
| GPT-5.6 Terra | 2.5 / 15 | executor/critic(daily·sprint·claude-codex) |
| GPT-5.4 | 2.5 / 15 | solo-openai architect（唯一の 1M ctx レーン） |
| Grok 4.5 | 2 / 6（実効入力約 $0.84 @88% cache） | critic(v1.10) |
| Grok 4.1 Fast | 0.2 / 0.5 | eco planner |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 単一貼付けのフォールバック |
| Gemini 3.1 Pro / 3.5 Flash | サブスクトークン | planner·architect·critic |

> † Fable 5 は Opus のちょうど2倍の単価。サブスク込み分（~7/12）も週次上限を消費する。
> ‡ Sonnet 5 は**トークナイザ変更で同一テキストが約 30% 多くトークン化**される — 実効コストは表示単価より高く見積もること。
> （参考：DeepSeek 系は DeepInfra プロバイダ経由なら V4 Pro $1.30/$2.60 — [§3-3](#3-3-契約--プロバイダ)。）

**プロファイル相対コスト**

| プロファイル | コスト | 主因 |
|---|---|---|
| ultimate-f5 | ●●●●● | default·executor Fable 5 — ~7/12 サブスク込み(週次上限の 50% まで)、以後 credits $10/50 |
| legend | ●●●●● | default Fable 5(7/12 後は credits) + executor Opus `:max` |
| ultimate / escalation | ●●●●● | executor Opus `:max`/Fable `:xhigh`(救援) + planner GPT-5.6 Sol `:xhigh` |
| coding-sprint | ●●●●○ | executor Opus `:max` |
| solo-anthropic | ●●●●○ | 全役割 Opus (executor/planner `:max`) |
| daily | ●●●○○ | メインループ Opus `:medium`、委譲は中/低価格に分散 |
| monorepo | ●●●○○ | executor/architect Opus + Gemini(サブスク) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash($0.14) + サブスク Gemini |

> **3つの節約レバー**：① 委譲作業を超安価モデル（DeepSeek V4 Flash $0.14、Grok Fast $0.2）/ サブスクトークン（Gemini）へ ② 失敗時のみ effort を上げる ③ メインループ（Anthropic フラッグシップ）は品質の上限なので維持しつつ、日常は `:medium`、コスト逼迫時は `:low` — Fable default（`legend`）の credits が負担なら default を `opus-4-8:high` へ。

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

**v1.11.0** · [CHANGELOG](./CHANGELOG.md) · [保守プレイブック](./MAINTAINING.md) · ライセンス [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
