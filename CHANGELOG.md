# Changelog

이 가이드의 모든 변경은 이 파일에 기록한다.

**버전 규칙 (SemVer 유사 — `MAJOR.MINOR`)**
- **MINOR ↑** — 프로필/모델 배치 추가·변경(반드시 실호출 검증 동반), 또는 인프라·i18n 등 독립적 기능 추가
- **PATCH/문서** — 오타·문구·근거 보강 (버전 유지 또는 `x.y.z`)
- **MAJOR ↑** — 구조 재설계 (역할 정의·셋업 방식·라우팅 모델 변경)

각 릴리스는 git 태그(`vX.Y`)로 고정한다.

---

## v1.8.0 — 2026-07-03

### Added
- **GitHub Actions 봇 예시 `docs/examples/cyber-cop-action.yml` (#9 Lv.3)** — 셀프호스티드 러너(gjc/gjc-cop 설치·로그인) 전제의 PR 자동 리뷰 워크플로. **pwn-request 구조적 회피**: PR 코드를 체크아웃/실행하지 않고 데이터로만 리뷰하므로 `pull_request_target`(fork PR 코멘트 가능)이 안전 — checkout 스텝 금지 명시. 권한은 `issues: write`(verdict 코멘트) + `pull-requests: read`(gh pr view/diff) 최소 — `pull-requests: write`(approve 권한)는 금지. verdict가 check 결과를 겸해(**MERGE=pass / DO-NOT-MERGE=fail**) required status로 쓸 수 있고, 사람이 PR별 네이티브 auto-merge를 켜는 방식으로 **봇 never-merge 계약을 유지한 채** 극한 자동화 가능. API-키 `cyber-cop-ci` 변형은 신규 셀렉터 라이브 검증 선행 전 미출하(파일 내 문서화). 신규 셀렉터 0.

## v1.7.0 — 2026-07-03

### Added
- **`gjc-cop --install-hook` — pre-push 훅 (#9 Lv.2)** — push 직전 나가는 diff(`remote_sha..local_sha`; 신규 브랜치는 `origin/HEAD` merge-base, 없으면 tip 커밋)를 **cross-family critic 1좌석**(`openai-codex/gpt-5.5:high`)이 판정. **기본 advisory**(verdict 출력만, push 허용) — `git config cop.strict true` 또는 `GJC_COP_STRICT=1`이면 APPROVE 아닐 때 push 차단(**strict에선 좌석 도달 전 모든 실패 — gjc 부재·diff 계산 실패·5MiB 초과·좌석 실패 — 가 fail-closed**; 리뷰 반영). 우회는 git 네이티브 `git push --no-verify`. 훅 파일은 thin shim(로직은 gjc-cop `hook-exec`) — 마커 기반 멱등 설치, **기존 타 훅은 절대 덮어쓰지 않음**(거부), `--uninstall-hook`은 우리 것만 제거. diff는 `@`-첨부 비신뢰 데이터 계약 유지, verdict는 first-line 파싱(fail-toward-blocking). 신규 셀렉터 0.
## v1.6.1 — 2026-07-03 (docs)

### Docs
- **README 4종 quickstart를 gjc-cop 원커맨드 플로우로 교체** — 홍보 섹션의 클론+`$GUIDE` 경로를 v1.6.0의 **클론 없이 2커맨드**(`curl … | GJC_SETUP_COP=1 bash` → `gjc-cop <PR>`)로 교체하고 `--panel`/`shell`/`watch` 소개, 클론/수동 경로는 공지 §3 링크로 강등. 공지 문서 0단계와 문구 정합. YAML embed·표 무변경.
- **카탈로그 스냅샷 `evidence/2026-07-03-catalog.txt`** — `--diff` vs 2026-07-02: **드리프트 없음**(신규/은퇴 모델·ctx/effort 변화 0; Gemini 3.5 Pro 미입점 확인).

## v1.6.0 — 2026-07-03

### Added
- **`gjc-cop` 원커맨드 reviewer (#9 Lv.1)** — `install.sh`에 **`GJC_SETUP_COP=1`** 플래그 추가: `routing-rules.md` + `scripts/cyber-cop-review.sh` + trusted `validate-profiles.py` + `scripts/gjc-cop` 래퍼를 `~/.gjc/agent/cyber-cop/`에 배송하고 `gjc-cop` 심링크를 `~/.local/bin`에 등록(멱등). **클론·`$GUIDE` 불요**: `gjc-cop <PR>`(REPO cwd 자동감지→4섹션 verdict) · `--panel <PR>`(3표 패널) · `shell`(대화형 리뷰어 세션) · `watch [interval]`(신규 PR 폴링·리뷰, 머지 금지). 래퍼가 **항상 신뢰 로컬 경로를 주입**하므로 #6 상대경로 인젝션 풋건이 구조적으로 소멸. 신규 셀렉터 0. `cyber-cop-review.sh`는 `$CYBER_COP_VALIDATOR` env로 배송된 trusted validator 위치를 수용. 문서: 공지 §3 0단계 · MAINTAINING §2.
## v1.5.7 — 2026-07-03 (docs errata)

### Fixed
- **`evidence/2026-07-03-errata.md` 신설 (append-only 정정)** — ultimate-final-report §2 벤치 표에서 Composer 2.5의 `74.7% → 54.0%` 붕괴 수치가 **SWE-bench Verified 열에 오배치**(정답: **Pro**; 같은 문서 §3.2·deep-research는 Pro로 정확히 인용). `evidence/`는 재작성 불가 감사추적이므로 **원본은 verbatim 보존**하고 dated errata 리포트로 정정. 판정 영향 없음. (codex-bot P2, PR #5 post-merge — repo 전체 미회신 코멘트 스윕에서 발견.)

## v1.5.6 — 2026-07-03

### Fixed
- **`scripts/cyber-cop-review.sh` 단일 모델 붕괴 교정 (#10, BLOCK급)** — 기존 헬퍼는 단일 `gjc -p --mpreset cyber-cop` 세션에 "4섹션 verdict"를 요구했고, 좌석 위임이 일어나지 않아 **본체(Opus)가 critic verdict까지 롤플레이**했다(세션 로그: task 위임 0·비-anthropic 좌석 0). cross-family 자기선호 방어가 라벨만 남고 위조되던 결함. **좌석 오케스트레이터로 재작성(Option A)**: architect=`anthropic/claude-opus-4-8:high`·critic=`openai-codex/gpt-5.5:high`를 좌석별 `gjc -p --model …`로 개별 호출 → critic이 **실제 cross-family로 실행**됨(호출 구조로 보장). 각 섹션 헤더에 실행 모델 명기, 불변식은 스크립트가 직접 `validate-profiles.py` 실행, 머지 권고는 verdict·불변식에서 결정론적 산출. `--panel` 플래그로 고위험 3표 cross-family 패널(+grok-4.3·gemini-3.1-pro-low). 페이로드는 기존 `@`-첨부·비신뢰 데이터 계약 유지. MAINTAINING §2·공지 문서 §3 정합.
- **`scripts/validate-profiles.py` `--root <dir>` 인자 추가** — 신뢰 검증기를 임의 트리의 데이터(gjc-profiles.yml + README*.md)에 대해 실행. cyber-cop 오케스트레이터가 PR head를 **코드 실행 없이 데이터로만** 검증하는 데 사용(RCE·import 셰도잉 차단).

## v1.5.5 — 2026-07-03 (docs)

### Docs
- **README 4종에 `cyber-cop` 대대적 홍보 섹션 추가** — 히어로 직후 상단에 featured 섹션(첫 reviewer 모드·역할 반전·cross-family critic 편향차단·3표 패널)과 "이 레포가 스스로 검증(PR #4~#7에서 머지 전 결함 10건 차단 + 머지 후 1건 → #7 수정)" 실증, 원라이너 시작 예시(REPO·`$GUIDE` 명시), 공지 문서 링크. 기존 1줄 What's New TIP를 대체. 버전 배지 1.5 → 1.5.5. YAML embed·표·프로필 매핑 무변경.

## v1.5.4 — 2026-07-03 (docs)

### Fixed
- **`docs/whats-new-cyber-cop.md` TL;DR** — the quick-start helper command used a relative `scripts/cyber-cop-review.sh`, which is absent after the one-line install (installer ships only `gjc-profiles.yml`) or when the reader is inside the repo under review. Now points at `$GUIDE/scripts/cyber-cop-review.sh` (setup-guide checkout), consistent with §3. (codex-connector[bot] P2, post-merge follow-up to #6.)

## v1.5.3 — 2026-07-03 (docs)

### Docs
- **`docs/whats-new-cyber-cop.md`** — cyber-cop reviewer 모드 공지(KO 정본, non-normative): 갭 논증(12종 author 모드·자기선호 편향·역할 가중치 반전) ·
  Use case · 사용법 3단계(수동 / 세션 상주 오케스트레이션 / 상설 PR-cop 세션) · 고위험 3표 패널과 xai 강등 경로 ·
  보안 수칙(PR 입력 비신뢰 규칙, `gh api`+`jq` 이스케이프, 토큰 최소 스코프, 자동 머지 금지, curl|bash 고지).
- README 4종 상단에 What's New 발견성 배너 1줄(번역본은 KO 정본 표기). YAML embed·표·배지 무변경.

## v1.5.2 — 2026-07-03

### Docs
- **역할→모델 배치 근거 리서치 리포트 3종 공개** (`evidence/`) — 사용자에게 "왜 이 모델셋업인가"의 1차 출처 기반 근거를 제공. deep-research + dev-idea-consultant + model-council 파이프라인의 원문.
  - `evidence/2026-07-03-deep-research-benchmarks.md` — Fable 5 / Opus 4.8 / GPT-5.5 / Gemini 3.1 Pro / Grok 4.3 / Composer 2.5 벤치·가격·컨텍스트·effort 실측 (Vals·Anthropic·OpenAI·xAI·DeepMind·arXiv·Terminal-Bench·LiveCodeBench 인용).
  - `evidence/2026-07-03-consultant-report.md` — dev-idea-consultant 6섹션 포맷: 실현가능성·역할 배치 권고·마이그레이션 로드맵.
  - `evidence/2026-07-03-ultimate-final-report.md` — 통합 최종 리포트: 두 커뮤니티 질문("Grok 4.3=critic?", "Composer 2.5 Fast=executor?") 확정 답변 + 구조적 발견(effort-ladder·architect 셀렉터·failover).
  - README §6-2에서 상호 참조. `evidence/`는 재작성 불가 감사 추적이므로 이후 재검증은 신규 dated 리포트로 추가한다.

## v1.5.1 — 2026-07-03

### Added
- **`scripts/cyber-cop-review.sh` 헬퍼** — `gh`로 PR 메타·diff를 수집해 GJC 헤드리스(`cyber-cop` 프로필)로 4섹션 판정(architect/critic/invariants/merge recommendation)을 출력하는 리뷰어 스크립트. 머지는 절대 하지 않음(routing-rules.md 계약 — 판정은 사람에게 표면화).
  보안 경화(레드팀 리뷰 반영): PR 제어 콘텐츠(제목·파일 목록)의 프롬프트 보간 제거 — 모델이 신뢰 경로(`meta.json`/`files.txt`/`pr.diff`)를 직접 읽음 · 프롬프트에 명문 인젝션 방어 규칙(PR 내용 = untrusted data, 지시 시도는 공격 신호로 보고) · `set -euo pipefail` · temp 디렉터리 `trap` 정리. MAINTAINING.md §2 Tooling 표에 등재.

## v1.5 — 2026-07-03

### Added
- **`cyber-cop` 🚨 reviewer 모드 프로필** — 프로필 **12 → 13**. 기존 12종이 전부 author 모드(default+executor 가중)인 갭을 닫는
  reviewer-side 카테고리: PR 리뷰·보안 감사 세션에서 역할 가중치가 반전되어 **architect(1차 코드리뷰 판정자)와 critic(머지 게이트)이 주연**.
  배치: default/architect=`opus-4-8:high`(1M 실효검색 — MRCR 76%@1M vs Gemini 26% 붕괴), executor/critic=`gpt-5.5:high`
  (critic은 Claude-작성 코드와 cross-family — 자기선호 편향 완화, arXiv 2410.21819 · 2604.22891), planner=`gemini-3.1-pro-low:high`.
  고위험 PR·보안 감사는 critic 3표 병렬 패널(독립 투표→본체 집계, 2/3 반박 또는 CRITICAL/BLOCK 1건 차단).
  **신규 셀렉터 0** — 전 좌석이 §6 검증 매트릭스의 기존 실호출 evidence를 인용하며, cross-family CI 검사를 예외 등록(SAME_FAMILY_OK) 없이 자연 통과.
- **`routing-rules.md` 리뷰어 계약 6조항** — 스왑 행(PR 리뷰·보안 감사 → cyber-cop) · 위임 순서(리뷰 진입→architect 선호출, 머지 게이트→critic/패널) ·
  default=집계자 제한(critic raw verdict 보존·노출) · 증거 계약(critic 1표당 file-backed blocking issue 또는 no-finding rationale) ·
  provenance fallback(작성 모델 unknown이면 non-default family ≥2 호출) · 근거 없는 LGTM 금지. `escalation`(author-side 게이트)과의 역할 구분 명시.

### Verified / Changed (red-team 딥리서치 2026-07-03)
- **12프로필 재검증**: deep-interview→ralplan→ultragoal 파이프라인으로 재감사. 결과 **12 인큐번트 12/12 KEEP**(모델 배치 무변경) — 아키텍처가 근거기반임을 확인. `cyber-cop`은 이 12종 감사와 별개로 추가된 13번째 reviewer-side 프로필이다.
- **L3 행동실측**: Fable-default 라우터 A/B(`ultimate` vs `legend`, 8쌍) — Fable-default는 품질 근소우위이나 **Opus 대비 1.83× 비용 + benign 과제 1건 refusal/error**. → Opus=권장 default, Fable=opt-in premium 재확인(ultimate-f5/legend 주석에 반영).
- **Composer**: Fast는 executor 부적합 재확인(=Standard 6×가·effort knob 없음·200k·reward-hacking 붕괴). grok-build Standard 접근성 미검증으로 `ultimate-fast`는 조건부 보류.
- **council 4대 권고 판정**: effort-ladder=ACCEPT, architect 셀렉터=RESOLVED(`-low:high` 유지), 메타심판 2차critic=ACCEPT(문서), ultimate-fast=조건부.
- **능력/비용정규화 이중 순위표(7/7 전후 2국면)**: Opus가 두 국면 모두 비용정규화 1위 — v1.4 split이 7/7 이후 더 방어적이 됨.
- 증거: `evidence/2026-07-03-l3-fable-rolefit.{jsonl,md}` · `evidence/2026-07-03-redteam-report.md`.

### Fixed
- **GitHub 앵커 VS16 결함 교정**: GitHub 슬러거는 이모지를 제거하되 **U+FE0F(변이 선택자)를 보존**한다(라이브 렌더링 HTML로 실측).
  `🗂️`(U+1F5C2 U+FE0F) 헤딩을 가리키는 §5 카탈로그 앵커 8곳(README×4)과 KO `#7-…-설치--제거`(🛠️) 앵커를 실동작 슬러그로 교정.

### Docs / Assets
- profiles-matrix.svg 재생성(13 프로필). README×4 배지(version-1.5 · profiles-13)·카운트·푸터 동기. gjc-profiles.yml 헤더 v1.5—13.

## v1.4 — 2026-07-02

### Added
- **Claude 5 패밀리 지원**(2026-07-01 출시, gjc 0.7.10 실호출 검증) — 프로필 **10 → 12**:
  - `ultimate-f5` 🔥 이벤트 프로필: default/executor = **Fable 5**(SWE-bench Verified **95.0** 신 1위, Opus 4.8 88.6 대비).
    구독 포함은 **~2026-07-07**(Pro/Max/Team 주간 한도의 50% 상한)뿐이며 이후 **usage credits($10/$50 per MTok)** 별도 과금 —
    "무료" 아님. 안전 분류기 거부가 **HTTP 200 + `stop_reason: refusal`** 로 오는 점 유의.
  - `legend` 👑 (display_name `legend5` — 동명 로컬 커스텀 프리셋 보호): 7/7 이후에도 지속 가능한 최강 구성 —
    Fable 5 는 default 한 자리만(credits 노출 최소), executor 는 `opus-4-8:max` 유지. credits 회피 시 default를 `opus-4-8:high`로.
- **effort 클램프 표 (GJC 실효 ≠ API)**: fable-5 상한 **xhigh**(`:max`는 xhigh로 침묵 클램프, thinking 상시-온) ·
  sonnet-5 상한 **high**(`:xhigh`/`:max` 침묵 클램프, 토크나이저 변경으로 동일 텍스트 ~30% 토큰 증가).
  API는 두 모델 모두 max 지원 — **GJC 파서 갭은 상류 제보됨**.
- §10 가격표: Fable 5($10/$50, 배치 $5/$25, 캐시 히트 $1) · Sonnet 5($3/$15, 인트로 $2/$10 ~2026-08-31) · GLM-5.2 행 추가.
  경쟁 동향 각주: GPT-5.6 Sol 파트너 프리뷰(6/26) · Gemini 3.5 Pro 7월 GA 연기 · Grok 4.5 프라이빗 베타 ·
  DeepInfra 신규 프로바이더(GJC 0.7.9~, DeepSeek V4 Pro/Flash + service-tier).

### Changed
- **`escalation` 재설계**: executor를 `claude-fable-5:xhigh`로 — 실패한 작업의 **구원투수**(간헐 투입이라 7/7 이후 credits 과금과도 궁합).
  critic의 기존 `xai/grok-4.3:xhigh`는 **no-op이었음**(xai 프로바이더 상한 high — 침묵 클램프로 ultimate와 동일 동작;
  xhigh는 grok-build 프로바이더 전용) → `:high`로 정정하고 클램프를 하드룰로 문서화.
- **`solo-anthropic` 전 역할 Opus 전환**(critic Sonnet 4.6 → Opus 4.8): 능력 우선 선택.
  ⚠자기선호 편향 캐비앗 병기 — 강한 모델일수록 편향이 더 큼(arXiv 2410.21819, 2604.22891), cross-family 프로필이 품질 경로.
  Sonnet 5 critic은 리뷰어 버그 리콜 실측 하락(63%→50%, CodeRabbit)으로 기각.
- **`eco.critic`**: `gemini-3.5-flash` → **`gemini-3.5-flash-low` 리터럴 핀**(구 셀렉터는 카탈로그에 리터럴 id가 없어 퍼지 매칭으로 우연 동작).
  glm-5.2 "라이브-카탈로그 전용" 캐비앗 폐기(0.7.10 번들 카탈로그 편입). eco executor 대안으로 `sonnet-5:medium`(≈sonnet-4-6:high, 인트로가) 주석.
- **codex ctx 룰 재작성**: 일괄 "272k" 폐기 → **gpt-5.4=1M / gpt-5.5=272K**(400K→272K 축소).
  solo-openai architect = gpt-5.4(1M)로 근거 정정, monorepo codex 배제 논거 재서술.
- **불변식 재서술**: "default=Opus 고정" → **"default=Anthropic 플래그십(Opus 4.8/Fable 5)"** (README·MAINTAINING·routing-rules·SVG 전체).
- `routing-rules.md`: Claude 5 하드룰 행(fable-5 xhigh 클램프·refusal, sonnet-5 high·토크나이저) +
  에스컬레이션 사다리에 모델별 상한 주석 + codex ctx 룰 갱신.

### Fixed
- `catalog-snapshot.sh`: `--diff`가 macOS(bash 3.2)에서 `mapfile` 미지원으로 고장 + 실패 후 스냅샷 덮어쓰기로 폴스루 → bash 3.2 호환 재작성.
  쿼리 stem 목록에 'fable' 부재로 드리프트 감지가 **claude-fable-5를 구조적으로 못 보던 맹점** 수정.
- `revalidate.sh`: 자격증명 만료를 회귀(`fail[]`)로 오분류 → `blocked(creds)` 분리 분류 추가.
- `validate-profiles.py`: fable-5/sonnet-5 effort 룰 추가(기존엔 WARN만), grok 룰 프로바이더 분리(xai ≤high —
  escalation no-op을 CI가 못 잡던 공범), gpt-5 base 룰 수정, dead-expression 정리.
- `install.sh`: 하드코딩 "10종" 카운트·로스터를 파싱 파생값으로; GJC 0.7.10 프리셋 rename/delete가 센티널 주석을 제거해
  managed block이 이름 기반 교체로 격하되는 경우(삭제 프로필 부활·수정 덮어쓰기) 경고 출력 + 문서화.
- CHANGELOG v1.3 날짜 정정(06-18 → 실제 태그 날짜 06-19).

### Docs / Assets
- SVG 재생성: role-winners(default 카드 → Fable 5) · profiles-matrix(12 프로필, 푸터 불변식 "Anthropic 플래그십"으로 재서술) ·
  effort-ladder(6단계 전부 + 모델별 클램프 스트립).
- 검증 매트릭스·배지 → **2026-07-02**(gjc 0.7.10 라이브 배터리 + 마이크로벤치 20/20 정답; openai-codex 재인증 후 `gpt-5.5:high` 검증 OK).
  `gemini-3.1-pro-high`는 카탈로그 목록에 떠도 호출은 여전히 400 — 함정 명시 유지.

## v1.3 — 2026-06-19

### Added
- **다국어(i18n)**: 영문 `README.en.md` · 중문 `README.zh.md` · 일문 `README.ja.md` 추가. 한국어 정본 포함 4개 파일 상단에 언어 내비. 셀렉터·YAML은 verbatim, 프로즈·YAML 주석은 번역, 심층 분석(§6-2/6-3)은 요약 + 한국어 정본·공식 docs 링크.
- `scripts/validate-profiles.py` 확장: **모든 `README*.md`의 임베드 YAML == `gjc-profiles.yml`** 패리티 검사(번역본 드리프트 방지). CI에 포함.

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
