#!/usr/bin/env python3
"""Static validator for gjc-profiles.yml — no credentials / no model calls.

Checks the durable invariants of the multi-vendor profile catalog so they can be
enforced in CI and by any future maintenance session:

  1. YAML parses; every profile has the 5 roles (default/executor/architect/planner/critic).
  2. Router invariant: if `anthropic` is in required_providers, `default` must be Anthropic
     (documented exceptions via NON_ANTHROPIC_DEFAULT_OK — surfaced as WARN, never silent).
  3. Cross-family review: executor-family != architect-family AND planner-family != critic-family
     (skipped for single-vendor profiles where it is impossible by construction).
  4. Effort-tier legality against the engine hard-rules (see EFFORT_RULES below).
  5. required_providers covers every provider actually used by the mapping.
  6. Multi-vendor collaboration (v2, human ruling 2026-07-10): every bundle spans >= 2 vendors —
     single-vendor demand belongs to GJC built-in profiles.
  7. README.md embedded ```yaml profiles block == gjc-profiles.yml (drift guard).

Exit non-zero on any hard violation. Usage: python3 scripts/validate-profiles.py
"""
from __future__ import annotations
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Optional --root <dir>: validate a different tree's DATA (gjc-profiles.yml + README*.md)
# while THIS trusted script executes. Used by cyber-cop-review.sh to check a PR head's
# data without executing the PR's code (no cd into / import from an untrusted tree).
if "--root" in sys.argv:
    _i = sys.argv.index("--root")
    if _i + 1 >= len(sys.argv):
        sys.exit("--root requires a directory argument")
    ROOT = pathlib.Path(sys.argv[_i + 1]).resolve()
PROFILES = ROOT / "gjc-profiles.yml"
README = ROOT / "README.md"
ROLES = {"default", "executor", "architect", "planner", "critic"}

# Documented intentional same-family pairs (design choices, not bugs).
# (profile, pair) -> rationale ; pair in {"exec_arch","plan_crit"}.
SAME_FAMILY_OK = {
    ("monorepo", "exec_arch"): "1M paste path is Opus; gpt-5.6 excluded (372K). Gemini planner removed (budget-only policy)",
    ("monorepo", "plan_crit"): "qwen planner + glm critic are distinct ocgo models; gpt-5.6 excluded from this 1M bundle; Grok critic is 500K so not used here",
    ("ultimate-opus", "exec_arch"): "human ruling 2026-07-10: Opus quality base; Sol planner + Grok critic carry cross-family verification (bundle stays 3-vendor)",
    ("coding-sprint", "exec_arch"): "Opus throughput executor+architect; Sol planner + Grok critic carry cross-family verification after Gemini architect was removed (budget-only policy)",
    ("escalation", "exec_arch"): "Fable rescue executor + Opus architect (both claude); Sol planner + Grok critic carry cross-family verification after Gemini architect was removed (budget-only policy)",
}

# D-3 (v3): ultimate-sol 드롭과 함께 이 예외는 사라진다. 비면 빈 dict 로 남긴다.
NON_ANTHROPIC_DEFAULT_OK = {}

