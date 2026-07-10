# 팩트시트 — v2.0.0 (기준일 2026-07-10 · gjc 0.9.6)

> [!NOTE]
> **이 문서는 non-normative 요약이다.** 규범 출처: 매핑 = [`gjc-profiles.yml`](../gjc-profiles.yml) · 운영 계약 = [`routing-rules.md`](../routing-rules.md) · 검증 원본 = [`evidence/`](../evidence/). 모든 수치는 **기재된 검증일 시점**이며 시점 민감하다 — 카탈로그·라이브 표면은 당일에도 변한다(07-10 오후 `gemini-3.5-flash*` 소멸 실측).

## 1. 릴리스

| 항목 | 값 |
|---|---|
| 가이드 버전 | **v2.0.0** (2026-07-10, [PR #21](https://github.com/project820/gjc-multivendor-setup-guide/pull/21) — cyber-cop 5라운드 후 사람 머지) |
| 기준 GJC | **0.9.6** (2026-07-10 12:36 KST 릴리스, 바이너리 sha256 = 공식 자산 digest 검증) |
| 번들 | **10종 · 4계층** (Core 3 · Premium exp 3 · Workflow 2 · Specialized exp 2) |
| 실호출 검증 | `evidence/2026-07-10-selectors-rerun-3.md` — v2 출하 셀렉터 **전 좌석 그린** |
| 리서치 근거 | 2축 블라인드 딥리서치(Claude Fable 5 Ultracode + Parallel.ai Ultra 2x) → 인간 freeze 2026-07-10 |

## 2. 번들 × 좌석 (요약)

| 번들 | default | executor | planner | architect | critic | 인증 |
|---|---|---|---|---|---|---|
| ⭐ daily | Opus:med | Terra:high | Sol:high | Gemini`-low:high` | Gemini`-low:high`¹ | 구독 3 |
| 🏎 coding-sprint | Opus:med | Opus:high | Sol:high² | Gemini`-low:high` | Terra:high² | 구독 3 |
| 🚨 cyber-cop | Opus:high | Sol:high | Gemini`-low:high` | Opus:high | Sol:high | 구독 3 |
| 🏆 ultimate-opus | Opus:high | Opus:high³ | Sol:xhigh | Opus:high³ | Grok4.5:high | +xai |
| 🧪 ultimate-sol | Sol:high⁴ | Sol:xhigh | Sol:xhigh | Opus:high | Grok4.5:high | +xai |
| 🔥 dream-team | Fable:high | Fable:xhigh³ | Sol:xhigh | Opus:high³ | Grok4.5:high | +xai |
| 🏛 llm-council | Opus:high⁵ | Terra:high | Sol:xhigh | Gemini`-low:high` | Grok4.5:high | 구독 3+xai |
| 🛡 escalation | Opus:high | Fable:xhigh | Sol:xhigh | Gemini`-low:high` | Grok4.5:high | 구독 3+xai |
| 💸 eco | Terra:med | DeepSeek V4 Flash | Luna:med | Gemini`-low:high` | Gemini 3-flash:low | codex+go+google |
| 🗺 monorepo | Opus:med | Opus:high³ | Gemini`-low:high` | Opus:high³ | GLM-5.2 | anthropic+google+go |

¹ architect와 동일 셀렉터 — 3벤더 구독-only 제약의 의도적 트레이드오프(xai 로그인 시 `grok-4.5:medium` 스왑 권장). ² plan/crit 동계열 — `SAME_FAMILY_OK` 인간판정. ³ exec/arch 동계열 — `SAME_FAMILY_OK`. ⁴ 유일한 Anthropic-보유 비-Anthropic 라우터(`NON_ANTHROPIC_DEFAULT_OK`, WARN). ⁵ 집계자 제한 — 판정석은 Google·xAI·OpenAI 3계열.

## 3. 모델 팩트 (검증일 명기)

| 모델 | $/1M in/out | GJC ctx 표면 | GJC 실효 effort 상한 | 검증 |
|---|---|---|---|---|
| Claude Opus 4.8 | 5 / 25 | **1M**/128K (단일 `@file` ~400k: 350k✅/476k🔴) | **max** (6단 전부) | 07-10✅ |
| Claude Fable 5 | 10 / 50 (배치 5/25) | 1M/128K | **xhigh** (`:max` 침묵 클램프) · thinking 상시-온 · refusal=HTTP 200+`stop_reason` · 30d retention/ZDR 불가 | 07-10✅ |
| GPT-5.6 Sol | 5 / 30 | **373K**/128K (0.9.6, API 1.05M과 별개) | **xhigh** 출하상한 (`:max` 수용·심도 미검증) | 07-10✅ |
| GPT-5.6 Terra | 2.5 / 15 | 373K/128K | xhigh 출하상한 | 07-10✅ |
| GPT-5.6 Luna | 1 / 6 | 373K/128K | xhigh 출하상한 | 07-10✅ |
| Gemini 3.1 Pro | 프리뷰/구독¹ | 1M/66K (MRCR 1M 26.3% — nominal ≠ recall) | `low`/`high` 2단 · **`-low:high` 리터럴 핀** | 07-10✅ |
| Gemini 3-flash | 프리뷰/구독¹ | 1M/66K | minimal..high | 07-10✅ |
| Grok 4.5 | 2 / 6 (실효 in ~$0.84 @88% cache) | provider 500K(exact-diff 안전 ~400K)·GJC 표기 222K 스테일 | **high** (`:xhigh`/`:max` 침묵 클램프) · **xai API 전용**(grok-build 변종 없음, 07-10 재조회) | 07-10✅ |
| DeepSeek V4 Flash | 0.14 / 0.28 | 1M | effort 생략 | 07-02✅ |
| GLM-5.2 | 1.40 / 4.40 | 1M/131K | effort 생략(opencode-go 규칙) | 07-02✅ |

¹ Antigravity = 무료 공개 프리뷰 + AI Pro/Ultra 구독 시 한도 상향([공식 plans](https://antigravity.google/docs/plans), 07-10 확인).

## 4. 0.9.6 엔진 변경점 (0.9.5 대비 실측)

- gpt-5.6 3종 usable prompt budget **272K → 373K** (카탈로그 유일 diff — `evidence/2026-07-10-catalog-gjc096.txt`)
- antigravity 퍼지 공간 **fail-closed**: `gemini-3.1-pro-high`/`-bogus` → "not found" (0.9.5의 침묵 -low 해석 함정 재현 안 됨 — `-low:high` 핀은 유지)
- 라이브 표면 당일 드리프트: `gemini-3.5-flash-low`/`-extra-low`/`gemini-pro-agent` 소멸 — `--list-models` 표기와 실호출이 어긋날 수 있음, **실호출이 진실**
- 내장 프로필 GPT-5.6 세대교체(`codex-*`/`opus-codex`/`fable-opus-codex`) — 단일·2벤더 수요 흡수
- `grok-4-1-fast`: xAI 2026-05-15 retire — 호출은 성공하나 **grok-4.3 요율 redirect 과금** (v2 퇴출)

## 5. 불변식 (validator 강제)

1. 전 번들 멀티벤더 — **실사용 벤더 ≥2** (required_providers 패딩으로 우회 불가, 패딩은 WARN)
2. default = Anthropic 플래그십 (예외: `ultimate-sol` WARN 등재 · anthropic 미포함 `eco`는 비적용)
3. exec/arch · plan/crit cross-family (예외는 `SAME_FAMILY_OK` 등재 + WARN 영구 표면화 — 현재 4건)
4. effort 하드룰 (§3 상한 위반은 하드에러)
5. required_providers ⊇ 실사용 provider
6. README×4 임베드 YAML == `gjc-profiles.yml` (parsed-mapping 비교 — `scripts/sync-readme-yaml.py`로 동기화)

## 6. 재평가 트리거

GJC 릴리스 diff · 카탈로그 드리프트(`catalog-snapshot.sh --diff`) · **Fable 프로모션 종료/재연장(~7/12 23:59 PT)** · grok-build에 4.5 등장 · 신모델 입점(Gemini 3.5 Pro GA 등) · 가격 개정 · 독립 leaderboard 등재 · validator 검사범위 변경 — 하나라도 발화하면 profile matrix 재계산.
