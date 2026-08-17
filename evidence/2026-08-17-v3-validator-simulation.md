# 2026-08-17 — v3 validator/roster 시뮬레이션 (제품 트리 무변경)

**목적**: `budget` 게이트 조건 3(validator green)과 승인 계획의 validator 개정
D-1/D-2/D-3 을 **v3 브랜치가 생기기 전에** 미리 돌려, 착수 후에 터질 결함을 앞당겨 잡는다.

**방법**: `git archive HEAD` 로 뽑은 임시 트리에 변경을 가하고 `sync-readme-yaml.py` 로
README 임베드를 맞춘 뒤 `validate-profiles.py` 실행. 저장소 밖(`mktemp -d`)에서만 수행했고
제품 트리는 건드리지 않았다. 기준 HEAD: `376cc52`.

**적용한 budget 매핑** (승인 계획 "게이트 — budget" 절 그대로):

```yaml
  budget:
    required_providers: [openai-codex, google-antigravity, opencode-go]
    model_mapping:
      default:   openai-codex/gpt-5.6-terra:medium
      executor:  opencode-go/glm-5.2
      planner:   opencode-go/qwen3.8-max
      architect: google-antigravity/gemini-3.1-pro-low:high
      critic:    google-antigravity/gemini-3.1-pro-low:high
```

**시뮬레이션한 validator 개정**
- D-1: `(p=="openai-codex" and m=="gpt-5.6-luna") -> {low,medium,high,xhigh,max}` 를 규칙 리스트 **맨 앞**에 삽입
- D-2: `fam["default"] == fam["critic"]` 이면 hard ERROR (allowlist 없음)
- D-3: `NON_ANTHROPIC_DEFAULT_OK` 의 `ultimate-sol` 엔트리 제거

---

## 실행 기록 (stdout 그대로)

```
### A. 현행 validator + budget
$ python3 scripts/validate-profiles.py
profiles checked: 11
  WARN  [coding-sprint] planner/critic same family (gpt) — intentional: human ruling 2026-07-10: Sol planner + Terra critic are distinct models; bundle stays 3-vendor mixed collaboration
  WARN  [ultimate-opus] executor/architect same family (claude) — intentional: human ruling 2026-07-10: Opus quality base; Sol planner + Grok critic carry cross-family verification (bundle stays 3-vendor)
  WARN  [ultimate-sol] non-Anthropic default (openai-codex/gpt-5.6-sol:high) — documented exception: opt-in experimental Sol-base premium: Sol leads long-horizon workflow completion (Agents' Last Exam 52.7 vs Fable 40.5, OpenAI launch table incl. competitor rows); trade-offs stay surfaced — 372K codex-surface router ctx (vs 1M) and weaker tool-calling axis (Toolathlon 58 vs Fable 61.7). Role-fit L3 pending (evidence/2026-08-16-selectors.md, two-axis synthesis A1).
  WARN  [dream-team] executor/architect same family (claude) — intentional: human ruling 2026-07-10: Fable executor vs Opus architect are distinct models; Sol planner + Grok critic carry cross-family verification
  WARN  [monorepo] executor/architect same family (claude) — intentional: all roles >=1M ctx; gpt-5.5 (272K)/5.6 (372K) excluded — gpt-5.4 is 1M but Opus ranks at least equal
OK — all invariants hold
exit=0

### B. budget 에 동일 family 강제(검사 생존 증명)
$ python3 scripts/validate-profiles.py
profiles checked: 11
  WARN  [coding-sprint] planner/critic same family (gpt) — intentional: human ruling 2026-07-10: Sol planner + Terra critic are distinct models; bundle stays 3-vendor mixed collaboration
  WARN  [ultimate-opus] executor/architect same family (claude) — intentional: human ruling 2026-07-10: Opus quality base; Sol planner + Grok critic carry cross-family verification (bundle stays 3-vendor)
  WARN  [ultimate-sol] non-Anthropic default (openai-codex/gpt-5.6-sol:high) — documented exception: opt-in experimental Sol-base premium: Sol leads long-horizon workflow completion (Agents' Last Exam 52.7 vs Fable 40.5, OpenAI launch table incl. competitor rows); trade-offs stay surfaced — 372K codex-surface router ctx (vs 1M) and weaker tool-calling axis (Toolathlon 58 vs Fable 61.7). Role-fit L3 pending (evidence/2026-08-16-selectors.md, two-axis synthesis A1).
  WARN  [dream-team] executor/architect same family (claude) — intentional: human ruling 2026-07-10: Fable executor vs Opus architect are distinct models; Sol planner + Grok critic carry cross-family verification
  WARN  [monorepo] executor/architect same family (claude) — intentional: all roles >=1M ctx; gpt-5.5 (272K)/5.6 (372K) excluded — gpt-5.4 is 1M but Opus ranks at least equal

FAIL (1 error(s)):
  ERROR [budget] planner/critic share family (ocgo) — breaks plan-critique independence
exit=1

### C. v3 로스터 + budget + D-1/D-2/D-3 시뮬레이션
$ python3 scripts/validate-profiles.py
profiles checked: 8
  WARN  [coding-sprint] planner/critic same family (gpt) — intentional: human ruling 2026-07-10: Sol planner + Terra critic are distinct models; bundle stays 3-vendor mixed collaboration
  WARN  [ultimate-opus] executor/architect same family (claude) — intentional: human ruling 2026-07-10: Opus quality base; Sol planner + Grok critic carry cross-family verification (bundle stays 3-vendor)
  WARN  [monorepo] executor/architect same family (claude) — intentional: all roles >=1M ctx; gpt-5.5 (272K)/5.6 (372K) excluded — gpt-5.4 is 1M but Opus ranks at least equal
OK — all invariants hold
exit=0

### D. D-1/D-2/D-3 만 적용하고 로스터는 그대로 (순서 위반 시뮬레이션)
$ python3 scripts/validate-profiles.py     # WARN 행은 A 와 동일하여 생략
profiles checked: 11

FAIL (1 error(s)):
  ERROR [ultimate-sol] default must be Anthropic when anthropic is available (got openai-codex/gpt-5.6-sol:high)
exit=1
```

