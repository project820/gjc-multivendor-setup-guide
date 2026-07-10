# 투트랙 설계 노트 — GPT-5.6 Sol 중심 track B (`ultimate-sol`) — 2026-07-10

> v1.12.0 `ultimate-sol` 신설 + default 불변식 명시-예외 개정의 근거 감사추적.
> 방법론: 당사자(Codex) 1:1 비교표 접수 → **1차 출처(openai.com/index/gpt-5-6) 헤드리스 렌더로 평가표 원문 직접 추출**(CSR 페이지라 리더모드로는 테이블 누락 — puppeteer로 innerText 확보) → Anthropic 공식 문서·보도 교차.

## 0. 선행 기록 정정 (errata — `2026-07-10-gpt-5.6-notes.md` §2-1 관련)

`evidence/`는 append-only이므로 원본은 보존하고 이 dated 노트로 정정한다:

1. **"OpenAI가 Sol의 SWE-Bench Pro를 공표하지 않았다"(TechTimes 07-07 인용) → 틀림.** 07-10 1차 출처 직접 렌더 결과, 공식 평가표 Coding 섹션에 SWE-Bench Pro 전 열이 존재한다: **Sol 64.6% · Terra 63.4% · Luna 62.7% · GPT-5.5 59.4% · Claude Mythos 5 80.3% · Claude Fable 5 80.0% · Opus 4.8 69.2% · Gemini 3.1 Pro Preview 54.2%**. TechTimes 기사가 프리뷰 시점 기준이었거나 오보. **자사 표에 Fable +15.4pt 열세를 실었으므로(자기불리 진술) Fable의 레포급 코딩 우위는 오히려 최상급 근거가 됐다.** METR 게이밍 캐비앗(§선행 노트)은 불변 — 게이밍 적발에도 64.6이라는 뜻.
2. **"SWE-Bench Pro 1위 = Fable 5(80.3)" → 80.3은 Claude Mythos 5.** 공식 표 기준 Fable 5는 80.0. (선행 웹 소스들의 80.3~80.4 "Fable" 표기는 Mythos와 혼용.) 판정 영향 없음 — Claude 5 기저의 우위는 동일.

## 1. 1차 출처 평가표 발췌 (openai.com/index/gpt-5-6, 2026-07-10 렌더 실측)

경쟁사 열을 포함한 OpenAI 자사 발표표 — 자기유리 방향 수치는 할인, 자기불리 방향(Fable 우위 행)은 강한 근거로 읽는다.

| 평가 | Sol | Terra | Luna | 5.5 | **Fable 5** | Opus 4.8 | 비고 |
|---|---|---|---|---|---|---|---|
| Agents' Last Exam | **52.7** | 50.4 | 50.3 | 46.9 | 40.5 | 45.2 | 장기 프로 워크플로 완주 — Sol +12.2 vs Fable |
| GDPval-AA v2 (Elo) | 1,747.8 | 1,593 | 1,591.8 | 1,493.7 | **1,759.6** | 1,600.1 | 지식노동 — Fable 1위 |
| AA Intelligence v4.1 | 58.9 | 55.0 | 51.2 | 54.8 | **59.9** | 55.7 | Fable 1위 (본문: Sol max가 1pt 이내 근접, 61% 빠르고 절반 비용) |
| AA Coding Agent v1.1 | **80 (max)** | 77.4 | 74.6 | 76.4 | 77.2 | 72.5 | Sol SOTA·Terra가 Fable 초과 |
| SWE-Bench Pro | 64.6 | 63.4 | 62.7 | 59.4 | **80.0** (Mythos 80.3) | 69.2 | **레포급 — Fable 압승(자사표 인정)** |
| DeepSWE v1.1 | **72.7** | 69.6 | 67.2 | 67.0 | 69.7 | 59.0 | 장기 엔지니어링 — Sol 우위 |
| Terminal-Bench 2.1 | **88.8** (Ultra 91.9) | 87.4 | 84.7 | 85.6 | 83.1 | 78.9 | 터미널 — Sol SOTA (Mythos 88) |
| Toolathlon | 58.0 | 53.1 | 53.4 | 55.6 | **61.7** | 59.9 | **툴 사용 — Claude 우위, Sol 열세** |
| FrontierMath Tier 4 | 83.0 | 68.3 | 58.5 | 72.5 | **87.8** | 56.1 | 최고난도 수학 — Fable 우위 |
| FrontierMath T1-3 | **89.0** | 84.9 | 78.6 | 85.3 | 87.0 | 80.0 | |
| GPQA Diamond | **94.6** | 92.9 | 92.3 | 93.6 | 92.6 | 92.0 | Gemini 3.1 Pro 94.3 |
| OSWorld 2.0 | **62.6** | 50.2 | 45.6 | 47.5 | — | 54.8 | 컴퓨터 사용 |
| BrowseComp | **90.4** (Ultra 92.2) | 87.5 | 83.3 | 84.4 | 84.3† | 85.9† | †Mythos 88 |
| CTF Challenges | **96.7** | 91.8 | 85.2 | 88.1 | — | — | 사이버 |
| ExploitBench | 73.5 | 52.9 | 33.2 | 47.9 | (Mythos **78**) | 40.0 | |
| HealthBench Prof. | 60.5 | 57.7 | 55.7 | 49.5 | **60.9** | 53.0 | |
| MMMU Pro (no tools) | **83.0** | 80.7 | 78.4 | 81.2 | — | — | Gemini 3.1 Pro 80.5 |
| GeneBench Pro | 28.7 | 23.3 | 10.8 | 12.0 | (거부) | 16.0 | 각주: **Fable은 고급 생물학 질문 대다수를 refusal** — refusal 리스크 공식 확인 |

