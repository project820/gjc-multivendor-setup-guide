# 팩트시트 — v3.0.0 (기준일 2026-08-17 · gjc 0.13.3)

> [!NOTE]
> **이 문서는 non-normative 요약이다.** 규범 출처: 매핑 = [`gjc-profiles.yml`](../gjc-profiles.yml) · 운영 계약 = [`routing-rules.md`](../routing-rules.md) · 검증 원본 = [`evidence/`](../evidence/). 모든 수치는 **기재된 검증일 시점**이며 시점 민감하다 — 카탈로그·라이브 표면은 당일에도 변한다(07-10 오후 `gemini-3.5-flash*` 소멸 실측).

## 1. 릴리스

| 항목 | 값 |
|---|---|
| 가이드 버전 | **v3.0.0** (카탈로그 재설계 — 8번들·4계층, daily.executor Luna:max) |
| 기준 GJC | **0.13.3** (로컬 바이너리 확인 2026-08-16 · [upstream v0.13.3](https://github.com/Yeachan-Heo/gajae-code/releases/tag/v0.13.3) 2026-08-15) |
| 번들 | **8종 · 4계층** (Core 3 · Premium exp 1 · Workflow 2 · Specialized exp 2) |
| 실호출 검증 | 출하 좌석 게이트 정본 = **`evidence/2026-08-17-selectors-rerun-2.md`**(개정된 revalidate.sh 실행, 회귀 0). 단일 메시지 476k 근거 = `evidence/2026-08-17-selectors.md`(하네스 수정 전 산출물). `evidence/2026-08-16-selectors.md` 는 eco.executor 가 DeepSeek 이던 시점이라 그 좌석이 403 으로 실패해 있다 |
| 리서치 근거 | 2축 블라인드 딥리서치(Claude Fable 5 Ultracode + Parallel.ai Ultra 2x) → 인간 freeze 2026-07-10 |

## 2. 번들 × 좌석 (요약)

| 번들 | default | executor | planner | architect | critic | 인증 |
|---|---|---|---|---|---|---|
| ⭐ daily | Opus5:med | Luna:max | Sol:high | Gemini`-low:high` | Gemini`-low:high`¹ | 구독 3 |
| 🏎 coding-sprint | Opus5:med | Opus5:high | Sol:high² | Gemini`-low:high` | Terra:high² | 구독 3 |
| 🚨 cyber-cop | Opus5:high | Sol:high | Gemini`-low:high` | Opus5:high | Sol:high | 구독 3 |
| 🏆 ultimate-opus | Opus5:high | Opus5:high³ | Sol:xhigh | Opus5:high³ | Grok4.6:high | +xai |
| 🏛 llm-council | Opus5:high⁵ | Terra:high | Sol:xhigh | Gemini`-low:high` | Grok4.6:high | 구독 3+xai |
| 🛡 escalation | Opus5:high | Fable:xhigh | Sol:xhigh | Gemini`-low:high` | Grok4.6:high | 구독 3+xai |
| 💸 budget | Terra:med | GLM-5.2 | Qwen3.8Max | Gemini`-low:high` | Gemini`-low:high` | codex+go+google |
| 🗺 monorepo | Opus5:med | Opus5:high³ | Gemini`-low:high` | Opus5:high³ | GLM-5.2 | anthropic+google+go |

¹ architect와 동일 셀렉터 — 3벤더 구독-only 제약의 의도적 트레이드오프(xai 로그인 시 `grok-4.6:medium` 스왑 권장). ² plan/crit 동계열 — `SAME_FAMILY_OK` 인간판정. ³ exec/arch 동계열 — `SAME_FAMILY_OK`. ⁵ 집계자 제한 — 판정석은 Google·xAI·OpenAI 3계열.

## 3. 모델 팩트 (검증일 명기)

| 모델 | $/1M in/out | GJC ctx 표면 | GJC 실효 effort 상한 | 검증 |
|---|---|---|---|---|
| Claude Opus 5 | 5 / 25 | **1M**/128K (단일 `@file` **476k 통과** — 08-17) | **max** (6단 전부) | 08-16·17✅ |
| Claude Opus 4.8 | 5 / 25 | **1M**/128K (단일 `@file` ~400k: 350k✅/476k🔴 — 구세대 수치) | **max** (6단 전부) | 07-10✅ 레거시 카나리 |
| Claude Fable 5 | 10 / 50 (배치 5/25) | 1M/128K | **xhigh** 출하상한 (`:max` 수용·심도 미검증) · thinking 상시-온 · refusal=HTTP 200+`stop_reason` · 30d retention/ZDR 불가 · 07-20부터 Max/premium Team 주간한도 50% 포함, Pro=credits | 08-16✅ |
| GPT-5.6 Sol | 5 / 30 | **372K**/128K (0.13.3 표기, API 1.05M과 별개) | **xhigh** 출하상한 (`:max` 수용·심도 미검증) | 08-16✅ |
| GPT-5.6 Terra | 2.5 / 15 | 372K/128K | xhigh 출하상한 | 08-16✅ |
| GPT-5.6 Luna | 1 / 6 | 372K/128K | **:max 출하**(D-1 이 `{max}` 단독 강제) | 08-16✅ |
| Gemini 3.1 Pro | 프리뷰/구독¹ | 1M/66K (MRCR 1M 26.3% — nominal ≠ recall) | `low`/`high` 2단 · **`-low:high` 리터럴 핀** | 08-16✅ |
| Gemini 3-flash | 프리뷰/구독¹ | 1M/66K | minimal..high | 08-16✅ |
| Grok 4.6 | 2 / 6 (<200k) · 4 / 12 (≥200k) | provider 500K | 카탈로그 **xhigh** · 출하 **high** · xai API | 08-16✅ |
| Grok 4.5 | 2 / 6 | 500K | **high** (레거시 카나리) | 08-16✅ |
| DeepSeek V4 Flash | 0.14 / 0.28 | 1M | effort 생략 | **미출하** — 카탈로그 잔류 · 이 계정 08-16·17 **403 China opt-in** |
| GLM-5.2 | 1.40 / 4.40 | 1M/131K | effort 생략(opencode-go 규칙) | 08-16·17✅ — budget executor · monorepo critic |
| Qwen3.8 Max | — | — | effort 생략(opencode-go 규칙) | 08-17✅ 프로브 ok — budget planner |

¹ Antigravity = 무료 공개 프리뷰 + AI Pro/Ultra 구독 시 한도 상향([공식 plans](https://antigravity.google/docs/plans)). Gemini 3.5 Pro 미입점.

## 4. 0.13.3 엔진 변경점 (0.9.6 대비 실측)

- 카탈로그 입점: `anthropic/claude-opus-5` · `xai/grok-4.6` · `grok-build/grok-4.5`/`grok-4.6`(bare) · Gemini 3.5/3.6 Flash
- gpt-5.6 3종 usable prompt budget **373K → 372K** (`evidence/2026-08-16-catalog.txt`)
- antigravity 퍼지 공간 fail-closed **유지** (`gemini-3.1-pro-high` not found)
- `gemini-3.5-flash-low` 07-10 소멸 → 08-16 부활(플랩) — 좌석 미승격
- `grok-build/grok-4.6:high` not found · bare OK
- DeepSeek V4: 카탈로그 잔류, 이 계정 403 China opt-in

## 5. 불변식 (validator 강제)

1. 전 번들 멀티벤더 — **실사용 벤더 ≥2** (required_providers 패딩으로 우회 불가, 패딩은 WARN)
2. default = Anthropic 플래그십 (anthropic 미요구 번들은 적용 대상 아님 — 예외 목록 없음)
3. exec/arch · plan/crit cross-family (예외는 `SAME_FAMILY_OK` 등재 + WARN 영구 표면화 — 현재 3건)
4. effort 하드룰 (§3 상한 위반은 하드에러)
5. required_providers ⊇ 실사용 provider
6. README×4 임베드 YAML == `gjc-profiles.yml` (parsed-mapping 비교 — `scripts/sync-readme-yaml.py`로 동기화)

## 6. 재평가 트리거

GJC 릴리스 diff · 카탈로그 드리프트(`catalog-snapshot.sh --diff`) · Fable 플랜 스플릿 가격 고통 · grok-build effort 서픽스 해석 · 신모델 입점(Gemini 3.5 Pro GA 등) · DeepSeek 지역 opt-in 해제 · 가격 개정 · 독립 leaderboard 등재 · validator 검사범위 변경 — 하나라도 발화하면 profile matrix 재계산.
