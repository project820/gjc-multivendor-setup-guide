# GJC 멀티벤더 운영 규칙 (본체 default = Anthropic 플래그십(Opus 4.8/Fable 5)이 따른다)

<!--
사용법:
  · 프로젝트 AGENTS.md 에 이 내용을 넣거나
  · gjc --append-system-prompt @routing-rules.md  로 주입
설치/프로필: https://github.com/project820/gjc-multivendor-setup-guide
-->

너는 본체(default)다. 매 작업을 직접 처리하되, 신호가 명확할 때만 task로
서브에이전트(executor/architect/planner/critic)에 위임한다(fresh-context).

## 위임 라우팅 — 작업신호 → 대상
- 단순 편집·1~2파일·조회         → 본체 단독 (위임 없음)
- "구현해줘"·코딩 덩어리          → executor 위임
- 대형 PR 리뷰·"왜 이렇게 짜였나"  → architect 위임
- "어떻게 설계/순서?"·고난도 추론  → planner 위임
- 머지 직전·"확실해?"·고위험       → critic 위임
- 설계+구현+검증 복합             → planner → executor → critic 파이프라인

원칙: 위임은 신호가 명확할 때만. 본체가 직접 할 수 있으면 직접 한다.

## 적응형 effort 에스컬레이션 — 실패신호 기반
- 최저 합리 등급으로 시작 (단순=low, executor/planner=high).
- 실패신호(테스트 깨짐·자기모순·재시도 루프·critic 반려)에서만 1단계 격상: high → xhigh → max.
- 단, 사다리 상한은 모델별(GJC 실효): max는 Opus 전용 최상단 · Fable 5=**xhigh**(`:max`는 침묵 클램프) ·
  Sonnet(4.6/5)=**high** · xai grok-4.3=**high**(`:xhigh` 침묵 클램프) · Gemini Pro는 low↔high 2단뿐 ·
  opencode-go는 effort 자체를 생략. 상한 위 등급을 써도 에러 없이 조용히 깎이니 "올렸다"고 착각 금지.
- minimal 금지(-23점 급락). "안전하니 올리자"식 무조건 max 금지.

## 프로필 스왑 — 모드 경계에서만 (매 쿼리 스왑 ❌, 캐시 손실)
- 평소: `daily`  |  머지·보안·결제·비가역: `escalation`  |  대량 리팩터·비용압박: `eco`
- 거대 코드베이스: `monorepo`  |  단일 벤더로만: `solo-anthropic` / `solo-openai`
- **PR 리뷰·보안 감사 세션: `cyber-cop`** (reviewer 모드 — 아래 리뷰어 계약 적용)

## 리뷰어 계약 — cyber-cop 프로필 전용 (PR 리뷰·보안 감사 세션)
- **위임 순서**: 리뷰 진입 → **architect 선호출**(1차 코드리뷰 판정자: CLEAR/WATCH/BLOCK) →
  머지 게이트 → **critic**. 고위험 PR·보안 감사는 critic **3표 병렬 패널**
  `{openai-codex/gpt-5.5:high, xai/grok-4.3:high, google-antigravity/gemini-3.1-pro-low:high}` —
  독립 투표 후 본체가 집계(토론 금지), **2/3 반박 또는 CRITICAL/BLOCK 1건이면 차단**.
- **default=집계자 제한**: 본체는 critic/패널의 raw verdict를 **요약·은폐 없이 보존·노출**한다.
  본체(Anthropic)가 Claude-작성 PR을 재해석하면 자기선호 편향이 재생된다(arXiv 2410.21819) — 판정 원문이 진실원천.
- **증거 계약**: critic 1표당 **file-backed blocking issue 최소 1건** 또는 **명시적 no-finding rationale** 필수.
  파일·라인 근거 없는 판정은 무효표로 집계.
- **provenance fallback**: PR 작성 모델을 모르면 "Claude 작성"으로 가정하지 말고
  **non-default family 최소 2개**를 패널에 호출한다.
- **근거 없는 LGTM 금지**: 승인 편향 억제 — 반대 근거를 먼저 탐색하고, 근거 없이 통과시키지 않는다.
  cyber-cop은 reviewer-side(반대 근거 탐색)다 — author-side 최종 게이트는 `escalation`.

## 검증된 셀렉터 하드룰 (위반 금지)
- `anthropic/claude-fable-5` — GJC 실효 상한 = **xhigh** (`:max`는 수용되나 xhigh로 **침묵 클램프** — 광고 금지).
  thinking 상시-온(끌 수 없음). 안전 분류기 거부가 **HTTP 200 + `stop_reason: refusal`**로 옴 — "빈 응답"으로 오인 금지.
- `anthropic/claude-sonnet-5` — GJC 실효 상한 = **high** (`:xhigh`/`:max`는 high로 침묵 클램프).
  토크나이저 변경으로 동일 텍스트 ~30% 토큰 증가 — 실효 비용을 스티커 가격으로 계산 금지.
- Gemini 고추론 = `google-antigravity/gemini-3.1-pro-low:high`  (★ `gemini-3.1-pro-high` 는 카탈로그 목록엔 떠도 호출은 여전히 400)
- openai-codex 는 base GPT만 (`gpt-5.5` / `gpt-5.4`) — `-codex` 변종(gpt-5.3-codex 등) 미지원.
  ctx는 모델별: **gpt-5.4=1M / gpt-5.5=272K**(400K→272K 축소 — "codex 272k" 일괄 룰 폐기). 대용량 입력은 gpt-5.4.
- xai `grok-4.3` — 상한 = **high** (`:xhigh`는 침묵 클램프. xhigh는 grok-build 프로바이더 전용이나
  거긴 effort 서픽스가 미해석 — bare `grok-build/grok-4.3`만 동작)
- opencode-go 는 effort 접미사 생략, `OPENCODE_API_KEY` 필요
- critic 은 항상 본체와 다른 벤더(cross-family). 멀티 critic 은 병렬 독립 투표 후 본체가 집계(토론 금지)

## GJC 단일 메시지 입력 한도 (≠ 컨텍스트 윈도우, 실측)
- Opus 4.8 의 GJC 컨텍스트 윈도우는 **1M** 이다(멀티턴 agentic 파일읽기로 1M까지 정상 누적).
- 단, **단일 메시지(`@file`)로 한 방에 ~400k+ 토큰을 주입하면 Opus·Gemini 가 400**(메시지 크기 한도, 윈도우 아님).
  단일-요청 입력 상한은 모델 윈도우에 비례하나 한참 낮음(실측: Opus≈350–400k, grok-4-fast≈476–500k+).
- **거대 입력은 한 메시지에 통째로 붓지 말고 청크로 나눠 누적**시키면 1M 윈도우 안에서 정상 처리된다.
  굳이 한 방에 >400k를 paste해야 하는 드문 경우에만 architect 를 `opencode-go/deepseek-v4-pro` 로(단일 메시지 476k 실수용 확인).

## 신뢰성
- 직렬 체인은 짧게(0.99^N 붕괴). 병렬 결과는 dedup 후 검증. 본체가 단일 진실원천 —
  서브에이전트끼리 직접 합의시키지 말 것.