---

## 판정

| 케이스 | 결과 | 의미 |
|---|---|---|
| A. 현행 validator + budget | exit 0, `[budget]` ERROR·WARN 0건 | **조건 3 예비 통과** |
| B. budget planner/critic 를 동일 family 로 강제 | exit 1, `ERROR [budget] planner/critic share family (ocgo)` | A 의 통과가 **검사 생존 상태에서 나온 것**임을 증명 |
| C. v3 로스터 7 + budget + D-1/D-2/D-3 | exit 0, `profiles checked: 8`, 의도된 WARN 3 | **v3 목표 상태가 통과한다** |
| D. D-1/D-2/D-3 만 적용, 로스터 유지 | exit 1, `ERROR [ultimate-sol] …` | **순서 제약**: 개정을 로스터 축소보다 먼저 넣으면 깨진다 |

### 결론

1. **budget 은 validator 를 넘는다.** effort 규칙 공백 없음 — `gemini … pro` 규칙
   `{low,high}` 가 `:high` 를 덮고, `glm-5.2`·`qwen3.8-max` 는 effort 무핀이라 규칙 대상이 아니다.
2. **개정 3종 중 budget 을 뒤집을 수 있는 것은 없다.** D-1 은 Luna 전용,
   D-2 는 budget 이 `gpt`↔`google` 로 이미 분리, D-3 은 budget 의 `required_providers` 에
   `anthropic` 이 없어 라우터 불변식이 애초에 발동하지 않는다.
   → **budget 을 `NON_ANTHROPIC_DEFAULT_OK` 에 등재하지 말 것.**
3. **케이스 D 가 계획의 "원자 단계" 요구에 실측 근거를 준다.** D-3 은 `ultimate-sol` 이
   드롭되기 때문에 안전한 것이지, 그 자체로 안전한 게 아니다. 개정과 로스터 축소를
   쪼개면 중간 커밋이 빨간불이 된다.
4. WARN 이 5 → 3 으로 줄어드는 것은 `dream-team`·`ultimate-sol` 드롭의 결과다.
   따라서 **`SAME_FAMILY_OK[("dream-team","exec_arch")]` 는 죽은 엔트리가 된다** —
   계획 D-3 이 지목하지 않은 항목이므로 v3 원자 단계에서 같이 지운다
   (`.gjc/v3-pending-docs/MAINTAINING-v3-updates.md` §5).

### 한계

- 이것은 **공식 조건 3 판정이 아니다.** 공식 판정은 v3 브랜치의 실제 YAML 에서 나온다.
- 시뮬레이션한 D-1/D-2/D-3 은 계획 문구를 옮긴 것이지 실제 구현체가 아니다.
  실제 구현이 다르게 작성되면 결과가 달라질 수 있다.
- 로스터 축소는 텍스트 단위로 프로필 블록을 제거해 흉내낸 것이라, v3 YAML 재구조가
  좌석까지 바꾸면 이 결과는 재실행이 필요하다.

---

## 2026-08-18 추가 — 결정 #1 이후 재실증 · fixture 4종 → 5종

이 문서의 시뮬레이션은 **결정 #1(Luna `:max`) 전**에 수행됐다. 그 뒤 D-1 의 합법 effort 가
`{low,medium,high,xhigh,max}` → **`{max}` 단독**으로 좁아졌으므로, 완전한 v3 릴리스 트리에서
다시 확인했다(`build-release-sim.sh` 1회 실행):

```
ok [invariants] OK — all invariants hold          (D-1/D-2/D-3 적용된 validator)
ok [fixtures]   v3 fixture 5종 전부 통과
  luna-xhigh-fail  · luna-medium-fail  · sol-max-fail  · terra-max-fail  · default-critic-fail
```

**`luna-max-pass` 는 없다** — 출하 트리가 `luna:max` 를 직접 들고 있으므로 accept 케이스는
`[canonical] real tree exits 0` 이 담당한다. 그 자리를 **좁아진 규칙을 행동으로 증명하는**
두 reject 케이스가 대신한다. `luna:medium` 은 **v2.1.0 에서 합법이었다** — 그래서
`luna-medium-fail` 이 "규칙이 실제로 좁아졌다" 의 증거가 된다.

### 순서 의존이 하나 더 있다 (2026-08-18 실측)

이 문서는 "D-3 를 로스터 축소보다 먼저 넣으면 FAIL" 을 정확히 기록했다. **두 번째 순서 제약**이
그 뒤에 발견됐다: `ci-fixture-check.sh` 를 `sync-readme-yaml.py` **앞**으로 당기면

```
FAIL [canonical] real tree should pass but exited 1
FAILED — validator fail-closed behaviour regressed        ← 거짓 단서
```

validator 는 멀쩡하다 — `[canonical]` 이 돌리는 `validate-profiles.py` 에 **README 임베드 YAML
패리티**가 들어 있어서, 로스터 변경 직후 README 4종이 낡아 터진 것이다(4 error, en·ja·md·zh).
`sync-readme-yaml.py` 를 돌리면 즉시 복구된다.

**"fail-closed behaviour regressed" 를 문자 그대로 믿고 D-1/D-2 를 뜯으면 시간을 태운다.**
상세는 `.gjc/v3-pending-scripts/README.md` 의 "순서 의존이 하나 더 있다" 절.
