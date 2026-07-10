<div align="center">

# 🧩 GJC 멀티벤더 극한 셋업

### claude · gpt · grok · gemini · opencode go — 5개 구독을 *역할별로* 쪼개 쓰는 검증된 설정

복잡한 모델 선택을 고민하지 말고, **한 줄로 설치**해 역할마다 최적 모델이 자동으로 배치되게 하라.

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-1.11.0-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/profiles-13-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="legend 셋업 — 역할별 최강 모델" width="100%">

</div>

**한국어 (이 문서) · [English](./README.en.md) · [中文](./README.zh.md) · [日本語](./README.ja.md)**

> [!NOTE]
> **이 가이드의 핵심은 GJC 공식 문서로 채택됐다** — 압축판이 [`docs/multi-vendor-profiles.md`](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md) 로 업스트림 머지됨([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev`). 역할·셀렉터 개념의 **정식 레퍼런스는 GJC 공식 docs**를 따르고, **이 레포는 거기 없는 것** — 원클릭 설치기, 13개 프로필 전체(`solo-*`·`claude-codex*`·`legend`·`cyber-cop` 포함), 그리고 [유지보수·검증 도구](./MAINTAINING.md)(정적 검증 CI + 라이브 셀렉터 배터리 + 카탈로그 드리프트 추적) — 를 제공한다.

## 🚨 NEW · `cyber-cop` — 첫 reviewer 모드 프로필

> 지금까지 12개 프로필은 전부 코드를 **쓰는(author)** 세션용이었다. **`cyber-cop`은 코드를 막아서는 세션**을 위한 13번째 프로필 — GJC 최초의 **reviewer 모드**다. 남의 PR을 검토하고, 반대 근거를 찾고, 머지 게이트에서 판정한다.

**무엇이 다른가**
- PR 리뷰·보안 감사에서 역할 가중치가 **반전** → **architect(1차 판정: CLEAR/WATCH/BLOCK)와 critic(머지 게이트)이 주연**, executor는 재현 PoC·failing test 조연으로 내려간다.
- critic이 **코드 작성자(Claude 가정) 대비 cross-family**(GPT-5.6 Sol — v1.11에서 gpt-5.5 동가 세대교체) → 자기선호 편향을 구조적으로 차단([arXiv 2410.21819](https://arxiv.org/abs/2410.21819)).
- 고위험 PR·보안 감사는 **3표 병렬 패널**(`gpt-5.6-sol` · `grok-4.5` · `gemini-3.1-pro`) 독립 투표 → 2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단.

**작동 증거 — 이 레포가 스스로 검증했다**
> PR #4~#7에서 리뷰 게이트가 **머지 전 결함 10건을 차단**했다(#4: 5건 · #6: 5건 · #7: 첫 투표 통과). 리뷰 헬퍼가 *자기 자신의* prompt-injection 결함으로 BLOCK 당했고(고친 뒤 통과), 본체(Anthropic)가 자기 계열 문서를 관대히 넘긴 지점 2건(상대경로 인젝션 표면·권한 과장)을 **cross-family critic(GPT-5.5)이 정확히 BLOCK**했다. (추가로 #6 머지 후 1건이 발견돼 #7로 즉시 수정.) 자기선호-편향 방어가 실전에서 작동함을 증명한 것이다.

**클론 없이 2커맨드로 시작 (v1.6+)**
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

### Extragoal — GPT-5.5 Pro 최종리뷰 레인 (opt-in, v1.9+)

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

이 한 줄이 **13개 프로필을 `~/.gjc/agent/models.yml` 에 안전 병합**하고 기본 프로필을 `daily` 로 설정한다. 기존 설정은 자동 백업되며, 재실행해도 깔끔히 갱신된다.

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
> 기본 프로필 지정: `curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash` · 기본값 설정 건너뛰기: `GJC_SETUP_DEFAULT=none`.

---

## 📑 목차

1. [왜 멀티벤더인가](#1--왜-멀티벤더인가)
2. [핵심 설계](#2--핵심-설계)
3. [GJC 엔진 사실](#3--gjc-엔진-사실)
4. [벤치마크 근거](#4--벤치마크-근거)
5. [최종 카탈로그 13종](#5-️-최종-카탈로그-13종)
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
| 🧠 **추론·설계**(planner) | 순서·수용기준 짜기 | **Gemini 3.1 Pro** (GPQA 94.3 / ARC-AGI-2 77.1)† |
| 🔨 **구현**(executor) | 실제 코드 작성·수정 | **Claude Fable 5** (SWE-bench Verified **95.0**) — 구독 포함 최강은 **Opus 4.8**(88.6) |
| 🔭 **코드리뷰**(architect) | 대형 리포 탐색·아키텍처 | **Gemini 3.1 Pro** (멀티모달 MMMU-Pro 81%)† · 초장문맥(>200k)은 **Opus** |
| ⚖️ **독립 비평**(critic) | 결과 적대 검증 | **cross-family** (본체와 다른 벤더) |
| 🎛️ **오케스트레이션**(default) | 도구호출·라우팅·정직성 | **Anthropic 플래그십** — Opus 4.8 (라우터 품질 = 전체 상한; `legend`/`ultimate-f5`는 Fable 5) |

> **벤치마크 기준일: 2026-07-02** (Claude 5 패밀리 출시 직후 재검증). † 추론·architect 축은 "후계자 임박" — GPT-5.6 Sol이 파트너 프리뷰 중(6/26, `max` effort + `ultra` 서브에이전트 모드, GA 수 주 내), Gemini 3.5 Pro(2M ctx, Deep Think)는 7월 GA로 연기. 출시 시 재검증 예정.

> 한 벤더로 5역할을 다 채우면 1등이 아닌 자리가 반드시 생긴다. 이 가이드는 그 5자리를 각각의 최적 벤더로 채우되, 비용·접근성·신뢰성까지 따져 **실제로 작동하는 조합**으로 정리한 결과다. GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro 기반 3종 독립 딥리서치를 교차검증하고, 셀렉터 검증 상태를 [§6](#6--검증-매트릭스)에 명시한다.

---

## 2. 🧭 핵심 설계

> **강한 본체 1개 고정 (default = Anthropic 플래그십 Opus/Fable) + 작업신호 기반 위임 + 실패신호 기반 effort 에스컬레이션.**

GJC에서 매 작업을 실제로 도는 건 `default`(본체) 하나다. executor/architect/planner/critic 은 본체가 **필요할 때만 `task`로 위임**하는 서브에이전트다(fresh-context).

<div align="center">
<img src="assets/architecture.svg" alt="본체 1개(default) + 서브에이전트 4 — 작업신호 위임" width="100%">
</div>

세 가지 설계 원칙:

- **본체는 절대 양보 불가.** median 작업의 대부분은 본체 혼자 처리하므로, 본체(default)를 약한 모델로 내리면 체감 성능 전체가 무너진다. 항상 Anthropic 플래그십(Opus 4.8 — `legend`/`ultimate-f5`에선 Fable 5).
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

**GJC 0.9.1~0.9.5 실효 기준**이다 — API 공식 스펙과 다른 곳이 있다(아래 각주):

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
> **하드룰 5선**: ① Gemini Pro는 `low`/`high`만 ② openai-codex ctx는 **모델별** — `gpt-5.4`=**1M** · `gpt-5.5`·`gpt-5.6 3종`=**272K**(5.6의 API 스펙은 1.05M — codex 표기 하한) ③ Sonnet(4.6/5)은 GJC에서 `xhigh`/`max` 불가 · **Fable 5는 `max` 불가**(각각 high/xhigh로 클램프) ④ opencode-go는 `:effort` 생략(deepseek-v4 계열만 예외적으로 지원) ⑤ xai `grok-4.5` 상한은 `high`(`:xhigh` 침묵 클램프 — xhigh는 grok-build 프로바이더 전용인데 그쪽은 effort 서픽스 자체가 해석되지 않는다). 범위 밖 등급은 에러가 아니라 **클램프**된다. gpt-5.6 3종은 카탈로그에 `max`까지 뜨고 실호출도 수용되나(07-10 검증) **심도 미검증 — 이 가이드의 출하 상한은 `xhigh`**.
>
> **각주(상류 갭)**: Claude 5 패밀리는 API 공식으로는 둘 다 `max`까지 지원한다. GJC 파서(0.9.1~0.9.5)가 fable 패밀리를 몰라 폴백 추론하고 sonnet-5가 4.6 클램프를 상속하는 **엔진 쪽 갭**이며, 재현 자료와 함께 **상류에 제보됨**. 이 가이드는 GJC 실효 기준으로 기재한다.

### 3-3. 구독 → 프로바이더

| 구독 | provider-id | 비고 |
|---|---|---|
| claude | `anthropic` | 전 effort. Claude 5 패밀리(Fable 5·Sonnet 5) 포함 |
| gpt | `openai-codex` | **ChatGPT 계정 → base GPT(gpt-5.6 sol/terra/luna · 5.5 · 5.4) 제공**. ctx: gpt-5.4=1M · 5.5/5.6 3종=272K |
| grok | `xai` | 전체 라인업 + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra 구독 토큰**. Gemini + 번들 Claude(Opus 4.6 — Claude 5 출시 후 번들 구성 재확인 전) |
| opencode go | `opencode-go` | API 키(`OPENCODE_API_KEY`) |

> [!NOTE]
> **openai-codex 경로 주의**: ChatGPT(Codex) 계정으로 로그인하면 **base GPT 모델(`gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5`, `gpt-5.4`)** 이 제공된다. standalone `-codex` 변종(`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex-max/mini`)은 이 경로에서 **미지원**(`not supported when using Codex with a ChatGPT account`)이라, 본 가이드는 코딩 역할도 검증된 **base GPT**로 통일한다.
>
> 대안 경로: `google-vertex`(API 키, 유료 per-token, 1M ctx) — 구독/쿼터 무관 fallback. 또 하나는 **DeepInfra**(gjc 0.7.9 신규 프로바이더, API 키): DeepSeek V4 Pro **$1.30/$2.60**(1M ctx) · V4 Flash $0.09/$0.18 — Standard/Priority(1.5×) 티어가 GJC `service-tier` 설정과 직결된다.

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
| planner (추론 GPQA/ARC-AGI) | **Gemini 3.1 Pro**† | GPQA 94.3 · ARC-AGI-2 77.1 (유동추론은 GPT-5.5 — [§6-2](#6-2-역할-배치-최적성-검토-deep-research--실측) · GPQA 단독 1위는 Sonnet 5 96.2) |
| architect (ctx·멀티모달) | **Gemini 3.1 Pro**† | 1M ctx · MMMU-Pro 81% |
| default (툴콜·정직성) | **Opus 4.8 / Fable 5** | 라우터 품질 = 전체 상한 (Fable은 refusal·과금 캐비앗 — [§5](#5-️-최종-카탈로그-13종)) |
| critic (독립성) | **cross-family** | 메타-심판 > 토론형 집계 |

> † **후계자 임박 각주**: planner 축은 GPT-5.6 Sol이 파트너 프리뷰 중(2026-06-26, `max` effort + `ultra` 서브에이전트 모드 — GA 수 주 내), architect 축은 Gemini 3.5 Pro(2M ctx, Deep Think)가 7월 GA로 연기. 어느 쪽이든 출시 시 이 표는 재검증 대상이다.

**핵심 합의 원칙**

1. **default = Anthropic 플래그십(Opus/Fable) 고정**(멀티벤더 프로필) — 라우터 품질이 전체 품질 상한. solo-* 는 단일 벤더 최강을 default로.
2. **architect = Gemini 3.1 Pro(멀티모달) / Opus(초장문맥)** — Gemini는 비전·중간 ctx 최적, 200k+ 텍스트 실효검색은 Opus(MRCR 76%@1M, Gemini는 26%로 붕괴).
3. **critic = cross-family** — 본체/플래너와 다른 벤더여야 편향이 완화된다(self-preference bias).
4. **구조 = 강본체 + 작업신호 위임 + 실패기반 effort 에스컬레이션.**
5. **매 쿼리 프로필 스왑 ❌** — 캐시 손실 > 이득. 모드 경계에서만 스왑.

> 벤치마크는 시점 민감하다 → 분기별 재검증 권장. 절대순위는 vals.ai 독립보드로 한정.

---

## 5. 🗂️ 최종 카탈로그 13종

<div align="center">
<img src="assets/profiles-matrix.svg" alt="프로필 × 역할 매트릭스" width="100%">
</div>

> ★ = 평소 권장. 상단 배너 = **`legend` 셋업**(지속 가능 최강 — default만 Fable 5). 비용 균형의 평소 권장은 **`daily`**(executor·critic을 저가로 교체). 멀티벤더 프로필은 `default = Anthropic 플래그십(Opus/Fable)`·`critic=cross-family`(solo-* 는 단일 벤더 최강), 전부 엔진 effort 하드룰 통과 + **셀렉터 검증 상태 추적**([§6](#6--검증-매트릭스); 07-09 rerun은 Grok/OpenAI/Gemini/opencode, Anthropic은 quota로 07-02 last-good 유지).

| 프로필 | 한 줄 정의 | 이럴 때 |
|---|---|---|
| ⭐ **daily** | 본체 Opus + 위임을 역할별 최적 벤더로 | **평소 기본** |
| 🏆 **ultimate** | 비용 무시, 역할별 최강 (지속 가능판) | 정확성이 비용보다 중요 |
| 🔥 **ultimate-f5** | Fable 5 중심 이벤트판 — **구독 포함 ~2026-07-12 23:59 PT(연장 확정)** | 이벤트 기간 최고 정확성 |
| 👑 **legend** | 본체만 Fable 5, 나머지는 지속 구조 | 7/12 이후에도 유지 가능한 최강 |
| 🏎️ **coding-sprint** | executor 주연 + 코딩인지 critic | 순수 구현 처리량 |
| 🛡️ **escalation** | 실패 신호 시 Fable 5 구원투수 + critic 멀티벤더 패널 | 머지·보안·결제·비가역 변경 |
| 🚨 **cyber-cop** | reviewer 모드 — architect·critic 주연, PR 리뷰·보안 감사 전용 | 남의 PR 검토·머지 게이트·보안 감사 |
| 💸 **eco** | 본체만 Opus, 위임은 전부 저가/구독 모델 | 비용 압박·대량 작업 |
| 🗺️ **monorepo** | 전역 ≥1M ctx (gpt-5.5/5.6 배제) | 거대 코드베이스 |
| 🧱 **solo-anthropic** | 전 역할 Opus (v1.4: critic도 Opus) | 단일 벤더로만 운영 |
| 🤖 **solo-openai** | 전 역할 base GPT (5.6 Sol 주력 · 5.4=1M 레인) | ChatGPT만 구독 |
| 🤝 **claude-codex** | Claude=실행·ctx / Codex=추론·비평 | Claude+Codex 2구독만 |
| 🥇 **claude-codex-max** | claude-codex 비용무시 최강판 | Claude+Codex · 정확성 우선 |

<details>
<summary><b>📋 전체 YAML 펼치기 (gjc-profiles.yml 와 동일 — 모델 매핑 기준, 주석의 §참조만 README에 맞춤)</b></summary>

```yaml
profiles:

  daily:                               # ★ 평소 기본 (--default daily)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 본체 효율 knee
      executor:  openai-codex/gpt-5.6-terra:high                # 코딩특화·동가($2.5/15)에 ≈GPT-5.5급(공식 5.6 평가표)·벤더분산(검증✅ 07-10)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 추론 검증1위(GPQA 94.3 / ARC-AGI-2 77.1)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx·멀티모달(MMMU-Pro 81%)
      critic:    xai/grok-4.5:medium                            # cross-family 독립비평. grok-4.5 $2/$6(실효 ~$0.84/$6.2). medium≈1.7k reasoning/~14s

  ultimate:                            # 비용무시, 역할별 최강 + 벤더분산 (지속 가능판 — 이벤트판은 ultimate-f5)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # 구독 포함 코딩 최강(SWE-bench Verified 88.6)
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 최상위 추론 + OpenAI 다양성(5.5→5.6 Sol 동가 세대교체)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx·멀티모달
      critic:    xai/grok-4.5:high                              # cross-family 독립비평

  ultimate-f5:                         # 🔥 이벤트: Fable 5 중심 — 구독 포함 ~2026-07-12 23:59 PT(7/7→7/12 연장 확정, 주간 한도 50% 상한), 이후 usage credits($10/$50)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # 라우터=품질 상한. refusal(HTTP 200+stop_reason) 유의
      executor:  anthropic/claude-fable-5:xhigh                 # SWE-bench Verified 95.0 신 1위. ⚠:max 금지(xhigh로 침묵 클램프)
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 추론 축은 Fable 우위 미입증(ARC-AGI-2 미공개) — GPT 유지(5.6 Sol 세대교체)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 멀티모달 검증 우위 유지(Fable 비전은 vendor-claimed)
      critic:    xai/grok-4.5:high                              # cross-family 불변 — Fable 자기평가 금지
      # 7/12(23:59 PT) 이후: default를 opus-4-8:high로 내리면 legend와 동일한 지속 구조

  legend:                              # 👑 Ultimate Legend — 7/12 이후에도 유지 가능한 최강 (fable은 default 한 자리만)
    display_name: legend5
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-fable-5:high                  # 라우터 품질 상한 = Fable (usage credits 노출 최소 지점)
      executor:  anthropic/claude-opus-4-8:max                  # 구독 포함 코딩 최강(88.6)
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.5:high
      # credits 비용 회피 시: default를 opus-4-8:high로 — ultimate와 동일해짐

  coding-sprint:                       # 순수 구현 처리량. executor 주연 + 코딩인지 critic
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 본체 오케스트레이션
      executor:  anthropic/claude-opus-4-8:max                  # 구독 포함 코딩 최강(88.6)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 추론 검증1위로 경량 계획
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx 리뷰
      critic:    openai-codex/gpt-5.6-terra:high                # 코딩인지 critic(실버그 포착), cross-family vs gemini

  escalation:                          # 고실패비용 — 실패 신호 시 최강 실행자(Fable 5) 투입 + critic 멀티벤더 병렬패널(§9)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-fable-5:xhigh                 # 실패한 작업의 구원투수(SWE-V 95.0). 간헐 사용 = credits 과금과도 궁합
      planner:   openai-codex/gpt-5.6-sol:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.5:high                              # + 3표 교차벤더 critic 패널(독립투표→본체집계). grok-4.5 :xhigh/:max는 high로 침묵 클램프라 미사용
      # (v1.3까지의 critic :xhigh는 no-op 클램프였음 — xhigh는 grok-build 프로바이더 전용이며 effort 서픽스 미지원)

  cyber-cop:                           # 🚨 reviewer 모드 — PR 리뷰·보안 감사 (author 모드의 역상)
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high                 # 불변식 준수 + 1M ctx. 집계자 제한 — critic raw verdict 보존·노출(routing-rules 계약)
      executor:  openai-codex/gpt-5.6-sol:high                  # 조연 — 재현 PoC·failing test·harness (Terminal-Bench 2.1 88.8 SOTA)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 리뷰 체크리스트·감사 범위 (critic과 cross-family)
      architect: anthropic/claude-opus-4-8:high                 # 주연1 — 1차 코드리뷰 판정자, 1M 실효검색(MRCR 76% vs Gemini 26%)
      critic:    openai-codex/gpt-5.6-sol:high                  # 주연2 — 머지 게이트, Claude-작성 코드와 cross-family
      # 고위험 PR·보안 감사: critic 3표 병렬 패널 {openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high,
      # google-antigravity/gemini-3.1-pro-low:high} — 독립 투표 후 본체 집계(토론 금지), 2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단
      # (3표째 grok은 xai 로그인 시 — 미보유면 2표 {gpt-5.6-sol, gemini}로도 provenance 최소치(non-default family ≥2) 충족)

  eco:                                 # 최저가 — 본체만 Opus(effort 절감), 위임은 초저가/구독 모델(검증표 기준✅)
    required_providers: [anthropic, opencode-go, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:low                  # 라우터는 못 내림, effort만 절감
      executor:  opencode-go/deepseek-v4-flash                  # $0.14/0.28, 1M, 최저가 코더(5번째 벤더). 대안: sonnet-5:medium(≈sonnet-4-6:high, 인트로 $2/10 ~8/31)
      planner:   xai/grok-4-1-fast:high                         # $0.2/0.5, 2M, 저가 추론
      architect: google-antigravity/gemini-3.1-pro-low          # 구독 토큰, 저effort, 1M ctx
      critic:    google-antigravity/gemini-3.5-flash-low        # 구독 토큰, 경량, cross-family vs executor(opencode-go). 리터럴 id 핀(구 'gemini-3.5-flash'는 퍼지 매칭)

  monorepo:                            # 거대 코드베이스 — 전역 1M ctx (★gpt-5.5/5.6 272K 배제 — gpt-5.4는 1M이나 Opus가 동급 이상)
    required_providers: [anthropic, google-antigravity, opencode-go]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 1M
      executor:  anthropic/claude-opus-4-8:high                 # 1M
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 추론(스코프 입력)
      architect: anthropic/claude-opus-4-8:high                 # Opus 4.8 = GJC 1M ctx 윈도우 지원(멀티턴 누적·검색 최상). 단일 메시지 paste만 ~400k 한도 — 한 방에 >400k는 opencode-go/deepseek-v4-pro
      critic:    opencode-go/glm-5.2                            # 오픈웨이트 1위(AA 51 > V4 Pro 44), 0.7.10 번들 카탈로그 편입, cross-family vs anthropic (대안: deepseek-v4-pro)

  solo-anthropic:                      # 단일 벤더로만 운영 — 전 역할 Opus (v1.4: critic Sonnet→Opus, 능력 우선)
    required_providers: [anthropic]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max
      planner:   anthropic/claude-opus-4-8:max
      architect: anthropic/claude-opus-4-8:high                 # 1M, Gemini 대체(폴백 1순위)
      critic:    anthropic/claude-opus-4-8:high                 # ⚠동일모델 자기평가=편향 최대(연구 확인) — 품질 경로는 cross-family 프로필
      # Sonnet 5 critic 비추천: 리뷰어 버그 리콜 실측 하락(63%→50%, 정밀도만 상승)

  solo-openai:                         # ChatGPT(Codex) 계정만 — base GPT 전용
    required_providers: [openai-codex]
    model_mapping:
      default:   openai-codex/gpt-5.6-sol:high                  # 라우터(base GPT 최강, ctx 272K)
      executor:  openai-codex/gpt-5.6-sol:xhigh                 # 이 계정 최강 코더
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 최상위 추론
      architect: openai-codex/gpt-5.4:high                      # ★gpt-5.4 = 1M ctx — 대용량 입력은 이쪽(5.5/5.6은 272K)
      critic:    openai-codex/gpt-5.6-terra:high                # ⚠동일벤더=독립성 약함(트레이드오프). Sol(executor)과 모델 분리

  claude-codex:                        # ★2벤더(Claude+Codex)만 — 평소 균형. Anthropic=실행·ctx / Codex=추론·비평
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 라우터·툴신뢰
      executor:  anthropic/claude-opus-4-8:high                 # 구독 포함 코딩 최강(SWE-bench 88.6)
      planner:   openai-codex/gpt-5.6-sol:high                  # OpenAI 추론 플래그십
      architect: anthropic/claude-opus-4-8:high                 # 1M 윈도우(gpt-5.5/5.6 272K 한계 회피)
      critic:    openai-codex/gpt-5.6-terra:high                # cross-family vs Opus(executor), 코딩인지

  claude-codex-max:                    # 2벤더(Claude+Codex) 최강 — 비용 무시
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # SWE-bench 88.6
      planner:   openai-codex/gpt-5.6-sol:xhigh                 # 최상위 추론
      architect: anthropic/claude-opus-4-8:high                 # 1M 윈도우
      critic:    openai-codex/gpt-5.6-sol:high                  # cross-family 독립 비평 vs Opus

# ─────────────────────────────────────────────────────────────────────────────
# Claude 5 패밀리(2026-07-01~): Fable 5 = $10/$50(Opus 2배), 구독 포함은 ~7/12 23:59 PT(7/7→7/12 연장 확정, 주간 한도 50%)뿐 — "무료" 아님.
#   Sonnet 5 = $3/$15(인트로 $2/$10 ~2026-08-31), 토크나이저 변경으로 동일 텍스트 ~30% 토큰 증가.
#   GJC 실효 effort: fable-5 ≤xhigh · sonnet-5 ≤high (API는 둘 다 max 지원 — GJC 파서 갭, 상류 제보됨).
# GPT-5.6(2026-07-09 GA): Sol $5/$30 · Terra $2.5/$15(≈GPT-5.5급을 반값에) · Luna $1/$6(미채용) — API 1.05M ctx/128K out, codex 표기 272K.
#   실호출 검증(2026-07-10, gjc 0.9.5): 3종 :medium/:high/:xhigh/:max 수용 · :bogus 거부. :max 심도 미검증 — 출하 상한 xhigh.
#   ⚠ METR: Sol의 SWE 평가 게이밍 적발 — SWE류 벤치 단독 근거 승격 금지(Terminal-Bench 2.1 88.8 SOTA는 공식+AA 교차확인).
# opencode-go: OPENCODE_API_KEY 설정 시 활성(eco.executor·monorepo.critic 에서 사용).
#   검증✅: deepseek-v4-flash/pro · glm-5.2 · minimax-m2.7 · qwen3.7-max · kimi-k2.6 · mimo-v2.5.
#   신규 입점(미검증·후보): kimi-k2.7-code(버짓 executor 유력) · minimax-m3(1M 멀티모달).
# 선택: grok 구독(SuperGrok OAuth)의 grok-build/composer 도 사용 가능:
#   grok-build/grok-4.3 (bare 셀렉터만 동작, effort 서픽스 미지원 — 검증✅ 2026-07-02).
```

</details>

> [!TIP]
> **opencode-go** 는 `OPENCODE_API_KEY` 설정 시 `eco`(executor)·`monorepo`(critic)에서 활성화된다(검증✅). grok 구독(SuperGrok)의 `xai/grok-composer-2.5-fast`(200k)도 검증됨 — throughput용 대안. 다른 opencode-go 모델(qwen3.7-max·kimi-k2.6·glm-5.1·minimax-m2.7·mimo-v2.5)도 전부 동작 확인. 신규 입점(미검증 후보): **kimi-k2.7-code**(버짓 executor 유력) · **minimax-m3**(1M 멀티모달).

#### 프로필별 설계 근거

- **daily** — 본체 Opus `:medium`(효율 knee), 구현은 코딩특화 `gpt-5.6-terra`(v1.11: gpt-5.4의 동가 후계 — $2.5/15에 ≈GPT-5.5급), 설계·리뷰는 추론/ctx 1위 Gemini, 비평은 저가 독립 Grok. 일상 작업의 품질/비용 균형점.
- **ultimate** — 비용을 포기하고 executor까지 Opus `:max`. planner는 OpenAI 다양성을 위해 `gpt-5.6-sol:xhigh`(v1.11: gpt-5.5의 동가 세대교체). **지속 가능판** — Fable 5 이벤트판은 `ultimate-f5`, 지속판 최상위는 `legend`.
- **ultimate-f5** — 🔥 **Fable 5 이벤트판**. Fable 5는 **2026-07-12 23:59 PT까지 구독에 포함**(7/7 종료 예정이 반발로 5일 연장 확정; Pro/Max/Team, **주간 사용 한도의 50% 상한** — "무료"가 아니다. 헤비 유저는 종료 전에 상한을 소진할 수 있다), **이후엔 usage credits 별도 과금**($10/$50, Opus의 2배; Anthropic은 capacity 확보 시 구독 복귀 방침 — 비확정). executor는 GJC 실효 최고 등급 `:xhigh`(`:max`는 xhigh로 침묵 클램프). **refusal 유의**: 신형 안전 분류기가 HTTP 200 + `stop_reason: refusal`로 거부할 수 있어 에이전트 하네스가 "빈 응답"으로 오인할 위험이 있다. **7/12 이후 다운그레이드 경로**: `legend`로 전환하거나 default를 `opus-4-8:high`로 내리면 `ultimate`와 동일한 지속 구조.
- **legend** — 👑 지속 가능 최강(상단 배너). Fable 5를 **default 한 자리에만** 둬서 7/12 이후 usage credits 노출을 최소화하면서 라우터 품질 상한을 유지하고, executor는 구독 포함 최강 Opus `:max`. `display_name: legend5` 는 로컬 커스텀 프리셋과의 이름 충돌(덮어쓰기)을 막는 보호 장치. 참고: default는 최다 호출 역할이라 credits 비용은 계속 발생한다 — 완전 회피하려면 default를 `opus-4-8:high`로(= `ultimate`와 동일).
- **coding-sprint** — executor 주연(Opus `:max`), 계획·리뷰는 가볍게, critic은 *코딩을 아는* `gpt-5.6-terra`로 실버그를 잡는다(cross-family vs gemini).
- **escalation** — v1.4 재설계: 실패 신호가 뜬 작업에 **최강 실행자 Fable 5 `:xhigh`를 구원투수로 투입**한다 — 간헐 사용이라 7/12 이후 usage credits 과금과도 궁합이 맞다. critic은 멀티벤더 3표 패널([§9](#9--병렬-에이전트--신뢰성)). 정직한 기록: v1.3까지의 critic `grok-4.3:xhigh`는 **no-op였다** — xai 프로바이더의 grok-4.3 상한이 high라 침묵 클램프로 `ultimate` critic과 동일 동작(xhigh는 grok-build 프로바이더 전용인데 그쪽은 effort 서픽스 자체가 해석되지 않는다). v1.4는 `:high`로 명시 교정했다. 되돌릴 수 없는 변경 전용.
- **cyber-cop** — 🚨 **reviewer 모드** (v1.5 신규): 기존 12종이 전부 author 모드(default+executor 가중)인 갭을 닫는 13번째 카테고리. 리뷰 세션에선 역할 가중치가 반전된다 — executor는 재현 PoC·failing test용 조연으로 내려가고, **architect(1차 코드리뷰 판정자)와 critic(머지 게이트)이 주연**이 된다. architect=Opus `:high`(1M 실효검색 76% vs Gemini 26% 붕괴 — 200k+ diff 통독), critic=`gpt-5.6-sol:high`(v1.11: gpt-5.5의 동가 세대교체; Claude-작성 코드와 cross-family — 자기선호 편향 완화, arXiv [2410.21819](https://arxiv.org/abs/2410.21819)). 고위험 PR·보안 감사는 critic 3표 패널(§9 규칙 그대로 — 독립 투표, 토론 금지, 2/3 반박 시 차단; 3표째 grok은 xai 로그인 시 — 그래서 xai는 `required_providers`에 없고, 미보유자도 2표 {gpt-5.6-sol, gemini}로 provenance 최소치를 지키며 운영 가능). 비용 대략치(100k in/10k out 리뷰 패스당): grok ~$0.15 · opus ~$0.75 · gpt-5.6-sol ~$0.80(5.5 동가) — critic은 머지 게이트에서만 호출되는 저빈도 자리라 상시 Sol도 부담이 작다. 운영 규칙(위임 순서·증거 계약·집계자 제한·provenance fallback·LGTM 금지)은 [`routing-rules.md`](./routing-rules.md)의 리뷰어 계약 참조. `escalation`과의 차이: escalation은 author-side 게이트(고쳐서 통과), cyber-cop은 reviewer-side(반대 근거 탐색).
- **eco** — 본체만 Opus(`:low`), executor는 최저가 `deepseek-v4-flash`(opencode-go — 5번째 벤더 활용; 대안: `sonnet-5:medium` ≈ sonnet-4-6:high, 인트로 $2/$10 ~8/31), planner는 초저가 Grok Fast, architect/critic은 구독 토큰 Gemini. critic은 `gemini-3.5-flash-low`로 **리터럴 id 핀**(구 `gemini-3.5-flash`는 퍼지 매칭으로 우연히 동작하던 것) — executor(opencode-go)와 cross-family.
- **monorepo** — 전 역할이 1M ctx. `gpt-5.5`·`gpt-5.6 3종`(272K)은 배제 — gpt-5.4는 1M이지만 Opus가 동급 이상. architect=**Opus**(1M 실효검색 1위 **76%@1M** — Gemini는 26%로 붕괴, Grok은 멀티모달 약함), critic=**`glm-5.2`**(cross-family, 대안 `deepseek-v4-pro`). 1M을 넘보는 거대 입력은 한 메시지에 통째로 붓지 말고 **청크로 나눠 멀티턴 누적**하면 1M 윈도우를 그대로 쓸 수 있다([§6-3](#6-3-잔여-공백-검토-gap-13--gjc-실효-컨텍스트-실측)) — 단일 메시지 >~400k paste만 `opencode-go/deepseek-v4-pro`로.
- **solo-anthropic** — 단일 벤더 운영, v1.4에서 critic까지 **전 역할 Opus**(능력 우선 선택). Sonnet 계열 critic은 비추천 — Sonnet 5 리뷰어 실측(CodeRabbit)에서 정밀도는 올랐지만 **버그 리콜이 63%→50%로 하락**했다. 단, 전부-Opus가 편향을 없애는 건 아니다: 연구상 **강한 모델일수록 자기선호 편향이 오히려 크고**(arXiv [2410.21819](https://arxiv.org/abs/2410.21819) · [2604.22891](https://arxiv.org/abs/2604.22891)), **능력이 편향을 상쇄하지 않는다**. 이 프로필은 "단일 벤더 제약 하의 능력 우선"이고, **품질 경로는 여전히 cross-family 프로필**이다.
- **solo-openai** — ChatGPT(Codex) 계정만 쓰는 사용자용. 전 역할을 base GPT로 — `-codex` 변종은 이 계정에서 미지원이라 제외. v1.11: 주력 4좌석을 `gpt-5.6-sol`로 세대교체(critic은 `gpt-5.6-terra`로 executor와 모델 분리), architect만 **gpt-5.4=1M** 유지(5.5/5.6은 272K — 대용량 입력은 architect gpt-5.4로). critic이 동일 벤더라 독립성은 약함.
- **claude-codex** — Claude+Codex **2구독만** 보유한 사용자용 Best 믹스. **Anthropic = 실행·컨텍스트**(default·executor·architect: Opus가 구독 포함 코딩 최강 SWE-bench 88.6 + 1M 윈도우 — gpt-5.5/5.6은 272K라 대형 ctx는 Opus가 유리), **Codex = 추론·비평**(planner: GPT-5.6 Sol 추론 플래그십 / critic: GPT-5.6 Terra가 Opus executor를 cross-family 독립 비평). 2벤더로도 5역할 cross-family critic 성립.
- **claude-codex-max** — 위를 비용 무시로 끌어올린 최강판(executor Opus `:max`, planner `gpt-5.6-sol:xhigh`).

---

## 6. ✅ 검증 매트릭스

> 2026-07-10(gjc 0.9.5)에 전 프로바이더 핵심 셀렉터를 `gjc -p --no-session --no-tools --model <sel> "..."` 로 **실제 호출**해 재검증했다(`evidence/2026-07-10-selectors-rerun-2.md`) — Anthropic rate-limit 해제로 전 좌석 그린, gpt-5.6 3종 신규 검증. "동작함"의 근거는 추정이 아니라 실호출 증거다.

| 프로바이더 | 검증된 셀렉터 (✅ 동작) |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh`(**07-10 rerun✅** — `:max`는 xhigh로 침묵 클램프) · `claude-sonnet-5:high`(07-10✅ — `:max`는 high로 침묵 클램프) · `claude-opus-4-8:high`(07-10✅, low·medium·max 07-02✅) · `claude-sonnet-4-6:high`(07-10✅) — 07-09 rate-limit 해제, 전 좌석 재검증 완료 |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh`(**07-10✅**) · `gpt-5.6-terra:high`/`:xhigh`(07-10✅) · `gpt-5.6-luna:high`(07-10✅) · 3종 `:max` 수용되나 심도 미검증(미출하) · `gpt-5.5:high`(07-02✅, v1.11에서 프로필 은퇴—카나리 유지) · `gpt-5.4:high`(1M ctx 레인) |
| `xai` | `grok-4.5:medium`/`:high`(07-09✅ — `:xhigh`/`:max`는 high로 침묵 클램프; xai 전용, provider 500K/GJC 222K floor, $2/$6) · `grok-4-1-fast:high`(07-02✅) · `grok-4-fast:high`(07-02✅) · `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `grok-build` | `grok-4.3`(**bare 셀렉터만** — effort 서픽스 미해석, 07-02✅. SuperGrok OAuth) |
| `google-antigravity` | `gemini-3.1-pro-low`(±`:high`, 07-10✅) · `gemini-3.5-flash-low`(**리터럴 핀**, 07-10✅) · `gemini-3.5-flash`(퍼지 매칭 동작) · ⚠`gemini-3.1-pro-high`는 0.9.5부터 400이 아니라 **-low 기본 effort로 침묵 퍼지 해석**(고추론 아님 — 함정) · `gemini-3-flash` · `claude-opus-4-6-thinking`(06-18 — Claude 5 출시 후 번들 구성 재확인 전) |
| `opencode-go` | `deepseek-v4-flash`·`deepseek-v4-pro`(07-02 재검증✅) · `glm-5.2`(**0.7.10 번들 편입**, 07-02✅) · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` (`OPENCODE_API_KEY` 필요) |

> [!WARNING]
> **이 환경에서 동작하지 않은 셀렉터**(피하라): `openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`(ChatGPT 계정 미지원) · `google-antigravity/gemini-3.1-pro-high`(**0.9.5부터 400이 아니라 `-low` 기본 effort로 침묵 퍼지 해석 — "성공"하지만 고추론이 아닌 함정**, 엔진은 `gemini-3.1-pro-low:high` 사용) · `gemini-3-pro`(은퇴) · `claude-sonnet-4-6-thinking`(404) · `gpt-oss-120b`(500). `opencode-go/*` 는 `OPENCODE_API_KEY` **미설정 시에만** 실패한다(키 설정 후 위 표대로 동작). 참고: `fable-5:max`·`sonnet-5:xhigh/max`·`grok-4.5:xhigh/max` 는 실패가 아니라 **침묵 클램프**다([§3-2](#3-2-추론등급effort-치트시트)) — gpt-5.6 3종의 `:max`는 수용되나 심도 미검증(미출하).

> [!NOTE]
> `opencode-go/glm-5.2` 는 **0.7.10부터 번들 카탈로그에 편입**됐다(구 "라이브 카탈로그 전용" 캐비앗 폐기). 반면 `google-antigravity/gemini-3.5-flash` 리터럴 id는 카탈로그에 없고(`-low`/`-extra-low`만 존재) **퍼지 매칭으로 우연히 동작**하는 것이라, v1.4 프로필은 `gemini-3.5-flash-low`로 핀했다. 디스커버리 미갱신 상태에선 `selector did not resolve` 로 활성화가 실패할 수 있다 — 재로그인/재시도로 카탈로그를 갱신하거나 번들 id로 대체하라(critic 은 `opencode-go/deepseek-v4-pro`, GLM 은 `zai/glm-5.2` — `zai` 를 `required_providers` 에 추가).

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

초기 8프로필(v1.0 기준)의 역할→모델 배치를 다회차 deep-research(독립 벤치 검증)와 라이브 추론 프로브로 재검토한 결과, 골격은 near-optimal로 확인됐다 — `claude-codex*` 2종은 동일 골격을 재사용하고, v1.4 신규 `ultimate-f5`·`legend` 는 [§5 설계 근거](#프로필별-설계-근거)에서 별도 검토했다.

- **`gemini-3.1-pro-low:high` 는 저하 모드가 아니다.** `thinkingLevel`은 별도 모델 변종이 아니라 동일 Gemini 3.1 Pro에 적용되는 per-request 파라미터이고 모델 기본값이 **HIGH**다. 공식 모델카드의 헤드라인 추론 점수(GPQA 94.3 · ARC-AGI-2 77.1)는 전부 *Thinking (High)* 에서 측정됐다 — 이 셀렉터는 **네이티브 고추론 기본모드**를 호출한다. 실측 프로브: `low`(18s) → `low:high`(22s) 지연 증가로 thinking 활성 확인, 표준 추론 정답은 GPT-5.5·Opus와 동일. *(잔여: GJC `:high` override의 네이티브 HIGH 매핑은 1차 출처 미확증 → 운영 중 추론 품질 모니터링 권장.)*
- **planner 추론 축은 분열한다.** GPQA Diamond(과학지식)는 상위권이 93~96%로 *saturated* — 단독 1위는 이제 **Sonnet 5(96.2)**, Gemini 3.1 Pro 94.3. ARC-AGI-2(추상·유동추론)는 **GPT-5.5가 명확히 앞선다**(0.850 vs 0.771; Fable 5는 미공개 — 추론 축 우위 미입증). 플래닝에 더 직결되는 유동추론(ARC) 기준 → ultimate/escalation planner=GPT 유지. **과학지식추론 비중이 크면 `planner → google-antigravity/gemini-3.1-pro-low:high`로 swap.** *(갱신 2026-07-10: GPT-5.6 Sol GA — 공식 평가 전면 우위(Agents' Last Exam 52.7 vs 46.9 · AA Intelligence 58.9 vs 54.8) + 동가 $5/$30 → v1.11에서 planner를 `gpt-5.6-sol:xhigh`로 세대교체. ARC-AGI-2의 5.6 수치는 미공개 — 축 근거는 공식 평가표+AA 지수. 근거: [evidence/2026-07-10-gpt-5.6-notes.md](./evidence/2026-07-10-gpt-5.6-notes.md).)*
- **executor 축은 v1.4에서 교체됐다.** **Fable 5가 SWE-bench Verified 95.0 / SWE-bench Pro 80.3으로 신 1위**(Opus 4.8 88.6 · GPT-5.5 82.6). Opus 4.8은 "구독 포함 코딩 최강"으로 유지 — Fable 5는 7/12 이후 usage credits 과금이라 상시 executor로는 비용 구조가 다르다(`ultimate-f5`/`escalation`에서만 채용). 터미널·에이전틱 축은 이제 **GPT-5.6 Sol이 SOTA**(Terminal-Bench 2.1 88.8) — 단 ⚠METR이 Sol의 SWE 평가 게이밍(역대 최고 비율)을 적발해 SWE류 점수는 할인해서 읽을 것. daily executor는 동가 후계 `gpt-5.6-terra`로 교체(v1.11).
- **xAI `grok-composer-2.5-fast`·`grok-code-fast-1` 은 eco·throughput 전용.** 독립 벤치 미공개/인플레이션으로 프론티어 코더가 아니며 grok-code-fast-1은 은퇴 예정 — executor 코어 비포함이 맞다.
- **default = Anthropic 플래그십.** Opus 4.8은 Vals Index 종합(서빙 모델 중 1위)으로 재확인. Fable 5 default(`legend`/`ultimate-f5`)는 품질 상한을 한 단계 더 올리지만 refusal 분류기·credits 과금 캐비앗을 동반한다([§5](#프로필별-설계-근거)).
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

설치기가 하는 일: `~/.gjc/agent/models.yml` 에 13개 프로필 안전 병합(재실행 시 자동 갱신) · 기존 파일 자동 백업 · 기본 프로필 `daily` 설정. `curl` + `python3` 만 있으면 된다.

```bash
# 옵션
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate bash    # 기본 프로필 지정
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
> **GJC 0.7.10 프리셋 rename/delete 주의**: 엔진의 커스텀 프리셋 rename/delete 기능은 `models.yml` 의 **주석을 전부 제거**한다 — 설치기의 관리 블록 센티널(주석)도 함께 사라져 이름 기반 교체로 격하되고, **사용자가 삭제한 프로필이 재설치 시 부활**할 수 있다(재현 확인). rename/delete 를 쓴 뒤 재설치할 땐 결과를 꼭 확인하고, 완전 제거는 백업 복원(`cp … .bak-*`)이 가장 확실하다.

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
| 머지/릴리즈 직전·보안·결제 | `escalation` |
| PR 리뷰·보안 감사 세션 | `cyber-cop` |
| 정확성 최우선 (Fable 5 이벤트 ~2026-07-12) | `ultimate-f5` → 이후 `legend` |
| 대량 리팩터·마이그레이션 | `eco` |
| 거대 코드베이스 진입 | `monorepo` |
| 단일 벤더로만 운영 | `solo-anthropic` |

---

## 9. 🧪 병렬 에이전트 + 신뢰성

직렬 핸드오프는 신뢰성이 `0.99ⁿ`로 떨어지고, 멀티에이전트는 잘못 묶으면 "false consensus"로 굳는다. 병렬 설계는 이 둘을 방어하도록 짠다.

```text
직렬 체인 5단계(각 0.99):  0.99^5 ≈ 95.1%    → 길수록 붕괴
병렬 독립 5개(OR 성공):    1-(0.01)^5 ≈ 100%  → 다양성이 신뢰성을 높인다
```

**설계 원칙**
- critic은 **본체와 다른 벤더로, 병렬 독립 투표 후 본체가 집계**(debate 금지 — 메타-심판이 우월).
- critic 패널 예: `{xai/grok-4.5:high, openai-codex/gpt-5.6-terra, google-antigravity/gemini-3.1-pro-low:high}` 동시 → 2/3 반박 시 폐기.
- executor fan-out은 **작업이 진짜 독립**(공유 상태 없음)일 때만.
- 체인은 짧게, 본체를 단일 진실원천으로(서브끼리 직접 합의 금지).

---

## 10. 💰 비용

Gemini(`google-antigravity`)는 **Google AI Pro/Ultra 구독 토큰**으로 동작한다(per-token 청구가 아니라 구독에 포함). **Fable 5는 2026-07-12 23:59 PT까지 Claude 구독(Pro/Max/Team)에 포함**(7/7 종료 예정이 5일 연장 확정)되나 주간 사용 한도의 50% 상한이 걸리고, **이후엔 usage credits 별도 과금**이다 — "무료"가 아니다. 나머지는 per-token 과금이며, 주요 모델 단가는 다음과 같다($/1M, 입력/출력):

| 모델 | $/1M (in/out) | 역할 |
|---|---|---|
| Claude Fable 5 | 10 / 50 (배치 5/25 · 캐시 히트 1)† | ultimate-f5 default·executor · legend default · escalation executor |
| Claude Opus 4.8 | 5 / 25 | default·executor |
| Claude Sonnet 5 | 3 / 15 (인트로 2/10 ~2026-08-31)‡ | eco executor 대안 |
| GPT-5.6 Sol | 5 / 30 (Fast 모드는 12.5/75) | planner(ultimate·legend·escalation) · cyber-cop critic·executor · solo-openai |
| GPT-5.6 Terra | 2.5 / 15 | executor/critic(daily·sprint·claude-codex) |
| GPT-5.4 | 2.5 / 15 | solo-openai architect(유일 1M ctx 레인) |
| Grok 4.5 | 2 / 6 (실효 입력 ~$0.84 @88% cache) | critic(v1.10) |
| Grok 4.1 Fast | 0.2 / 0.5 | eco planner |
| GLM-5.2 (opencode-go) | 1.40 / 4.40 | monorepo critic |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · >400k 단일 paste 폴백 |
| Gemini 3.1 Pro / 3.5 Flash | 구독 토큰 | planner·architect·critic |

> † Fable 5는 Opus의 정확히 2배 단가. 구독 포함분(~7/12)도 주간 한도를 소모한다.
> ‡ Sonnet 5는 **토크나이저 변경으로 동일 텍스트가 ~30% 더 많은 토큰**이 된다 — 실효 비용은 스티커 단가보다 높게 잡을 것.
> (참고: DeepSeek 계열은 DeepInfra 프로바이더 경유 시 V4 Pro $1.30/$2.60 — [§3-3](#3-3-구독--프로바이더).)

**프로필 상대 비용**

| 프로필 | 비용 | 핵심 비용 동인 |
|---|---|---|
| ultimate-f5 | ●●●●● | default·executor Fable 5 — ~7/12 구독 포함(주간 한도 50% 상한), 이후 credits $10/50 |
| legend | ●●●●● | default Fable 5(7/12 후 credits) + executor Opus `:max` |
| ultimate / escalation | ●●●●● | executor Opus `:max`/Fable `:xhigh`(구원투수) + planner GPT-5.6 Sol `:xhigh` |
| coding-sprint | ●●●●○ | executor Opus `:max` |
| solo-anthropic | ●●●●○ | 전 역할 Opus (executor/planner `:max`) |
| daily | ●●●○○ | 본체 Opus `:medium`, 위임은 중·저가로 분산 |
| monorepo | ●●●○○ | executor/architect Opus + Gemini(구독) + GLM-5.2 |
| eco | ●○○○○ | executor DeepSeek V4 Flash($0.14) + 구독 Gemini |

> **3대 절감 레버**: ① 위임 work를 초저가 모델(DeepSeek V4 Flash $0.14, Grok Fast $0.2)·구독 토큰(Gemini)으로 ② 실패 시에만 effort 격상 ③ 본체(Anthropic 플래그십)는 품질 상한이라 유지하되 일상은 `:medium`, 비용압박 시 `:low` — Fable default(`legend`)의 credits가 부담이면 default를 `opus-4-8:high`로.

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

**v1.11.0** · [CHANGELOG](./CHANGELOG.md) · [유지보수·검증 플레이북](./MAINTAINING.md) · 라이선스 [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
