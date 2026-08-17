# v3 안내 — 카탈로그 축소와 좌석 재정의

> 기준일: 2026-08-17 (v2.1.0 태그 커밋 `ee59289` 에서 v3 브랜치 분기).

## 한 줄 요약

10번들을 **7번들 + budget 게이트**로 줄이고, Core 를 **"구독 3벤더 로그인만으로 도는 것"**
으로 다시 정의하고, 선택 가이드를 **보유 구독 기준**으로 재설계했다.

## 왜 줄였나

v2 는 10개 번들을 4계층에 늘어놓았다. 문제는 개수가 아니라 **트리거 없는 번들**이었다.
세 축의 독립 조사(Parallel Ultra4x · Claude Fable 5 · Grok 4.6)가 원안을 전부 REVISE 로
기각했고, 공통 지적이 "숫자를 먼저 정하고 빈칸을 채웠다" 였다.

v3 는 개수를 목표로 두지 않는다. **사람이 설명할 수 있는 수요**가 있는 번들만 남긴다.

## 남은 것 · 사라진 것

아래 표는 **v2.1.0 에 실제로 출하돼 있던 10번들** 기준이다.

| 번들 | v3 | 사유 |
|---|---|---|
| `daily` · `coding-sprint` · `cyber-cop` | 유지 | 수요 명확 |
| `ultimate-opus` | 유지 | Anthropic 품질 기저 최고사양 |
| `escalation` | 유지 | 실패 신호 시 부르는 수동 게이트. Fable executor 의 출구 |
| `llm-council` | **유지** | routing-rules 의 Council 계약이 이 프로필을 진입점·좌석 소스로 참조한다 |
| `monorepo` | 유지 | 전역 1M ctx |
| `budget` | **게이트** | 3조건(프로브 3종 그린 · 비-ocgo 가족 분리 · validator green) 충족 전 미출하 |
| `eco` | **삭제** | 독립 트리거 소멸 — 저가 5역할은 `budget` 이 흡수. DeepSeek 지역 정책은 v2.1.0 좌석 교체 사유이지 v3 삭제 사유가 아님 <!-- 판정 완료: "glm-5.2 SKU 근거 약함" 문구는 쓰지 않는다. 2026-08-17 실측 — v2.1.0 에서 glm-5.2 는 `eco.executor` 와 **`monorepo.critic`** 두 좌석이고 `monorepo` 는 v3 에 남는다. 게다가 v3 `budget` 은 glm-5.2 를 executor 로 쓴다. 그 사유를 쓰면 살아남는 번들 둘을 동시에 부정한다 --> |
| `dream-team` | **삭제** | Fable 을 default 로 못 쓰게 되자 escalation 과 **3/5 좌석이 같아졌다**(executor·planner·critic 동일 / default·architect 상이 — 2026-08-17 실측). 남은 차이를 살리려면 새 validator waiver 가 필요해 부채만 는다 |
| `ultimate-sol` | **삭제** | Sol 3좌석 밀집. daily·ultimate-opus 가 이미 Sol planner 를 흡수 |

### 표에 없는 이름들 — 원안 후보였을 뿐 출하된 적 없다

승인 계획은 드롭 목록에 `trio` · `luna-scale` · `research-long` 도 함께 적는다. 다만
그 목록은 **v3 원안 후보 집합** 기준이라, 이 셋은 `gjc-profiles.yml` 에 들어온 적이 없다
(현행 파일에 0건, 커밋 이력에도 0건). 사용자가 쓰던 번들이 없어지는 게 아니므로
위 표에 넣지 않는다.

- `trio` — 연구 3축이 유일하게 만장일치로 지지한 후보였지만, 독립 트리거가
  기존 번들과 겹쳐 채택하지 않았다.
- `luna-scale` — 독립 트리거 없음.
- `research-long` — 5역할 고정 엔진으로는 표현할 수 없는 워크플로였다.

## 좌석 변경 — `daily.executor` 가 Luna `:max` 로

제목이 "좌석 재정의" 인데 지금까지 번들 목록만 있었다. 실제로 바뀌는 좌석은 하나다.

| 번들 | 역할 | v2.1.0 | v3 |
|---|---|---|---|
| `daily` | executor | `openai-codex/gpt-5.6-terra:high` | **`openai-codex/gpt-5.6-luna:max`** |

`daily` 는 가장 많이 쓰는 번들이므로 이 변경은 대부분의 사용자에게 체감된다.

