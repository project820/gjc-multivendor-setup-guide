# Maintaining this guide — research & validation playbook

This repo is meant to stay correct as model catalogs, prices, and provider behavior drift.
Anything in here can be picked up by a fresh session (human or a `gjc` agent) **without prior context** — clone the repo and follow this file.

> One-line orientation: the profiles assign GJC's five roles (`default` / `executor` / `architect` / `planner` / `critic`) to the best model per role across vendors. `default` stays on the strongest router (an Anthropic flagship — Opus 4.8 or Fable 5 — when available); `critic` stays cross-family. Everything is **user config** (`~/.gjc/agent/models.yml`), not bundled defaults.

---

## 1. Durable invariants (never silently break these)

1. **`default` = strongest router.** If `anthropic` is in `required_providers`, `default` must be an **Anthropic flagship (Opus 4.8 / Fable 5)**. A weak router caps whole-system quality. (The CI invariant only checks Anthropic-family, so both flagships pass.)
2. **`critic` is cross-family** from the `executor`/`planner` it reviews — except where impossible (single-vendor `solo-*`, 2-vendor `claude-codex*`) or ctx-forced (`monorepo`). Documented exceptions live in `scripts/validate-profiles.py` (`SAME_FAMILY_OK`).
3. **Effort hard-rules** (⚠ these are **GJC-effective** ceilings as of 0.7.10, NOT the API's own tiers — the Claude API accepts `max` on both Fable 5 and Sonnet 5; the GJC parser gap is reported upstream): Opus 4.6+ `minimal..max`; **Fable 5 `≤xhigh`** (`:max` silently clamps to xhigh; thinking always-on); **Sonnet 4.6/5 `≤high`** (`:xhigh`/`:max` silently clamp); GPT 5.2+/codex `low..xhigh`; **Gemini Pro `low`/`high` only**; Gemini Flash `minimal..high`; **xai Grok 4.3 `≤high`** (`xhigh` exists only on the `grok-build` provider, whose effort suffixes don't resolve — bare selector only); opencode-go: omit `:effort`.
4. **Antigravity high reasoning = `gemini-3.1-pro-low:high`** (the `gemini-3.1-pro-high` id 400s — backend has no such model; `thinkingLevel` is a per-request param).
5. **`-codex` variants don't work on a ChatGPT/Codex account** — use base `gpt-5.5` / `gpt-5.4`.
6. **Single-message `@file` input limit (~400k) ≠ context window (1M).** Chunk huge inputs across turns.
7. **Bundled vs live catalog**: `opencode-go` and `google-antigravity` discover additional models from the provider API after `/login`. As of gjc 0.7.10, `glm-5.2` is in the **bundled** catalog (the old "live-only" caveat is retired); `gemini-3.5-flash` has no literal bundled id (only `-low`/`-extra-low`) — pin `google-antigravity/gemini-3.5-flash-low` instead of relying on fuzzy resolution.

Every claim in `README.md` is **time-sensitive (catalog at validation date)** — keep the dated caveat.

---

## 2. Tooling

| Script | Needs creds? | What it does |
| --- | --- | --- |
| `scripts/validate-profiles.py` | no | Static guard: YAML valid, 5 roles, router invariant, cross-family (with allowlist), effort legality, `required_providers` coverage, README-embed == `gjc-profiles.yml`. **Runs in CI.** |
| `scripts/revalidate.sh` | yes (`/login`) | Live battery: every profile selector via real `gjc -p`; records `evidence/<date>-selectors.md`; non-zero exit on regression. `SELECTORS_ONLY=1` skips long-context probes. |
| `scripts/catalog-snapshot.sh` | yes | Dumps the live catalog to `evidence/<date>-catalog.txt`; `--diff` compares the two newest snapshots (new/retired models, ctx/effort drift — snapshots carry no price data; verify prices against official pages). |
| `scripts/cyber-cop-review.sh` | yes (`/login` + `gh`) | Headless cyber-cop reviewer-mode PR review; prints 4-section verdict; never merges. |

```bash
python3 scripts/validate-profiles.py          # before every commit / in CI
bash scripts/revalidate.sh                     # on an authed machine (quarterly / on catalog news)
bash scripts/catalog-snapshot.sh               # snapshot; later: scripts/catalog-snapshot.sh --diff
```

