<div align="center">

# 🧩 GJC 멀티벤더 극한 셋업

### claude · gpt · grok · gemini · opencode go — 5개 구독을 *역할별로* 쪼개 쓰는 검증된 설정

복잡한 모델 선택을 고민하지 말고, **한 줄로 설치**해 역할마다 최적 모델이 자동으로 배치되게 하라.

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-1.1-2496ED?style=flat-square)](./CHANGELOG.md)
![Profiles](https://img.shields.io/badge/profiles-10-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/selectors-live%20tested%202026--06--18-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="ultimate 셋업 — 역할별 최강 모델" width="100%">

</div>

---

## ⚡ 30초 설치 (한 줄 복붙)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

이 한 줄이 **10개 프로필을 `~/.gjc/agent/models.yml` 에 안전 병합**하고 기본 프로필을 `daily` 로 설정한다. 기존 설정은 자동 백업되며, 재실행해도 깔끔히 갱신된다.

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
5. [최종 카탈로그 10종](#5--최종-카탈로그-10종)
6. [검증 매트릭스](#6--검증-매트릭스)
7. [설치 / 제거](#7--설치--제거)
8. [동적 라우팅 전략](#8--동적-라우팅-전략)
9. [병렬 에이전트 + 신뢰성](#9--병렬-에이전트--신뢰성)
10. [비용](#10--비용)
11. [출처](#11--출처)

---

## 1. 🎯 왜 멀티벤더인가

claude·gpt·grok·gemini·opencode go 를 다 구독해놓고 한 모델만 쓰는 건, 매 역할에서 *차선*을 쓰는 것과 같다. 검증된 벤치마크는 **역할마다 1위 벤더가 다르다**는 걸 보여준다:

| 역할 | 무엇을 하나 | 최적 모델 |
|---|---|---|
| 🧠 **추론·설계**(planner) | 순서·수용기준 짜기 | **Gemini 3.1 Pro** (GPQA 94.3 / ARC-AGI-2 77.1) |
| 🔨 **구현**(executor) | 실제 코드 작성·수정 | **Claude Opus 4.8** (SWE-bench Verified 88.6) |
| 🔭 **코드리뷰**(architect) | 대형 리포 탐색·아키텍처 | **Gemini 3.1 Pro** (멀티모달 MMMU-Pro 81%) · 초장문맥(>200k)은 **Opus** |
| ⚖️ **독립 비평**(critic) | 결과 적대 검증 | **cross-family** (본체와 다른 벤더) |
| 🎛️ **오케스트레이션**(default) | 도구호출·라우팅·정직성 | **Claude Opus 4.8** (라우터 품질 = 전체 상한) |

> 한 벤더로 5역할을 다 채우면 1등이 아닌 자리가 반드시 생긴다. 이 가이드는 그 5자리를 각각의 최적 벤더로 채우되, 비용·접근성·신뢰성까지 따져 **실제로 작동하는 조합**으로 정리한 결과다. GPT-5.5 · Claude Opus 4.8 · Gemini 3.1 Pro 기반 3종 독립 딥리서치를 교차검증하고, **모든 프로필의 셀렉터를 실제 호출로 검증**했다([§6](#6--검증-매트릭스)).

---

## 2. 🧭 핵심 설계

> **강한 본체 1개 고정 (default = Opus) + 작업신호 기반 위임 + 실패신호 기반 effort 에스컬레이션.**

GJC에서 매 작업을 실제로 도는 건 `default`(본체) 하나다. executor/architect/planner/critic 은 본체가 **필요할 때만 `task`로 위임**하는 서브에이전트다(fresh-context).

<div align="center">
<img src="assets/architecture.svg" alt="본체 1개(default) + 서브에이전트 4 — 작업신호 위임" width="100%">
</div>

세 가지 설계 원칙:

- **본체는 절대 양보 불가.** median 작업의 대부분은 본체 혼자 처리하므로, 본체(default)를 약한 모델로 내리면 체감 성능 전체가 무너진다. 항상 Opus.
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

```text
Opus 4.6/4.7/4.8        minimal low medium high xhigh max   ← 6단계 전부
Sonnet 4.6              minimal low medium high              ← xhigh/max 없음
GPT 5.4 / 5.5 (base)    low medium high xhigh                ← 5.5 기본 xhigh
Grok 4.x (4.3 등)       minimal low medium high xhigh
opencode-go deepseek-v4  minimal low medium high xhigh
opencode-go 기타         ── effort 접미사 생략(기본값) ──
google-antigravity Gemini  gemini-3.1-pro-low:high (고추론) · gemini-3.1-pro-low (저효과)
```

> [!IMPORTANT]
> **하드룰 4선**: ① Gemini Pro는 `low`/`high`만 ② openai-codex ctx **272k 상한**(거대 코드베이스 배제) ③ Sonnet `xhigh`/`max` 불가 ④ opencode-go는 `:effort` 생략. 범위 밖 등급은 에러가 아니라 **클램프**된다.

### 3-3. 구독 → 프로바이더

| 구독 | provider-id | 비고 |
|---|---|---|
| claude | `anthropic` | 전 effort |
| gpt | `openai-codex` | **ChatGPT 계정 → base GPT(gpt-5.5/5.4) 제공**. ctx 272k |
| grok | `xai` | 전체 라인업 + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra 구독 토큰**. Gemini + 번들 Claude(Opus 4.6) |
| opencode go | `opencode-go` | API 키(`OPENCODE_API_KEY`) |

> [!NOTE]
> **openai-codex 경로 주의**: ChatGPT(Codex) 계정으로 로그인하면 **base GPT 모델(`gpt-5.5`, `gpt-5.4`)** 이 제공된다. standalone `-codex` 변종(`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex-max/mini`)은 이 경로에서 **미지원**(`not supported when using Codex with a ChatGPT account`)이라, 본 가이드는 코딩 역할도 검증된 **base GPT**로 통일한다.
>
> 대안 경로: `google-vertex`(API 키, 유료 per-token, 1M ctx) — 구독/쿼터 무관 fallback.

### 3-4. 셀렉터 문법

```text
<provider-id>/<model-id>:<effort>            예) anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   (Gemini 고추론 — 엔진 정식 경로)
opencode-go/<model>                           (effort 생략 = 모델 기본값)
```

---

## 4. 📊 벤치마크 근거

**역할별 검증된 1위** (vals.ai 독립보드 · 공식 모델카드 기준)

| 역할(축) | 1위 | 수치 |
|---|---|---|
| executor (SWE-bench Verified) | **Opus 4.8** | 88.6% (GPT-5.5 82.6 · Gemini 3.1 Pro 80.6) |
| planner (추론 GPQA/ARC-AGI) | **Gemini 3.1 Pro** | GPQA 94.3 · ARC-AGI-2 77.1 |
| architect (ctx·멀티모달) | **Gemini 3.1 Pro** | 1M ctx · MMMU-Pro 81% |
| default (툴콜·정직성) | **Opus 4.8** | 라우터 품질 = 전체 상한 |
| critic (독립성) | **cross-family** | 메타-심판 > 토론형 집계 |

**핵심 합의 원칙**

1. **default = Opus 4.8 고정**(멀티벤더 프로필) — 라우터 품질이 전체 품질 상한. solo-* 는 단일 벤더 최강을 default로.
2. **architect = Gemini 3.1 Pro(멀티모달) / Opus(초장문맥)** — Gemini는 비전·중간 ctx 최적, 200k+ 텍스트 실효검색은 Opus(MRCR 76%@1M, Gemini는 26%로 붕괴).
3. **critic = cross-family** — 본체/플래너와 다른 벤더여야 편향이 완화된다(self-preference bias).
4. **구조 = 강본체 + 작업신호 위임 + 실패기반 effort 에스컬레이션.**
5. **매 쿼리 프로필 스왑 ❌** — 캐시 손실 > 이득. 모드 경계에서만 스왑.

> 벤치마크는 시점 민감하다 → 분기별 재검증 권장. 절대순위는 vals.ai 독립보드로 한정.

---

## 5. 🗂️ 최종 카탈로그 10종

<div align="center">
<img src="assets/profiles-matrix.svg" alt="7 프로필 × 5 역할 매트릭스" width="100%">
</div>

> ★ = 평소 권장. 상단 배너 = **`ultimate` 셋업**(역할별 최강 · 정확성 우선). 그걸 비용 균형으로 낮춘 게 평소 권장 **`daily`**(executor·critic만 저가로 교체). 멀티벤더 프로필은 `default=Opus 고정`·`critic=cross-family`(solo-* 는 단일 벤더 최강), 전부 엔진 effort 하드룰 통과 + **모든 셀렉터 실호출 검증**([§6](#6--검증-매트릭스)).

| 프로필 | 한 줄 정의 | 이럴 때 |
|---|---|---|
| ⭐ **daily** | 본체 Opus + 위임을 역할별 최적 벤더로 | **평소 기본** |
| 🏆 **ultimate** | 비용 무시, 역할별 최강 | 정확성이 비용보다 중요 |
| 🏎️ **coding-sprint** | executor 주연 + 코딩인지 critic | 순수 구현 처리량 |
| 🛡️ **escalation** | 전역 최대 등급 + critic 멀티벤더 패널 | 머지·보안·결제·비가역 변경 |
| 💸 **eco** | 본체만 Opus, 위임은 전부 저가/구독 모델 | 비용 압박·대량 작업 |
| 🗺️ **monorepo** | 전역 ≥1M ctx (codex 배제) | 거대 코드베이스 |
| 🧱 **solo-anthropic** | 전 역할 Anthropic | 단일 벤더로만 운영 |
| 🤖 **solo-openai** | 전 역할 base GPT (ctx 272k) | ChatGPT만 구독 |
| 🤝 **claude-codex** | Claude=실행·ctx / Codex=추론·비평 | Claude+Codex 2구독만 |
| 🥇 **claude-codex-max** | claude-codex 비용무시 최강판 | Claude+Codex · 정확성 우선 |

<details>
<summary><b>📋 전체 YAML 펼치기 (gjc-profiles.yml 와 동일)</b></summary>

```yaml
profiles:

  daily:                               # ★ 평소 기본 (--default daily)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 본체 효율 knee
      executor:  openai-codex/gpt-5.4:high                      # 코딩특화·중가($2.5/15)·벤더분산
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 추론 검증1위(GPQA 94.3 / ARC-AGI-2 77.1)
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx·멀티모달(MMMU-Pro 81%)
      critic:    xai/grok-4.3:medium                            # cross-family 저가 독립비평($1.25/2.5)

  ultimate:                            # 비용무시, 역할별 최강 + 벤더분산
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # 접근가능 코딩 1위(SWE-bench Verified 88.6)
      planner:   openai-codex/gpt-5.5:xhigh                     # 최상위 추론 + OpenAI 다양성
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx·멀티모달
      critic:    xai/grok-4.3:high                              # cross-family 독립비평

  coding-sprint:                       # 순수 구현 처리량. executor 주연 + 코딩인지 critic
    required_providers: [anthropic, openai-codex, google-antigravity]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 본체 오케스트레이션
      executor:  anthropic/claude-opus-4-8:max                  # 접근가능 코딩 1위(88.6)
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 추론 검증1위로 경량 계획
      architect: google-antigravity/gemini-3.1-pro-low:high     # 1M ctx 리뷰
      critic:    openai-codex/gpt-5.4:high                      # 코딩인지 critic(실버그 포착), cross-family vs gemini

  escalation:                          # 고실패비용. 전역 최대 + critic 멀티벤더 병렬패널(§9)
    required_providers: [anthropic, openai-codex, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max
      planner:   openai-codex/gpt-5.5:xhigh
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    xai/grok-4.3:xhigh                             # + 3표 교차벤더 critic 패널(독립투표→본체집계)

  eco:                                 # 최저가 — 본체만 Opus(effort 절감), 위임은 초저가/구독 모델
    required_providers: [anthropic, opencode-go, google-antigravity, xai]
    model_mapping:
      default:   anthropic/claude-opus-4-8:low                  # 라우터는 못 내림, effort만 절감
      executor:  opencode-go/deepseek-v4-flash                  # $0.14/0.28, 1M, 최저가 코더(5번째 벤더)
      planner:   xai/grok-4-1-fast:high                         # $0.2/0.5, 2M, 저가 추론
      architect: google-antigravity/gemini-3.1-pro-low          # 구독 토큰, 저effort, 1M ctx
      critic:    google-antigravity/gemini-3.5-flash            # 구독 토큰, 경량, cross-family vs executor(opencode-go)

  monorepo:                            # 거대 코드베이스 — 전역 1M ctx (★codex 272k 배제)
    required_providers: [anthropic, google-antigravity, opencode-go]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 1M
      executor:  anthropic/claude-opus-4-8:high                 # 1M
      planner:   google-antigravity/gemini-3.1-pro-low:high     # 추론(스코프 입력)
      architect: anthropic/claude-opus-4-8:high                 # Opus 4.8 = GJC 1M ctx 윈도우 지원(멀티턴 누적·검색 최상). 단일 메시지 paste만 ~400k 한도 — 한 방에 >400k는 opencode-go/deepseek-v4-pro
      critic:    opencode-go/glm-5.2                            # 신규 오픈웨이트 1위(AA 51 > V4 Pro 44), cross-family vs anthropic (대안: deepseek-v4-pro)

  solo-anthropic:                      # 단일 벤더로만 운영, 신뢰성 곱셈붕괴(0.99^N) 회피
    required_providers: [anthropic]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max
      planner:   anthropic/claude-opus-4-8:max
      architect: anthropic/claude-opus-4-8:high                 # 1M, Gemini 대체(폴백 1순위)
      critic:    anthropic/claude-sonnet-4-6:high               # ⚠동일벤더=독립성 약함(트레이드오프)

  solo-openai:                         # ChatGPT(Codex) 계정만 — base GPT 전용 (★ctx 272k 상한)
    required_providers: [openai-codex]
    model_mapping:
      default:   openai-codex/gpt-5.5:high                      # 라우터(base GPT 최강)
      executor:  openai-codex/gpt-5.5:xhigh                     # 이 계정 최강 코더
      planner:   openai-codex/gpt-5.5:xhigh                     # 최상위 추론
      architect: openai-codex/gpt-5.4:high                      # 272k 상한 — 거대 코드베이스엔 부적합
      critic:    openai-codex/gpt-5.4:high                      # ⚠동일벤더=독립성 약함(트레이드오프)

  claude-codex:                        # ★2벤더(Claude+Codex)만 — 평소 균형. Anthropic=실행·ctx / Codex=추론·비평
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:medium               # 라우터·툴신뢰
      executor:  anthropic/claude-opus-4-8:high                 # 코딩 1위(SWE-bench 88.6)
      planner:   openai-codex/gpt-5.5:high                      # OpenAI 추론 플래그십
      architect: anthropic/claude-opus-4-8:high                 # 1M 윈도우(codex 272k 한계 회피)
      critic:    openai-codex/gpt-5.4:high                      # cross-family vs Opus(executor), 코딩인지

  claude-codex-max:                    # 2벤더(Claude+Codex) 최강 — 비용 무시
    required_providers: [anthropic, openai-codex]
    model_mapping:
      default:   anthropic/claude-opus-4-8:high
      executor:  anthropic/claude-opus-4-8:max                  # SWE-bench 88.6 코딩 1위
      planner:   openai-codex/gpt-5.5:xhigh                     # 최상위 추론(ARC-AGI-2 강)
      architect: anthropic/claude-opus-4-8:high                 # 1M 윈도우
      critic:    openai-codex/gpt-5.5:high                      # cross-family 독립 비평 vs Opus
```

</details>

> [!TIP]
> **opencode-go** 는 `OPENCODE_API_KEY` 설정 시 `eco`(executor)·`monorepo`(critic)에서 활성화된다(검증✅). grok 구독(SuperGrok)의 `xai/grok-composer-2.5-fast`(200k)도 검증됨 — throughput용 대안. 다른 opencode-go 모델(qwen3.7-max·kimi-k2.6·glm-5.1·minimax-m2.7·mimo-v2.5)도 전부 동작 확인.

#### 프로필별 설계 근거

- **daily** — 본체 Opus `:medium`(효율 knee), 구현은 코딩특화 `gpt-5.4`, 설계·리뷰는 추론/ctx 1위 Gemini, 비평은 저가 독립 Grok. 일상 작업의 품질/비용 균형점.
- **ultimate** — 비용을 포기하고 executor까지 Opus `:max`. planner는 OpenAI 다양성을 위해 `gpt-5.5:xhigh`.
- **coding-sprint** — executor 주연(Opus `:max`), 계획·리뷰는 가볍게, critic은 *코딩을 아는* `gpt-5.4`로 실버그를 잡는다(cross-family vs gemini).
- **escalation** — 전역 최대 등급 + critic 멀티벤더 3표 패널([§9](#9--병렬-에이전트--신뢰성)). 되돌릴 수 없는 변경 전용.
- **eco** — 본체만 Opus(`:low`), executor는 최저가 `deepseek-v4-flash`(opencode-go — 5번째 벤더 활용), planner는 초저가 Grok Fast, architect/critic은 구독 토큰 Gemini. critic(Gemini)은 executor(opencode-go)와 cross-family.
- **monorepo** — 전 역할이 1M ctx. openai-codex(272k)는 의도적으로 배제. architect=**Opus**(1M 실효검색 1위 **76%@1M** — Gemini는 26%로 붕괴, Grok은 멀티모달 약함), critic=`deepseek-v4-pro`(cross-family). 1M 토큰을 넘는 코드베이스는 architect를 `xai/grok-4-fast`(2M, 실효 미검증)로 swap.
- **solo-anthropic** — 단일 벤더 운영. critic이 동일 벤더라 독립성은 약함(명시적 트레이드오프).
- **solo-openai** — ChatGPT(Codex) 계정만 쓰는 사용자용. 전 역할을 base GPT(gpt-5.5/5.4)로 — `-codex` 변종은 이 계정에서 미지원이라 제외. ctx 272k 상한이라 거대 코드베이스엔 부적합하고, critic이 동일 벤더라 독립성은 약함.
- **claude-codex** — Claude+Codex **2구독만** 보유한 사용자용 Best 믹스. **Anthropic = 실행·컨텍스트**(default·executor·architect: Opus가 코딩 1위 SWE-bench 88.6 + 1M 윈도우 — codex는 272k라 대형 ctx는 Opus가 유일), **Codex = 추론·비평**(planner: GPT-5.5 추론 플래그십 / critic: GPT가 Opus executor를 cross-family 독립 비평). 2벤더로도 5역할 cross-family critic 성립.
- **claude-codex-max** — 위를 비용 무시로 끌어올린 최강판(executor Opus `:max`, planner `gpt-5.5:xhigh`).

---

## 6. ✅ 검증 매트릭스

> 모든 셀렉터를 이 환경에서 `gjc -p --no-session --no-tools --model <sel> "..."` 로 **실제 호출**해 동작을 확인했다(2026-06-18). "동작함"의 근거는 추정이 아니라 실호출이다.

| 프로바이더 | 검증된 셀렉터 (✅ 동작) |
|---|---|
| `anthropic` | `claude-opus-4-8`(low·medium·high·max) · `claude-sonnet-4-6:high` |
| `openai-codex` | `gpt-5.5`(high·xhigh) · `gpt-5.4:high` · `gpt-5.4-mini:high` |
| `xai` | `grok-4.3`(high·xhigh) · `grok-4-1-fast:high` · `grok-4-fast:high` · `grok-code-fast-1` · `grok-composer-2.5-fast` |
| `google-antigravity` | `gemini-3.1-pro-low` · `gemini-3.1-pro-low:high` · `gemini-3.5-flash` · `gemini-3-flash` · `claude-opus-4-6-thinking` |
| `opencode-go` | `deepseek-v4-flash` · `deepseek-v4-pro` · `glm-5.2` · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` (`OPENCODE_API_KEY` 필요) |

> [!WARNING]
> **이 환경에서 동작하지 않은 셀렉터**(피하라): `openai-codex/gpt-5.3-codex`·`gpt-5.2-codex`·`gpt-5.1-codex-max`·`gpt-5.1-codex-mini`(ChatGPT 계정 미지원) · `google-antigravity/gemini-3.1-pro-high`(엔진은 `gemini-3.1-pro-low:high` 사용) · `gemini-3-pro`(은퇴) · `claude-sonnet-4-6-thinking`(404) · `gpt-oss-120b`(500). `opencode-go/*` 는 `OPENCODE_API_KEY` **미설정 시에만** 실패한다(키 설정 후 위 표대로 동작).

재현:
```bash
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.4:high" "Reply exactly: OK"
```

---

### 6-2. 역할 배치 최적성 검토 (deep-research + 실측)

8프로필의 역할→모델 배치를 다회차 deep-research(독립 벤치 검증)와 라이브 추론 프로브로 재검토한 결과, 골격은 near-optimal로 확인됐다.

- **`gemini-3.1-pro-low:high` 는 저하 모드가 아니다.** `thinkingLevel`은 별도 모델 변종이 아니라 동일 Gemini 3.1 Pro에 적용되는 per-request 파라미터이고 모델 기본값이 **HIGH**다. 공식 모델카드의 헤드라인 추론 점수(GPQA 94.3 · ARC-AGI-2 77.1)는 전부 *Thinking (High)* 에서 측정됐다 — 이 셀렉터는 **네이티브 고추론 기본모드**를 호출한다. 실측 프로브: `low`(18s) → `low:high`(22s) 지연 증가로 thinking 활성 확인, 표준 추론 정답은 GPT-5.5·Opus와 동일. *(잔여: GJC `:high` override의 네이티브 HIGH 매핑은 1차 출처 미확증 → 운영 중 추론 품질 모니터링 권장.)*
- **planner 추론 축은 분열한다.** GPQA Diamond(과학지식)는 Gemini 3.1 Pro 1위지만 상위권이 93~95%로 *saturated*(통계적 우위 미미). ARC-AGI-2(추상·유동추론)는 **GPT-5.5가 명확히 앞선다**(0.850 vs 0.771). 플래닝에 더 직결되는 유동추론(ARC) 기준 → ultimate/escalation `planner=GPT-5.5` 유지. **과학지식추론 비중이 크면 `planner → google-antigravity/gemini-3.1-pro-low:high`로 swap.**
- **executor=Opus 우위는 SWE-bench 축 한정.** vals.ai SWE-bench Verified Opus 4.8 88.6 > GPT-5.5 82.6로 유지되나 DeepSWE/Terminal-Bench에선 GPT-5.5가 앞선다 — repo-스케일 버그픽스=Opus, 터미널·에이전틱=GPT-5.5도 고려.
- **xAI `grok-composer-2.5-fast`·`grok-code-fast-1` 은 eco·throughput 전용.** 독립 벤치 미공개/인플레이션으로 프론티어 코더가 아니며 grok-code-fast-1은 은퇴 예정 — executor 코어 비포함이 맞다.
- **default=Opus** 는 Vals Index 종합(서빙 모델 중 1위)으로 재확인.
- **architect 장문맥 정정**: Gemini의 명목 1M은 실효 1M이 아니다 — MRCR v2 8-needle 128K 84.9% → 1M **26.3%** 붕괴, 반면 **Opus 4.6은 1M 76% 유지**(4.8 수치는 미공개). Grok 4.3 멀티모달은 12/16 하위권이라 비전 architect엔 부적합 → **monorepo architect를 Grok→Opus로 교정**했고, 표준 프로필 architect=Gemini는 멀티모달·중간 ctx 한정 최적이다. (GJC 경유 실효 상한은 [§6-3](#6-3-잔여-공백-검토-gap-13--gjc-실효-컨텍스트-실측) 참조.)

> 출처: [vals.ai GPQA](https://www.vals.ai/benchmarks/gpqa) · [vals.ai SWE-bench](https://www.vals.ai/benchmarks/swebench) · [vals.ai MMMU](https://www.vals.ai/benchmarks/mmmu) · [Gemini 3.1 Pro card (MRCR)](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini thinking docs](https://ai.google.dev/gemini-api/docs/thinking) · [Opus 4.6 (MRCR 76%@1M)](https://www.anthropic.com/news/claude-opus-4-6) · [long-context 보드](https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/) · [llm-stats ARC-AGI-2](https://llm-stats.com/benchmarks/arc-agi-v2) · [xAI Composer 2.5](https://x.ai/news/composer-2-5)

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

> 핵심: Opus 4.8 컨텍스트 윈도우는 GJC에서 **1M 정상**(멀티턴 누적). 단일 메시지로 한 방에 넣을 수 있는 양만 ~400k(Opus/Gemini) — 그 이상 **단일 paste**는 Grok/DeepSeek이 견고하다(실측). **거대 입력은 한 메시지에 통째로 붓지 말고 청크로 나눠 누적하면 1M 윈도우를 그대로 활용**할 수 있다. (이 표는 GJC 내부에서 독립 재검증 통과 — 20/20 일치, 2026-06-18.) 출처: [Context Arena](https://contextarena.ai/) · [GLM-5.2 (AA)](https://artificialanalysis.ai/models/glm-5-2) · [Opus 4.8 what's-new](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)

---

## 7. 🛠️ 설치 / 제거

### 원클릭 (권장)

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

설치기가 하는 일: `~/.gjc/agent/models.yml` 에 10개 프로필 안전 병합(재실행 시 자동 갱신) · 기존 파일 자동 백업 · 기본 프로필 `daily` 설정. `curl` + `python3` 만 있으면 된다.

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

---

## 8. 🔀 동적 라우팅 전략

> **"쿼리마다 프로필 교체" ❌ / "강본체 1개 + 가벼운 룰 1겹" ✅.** 라우팅 주체는 본체(Opus), 프로필은 목적지 풀이다.

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
- critic 패널 예: `{xai/grok-4.3, openai-codex/gpt-5.4, google-antigravity/gemini-3.1-pro-low:high}` 동시 → 2/3 반박 시 폐기.
- executor fan-out은 **작업이 진짜 독립**(공유 상태 없음)일 때만.
- 체인은 짧게, 본체를 단일 진실원천으로(서브끼리 직접 합의 금지).

---

## 10. 💰 비용

Gemini(`google-antigravity`)는 **Google AI Pro/Ultra 구독 토큰**으로 동작한다(per-token 청구가 아니라 구독에 포함). 나머지는 per-token 과금이며, 주요 모델 단가는 다음과 같다($/1M, 입력/출력):

| 모델 | $/1M (in/out) | 역할 |
|---|---|---|
| Claude Opus 4.8 | 5 / 25 | default·executor |
| Claude Sonnet 4.6 | 3 / 15 | solo critic |
| GPT-5.5 | 5 / 30 | planner(ultimate) |
| GPT-5.4 | 2.5 / 15 | executor/critic(daily·sprint) |
| Grok 4.3 | 1.25 / 2.5 | critic |
| Grok 4.1 Fast | 0.2 / 0.5 | eco planner |
| DeepSeek V4 Flash / Pro (opencode-go) | 0.14/0.28 · 1.74/3.48 | eco executor · monorepo critic |
| Gemini 3.1 Pro / 3.5 Flash | 구독 토큰 | planner·architect·critic |

**프로필 상대 비용**

| 프로필 | 비용 | 핵심 비용 동인 |
|---|---|---|
| ultimate / escalation | ●●●●● | executor Opus `:max` + planner GPT-5.5 `:xhigh` |
| coding-sprint | ●●●●○ | executor Opus `:max` |
| daily | ●●●○○ | 본체 Opus `:medium`, 위임은 중·저가로 분산 |
| monorepo | ●●●○○ | executor Opus + Grok/Gemini(구독) |
| solo-anthropic | ●●●○○ | 전부 Opus(critic만 Sonnet) |
| eco | ●○○○○ | executor DeepSeek V4 Flash($0.14) + 구독 Gemini |

> **3대 절감 레버**: ① 위임 work를 초저가 모델(DeepSeek V4 Flash $0.14, Grok Fast $0.2)·구독 토큰(Gemini)으로 ② 실패 시에만 effort 격상 ③ 본체(Opus)는 품질 상한이라 유지하되 일상은 `:medium`, 비용압박 시 `:low`.

---

## 11. 📖 출처

**코딩(executor)** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.0](https://www.tbench.ai/leaderboard/terminal-bench/2.0)

**추론(planner)** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

**ctx·멀티모달(architect)** · [Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/)

**툴콜·정직성(default)** · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [τ²-Bench](https://arxiv.org/abs/2506.07982)

**독립성·라우팅(critic+설계)** · [self-preference bias](https://arxiv.org/abs/2410.21819) · [Judging with Many Minds](https://arxiv.org/abs/2505.19477) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)

**공식 모델/가격** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

---

<div align="center">

**한 줄로 설치하고, 역할마다 최적 모델로.**

**v1.1** · [CHANGELOG](./CHANGELOG.md) · 라이선스 [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
