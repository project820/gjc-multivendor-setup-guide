<div align="center">

# 🧩 GJC 멀티벤더 극한 셋업

### claude · gpt · grok · gemini · opencode go — 5개 구독을 *역할별로* 쪼개 쓰는 검증된 설정

복잡한 모델 선택을 고민하지 말고, **한 줄로 설치**해 역할마다 최적 모델이 자동으로 배치되게 하라.

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-2.0.0-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/bundles-10%20·%204%20tiers-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="dream-team 셋업 — 역할별 최강 가설" width="100%">

</div>

**한국어 (이 문서) · [English](./README.en.md) · [中文](./README.zh.md) · [日本語](./README.ja.md)**

> [!NOTE]
> **이 가이드의 핵심은 GJC 공식 문서로 채택됐다** — 압축판이 [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md) 로 업스트림 머지됨([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev`). 역할·셀렉터 개념의 **정식 레퍼런스는 GJC 공식 docs**를 따르고, **이 레포는 거기 없는 것** — 원클릭 설치기, 4계층 10번들 카탈로그(`cyber-cop` reviewer 모드·Council/Escalation 워크플로 계약 포함), 그리고 [유지보수·검증 도구](./MAINTAINING.md)(정적 검증 CI + 라이브 셀렉터 배터리 + 카탈로그 드리프트 추적) — 를 제공한다.

## 🚨 `cyber-cop` — reviewer 모드 프로필

> author 모드 번들은 전부 코드를 **쓰는** 세션용이다. **`cyber-cop`은 코드를 막아서는 세션**을 위한 번들 — GJC 최초의 **reviewer 모드**다. 남의 PR을 검토하고, 반대 근거를 찾고, 머지 게이트에서 판정한다.

**무엇이 다른가**
- PR 리뷰·보안 감사에서 역할 가중치가 **반전** → **architect(1차 판정: CLEAR/WATCH/BLOCK)와 critic(머지 게이트)이 주연**, executor는 재현 PoC·failing test 조연으로 내려간다.
- critic이 **코드 작성자(Claude 가정) 대비 cross-family**(GPT-5.6 Sol) → 자기선호 편향을 구조적으로 차단([arXiv 2410.21819](https://arxiv.org/abs/2410.21819)).
- 고위험 PR·보안 감사는 **3표 병렬 패널**(`gpt-5.6-sol` · `grok-4.5` · `gemini-3.1-pro`) 독립 투표 → 2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단.

**작동 증거 — 이 레포가 스스로 검증했다**
> PR #4~#7에서 리뷰 게이트가 **머지 전 결함 10건을 차단**했다(#4: 5건 · #6: 5건 · #7: 첫 투표 통과). 리뷰 헬퍼가 *자기 자신의* prompt-injection 결함으로 BLOCK 당했고(고친 뒤 통과), 본체(Anthropic)가 자기 계열 문서를 관대히 넘긴 지점 2건(상대경로 인젝션 표면·권한 과장)을 **cross-family critic(당시 좌석 GPT-5.5 — 현행 critic 좌석은 GPT-5.6 Sol)이 정확히 BLOCK**했다. (추가로 #6 머지 후 1건이 발견돼 #7로 즉시 수정.) 자기선호-편향 방어가 실전에서 작동함을 증명한 것이다.

**클론 없이 2커맨드로 시작**
```bash
# 전제: gh CLI 설치·인증(gh auth login) + gjc 프로바이더 /login 완료
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_COP=1 bash
export PATH="$HOME/.local/bin:$PATH"   # 설치기가 PATH 경고를 출력한 경우 1회
cd <리뷰할-레포>
gjc-cop 123               # PR #123 → 4섹션 verdict (REPO는 cwd 자동 감지 — 머지는 절대 안 함)
# gjc-cop --panel 123     # 고위험: 3표 cross-family 패널
# gjc-cop shell           # 대화형 리뷰어 세션(신뢰 계약 자동 주입)
# gjc-cop watch           # 신규 PR 폴링·자동 리뷰(머지는 사람이 결정)
```
클론/수동 경로(래퍼 없이 동작 원리 그대로)는 [공지 문서 §3](./docs/whats-new-cyber-cop.md) 참조.

📖 갭 논증·사용법 3단계·자동 리뷰 파이프라인·보안 수칙 전체 → **[cyber-cop 공지 문서](./docs/whats-new-cyber-cop.md)**

### Extragoal — GPT-5.5 Pro 최종리뷰 레인 (opt-in)

GPT-5.5 **Pro** 구독자가 Pro의 심층 추론을 개발·QA·보안점검의 회전수-1 판정석에 투입하는 별도 레인. 상류 gajae-code의 extragoal 외부 리뷰 게이트를 설치 가능한 경험으로 포장한다 — **상류 기본 레인은 이것 없이도 항상 동작하고, Pro 레인은 어느 단계에서도 전제조건이 아니다.**

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | GJC_SETUP_EXTRAGOAL=1 bash
```

extragoal 스킬(상류 SHA-핀 fetch) + courier 도구 4종(무설치 수동 courier → `--check-env` 반자동 → 상주 브라우저 3단 사다리)을 배송한다. 3단 사다리·계약 매핑·지뢰 목록 전체 → **[Extragoal Maximalist 문서](./docs/extragoal-maximalist.md)**

---

## ⚡ 30초 설치 (한 줄 복붙)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

이 한 줄이 **10개 번들을 `~/.gjc/agent/models.yml` 에 안전 병합**하고 기본 프로필을 `daily` 로 설정한다. 기존 설정은 자동 백업되며, 재실행해도 깔끔히 갱신된다.

```bash
gjc --mpreset daily        # 이번 세션만 적용
gjc                        # 새 세션은 자동으로 daily 사용
```

> [!IMPORTANT]
> **설치 후 프로바이더 로그인이 필요하다.** GJC는 자체 OAuth를 쓰므로(네이티브 `agy`/`grok` CLI 로그인과 공유되지 않음), GJC를 켜고 아래를 한 번씩 실행하라(브라우저 인증):
>
> ```text
> /login anthropic           # claude
> /login openai-codex        # gpt (ChatGPT 계정 → base GPT 제공)
> /login google-antigravity  # gemini (Google AI Pro/Ultra 구독)
> /login xai                 # grok 전체 라인업 + Composer
> ```
> opencode-go 는 API 키 방식: `/provider add` 또는 환경변수 `OPENCODE_API_KEY`. 인증 상태는 `/provider` 로 확인.

> [!TIP]
> 기본 프로필 지정: `curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash` · 기본값 설정 건너뛰기: `GJC_SETUP_DEFAULT=none`.

---

## 📑 목차

1. [왜 멀티벤더인가](#1--왜-멀티벤더인가)
2. [핵심 설계](#2--핵심-설계)
3. [GJC 엔진 사실](#3--gjc-엔진-사실)
4. [벤치마크 근거](#4--벤치마크-근거)
5. [최종 카탈로그 — 10 번들 · 4계층](#5-️-최종-카탈로그--10-번들--4계층)
6. [검증 매트릭스](#6--검증-매트릭스)
7. [설치 / 제거](#7-️-설치--제거)
8. [동적 라우팅 전략](#8--동적-라우팅-전략)
9. [병렬 에이전트 + 신뢰성](#9--병렬-에이전트--신뢰성)
10. [비용](#10--비용)
11. [출처](#11--출처)

---

## 1. 🎯 왜 멀티벤더인가

claude·gpt·grok·gemini·opencode go 를 다 구독해놓고 한 모델만 쓰는 건, 매 역할에서 *차선*을 쓰는 것과 같다. 검증된 벤치마크는 **역할마다 1위 벤더가 다르다**는 걸 보여준다:

| 역할 | 무엇을 하나 | 최적 모델 |
|---|---|---|
| 🧠 **추론·설계**(planner) | 순서·수용기준 짜기 | **GPT-5.6 Sol** (Agents' Last Exam 52.7 · 2026-07-09 GA)† — 번들별 좌석은 [§5](#5-️-최종-카탈로그--10-번들--4계층) 참조(예외: cyber-cop·monorepo=Gemini, eco=Luna) |
| 🔨 **구현**(executor) | 실제 코드 작성·수정 | **Claude Fable 5** (SWE-bench Verified **95.0**) — 구독 포함 최강은 **Opus 4.8**(88.6) |
| 🔭 **코드리뷰**(architect) | 대형 리포 탐색·아키텍처 | **Gemini 3.1 Pro** (멀티모달 MMMU-Pro 81%)† · 초장문맥(>200k)은 **Opus** |
| ⚖️ **독립 비평**(critic) | 결과 적대 검증 | **cross-family** (본체와 다른 벤더) |
| 🎛️ **오케스트레이션**(default) | 도구호출·라우팅·정직성 | **Anthropic 플래그십** — Opus 4.8 (라우터 품질 = 전체 상한; `dream-team`은 Fable 5. 비-Anthropic 라우터는 opt-in `ultimate-sol`(Sol)과 Anthropic 미포함 `eco`(Terra)뿐) |

> **벤치마크 기준일: 2026-07-10** (planner 행 — GPT-5.6 Sol GA 반영). † 07-02 스냅샷: planner 축 구 1위는 Gemini 3.1 Pro(GPQA 94.3 / ARC-AGI-2 77.1)였으나 07-09 Sol GA로 세대교체 됨([§6-2](#6-2-역할-배치-최적성-검토-deep-research--실측)). architect 축은 2026-07-02 기준 유지 — Gemini 3.5 Pro(2M ctx, Deep Think) 7월 GA 연기, 출시 시 재검증 예정.

> 한 벤더로 5역할을 다 채우면 1등이 아닌 자리가 반드시 생긴다. 이 가이드는 그 5자리를 각각의 최적 벤더로 채우되, 비용·접근성·신뢰성까지 따져 **실제로 작동하는 조합**으로 정리한 결과다. v1은 3종 독립 딥리서치(GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro), v2는 2축 블라인드 독립 리서치(Claude Fable 5 Ultracode · Parallel.ai Ultra 2x, 2026-07-10)를 교차검증했으며([§6-2](#6-2-역할-배치-최적성-검토-deep-research--실측)), 셀렉터 검증 상태를 [§6](#6--검증-매트릭스)에 명시한다.

---

## 2. 🧭 핵심 설계

> **강한 본체 1개 고정 (default = Anthropic 플래그십 Opus/Fable) + 작업신호 기반 위임 + 실패신호 기반 effort 에스컬레이션.**

GJC에서 매 작업을 실제로 도는 건 `default`(본체) 하나다. executor/architect/planner/critic 은 본체가 **필요할 때만 `task`로 위임**하는 서브에이전트다(fresh-context).

<div align="center">
<img src="assets/architecture.svg" alt="본체 1개(default) + 서브에이전트 4 — 작업신호 위임" width="100%">
</div>

세 가지 설계 원칙:

- **본체는 절대 양보 불가.** median 작업의 대부분은 본체 혼자 처리하므로, 본체(default)를 약한 모델로 내리면 체감 성능 전체가 무너진다. 기본은 Anthropic 플래그십(Opus 4.8 — `dream-team`은 Fable 5). 비-Anthropic 라우터는 둘뿐: opt-in 실험 `ultimate-sol`(Sol — validator 등재+WARN)과 Anthropic 미포함 저단가 실험 `eco`(Terra — router 불변식 비적용).
- **다양성은 "검증"에서만 이득.** critic은 본체와 다른 벤더로 둬 독립성을 확보하되, 직렬 체인은 짧게 유지한다(신뢰성은 `0.99ⁿ`로 떨어진다).
- **effort는 비대칭 경제학.** `medium→high`는 점수 +1~2점에 토큰 ~23배. 무조건 `max`는 낭비 — "못 풀어서" 올리는 것만 정당.

---

## 3. 🔧 GJC 엔진 사실

### 3-1. 역할 5종

| 역할 | 실행 위치 | 1순위 역량 |
|---|---|---|
| `default` | **본체(메인 루프)** | 도구호출 신뢰성 · 정직성 |
| `executor` | 서브에이전트(`task` 위임 시만) | 실코딩(SWE-bench) |
| `architect` | 서브에이전트 | 대용량 ctx · 멀티모달 코드리뷰 |
| `planner` | 서브에이전트 | 최상위 추론 · 시퀀싱 |
| `critic` | 서브에이전트 | 독립 적대 비평 |

### 3-2. 추론등급(Effort) 치트시트

**GJC 0.9.6 실효 기준**이다(2026-07-10 실호출 배터리) — API 공식 스펙과 다른 곳이 있다(아래 각주):

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← 6단계 전부
Fable 5                 minimal low medium high xhigh       ← :max는 xhigh로 침묵 클램프 · thinking 상시-온
Sonnet 4.6 / 5          minimal low medium high              ← :xhigh/:max는 high로 침묵 클램프
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 기본 xhigh
GPT 5.6 Sol/Terra/Luna  low medium high xhigh (max)          ← :max 수용되나 심도 미검증 — 출하 상한 xhigh
Grok 4.5 (xai)          low medium high                      ← :xhigh/:max는 high로 침묵 클램프 · minimal은 네이티브 effort 아님
grok-build/grok-4.3     ── bare 셀렉터만 (effort 서픽스 미해석) ──
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go 기타         ── effort 접미사 생략(기본값) ──
google-antigravity Gemini  gemini-3.1-pro-low:high (고추론) · gemini-3.1-pro-low (저effort)
```

> [!IMPORTANT]
> **하드룰 5선**: ① Gemini Pro는 `low`/`high`만 — 고추론은 `gemini-3.1-pro-low:high` 리터럴 핀(0.9.6부터 퍼지 공간 fail-closed — 잘못된 id는 "not found") ② openai-codex ctx는 **모델별** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K** · `gpt-5.6 3종`=**373K**(0.9.6에서 272K→373K 상향; API 스펙 1.05M과 별개의 usable prompt budget) ③ Sonnet(4.6/5)은 GJC에서 `xhigh`/`max` 불가 · **Fable 5는 `max` 불가**(각각 high/xhigh로 클램프) ④ opencode-go는 `:effort` 생략(deepseek-v4 계열만 예외적으로 지원) ⑤ xai `grok-4.5` 상한은 `high`(`:xhigh` 침묵 클램프 — xhigh는 grok-build 프로바이더 전용인데 그쪽은 effort 서픽스 자체가 해석되지 않는다). 범위 밖 등급은 에러가 아니라 **클램프**된다. gpt-5.6 3종은 카탈로그에 `max`까지 뜨고 실호출도 수용되나(07-10 검증) **심도 미검증 — 이 가이드의 출하 상한은 `xhigh`**.
>
> **각주(상류 갭)**: Claude 5 패밀리는 API 공식으로는 둘 다 `max`까지 지원한다. GJC 파서(0.9.1~0.9.6)가 fable 패밀리를 몰라 폴백 추론하고 sonnet-5가 4.6 클램프를 상속하는 **엔진 쪽 갭**이며, 재현 자료와 함께 **상류에 제보됨**. 이 가이드는 GJC 실효 기준으로 기재한다.

### 3-3. 구독 → 프로바이더

| 구독 | provider-id | 비고 |
|---|---|---|
| claude | `anthropic` | 전 effort. Claude 5 패밀리(Fable 5·Sonnet 5) 포함 |
| gpt | `openai-codex` | **ChatGPT 계정 → base GPT(gpt-5.6 sol/terra/luna · 5.5 · 5.4) 제공**. ctx: gpt-5.4=1M · 5.5=272K · 5.6 3종=373K |
| grok | `xai` | 전체 라인업 + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra 구독 토큰**. Gemini + 번들 Claude(Opus 4.6 — 2026-07-02 기준, 이후 번들 구성 미재확인) |
| opencode go | `opencode-go` | API 키(`OPENCODE_API_KEY`) |

> [!NOTE]
> **openai-codex 경로 주의**: ChatGPT(Codex) 계정으로 로그인하면 **base GPT 모델(`gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5`, `gpt-5.4`)** 이 제공된다. standalone `-codex` 변종(`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex-max/mini`)은 이 경로에서 **미지원**(`not supported when using Codex with a ChatGPT account`)이라, 본 가이드는 코딩 역할도 검증된 **base GPT**로 통일한다.
>
> 대안 경로: `google-vertex`(API 키, 유료 per-token, 1M ctx) — 구독/쿼터 무관 fallback. 또 하나는 **DeepInfra**(API 키): DeepSeek V4 Pro **$1.30/$2.60**(1M ctx) · V4 Flash $0.09/$0.18 — Standard/Priority(1.5×) 티어가 GJC `service-tier` 설정과 직결된다.

### 3-4. 셀렉터 문법

```text
<provider-id>/<model-id>:<effort>            예) anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   (Gemini 고추론 — 엔진 정식 경로)
opencode-go/<model>                           (effort 생략 = 모델 기본값)
```

---

## 4. 📊 벤치마크 근거

**역할별 검증된 1위** (vals.ai 독립보드 · 공식 모델카드 기준 — **기준일 2026-07-02**)

| 역할(축) | 1위 | 수치 |
|---|---|---|
| executor (SWE-bench Verified) | **Fable 5** | **95.0%** (Opus 4.8 88.6 = **구독 포함 최강** · GPT-5.5 82.6 · Gemini 3.1 Pro 80.6) |
| planner (장기 워크플로·추론) | **GPT-5.6 Sol**† | Agents' Last Exam 52.7(5.5: 46.9) · AA Intelligence 58.9 — GPQA 단독 1위는 Sonnet 5 96.2 · 과학지식 특화는 Gemini 3.1 Pro 94.3 ([§6-2](#6-2-역할-배치-최적성-검토-deep-research--실측)) |
| architect (ctx·멀티모달) | **Gemini 3.1 Pro**† | 1M ctx · MMMU-Pro 81% |
| default (툴콜·정직성) | **Opus 4.8 / Fable 5** | 라우터 품질 = 전체 상한 (Fable은 refusal·과금 캐비앗 — [§5](#5-️-최종-카탈로그--10-번들--4계층)) |
| critic (독립성) | **cross-family** | 메타-심판 > 토론형 집계 |

> † planner 행은 **2026-07-10 기준**(GPT-5.6 Sol 07-09 GA — ARC-AGI-2 5.6 수치 미공개, 근거는 공식 평가표+AA 지수). 번들별 planner 좌석은 §5 좌석표가 진실(예외: cyber-cop·monorepo=Gemini, eco=Luna). architect 축은 Gemini 3.5 Pro 출시 시 재검증 대상(2026-07-02 기준).

**핵심 합의 원칙**

1. **default = Anthropic 플래그십(Opus/Fable) 고정** — 라우터 품질이 전체 품질 상한. 예외 둘: `ultimate-sol`(Sol 라우터 — validator 등재 + WARN 표면화 opt-in 실험) · `eco`(Anthropic 미포함 번들 — Terra 라우터, router 불변식 비적용).
2. **architect = Gemini 3.1 Pro(멀티모달) / Opus(초장문맥)** — Gemini는 비전·중간 ctx 최적, 200k+ 텍스트 실효검색은 Opus(MRCR 76%@1M, Gemini는 26%로 붕괴).
3. **critic = cross-family** — 본체/플래너와 다른 벤더여야 편향이 완화된다(self-preference bias).
4. **구조 = 강본체 + 작업신호 위임 + 실패기반 effort 에스컬레이션.**
5. **매 쿼리 프로필 스왑 ❌** — 캐시 손실 > 이득. 모드 경계에서만 스왑.

> 벤치마크는 시점 민감하다 → 분기별 재검증 권장. 절대순위는 vals.ai 독립보드로 한정.

---

## 5. 🗂️ 최종 카탈로그 — 10 번들 · 4계층

<div align="center">
<img src="assets/profiles-matrix.svg" alt="프로필 × 역할 매트릭스" width="100%">
</div>

> ★ = 평소 권장. **v2.0.0 구조 전환**: "동등한 프로필 N개"가 아니라 **user-facing 번들 10개를 4계층(tier)** 으로 나눈다 — 신뢰 등급이 같지 않다. 멀티벤더 불변식: 전 번들 `required_providers ≥ 2`(단일 벤더 수요는 GJC 0.9.6 내장 프로필 몫) · `critic=cross-family` 기본(예외는 validator `SAME_FAMILY_OK` 등재 + WARN 영구 표면화) · 전부 엔진 effort 하드룰 통과 + **셀렉터 검증 상태 추적**([§6](#6--검증-매트릭스); 2026-07-10 gjc **0.9.6** 첫 배터리 — 전 출하 셀렉터 그린).

| Tier | 번들 | 한 줄 정의 | 이럴 때 |
|---|---|---|---|
| Core | ⭐ **daily** | 본체 Opus + 위임 역할별 분산 — **구독 OAuth 3벤더만으로 activation** | **평소 기본** |
| Core | 🏎️ **coding-sprint** | executor 를 Opus 로 승격한 구현 처리량 특화 | 순수 구현 스프린트 |
| Core | 🚨 **cyber-cop** | reviewer 모드 — architect·critic 주연, PR 리뷰·보안 감사 전용 | 남의 PR 검토·머지 게이트·보안 감사 |
| Premium (exp) | 🏆 **ultimate-opus** | Anthropic 품질 기저 프리미엄 (구 `ultimate` 후계) | 정확성이 비용보다 중요 |
| Premium (exp) | 🧪 **ultimate-sol** | Sol 기저 프리미엄 — agentic/터미널/브라우징 축. **Anthropic 보유 번들 중 유일한 비-Anthropic default**(validator 예외; eco 는 Anthropic 자체가 없음) | 장기 자율 워크플로 실험 |
| Premium (exp) | 🔥 **dream-team** | 역할별 최강 가설 — Fable default+executor (구 `ultimate-f5`/`legend` 후계) | 최고 품질, credits 각오 |
| Workflow | 🏛️ **llm-council** | 4계열 좌석표(판정석은 Google·xAI·OpenAI 3계열 — **본체 Anthropic 은 집계자 제한**) — 투표·quorum 은 routing-rules 의 Council 계약이 실행 | 다계열 합의가 필요한 결정 |
| Workflow | 🛡️ **escalation** | 수동 에스컬레이션 — Fable 구원투수 + critic 3표 패널 | 머지·보안·결제·비가역 변경 |
| Specialized (exp) | 💸 **eco** | 멀티벤더 저단가 실험 — *절대 최저가 아님*(최소 의존 저가는 내장 `codex-eco`) | 비용 압박·대량 작업 |
| Specialized (exp) | 🗺️ **monorepo** | 전역 ≥1M ctx (gpt-5.5 272K/5.6 373K 배제) | 거대 코드베이스 |

**v1.11.0 → v2.0.0 마이그레이션**: `ultimate`→`ultimate-opus` · `ultimate-f5`/`legend`→`dream-team` · `solo-anthropic`/`solo-openai`/`claude-codex`/`claude-codex-max` → **삭제** — 단일·2벤더 수요는 GJC 0.9.6 내장 프로필(`claude-opus`/`claude-fable`/`codex-*`/`opus-codex`/`fable-opus-codex`)이 흡수한다(매핑 등가가 아니라 use-case 흡수). `llm-council`·`ultimate-sol` 신설.

<details>
<summary><b>📋 전체 YAML 펼치기 (gjc-profiles.yml 와 동일 — 모델 매핑 기준, 주석의 §참조만 README에 맞춤)</b></summary>

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
      critic:    google-antigravity/gemini-3.1-pro-low:high     # v2: grok→Gemini — xai 키 장벽 제거(구독-only daily) + 본체(Opus)와 cross-family 유지(PR #21 패널 반영). ⚠architect 와 동일 셀렉터 — 3벤더 구독-only 제약에서 본체교차+plan/crit교차를 동시에 만족하는 계열이 Google 뿐(의도적 수용). 독립성 강화 원하면 xai 로그인 후 critic 을 xai/grok-4.5:medium 으로 스왑(구 v1.11 좌석)

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

  ultimate-sol:                        # 🧪 OpenAI(Sol) 기저 프리미엄 — agentic/terminal/브라우징 축. Anthropic 보유 번들 중 유일한 비-Anthropic default(validator 예외; anthropic 미포함 eco 는 불변식 비적용)
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

  llm-council:                         # 🏛 4계열 좌석표(판정석은 Google·xAI·OpenAI 3계열, 본체 Anthropic 은 집계자 제한 — 자기선호 격리). ★프로필은 좌석표일 뿐 — 병렬 독립호출·quorum·raw verdict 보존은
    required_providers: [anthropic, openai-codex, google-antigravity, xai]   #   routing-rules.md "Council 계약"이 실행한다(YAML 이 자동 실행하지 않음)
    model_mapping:
      default:   anthropic/claude-opus-4-8:high                 # 집계자 제한 — 요약·은폐 없이 raw verdict 보존
      executor:  openai-codex/gpt-5.6-terra:high                # 재현·검증 잡무
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 의제 분해
      architect: google-antigravity/gemini-3.1-pro-low:high     # council 판정석 1 (Google)
      critic:    xai/grok-4.5:high                              # council 판정석 2 (xAI)

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
> **opencode-go** 는 `OPENCODE_API_KEY` 설정 시 `eco`(executor)·`monorepo`(critic)에서 활성화된다(검증✅). grok 구독(SuperGrok)의 `xai/grok-composer-2.5-fast`(200k)도 검증됨 — throughput용 대안. 다른 opencode-go 모델(qwen3.7-max·kimi-k2.6·glm-5.1·minimax-m2.7·mimo-v2.5)도 전부 동작 확인. 신규 입점(미검증 후보): **kimi-k2.7-code**(버짓 executor 유력) · **minimax-m3**(512K 멀티모달 — 카탈로그 실측치, `2026-07-10-catalog-gjc096.txt`).

#### 프로필별 설계 근거

- **daily** — 본체 Opus `:medium`(효율 knee), 구현은 코딩특화 `gpt-5.6-terra`($2.5/15에 ≈GPT-5.5급), 분해는 장기 워크플로 1위 `gpt-5.6-sol:high`(v2: gemini→sol — Agents' Last Exam 52.7), 설계·리뷰와 비평은 Gemini `-low:high`(v2: critic grok→gemini — **xai 키 장벽 제거로 구독 OAuth 3벤더만으로 activation** + 본체(Anthropic)와 cross-family 유지; Grok critic 은 defect-recall 직접근거 0건이라 diversity 좌석은 프리미엄 계열로 이동). ⚠architect·critic 이 동일 셀렉터 — 3벤더 구독-only 제약에서 본체교차+plan/crit교차를 동시에 만족하는 계열이 Google 뿐이라 의도적으로 수용(독립성 강화가 필요하면 xai 로그인 후 critic 을 `grok-4.5:medium`으로 스왑 — 구 v1.11 좌석). 일상 작업의 품질/비용 균형점.
- **coding-sprint** — executor 주연(Opus `:high` — v2: `:max` 상시 대신 실패신호 시에만 격상, [§8-2](#8-2-적응형-effort-에스컬레이션)), planner 는 `gpt-5.6-sol:high`(v2: gemini→sol — 스프린트 분해는 Sol 축), critic은 *코딩을 아는* `gpt-5.6-terra`로 실버그를 잡는다. ⚠planner/critic 이 같은 gpt 계열 — 인간 판정(2026-07-10)으로 `SAME_FAMILY_OK` 등재(모델은 Sol≠Terra 분리, 번들 전체는 3벤더).
- **cyber-cop** — 🚨 **reviewer 모드**: author 모드(default+executor 가중)의 역상. 리뷰 세션에선 역할 가중치가 반전된다 — executor는 재현 PoC·failing test용 조연으로 내려가고, **architect(1차 코드리뷰 판정자)와 critic(머지 게이트)이 주연**이 된다. architect=Opus `:high`(1M 실효검색 76% vs Gemini 26% 붕괴 — 200k+ diff 통독), critic=`gpt-5.6-sol:high`(Claude-작성 코드와 cross-family — 자기선호 편향 완화, arXiv [2410.21819](https://arxiv.org/abs/2410.21819)). 고위험 PR·보안 감사는 critic 3표 패널(§9 규칙 — 독립 투표, 토론 금지, 2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단; 3표째 grok은 xai 로그인 시 — 그래서 xai는 `required_providers`에 없고, 미보유자도 2표 {gpt-5.6-sol, gemini}로 provenance 최소치를 지키며 운영 가능). 운영 규칙(위임 순서·증거 계약·집계자 제한·provenance fallback·LGTM 금지)은 [`routing-rules.md`](./routing-rules.md)의 리뷰어 계약 참조. `escalation`과의 차이: escalation은 author-side 게이트(고쳐서 통과), cyber-cop은 reviewer-side(반대 근거 탐색). v1.11.0 매핑 그대로(KEEP).
- **ultimate-opus** — 🏆 Anthropic 품질 기저 프리미엄(구 `ultimate` 후계). default·executor·architect 를 Opus `:high`로 통일해 안정성·1M·구독 한계비용을 취하고, 교차검증은 **Sol planner `:xhigh` + Grok critic `:high`** 가 담당한다. ⚠executor/architect 동일 claude 계열 — 인간 판정 `SAME_FAMILY_OK`(WARN 영구 표면화). Opus 3좌석은 "세 독립 의견"이 아니다 — council 품질을 암시하지 말 것.
- **ultimate-sol** — 🧪 Sol 기저 프리미엄(experimental). Sol이 검증 우위인 축 — 장기 워크플로 완주(Agents' Last Exam 52.7)·터미널(T-B 2.1 88.8 SOTA)·브라우징(BrowseComp 90.4)·컴퓨터 사용(OSWorld 62.6) — 에 default/executor/planner 3좌석을 몰아준다. **Anthropic 보유 번들 중 유일한 비-Anthropic default**(validator `NON_ANTHROPIC_DEFAULT_OK` 등재 — WARN 표면화; Anthropic 미포함 `eco`의 Terra 라우터는 불변식 자체가 비적용). 트레이드오프 명시: 라우터 ctx **373K**(Opus 1M 대비)·툴사용 축 열세(Toolathlon 58 vs Fable 61.7)·⚠METR의 SWE 게이밍 적발(SWE류 단독근거 금지). OpenAI 3좌석 자기강화는 Opus architect + Grok critic 이 완충. role-fit L3 전까지 experimental.
- **dream-team** — 🔥 역할별 최강 *가설*(구 `ultimate-f5`/`legend` 후계). **Fable 5 = default+executor**(SWE-Bench Pro 80.0 — OpenAI 자사표의 자기불리 인정 · FrontierMath T4 87.8), 분해는 Sol `:xhigh`, 설계리뷰는 Opus `:high`(1M), 비평은 제3계열 Grok. Fable 캐비앗 3종 세트: ① 구독 포함 이벤트 ~7/12 23:59 PT(이후 **usage credits $10/$50** — default+executor 2좌석이라 노출 최대) ② refusal 이 HTTP 200+`stop_reason:refusal` 로 옴 ③ 30-day retention·ZDR 불가. ⚠executor(Fable)/architect(Opus) 동일 claude 계열 — 인간 판정 `SAME_FAMILY_OK`(모델 분리 + Sol/Grok 교차검증).
- **llm-council** — 🏛 4계열 좌석표(Anthropic·OpenAI·Google·xAI). **판정석은 Google(Gemini)·xAI(Grok)·OpenAI(Sol/Terra) 3계열이고, 본체 Anthropic(Opus)은 집계자 제한** — 자기선호 편향 격리를 위해 본체는 판정에 참여하지 않고 raw verdict 를 보존·노출만 한다(4계열 "합의"가 아니라 "3계열 판정 + 제4계열 집계"). **프로필 활성화만으로 council 은 시작되지 않는다** — 병렬 독립호출·상호 비공개·raw verdict 보존·quorum(CRITICAL/HIGH dissent 비다수결)은 [`routing-rules.md`](./routing-rules.md)의 **Council 계약**을 본체가 실행해야 발생한다. 벤더 수 ≠ 독립 표 수(오류 상관) — 표 산술로 확신을 부풀리지 않는다.
- **escalation** — 🛡 **수동** 에스컬레이션(실패 자동 감지 아님 — 트리거·재시도 예산·human gate 는 routing-rules 의 Escalation 계약). 실패 신호가 뜬 작업에 **최강 실행자 Fable 5 `:xhigh`를 구원투수로 투입** — 간헐 사용이라 credits 과금과도 궁합이 맞다. critic은 멀티벤더 3표 패널([§9](#9--병렬-에이전트--신뢰성)). Fable refusal 시 executor 를 Opus `:max`로 강등하고 사람에게 보고. 되돌릴 수 없는 변경 전용. v1.11.0 매핑 그대로(KEEP).
- **eco** — 💸 멀티벤더 저단가 *실험* — **절대 최저비용이 아니다**(최소 의존 저가 경로는 GJC 0.9.6 내장 `codex-eco`). v2 전면 재편: default `gpt-5.6-terra:medium`(anthropic 미포함 번들이라 router 불변식 비적용), executor 최저가 `deepseek-v4-flash`($0.14/0.28), planner `gpt-5.6-luna:medium`(v2: `grok-4-1-fast`는 **2026-05-15 retire — legacy slug 는 grok-4.3 요율 redirect 과금**(xAI 공식 migration 문서)이라 퇴출), architect Gemini `-low:high` 리터럴 핀, critic `gemini-3-flash:low`(v2: `gemini-3.5-flash-low`가 07-10 오후 라이브에서 소멸 — [§6](#6--검증-매트릭스)) — executor(opencode-go)와 cross-family. xai·anthropic 키 불필요(3벤더).
- **monorepo** — 🗺 전 역할이 1M ctx. `gpt-5.5`(272K)·`gpt-5.6 3종`(373K)은 배제 — gpt-5.4는 1M이지만 Opus가 동급 이상. architect=**Opus**(1M 실효검색 1위 **76%@1M** — Gemini는 26%로 붕괴), critic=**`glm-5.2`**(cross-family, 대안 `deepseek-v4-pro`). **1M nominal window ≠ 완전 recall** — 거대 입력은 한 메시지에 통째로 붓지 말고 **청크로 나눠 멀티턴 누적**([§6-3](#6-3-잔여-공백-검토-gap-13--gjc-실효-컨텍스트-실측)) — 단일 메시지 >~400k paste만 `opencode-go/deepseek-v4-pro`로. v1.11.0 매핑 그대로(KEEP).

**삭제된 프로필의 행선지** — `solo-anthropic`/`solo-openai`(단일 벤더)와 `claude-codex`/`claude-codex-max`(2벤더 고정 믹스)는 v2 멀티벤더 카탈로그 원칙(혼합 구독 콜라보레이션 — 인간 판정 2026-07-10)에 따라 퇴출됐다. GJC 0.9.6 내장 프로필이 해당 use-case 를 흡수한다: 단일 Anthropic → 내장 `claude-opus`/`claude-fable`, 단일 Codex → 내장 `codex-eco`/`codex-medium`/`codex-pro`, Claude+Codex 2벤더 → 내장 `opus-codex`/`fable-opus-codex`(0.9.6에서 GPT-5.6 계열로 갱신됨). 내장 매핑은 이 가이드 구판과 byte-identical 하지 않다 — 세부 좌석이 중요하면 구판 YAML(`git show v1.11.0:gjc-profiles.yml`)을 로컬 커스텀으로 유지하라.
---

## 6. ✅ 검증 매트릭스

> 2026-07-10(gjc **0.9.6** — 당일 0.9.5→0.9.6 업그레이드 후 재배터리)에 전 프로바이더 핵심 셀렉터를 `gjc -p --no-session --no-tools --model <sel> "..."` 로 **실제 호출**해 재검증했다(`evidence/2026-07-10-selectors-rerun-3.md`; 0.9.5 그린 기록은 rerun-2) — **v2 출하 셀렉터 전 좌석 그린**. 이 배터리에서 antigravity 라이브 표면의 당일 드리프트(아래 WARNING)를 잡아 eco.critic 을 교체했다. "동작함"의 근거는 추정이 아니라 실호출 증거다.

| 프로바이더 | 검증된 셀렉터 (✅ 동작) |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh`(**07-10 rerun✅** — `:max`는 xhigh로 침묵 클램프) · `claude-sonnet-5:high`(07-10✅ — `:max`는 high로 침묵 클램프) · `claude-opus-4-8:high`(07-10✅, low·medium·max 07-02✅) · `claude-sonnet-4-6:high`(07-10✅) — 07-09 rate-limit 해제, 전 좌석 재검증 완료 |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh`(**07-10✅**) · `gpt-5.6-terra:high`/`:xhigh`(07-10✅) · `gpt-5.6-luna:high`(07-10✅) · 3종 `:max` 수용되나 심도 미검증(미출하) · `gpt-5.5:high`(07-02✅, v1.11에서 프로필 은퇴—카나리 유지) · `gpt-5.4:high`(1M ctx 레인) |
| `xai` | `grok-4.5:medium`/`:high`(07-10✅ — `:xhigh`/`:max`는 high로 침묵 클램프; xai 전용, provider 500K/GJC 222K floor, $2/$6) · `grok-4-fast:high`(07-10✅) · ⚠`grok-4-1-fast:high`는 호출은 성공하나 **xAI 가 2026-05-15 retire — grok-4.3 요율 redirect 과금**(v2에서 퇴출) · `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3`(**bare 셀렉터만** — effort 서픽스 미해석, 07-02✅. SuperGrok OAuth) |
| `google-antigravity` | `gemini-3.1-pro-low`(±`:high`, 07-10✅) · `gemini-3-flash`(±`:low`, **07-10✅ — v2 eco.critic**) · ⚠0.9.6부터 퍼지 공간 **fail-closed**: `gemini-3.1-pro-high`/`-bogus`는 "not found"(0.9.5의 침묵 -low 해석 함정 재현 안 됨 — 핀은 유지) · ⚠**라이브 표면 당일 드리프트**: `gemini-3.5-flash-low`/`-extra-low`/`gemini-pro-agent` 07-10 오후 소멸("not found" — `--list-models` 표기와 불일치, 실호출이 진실) |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro`(07-02 재검증✅) · `glm-5.2`(**0.7.10 번들 편입**, 07-02✅) · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` (`OPENCODE_API_KEY` 필요) |

> [!WARNING]
> **이 환경에서 동작하지 않은 셀렉터**(피하라): `openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`(ChatGPT 계정 미지원) · `google-antigravity/gemini-3.1-pro-high`·`gemini-3.5-flash-low`·`gemini-3.5-flash`·`gemini-pro-agent`(**0.9.6/07-10 오후 기준 "not found"** — 고추론은 `gemini-3.1-pro-low:high`, 경량 Gemini 는 `gemini-3-flash:low`) · `gemini-3-pro`(은퇴) · `claude-sonnet-4-6-thinking`(404) · `gpt-oss-120b`(500). `opencode-go/*` 는 `OPENCODE_API_KEY` **미설정 시에만** 실패한다(키 설정 후 위 표대로 동작). 참고: `fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.5:xhigh/max` 는 실패가 아니라 **침묵 클램프**다([§3-2](#3-2-추론등급effort-치트시트)) — gpt-5.6 3종의 `:max`는 수용되나 심도 미검증(미출하).

> [!NOTE]
> `opencode-go/glm-5.2` 는 **0.7.10부터 번들 카탈로그에 편입**됐다(구 "라이브 카탈로그 전용" 캐비앗 폐기). antigravity 라이브 표면은 당일에도 변한다(07-10 오후 `gemini-3.5-flash*` 소멸 실측) — `--list-models` 는 캐시된 표기를 보여줄 수 있으니 **좌석 채택 전 실호출로 확인**하라. 디스커버리 미갱신 상태에선 `selector did not resolve` 로 활성화가 실패할 수 있다 — 재로그인/재시도로 카탈로그를 갱신하거나 번들 id로 대체하라(eco critic 대안: `opencode-go/deepseek-v4-pro`, GLM 은 `zai/glm-5.2` — `zai` 를 `required_providers` 에 추가).

**지연 참고** (마이크로벤치 2026-07-02; Grok 4.5 행만 2026-07-09 streaming bench):

| 셀렉터 | 코딩 | 추론 | 비고 |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **전체 최속** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | 코딩에서 sonnet-5 대비 +3~4s |
| `grok-4.5:medium` / `:high` | ~14s / ~50s | TTFT ~13s / ~48s | 2026-07-09 streaming bench; high는 고위험 critic 전용 |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | 코딩 지연 아웃라이어 |
| `glm-5.2` | **21.9s** | 4.0s | 코딩 최저속 — critic엔 무방 |

재현:
```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
```

---

### 6-2. 역할 배치 최적성 검토 (deep-research + 실측)

초기 8프로필(v1.0 기준)의 역할→모델 배치를 다회차 deep-research(독립 벤치 검증)와 라이브 추론 프로브로 재검토한 결과, 골격은 near-optimal로 확인됐다. **v2.0.0 은 여기에 2축 블라인드 독립 딥리서치(Claude Fable 5 Ultracode + Parallel.ai Ultra 2x, 2026-07-10)를 추가**해 10-bundle 4계층 구조로 재편했다 — 두 축의 공통 결론: 출시 상태·역할 축 배치는 지지(SUPPORT), profile/workflow 경계·tier 라벨·strict provider 마찰은 수정(REVISE). Premium 3종의 role-fit L3 실측은 잔여 과제로 남긴다(experimental 라벨의 이유).

- **`gemini-3.1-pro-low:high` 는 저하 모드가 아니다.** `thinkingLevel`은 별도 모델 변종이 아니라 동일 Gemini 3.1 Pro에 적용되는 per-request 파라미터이고 모델 기본값이 **HIGH**다. 공식 모델카드의 헤드라인 추론 점수(GPQA 94.3 · ARC-AGI-2 77.1)는 전부 *Thinking (High)* 에서 측정됐다 — 이 셀렉터는 **네이티브 고추론 기본모드**를 호출한다. 실측 프로브: `low`(18s) → `low:high`(22s) 지연 증가로 thinking 활성 확인, 표준 추론 정답은 GPT-5.5·Opus와 동일. *(잔여: GJC `:high` override의 네이티브 HIGH 매핑은 1차 출처 미확증 → 운영 중 추론 품질 모니터링 권장.)*
- **planner 추론 축은 분열한다.** GPQA Diamond(과학지식)는 상위권이 93~96%로 *saturated* — 단독 1위는 이제 **Sonnet 5(96.2)**, Gemini 3.1 Pro 94.3. ARC-AGI-2(추상·유동추론)는 **GPT-5.5가 명확히 앞선다**(0.850 vs 0.771; Fable 5는 미공개 — 추론 축 우위 미입증). 플래닝에 더 직결되는 유동추론(ARC) 기준 → ultimate/escalation planner=GPT 유지. **과학지식추론 비중이 크면 `planner → google-antigravity/gemini-3.1-pro-low:high`로 swap.** *(갱신 2026-07-10: GPT-5.6 Sol GA — 공식 평가 전면 우위(Agents' Last Exam 52.7 vs 46.9 · AA Intelligence 58.9 vs 54.8) + 동가 $5/$30 → v1.11에서 planner를 `gpt-5.6-sol:xhigh`로 세대교체. ARC-AGI-2의 5.6 수치는 미공개 — 축 근거는 공식 평가표+AA 지수. 근거: [evidence/2026-07-10-gpt-5.6-notes.md](./evidence/2026-07-10-gpt-5.6-notes.md).)*
- **executor 축은 v1.4에서 교체됐다.** **Fable 5가 SWE-bench Verified 95.0 / SWE-Bench Pro 80.0으로 신 1위**(Opus 4.8 88.6 · GPT-5.5 82.6; Pro 80.3은 별도 열의 Mythos 5 — [errata E1](./evidence/2026-07-10-errata.md)). Opus 4.8은 "구독 포함 코딩 최강"으로 유지 — Fable 5는 7/12 이후 usage credits 과금이라 상시 executor로는 비용 구조가 다르다(`dream-team`/`escalation`에서만 채용). 터미널·에이전틱 축은 이제 **GPT-5.6 Sol이 SOTA**(Terminal-Bench 2.1 88.8) — 단 ⚠METR이 Sol의 SWE 평가 게이밍(역대 최고 비율)을 적발해 SWE류 점수는 할인해서 읽을 것. daily executor는 동가 후계 `gpt-5.6-terra`.
- **xAI `grok-composer-2.5-fast`·`grok-code-fast-1` 은 eco·throughput 전용.** 독립 벤치 미공개/인플레이션으로 프론티어 코더가 아니며 grok-code-fast-1은 은퇴 예정 — executor 코어 비포함이 맞다.
- **default = Anthropic 플래그십.** Opus 4.8은 Vals Index 종합(서빙 모델 중 1위)으로 재확인. Fable 5 default(`dream-team`)는 품질 상한을 한 단계 더 올리지만 refusal 분류기·credits 과금 캐비앗을 동반한다([§5](#프로필별-설계-근거)). `ultimate-sol`의 Sol 라우터는 opt-in 실험(WARN 표면화).
- **architect 장문맥 정정**: Gemini의 명목 1M은 실효 1M이 아니다 — MRCR v2 8-needle 128K 84.9% → 1M **26.3%** 붕괴, 반면 **Opus 4.6은 1M 76% 유지**(4.8 수치는 미공개). Grok 4.3 멀티모달은 12/16 하위권이라 비전 architect엔 부적합 → **monorepo architect를 Grok→Opus로 교정**했고, 표준 프로필 architect=Gemini는 멀티모달·중간 ctx 한정 최적이다. (후계자 임박: Gemini 3.5 Pro 2M ctx·Deep Think — 7월 GA로 연기, 출시 시 `{low,high}` 클램프 룰 재검증.) (GJC 경유 실효 상한은 [§6-3](#6-3-잔여-공백-검토-gap-13--gjc-실효-컨텍스트-실측) 참조.)

> 출처: [vals.ai GPQA](https://www.vals.ai/benchmarks/gpqa) · [vals.ai SWE-bench](https://www.vals.ai/benchmarks/swebench) · [vals.ai MMMU](https://www.vals.ai/benchmarks/mmmu) · [Gemini 3.1 Pro card (MRCR)](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini thinking docs](https://ai.google.dev/gemini-api/docs/thinking) · [Opus 4.6 (MRCR 76%@1M)](https://www.anthropic.com/news/claude-opus-4-6) · [long-context 보드](https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/) · [llm-stats ARC-AGI-2](https://llm-stats.com/benchmarks/arc-agi-v2) · [xAI Composer 2.5](https://x.ai/news/composer-2-5)

> 📑 **전체 리서치 리포트 (1차 출처 인용 포함)** — 이 배치 근거의 원문 3종: [딥리서치 벤치마크](./evidence/2026-07-03-deep-research-benchmarks.md) · [컨설턴트 리포트](./evidence/2026-07-03-consultant-report.md) · [통합 최종 리포트](./evidence/2026-07-03-ultimate-final-report.md). "왜 이 모델셋업인가"의 근거 전문·council 합의·확정 답변(Grok=critic / Composer Fast≠executor)이 여기에 있다. 발행 리포트는 verbatim 보존되며 정정은 **[errata](./evidence/2026-07-03-errata.md)** 로 배송된다(현재 E1: Composer 74.7→54.0은 SWE-bench **Pro** 수치 — 최종 리포트 표의 Verified 열 오배치 정정).

---

### 6-3. 잔여 공백 검토 (gap 1~3 · GJC 실효 컨텍스트 실측)

Opus 4.8은 GJC에서 **1M 컨텍스트 윈도우를 정상 지원**한다(멀티턴 누적 — 상태바 `◫ %/1M` 확인). 아래 표는 그와 **별개로**, 거대 컨텍스트를 **단일 메시지(`@파일`)로 한 방에** 주입할 때의 입력 크기 한도 실측이다(3-needle 멀티홉 검색 기준) — 윈도우 한도가 아님:

| 토큰(단일요청) | Opus 4.8 | Gemini 3.1 Pro | Grok 4.3 / 4-fast | DeepSeek V4 Pro |
|---|:---:|:---:|:---:|:---:|
| ~130k · 250k · 350k | ✅ | ✅ | ✅ | ✅ |
| ~476k | 🔴 400 | 🔴 400 | ✅ (89s) | ✅ (36s) |
| ~857k | 🔴 | 🔴 | 🔴 400 | — |

- **gap1 — Grok 2M architect swap: ❌ 기각.** 독립 벤치(Context Arena MRCR v2)에서 Grok은 deep-bin 검색이 **최하위**(grok-4.20 256–512k 0.117), 2M bin은 어떤 보드에도 없고 grok-4-fast의 2M은 측정된 검색 점수가 0(마케팅/훈련 주장). 실측도 857k에서 400. → "1M 초과는 grok-4-fast(2M)" 가정 폐기.
- **gap2 — Opus 4.8 장문맥:** Opus 4.8은 **GJC에서 1M 컨텍스트 윈도우를 지원**한다(멀티턴 agentic 파일읽기로 1M까지 정상 누적). 위 표의 ~400k 400은 **윈도우 한도가 아니라 단일 메시지(`@파일`) 입력 크기 한도**다. (참고: 공개된 MRCR 76%@1M은 Opus 4.6 수치, 4.8은 미공개.) → monorepo architect=**Opus 유지**(1M ctx 정상, 검색 최상위). 단 **한 메시지에 >~400k 토큰을 통째로 paste**하는 드문 경우만 `opencode-go/deepseek-v4-pro`로(단일 메시지 476k 실수용 확인).
- **gap3 — GLM-5.2 vs DeepSeek:** eco executor=**DeepSeek V4 Flash 유지**(GLM-5.2 $1.40/$4.40 = 입력 10×·출력 15×, eco엔 과함). **monorepo critic은 `opencode-go/glm-5.2`로 업그레이드**(실호출 검증✅) — 신규 오픈웨이트 1위(AA Index 51; DeepSeek V4 Pro 52→**44 하락**), cross-family 독립 유지, opencode-go 구독 내 서빙이라 한계비용 낮음. (저가 우선 시 `deepseek-v4-pro`로 되돌리면 됨.)

> 핵심: Opus 4.8 컨텍스트 윈도우는 GJC에서 **1M 정상**(멀티턴 누적). 단일 메시지로 한 방에 넣을 수 있는 양만 ~400k(Opus/Gemini) — 그 이상 **단일 paste**는 Grok/DeepSeek이 견고하다(실측). **거대 입력은 한 메시지에 통째로 붓지 말고 청크로 나눠 누적하면 1M 윈도우를 그대로 활용**할 수 있다. (이 표는 GJC 내부에서 독립 재검증 통과 — 20/20 일치, 실측일 2026-06-18.) 출처: [Context Arena](https://contextarena.ai/) · [GLM-5.2 (AA)](https://artificialanalysis.ai/models/glm-5-2) · [Opus 4.8 what's-new](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)

---

## 7. 🛠️ 설치 / 제거

### 원클릭 (권장)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

설치기가 하는 일: `~/.gjc/agent/models.yml` 에 10개 번들 안전 병합(재실행 시 자동 갱신 — v1.x 관리 블록의 구 프로필은 교체됨) · 기존 파일 자동 백업 · 기본 프로필 `daily` 설정. `curl` + `python3` 만 있으면 된다.

```bash
# 옵션
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash  # 기본 프로필 지정
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash        # 기본값 설정 건너뜀
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash    # 에이전트 경로 override
```

### 프로바이더 인증 (필수)

설치는 프로필만 깐다. GJC를 켜고 각 벤더에 한 번씩 로그인하라:

```text
/login anthropic           # claude
/login openai-codex        # gpt(base GPT)
/login google-antigravity  # gemini (Google AI Pro/Ultra 구독)
/login xai                 # grok 전체 라인업 + Composer
```

opencode-go 는 `/provider add` 또는 환경변수 `OPENCODE_API_KEY`.

### 수동 설치 / 검증 / 제거

[`gjc-profiles.yml`](./gjc-profiles.yml) 의 `profiles:` 블록을 `~/.gjc/agent/models.yml` 의 `profiles:` 아래에 붙여넣고 `gjc --mpreset daily --default`.

```bash
gjc --list-models daily                       # 적용 확인
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # 되돌리기(백업 복원)
```

> [!WARNING]
> **GJC 0.7.10~0.9.1 프리셋 rename/delete 주의**: 엔진의 커스텀 프리셋 rename/delete 기능은 `models.yml` 의 **주석을 전부 제거**한다 — 설치기의 관리 블록 센티널(주석)도 함께 사라져 이름 기반 교체로 격하되고, **사용자가 삭제한 프로필이 재설치 시 부활**할 수 있다(재현 확인). rename/delete 를 쓴 뒤 재설치할 땐 결과를 꼭 확인하고, 완전 제거는 백업 복원(`cp … .bak-*`)이 가장 확실하다. (0.9.6에서는 미재검증 — 재현 확인은 0.7.10~0.9.1.)

---

## 8. 🔀 동적 라우팅 전략

> **"쿼리마다 프로필 교체" ❌ / "강본체 1개 + 가벼운 룰 1겹" ✅.** 라우팅 주체는 본체(Anthropic 플래그십), 프로필은 목적지 풀이다.

> [!TIP]
> 아래 라우팅 룰을 본체가 따르게 하려면 [`routing-rules.md`](./routing-rules.md) 를 프로젝트 `AGENTS.md` 에 넣거나 `gjc --append-system-prompt @routing-rules.md` 로 주입하라(설치된 프로필 + 검증된 셀렉터 하드룰 + GJC 실효 ctx 상한까지 한 파일에 포함).

### 8-1. 작업신호 → 위임

<div align="center">
<img src="assets/routing-tree.svg" alt="작업신호 → 위임 라우팅" width="100%">
</div>

규칙: **위임은 신호가 명확할 때만.** 본체가 직접 할 수 있으면 직접.

### 8-2. 적응형 effort 에스컬레이션

<div align="center">
<img src="assets/effort-ladder.svg" alt="적응형 effort 에스컬레이션" width="100%">
</div>

- ✅ 못 풀어서 올리는 건 정당 / ❌ "올리면 안전하겠지"는 낭비.
- Minimal 금지. 저점은 `low`까지. Gemini는 `low↔high` 단일 점프.

### 8-3. 프로필 스왑 (모드 경계에서만)

| 신호 | 스왑 → |
|---|---|
| 세션 시작·일반 작업 | `daily` |
| 순수 구현 스프린트 | `coding-sprint` |
| 머지/릴리즈 직전·보안·결제 | `escalation` (수동 트리거 — routing-rules 의 Escalation 계약) |
| PR 리뷰·보안 감사 세션 | `cyber-cop` |
| 다계열 합의가 필요한 결정 | `llm-council` (+ routing-rules 의 Council 계약) |
| 정확성 최우선 (opt-in premium) | `ultimate-opus` / `ultimate-sol`(Sol 축 실험) / `dream-team`(Fable·credits 각오) |
| 대량 리팩터·마이그레이션 | `eco` |
| 거대 코드베이스 진입 | `monorepo` |
| 단일 벤더로만 운영 | GJC 내장 프로필(`claude-opus`·`codex-*` 등 — 이 카탈로그 밖) |

---

## 9. 🧪 병렬 에이전트 + 신뢰성

직렬 핸드오프는 신뢰성이 `0.99ⁿ`로 떨어지고, 멀티에이전트는 잘못 묶으면 "false consensus"로 굳는다. 병렬 설계는 이 둘을 방어하도록 짠다.

```text
직렬 체인 5단계(각 0.99):  0.99^5 ≈ 95.1%    → 길수록 붕괴
병렬 독립 5개(OR 성공):    1-(0.01)^5 ≈ 100%  → 다양성이 신뢰성을 높인다
```

**설계 원칙**
- critic은 **본체와 다른 벤더로, 병렬 독립 투표 후 본체가 집계**(debate 금지 — 메타-심판이 우월).
- critic 패널 예: `{openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high, google-antigravity/gemini-3.1-pro-low:high}` 동시 → 2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단. **CRITICAL/HIGH dissent 는 다수결로 기각 불가** — 해소 또는 human gate.
- executor fan-out은 **작업이 진짜 독립**(공유 상태 없음)일 때만.
- 체인은 짧게, 본체를 단일 진실원천으로(서브끼리 직접 합의 금지).

---

## 10. 💰 비용

Gemini(`google-antigravity`)는 **무료 공개 프리뷰 + Google AI Pro/Ultra 구독 시 한도 상향**으로 동작한다(per-token 청구 아님 — [Antigravity plans 공식 문서](https://antigravity.google/docs/plans), 2026-07-10 확인). **Fable 5는 2026-07-12 23:59 PT까지 Claude 구독(Pro/Max/Team)에 포함**(7/7→7/12 연장 — 공식 1차 연장 페이지는 미확보, 복수 2차 보도 기준)되나 주간 사용 한도의 50% 상한이 걸리고, **이후엔 usage credits 별도 과금**이다 — "무료"가 아니다. 나머지는 per-token 과금이며, 주요 모델 단가는 다음과 같다($/1M, 입력/출력):

| 모델 | $/1M (in/out) | 역할 |
|---|---|---|
| Claude Fable 5 | 10 / 50 (배치 5/25 · 캐시 히트 1)† | dream-team default·executor · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor 기간산업 |
| Claude Sonnet 5 | 3 / 15 (인트로 2/10 ~2026-08-31)‡ | eco executor 대안 |
| GPT-5.6 Sol | 5 / 30 (Fast 모드는 12.5/75) | planner(daily·sprint·ultimate-opus·dream-team·council·escalation) · ultimate-sol 3좌석 · cyber-cop executor·critic |
| GPT-5.6 Terra | 2.5 / 15 | daily executor · coding-sprint critic · llm-council executor · eco default |
| GPT-5.6 Luna | 1 / 6 | eco planner (v2 신규 채용) |
| Grok 4.5 | 2 / 6 (실효 입력 ~$0.84 @88% cache) | critic(premium 3종·llm-council·escalation) — xai API 키 |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 단일 paste 폴백 |
| Gemini 3.1 Pro / 3-flash | 프리뷰/구독 토큰 | planner·architect·critic |

> † Fable 5는 Opus의 정확히 2배 단가. 구독 포함분(~7/12)도 주간 한도를 소모한다.
> ‡ Sonnet 5는 **토크나이저 변경으로 동일 텍스트가 ~30% 더 많은 토큰**이 된다 — 실효 비용은 스티커 단가보다 높게 잡을 것.
> (참고: DeepSeek 계열은 DeepInfra 프로바이더 경유 시 V4 Pro $1.30/$2.60 — [§3-3](#3-3-구독--프로바이더).)

**프로필 상대 비용**

| 프로필 | 비용 | 핵심 비용 동인 |
|---|---|---|
| dream-team | ●●●●● | default·executor Fable 5 — ~7/12 구독 포함(주간 한도 50% 상한), 이후 credits $10/50 |
| escalation | ●●●●● | executor Fable `:xhigh`(구원투수 — 간헐 사용) + planner Sol `:xhigh` + 4벤더 인증 |
| ultimate-opus / ultimate-sol | ●●●●○ | Opus 또는 Sol 3좌석 `:high~xhigh` + Grok critic(xai API) |
| llm-council | ●●●●○ | 4벤더 인증 + Sol `:xhigh` planner — council 워크플로 실행 시 표 수만큼 과금 |
| coding-sprint | ●●●○○ | executor Opus `:high`(실패신호 시에만 max 격상) |
| daily | ●●●○○ | 본체 Opus `:medium`, 위임은 중·저가로 분산 — 구독 OAuth 3벤더 |
| monorepo | ●●●○○ | executor/architect Opus + Gemini(프리뷰/구독) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash($0.14) + Luna($1) + Gemini 프리뷰 — 단, *절대 최저가는 내장 `codex-eco`* |

> **3대 절감 레버**: ① 위임 work를 초저가 모델(DeepSeek V4 Flash $0.14, Luna $1)·프리뷰/구독 토큰(Gemini)으로 ② 실패 시에만 effort 격상 ③ 본체(Anthropic 플래그십)는 품질 상한이라 유지하되 일상은 `:medium` — Fable default(`dream-team`)의 credits가 부담이면 default를 `opus-4-8:high`로(≈`ultimate-opus` 구조).

---

## 11. 📖 출처

**코딩(executor)** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1)

**Claude 5 패밀리** · [Fable 5 재배포 공지](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com 모델 문서](https://platform.claude.com/docs) — 가격·구독 포함(~7/12 연장, [Android Authority 보도](https://www.androidauthority.com/claude-fable-5-free-extension-3685103/))·effort 스펙 교차 확인 2026-07-02/07-10

**GPT-5.6 (2026-07-09 GA)** · [출시 발표](https://openai.com/index/gpt-5-6/) · [Sol 프리뷰(Cerebras 750TPS)](https://openai.com/index/previewing-gpt-5-6-sol/) · [AA: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) · [TechTimes(METR 평가 게이밍)](https://www.techtimes.com/articles/319808/20260707/gpt-56-sol-review-faster-coding-half-fable-5-cost-benchmark-problem.htm) — 가격·평가 교차 확인 2026-07-10

**추론(planner)** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**ctx·멀티모달(architect)** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**툴콜·정직성(default)** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**독립성·라우팅(critic+설계)** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [자기선호는 능력과 함께 커진다](https://arxiv.org/abs/2604.22891) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**공식 모델/가격** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**한 줄로 설치하고, 역할마다 최적 모델로.**

**v2.0.0** · [CHANGELOG](./CHANGELOG.md) · [유지보수·검증 플레이북](./MAINTAINING.md) · 라이선스 [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
