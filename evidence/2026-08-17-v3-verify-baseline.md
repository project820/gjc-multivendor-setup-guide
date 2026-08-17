# v3 대기 패키지 검증 기준선 — 2026-08-18

`verify-all.sh` 전체 출력과 트리 지문을 **그 시점 그대로** 남긴다.
다음 세션은 같은 명령을 돌려 이 파일과 대조하면 **내 통제 밖의 드리프트**를 즉시 안다
(사용자 편집 · `git pull` · 태그 생성 · 다른 세션의 작업 등).

기준선이 초록인지 아는 것은 음성 경로 판정의 전제다 — 초록 아닌 상태에서
"FAIL 이 떴다" 는 아무 정보가 아니다(`check-gates-negative.sh` 가 그래서 중단한다).

## 트리 지문

```
HEAD                     ee59289e14bcc0a5a09ca8687f0725b338399c1c
HEAD(short)              ee59289
v2.1.0 태그              v2.1.0
없음 (exit 128) — 유일한 블로커
origin/feat/v3-...       없음
git status --porcelain    3줄 (알려진 junk 3개)
git diff                 clean
gjc                      gjc/0.13.3
python3 (로컬)            3.9.6 · CI 핀 3.12

대기 패키지
  scripts   15개
  docs      10개
  evidence  7개 (이 파일 포함 전)
  MAINTAINING-v3-updates.md  37개 절

정본 ultragoal 원장 (네 곳 중 이것만 정본)
  경로  .gjc/_session-<redacted>/ultragoal/
  goals.json sha256  c9a36e9be2c28391f99972f1883d2cb23b090e6097ade9797274ad238a47f977
  ledger.jsonl 줄수   52
  goal 상태          G001=complete G002=complete G003=blocked G004=blocked G005=blocked G006=complete
```

## 주요 스크립트 sha256 (앞 16자)

```
verify-all.sh              46bc80d62334b319
build-release-sim.sh       b1056a2523617b32
check-gates-negative.sh    a303259ae26cd007
check-v3-target-state.sh   dee09cbbcd7a1cda
check-anchor-drift.py      a0b44010710cd395
slug-anchor-check.py       45b15ecb73119fad
check-sim-doc-parity.py    09d7bd1dbf9e4e3f
```

## `verify-all.sh` 전체 출력

```
== 1. 현행 트리 상태 (치환 전에만 유효한 것 포함) ==
  ✅ sim ↔ 문서 문자열 대조    OK — 시뮬이 쓰는 문자열 11종이 문서 표에도 있다
  ✅ 런북 앵커 30종                OK — 앵커 30종 전부 유일 매칭 · 배너 미삽입 2종 확인 · 삽입 지점 형태 2종 유지
  ✅ 링크 무결성 (README 4종)     OK — 검사한 모든 링크가 실재 헤딩을 가리킨다 (README 4종)
  ✅ provider 패리티                 OK — required_providers match across 4 README file(s), 10 profiles
  ✅ factsheet §2 패리티            OK — factsheet §2 matches gjc-profiles.yml (10 bundles, 50 seat cells)
  ✅ validator 불변식                OK — all invariants hold
  ✅ fixture 배터리                  OK — every fixture behaved as expected
  ✅ roster 적용 드라이런         OK — 적용 가능(파일 미변경).
  ✅ validator 적용 드라이런      OK — D-1/D-2/D-3 앵커 모두 유일 매칭. 적용 가능(파일 미변경).

== 2. 조립된 v3 릴리스 후보 ==
  ✅ 릴리스 후보 조립 + 25축    OK — v3 게이트 통과 (출하 게이트 포함)
  ✅ 링크 무결성 (릴리스 후보 전수) OK — 검사한 모든 링크가 실재 헤딩을 가리킨다 (전수 .md)

== 3. 게이트가 실제로 잡는가 (음성 경로 16종) ==
  ✅ 음성 경로 일괄               OK — 음성 경로 16 종 전부 기대대로 동작

== 4. 사람 액션 ==
  ⏸ v2.1.0 태그 없음 — 이것이 유일한 블로커다
       git tag -a v2.1.0 ee59289 -m "v2.1.0 — Opus 5 · Grok 4.6 like-for-like 승격"
       git push origin v2.1.0
  ⏸ 결정 #2~#10 — .gjc/V3-HANDOFF.md 의 결정표

OK — 검증 12 종 전부 통과 (사람 액션은 별개)
```

## 판정

**검증 12종 전부 통과 · 음성 경로 16종 전부 기대대로 · 릴리스 후보 25축 초록.**
사람 액션 2건(`v2.1.0` 태그 · 결정 #2~#10)은 exit code 에 들어가지 않는다 —
검증 통과와 출하 가능은 다른 얘기다.

---

## Errata — 2026-08-17

이 기록의 원래 파일명과 본문 머리의 날짜는 `2026-08-18` 이었다. 시스템 시계 확인 결과
실제 작성일은 **2026-08-17** 이다(KST). 미래 날짜가 박힌 증거 파일명을 그대로
출하하지 않기 위해 파일명을 `2026-08-17-v3-verify-baseline.md` 로 정정했다.
위 본문은 손대지 않았다 — 원문의 `2026-08-18` 표기는 그 시점의 오기로 읽어라.

## Errata 2 — 2026-08-17 (이 기준선의 범위)

이 기록은 **`main`(v2.1.0, 10번들·50 좌석셀) 트리의 기준선**이다.
`feat/v3-catalog-redesign` 브랜치의 검증 출력이 아니다 — PR 본문이 이걸 이 PR 의
검증 결과로 인용했다면 오독이다. 브랜치 검증은 각 커밋의 게이트 실행 출력과
`evidence/2026-08-17-v3-budget-gate-ruling.md` 를 봐라.

또한 30행의 머신 로컬 세션 UUID 는 **`<redacted>` 로 지웠다.** append-only 는 측정값을
보호하는 원칙이고, 이 레포 밖에서 아무 의미도 없는 로컬 식별자를 공개 저장소에 남길
근거는 아니다(cyber-cop 패널 지적). 지운 것은 UUID 문자열뿐이고 그 줄의 나머지·다른
모든 측정값은 그대로다. 줄바꿈이 깨진 지문 블록도 원문 그대로 뒀다 — 판독은 어렵지만
측정 기록이다.
