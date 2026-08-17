# 역할 배치 딥다이브 — 최적성 검토 · 잔여 공백 실측

> [!NOTE]
> **이 문서는 non-normative 리서치 딥다이브 기록이다.** 규범 출처는 [README §6](../README.md#6--검증-매트릭스)와 [`../evidence/`](../evidence/)다.
> 원문 작성 2026-07-03/07-10 · README에서 이관 2026-07-10, v2.0.1.
> EN/ZH/JA는 요약+링크만 유지 — MAINTAINING §4 계약.

---

## 6-2. 역할 배치 최적성 검토 (deep-research + 실측)

초기 8프로필(v1.0 기준)의 역할→모델 배치를 다회차 deep-research(독립 벤치 검증)와 라이브 추론 프로브로 재검토한 결과, 골격은 near-optimal로 확인됐다. **v2.0.0 은 여기에 2축 블라인드 독립 딥리서치(Claude Fable 5 Ultracode + Parallel.ai Ultra 2x, 2026-07-10)를 추가**해 10-bundle 4계층 구조로 재편했다 — 두 축의 공통 결론: 출시 상태·역할 축 배치는 지지(SUPPORT), profile/workflow 경계·tier 라벨·strict provider 마찰은 수정(REVISE). Premium 3종의 role-fit L3 실측은 잔여 과제로 남긴다(experimental 라벨의 이유).

- **`gemini-3.1-pro-low:high` 는 저하 모드가 아니다.** `thinkingLevel`은 별도 모델 변종이 아니라 동일 Gemini 3.1 Pro에 적용되는 per-request 파라미터이고 모델 기본값이 **HIGH**다. 공식 모델카드의 헤드라인 추론 점수(GPQA 94.3 · ARC-AGI-2 77.1)는 전부 *Thinking (High)* 에서 측정됐다 — 이 셀렉터는 **네이티브 고추론 기본모드**를 호출한다. 실측 프로브: `low`(18s) → `low:high`(22s) 지연 증가로 thinking 활성 확인, 표준 추론 정답은 GPT-5.5·Opus와 동일. *(잔여: GJC `:high` override의 네이티브 HIGH 매핑은 1차 출처 미확증 → 운영 중 추론 품질 모니터링 권장.)*
- **planner 추론 축은 분열한다.** GPQA Diamond(과학지식)는 상위권이 93~96%로 *saturated* — 단독 1위는 이제 **Sonnet 5(96.2)**, Gemini 3.1 Pro 94.3. ARC-AGI-2(추상·유동추론)는 **GPT-5.5가 명확히 앞선다**(0.850 vs 0.771; Fable 5는 미공개 — 추론 축 우위 미입증). 플래닝에 더 직결되는 유동추론(ARC) 기준 → ultimate/escalation planner=GPT 유지. **과학지식추론 비중이 크면 `planner → google-antigravity/gemini-3.1-pro-low:high`로 swap.** *(갱신 2026-07-10: GPT-5.6 Sol GA — 공식 평가 전면 우위(Agents' Last Exam 52.7 vs 46.9 · AA Intelligence 58.9 vs 54.8) + 동가 $5/$30 → v1.11에서 planner 축을 GPT-5.6 Sol로 세대교체(좌석 effort는 번들별: daily/coding-sprint `:high`, 프리미엄·워크플로 `:xhigh`). ARC-AGI-2의 5.6 수치는 미공개 — 축 근거는 공식 평가표+AA 지수. 근거: [evidence/2026-07-10-gpt-5.6-notes.md](../evidence/2026-07-10-gpt-5.6-notes.md).)*
- **executor 축은 v1.4에서 교체됐다.** **Fable 5가 SWE-bench Verified 95.0 / SWE-Bench Pro 80.0으로 신 1위**(Opus 4.8 88.6 · GPT-5.5 82.6; Pro 80.3은 별도 열의 Mythos 5 — [errata E1](../evidence/2026-07-10-errata.md)). Opus 4.8은 "구독 포함 코딩 최강"으로 유지 — Fable 5는 7/12 이후 usage credits 과금이라 상시 executor로는 비용 구조가 다르다(`dream-team`/`escalation`에서만 채용). 터미널·에이전틱 축은 이제 **GPT-5.6 Sol이 SOTA**(Terminal-Bench 2.1 88.8) — 단 ⚠METR이 Sol의 SWE 평가 게이밍(역대 최고 비율)을 적발해 SWE류 점수는 할인해서 읽을 것. daily executor는 동가 후계 `gpt-5.6-terra`.
- **xAI `grok-composer-2.5-fast`·`grok-code-fast-1` 은 eco·throughput 전용.** 독립 벤치 미공개/인플레이션으로 프론티어 코더가 아니며 grok-code-fast-1은 은퇴 예정 — executor 코어 비포함이 맞다.
- **default = Anthropic 플래그십.** Opus 4.8은 Vals Index 종합(서빙 모델 중 1위)으로 재확인. Fable 5 default(`dream-team`)는 품질 상한을 한 단계 더 올리지만 refusal 분류기·credits 과금 캐비앗을 동반한다([§5](../README.md#프로필별-설계-근거)). `ultimate-sol`의 Sol 라우터는 opt-in 실험(WARN 표면화).
- **architect 장문맥 정정**: Gemini의 명목 1M은 실효 1M이 아니다 — MRCR v2 8-needle 128K 84.9% → 1M **26.3%** 붕괴, 반면 **Opus 4.6은 1M 76% 유지**(4.8 수치는 미공개). Grok 4.3 멀티모달은 12/16 하위권이라 비전 architect엔 부적합 → **monorepo architect를 Grok→Opus로 교정**했고, 표준 프로필 architect=Gemini는 멀티모달·중간 ctx 한정 최적이다. (후계자 임박: Gemini 3.5 Pro 2M ctx·Deep Think — 7월 GA로 연기, 출시 시 `{low,high}` 클램프 룰 재검증.) (GJC 경유 실효 상한은 [§6-3](#6-3-잔여-공백-검토-gap-13--gjc-실효-컨텍스트-실측) 참조.)

> 출처: [vals.ai GPQA](https://www.vals.ai/benchmarks/gpqa) · [vals.ai SWE-bench](https://www.vals.ai/benchmarks/swebench) · [vals.ai MMMU](https://www.vals.ai/benchmarks/mmmu) · [Gemini 3.1 Pro card (MRCR)](https://deepmind.google/models/model-cards/gemini-3-1-pro/) · [Gemini thinking docs](https://ai.google.dev/gemini-api/docs/thinking) · [Opus 4.6 (MRCR 76%@1M)](https://www.anthropic.com/news/claude-opus-4-6) · [long-context 보드](https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/) · [llm-stats ARC-AGI-2](https://llm-stats.com/benchmarks/arc-agi-v2) · [xAI Composer 2.5](https://x.ai/news/composer-2-5)

> 📑 **전체 리서치 리포트 (1차 출처 인용 포함)** — 이 배치 근거의 원문 3종: [딥리서치 벤치마크](../evidence/2026-07-03-deep-research-benchmarks.md) · [컨설턴트 리포트](../evidence/2026-07-03-consultant-report.md) · [통합 최종 리포트](../evidence/2026-07-03-ultimate-final-report.md). "왜 이 모델셋업인가"의 근거 전문·council 합의·확정 답변(Grok=critic / Composer Fast≠executor)이 여기에 있다. 발행 리포트는 verbatim 보존되며 정정은 **[errata](../evidence/2026-07-03-errata.md)** 로 배송된다(현재 E1: Composer 74.7→54.0은 SWE-bench **Pro** 수치 — 최종 리포트 표의 Verified 열 오배치 정정).

---

## 6-3. 잔여 공백 검토 (gap 1~3 · GJC 실효 컨텍스트 실측)

Opus 4.8은 GJC에서 **1M 컨텍스트 윈도우를 정상 지원**한다(멀티턴 누적 — 상태바 `◫ %/1M` 확인). 아래 표는 그와 **별개로**, 거대 컨텍스트를 **단일 메시지(`@파일`)로 한 방에** 주입할 때의 입력 크기 한도 실측이다(3-needle 멀티홉 검색 기준) — 윈도우 한도가 아님:

| 토큰(단일요청) | Opus 4.8 | Gemini 3.1 Pro | Grok 4.3 / 4-fast | DeepSeek V4 Pro |
|---|:---:|:---:|:---:|:---:|
| ~130k · 250k · 350k | ✅ | ✅ | ✅ | ✅ |
| ~476k | 🔴 400 | 🔴 400 | ✅ (89s) | ✅ (36s) |
| ~857k | 🔴 | 🔴 | 🔴 400 | — |

- **gap1 — Grok 2M architect swap: ❌ 기각.** 독립 벤치(Context Arena MRCR v2)에서 Grok은 deep-bin 검색이 **최하위**(grok-4.20 256–512k 0.117), 2M bin은 어떤 보드에도 없고 grok-4-fast의 2M은 측정된 검색 점수가 0(마케팅/훈련 주장). 실측도 857k에서 400. → "1M 초과는 grok-4-fast(2M)" 가정 폐기.
- **gap2 — Opus 장문맥:** Opus 는 **GJC에서 1M 컨텍스트 윈도우를 지원**한다(멀티턴 agentic 파일읽기로 1M까지 정상 누적). 위 표의 ~400k 400은 **윈도우 한도가 아니라 단일 메시지(`@파일`) 입력 크기 한도**다. (참고: 공개된 MRCR 76%@1M은 Opus 4.6 수치, 4.8은 미공개.) → monorepo architect=**Opus 유지**(1M ctx 정상, 검색 최상위). **v2.1.0 갱신**: 위 표의 476k 🔴 는 Opus 4.8 세대 수치다. 2026-08-17 배터리에서 `claude-opus-5:high` 는 **476k 단일 메시지도 통과**했다(needle 회수 성공, `evidence/2026-08-17-selectors.md`). 따라서 >400k 단일 paste 에 별도 셀렉터로 갈아탈 필요가 없어졌다 — architect 좌석의 Opus 5 가 그대로 처리한다. `xai/grok-4-fast:high` 도 476k 통과. `deepseek-v4-pro` 는 과거 통과했으나 이 계정 403 이라 권장 대상이 아니다.
- **gap3 — GLM-5.2 vs DeepSeek:** 원래 판단은 eco executor=DeepSeek V4 Flash 유지(GLM-5.2 $1.40/$4.40 = 입력 10×·출력 15×, eco엔 과함)였다. **v2.1.0 에서 뒤집혔다** — 2026-08-16·17 실호출에서 `deepseek-v4-flash` 가 이 계정 **403 China opt-in** 이라 출하 좌석 자격을 잃었고, eco executor 도 `opencode-go/glm-5.2` 로 교체했다(코딩 프로브 8/8·5.1s, `evidence/2026-08-17-eco-executor.md`). **monorepo critic 도 `opencode-go/glm-5.2`** — 신규 오픈웨이트 1위(AA Index 51; DeepSeek V4 Pro 52→**44 하락**), cross-family 독립 유지, opencode-go 구독 내 서빙이라 한계비용 낮음. 지역 정책이 풀리면 저가 우선 관점에서 deepseek 재평가.

> 핵심: Opus 컨텍스트 윈도우는 GJC에서 **1M 정상**(멀티턴 누적). **위 표**의 단일 메시지 한도(~400k, Opus/Gemini)는 **Opus 4.8 세대 실측(2026-06-18)** 이다 — **Opus 5 는 476k 단일 메시지를 통과**한다(2026-08-17, `evidence/2026-08-17-selectors.md`). 그래도 **거대 입력은 한 메시지에 통째로 붓지 말고 청크로 나눠 누적**하는 편이 낫다(1M nominal window ≠ 완전 recall). 위 표는 GJC 내부에서 독립 재검증 통과 — 20/20 일치, 실측일 2026-06-18. 출처: [Context Arena](https://contextarena.ai/) · [GLM-5.2 (AA)](https://artificialanalysis.ai/models/glm-5-2) · [Opus 4.8 what's-new](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)
