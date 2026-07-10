# Changelog

이 가이드의 모든 변경은 이 파일에 기록한다.

**버전 규칙 (SemVer 유사 — `MAJOR.MINOR`)**
- **MINOR ↑** — 프로필/모델 배치 추가·변경(반드시 실호출 검증 동반), 또는 인프라·i18n 등 독립적 기능 추가
- **PATCH/문서** — 오타·문구·근거 보강 (버전 유지 또는 `x.y.z`)
- **MAJOR ↑** — 구조 재설계 (역할 정의·셋업 방식·라우팅 모델 변경)

각 릴리스는 git 태그(`vX.Y`)로 고정한다.

---

## v2.0.0 — 2026-07-10

### Changed (MAJOR — 카탈로그 구조 재설계)
- **13 프로필 → 10 번들 · 4계층(tier)**. "동등한 프로필 N개" 모델을 폐기하고 신뢰 등급이 다른 4계층으로 재편: **Core**(`daily`·`coding-sprint`·`cyber-cop` — 구독 OAuth 3벤더) / **Premium experimental**(`ultimate-opus`·`ultimate-sol`·`dream-team` — role-fit L3 전 "최강" 단정 금지) / **Workflow bundle**(`llm-council`·`escalation` — 좌석표 + routing-rules 의 Council/Escalation 계약 필수) / **Specialized experimental**(`eco`·`monorepo`). 근거: 2축 블라인드 독립 딥리서치(Claude Fable 5 Ultracode + Parallel.ai Ultra 2x, 2026-07-10) 공통 verdict REVISE + 인간 configuration freeze(동일자).
- **이름 승계**: `ultimate`→`ultimate-opus`(executor `:max`→`:high`, architect gemini→**opus** — MRCR 1M 실효검색) · `ultimate-f5`/`legend`→`dream-team`(Fable default+executor). **신설**: `ultimate-sol`(Sol 3좌석 — 유일한 비-Anthropic default, validator 예외 등재) · `llm-council`(4계열 합의 좌석표).
- **삭제**: `solo-anthropic`·`solo-openai`·`claude-codex`·`claude-codex-max` — v2 멀티벤더 원칙(전 번들 `required_providers ≥ 2`, 혼합 구독 콜라보레이션 — 인간 판정 2026-07-10). 단일·2벤더 수요는 GJC 0.9.6 내장 프로필(`claude-opus`/`claude-fable`/`codex-*`/`opus-codex`/`fable-opus-codex`)이 흡수(매핑 등가 아님 — 구판 좌석은 `git show v1.11.0:gjc-profiles.yml`).
- **좌석 변경**: `daily.planner` gemini→`gpt-5.6-sol:high` · `daily.critic` grok→`opus-4-8:high`(xai 키 장벽 제거 — 구독-only 3벤더 daily) · `coding-sprint.planner` gemini→`gpt-5.6-sol:high`(critic terra 유지 — plan/crit 동계열은 SAME_FAMILY_OK 등재) · `coding-sprint`/`ultimate-opus` executor `:max`→`:high`(실패신호 시에만 격상) · `eco` 전면 재편: default `opus:low`→`terra:medium`, planner `grok-4-1-fast:high`(**xAI 2026-05-15 retire — grok-4.3 요율 redirect 과금, 공식 migration 문서**)→`gpt-5.6-luna:medium`(Luna 첫 채용), architect `-low:high` 리터럴 핀, critic `gemini-3.5-flash-low`(**07-10 오후 라이브 소멸**)→`gemini-3-flash:low`, anthropic·xai 제거(3벤더). `escalation`·`cyber-cop`·`monorepo` 매핑은 v1.11.0 그대로(KEEP).
- **GJC 0.9.6 재기준화** — 당일(07-10 12:36 KST) 릴리스 확인 후 업그레이드(바이너리 sha256 = 공식 자산 digest). 카탈로그 유일 diff: gpt-5.6 3종 ctx **272K→373K** usable prompt budget. antigravity 퍼지 공간 **fail-closed** 전환(`gemini-3.1-pro-high`/`-bogus`는 이제 "not found" — 0.9.5 침묵 -low 해석 함정 재현 안 됨, `-low:high` 핀은 유지). 전 문서·주석·SVG 스탬프 0.9.6/373K 동기화.
- **validator 확장**: `NON_ANTHROPIC_DEFAULT_OK`(ultimate-sol) · 멀티벤더 불변식(`required_providers ≥ 2` 하드에러) · `SAME_FAMILY_OK` 재작성(monorepo 유지 + ultimate-opus/dream-team exec_arch + coding-sprint plan_crit — 인간 판정 근거 명기, 전부 WARN 영구 표면화).
- **routing-rules.md v2**: 번들 4계층 표 + **Council 계약**(병렬 독립호출·상호 비공개·raw verdict 보존·CRITICAL/HIGH dissent 비다수결) + **Escalation 계약**(수동 트리거·재시도 예산·Fable refusal 시 Opus 강등·human gate) 신설. Grok critic 좌석 의미 재정의: "결함회수 최강"이 아니라 **제3계열 독립 dissent**(2축 리서치 합의 — critic-specific 근거 0건).
- README×4 전면 동기화(4열 tier 표·설계 근거·마이그레이션·비용표) · install.sh 예시 · gen_svgs(10번들 매트릭스·dream-team 배너).