**축 요약**: 장기 워크플로 완주·터미널·컴퓨터 사용·브라우징·사이버·멀티모달 = **Sol** / 레포급 코딩·지식노동·지능지수·툴 사용·최고난도 수학 = **Fable(Claude 5 기저)**. "Sol이 전면 우위"라는 중론은 부정확 — **역할 축이 깨끗하게 갈린다.** 이것이 투트랙의 근거다.

## 2. Claude Mythos 5 — track A 후계 아님 (조사 결과)

- Fable 5와 **동일 기저 모델**, 특정 영역(사이버·생물학) 세이프가드를 해제한 변종. 2026-06-09 동시 발표, 6/12 수출통제로 중단 → 6/30 해제.
- **일반 판매 없음** — Project Glasswing(미 정부 협력) 승인 고객(사이버 방어·인프라 사업자) 한정. GJC 카탈로그 미입점(07-10 확인: `gjc --list-models`에 mythos 없음).
- 가격 $10/$50(Fable 동일). → 표의 Mythos 우위 행(SWE-Pro 80.3, ExploitBench 78, T-B 88)은 **"세이프가드 없는 Fable"의 상한**으로 읽으면 된다. 프로필 채용 불가.
- 출처: [Anthropic 발표](https://www.anthropic.com/news/claude-fable-5-mythos-5) · [platform.claude.com 모델 문서](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) · [CNBC](https://www.cnbc.com/2026/06/09/anthropic-mythos-claude-fable-5.html)

## 3. Track B 설계 — `ultimate-sol` 🌞 (opt-in·실험적)

당사자(Codex) 권장안(orchestrator/executor/reviewer=Sol · planner/architect/critic=Fable)을 GJC 현실로 보정:

| 역할 | 채택 | 근거 (1차 출처 축) | Codex 안과의 차이 |
|---|---|---|---|
| default | `gpt-5.6-sol:high` | ALE 52.7 vs 40.5(완주) · 토큰 효율 | 동일. ⚠트레이드오프 명기: codex 표면 **ctx 272K**(Opus/Fable 1M 대비 라우터 누적 한계) + **툴콜 축 열세**(Toolathlon 58 vs 61.7) |
| executor | `gpt-5.6-sol:xhigh` | T-B 88.8 SOTA·DeepSWE 72.7·CTF 96.7 | 동일. ⚠레포급(SWE-Pro 64.6 vs 80.0)은 명시적 비적합 — 대형 마이그레이션·구원투수는 track A(escalation) |
| planner | `claude-fable-5:xhigh` | AA-Int 59.9·GDPval 1759.6·FrontierMath T4 87.8 | 동일(수용). 7/12 후 credits — 저빈도 좌석이라 노출 제한적 |
| architect | `claude-opus-4-8:high` | MRCR 76%@1M 실측 — 272K 본체의 장문맥 보완 레인 | Codex는 Fable — Opus 채택: 장문맥 실측 우위 + 구독 포함 + Fable 과잉탐색·credits 회피 |
| critic | `xai/grok-4.5:high` | 3족 보존 — executor(gpt)·planner(claude) 모두와 cross-family | Codex는 Fable — **planner=Fable과 동일 계열이라 plan_crit cross-family 위반**, grok으로 보정 |

- **default 불변식 개정**: 폐기가 아니라 **명시 예외 allowlist**(`NON_ANTHROPIC_DEFAULT_OK`, SAME_FAMILY_OK 선례) — 예외마다 rationale 필수, WARN으로 영구 표면화, 그 외 프로필은 계속 에러. "시간이 지나면 불변식도 바뀐다"(운영자 방침)를 fail-closed 형태로 수용.
- **실험적 라벨**: L3 rolefit **사전(事前)** 출하(ultimate-f5 v1.4 선례 — 출하 후 L3로 권고 조정). 벤더 자사표 기반 배치임을 명기, L3 실측 후 조정.
- 셀렉터 실호출: 전 좌석 2026-07-10 배터리로 기검증(sol high/xhigh · fable xhigh · opus high · grok high — `2026-07-10-selectors-rerun-2.md`). 신규 셀렉터 0.

## 4. 스왑 가이드 (투트랙 경계)

- **track A가 기본**: 레포급 코딩·대형 마이그레이션·1M 장문맥 세션·툴콜 신뢰성 중심 → `ultimate`/`legend`/`escalation`.
- **track B로**: 장기 자율 워크플로 완주·터미널/CLI 중심·브라우저/컴퓨터 사용·사이버 작업 + 세션 컨텍스트가 272K 안에서 도는 경우 → `ultimate-sol`.
- 혼합 금지 원칙 불변(매 쿼리 스왑 ❌) — 모드 경계에서만.
