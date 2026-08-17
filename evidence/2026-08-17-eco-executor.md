# 2026-08-17 — eco.executor 좌석 교체 실호출 증거

컨텍스트: v2.1.0 PR #25 리뷰에서 `gjc-cop` critic 이 REQUEST_CHANGES 를 냈다.
지적 요지 — 출하 좌석 `eco.executor = opencode-go/deepseek-v4-flash` 가 이 계정에서
403 을 반환하는데, `scripts/revalidate.sh` 가 그 셀렉터를 필수 `ok` 그리드에서
정보성 `ok-live` 로 내려 **깨진 출하 좌석이 게이트를 통과**하게 만들었다는 것.

이 파일은 append-only 다. 기존 `evidence/2026-08-16-selectors.md` 는 수정하지 않았다.

## 프로브

명령 형태: `gjc -p --no-session --no-tools --model <selector> "Reply with exactly: OK"`

| selector | 결과 | 비고 |
|---|---|---|
| `opencode-go/glm-5.2` | **ok** | 2026-08-17 재확인. 08-16 기록(8.9s)과 일치 |
| `opencode-go/deepseek-v4-flash` | **fail [403 China opt-in]** | 08-16 기록과 동일. 카탈로그 id 는 생존 — 계정/지역 엔타이틀먼트 문제이지 delist 아님 |

## 조치

1. `gjc-profiles.yml` — `eco.executor` 를 `opencode-go/deepseek-v4-flash` → **`opencode-go/glm-5.2`** 로 교체.
   yml 주석이 이미 "지역 차단이면 GLM/Luna 로 수동 스왑"을 예고하고 있었다.
   `glm-5.2` 는 이미 필수 `ok` 그리드에 있으므로 게이트를 낮출 필요가 없다.
2. `scripts/revalidate.sh` — deepseek 를 정보성 카나리로 **명시 분류**. 왜 출하 좌석이
   아닌지, 어떤 조건에서 재평가하는지를 주석에 적었다. 조용한 강등이 아니다.
3. `README.md` — "deepseek-v4-flash/pro·glm-5.2는 검증됐고" 라는 **거짓 주장**을 정정.
   deepseek 는 이 계정에서 403 이고 출하 좌석이 아니라고 명시.

## family 영향

교체 후 `eco` 좌석: default `gpt-5.6-terra:medium`(gpt) · executor `glm-5.2`(ocgo) ·
planner `gpt-5.6-luna:medium`(gpt) · architect `gemini-3.1-pro-low:high`(google) ·
critic `gemini-3-flash:low`(google).

- executor ↔ architect = ocgo ↔ google → cross-family, PASS
- planner ↔ critic = gpt ↔ google → cross-family, PASS
- `required_providers` = openai-codex · opencode-go · google-antigravity → 3벤더 불변

교체 전(deepseek 도 ocgo)과 family 배치가 동일하므로 불변식 영향 없음.

## 범위 메모

v2.1.0 은 like-for-like MINOR 다. 이 좌석 교체는 원래 계획한 Opus/Grok 승격 쌍에
더해지는 **세 번째 변경**이며, 리뷰가 발견한 결함을 고치기 위한 것이다.
카탈로그 구조 재설계(번들 축소·validator 개정)는 v3 MAJOR 로 분리한 상태 그대로다.

v3 는 `eco` 번들 자체를 DROP 하기로 이미 확정돼 있다(죽은 executor 가 DROP 근거였다).
이 교체는 v2.1.0 이 머지되기까지의 기간 동안 출하 좌석이 거짓말하지 않게 하는 조치다.

---

## 부록 — kimi 계열 실호출 (2026-08-17)

사용자가 "kimi k3 도 좋다더라"는 전언을 전해 확인했다. 전언은 근거가 아니므로 실호출로 확인했다.

| selector | 결과 | 카탈로그 |
|---|---|---|
| `opencode-go/kimi-k3` | **ok** (7s) | 1M ctx · 131K out · minimal,low,medium,high,xhigh · images yes |
| `opencode-go/kimi-k2.7-code` | **ok** (8s) | 262K ctx · 262K out · minimal,low,medium,high,xhigh |

### 현 출하 좌석과의 대비

`monorepo.critic = opencode-go/glm-5.2` 와 비교:

| | ctx | max-out | efforts | images |
|---|---|---|---|---|
| `glm-5.2` (현 출하) | 1M | 131K | minimal..xhigh | no |
| `kimi-k3` | 1M | 131K | minimal..xhigh | yes |

컨텍스트·출력·effort 사다리가 동일하다. images 지원만 다르고 critic 좌석에는 무관하다.
**동급 후보이지 업그레이드 근거가 아니다.**

### 판정: 이번 릴리스에서 좌석 채택하지 않음

- 실호출은 통과했으나 **role-fit 증거가 없다.** 카탈로그 존재와 핑 성공은 좌석 자격이 아니다
  (`MAINTAINING.md` 의 프로필/모델 변경 규율, 그리고 v3 조사 3축이 공통으로 세운 기준).
- v2.1.0 은 like-for-like MINOR 다. 이미 리뷰 블로커(403 좌석) 때문에 계획에 없던 교체를
  하나 넣었다. 근거 없는 두 번째 좌석 교체를 얹으면 릴리스 성격이 무너진다.