`evidence/` is the durable audit trail — committed, dated, never rewritten. It backs the README's "verified" claims.
It also holds the dated deep-research / consultant / model-council reports that justify the role→model assignments (`evidence/<date>-deep-research-benchmarks.md`, `-consultant-report.md`, `-ultimate-final-report.md`), cross-linked from README §6-2. Re-validation ships as a *new* dated report — never edit a published one.

---

## 3. Maintenance cadence

- **Quarterly, or on any model launch/retirement/price change:**
  1. `bash scripts/catalog-snapshot.sh` then `--diff` vs the last snapshot → spot drift.
  2. `bash scripts/revalidate.sh` → regenerate the selector evidence; fix any regression.
  3. If a better model appears for a role (benchmark + live-verified), update `gjc-profiles.yml` **and** the README embedded YAML + cheatsheet, re-run `validate-profiles.py`, and add a CHANGELOG entry.
- **Benchmark sourcing**: rank by role axis — executor=SWE-bench Verified (vals.ai), planner=GPQA/ARC-AGI, architect=ctx+MMMU, default=tool-calling/honesty, critic=independence. Cite vals.ai / Artificial Analysis / official model cards; avoid single-source absolute rankings. Latency is GJC-routed indicative only.

---

## 4. Release discipline (SemVer-ish `MAJOR.MINOR`)

- **MINOR** — profile/model placement change (must ship with `revalidate.sh` evidence), or a substantial standalone addition such as infra tooling or a new language (i18n) — see v1.2/v1.3.
- **PATCH/Docs** — wording/rationale; keep version or `x.y.z`.
- **MAJOR** — structural redesign (role model, setup flow, routing).
- Every release: `python3 scripts/validate-profiles.py` green → update `CHANGELOG.md` → tag `vX.Y`.
- **Adding or moving a profile touches a 5-file set that must move together**: `gjc-profiles.yml` + the embedded YAML blocks in **all four** `README*.md` (the validator enforces README↔file parity and fails CI on any mismatch). `install.sh` derives its profile count/roster from the downloaded YAML (since v1.4), so it needs no manual edit — but sanity-check its output once.
- **i18n**: when `gjc-profiles.yml` or the catalog changes, update the YAML block + tables in **all** language READMEs (`README.md` KO canonical · `README.en.md` · `README.zh.md` · `README.ja.md`). `validate-profiles.py` enforces YAML parity across every `README*.md`. Prose/comments translate; selectors stay verbatim. **KO-only blocks (intentional — do not "fix" translations by re-adding them)**: the §5 per-profile design-rationale block, the §5 `opencode-go`/grok-composer TIP, the table of contents, and the deep §6-2/§6-3 analysis (translations carry a summary paragraph + links to the KO canonical instead). `routing-rules.md` ships **Korean-only** by design — selectors/profile names in it are language-neutral; keep a language note next to the injection command in EN/ZH/JA.

---

## 5. Upstream (Yeachan-Heo/gajae-code)

A compressed version of this guide **was merged upstream** as `docs/multi-vendor-profiles.md` ([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev` branch) — upstream now maintains that page themselves (e.g. PR #1333 updated it for Sonnet 5), so expect it to drift from this repo and don't treat it as canonical. For **future upstream PRs** (target **`dev`**, not `main`; `main` is protected), the maintainer bot requires:
- docs-only diff (+ regenerated `packages/coding-agent/src/internal-urls/docs-index.generated.ts` via `bun --cwd=packages/coding-agent run generate-docs-index`),
- selector verification evidence in the PR body,
- **owner confirmation** for normative product claims (axis leaders, rankings, price/latency).

This standalone repo keeps the **one-line installer + full profile set (incl. `solo-*`, `claude-codex*`) + benchmarking tooling** that the upstream docs page does not carry, so it stays useful after any upstream merge.

---

## 6. Quick context for a cold-start session

Read in order: this file → `README.md` (§ verified selector notes) → `gjc-profiles.yml`. The newest `evidence/*-selectors.md` shows the last live-verified state. Re-verify before trusting any selector: `gjc -p --no-session --no-tools --model <selector> "Reply OK"`.
