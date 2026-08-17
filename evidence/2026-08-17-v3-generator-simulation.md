# 2026-08-17 — v3 파생·동기화 표면 사전 검증

본문: `gen_svgs.py` 가 v3 로스터에서 요구하는 편집 3건
· 부록 1: `revalidate.sh` 로스터는 자동
· 부록 2: `docs/factsheet.md` §2 · `install.sh` 로스터 실측
· 부록 3: i18n 미러 계약 감사
· 부록 4: CI 워크플로 파일명 오류 수정 + 스니펫 실증 · `routing-rules.md` 점검

**목적**: `V3-HANDOFF.md` 는 "SVG 재생성 = 생성기가 v3 YAML 에서 좌석을 파생한다" 로
적어놨다. 파생은 맞지만 **자동은 아니다.** v2.1.0 리뷰에서 `gen_svgs.py` 를 하드코딩
테이블에서 YAML 파생으로 바꾸면서 **양방향 fail-closed** 를 넣었기 때문에, 로스터가
바뀌면 생성기 쪽 테이블도 같이 고쳐야 한다. 그 필요 편집을 미리 열거한다.

**방법**: `git archive HEAD` 임시 트리에 v3 로스터(7) + budget 을 넣고 `gen_svgs.py` 를
돌린 뒤, 나온 오류를 하나씩 고쳐 다시 돌리는 것을 반복. 저장소 밖에서만 수행했고
제품 트리는 건드리지 않았다. 기준 HEAD: `376cc52`.

---

## 실행 기록 (stdout 그대로 · 경로는 임시 트리)

```
--- step 1
gen_svgs: /private/var/folders/yy/jvyvnf4x4_1b9pf7p3fq18gr0000gn/T/tmp.zY0PPm0owJ/gjc-profiles.yml has bundles with no SVG chrome: ['budget'] — add them to _PROFILE_CHROME
exit=1
--- step 2
gen_svgs: _PROFILE_CHROME lists bundles absent from /private/var/folders/yy/jvyvnf4x4_1b9pf7p3fq18gr0000gn/T/tmp.C10KdIRddT/gjc-profiles.yml: ['dream-team', 'eco', 'ultimate-sol'] — remove them
exit=1
--- step 3
gen_svgs: unknown model 'qwen3.8-max' in 'opencode-go/qwen3.8-max' — add it to _MODEL_DISPLAY
exit=1
--- step 4
wrote /private/var/folders/yy/jvyvnf4x4_1b9pf7p3fq18gr0000gn/T/tmp.3ie0lfDveE/assets/profiles-matrix.svg (16572 bytes)
wrote /private/var/folders/yy/jvyvnf4x4_1b9pf7p3fq18gr0000gn/T/tmp.3ie0lfDveE/assets/effort-ladder.svg (5321 bytes)
wrote /private/var/folders/yy/jvyvnf4x4_1b9pf7p3fq18gr0000gn/T/tmp.3ie0lfDveE/assets/architecture.svg (4554 bytes)
exit=0
```

---

## v3 원자 단계에서 `scripts/gen_svgs.py` 에 필요한 편집 — **오류가 나는 3건** (전부 아님)

| # | 편집 | 근거 오류 |
|---|---|---|
| 1 | `_PROFILE_CHROME` 에 `budget` 추가 (라벨 + tier 캡션) | `has bundles with no SVG chrome: ['budget']` |
| 2 | `_PROFILE_CHROME` 에서 `dream-team` · `eco` · `ultimate-sol` **제거** | `_PROFILE_CHROME lists bundles absent from …: ['dream-team', 'eco', 'ultimate-sol'] — remove them` |
| 3 | `_MODEL_DISPLAY` 에 `qwen3.8-max` 추가 | `unknown model 'qwen3.8-max' in 'opencode-go/qwen3.8-max'` |

셋을 다 하면 `exit=0` 으로 `profiles-matrix.svg` · `effort-ladder.svg` ·
`architecture.svg` 세 개가 생성된다.