### Validation
- 실호출(2026-07-10, **gjc 0.9.6**): `SELECTORS_ONLY=1 revalidate.sh` → `evidence/2026-07-10-selectors-rerun-3.md` — **v2 출하 셀렉터 전 좌석 그린**(+ 수동 4행: `gemini-3-flash:low`·`opus:medium`·`terra:medium`·`luna:medium` ok). 배터리가 antigravity 라이브 표면 당일 드리프트(`gemini-3.5-flash*`·`gemini-pro-agent` 소멸)를 적발 → eco.critic 교체로 즉시 반영(검증 안 된 셀렉터 출하 금지 원칙). `python3 scripts/validate-profiles.py` green(신규 불변식 + README×4 파리티, 의도된 WARN 5건).

### Evidence
- `evidence/2026-07-10-catalog-gjc096.txt`(0.9.5 대비 diff = gpt-5.6 373K뿐) · `evidence/2026-07-10-selectors-rerun-3.md`(0.9.6 첫 배터리 + findings) · `evidence/2026-07-10-errata.md`(E1: BrowseComp 열 오귀속 84.3=Opus/85.9=Gemini · E2: Luna T-B 84.3/84.7→84.7 채택 · R1: grok-build 재조회 — 4.5 여전히 xai 전용).
- 리서치 freeze 정본(레포 외부): `~/multivendor/research/2026-07-10-gjc-v2-profile-review/outputs/two-axis-synthesis-and-proposed-config-v1.md`(Amendment A1 포함, SHA256 고정).

### Not shipped
- Premium 3종의 role-fit L3 실측(승격 조건) · gpt-5.6 `:max` reasoning-token 계측 · Fable refusal 정량화 · Council/Escalation E2E 검증 · 번들별 비용 실측 — freeze 문서 §8의 후속 실험 목록.

## v1.11.0 — 2026-07-10

