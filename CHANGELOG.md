# Changelog

이 가이드의 모든 변경은 이 파일에 기록한다.

**버전 규칙 (SemVer 유사 — `MAJOR.MINOR`)**
- **MINOR ↑** — 프로필/모델 배치 추가·변경 (반드시 실호출 검증 동반)
- **PATCH/문서** — 오타·문구·근거 보강 (버전 유지 또는 `x.y.z`)
- **MAJOR ↑** — 구조 재설계 (역할 정의·셋업 방식·라우팅 모델 변경)

각 릴리스는 git 태그(`vX.Y`)로 고정한다.

---

## v1.1 — 2026-06-18

### Added
- **Claude+Codex 2벤더 프로필** 2종: `claude-codex`(평소 균형), `claude-codex-max`(비용무시 최강).
  설계 — **Anthropic = 실행·컨텍스트**(default·executor·architect=Opus; codex 272k라 1M ctx는 Opus만),
  **Codex = 추론·비평**(planner=gpt-5.5 / critic=GPT, executor=Opus와 cross-family).
- **버전 관리 도입**: CHANGELOG · version 배지 · git 태그(`v1.0`/`v1.1`).

### Changed
- 프로필 **8 → 10**. 매트릭스 SVG · README 표/임베드 YAML · install.sh 동기.

---

## v1.0 — 2026-06-18

### Added
- 초판. claude·gpt·grok·gemini·opencode go **5벤더 역할 분담 8프로필**
  (daily★/ultimate/coding-sprint/escalation/eco/monorepo/solo-anthropic/solo-openai).
- `routing-rules.md`(본체 운영 규칙, `@`로 주입) · `install.sh`(원클릭 안전 병합) · SVG 5종(매트릭스·역할승자·아키텍처·라우팅·effort).
- §6 검증 매트릭스 · §6-2 최적성 검토 · §6-3 잔여공백·GJC 실효 ctx 실측.

### Verified (GJC 실호출, 2026-06-18 · GJC 내부 재검증 20/20)
- `gemini-3.1-pro-low:high` = 네이티브 고추론 (`gemini-3.1-pro-high`는 400 — 백엔드 id 부재).
- `openai-codex`는 base GPT만(`gpt-5.5`/`gpt-5.4`) — `-codex` 변종 미지원.
- `opencode-go/glm-5.2` 서빙 확인 → monorepo critic 채택(신규 오픈웨이트 1위).
- Opus 4.8 컨텍스트 윈도우 = **1M**(멀티턴 누적). 단일 메시지 입력 한도 ~400k는 윈도우와 별개.
- architect 장문맥: 명목 1M ≠ 실효 — Gemini 1M 26.3% 붕괴 / Opus 4.6 76% 유지.
