#!/usr/bin/env python3
"""승인 계획의 validator 개정 D-1·D-2·D-3(+D-3b) 을 `scripts/validate-profiles.py` 에 적용한다.

**왜 스크립트인가**: 계획은 D-1/D-2/D-3 를 산문으로만 적어놨다. 사람이 손으로 옮기면
삽입 위치(특히 D-1 이 일반 gpt-5.x 룰보다 **앞**이어야 한다는 순서 제약)를 틀리기 쉽고,
틀려도 조용히 통과한다. 이 스크립트는 **고유 앵커 문자열**로만 지목하고, 앵커가 없거나
여러 번 나오면 **중단**한다(행 번호에 의존하지 않는다 — v3 는 이 파일을 편집하므로).

적용 후 검증은 `scripts/ci-fixture-check.sh` 가 한다(v3 fixture 5종이 자동 활성화된다).

사용:
  python3 scripts/apply-validator-v3.py --check   # 적용 가능한지만 확인, 파일 미변경
  python3 scripts/apply-validator-v3.py           # 실제 적용
  python3 scripts/apply-validator-v3.py --root DIR
종료코드: 0 성공 / 1 앵커 불일치·이미 적용됨 등 실패
"""
import argparse
import pathlib
import subprocess
import sys

# ── 앵커: 각각 파일 안에서 정확히 1회만 나와야 한다 ───────────────────────────
A_D1 = '''def _eff_rules():
    return [
'''
NEW_D1 = '''def _eff_rules():
    return [
        # D-1 (v3): Luna exact matcher — 반드시 일반 gpt-5.[2-9] 룰보다 앞에 온다.
        # Sol/Terra 는 계속 xhigh 상한이고 Luna 는 **:max 만** 합법이다.
        # 사용자 결정(2026-08-17): "luna 는 max 만 허용한다" — 계획 원안의
        # {low,medium,high,xhigh,max} 를 {max} 단독으로 좁혔다. v3 에서 Luna 좌석은
        # daily.executor 하나뿐이므로(eco.planner 는 eco 와 함께 삭제) 다른 effort 는
        # 출하 경로가 없다. 좁은 쪽이 fail-closed 다.
        (lambda p, m: p == "openai-codex" and m == "gpt-5.6-luna", {"max"}),
'''

A_D2 = '''        # 4. effort legality
'''
NEW_D2 = '''        # D-2 (v3): default 와 critic 이 같은 family 면 hard ERROR. allowlist 없음.
        if fam["default"] == fam["critic"]:
            errors.append(f"[{name}] default/critic share family ({fam['default']}) — breaks final-review independence")
        # 4. effort legality
'''

A_D3_START = '''NON_ANTHROPIC_DEFAULT_OK = {'''
NEW_D3 = '''# D-3 (v3): ultimate-sol 드롭과 함께 이 예외는 사라진다. 비면 빈 dict 로 남긴다.
NON_ANTHROPIC_DEFAULT_OK = {}
'''


def _default_root():
    parent = pathlib.Path(__file__).resolve().parent.parent
    if (parent / "gjc-profiles.yml").exists():
        return parent
    try:
        top = subprocess.run(
            ["git", "-C", str(pathlib.Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return parent
    if not top:
        return parent
    print(f"note: repo root resolved via git → {top}", file=sys.stderr)
    return pathlib.Path(top)


def _once(text, anchor, label):
    n = text.count(anchor)
    if n != 1:
        sys.exit(f"apply-validator-v3: {label} 앵커가 {n}회 매칭됨(1회여야 함) — 수동 확인 필요")


def main():
    ap = argparse.ArgumentParser(description="apply v3 validator amendments D-1/D-2/D-3")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true", help="적용 가능성만 확인하고 쓰지 않는다")
    args = ap.parse_args()
    root = pathlib.Path(args.root) if args.root else _default_root()

    path = root / "scripts" / "validate-profiles.py"
    if not path.exists():
        sys.exit(f"apply-validator-v3: {path} not found")
    src = path.read_text(encoding="utf-8")

    if "D-1 (v3)" in src or "D-2 (v3)" in src or "D-3 (v3)" in src:
        sys.exit("apply-validator-v3: 이미 적용된 흔적이 있다 — 중복 적용 방지로 중단")

    A_D3B = '    ("dream-team", "exec_arch"): '
    _once(src, A_D3B, "D-3b")
    _once(src, A_D1, "D-1")
    _once(src, A_D2, "D-2")
    _once(src, A_D3_START, "D-3")

    # D-3 은 dict 리터럴 전체를 지워야 하므로 시작 앵커부터 닫는 '}' 줄까지 잘라낸다.
    i = src.index(A_D3_START)
    j = src.index("\n}\n", i) + len("\n}\n")
    # 바로 위 설명 주석 줄도 함께 교체 대상에 넣는다(고아 주석 방지).
    k = src.rfind("# Documented non-Anthropic default routers", 0, i)
    if k == -1:
        sys.exit("apply-validator-v3: D-3 설명 주석을 찾지 못했다 — 수동 확인 필요")

    out = src[:k] + NEW_D3 + src[j:]
    # D-3b: dream-team 은 v3 로스터에서 드롭되므로 SAME_FAMILY_OK 엔트리가 죽은 예외가 된다.
    # 한 엔트리가 여러 줄에 걸칠 수 있어 다음 항목 시작(또는 dict 닫힘)까지 잘라낸다.
    b = out.index(A_D3B)
    e = out.index("\n", b)
    while True:
        nxt = out[e + 1:]
        if nxt.lstrip().startswith('("') or nxt.lstrip().startswith("}"):
            break
        e = out.index("\n", e + 1)
    out = out[:b] + out[e + 1:]
    out = out.replace(A_D1, NEW_D1, 1)
    out = out.replace(A_D2, NEW_D2, 1)

    if args.check:
        print("OK — D-1/D-2/D-3 앵커 모두 유일 매칭. 적용 가능(파일 미변경).")
        return 0

    path.write_text(out, encoding="utf-8")
    print(f"OK — D-1/D-2/D-3 적용 완료: {path}")
    print("다음: bash scripts/ci-fixture-check.sh  (v3 fixture 5종이 자동 활성화된다)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