# provider-id -> vendor family (for cross-family checks)
FAMILY = {
    "anthropic": "claude", "openai-codex": "gpt", "openai": "gpt",
    "google-antigravity": "google", "google-gemini-cli": "google", "google": "google",
    "xai": "grok", "opencode-go": "ocgo", "zai": "zai",
    "kimi-code": "kimi", "xiaomi": "mimo", "minimax-code": "minimax", "cursor": "cursor",
}
# Legal effort suffixes by model class. Matchers take (provider, model_id) so
# per-provider ceilings can differ (same model id can clamp differently by provider).
# Sets encode GJC-EFFECTIVE shipped ceilings (live-verified 2026-08-16 on gjc 0.13.3), NOT the API ones:
#   fable-5 <=xhigh (:max still returns OK — possible silent clamp; never shipped)
#   sonnet-5 shipped legality stays <=high (catalog now lists xhigh/max; clamp-vs-real unmeasured)
#   opus-5 / opus-4.x = full ladder including max
#   xai grok-4.6: catalog lists low..xhigh and :xhigh resolves live (2026-08-16), but its depth is
#   un-benchmarked — deliberate fail-closed ceiling stays high, same treatment as gpt-5.6 :max below
#   xai grok-4.5 <=high
#   grok-build effort suffixes still don't resolve (grok-4.6:high = not found; bare grok-4.6 OK)
#   gpt-5.6-sol/terra/luna: catalog lists low..max and :max is accepted live,
#   but its depth is un-benchmarked — deliberate fail-closed ceiling stays xhigh (gpt-5.[2-9] rule).
def _eff_rules():
    return [
        # D-1 (v3): Luna exact matcher — 반드시 일반 gpt-5.[2-9] 룰보다 앞에 온다.
        # Sol/Terra 는 계속 xhigh 상한이고 Luna 는 **:max 만** 합법이다.
        # 사용자 결정(2026-08-17): "luna 는 max 만 허용한다" — 계획 원안의
        # {low,medium,high,xhigh,max} 를 {max} 단독으로 좁혔다. v3 에서 Luna 좌석은
        # daily.executor 하나뿐이므로(eco.planner 는 eco 와 함께 삭제) 다른 effort 는
        # 출하 경로가 없다. 좁은 쪽이 fail-closed 다.
        (lambda p, m: p == "openai-codex" and m == "gpt-5.6-luna", {"max"}),
        # Daybreak Blue — GJC openai-codex 핀. 카탈로그 minimal..xhigh (:max 없음). 출하 좌석은 :high.
        (lambda p, m: p == "openai-codex" and m == "gpt-daybreak-blue-latest", {"minimal","low","medium","high","xhigh"}),
        (lambda p, m: m.startswith("claude-fable-5"), {"minimal","low","medium","high","xhigh"}),   # :max accepted; do not ship
        (lambda p, m: m.startswith("claude-sonnet-5"), {"minimal","low","medium","high"}),          # catalog lists xhigh/max; shipped legality stays high
        (lambda p, m: m.startswith("claude-opus-5"), {"minimal","low","medium","high","xhigh","max"}),
        (lambda p, m: m.startswith("claude-opus-4"), {"minimal","low","medium","high","xhigh","max"}),
        (lambda p, m: m.startswith("claude-sonnet-4"), {"minimal","low","medium","high"}),
        (lambda p, m: m.startswith("claude-haiku-4"), {"minimal","low","medium","high","xhigh"}),
        (lambda p, m: m.startswith("gpt-5.1-codex-mini"), {"medium","high"}),
        (lambda p, m: re.match(r"gpt-5\.[2-9]", m), {"low","medium","high","xhigh"}),
        (lambda p, m: m.startswith("gpt-5"), {"minimal","low","medium","high"}),  # base gpt-5/gpt-5.1 (catalog: minimal..high)
        (lambda p, m: "gemini" in m and "pro" in m, {"low","high"}),
        (lambda p, m: "gemini" in m and "flash" in m, {"minimal","low","medium","high"}),
        (lambda p, m: p == "xai" and m.startswith("grok-4.6"), {"low","medium","high"}),  # catalog has xhigh; shipped ceiling high (depth un-benchmarked)
        (lambda p, m: p == "xai" and m.startswith("grok-4.5"), {"low","medium","high"}),
        (lambda p, m: p == "xai" and m.startswith("grok"), {"minimal","low","medium","high"}),
        (lambda p, m: p == "grok-build" and m.startswith("grok"), set()),  # effort suffixes don't resolve — bare selectors only
    ]

def family_of(selector: str) -> str:
    prov = selector.split("/", 1)[0]
    return FAMILY.get(prov, prov)

def split_selector(selector: str):
    prov, rest = selector.split("/", 1)
    if ":" in rest:
        model, eff = rest.rsplit(":", 1)
    else:
        model, eff = rest, None
    return prov, model, eff

def load_profiles(text: str) -> dict:
    try:
        import yaml
        return yaml.safe_load(text)["profiles"]
    except ModuleNotFoundError:
        sys.exit("PyYAML required: pip install pyyaml")