**validator 가 Luna 를 `:max` 단독으로 강제한다.** `gpt-5.6-luna` 에 다른 effort 를
쓰면 검증이 거부한다(`illegal effort '…' for gpt-5.6-luna (legal: ['max'])`).
Sol·Terra 의 출하 상한은 `xhigh` 로 그대로다.

## 업그레이드하면 내 설정은 어떻게 되나 (2026-08-17 실측)

`install.sh` 로 설치한 상태라면 **재실행 한 번으로 끝난다.**

```
· 프로필 8종 병합 완료 → ~/.gjc/agent/models.yml
사용자 번들: budget · coding-sprint · cyber-cop · daily · escalation · llm-council · monorepo · ultimate-opus
```

관리블록(sentinel)을 통째로 교체하므로 **삭제된 3개 번들은 자동으로 사라진다** —
고아로 남지 않는다. 즉 `eco`·`dream-team`·`ultimate-sol` 을 쓰던 사람은
업그레이드 순간 그 번들을 **잃는다.**


> `models.yml` 을 **손으로 편집해** sentinel 이 지워진 경우에만 구 번들이 남는다.
> `install.sh` 가 그 상태를 실행 중에 경고한다. 남은 항목은 문서·검증 대상이 아니므로
> 직접 지우는 편이 낫다.

> **정직하게 적는다 — 이건 측정으로 이긴 좌석이 아니다.**
> `:max` 와 `:xhigh` 를 10개 태스크 × 3반복 = 60콜로 비교했고, 이 난이도에서는
> **정확도 이득이 나오지 않았다**(효과크기 0/10, Wilcoxon 단측 p=0.1587). 토큰은
> `:max` 가 평균 47.1 vs 32.2 로 더 쓴다. 좌석은 그 결과를 **알고** 내린 정책 결정이다.
> 원시 60콜과 사전등록 채점기가 `evidence/` 에 보존돼 있으니 직접 확인할 수 있다.

## Core 의 의미가 바뀐다

v2 의 Core 는 "3벤더 진입점" 이었다. v3 의 Core 는 **`anthropic`·`openai-codex`·
`google-antigravity` 구독 로그인만으로 activation 되는 것**이다. 정의가 인증 방식으로
바뀌었으므로, 어떤 프로바이더가 Core 에 들어오는지는 로그인 경로가 실제로 되는지에 달렸다.

> **"키 없이 로그인만" 이라고만 쓰면 정의가 안 된다** (2026-08-17 실측 정정).
> `xai` 도 `/login xai` 가 되므로, 그 표현이면 `escalation`·`llm-council`·`ultimate-opus`
> **셋이 함께 Core 에 들어온다.** 실측 분류:
>
> | 분류 | 번들 |
> |---|---|
> | 구독 3벤더만 (= **Core**) | `daily` · `coding-sprint` · `cyber-cop` |
> | 로그인 가능하지만 `xai` 필요 | `escalation` · `llm-council` · `ultimate-opus` |
> | **키 필수**(`opencode-go`) | `monorepo` · `budget` |
>
> 구분 기준은 "키 유무" 가 아니라 **"어느 벤더까지 필요한가"** 다. 퍼널 문서의
> `> **세 벤더 로그인만 있으면** 첫 행이 열린다` 가 정확한 표현이고, 이 절이 그걸 따른다.

## 선택 가이드가 바뀐다

tier 나열을 버렸다. **보유 구독**에서 시작해 실행 가능한 번들을 보여준다.
자세한 표는 README 의 "어떤 번들을 쓸까?" 절.

## 이 릴리스가 약속하지 않는 것

- **검증 없는 셀렉터는 문서에 없다.** 신규 좌석은 dated 실호출 기록이 있어야 오른다.
- Gemini 3.7 · `gpt-5.6-cyber` · `grok-build/grok-4.6:high` 는 실호출이 not found 라 미출하.
- Daybreak Blue 는 **승인 계정 보유자 한정 opt-in 각주**다. Core 필수 의존이 아니고,
  미보유자는 기존 구성 그대로 돌아간다(패널 좌석이 아니라 수동 교차확인 핀이다).

## 이전 안내

[v2 안내](./whats-new-v2.md) · [cyber-cop 안내](./whats-new-cyber-cop.md) — 둘 다 그 시점
기준 문서이며 본문은 그대로 보존한다.