### Changed
- **GPT-5.6 세대교체 (Tier 1, like-for-like)** — GPT-5.6 Sol/Terra/Luna GA(2026-07-09) 반영. 전 gpt-5.5 좌석 → **`gpt-5.6-sol`**(동가 $5/$30, 동일 effort): ultimate/ultimate-f5/legend/escalation.planner`:xhigh` · cyber-cop.executor/critic`:high`(+고위험 패널 좌석) · solo-openai default/executor/planner · claude-codex.planner · claude-codex-max.planner/critic. 1M ctx 근거가 아닌 gpt-5.4 좌석 → **`gpt-5.6-terra`**(동가 $2.5/$15, ≈GPT-5.5급): daily.executor`:high` · coding-sprint.critic · claude-codex.critic · solo-openai.critic. **유지**: solo-openai.architect=gpt-5.4:high(유일 1M ctx 레인) · monorepo(5.6도 codex 272K라 배제 지속) · eco. **미채용**: Luna(포지션 없음) · `:max` 셀렉터(수용되나 심도 미검증 — 출하 상한 xhigh). 도구 좌석 동기화: cyber-cop-review.sh CRIT_MODEL · gjc-cop pre-push 훅 · revalidate.sh 배터리 · gen_svgs · README×4 · routing-rules · MAINTAINING · whats-new-cyber-cop.
- **Fable 5 이벤트 연장 반영** — 구독 포함 종료 ~7/7 → **~2026-07-12 23:59 PT(연장 확정)** 전면 정정(profiles 주석 · README×4 표/불릿/비용 · SVG 스탬프). Anthropic "capacity 확보 시 구독 복귀 방침(비확정)" 병기.
- **gemini-3.1-pro-high 함정 형태 변화 (0.9.5)** — 카탈로그 delisting + 실측: 이제 400이 아니라 **퍼지 매칭으로 `-low` 기본 effort에 침묵 해석되어 "성공"**(`-bogus`도 성공). 문서를 "호출 400" → "성공하지만 고추론 아님" 함정으로 재작성, revalidate 카나리를 expect-fail → informational ok-live 재분류.
- README 배지 정정: v1.6 이후 누락됐던 version 배지 → 1.11.0.
- **리뷰어 좌석 escape hatch** — PR #19 critic(gpt-5.6-sol) HIGH 지적("머지 게이트 좌석을 rolefit 실측 없이 교체") 절충: `CYBER_COP_CRIT_MODEL`(cyber-cop-review.sh) / `GJC_COP_HOOK_MODEL`(gjc-cop pre-push 훅) env로 critic 좌석을 즉시 다른 cross-family 모델(예: gpt-5.5:high)로 핀 가능. 판정 원문·반론·수용 내역은 `evidence/2026-07-10-gpt-5.6-notes.md` §8.

### Validation
- 실호출(2026-07-10, gjc 0.9.5): gpt-5.6-sol `:medium`/`:high`/`:xhigh` · terra `:high`/`:xhigh` · luna `:high` 전부 ok · 3종 `:max` 수용(심도 미검증 — 미출하) · `:bogus` 거부. `SELECTORS_ONLY=1 revalidate.sh` → `evidence/2026-07-10-selectors-rerun-2.md` **전 프로바이더 그린**(Anthropic rate-limit 해제 — fable-5/sonnet-5/opus/sonnet-4-6 재검증, 07-02 last-good 캐비앗 해소). 첫 `2026-07-10-selectors.md`는 gemini-3.1-pro-high 행동 변화를 fail-closed로 잡은 스냅샷으로 보존. `python3 scripts/validate-profiles.py` green(README×4 파리티).

### Evidence
- `evidence/2026-07-10-gpt-5.6-notes.md` — 방법론(당사자 Codex 조사본 → 독립 병렬 리서치 교차검증 → 실호출), 확정 팩트, **불일치 기록**(OpenAI의 Sol SWE-Bench Pro 미공표 vs 당사자 표 64.6% 충돌 · METR의 Sol SWE 평가 게이밍 적발 — SWE류 벤치 단독 근거 승격 금지), Fable 연장 근거, 카탈로그 드리프트, `:max` 심도 프로브 결론불가 기록.
- `evidence/2026-07-10-catalog.txt`(diff: gpt-5.6 3종 추가 · gemini-3.1-pro-high 제거) · `evidence/2026-07-10-selectors.md` · `evidence/2026-07-10-selectors-rerun-2.md`(authoritative).

### Not shipped
- gpt-5.6 `:max` effort(reasoning-token 계측 후 별도 판단) · Luna 좌석 · Sol Fast($12.5/$75) · Sol/Terra L3 rolefit 실측(후속 PR — SWE류 벤치는 METR 게이밍 적발로 단독 근거 불인정).

## v1.10.0 — 2026-07-09

### Changed
- **Grok 4.5 critic refresh (Tier 1)** — grok-4.5 입점(2026-07-09, gjc 0.9.1)에 맞춰 critic 슬롯을 grok-4.3 → **xai/grok-4.5** like-for-like 스왑: `daily.critic`=`:medium`, `ultimate`/`ultimate-f5`/`legend`/`escalation`.critic + cyber-cop 고위험 xai 패널 좌석=`:high`. cross-family 불변 유지, cyber-cop.critic(gpt-5.5)·eco(grok-4-1-fast)·기타 프로필 무변경.
- grok-4.5 팩트 반영: xai API 전용(grok-build/OAuth 변종 없음) · provider ctx 500K(auto-compact 80% → exact-diff 안전 ~400K) · GJC `--list-models` 스테일 222K/8.9K(보수적 하한) · effort 천장 high(`:xhigh`/`:max`는 high로 침묵 클램프 → 미출하) · 가격 $2/$6 실효 $0.84/$6.2(@88% cache). 엔진 하드룰 헤더 0.7.10 → 0.9.1, README×4·routing-rules·MAINTAINING·gen_svgs 동기화.

