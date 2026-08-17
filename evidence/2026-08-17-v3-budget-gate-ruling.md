# budget 게이트 3조건 공식 판정 — 통과 (2026-08-17)

승인된 계획의 `budget` 게이트는 3조건이다. 조건 1·2 는 브랜치 착수 전에 충족됐고,
**조건 3(실제 v3 브랜치 YAML 에서 validator green)** 만 브랜치 대기 상태였다.
이 기록은 그 조건 3 을 **시뮬레이션이 아니라 브랜치 실물 트리에서** 실행한 원시 출력이다.

## 조건 1 — 3종 dated 프로브 그린: 충족

`evidence/2026-08-17-v3-probes.md` — `opencode-go/qwen3.8-max` ok ·
`opencode-go/glm-5.2` ok · `opencode-go/minimax-m3` ok (2026-08-17 실호출).
Qwen 프로브 실패 시 budget 미출하(계획 C-5 단일화)였으므로, 이 그린이 전제조건이었다.

## 조건 2 — 비-ocgo 좌석으로 가족 분리: 충족

- executor(`ocgo`) ↔ architect(`google`) — cross-family PASS
- planner(`ocgo`) ↔ critic(`google`) — cross-family PASS
- default(`gpt`) ↔ critic(`google`) — v3 D-2 hard ERROR 규칙에도 PASS
- `required_providers` 3벤더 — `openai-codex` · `google-antigravity` · `opencode-go`

`FAMILY[opencode-go] = "ocgo"` 로 접히는 문제는 architect/critic 을 Google 로 빼서 해소된다.

## 조건 3 — 브랜치 실물 트리 validator green: 통과

아래는 이 브랜치에서 실행한 원시 출력이다.

```
### 실행 환경
date: 2026-08-17 21:28 KST
branch: feat/v3-catalog-redesign
HEAD: ce7b30877e371c356f9a953b611044eb241c0a15
python: Python 3.9.6

### budget 좌석 (gjc-profiles.yml 실물)
required_providers: ['openai-codex', 'google-antigravity', 'opencode-go']
  default    openai-codex/gpt-5.6-terra:medium
  executor   opencode-go/glm-5.2
  planner    opencode-go/qwen3.8-max
  architect  google-antigravity/gemini-3.1-pro-low:high
  critic     google-antigravity/gemini-3.1-pro-low:high

### 로스터
['budget', 'coding-sprint', 'cyber-cop', 'daily', 'escalation', 'llm-council', 'monorepo', 'ultimate-opus']

### 조건 3 — validator (브랜치 실물 트리)
profiles checked: 8
  WARN  [coding-sprint] planner/critic same family (gpt) — intentional: human ruling 2026-07-10: Sol planner + Terra critic are distinct models; bundle stays 3-vendor mixed collaboration
  WARN  [ultimate-opus] executor/architect same family (claude) — intentional: human ruling 2026-07-10: Opus quality base; Sol planner + Grok critic carry cross-family verification (bundle stays 3-vendor)
  WARN  [monorepo] executor/architect same family (claude) — intentional: all roles >=1M ctx; gpt-5.5 (272K)/5.6 (372K) excluded — gpt-5.4 is 1M but Opus ranks at least equal
OK — all invariants hold
exit=0
```

## 판정

**3조건 전부 통과 — `budget` 은 v3.0.0 에 출하한다.**

v3 개정 3건 중 어느 것도 budget 을 뒤집지 않는다:

- **D-1**(Luna exact matcher) — `openai-codex/gpt-5.6-luna` 에만 매칭. budget 은 Luna 미사용.
- **D-2**(default↔critic 동일 family hard ERROR) — budget 은 default `gpt` ↔ critic `google` 로 분리.
- **D-3**(`NON_ANTHROPIC_DEFAULT_OK` 공집합) — budget 의 default 는 비-Anthropic 이지만
  `required_providers` 에 `anthropic` 이 없어 라우터 불변식 자체가 발동하지 않는다.
  budget 을 allowlist 에 넣을 필요가 없다 — 넣으면 불필요한 예외가 된다.

## 따라 나오는 문서 정정

판정이 나왔으므로 `budget` 을 조건부로 서술한 문구는 전부 거짓이 된다:

- `CHANGELOG.md` — `### Not shipped` 의 `⏸ budget` 항목 제거, `Validation` 에 이 판정 기록.
- `CHANGELOG.md` — 좌석을 잃은 셀렉터 "4종 … budget 탈락 시 `gpt-5.6-terra:medium`" → **3종**.
  `gpt-5.6-terra:medium` 은 `budget.default` 로 좌석을 유지한다.
- README ×4 — "게이트 통과 시에만 노출" 류 조건부 표현 제거.
  `install.sh` 는 `gjc-profiles.yml` 에서 로스터를 파생하므로 설치자 전원이 budget 을 받는다.
