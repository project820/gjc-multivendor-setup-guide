# Changelog

이 가이드의 모든 변경은 이 파일에 기록한다.

**버전 규칙 (SemVer 유사 — `MAJOR.MINOR`)**
- **MINOR ↑** — 프로필/모델 배치 추가·변경 (반드시 실호출 검증 동반)
- **PATCH/문서** — 오타·문구·근거 보강 (버전 유지 또는 `x.y.z`)
- **MAJOR ↑** — 구조 재설계 (역할 정의·셋업 방식·라우팅 모델 변경)

각 릴리스는 git 태그(`vX.Y`)로 고정한다.

---

## v1.2 — 2026-06-18

### Added
- **업스트림 채택**: 가이드 압축판이 GJC 본 레포에 `docs/multi-vendor-profiles.md` 로 머지됨([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev`). README 상단에 공식문서 배너 + 포지셔닝(이 레포 = 설치기·전체 프로필·검증 도구) 추가.

### Docs
- 검증된 셀렉터 표에 **라이브-카탈로그 주의** 추가: `opencode-go/glm-5.2`·`google-antigravity/gemini-3.5-flash` 는 번들 스냅샷에 없고 프로바이더 디스커버리로만 해석되므로, 갱신 전엔 `selector did not resolve` 로 활성화 실패 가능 — 재로그인/재시도 또는 번들 대체(`opencode-go/deepseek-v4-pro` / `zai/glm-5.2`). (upstream PR #860 레드팀 리뷰 반영.)

### Infra
- **지속 유지보수 기반 추가** — 세션 독립으로 레포가 자가검증·벤치·드리프트 추적 가능:
  - `scripts/validate-profiles.py` (크레덴셜 불요 정적 검증: 5역할·router 불변식·cross-family[예외 allowlist]·effort 하드룰·README 임베드 동기) + GitHub Actions `validate-profiles`.
  - `scripts/revalidate.sh` (인증 머신 라이브 셀렉터 배터리 → `evidence/<date>-selectors.md`, 회귀 시 비정상 종료).
  - `scripts/catalog-snapshot.sh` (라이브 카탈로그 스냅샷 + `--diff` 드리프트 감지).
  - `evidence/` 날짜별 감사 추적 시드(2026-06-18) · `MAINTAINING.md` 플레이북.

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
