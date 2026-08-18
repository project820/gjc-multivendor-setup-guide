#!/usr/bin/env python3
"""`slug-anchor-check.py` 가 **실제로 fail-closed 인지** 픽스처로 증명한다.

왜 필요한가
-----------
링크 게이트는 그린이면 아무 말도 안 한다. 그래서 "검사한다고 말하고 실제로는 안 하는"
상태를 눈으로 못 잡는다 — v3 작업에서 이 클래스의 결함이 **세 번** 나왔다:

  1. 4칸 들여쓰기를 코드블록으로 보고 덮어서 중첩 리스트 안 링크가 통째로 미검사.
  2. 들여쓰기를 먼저 지운 뒤 폭 제한을 걸어 그 제한이 죽은 코드가 됨 → 들여쓴 ``` 이
     펜스를 열고 EOF 까지 마스킹.
  3. HTML 속성에 따옴표를 강제해 `<img src=a.svg>` 같은 깨진 참조가 그냥 통과.

셋 다 게이트는 `OK` 를 찍고 있었다. 그래서 **음성 경로를 픽스처로 고정**한다.
각 케이스는 임시 트리에 최소 문서를 만들고 종료코드를 기대값과 대조한다.

`ci-fixture-check.sh` 가 validator 에 대해 하는 일과 같은 계약이다.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "slug-anchor-check.py")
T = chr(96) * 3          # ``` — 이 파일 자체가 픽스처에 걸리지 않도록 조립해서 쓴다

# name -> (README.md 줄들, 기대 종료코드)
CASES = {
    # 마스킹이 과하면 링크가 조용히 사라진다 → 반드시 검사돼야 한다
    "indented-fence-must-not-open": (
        ["# Target", "", "- top", "        " + T, "        code", "        " + T,
         "", "[after](#gone)"], 1),
    "nested-list-link-must-be-checked": (
        ["# Target", "", "- top", "    - [nested](#gone)"], 1),
    "unclosed-fence-must-fail": (
        ["# Target", "", T, "code that never closes", "", "[hidden](#gone)"], 1),
    # 마스킹이 모자라면 코드 샘플이 죽은 링크로 오탐된다 → 반드시 무시돼야 한다
    "normal-fence-must-mask": (
        ["# Target", "", T + "yaml", "[fenced](./missing.md)", T, "",
         "[ok](#target)"], 0),
    "blockquote-fence-must-mask": (
        ["# Target", "", "> " + T, "> [fenced](./missing.md)", "> " + T, "",
         "[ok](#target)"], 0),
    "inline-code-span-must-mask": (
        ["# Target", "", "문서가 링크 문법을 이야기한다: `](./missing.md)`", "",
         "[ok](#target)"], 0),
    "prose-backtick-run-must-not-open-fence": (
        ["# Target", "", "여는/닫는 펜스(" + T + T + " 안의", T + " 에서), `~~~` 도.",
         "", "[after-prose](#gone)"], 1),
    # HTML 참조
    "unquoted-img-src-must-be-checked": (
        ["# Target", "", "<img src=assets/missing.svg>"], 1),
    "unquoted-a-href-must-be-checked": (
        ["# Target", "", "<a href=missing.md>x</a>"], 1),
    "quoted-img-src-ok": (
        ["# Target", "", '<img src="assets/ok.svg">'], 0),
    # reference-style: 산문은 링크가 아니다, 꺾쇠는 대상에 포함되지 않는다
    "prose-ref-definition-must-be-ignored": (
        ["# Target", "", "[주의]: 이건 산문이다.", "", "[ok](#target)"], 0),
    "angle-ref-definition-must-resolve": (
        ["# Target", "", "[angle]: <#target>"], 0),
    "broken-ref-definition-must-fail": (
        ["# Target", "", "[broken]: ./assets/missing.svg"], 1),
}


def run_case(lines):
    d = tempfile.mkdtemp(prefix="link-fixture.")
    open(os.path.join(d, "gjc-profiles.yml"), "w").close()
    os.makedirs(os.path.join(d, "assets"), exist_ok=True)
    open(os.path.join(d, "assets", "ok.svg"), "w").close()
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    proc = subprocess.run([sys.executable, CHECKER, "--root", d, "--all"],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout


def main():
    print("## 링크 게이트 fail-closed 픽스처")
    bad = []
    for name, (lines, want) in sorted(CASES.items()):
        rc, out = run_case(lines)
        if rc == want:
            print("ok   [%s] exit %d" % (name, rc))
        else:
            bad.append(name)
            print("FAIL [%s] exit %d, 기대 %d" % (name, rc, want))
            for line in out.strip().split("\n"):
                print("       " + line)
    print()
    if bad:
        print("FAILED — 링크 게이트가 기대대로 동작하지 않는다: %s" % ", ".join(bad))
        return 1
    print("OK — 픽스처 %d종 전부 기대대로 동작한다" % len(CASES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