> **🔴 2026-08-17 정정 — `exit 0` 은 "맞다" 가 아니다.**
> 이 표는 **오류를 근거로** 뽑았다. 그래서 `gen_svgs.py` 의 fail-closed 검사가 잡는
> 것만 들어 있다. 그 검사는 `_PROFILE_CHROME` 키 ↔ YAML 로스터만 대조하고
> **하드코딩된 제목·푸터 산문은 보지 않는다.** 아래는 **오류 없이 조용히 틀린 SVG**
> 를 만든다(실측):
>
> - `gen_role_winners()` — `role-winners.svg` 는 제목·카드 전체가 **`🔥 dream-team`
>   배너**다. v3 는 dream-team 을 삭제하므로 **없는 번들을 광고하는 SVG** 가 된다.
> - `profiles-matrix` 푸터 — `예외: opt-in ultimate-sol=Sol · anthropic 미포함
>   eco=Terra` 와 `🔥 dream-team = Fable 5`. 셋 다 v3 에서 삭제된 번들이다.
>   (v3 의 anthropic 미포함 번들은 `budget` 이다.)
> - `effort-ladder` chip — `GPT-5.6 3종 = 출하 ≤ xhigh` 는 **Luna 좌석 결정에 종속**이다.
>
> 즉 **이 문서의 "편집 3건" 은 생성기를 돌아가게 하는 최소 집합**이고,
> G004 항목 3 이 요구하는 "현행 좌석 반영" 집합이 아니다. 전체 목록과 미결 결정은
> `.gjc/v3-pending-docs/MAINTAINING-v3-updates.md` §6 정정 절을 정본으로 본다.

### 왜 이게 중요한가

`gen_svgs.py` 의 fail-closed 는 **양방향**이다(`gen_svgs.py` `_load_profiles`):
- YAML 에 있는데 chrome 이 없으면 → 중단
- chrome 에 있는데 YAML 에 없으면 → 중단("remove them")

즉 **로스터 축소만 하고 chrome 을 안 지워도 생성기가 멈춘다.** 편집 1 만 하고 2 를
빠뜨리는 실수가 가장 나오기 쉬운데, 그 경우 step 2 의 오류로 바로 걸린다.
이 설계는 v2.1.0 에서 좌석 교체가 SVG 에 반영되지 않아 공개 문서가 정본과 반대로
말했던 사고의 재발 방지책이므로, **완화하지 말고 테이블을 맞춰야 한다.**

### 주의

- `budget` 의 라벨·tier 캡션 문구는 이 시뮬레이션에서 임시로
  `("💳 budget", "Gate · 구독 없이 저가 API")` 를 썼다. **이 값을 베끼지 말 것.**
  실제 이모지·라벨의 정본은 `.gjc/v3-pending-docs/README-funnel-section.md` 다
  (거기서는 `💸 budget` — 드롭되는 `eco` 가 쓰던 이모지를 그대로 승계). 생성기 라벨을
  퍼널 문서와 다르게 정하면 공개 표면이 또 어긋난다.
- `qwen3.8-max` 표시명도 마찬가지로 임시값(`"Qwen3.8 Max"`)이다.
- budget 이 게이트에서 탈락하면 편집 1·3 은 불필요하고 편집 2 만 남는다.
- 이 검증은 좌석이 계획대로일 때의 결과다. v3 YAML 재구조가 좌석을 바꾸면 재실행해야 한다.

---

## 부록 — `revalidate.sh` 로스터는 반대로 자동이다

같은 v3 시뮬레이션 트리에서 `DRY_RUN=1 bash scripts/revalidate.sh` 를 돌렸다.

- **exit 0**, 회귀 없음.
- 파생된 출하 셀렉터 목록에 **`opencode-go/qwen3.8-max` 가 자동으로 들어왔다**
  (`| \`opencode-go/qwen3.8-max\` | ok | ok |`). budget 좌석을 YAML 에 넣은 것만으로
  게이트 대상에 편입된다.

즉 두 파생 표면이 서로 다르게 동작한다:

| 표면 | 로스터 변경 시 |
|---|---|
| `scripts/revalidate.sh` 셀렉터 로스터 | **자동** — YAML 에서 파생, 손댈 것 없음 |
| `scripts/gen_svgs.py` 좌석 셀 | **자동** — YAML 에서 파생 |
| `scripts/gen_svgs.py` `_PROFILE_CHROME` / `_MODEL_DISPLAY` | **수동** — 위 편집 3건 필요 |

