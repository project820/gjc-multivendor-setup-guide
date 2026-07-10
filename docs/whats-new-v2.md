# What's new — v2.0.0: 13 프로필 → 10 번들 · 4계층 (2026-07-10)

> [!NOTE]
> **이 문서는 non-normative 설명 공지다.** 규범 출처: 매핑 = [`gjc-profiles.yml`](../gjc-profiles.yml) · 운영 계약 = [`routing-rules.md`](../routing-rules.md) · 카탈로그 요약 = [README §5](../README.md#5-%EF%B8%8F-최종-카탈로그--10-번들--4계층) · 상세 이력 = [CHANGELOG v2.0.0](../CHANGELOG.md). 이 문서와 규범 문서가 다르면 규범 문서가 옳다.

---

## 1. 한 줄 요약

**"동등한 프로필 13개"를 폐기하고, 신뢰 등급이 다른 4계층(tier) 위에 10개 user-facing 번들을 재배치했다.** 프로필 YAML이 할 수 있는 것(좌석 매핑)과 할 수 없는 것(council 투표·자동 escalation)의 경계를 문서 전면에 드러낸 것이 이번 개편의 본질이다.

## 2. 왜 바꿨나

1. **2축 블라인드 독립 딥리서치**(Claude Fable 5 Ultracode + Parallel.ai Ultra 2x, 2026-07-10)가 공통으로 **REVISE** 판정 — 모델 세대·역할 축 배치는 지지하되, "N개 동등 프로필" 서사·profile/workflow 경계 혼동·strict provider 마찰을 수정하라고 결론.
2. **GJC 0.9.6이 같은 날 출시** — GPT-5.6 usable prompt budget 272K→**373K**, antigravity 퍼지 해석 **fail-closed** 전환, 내장 프로필의 GPT-5.6 세대교체. v1 카탈로그의 단일·2벤더 프로필 수요를 내장이 흡수하게 됨.
3. **당일 라이브 드리프트 실측** — 0.9.6 첫 실호출 배터리가 `gemini-3.5-flash-low` 소멸을 적발(v1.11.0 `eco`를 이미 깨뜨린 상태). "검증 안 된 셀렉터 출하 금지" 원칙이 실전에서 작동했다.

## 3. 무엇이 바뀌었나

| Tier | 번들 | 비고 |
|---|---|---|
| **Core** | `daily` ⭐ · `coding-sprint` · `cyber-cop` | 구독 OAuth 3벤더(anthropic·openai-codex·google-antigravity)만으로 activation |
| **Premium (experimental)** | `ultimate-opus` · `ultimate-sol` · `dream-team` | 최고품질 *가설* — role-fit L3 실측 전 "최강" 단정 금지. xai API 키 필요 |
| **Workflow bundle** | `llm-council` · `escalation` | 좌석표 + [routing-rules](../routing-rules.md)의 Council/Escalation 계약이 있어야 동작 |
| **Specialized (experimental)** | `eco` · `monorepo` | 저단가 실험(절대 최저가 아님) / 전역 1M ctx |

**이름 승계·삭제**
- `ultimate` → `ultimate-opus` (executor `:max`→`:high`, architect gemini→opus)
- `ultimate-f5` / `legend` → `dream-team` (Fable default+executor)
- 신설: `ultimate-sol`(유일한 Anthropic-보유 비-Anthropic 라우터 — validator 예외 등재) · `llm-council`
- **삭제**: `solo-anthropic` · `solo-openai` · `claude-codex` · `claude-codex-max` — 단일·2벤더 수요는 GJC 0.9.6 내장(`claude-opus`/`codex-*`/`opus-codex`/`fable-opus-codex`)이 흡수. 구판 좌석이 필요하면 `git show v1.11.0:gjc-profiles.yml`.

**핵심 좌석 변경**
- `daily`: planner gemini→**Sol** · critic grok→**Gemini**(xai 키 장벽 제거 + 본체와 cross-family 유지)
- `eco`: 전면 재편 — planner는 retire된 `grok-4-1-fast`에서 **Luna**로, critic은 소멸한 `gemini-3.5-flash-low`에서 **`gemini-3-flash:low`**로, anthropic·xai 제거(3벤더)
- `escalation` · `cyber-cop` · `monorepo`: v1.11.0 매핑 그대로 KEEP

## 4. 정직성 재표기 (이번 개편의 진짜 알맹이)

- **llm-council은 "4계열 합의"가 아니다** — 판정석은 Google·xAI·OpenAI 3계열이고, 본체 Anthropic은 자기선호 격리를 위해 **집계자 제한**("3계열 판정 + 제4계열 집계").
- **escalation은 수동이다** — 실패 자동 감지 없음. 트리거·재시도 예산·human gate는 routing-rules 계약.
- **Grok critic은 "결함회수 최강"이 아니라 제3계열 독립 dissent** — critic-specific 근거 0건(2축 리서치 합의).
- **1M nominal window ≠ 완전 recall** — 단일 메시지 `@file` 한도는 ~400k(실측 350k ✅ / 476k 🔴).
- 모든 same-family 예외는 validator `SAME_FAMILY_OK`/`NON_ANTHROPIC_DEFAULT_OK` 등재 + **WARN 영구 표면화** — 침묵하는 예외는 없다.

## 5. 검증 방법론

- **freeze 전**: 2축 블라인드 리서치 → citation audit → 인간 configuration freeze(2026-07-10).
- **freeze 후**: gjc 0.9.6 재기준화(바이너리 sha256 = 공식 자산 digest) → 카탈로그 재채취 → 실호출 배터리(`evidence/2026-07-10-selectors-rerun-3.md` — v2 출하 셀렉터 전 좌석 그린).
- **출하 게이트**: cyber-cop **5라운드**(3표 cross-family 패널) — BLOCK×4 → clear. 패널이 freeze 승인안의 자기 계약 위반(daily.critic=본체 동일벤더)까지 잡아 수리시켰다. 라운드별 대응표는 [PR #21 코멘트](https://github.com/project820/gjc-multivendor-setup-guide/pull/21) 참조. 머지는 사람이 결정했다.

## 6. 마이그레이션 3줄

```bash
curl -fsSL https://raw.githubusercontent.com/project820/gjc-multivendor-setup-guide/main/install.sh | bash
# 동일 이름 번들은 v2 매핑으로 교체된다. 삭제된 v1 프로필(solo-* 등)이 로컬에 남아 있으면
# 수동 삭제하거나 GJC 내장 프로필로 갈아탄다 — 구판 좌석 참조: git show v1.11.0:gjc-profiles.yml
```

## 7. 미출하 (다음 과제)

Premium 3종 role-fit L3 · gpt-5.6 `:max` 심도 계측 · Fable refusal 정량화 · Council/Escalation E2E · 번들별 비용 실측 · gen_svgs↔YAML 파리티 가드. 상세: [CHANGELOG v2.0.0 "Not shipped"](../CHANGELOG.md).
