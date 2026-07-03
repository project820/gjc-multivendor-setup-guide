#!/usr/bin/env python3
"""Static validator for gjc-profiles.yml — no credentials / no model calls.

Checks the durable invariants of the multi-vendor profile catalog so they can be
enforced in CI and by any future maintenance session:

  1. YAML parses; every profile has the 5 roles (default/executor/architect/planner/critic).
  2. Router invariant: if `anthropic` is in required_providers, `default` must be Anthropic.
  3. Cross-family review: executor-family != architect-family AND planner-family != critic-family
     (skipped for single-vendor profiles where it is impossible by construction).
  4. Effort-tier legality against the engine hard-rules (see EFFORT_RULES below).
  5. required_providers covers every provider actually used by the mapping.
  6. README.md embedded ```yaml profiles block == gjc-profiles.yml (drift guard).

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
    ("monorepo", "exec_arch"): "all roles >=1M ctx; gpt-5.5 (272K) excluded — gpt-5.4 is 1M but Opus ranks at least equal",
    ("claude-codex", "exec_arch"): "2-vendor: Anthropic = execution/context lane",
    ("claude-codex", "plan_crit"): "2-vendor: Codex = reasoning/critique lane",
    ("claude-codex-max", "exec_arch"): "2-vendor: Anthropic = execution/context lane",
    ("claude-codex-max", "plan_crit"): "2-vendor: Codex = reasoning/critique lane",
}

# provider-id -> vendor family (for cross-family checks)
FAMILY = {
    "anthropic": "claude", "openai-codex": "gpt", "openai": "gpt",
    "google-antigravity": "google", "google-gemini-cli": "google", "google": "google",
    "xai": "grok", "opencode-go": "ocgo", "zai": "zai",
    "kimi-code": "kimi", "xiaomi": "mimo", "minimax-code": "minimax", "cursor": "cursor",
}
# Legal effort suffixes by model class. Matchers take (provider, model_id) so
# per-provider ceilings can differ (same model id can clamp differently by provider).
# Sets encode GJC-EFFECTIVE ceilings (0.7.10, live-verified 2026-07-02), NOT the API ones:
#   fable-5 <=xhigh (:max silently clamps) · sonnet-5 <=high (API allows max — upstream gap)
#   xai grok <=high (:xhigh silently clamps; xhigh exists only on the grok-build provider,
#   whose effort suffixes don't resolve at all — bare grok-build selectors only).
def _eff_rules():
    return [
        (lambda p, m: m.startswith("claude-fable-5"), {"minimal","low","medium","high","xhigh"}),   # :max -> silent clamp to xhigh
        (lambda p, m: m.startswith("claude-sonnet-5"), {"minimal","low","medium","high"}),          # :xhigh/:max -> silent clamp to high
        (lambda p, m: m.startswith("claude-opus-4"), {"minimal","low","medium","high","xhigh","max"}),
        (lambda p, m: m.startswith("claude-sonnet-4"), {"minimal","low","medium","high"}),
        (lambda p, m: m.startswith("claude-haiku-4"), {"minimal","low","medium","high","xhigh"}),
        (lambda p, m: m.startswith("gpt-5.1-codex-mini"), {"medium","high"}),
        (lambda p, m: re.match(r"gpt-5\.[2-9]", m), {"low","medium","high","xhigh"}),
        (lambda p, m: m.startswith("gpt-5"), {"minimal","low","medium","high"}),  # base gpt-5/gpt-5.1 (catalog: minimal..high)
        (lambda p, m: "gemini" in m and "pro" in m, {"low","high"}),
        (lambda p, m: "gemini" in m and "flash" in m, {"minimal","low","medium","high"}),
        (lambda p, m: p == "xai" and m.startswith("grok"), {"minimal","low","medium","high"}),      # :xhigh -> silent clamp to high
        (lambda p, m: p == "grok-build" and m.startswith("grok"), set()),  # catalog lists xhigh but effort suffixes don't resolve — bare selectors only
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
        # 2. router invariant
        if "anthropic" in req and fam["default"] != "claude":
            errors.append(f"[{name}] default must be Anthropic when anthropic is available (got {mm['default']})")
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

    # 6. README embed sync — every README*.md with an embedded yaml block must match gjc-profiles.yml
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