"생성기가 파생한다" 를 뭉뚱그려 쓰면 이 차이가 사라진다. `MAINTAINING.md` §4 동기화
표면 문구에서 이 구분을 명시하도록 `.gjc/v3-pending-docs/MAINTAINING-v3-updates.md` §2 를
고쳤다(기존 초안은 "so they follow automatically" 로 뭉뚱그려 틀린 지침이었다).

---

## 부록 2 — 나머지 동기화 표면 실측 (머지된 main `ee59289` 기준)

`MAINTAINING-v3-updates.md` §2 가 나열한 동기화 표면 전부에 대해 "지금 어긋나 있나" 를
확인했다. v2.1.0 이 이미 출하됐으므로 이건 가설이 아니라 릴리스 상태 점검이다.

### `docs/factsheet.md` §2 — 드리프트 없음

번들 집합(양방향)과 5역할 좌석 셀을 `gjc-profiles.yml` 과 대조:

```
OK — factsheet §2 matches gjc-profiles.yml (10 bundles, 50 seat cells)
```

factsheet 는 **자동 가드가 전혀 없는 유일한 표면**인데도 v2.1.0 에서 안 흘렸다.
재발 방지용 검사 스크립트를 `.gjc/v3-pending-scripts/check-factsheet-parity.py` 로
**제안(계획 외)** 해뒀다 — 채택 여부는 사람이 정한다.

### `install.sh` 로스터 — 정본과 일치

`install.sh` 는 `profiles:` 블록에서 2칸 들여쓰기 키를 정규식으로 긁어 로스터를 만든다
(하드코딩 없음). 그 로직을 현재 YAML 에 그대로 적용한 결과:

```
install.sh 파생: ['daily','coding-sprint','cyber-cop','ultimate-opus','ultimate-sol','dream-team','llm-council','escalation','eco','monorepo']
YAML 정본     : ['daily','coding-sprint','cyber-cop','ultimate-opus','ultimate-sol','dream-team','llm-council','escalation','eco','monorepo']
일치: True   초과: 없음   누락: 없음
```

순서까지 동일하다. `MAINTAINING-v3-updates.md` §2 초안의
"`install.sh` derives its roster from the downloaded YAML; sanity-check its output once"
가 요구한 확인은 이것으로 끝났다.

### 표면별 가드 현황 정리

| 표면 | 가드 | v3 로스터 변경 시 |
|---|---|---|
| README 임베드 | validator 6번 체크 · `check-provider-parity.py` | 자동 검출 |
| SVG 좌석 셀 | `gen_svgs.py` YAML 파생 | 자동 |
| SVG chrome / 모델 표시명 | `gen_svgs.py` 양방향 fail-closed | **수동 편집 3건 필요** |
| revalidate 셀렉터 로스터 | YAML 파생 | 자동 |
| `install.sh` 로스터 | YAML 파생(정규식) | 자동 |
| `docs/factsheet.md` §2 | **없음** | **수동 — 제안 스크립트 채택 시 자동화 가능** |

---

## 부록 3 — i18n 미러 계약 감사 (머지된 main `ee59289`)

v3 는 퍼널 절을 **README 4종 전부**에서 교체한다(계획 F). 그 전에 현행 미러가
`MAINTAINING.md` §4 의 KO-only 계약을 지키고 있는지 확인했다.

계약 원문(§4 i18n): TOC · §5 프로필별 설계 근거 · §5 `opencode-go` TIP ·
§6-2/§6-3 심층분석 = **KO-only**, 번역본은 "요약 문단 + KO 정본 링크" 로 대체.
`validate-profiles.py` 는 YAML 임베드 parity 만 강제하고 산문 구조는 안 본다.

