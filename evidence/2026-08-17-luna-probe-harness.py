#!/usr/bin/env python3
"""Luna :max vs :xhigh 사전등록 paired 비교.

프로토콜(사전 고정, 사후 조정 금지):
  - 10개 태스크, 정답 자동 채점
  - 각 태스크 x {max, xhigh} x 3반복 = 60콜
  - 지표: 정답 점수(0/1), output 토큰 수, 지연
  - 합격: Wilcoxon p<0.05 (단측, max 우월) AND
          최소 4/10 태스크에서 max 평균이 xhigh 평균보다 +0.1 이상 앞서고
          그 우위가 각 태스크 3회 중 2회 이상 재현
"""
import json, re, subprocess, sys, tempfile, shutil, time, pathlib

TASKS = [
    ("t01", "What is 2^17? Reply with only the number.", lambda s: "131072" in s),
    ("t02", "A train leaves at 14:47 and the trip takes 3 hours 38 minutes. What time does it arrive? Reply HH:MM only.", lambda s: "18:25" in s),
    ("t03", "How many distinct anagrams does the word BALLOON have? Reply with only the number.", lambda s: "1260" in s),
    ("t04", "What is the 12th Fibonacci number if F(1)=1 and F(2)=1? Reply with only the number.", lambda s: re.search(r'\b144\b', s) is not None),
    ("t05", "Solve for x: 3x + 7 = 5x - 11. Reply with only the number.", lambda s: re.search(r'\b9\b', s) is not None),
    ("t06", "In a round-robin tournament with 9 teams where each pair plays once, how many games are played? Reply with only the number.", lambda s: re.search(r'\b36\b', s) is not None),
    ("t07", "What is the remainder when 7^100 is divided by 13? Reply with only the number.", lambda s: re.search(r'\b9\b', s) is not None),
    ("t08", "A number is 3 more than twice another. Their sum is 42. What is the smaller number? Reply with only the number.", lambda s: re.search(r'\b13\b', s) is not None),
    ("t09", "How many trailing zeros are in 50! ? Reply with only the number.", lambda s: re.search(r'\b12\b', s) is not None),
    ("t10", "What is the sum of all prime numbers below 20? Reply with only the number.", lambda s: re.search(r'\b77\b', s) is not None),
]
REPS = 3
EFFORTS = ["max", "xhigh"]
MODEL = "openai-codex/gpt-5.6-luna"


def call(selector, prompt):
    d = tempfile.mkdtemp()
    t0 = time.time()
    try:
        r = subprocess.run(
            ["gjc", "-p", "--session-dir", d, "--no-tools", "--model", selector, prompt],
            capture_output=True, text=True, timeout=180)
        out = r.stdout.strip()
    except subprocess.TimeoutExpired:
        out = ""
    el = time.time() - t0
    tokens = None
    tl = None
    for f in pathlib.Path(d).rglob("*.jsonl"):
        for line in f.read_text(errors="ignore").splitlines():
            try:
                o = json.loads(line)
            except Exception:
                continue
            def w(x):
                nonlocal tokens, tl
                if isinstance(x, dict):
                    for k, v in x.items():
                        if k == "thinkingLevel":
                            tl = v
                        if k == "usage" and isinstance(v, dict):
                            tokens = v.get("output")
                        w(v)
                elif isinstance(x, list):
                    for i in x:
                        w(i)
            w(o)
    shutil.rmtree(d, ignore_errors=True)
    return out, tokens, el, tl


def main():
    rows = []
    total = len(TASKS) * len(EFFORTS) * REPS
    n = 0
    for tid, prompt, check in TASKS:
        for eff in EFFORTS:
            for rep in range(REPS):
                n += 1
                out, tok, el, tl = call(f"{MODEL}:{eff}", prompt)
                ok = 1 if check(out) else 0
                rows.append({"task": tid, "effort": eff, "rep": rep,
                             "score": ok, "outTokens": tok, "sec": round(el, 1),
                             "thinkingLevel": tl})
                print(f"[{n}/{total}] {tid} {eff} rep{rep}: score={ok} tok={tok} {el:.1f}s", flush=True)
    pathlib.Path("/tmp/luna_raw.json").write_text(json.dumps(rows, indent=1))
    print("wrote /tmp/luna_raw.json")


if __name__ == "__main__":
    main()
