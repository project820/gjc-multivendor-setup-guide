<div align="center">

# 🧩 GJC 멀티벤더 극한 셋업

### claude · gpt · grok · gemini · opencode go — 5개 구독을 *역할별로* 쪼개 쓰는 검증된 설정

복잡한 모델 선택을 고민하지 말고, **한 줄로 설치**해 역할마다 최적 모델이 자동으로 배치되게 하라.

[![GJC](https://img.shields.io/badge/for-Gajae%20Code%20(GJC)-e23?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code)
[![Version](https://img.shields.io/badge/version-2.0.1-2496ED?style=flat-square)](./CHANGELOG.md)
[![Upstream](https://img.shields.io/badge/upstream-merged%20into%20GJC%20docs-brightgreen?style=flat-square)](https://github.com/Yeachan-Heo/gajae-code/pull/860)
![Profiles](https://img.shields.io/badge/bundles-10%20·%204%20tiers-blue?style=flat-square)
![Vendors](https://img.shields.io/badge/vendors-5-success?style=flat-square)
![Verified](https://img.shields.io/badge/rerun-all%20providers%202026--07--10-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey?style=flat-square)

<img src="assets/role-winners.svg" alt="dream-team 셋업 — 역할별 최강 가설" width="100%">

</div>

**한국어 (이 문서) · [English](./README.en.md) · [中文](./README.zh.md) · [日本語](./README.ja.md)**

> [!NOTE]
> 핵심 역할·셀렉터 개념은 [GJC 공식 문서](https://github.com/Yeachan-Heo/gajae-code/blob/dev/docs/multi-vendor-profiles.md)에 업스트림 머지됐다([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev`). 이 레포는 원클릭 설치, 4계층 10번들 카탈로그와 [유지보수·검증 도구](./MAINTAINING.md)를 제공한다.

---

## ⚡ 30초 설치

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
```

이 한 줄이 **10개 번들을 `~/.gjc/agent/models.yml` 에 안전 병합**하고 기본 프로필을 `daily` 로 설정한다. 기존 설정은 자동 백업되며, 재실행해도 깔끔히 갱신된다.

```bash
gjc --mpreset daily        # 이번 세션만 적용
gjc                        # 새 세션은 자동으로 daily 사용
```

> [!IMPORTANT]
> **설치 후 프로바이더 로그인이 필요하다.** GJC OAuth는 네이티브 `agy`/`grok` CLI 로그인과 공유되지 않는다. GJC에서 아래를 한 번씩 실행하라:
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

## 🧭 어떤 번들을 쓸까?

| Tier | 번들 | 한 줄 정의 | 이럴 때 |
|---|---|---|---|
| Core | ⭐ **daily** | 본체 Opus + 위임 역할별 분산 — **구독 OAuth 3벤더만으로 activation** | **평소 기본** |
| Core | 🏎️ **coding-sprint** | executor 를 Opus 로 승격한 구현 처리량 특화 | 순수 구현 스프린트 |
| Core | 🚨 **cyber-cop** | reviewer 모드 — architect·critic 주연, PR 리뷰·보안 감사 전용 | 남의 PR 검토·머지 게이트·보안 감사 |
| Premium (exp) | 🏆 **ultimate-opus** | Anthropic 품질 기저 프리미엄 | 정확성이 비용보다 중요 |
| Premium (exp) | 🧪 **ultimate-sol** | Sol 기저 프리미엄 — agentic/터미널/브라우징 축 | 장기 자율 워크플로 실험 |
| Premium (exp) | 🔥 **dream-team** | 역할별 최강 가설 — Fable default+executor | 최고 품질, credits 각오 |
| Workflow | 🏛️ **llm-council** | 4계열 좌석표와 Council 계약 | 다계열 합의가 필요한 결정 |
| Workflow | 🛡️ **escalation** | 수동 에스컬레이션 — Fable 구원투수 + critic 3표 패널 | 머지·보안·결제·비가역 변경 |
| Specialized (exp) | 💸 **eco** | 멀티벤더 저단가 실험 — *절대 최저가 아님* | 비용 압박·대량 작업 |
| Specialized (exp) | 🗺️ **monorepo** | 전역 ≥1M ctx | 거대 코드베이스 |

전체 카탈로그 ↓ [§5](#5-️-최종-카탈로그--10-번들--4계층) · reviewer 모드·티저는 아래 참조.

> **🚨 cyber-cop** — GJC 최초 reviewer 모드: architect·critic이 주연이고 executor는 재현 조연이다. 고위험 PR은 3표 패널로 판정하며, PR #4~#7에서 머지 전 결함 10건을 차단했다.
> 설치: `curl -fsSL …/install.sh | GJC_SETUP_COP=1 bash` → `gjc-cop 123`
> → [공지 문서](./docs/whats-new-cyber-cop.md)

> **Extragoal — GPT-5.5 Pro 최종리뷰 레인 (opt-in)** — Pro 심층 추론을 개발·QA·보안점검의 회전수-1 판정석에 투입한다. 상류 기본 레인은 이것 없이도 동작하며, `GJC_SETUP_EXTRAGOAL=1`로 설치한다.
> → [Extragoal Maximalist 문서](./docs/extragoal-maximalist.md)

---

## 📑 목차

- [⚡ 30초 설치](#-30초-설치)
- [🧭 어떤 번들을 쓸까?](#-어떤-번들을-쓸까)
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

| 역할 | 무엇을 하나 | 최적 모델 |
|---|---|---|
| 🧠 **추론·설계**(planner) | 순서·수용기준 짜기 | **GPT-5.6 Sol** (Agents' Last Exam 52.7 · 2026-07-09 GA) — 번들별 좌석은 [§5](#5-️-최종-카탈로그--10-번들--4계층) 참조(예외: cyber-cop·monorepo=Gemini, eco=Luna) |
| 🔨 **구현**(executor) | 실제 코드 작성·수정 | **Claude Fable 5** (SWE-bench Verified **95.0**) — 구독 포함 최강은 **Opus 4.8**(88.6) |
| 🔭 **코드리뷰**(architect) | 대형 리포 탐색·아키텍처 | **Gemini 3.1 Pro** (멀티모달 MMMU-Pro 81%) · 초장문맥(>200k)은 **Opus** |
| ⚖️ **독립 비평**(critic) | 결과 적대 검증 | **cross-family** (본체와 다른 벤더) |
| 🎛️ **오케스트레이션**(default) | 도구호출·라우팅·정직성 | **Anthropic 플래그십** — Opus 4.8 (라우터 품질 = 전체 상한; `dream-team`은 Fable 5. 비-Anthropic 라우터는 opt-in `ultimate-sol`(Sol)과 Anthropic 미포함 `eco`(Terra)뿐) |

---

## 2. 🧭 핵심 설계

> **강한 본체 1개 고정 (default = Anthropic 플래그십 Opus/Fable) + 작업신호 기반 위임 + 실패신호 기반 effort 에스컬레이션.**

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

### 하드룰 5선

1. Gemini Pro는 `low`/`high`만 — 고추론은 `gemini-3.1-pro-low:high` 리터럴 핀(0.9.6부터 퍼지 공간 fail-closed — 잘못된 id는 "not found").
2. openai-codex ctx는 **모델별** — `gpt-5.4`=**1M** · `gpt-5.5`=**272K** · `gpt-5.6 3종`=**373K**(0.9.6에서 272K→373K; API 스펙 1.05M과 별개의 usable prompt budget).
3. Sonnet(4.6/5)은 GJC에서 `xhigh`/`max` 불가 · **Fable 5는 `max` 불가**(각각 high/xhigh로 클램프).
4. opencode-go는 `:effort` 생략(deepseek-v4 계열만 예외적으로 지원).
5. xai `grok-4.5` 상한은 `high`(`:xhigh` 침묵 클램프; xhigh는 grok-build 전용이나 그쪽은 effort 서픽스를 해석하지 않음). 범위 밖 등급은 에러가 아니라 **클램프**되고, gpt-5.6 3종 `:max`는 수용되나 심도 미검증이므로 출하 상한은 `xhigh`다.

> **각주(상류 갭)**: Claude 5 패밀리는 API 공식으로는 둘 다 `max`까지 지원한다. GJC 파서(0.9.1~0.9.6)의 fable 폴백·sonnet-5의 4.6 클램프 상속은 **엔진 쪽 갭**이며 재현 자료와 함께 상류에 제보됐다.

### 3-3. 구독 → 프로바이더

| 구독 | provider-id | 비고 |
|---|---|---|
| claude | `anthropic` | 전 effort. Claude 5 패밀리(Fable 5·Sonnet 5) 포함 |
| gpt | `openai-codex` | **ChatGPT 계정 → base GPT(gpt-5.6 sol/terra/luna · 5.5 · 5.4) 제공**. ctx: gpt-5.4=1M · 5.5=272K · 5.6 3종=373K |
| grok | `xai` | 전체 라인업 + Composer |
| gemini | `google-antigravity` | **Google AI Pro/Ultra 구독 토큰**. Gemini + 번들 Claude(Opus 4.6 — 2026-07-02 기준, 이후 번들 구성 미재확인) |
| opencode go | `opencode-go` | API 키(`OPENCODE_API_KEY`) |

> [!NOTE]
> ChatGPT(Codex)는 base GPT만 제공하며 standalone `-codex` 변종은 미지원이다. `google-vertex`·DeepInfra는 API 키 유료 대안이다.

### 3-4. 셀렉터 문법

```text
<provider-id>/<model-id>:<effort>            예) anthropic/claude-opus-4-8:high
google-antigravity/gemini-3.1-pro-low:high   (Gemini 고추론 — 엔진 정식 경로)
opencode-go/<model>                           (effort 생략 = 모델 기본값)
```

---

## 4. 📊 벤치마크 근거

| 역할(축) | 1위 | 수치 |
|---|---|---|
| executor (SWE-bench Verified) | **Fable 5** | **95.0%** (Opus 4.8 88.6 = **구독 포함 최강** · GPT-5.5 82.6 · Gemini 3.1 Pro 80.6) |
| planner (장기 워크플로·추론) | **GPT-5.6 Sol**† | Agents' Last Exam 52.7(5.5: 46.9) · AA Intelligence 58.9 — GPQA 단독 1위는 Sonnet 5 96.2 · 과학지식 특화는 Gemini 3.1 Pro 94.3 ([§6-2](./docs/deep-dive-role-fit.md#6-2-역할-배치-최적성-검토-deep-research--실측)) |
| architect (ctx·멀티모달) | **Gemini 3.1 Pro**† | 1M ctx · MMMU-Pro 81% |
| default (툴콜·정직성) | **Opus 4.8 / Fable 5** | 라우터 품질 = 전체 상한 (Fable은 refusal·과금 캐비앗 — [§5](#5-️-최종-카탈로그--10-번들--4계층)) |
| critic (독립성) | **cross-family** | 메타-심판 > 토론형 집계 |

**핵심 합의 원칙** — † planner는 2026-07-10 Sol GA를 반영해 2026-07-02 Gemini 3.1 Pro 스냅샷을 대체했고, architect 축은 Gemini 3.5 Pro 출시 시 재검증한다.

1. **default = Anthropic 플래그십(Opus/Fable) 고정** — 라우터 품질이 전체 품질 상한. 예외 둘: `ultimate-sol`(Sol 라우터 — validator 등재 + WARN 표면화 opt-in 실험) · `eco`(Anthropic 미포함 번들 — Terra 라우터, router 불변식 비적용).
2. **architect = Gemini 3.1 Pro(멀티모달) / Opus(초장문맥)** — Gemini는 비전·중간 ctx 최적, 200k+ 텍스트 실효검색은 Opus(MRCR 76%@1M, Gemini는 26%로 붕괴).
3. **critic = cross-family** — 본체/플래너와 다른 벤더여야 편향이 완화된다(self-preference bias).
4. **구조 = 강본체 + 작업신호 위임 + 실패기반 effort 에스컬레이션.**
5. **매 쿼리 프로필 스왑 ❌** — 캐시 손실 > 이득. 모드 경계에서만 스왑.

---

## 5. 🗂️ 최종 카탈로그 — 10 번들 · 4계층

<div align="center">
<img src="assets/profiles-matrix.svg" alt="프로필 × 역할 매트릭스" width="100%">
</div>

> ★ = 평소 권장. v2.0.0은 동등한 프로필 묶음이 아니라 4계층 10번들이다. 전 번들 `required_providers ≥ 2`, 기본 `critic=cross-family`(예외는 `SAME_FAMILY_OK`+WARN), 엔진 effort 하드룰과 셀렉터 검증([§6](#6--검증-매트릭스))을 따른다. 2026-07-10 gjc **0.9.6** 배터리에서 출하 좌석은 그린이었다.

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

<details>
<summary><b>v1.11 → v2 마이그레이션</b></summary>

`ultimate`→`ultimate-opus`, `ultimate-f5`/`legend`→`dream-team`; `llm-council`·`ultimate-sol`은 신설됐다. `solo-anthropic`/`solo-openai`/`claude-codex`/`claude-codex-max`는 v2의 멀티벤더 원칙에 따라 제거했고, 해당 수요는 GJC 0.9.6 내장 `claude-*`·`codex-*`·`opus-codex`·`fable-opus-codex`가 흡수한다(매핑 등가 아님). 세부 diff는 [CHANGELOG](./CHANGELOG.md)와 [v2 안내](./docs/whats-new-v2.md)를 참조.
</details>

> [!TIP]
> **opencode-go** 는 `OPENCODE_API_KEY` 설정 시 `eco` executor·`monorepo` critic에서 활성화된다(검증✅). `deepseek-v4-flash/pro`·`glm-5.2`는 검증됐고, 신규 입점 후보 `kimi-k2.7-code`·`minimax-m3`는 미검증이다.

#### 프로필별 설계 근거

- **daily** — Opus `:medium`·Terra·Sol·Gemini의 일상 균형점; ⚠ architect·critic 동일 Gemini는 구독 OAuth 3벤더 제약에서 의도 수용(독립성 강화는 xai critic 스왑).
- **coding-sprint** — Opus `:high` executor와 Sol 분해의 구현 처리량 번들; ⚠ planner/critic GPT 계열은 2026-07-10 `SAME_FAMILY_OK`(Sol≠Terra, 전체 3벤더).
- **cyber-cop** — Opus architect 1차 판정·Sol critic 머지 게이트의 reviewer 모드; 고위험은 3표 독립 패널로 반대 근거를 찾는다.
- **ultimate-opus** — Opus 3좌석의 안정성·1M을 Sol planner·Grok critic이 보완한다; ⚠ 같은 Claude 계열은 `SAME_FAMILY_OK`이며 세 독립 의견이 아니다.
- **ultimate-sol** — Sol 장기 워크플로·터미널·브라우징 3좌석 experimental; ⚠ 유일한 비-Anthropic default(`NON_ANTHROPIC_DEFAULT_OK`), ctx 373K와 METR SWE 게이밍으로 SWE 단독근거 금지.
- **dream-team** — Fable default+executor, Sol·Opus·Grok의 최고품질 가설; ⚠ ~7/12 23:59 PT 뒤 credits $10/$50, HTTP 200 refusal·30-day retention·ZDR 불가, Claude 계열은 `SAME_FAMILY_OK`.
- **llm-council** — Google·xAI·OpenAI가 판정하고 Anthropic은 raw verdict를 보존하는 집계자; [`routing-rules.md`](./routing-rules.md)의 Council 계약(독립호출·quorum)이 필요하다.
- **escalation** — 실패 뒤 Fable `:xhigh`와 3표 critic을 쓰는 수동 게이트; Escalation 계약이 트리거·human gate를 정하고 refusal 시 Opus `:max`로 강등한다.
- **eco** — Terra·DeepSeek·Luna·Gemini 저단가 실험(절대 최저가는 내장 `codex-eco`); `grok-4-1-fast` retire/redirect 뒤 critic은 07-10 `gemini-3-flash:low`로 교체됐다.
- **monorepo** — Opus architect·GLM-5.2 critic의 1M ctx 번들; 완전 recall이 아니므로 청크 누적하고 >~400k paste만 DeepSeek V4 Pro를 쓴다.

---

## 6. ✅ 검증 매트릭스

> 범례: ✅ 실호출 그린(괄호=검증일) · 🔴 실패 · ⚠ 주의/클램프 · †‡ 각주 · ●○ 상대비용.
> 2026-07-10 gjc **0.9.6**에서 전 프로바이더 핵심 셀렉터를 `gjc -p --no-session --no-tools --model <sel> "..."`로 실호출했다([rerun-3](./evidence/2026-07-10-selectors-rerun-3.md); 0.9.5 그린은 rerun-2). v2 출하 좌석은 전부 그린이며, 당일 antigravity 드리프트로 eco.critic을 교체했다.

| 프로바이더 | 검증된 셀렉터 |
|---|---|
| `anthropic` | `claude-fable-5:high`/`:xhigh` · `claude-sonnet-5:high` · `claude-opus-4-8:high` · `claude-sonnet-4-6:high` — sel ✅(07-10) |
| `openai-codex` | `gpt-5.6-sol:medium`/`:high`/`:xhigh` · `gpt-5.6-terra:high`/`:xhigh` · `gpt-5.6-luna:high` · `gpt-5.5:high` · `gpt-5.4:high` — sel ✅(07-10; 5.5=07-02) |
| `xai` | `grok-4.5:medium`/`:high` · `grok-4-fast:high` · `grok-4-1-fast:high` · `grok-code-fast-1` · `grok-composer-2.5-fast` — sel ✅(07-10; 4-1 retired) |
| `grok-build` | `grok-4.3` (bare) — sel ✅(07-02) |
| `google-antigravity` | `gemini-3.1-pro-low`/`:high` · `gemini-3-flash`/`:low` — sel ✅(07-10) |
| `opencode-go` | `deepseek-v4-flash` · `deepseek-v4-pro` · `glm-5.2` · `glm-5.1` · `minimax-m2.7` · `qwen3.7-max` · `kimi-k2.6` · `mimo-v2.5` — sel ✅(07-02) |

- `fable-5:max`→xhigh, `sonnet-5:xhigh/max`→high, `grok-4.5:xhigh/max`→high은 실패가 아닌 침묵 클램프다.
- GPT-5.6 3종 `:max`는 수용되지만 심도 미검증이라 미출하이며, `gpt-5.5:high`는 07-02 그린 카나리다.
- `grok-4-1-fast`는 호출돼도 2026-05-15 retire 뒤 grok-4.3 요율로 redirect 과금돼 v2에서 제외했다.
- 0.9.6부터 Gemini 퍼지 공간은 fail-closed다. `gemini-3.1-pro-high`의 0.9.5 침묵 `-low` 해석은 재현되지 않는다.
- `glm-5.2`는 0.7.10부터 번들에 편입됐고 `OPENCODE_API_KEY`가 필요하다.

<details>
<summary><b>실패한 셀렉터 (피하라)</b></summary>

- `openai-codex/gpt-5.3-codex` · `gpt-5.2-codex` · `gpt-5.1-codex-max/mini` — ChatGPT 계정 미지원.
- `google-antigravity/gemini-3.1-pro-high` — 0.9.6 기준 not found; 고추론은 `gemini-3.1-pro-low:high`.
- `gemini-3.5-flash-low` · `gemini-3.5-flash` · `gemini-pro-agent` — 2026-07-10 오후 not found.
- `gemini-3-pro` — 은퇴.
- `claude-sonnet-4-6-thinking` — 404.
- `gpt-oss-120b` — 500.
- `opencode-go/*` — `OPENCODE_API_KEY` 미설정 시 실패.

</details>

> [!NOTE]
> antigravity 라이브 표면은 당일에도 변하고 `--list-models` 표기는 캐시일 수 있다. 좌석 채택 전 실호출하고, 디스커버리 미갱신이면 재로그인/재시도 또는 번들 id를 사용하라(eco critic 대안 `opencode-go/deepseek-v4-pro`; GLM은 `zai/glm-5.2`와 `zai` provider 추가).

<details>
<summary><b>지연 참고 (마이크로벤치 2026-07-02; Grok 4.5만 2026-07-09 streaming)</b></summary>

| 셀렉터 | 코딩 | 추론 | 비고 |
|---|---|---|---|
| `sonnet-5:medium` / `:high` | **3.1s** / 3.5s | 3.5s / 3.4s | **전체 최속** |
| `opus-4-8:high` | 4.0s | 3.9s | |
| `fable-5:medium`~`:max(→xhigh)` | 6.7~7.7s | 3.5~6.3s | 코딩에서 sonnet-5 대비 +3~4s |
| `grok-4.5:medium` / `:high` | ~14s / ~50s | TTFT ~13s / ~48s | high는 고위험 critic 전용 |
| `deepseek-v4-flash` | 4.6s | 5.5s | |
| `gemini-3.1-pro-low:high` | **17.4s** | 5.7s | 코딩 지연 아웃라이어 |
| `glm-5.2` | **21.9s** | 4.0s | 코딩 최저속 — critic엔 무방 |

</details>

```bash
gjc -p --no-session --no-tools --model "anthropic/claude-fable-5:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "google-antigravity/gemini-3.1-pro-low:high" "Reply exactly: OK"
gjc -p --no-session --no-tools --model "openai-codex/gpt-5.6-terra:high" "Reply exactly: OK"
```

### 6-2·6-3. 역할 배치 딥다이브 (이관됨)

다회차 딥리서치+실측으로 역할→모델 배치가 near-optimal임을 확인했다. planner는 07-10 Sol 세대교체, Gemini 명목 1M≠실효 1M(MRCR 26%@1M vs Opus 76%), 단일 메시지 한도 ~400k는 윈도우 한도가 아니므로 청크 누적이 전제다. 전문: [docs/deep-dive-role-fit.md](./docs/deep-dive-role-fit.md)

---

## 7. 🛠️ 설치 / 제거

[§30초 설치](#-30초-설치)의 설치·로그인을 따른다.

```bash
# 옵션
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=ultimate-opus bash  # 기본 프로필 지정
curl -fsSL …/install.sh | GJC_SETUP_DEFAULT=none bash        # 기본값 설정 건너뜀
curl -fsSL …/install.sh | GJC_CODING_AGENT_DIR=/path bash    # 에이전트 경로 override
```

### 수동 설치 / 검증 / 제거

[`gjc-profiles.yml`](./gjc-profiles.yml)의 `profiles:` 블록을 `~/.gjc/agent/models.yml` 아래에 붙여넣고 `gjc --mpreset daily --default`.

```bash
gjc --list-models daily                       # 적용 확인
cp ~/.gjc/agent/models.yml.bak-*  ~/.gjc/agent/models.yml   # 되돌리기(백업 복원)
```

> [!WARNING]
> **GJC 0.7.10~0.9.1 프리셋 rename/delete 주의**: 엔진의 커스텀 프리셋 rename/delete는 `models.yml` 주석을 전부 제거해 설치기의 관리 블록 센티널도 사라진다. 삭제한 프로필이 재설치 때 부활할 수 있으므로 결과를 확인하고, 완전 제거는 백업 복원(`cp … .bak-*`)이 가장 확실하다. 0.9.6에서는 미재검증이다.

---

## 8. 🔀 동적 라우팅 전략

> [`routing-rules.md`](./routing-rules.md)를 프로젝트 `AGENTS.md`에 넣거나 `gjc --append-system-prompt @routing-rules.md`로 주입한다.

<div align="center">
<img src="assets/routing-tree.svg" alt="작업신호 → 위임 라우팅" width="100%">
</div>

**작업신호 → 위임** — 위임은 신호가 명확할 때만, 본체가 직접 할 수 있으면 직접.

<div align="center">
<img src="assets/effort-ladder.svg" alt="적응형 effort 에스컬레이션" width="100%">
</div>

**effort 사다리** — 못 풀어서 올리는 것만 정당 · 저점은 low까지 · Gemini는 low↔high 단일 점프.

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

```text
직렬 5단계(각 0.99): 0.99^5 ≈ 95.1%   /   병렬 독립 5개(OR 성공): 1-(0.01)^5 ≈ 100%
```

- critic은 **본체와 다른 벤더로, 병렬 독립 투표 후 본체가 집계**(debate 금지 — 메타-심판이 우월).
- critic 패널 예: `{openai-codex/gpt-5.6-sol:high, xai/grok-4.5:high, google-antigravity/gemini-3.1-pro-low:high}` 동시 → 2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단. **CRITICAL/HIGH dissent 는 다수결로 기각 불가** — 해소 또는 human gate.
- executor fan-out은 **작업이 진짜 독립**(공유 상태 없음)일 때만.
- 체인은 짧게, 본체를 단일 진실원천으로(서브끼리 직접 합의 금지).

---

## 10. 💰 비용

Gemini는 [Google AI Pro/Ultra](https://antigravity.google/docs/plans) 구독 토큰, 나머지는 per-token 과금이다($/1M, 입력/출력). Fable 포함·credits 캐비앗은 §5를 따른다.

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
> (참고: DeepSeek 계열은 DeepInfra 프로바이더(API 키) 경유 시 V4 Pro $1.30/$2.60.)

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

---

## 11. 📖 출처

**코딩(executor)** · [Vals SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) · [swebench.com](https://www.swebench.com/verified.html) · [Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1)
**Claude 5 패밀리** · [Fable 5 재배포 공지](https://www.anthropic.com/news/redeploying-fable-5) · [platform.claude.com 모델 문서](https://platform.claude.com/docs) — 가격·구독 포함(~7/12 연장, [Android Authority 보도](https://www.androidauthority.com/claude-fable-5-free-extension-3685103/))·effort 스펙 교차 확인 2026-07-02/07-10
**GPT-5.6 (2026-07-09 GA)** · [출시 발표](https://openai.com/index/gpt-5-6/) · [Sol 프리뷰(Cerebras 750TPS)](https://openai.com/index/previewing-gpt-5-6-sol/) · [AA: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) · [TechTimes(METR 평가 게이밍)](https://www.techtimes.com/articles/319808/20260707/gpt-56-sol-review-faster-coding-half-fable-5-cost-benchmark-problem.htm) — 가격·평가 교차 확인 2026-07-10
**역할·라우팅** · [Gemini 3.1 Pro card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [AA Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [self-preference bias](https://arxiv.org/abs/2410.21819) · [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/)
**공식 모델/가격** · [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) · [OpenAI](https://openai.com/api/pricing/) · [xAI](https://docs.x.ai/developers/models)

<div align="center">

**한 줄로 설치하고, 역할마다 최적 모델로.**
**v2.0.1** · [CHANGELOG](./CHANGELOG.md) · [유지보수·검증 플레이북](./MAINTAINING.md) · 라이선스 [CC BY 4.0](./LICENSE) · GJC = [Gajae Code](https://github.com/Yeachan-Heo/gajae-code)

</div>