| 계약 항목 | KO | EN | ZH | JA | 판정 |
|---|---|---|---|---|---|
| TOC 헤딩 (KO-only) | 있음 | 없음 | 없음 | 없음 | ✅ |
| §5 `#### 프로필별 설계 근거` (KO-only) | 있음 | 없음 | 없음 | 없음 | ✅ |
| §6-2/6-3 심층분석 본문 | 전부 `docs/deep-dive-role-fit.md` 로 이관, 4종 모두 링크만 보유 | | | | ✅ |
| YAML 임베드 블록 | 있음 | 있음 | 있음 | 있음 | ✅ (validator 강제) |
| 번호 절 스켈레톤 (`1`~`11`) | 기준 | 동일 | 동일 | 동일 | ✅ |
| **`### 6-2·6-3 …(이관됨)` 스텁 헤딩** | 있음 | **있음** | 없음 | 없음 | ⚠️ **비일관** |

§5 분량도 계약과 맞는다: KO 166행 vs EN 120 · ZH 121 · JA 118 — 차이가 곧 KO-only 블록이다.

### 유일한 지적: §6-2/6-3 스텁 헤딩

EN 만 `### 6-2·6-3. Role-fit deep dive (moved)` 헤딩을 달고 있고 ZH·JA 는 같은 자리에
요약 문단만 둔다(§6 길이 EN 63행 vs ZH 61 · JA 61 — 헤딩 + 빈 줄 차이).

**계약 위반은 아니다.** 계약이 KO-only 로 지정한 것은 *심층분석 본문*이고, 그건 세 미러
어디에도 없다. 스텁은 이정표일 뿐이다. 다만 같은 계약 아래 미러 셋이 서로 다르게
렌더된다는 뜻이라, v3 에서 README 4종을 손댈 때 **어느 쪽으로 통일할지 정해야 한다.**

**심각도 낮음.** 사실 오류가 아니라 표기 비일관이다. 그리고 **EN/ZH/JA 본문 산문은 잠긴
비목표**이므로 이번에 고치지 않았다 — 기록만 남긴다.

### v3 i18n 착수 시 주의

- 계약이 "translations 에 KO-only 블록을 **되살리지 말라**" 고 명시한다
  (`do not "fix" translations by re-adding them`). 퍼널 절을 미러에 옮길 때
  KO 전용 근거 문단을 딸려 보내지 않도록 할 것.
- `routing-rules.md` 는 설계상 **한국어 전용**이다(§4). 미러링 대상이 아니다.

---

## 부록 4 — CI 워크플로 파일명 오류 (핸드오프 패키지 결함) + 스니펫 실증

### 결함: 존재하지 않는 파일을 고치라고 적혀 있었다

대기 문서의 v3 착수 절차 2번이 이렇게 적혀 있었다:

```
2. `.github/workflows/validate-profiles.yml` 에 두 스텝 추가
```

**그런 파일은 없다.** 실제 트리:

```
.github/workflows/validate.yml     ← 파일은 이것 하나뿐
```

혼동의 출처는 워크플로 내부 이름이다 — `validate.yml` 의 `name:` 이 `validate-profiles`,
잡 이름이 `static-validation` 이다. GitHub Actions UI 와 `gh pr view` 의
`workflowName: validate-profiles` 도 파일명이 아니라 이 `name:` 을 보여준다.
v3 착수자가 파일명으로 찾으면 못 찾는다. 수정 완료.

### 두루뭉술한 "두 스텝 추가" 를 실제 스니펫으로 교체하고 실증

`.gjc/v3-pending-scripts/README.md` 의 YAML 블록을 **파싱해서 그대로** 임시 트리의
`validate.yml` 뒤에 붙이고 검증했다(사람이 옮겨 적다 들여쓰기를 틀리는 걸 막으려고,
문서에 적힌 것과 실행한 것이 같은 바이트임을 보장했다).

결과:

```
steps: 6
  - actions/checkout@v4
  - actions/setup-python@v5
  - None                                            (pip install pyyaml)
  - Validate profile invariants (no credentials needed)
  - Validator fail-closed fixtures
  - README required_providers parity

validate=0   fixtures=0   parity=0
```

- YAML 이 정상 파싱되고 두 스텝이 `static-validation` 잡의 steps 로 정확히 들어간다(들여쓰기 OK).
- 세 명령 모두 실제로 exit 0.
- `pip install pyyaml` 이 이미 있어 parity 스크립트의 의존성도 충족된다 — 스텝 추가 불필요.

### 부수 확인: `routing-rules.md` §"검증된 셀렉터 하드룰"

