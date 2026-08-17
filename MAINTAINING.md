# Maintaining this guide — research & validation playbook

This repo is meant to stay correct as model catalogs, prices, and provider behavior drift.
Anything in here can be picked up by a fresh session (human or a `gjc` agent) **without prior context** — clone the repo and follow this file.

> One-line orientation: the profiles assign GJC's five roles (`default` / `executor` / `architect` / `planner` / `critic`) to the best model per role across vendors. `default` stays on the strongest router (an Anthropic flagship — Opus 5 or Fable 5 — when available); `critic` stays cross-family. Everything is **user config** (`~/.gjc/agent/models.yml`), not bundled defaults.

---

## 1. Durable invariants (never silently break these)

1. **`default` = strongest router.** If `anthropic` is in `required_providers`, `default` must be an **Anthropic flagship (Opus 5 / Fable 5)**. A weak router caps whole-system quality. Documented exceptions live in `scripts/validate-profiles.py` (`NON_ANTHROPIC_DEFAULT_OK` — **empty since v3.0.0**: `ultimate-sol` was its only entry and it was dropped. `budget` is not an exception but out of scope — it does not require `anthropic`, so the invariant never fires).
2. **`critic` is cross-family** from the `executor`/`planner` it reviews. Documented exceptions live in `scripts/validate-profiles.py` (`SAME_FAMILY_OK` — **3 entries since v3.0.0**: ctx-forced `monorepo` exec_arch + human-ruled 2026-07-10 `ultimate-opus` exec_arch and `coding-sprint` plan_crit; the `dream-team` entry died with the bundle). Since v3.0.0 `default` ↔ `critic` sharing a family is a **hard ERROR** with no allowlist (rule D-2). **Invariant: every bundle spans ≥2 vendors** — single-vendor demand belongs to GJC built-in profiles, not this catalog.
3. **Effort hard-rules** (⚠ these are **GJC-effective** ceilings as of 0.13.3, NOT the API's own tiers): Opus 5 / Opus 4.6+ `minimal..max`; **Fable 5 `≤xhigh`** (`:max` still returns OK — possible clamp, never shipped; thinking always-on); **Sonnet 4.6/5 shipped legality `≤high`** (catalog now lists xhigh/max on Sonnet 5; clamp-vs-real unmeasured); GPT 5.2+/codex `low..xhigh`; **GPT-5.6 Sol/Terra shipped ceiling stays `xhigh`** (`:max` is accepted live but its depth is un-benchmarked — not shipped); **GPT-5.6 Luna is `:max` only** since v3.0.0 — validator rule D-1 rejects every other effort, and that seat is a **policy** decision, not a measured win (the pre-registered `:max` vs `:xhigh` battery failed: effect size 0/10, Wilcoxon one-sided p=0.1587); **Gemini Pro `low`/`high` only**; Gemini Flash `minimal..high`; **xai Grok 4.6 catalog `low..xhigh`** (shipped seats `:high`; `:xhigh` accepted 2026-08-16, no L3); **xai Grok 4.5 `≤high`** (legacy canary); grok-build effort suffixes still do not resolve (`grok-4.6:high` = not found, bare OK); opencode-go: omit `:effort`.
4. **Antigravity high reasoning = `gemini-3.1-pro-low:high`** (literal pin). Fuzzy space stays **fail-closed** (`gemini-3.1-pro-high` = not found). Gemini 3.5 Pro is **not** in the 2026-08-16 catalog. Flash 3.5/3.6 ids flap (3.5-flash-low vanished 07-10 PM, resurrected 08-16) — the light seat `gemini-3-flash:low` was `eco.critic` in v2.1.0 and holds **zero shipped seats since v3.0.0**.
5. **`-codex` variants don't work on a ChatGPT/Codex account** — use base `gpt-5.6-sol`/`gpt-5.6-terra`/`gpt-5.6-luna` / `gpt-5.5` / `gpt-5.4` (5.6 trio live-verified 2026-08-16; gjc 0.13.3 usable prompt budget **372K** each — 373K was the 0.9.6 print; API spec 1.05M is a separate contract).
6. **Single-message `@file` input limit ≠ context window (1M), and it is generation-specific.** Opus 4.8 measured 350k ✅ / 476k 🔴. **Opus 5 passes 476k** (2026-08-17 battery, `evidence/2026-08-17-selectors.md`); `xai/grok-4-fast:high` also passes 476k. Chunking huge inputs across turns is still preferred because a 1M nominal window is not full recall.
7. **Bundled vs live catalog**: `opencode-go` and `google-antigravity` discover additional models from the provider API after `/login`. `glm-5.2` is bundled; `xai/grok-4.6` is the shipped Grok critic (500K, $2/$6 below 200k prompt). `grok-build/grok-4.6` resolves **bare only**. Catalog snapshots contain no price; verify price from xAI/OpenRouter. `opencode-go/deepseek-v4-flash` may 403 on China-hosted opt-in accounts (2026-08-16) without being delisted. **Two durable lessons:** retired slugs can keep answering while silently redirecting billing (`grok-4-1-fast` was retired by xAI on 2026-05-15 and redirects to grok-4.3 rates — still probed as an informational canary in `revalidate.sh`), and catalog metadata can lag the provider's live surface, so a live call is the truth, not `--list-models`.

Every claim in `README.md` is **time-sensitive (catalog at validation date)** — keep the dated caveat.

---

## 2. Tooling

| Script | Needs creds? | What it does |
| --- | --- | --- |
| `scripts/validate-profiles.py` | no | Static guard: YAML valid, 5 roles, router invariant, cross-family (with allowlist), effort legality, `required_providers` coverage, README-embed == `gjc-profiles.yml`. **Runs in CI.** |
| `scripts/revalidate.sh` | yes (`/login`) | Live battery: every profile selector via real `gjc -p`; records `evidence/<date>-selectors.md`; non-zero exit on regression. `SELECTORS_ONLY=1` skips long-context probes. |
| `scripts/catalog-snapshot.sh` | yes | Dumps the live catalog to `evidence/<date>-catalog.txt`; `--diff` compares the two newest snapshots (new/retired models, ctx/effort drift — snapshots carry no price data; verify prices against official pages). |
| `scripts/cyber-cop-review.sh` | yes (`/login` + `gh`) | Headless cyber-cop reviewer-mode PR review, **seat orchestrator**: per-seat `gjc -p --model …` calls so the critic really runs on `openai-codex/gpt-5.6-sol` (cross-family vs the Claude author) — not role-played by the default model (#10). Each section names its executing model; INVARIANTS run by the script itself; `--panel` adds the 3-vote high-risk critic panel. Never merges. |
| `scripts/gjc-cop` | yes (`/login` + `gh`) | One-command reviewer wrapper shipped by `install.sh GJC_SETUP_COP=1` to `~/.local/bin/gjc-cop` (deps in `~/.gjc/agent/cyber-cop/`). `gjc-cop <PR>` / `--panel <PR>` / `shell` / `watch` / `--install-hook` (pre-push: outgoing diff → single cross-family critic; advisory default, `git config cop.strict true` blocks non-APPROVE — in strict, EVERY pre-seat failure (missing gjc, diff-computation failure, >5MiB diff, seat failure) fails closed; bypass `git push --no-verify`) — clone-free; always injects trusted local paths (kills the #6 relative-path injection class by construction). Wraps `cyber-cop-review.sh`; never merges. |
| `scripts/extragoal-gate-init` | no | Shipped by `install.sh GJC_SETUP_EXTRAGOAL=1` to `~/.gjc/agent/extragoal/` + `~/.local/bin`. Creates/idempotently updates a review working directory **outside the repo** with `.gjc/config.yml` disabling the injected `goal` tool (per the upstream gate contract). |
| `scripts/extragoal-courier-pack` | no | Assembles the Stage 1 review bundle with git only (rung-1 manual courier). Enforces Stage 0 fail-closed: rejects uncommitted/untracked work, the default branch (`EXTRAGOAL_ALLOW_BRANCH=1` override), and an empty merge-base diff; validates the base ref; defaults the bundle out of the repo, registering an in-repo override in `info/exclude` (worktree-safe via `git rev-parse --git-path`). |
| `scripts/extragoal-courier-secret-scan` | no | Mandatory pre-send scan for the courier lane (the bundle leaves the machine). Blocks (exit 1) on private keys, cloud/API/GitHub tokens, JWTs, and quoted **or unquoted** env-style secret assignments; a scan error also fails closed (exit 2). |
| `scripts/extragoal-courier-verdict` | no | Parses the reviewer reply's **last non-empty line**; exit 0=APPROVE / 1=REQUEST_CHANGES / 2=malformed (quoted-only verdict token, or APPROVE alongside CRITICAL/HIGH — human triage required). |

```bash
python3 scripts/validate-profiles.py          # before every commit / in CI
bash scripts/revalidate.sh                     # on an authed machine (quarterly / on catalog news)
bash scripts/catalog-snapshot.sh               # snapshot; later: scripts/catalog-snapshot.sh --diff
```

`evidence/` is the durable audit trail — committed, dated, never rewritten. It backs the README's "verified" claims.
It also holds the dated deep-research / consultant / model-council reports that justify the role→model assignments (`evidence/<date>-deep-research-benchmarks.md`, `-consultant-report.md`, `-ultimate-final-report.md`), cross-linked from docs/deep-dive-role-fit.md (formerly README §6-2). Re-validation ships as a *new* dated report — never edit a published one.

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
- **MAJOR** — structural redesign (role model, setup flow, routing). Worked example: **v3.0.0**
  cut the catalog from 10 bundles to 8 (dropping `dream-team`·`eco`·`ultimate-sol`, adding
  `budget` after its 3-condition gate passed — `evidence/2026-08-17-v3-budget-gate-ruling.md`),
  redefined the Core tier from
  "three-provider entry point" to "activates with the three subscription logins alone
  (`anthropic`, `openai-codex`, `google-antigravity`) — no API key and no `xai`", replaced the
  tier-ordered selection funnel with a minimum-required-provider matrix, and amended the
  validator itself (Luna-only `:max`, hard `default`↔`critic` family rule). A MAJOR is not
  "many edits" — it is a change to a contract readers or the gate already depend on.
- Every release: `python3 scripts/validate-profiles.py` green → update `CHANGELOG.md` → tag `vX.Y.Z`.
- **Adding or moving a profile touches a 5-file set that must move together**: `gjc-profiles.yml` + the embedded YAML blocks in **all four** `README*.md` (the validator enforces README↔file parity and fails CI on any mismatch). `install.sh` derives its profile count/roster from the downloaded YAML (since v1.4), so it needs no manual edit — but sanity-check its output once.
- **i18n**: when `gjc-profiles.yml` or the catalog changes, update the YAML block + tables in **all** language READMEs (`README.md` KO canonical · `README.en.md` · `README.zh.md` · `README.ja.md`). `validate-profiles.py` enforces YAML parity across every `README*.md`. Prose/comments translate; selectors stay verbatim. **KO-only blocks (intentional — do not "fix" translations by re-adding them)**: the §5 per-profile design-rationale block, the §5 `opencode-go`/grok-composer TIP, the table of contents, and the deep §6-2/§6-3 analysis (now `docs/deep-dive-role-fit.md`, KO-only doc) (translations carry a summary paragraph + links to the KO canonical instead). `routing-rules.md` ships **Korean-only** by design — selectors/profile names in it are language-neutral; keep a language note next to the injection command in EN/ZH/JA.

---

## 5. Upstream (Yeachan-Heo/gajae-code)

A compressed version of this guide **was merged upstream** as `docs/multi-vendor-profiles.md` ([PR #860](https://github.com/Yeachan-Heo/gajae-code/pull/860), `dev` branch) — upstream now maintains that page themselves (e.g. PR #1333 updated it for Sonnet 5), so expect it to drift from this repo and don't treat it as canonical. For **future upstream PRs** (target **`dev`**, not `main`; `main` is protected), the maintainer bot requires:
- docs-only diff (+ regenerated `packages/coding-agent/src/internal-urls/docs-index.generated.ts` via `bun --cwd=packages/coding-agent run generate-docs-index`),
- selector verification evidence in the PR body,
- **owner confirmation** for normative product claims (axis leaders, rankings, price/latency).

This standalone repo keeps the **one-line installer + full 10-bundle catalog (4 tiers, incl. `cyber-cop` reviewer mode and the Council/Escalation workflow contracts) + benchmarking tooling** that the upstream docs page does not carry, so it stays useful after any upstream merge.

---

## 6. Quick context for a cold-start session

Read in order: this file → `README.md` (§ verified selector notes) → `gjc-profiles.yml`. The newest `evidence/*-selectors.md` shows the last live-verified state. Re-verify before trusting any selector: `gjc -p --no-session --no-tools --model <selector> "Reply OK"`.