def main() -> int:
    errors: list[str] = []
    warns: list[str] = []
    profiles = load_profiles(PROFILES.read_text(encoding="utf-8"))

    for name, prof in profiles.items():
        mm = (prof or {}).get("model_mapping", {})
        req = set((prof or {}).get("required_providers", []))
        # 1. roles present
        missing = ROLES - set(mm)
        if missing:
            errors.append(f"[{name}] missing roles: {sorted(missing)}")
            continue
        fam = {r: family_of(v) for r, v in mm.items()}
        used_prov = {v.split('/',1)[0] for v in mm.values()}
        # 2. router invariant (documented exceptions -> WARN)
        if "anthropic" in req and fam["default"] != "claude":
            if name in NON_ANTHROPIC_DEFAULT_OK:
                warns.append(f"[{name}] non-Anthropic default ({mm['default']}) — documented exception: {NON_ANTHROPIC_DEFAULT_OK[name]}")
            else:
                errors.append(f"[{name}] default must be Anthropic when anthropic is available (got {mm['default']})")
        # 2b. multi-vendor collaboration invariant (v2): no single-vendor bundles.
        # Checked against providers ACTUALLY USED by the mapping (not required_providers,
        # which could be padded with unused entries to game the check — PR #21 critic).
        if len(used_prov) < 2:
            errors.append(f"[{name}] single-vendor bundle (mapping uses only {sorted(used_prov)}) — v2 catalog requires >=2 vendors; single-vendor demand belongs to GJC built-ins")
        padding = req - used_prov
        if padding:
            warns.append(f"[{name}] required_providers lists providers the mapping never uses: {sorted(padding)} — activation burden without a seat; drop or justify")
        # 3. cross-family (skip single-vendor; allow documented exceptions)
        if len(req) > 1:
            if fam["executor"] == fam["architect"]:
                if (name, "exec_arch") in SAME_FAMILY_OK:
                    warns.append(f"[{name}] executor/architect same family ({fam['executor']}) — intentional: {SAME_FAMILY_OK[(name,'exec_arch')]}")
                else:
                    errors.append(f"[{name}] executor/architect share family ({fam['executor']}) — breaks code-review independence")
            if fam["planner"] == fam["critic"]:
                if (name, "plan_crit") in SAME_FAMILY_OK:
                    warns.append(f"[{name}] planner/critic same family ({fam['planner']}) — intentional: {SAME_FAMILY_OK[(name,'plan_crit')]}")
                else:
                    errors.append(f"[{name}] planner/critic share family ({fam['planner']}) — breaks plan-critique independence")
        # D-2 (v3): default 와 critic 이 같은 family 면 hard ERROR. allowlist 없음.
        if fam["default"] == fam["critic"]:
            errors.append(f"[{name}] default/critic share family ({fam['default']}) — breaks final-review independence")
        # 4. effort legality
        for role, sel in mm.items():
            prov, model, eff = split_selector(sel)
            if eff is None:
                continue
            legal = None
            for matcher, allowed in _eff_rules():
                try:
                    if matcher(prov, model):
                        legal = allowed; break
                except Exception:
                    pass
            if legal is None:
                warns.append(f"[{name}.{role}] no effort rule for '{model}:{eff}' (unverified)")
            elif eff not in legal:
                errors.append(f"[{name}.{role}] illegal effort '{eff}' for {model} (legal: {sorted(legal)})")
        # 5. required_providers covers usage
        uncovered = used_prov - req
        if uncovered:
            errors.append(f"[{name}] uses providers not in required_providers: {sorted(uncovered)}")

    # 6. README embed sync — every README*.md with an embedded yaml block must match gjc-profiles.yml.
    # Comparison is on PARSED model_mapping dicts (not text), so localized READMEs may embed a
    # comment-stripped variant (scripts/sync-readme-yaml.py) and still stay parity-green.
    import yaml
    file_map = {n: p["model_mapping"] for n, p in profiles.items()}
    readmes = sorted(ROOT.glob("README*.md"))
    checked_any = False
    for rf in readmes:
        rtext = rf.read_text(encoding="utf-8")
        m = re.search(r"```yaml\n(profiles:.*?)\n```", rtext, re.S)
        if not m:
            continue
        checked_any = True
        embed = yaml.safe_load(m.group(1))["profiles"]
        embed_map = {n: p["model_mapping"] for n, p in embed.items()}
        if embed_map != file_map:
            errors.append(f"{rf.name} embedded profiles != gjc-profiles.yml (drift). Re-sync its YAML block.")
    if not checked_any:
        warns.append("no README*.md has an embedded ```yaml profiles block")

    print(f"profiles checked: {len(profiles)}")
    for w in warns:
        print(f"  WARN  {w}")
    if errors:
        print(f"\nFAIL ({len(errors)} error(s)):")
        for e in errors:
            print(f"  ERROR {e}")
        return 1
    print("OK — all invariants hold")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