셀렉터 정확성은 정본과 일치한다 — `eco.planner = gpt-5.6-luna:medium`(문서의
"Luna … eco.planner 채용" 과 일치) · `grok-build/grok-4.6:high` 는 not found 로 정확히 표기 ·
xai 인증은 메커니즘 단정 없이 "`/login xai` 또는 XAI_API_KEY" · 클램프는 "미측정" 유지 ·
Opus 5 476k 통과가 증거 포인터와 함께 기재.

**지적 1건(심각도 낮음)**: §82 헤딩이 `기준 gjc 0.13.3, 2026-08-16 실호출` 인데, 그 절의
규칙 일부는 08-17 근거다(xai 인증 관찰은 본문에 `08-17:` 로 명시, eco.executor 의
`glm-5.2` 전환과 grok 상한도 08-17 리뷰 산물). 출하 좌석 게이트 정본도
`evidence/2026-08-17-selectors-rerun-2.md` 다. 기술적 오류가 아니라 **출처 라벨이 좁은 것**이고,
개별 규칙에는 08-17 주석이 달려 있어 독자가 오도되지는 않는다.
**v3 에서 이 절을 손댈 때 헤딩 날짜를 함께 갱신할 것.** 지금은 제품 파일을 건드리지 않는다
(태그 전 main 에 커밋하면 0a 분기점이 흔들린다).

---

## 2026-08-18 추가 — 이 문서의 편집 목록은 **필요조건이었을 뿐 충분조건이 아니었다**

이 문서는 `gen_svgs.py` 편집 **3건**(`_PROFILE_CHROME` 에 budget 추가 · 죽은 3번들 제거 ·
`_MODEL_DISPLAY` 에 qwen3.8-max 추가)을 fail-closed 오류로부터 도출했다. **그 3건은 맞다** —
없으면 생성기가 exit 1 한다.

**다만 3건을 다 해도 결과물이 틀린다.** 2026-08-18 에 시뮬레이션 릴리스 트리를 조립해
SVG 를 재생성하니 **오류 0 · exit 0** 인데 이렇게 렌더됐다:

```
assets/profiles-matrix.svg  푸터  "…default = Anthropic 플래그십(예외: opt-in ultimate-sol=Sol
                                   · anthropic 미포함 eco=Terra)…"
                            푸터  "…🔥 dream-team = Fable 5 (Max/premium Team 주간한도 50% …)"
assets/role-winners.svg     제목  "🔥 dream-team 셋업 — 역할별 최강 가설 (Premium · experimental)"
```

fail-closed 검사가 `_PROFILE_CHROME` **키**만 로스터와 대조하고 **하드코딩 산문은 안 보기**
때문이다. 이 문서가 그 사실을 이미 경고했지만(`주의` 절), **구체적 문자열 목록은 없었다.**

→ 산문 편집 **6건**의 확정 목록은 `MAINTAINING-v3-updates.md` **§11**,
자동 가드는 `check-v3-target-state.sh --ship` 의 **`svg-prose` 축**이다.
`grep -c "🔥 dream-team" scripts/gen_svgs.py` 가 **5 → 0** 이어야 한다(실측).

### 이 문서의 "임시값" 경고가 실제로 유효했다

`budget` 라벨을 `("💳 budget", "Gate · 구독 없이 저가 API")` 로 쓰고 **"베끼지 말 것"** 이라고
적어둔 것 — 옳았다. 2026-08-18 확인: 퍼널 문서의 정본 이모지는 `💸 budget` 이고,
**tier 캡션은 아직 아무도 안 정했다**(결정 #6, `MAINTAINING-v3-updates.md` §10 의 "⏸ 3번" 절).
결정 #6 을 받을 때 **tier 배정까지 같이 물어야 한다** — 원래 질문에 빠져 있었다.

### `§82` 표기 오탐 안내

이 문서 254행의 `§82` 는 `docs/factsheet.md` 의 하위 절을 가리키는 표기이고
`MAINTAINING-v3-updates.md` 의 절 번호가 아니다(그 문서는 §31 까지). 참조 감사에서
오탐으로 확인됐다 — `MAINTAINING-v3-updates.md` §30.