- v3 budget 번들의 좌석 매핑은 리뷰에서 **단일 확정·대체 경로 없음**으로 못 박혔다
  (ARCH-V3-P2-002 / CV3P2-F02 가 MiniMax fallback 을 제거한 이유가 바로 이것).
  여기에 kimi 를 새 대체 후보로 끼우면 그 결정을 되돌리는 것이 된다.

### 재평가 트리거로 등재

`opencode-go/kimi-k3` — 1M ctx 오픈웨이트 후보. 아래가 갖춰지면 `monorepo.critic` 또는
v3 `budget` 좌석 후보로 재평가한다.

1. 동일 코퍼스에서 `glm-5.2` 와의 blind 대조 채점 (critic 역할 적합성)
2. 리워드 해킹 관련 자기공시 유무 확인 (현 `glm-5.2` 는 Z.ai 자기공시 이력이 이미 재평가 트리거로 등재돼 있다)
3. 가격·레이트리밋 공식 문서 확인

`opencode-go/kimi-k2.7-code` — 262K ctx 로 `monorepo` 의 전역 1M 요구를 못 채운다. 해당 좌석 후보 아님.

---

## 부록 2 — eco.executor role-fit 비교 프로브 (2026-08-17)

`gjc-cop` critic 이 정당하게 지적했다: kimi 를 "실호출 ≠ role-fit" 으로 거절해 놓고
`glm-5.2` 를 같은 수준의 증거(핑 + family 분석)로 executor 에 앉힌 것은 이중잣대다.
게다가 `README.md` §6 지연표는 `glm-5.2` 를 **"코딩 21.9s · 코딩 최저속 — critic 엔 무방"**
이라고 적고 있었다 — 레포 자신의 측정이 코딩 좌석에 부적합하다고 말하는 모델을
코딩 담당 좌석에 앉힌 셈이다.

그래서 실제 코딩 태스크로 비교했다.

### 프로토콜

- 태스크: `merge_intervals(intervals)` 구현 (겹치는 닫힌 구간 병합). 정렬 안 됨·빈 입력·
  중복·완전 포함 케이스 포함. 출력은 단일 ```python 블록만 요구.
- 호출: `gjc -p --no-session --no-tools --model <selector> "<task>"`
- 채점: 사전 고정한 8개 케이스(빈 입력, 단일, 표준 병합, 경계 접촉 `[1,4]+[4,5]`,
  완전 포함, 역순 입력, 중복, 중복+포함)를 실행해 정확 일치 수를 셈. 채점 코드는
  모델별로 동일하고 사후 조정하지 않았다.
- 후보는 eco 의 `required_providers`(openai-codex · opencode-go · google-antigravity)
  안에서 고르되, `executor ↔ architect` 계열 독립 제약상 architect 가 google 이므로
  executor 는 gpt 또는 ocgo 로 한정된다.

### 결과

| selector | 지연 | 정확도 | 비고 |
|---|---|---|---|
| `openai-codex/gpt-5.6-terra:medium` | 3.5s | **8/8** | 이미 eco.default — 같은 좌석 중복 |
| `openai-codex/gpt-5.6-luna:high` | 4.9s | **8/8** | 이미 eco.planner — 같은 좌석 중복 |
| `opencode-go/glm-5.2` | 5.1s | **8/8** | 채택 |
| `opencode-go/kimi-k3` | 6.0s | **8/8** | 미채택(아래) |

### 판정

- **네 후보 모두 이 태스크에서 정확했고 지연은 3.5~6.0s 안에 모였다.**
- `glm-5.2` 의 07-02 마이크로벤치 **21.9s 는 이 태스크에서 재현되지 않았다**(5.1s).
  07-02 수치는 다른/더 무거운 태스크 기준이므로 직접 비교 대상이 아니다. 다만
  "코딩 최저속이라 critic 전용" 이라는 기존 서술은 executor 배치를 막는 근거로
  쓰기에 충분하지 않다 — README §6 표기를 08-17 측정과 함께 갱신했다.
- **`glm-5.2` 채택 근거**: (a) 이 프로브에서 정확·지연 모두 후보군과 동급,
  (b) terra/luna 는 같은 번들의 default/planner 라 좌석 중복이 생김,
  (c) 이미 레포의 확립된 좌석(`monorepo.critic`)이고 필수 `ok` 검증 그리드에 있음,
  (d) 가격이 문서화돼 있음($1.40/$4.40 MIT).
- **`kimi-k3` 미채택 근거 정정**: 이제 `glm-5.2` 와 **동일한 수준의 증거**를 갖는다.
  따라서 "role-fit 증거 없음" 은 더 이상 kimi 만의 결격 사유가 아니다. 미채택 사유는
  (a) 채울 좌석이 없고, (b) 레포에 가격·레이트리밋 문서가 없으며, (c) 필수 검증
  그리드에 없다는 운영상의 이유다. 재평가 트리거로 계속 등재한다.

### 이 프로브가 증명하지 않는 것

단발 알고리즘 태스크 1건이다. 지속적 agentic 코딩, 도구 호출, 다중 파일 편집,
장문 컨텍스트 거동은 측정하지 않았다. eco 는 Specialized(exp) 저단가 실험 번들이며
이 좌석은 그 수준의 증거로 배치된 것이다 — 프리미엄 좌석 승격 근거로 쓰지 말 것.
