#!/usr/bin/env python3
"""`install.sh` 의 config.yml 편집 블록이 **유효한 YAML 만 쓰는지** 픽스처로 증명한다.

왜 필요한가
-----------
2026-08-19 실사용자 실측: `install.sh` 가 `config.yml` 을 파싱 불가로 만들어
**GJC 가 기동조차 못 했다.**

    StartupAuthConfigError: Startup auth config ~/.gjc/agent/config.yml: invalid-yaml.

원인은 `modelProfile` 의 형태 가정이었다. GJC 는 비어 있을 때 이렇게 쓴다:

    modelProfile:
      {}

편집기는 블록 매핑만 가정하고 `  default: daily` 를 끼워 넣어 `  {}` 를 남겼다.
설치 스크립트는 **자기가 쓴 파일을 한 번도 파싱해보지 않았다.**

이 픽스처는 install.sh 안의 실제 블록을 그대로 떼어내 돌린다 — 사본을 따로 두면
스크립트가 바뀌었을 때 같이 안 바뀌므로 의미가 없다.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTALL = os.path.join(os.path.dirname(HERE), "install.sh")

# (이름) -> (기존 config.yml, 기대 modelProfile)
CASES = {
    "empty-flow-mapping-on-next-line":
        ("modelProfile: \n  {}\nnotifications: \n  enabled: true\n", {"default": "daily"}),
    "inline-empty-flow-mapping":
        ("modelProfile: {}\nnotifications: \n  enabled: true\n", {"default": "daily"}),
    "explicit-null":
        ("modelProfile: null\nnotifications: \n  enabled: true\n", {"default": "daily"}),
    "tilde-null":
        ("modelProfile: ~\nnotifications: \n  enabled: true\n", {"default": "daily"}),
    "existing-default-is-replaced":
        ("modelProfile: \n  default: old\nnotifications: \n  enabled: true\n", {"default": "daily"}),
    "sibling-keys-survive":
        ("modelProfile: \n  default: old\n  pinned: keepme\nnotifications: \n  enabled: true\n",
         {"default": "daily", "pinned": "keepme"}),
    "key-absent":
        ("notifications: \n  enabled: true\n", {"default": "daily"}),
    "empty-file":
        ("", {"default": "daily"}),
}


def extract_block():
    """install.sh 에서 set-default-profile heredoc 본문을 떼어낸다."""
    src = open(INSTALL, encoding="utf-8").read().split("\n")
    start = next((i for i, l in enumerate(src) if "BEGIN set-default-profile" in l), None)
    if start is None:
        sys.exit("FAILED — install.sh 에서 'BEGIN set-default-profile' 표지를 찾지 못했다")
    end = next((i for i in range(start + 1, len(src)) if src[i].strip() == "PY"), None)
    if end is None:
        sys.exit("FAILED — heredoc 종료 표지(PY)를 찾지 못했다")
    return "\n".join(src[start + 1:end])


def main():
    import yaml

    block = extract_block()
    print("## install.sh config.yml 편집 픽스처")
    bad = []
    for name, (before, want) in sorted(CASES.items()):
        with tempfile.TemporaryDirectory(prefix="install-cfg.") as d:
            cfg = os.path.join(d, "config.yml")
            if before:
                with open(cfg, "w", encoding="utf-8") as fh:
                    fh.write(before)
            script = os.path.join(d, "block.py")
            with open(script, "w", encoding="utf-8") as fh:
                fh.write(block)
            proc = subprocess.run([sys.executable, script, cfg, "daily"],
                                  capture_output=True, text=True)
            after = open(cfg, encoding="utf-8").read() if os.path.exists(cfg) else ""
            try:
                parsed = yaml.safe_load(after) or {}
                got = parsed.get("modelProfile")
            except Exception as exc:
                bad.append(name)
                print("FAIL [%s] config.yml 이 깨졌다 — %s"
                      % (name, str(exc).splitlines()[0]))
                for l in after.split("\n")[:6]:
                    print("       |%s" % l)
                continue
            # 중복 키는 safe_load 가 조용히 삼키므로 원문에서 직접 센다
            dupes = len(re.findall(r"(?m)^modelProfile\s*:", after))
            if got != want:
                bad.append(name)
                print("FAIL [%s] modelProfile=%r, 기대 %r" % (name, got, want))
                if proc.stderr.strip():
                    print("       stderr: %s" % proc.stderr.strip().splitlines()[0])
            elif dupes > 1:
                bad.append(name)
                print("FAIL [%s] modelProfile 키가 %d개 (중복)" % (name, dupes))
            else:
                print("ok   [%s] modelProfile=%r" % (name, got))
    print()
    if bad:
        print("FAILED — install.sh 가 잘못된 config.yml 을 쓴다: %s" % ", ".join(bad))
        return 1
    print("OK — 픽스처 %d종 전부 유효한 config.yml 을 만든다" % len(CASES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