### Validation
- 실호출(2026-07-09, gjc 0.9.1): `xai/grok-4.5:medium`·`:high` ok · `:xhigh`/`:max` high 클램프 · `:bogus` 거부. `scripts/revalidate.sh` → `evidence/2026-07-09-selectors-rerun-4.md`(첫 `2026-07-09-selectors.md`는 rate-limit 분류 보강 전 false-regression 스냅샷, `rerun-2/3`은 중간 snapshot으로 보존). `python3 scripts/validate-profiles.py` green(파리티 + grok-4.5 `:xhigh`/`:max` 거부). README 4종 배지는 07-09 rerun 적용 범위를 Grok/OpenAI/Gemini/opencode로 명시.
- PR #18 cyber-cop 1차~4차 패널 지적 반영: Grok 4.5 패널 좌석은 diff가 ~400K-token 안전 예산을 넘으면 optional VOID 처리, `revalidate.sh`는 expected-fail canary가 갑자기 성공하거나 auth/quota로 불명확하면 nonzero 처리, README×4/`gjc-profiles.yml`/SVG의 검증 문구를 07-09 rerun 범위와 Anthropic 07-02 last-good로 정정, Grok 4.5 effort/latency 표를 `low/medium/high` 및 ~50s high-effort 벤치로 정정.

### Evidence
- `evidence/2026-07-09-catalog.txt`(diff: grok-4.5 추가만) · `evidence/2026-07-09-selectors-rerun-4.md`(final authoritative rerun after cyber-cop fixes; Anthropic seats blocked by 7d rate-limit, grok/openai/gemini/opencode OK, expected-fail canaries enforced fail-closed) · `evidence/2026-07-09-grok-4.5-notes.md`(models_cache 500K/auto-compact/네이티브 effort low-med-high, 카탈로그 불일치, xhigh/max 클램프, 지연 벤치, 가격, AA 벤치 GPQA 93.1 등 — 출처 명시).

### Not shipped
- grok-4.5의 executor/planner/architect/default 승격 없음 — 벤더/벤치 주장만으로 주력 역할 출하 금지. 주력 배치는 별도 Tier 2 L3 rolefit(planner/executor/architect + critic high/medium A/B) 실측 후 후속 PR. `:xhigh`/`:max` 셀렉터 미출하.

## v1.9.0 — 2026-07-06

### Added
- **Extragoal maximalist edition (opt-in: `GJC_SETUP_EXTRAGOAL=1`)** — GPT-5.5 Pro 구독자가 Pro의 심층 추론을 개발·QA·보안점검에 활용하도록, 상류 gajae-code의 extragoal 외부 리뷰 게이트를 이 가이드에서 설치 가능한 경험으로 포장한다. `install.sh`가 상류 스킬 템플릿을 **커밋 SHA 핀**으로 fetch·추출(frontmatter-first, fail-loud 검증)하고 courier 레인 도구 4종(`extragoal-gate-init`·`extragoal-courier-{pack,secret-scan,verdict}`)을 `~/.gjc/agent/extragoal/`에 배송, `~/.local/bin`에 등록한다. **상류 기본 레인(headless GJC 리뷰어)은 항상 바닥으로 남고 Pro 레인은 어느 단계에서도 전제조건이 아니다.** `docs/extragoal-maximalist.md`가 3단 사다리(수동 courier → `--check-env` 반자동 → 상주 브라우저)와 회전수-1 Pro 활용 독트린을 문서화. courier 도구는 전부 fail-closed(시크릿 히트 차단, verdict 마지막-비공백-줄 파싱, 인용/CRITICAL-동반 APPROVE malformed 처리, Stage 0 클린트리·기본브랜치·빈diff 거부). insane-review는 fivetaku 소유(MIT)라 설치하지 않고 마켓플레이스 경로·env 계약만 안내. 프로필 변경 0, 신규 셀렉터 0.

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
