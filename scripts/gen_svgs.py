#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_svgs.py — GJC 멀티벤더 가이드 SVG 자산 재생성기 (v1.12.0)

assets/ 아래 4개 SVG 를 데이터 기반으로 재생성한다:
  - role-winners.svg     : 👑 legend (Ultimate Legend) 역할별 최강 배너
  - profiles-matrix.svg  : 14 프로필 × 5 역할 매트릭스
  - effort-ladder.svg    : effort 6단계 사다리 + 모델별 클램프 스트립
  - architecture.svg     : 본체 1 + 서브에이전트 4 (본체 라벨 프로필-중립)

routing-tree.svg 는 모델명 하드코딩이 없어 재생성 대상이 아니다 (건드리지 말 것).

사용법:
  python3 scripts/gen_svgs.py            # repo 루트 기준 assets/ 에 출력
  python3 scripts/gen_svgs.py --out DIR  # 다른 디렉터리에 출력

데이터 원천: gjc-profiles.yml (v1.12.0, 14 프로필). 프로필이 바뀌면
아래 PROFILES 테이블을 yml 과 동기화한 뒤 재실행한다.
검증 스탬프 날짜는 VERIFY_DATE 하나만 고치면 된다.
"""

import argparse
import os
import re

VERIFY_DATE = "2026-07-10"
GJC_VERSION = "0.9.5"

FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"

# ── 벤더 팔레트 ──────────────────────────────────────────────────────────────
# (fill, accent, dark-text)
VENDORS = {
    "anthropic": ("#FBE9E4", "#D9583E", "#8A2B1A"),   # coral/red
    "openai":    ("#E3F4EE", "#10A37F", "#0A6B53"),   # green
    "google":    ("#E8F0FE", "#4285F4", "#1A56C4"),   # blue
    "xai":       ("#EEF1F5", "#475569", "#2D3A4D"),   # dark slate
    "opencode":  ("#DFF3F4", "#0E7490", "#155E63"),   # teal
}
VENDOR_LABELS = [
    ("anthropic", "Anthropic"),
    ("openai", "OpenAI"),
    ("google", "Google"),
    ("xai", "xAI"),
    ("opencode", "opencode-go"),
]

ROLES = ["🎛 default", "🔨 executor", "🧠 planner", "🔭 architect", "⚖ critic"]

# ── 프로필 데이터 (gjc-profiles.yml v1.10.0 와 1:1 동기화) ─────────────────────
# 셀 = (vendor, model_display, effort_display)  — effort_display None 이면 생략.
# Gemini 셀렉터 gemini-3.1-pro-low:high 는 모델 'Gemini 3.1 Pro-low' + effort ':high'
# 로 분리 표기한다 (과거 'low:high' 병합 오표기 금지).
A, O, G, X, C = "anthropic", "openai", "google", "xai", "opencode"
GEM_HI = (G, "Gemini 3.1 Pro-low", ":high")

PROFILES = [
    ("⭐ daily", "평소 기본", [
        (A, "Opus 4.8", ":medium"), (O, "GPT-5.6 Terra", ":high"),
        GEM_HI, GEM_HI, (X, "Grok 4.5", ":medium")]),
    ("🏆 ultimate", None, [
        (A, "Opus 4.8", ":high"), (A, "Opus 4.8", ":max"),
        (O, "GPT-5.6 Sol", ":xhigh"), GEM_HI, (X, "Grok 4.5", ":high")]),
    ("🔥 ultimate-f5", "⚡ ~7/12 이벤트", [
        (A, "Fable 5", ":high"), (A, "Fable 5", ":xhigh"),
        (O, "GPT-5.6 Sol", ":xhigh"), GEM_HI, (X, "Grok 4.5", ":high")]),
    ("👑 legend", "Ultimate Legend", [
        (A, "Fable 5", ":high"), (A, "Opus 4.8", ":max"),
        (O, "GPT-5.6 Sol", ":xhigh"), GEM_HI, (X, "Grok 4.5", ":high")]),
    ("🌞 ultimate-sol", "투트랙 B (실험적)", [
        (O, "GPT-5.6 Sol", ":high"), (O, "GPT-5.6 Sol", ":xhigh"),
        (A, "Fable 5", ":xhigh"), (A, "Opus 4.8", ":high"),
        (X, "Grok 4.5", ":high")]),
    ("🏎 coding-sprint", None, [
        (A, "Opus 4.8", ":medium"), (A, "Opus 4.8", ":max"),
        GEM_HI, GEM_HI, (O, "GPT-5.6 Terra", ":high")]),
    ("🛡 escalation", "구원투수=Fable", [
        (A, "Opus 4.8", ":high"), (A, "Fable 5", ":xhigh"),
        (O, "GPT-5.6 Sol", ":xhigh"), GEM_HI, (X, "Grok 4.5", ":high")]),
    ("🚨 cyber-cop", "reviewer 모드", [
        (A, "Opus 4.8", ":high"), (O, "GPT-5.6 Sol", ":high"),
        GEM_HI, (A, "Opus 4.8", ":high"), (O, "GPT-5.6 Sol", ":high")]),
    ("💸 eco", None, [
        (A, "Opus 4.8", ":low"), (C, "DeepSeek V4 Flash", None),
        (X, "Grok 4.1 Fast", ":high"),
        (G, "Gemini 3.1 Pro-low", "-low (저effort)"),
        (G, "Gemini 3.5 Flash-low", None)]),
    ("🗺 monorepo", None, [
        (A, "Opus 4.8", ":medium"), (A, "Opus 4.8", ":high"),
        GEM_HI, (A, "Opus 4.8", ":high"), (C, "GLM-5.2", None)]),
    ("🧱 solo-anthropic", "전 역할 Opus", [
        (A, "Opus 4.8", ":high"), (A, "Opus 4.8", ":max"),
        (A, "Opus 4.8", ":max"), (A, "Opus 4.8", ":high"),
        (A, "Opus 4.8", ":high")]),
    ("🤖 solo-openai", None, [
        (O, "GPT-5.6 Sol", ":high"), (O, "GPT-5.6 Sol", ":xhigh"),
        (O, "GPT-5.6 Sol", ":xhigh"), (O, "GPT-5.4", ":high"),
        (O, "GPT-5.6 Terra", ":high")]),
    ("🤝 claude-codex", None, [
        (A, "Opus 4.8", ":medium"), (A, "Opus 4.8", ":high"),
        (O, "GPT-5.6 Sol", ":high"), (A, "Opus 4.8", ":high"),
        (O, "GPT-5.6 Terra", ":high")]),
    ("🥇 claude-codex-max", None, [
        (A, "Opus 4.8", ":high"), (A, "Opus 4.8", ":max"),
        (O, "GPT-5.6 Sol", ":xhigh"), (A, "Opus 4.8", ":high"),
        (O, "GPT-5.6 Sol", ":high")]),
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def svg_open(w, h, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{FONT}" role="img">\n'
        f'<title>{esc(title)}</title>\n'
        f'<rect width="{w}" height="{h}" rx="18" fill="#ffffff"/>'
        f'<rect width="{w}" height="{h}" rx="18" fill="none" stroke="#ECECF1"/>\n'
    )


ARROW_DEF = ('<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="6.5" '
             'refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#9AA0AE"/>'
             '</marker></defs>\n')


# ═════════════════════════════════════════════════════════════════════════════
# 1. role-winners.svg — 👑 legend (Ultimate Legend) 배너
# ═════════════════════════════════════════════════════════════════════════════
def gen_role_winners():
    W, H = 1256, 268
    cards = [
        # (role, role_desc, vendor, model, effort, rationale)
        ("🎛 default", "오케스트레이션·툴 신뢰성", A, "Claude Fable 5", ":high",
         "Anthropic · 라우터=품질 상한"),
        ("🔨 executor", "실코딩", A, "Claude Opus 4.8", ":max",
         "Anthropic · 구독 포함 코딩 최강"),
        ("🧠 planner", "최상위 추론·설계", O, "GPT-5.6 Sol", ":xhigh",
         "OpenAI · 5.6 플래그십 추론"),
        ("🔭 architect", "멀티모달·1M ctx 리뷰", G, "Gemini 3.1 Pro-low", ":high",
         "Google · MMMU 81% 검증 우위"),
        ("⚖ critic", "독립 적대 비평", X, "Grok 4.5", ":high",
         "xAI · cross-family(vs Anthropic)"),
    ]
    s = svg_open(W, H, "👑 legend (Ultimate Legend) 셋업 — 역할별 최강 모델")
    s += (f'<text x="24" y="44" font-size="22" font-weight="700" fill="#1A1A28">'
          f'👑 legend (Ultimate Legend) 셋업 — 역할별 최강 모델</text>\n')
    s += ('<text x="24" y="70" font-size="13" fill="#6B6B7B">한 벤더가 모든 역할에서 '
          '1위는 아니다 — 5역할을 강점별로 4개 벤더에 분산(Anthropic·OpenAI·Google·xAI)'
          '</text>\n')
    cw, ch, gap, y0 = 232, 152, 12, 92
    for i, (role, desc, vendor, model, effort, why) in enumerate(cards):
        fill, accent, dark = VENDORS[vendor]
        x = 24 + i * (cw + gap)
        tx = x + 16
        model_fs = 16 if len(model) <= 15 else 13.5
        s += (f'<rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="14" fill="{fill}"/>'
              f'<rect x="{x}" y="{y0}" width="{cw}" height="6" rx="3" fill="{accent}"/>\n')
        s += (f'<text x="{tx}" y="{y0+32}" font-size="15" font-weight="700" '
              f'fill="{dark}">{esc(role)}</text>\n')
        s += (f'<text x="{tx}" y="{y0+53}" font-size="11.5" fill="#5a5a6a">'
              f'{esc(desc)}</text>\n')
        s += (f'<text x="{tx}" y="{y0+84}" font-size="{model_fs}" font-weight="800" '
              f'fill="#1A1A28">{esc(model)}</text>\n')
        s += (f'<text x="{tx}" y="{y0+106}" font-size="12.5" font-weight="700" '
              f'fill="{accent}">{esc(effort)}</text>\n')
        s += (f'<text x="{tx}" y="{y0+130}" font-size="10.8" fill="{dark}" '
              f'opacity="0.85">{esc(why)}</text>\n')
    s += "</svg>"
    return s


# ═════════════════════════════════════════════════════════════════════════════
# 2. profiles-matrix.svg — 12 프로필 × 5 역할
# ═════════════════════════════════════════════════════════════════════════════
def gen_profiles_matrix():
    n = len(PROFILES)
    W = 1088
    row_h, row_gap = 58, 8
    rows_y0 = 172
    footer_y = rows_y0 + n * (row_h + row_gap) + 28
    H = footer_y + 42
    title = f"GJC 멀티벤더 — {n} 프로필 × 5 역할 매트릭스"
    s = svg_open(W, H, title)
    s += (f'<text x="24" y="46" font-size="22" font-weight="700" fill="#1A1A28">'
          f'GJC 멀티벤더 — {n} 프로필 × 5 역할</text>\n')
    s += (f'<text x="24" y="72" font-size="13" fill="#6B6B7B">행=프로필 · 열=역할 · '
          f'색=벤더 · 07-10 rerun: 전 프로바이더 그린(gpt-5.6 3종 신규 검증 · Anthropic rate-limit 해제)</text>\n')
    # 벤더 범례 (헤더 행과 분리 — 자체 라인 + 구분선)
    lx = 24
    for key, label in VENDOR_LABELS:
        fill, accent, _ = VENDORS[key]
        s += (f'<rect x="{lx}" y="90" width="14" height="14" rx="3" fill="{fill}" '
              f'stroke="{accent}"/>\n')
        s += f'<text x="{lx+20}" y="102" font-size="12" fill="#444">{esc(label)}</text>\n'
        lx += 20 + 7 * len(label) + 26
    s += f'<line x1="24" y1="118" x2="{W-24}" y2="118" stroke="#F0F0F4"/>\n'
    # 역할 헤더 (범례와 별도 행)
    col_x = [188, 364, 540, 716, 892]
    cell_w = 168
    for cx, role in zip(col_x, ROLES):
        s += (f'<text x="{cx + cell_w//2}" y="148" font-size="13" font-weight="600" '
              f'fill="#33334a" text-anchor="middle">{esc(role)}</text>\n')
    # 행
    for r, (name, sub, cells) in enumerate(PROFILES):
        y = rows_y0 + r * (row_h + row_gap)
        band = "#FFFFFF" if r % 2 == 0 else "#FAFAFC"
        s += f'<rect x="24" y="{y}" width="{W-48}" height="{row_h}" rx="10" fill="{band}"/>\n'
        name_y = y + 27 if sub else y + 33
        s += (f'<text x="34" y="{name_y}" font-size="13.5" font-weight="700" '
              f'fill="#1A1A28">{esc(name)}</text>\n')
        if sub:
            s += (f'<text x="34" y="{y+45}" font-size="10.5" fill="#D9583E" '
                  f'font-weight="600">{esc(sub)}</text>\n')
        for cx, (vendor, model, effort) in zip(col_x, cells):
            fill, accent, dark = VENDORS[vendor]
            cy = y + 5
            s += (f'<rect x="{cx}" y="{cy}" width="{cell_w}" height="48" rx="8" '
                  f'fill="{fill}"/>'
                  f'<rect x="{cx}" y="{cy}" width="4.5" height="48" rx="2" '
                  f'fill="{accent}"/>\n')
            fs = 12.5 if len(model) <= 12 else (11 if len(model) <= 17 else 10.2)
            my = cy + 22 if effort else cy + 29
            s += (f'<text x="{cx+14}" y="{my}" font-size="{fs}" font-weight="700" '
                  f'fill="{dark}">{esc(model)}</text>\n')
            if effort:
                s += (f'<text x="{cx+14}" y="{cy+39}" font-size="10.5" fill="{dark}" '
                      f'opacity="0.8">{esc(effort)}</text>\n')
    # 푸터
    s += (f'<text x="24" y="{footer_y}" font-size="11.5" fill="#6B6B7B">불변식: '
          f'멀티벤더 프로필 default = Anthropic 플래그십(Opus/Fable) 고정 · '
          f'critic = 본체와 다른 벤더 · solo-* 는 단일 벤더 최강(독립성 트레이드오프)'
          f'</text>\n')
    s += (f'<text x="24" y="{footer_y+20}" font-size="11.5" fill="#6B6B7B">'
          f'엔진 effort 하드룰 합법 · ⚡ ultimate-f5 = Fable 5 구독 포함 이벤트'
          f'(7/12 23:59 PT 종료 — 7/7→7/12 연장, 이후 usage credits $10/$50) · gjc {GJC_VERSION}</text>\n')
    s += "</svg>"
    return s


# ═════════════════════════════════════════════════════════════════════════════
# 3. effort-ladder.svg — 6단계 사다리 + 모델별 클램프 스트립
# ═════════════════════════════════════════════════════════════════════════════
def gen_effort_ladder():
    W, H = 1150, 420
    levels = [
        # (label, note, fill, text_color, banned)
        (":minimal", "사용 금지(-23점)", "#F4F4F6", "#9AA0AE", True),
        (":low", "평소 시작", "#FDECE7", "#8A2B1A", False),
        (":medium", "효율 knee", "#FAD9CE", "#8A2B1A", False),
        (":high", "막히면", "#F6C9BC", "#8A2B1A", False),
        (":xhigh", "계속 실패", "#EC9A85", "#5A1A0E", False),
        (":max", "최후", "#D9583E", "#FFFFFF", False),
    ]
    bw, gap, x0 = 150, 34, 40
    bottom = 240
    heights = [56, 76, 96, 116, 140, 164]
    s = svg_open(W, H, "적응형 effort 에스컬레이션 — 6단계 사다리")
    s = s.replace("</title>\n", "</title>\n" + ARROW_DEF, 1)
    s += ('<text x="24" y="42" font-size="18" font-weight="700" fill="#1A1A28">'
          '⚙ 적응형 effort 에스컬레이션 (실패신호 기반) — 사다리 6단계</text>\n')
    xs = []
    for i, (label, note, fill, tc, banned) in enumerate(levels):
        x = x0 + i * (bw + gap)
        xs.append(x)
        h = heights[i]
        y = bottom - h
        dash = ' stroke="#C9CDD6" stroke-dasharray="5 4"' if banned else ""
        s += f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="12" fill="{fill}"{dash}/>\n'
        cx = x + bw / 2
        label_fs = 14 if banned else 16
        s += (f'<text x="{cx}" y="{y+22}" font-size="{label_fs}" font-weight="800" '
              f'fill="{tc}" text-anchor="middle">{esc(("🚫 " if banned else "") + label)}</text>\n')
        s += (f'<text x="{cx}" y="{bottom-12}" font-size="10.5" fill="{tc}" '
              f'text-anchor="middle" opacity="0.9">{esc(note)}</text>\n')
    # 에스컬레이션 화살표 (low 부터 — minimal 은 금지 구간이라 사다리 밖)
    for i in range(1, 5):
        x1 = xs[i] + bw + 3
        x2 = xs[i + 1] - 6
        y1 = bottom - heights[i] + 8
        y2 = bottom - heights[i + 1] + 12
        mx = (x1 + x2) / 2
        s += (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#9AA0AE" '
              f'stroke-width="1.5" marker-end="url(#ah)"/>\n')
        s += (f'<text x="{mx}" y="{y2-24}" font-size="9.5" fill="#7A7F8C" '
              f'text-anchor="middle">실패신호</text>\n')
        s += (f'<text x="{mx}" y="{y2-13}" font-size="9.5" fill="#7A7F8C" '
              f'text-anchor="middle">필요 단계만큼 ↑</text>\n')
    # 모델별 클램프 스트립
    strip_y = 270
    s += (f'<text x="24" y="{strip_y}" font-size="12.5" font-weight="700" '
          f'fill="#33334a">모델별 effort 상한 — GJC {GJC_VERSION} 실효 '
          f'(검증 {VERIFY_DATE})</text>\n')
    chips = [
        "Opus 4.8 = minimal..max",
        "Fable 5 ≤ xhigh (GJC, :max 클램프)",
        "Sonnet 4.6/5 ≤ high",
        "GPT-5.6 3종 = 출하 ≤ xhigh (:max 수용·심도 미검증)",
        "xai Grok 4.5 ≤ high",
        "Gemini Pro = {low, high}",
        "opencode-go = effort 생략",
    ]
    cx = 24
    cy = strip_y + 12
    for chip in chips:
        wpx = int(7.1 * sum(2 if ord(ch) > 0x2E7F else 1 for ch in chip)) + 22
        if cx + wpx > W - 24:          # 우측 잘림 방지 — 다음 줄로 랩
            cx = 24
            cy += 34
        s += (f'<rect x="{cx}" y="{cy}" width="{wpx}" height="26" rx="13" '
              f'fill="#F6F6FA" stroke="#E2E2EA"/>\n')
        s += (f'<text x="{cx + wpx/2}" y="{cy+17}" font-size="11" fill="#3A3A4C" '
              f'text-anchor="middle">{esc(chip)}</text>\n')
        cx += wpx + 12
    # 각주
    s += (f'<text x="24" y="{cy+56}" font-size="12" fill="#1A1A28">✅ 못 풀어서 '
          f'올리는 건 정당 (테스트깨짐·자기모순·critic반려)   ❌ "올리면 안전하겠지"는 '
          f'낭비 — medium→high: +1~2점에 토큰 ~23배</text>\n')
    s += (f'<text x="24" y="{cy+78}" font-size="12" fill="#6B6B7B">🚫 minimal 은 '
          f'품질 급락(-23점) — 실전 저점은 low · 클램프는 침묵 적용(에러 없이 상한으로 '
          f'하향)이라 셀렉터에 상한 초과 effort 를 쓰지 말 것</text>\n')
    s += "</svg>"
    return s


# ═════════════════════════════════════════════════════════════════════════════
# 4. architecture.svg — 본체 라벨 프로필-중립화 (나머지 v1.3 그대로)
# ═════════════════════════════════════════════════════════════════════════════
def gen_architecture():
    W, H = 1000, 472
    s = svg_open(W, H, "강본체 1 + 서브에이전트 4 — 작업신호 위임")
    s = s.replace("</title>\n", "</title>\n" + ARROW_DEF, 1)
    s += ('<text x="32" y="40" font-size="17" font-weight="700" fill="#1A1A28">'
          '본체 1개(default) + 서브에이전트 4 — 신호가 명확할 때만 위임</text>\n')
    s += ('<rect x="425" y="60" width="150" height="38" rx="19" fill="#F4F4F8" '
          'stroke="#D9D9E3"/><text x="500" y="84" font-size="13" font-weight="600" '
          'fill="#33334a" text-anchor="middle">📥 사용자 작업</text>\n')
    s += ('<line x1="500" y1="98" x2="500" y2="122" stroke="#9AA0AE" '
          'stroke-width="1.5" marker-end="url(#ah)"/>\n')
    # 본체 박스 — 프로필-중립 라벨 (v1.4: legend/ultimate-f5 는 Fable 5 default)
    s += '<rect x="320" y="124" width="360" height="90" rx="14" fill="#D9583E"/>\n'
    s += ('<text x="500" y="150" font-size="14.5" font-weight="800" fill="#fff" '
          'text-anchor="middle">🎛 default · 본체</text>\n')
    s += ('<text x="500" y="172" font-size="13" font-weight="700" fill="#fff" '
          'text-anchor="middle">default 프로필의 Anthropic 플래그십</text>\n')
    s += ('<text x="500" y="189" font-size="11.5" font-weight="700" fill="#FFD9CE" '
          'text-anchor="middle">(Opus 4.8 / Fable 5)</text>\n')
    s += ('<text x="500" y="206" font-size="10.5" fill="#FFE7E0" '
          'text-anchor="middle">읽기 · 편집 · 도구호출 · 라우팅</text>\n')
    s += ('<path d="M680 169 C 760 169, 760 110, 690 124" fill="none" '
          'stroke="#C9CDD6" stroke-width="1.3" stroke-dasharray="4 3" '
          'marker-end="url(#ah)"/>\n')
    s += '<text x="772" y="150" font-size="11" fill="#7A7F8C">단순 작업(대부분)</text>\n'
    s += '<text x="772" y="166" font-size="11" fill="#7A7F8C">→ 본체 단독</text>\n'
    agents = [
        (140, 40, "구현", 298, "🔨 executor", "실코딩 (구현)", "#D9583E"),
        (380, 280, "리뷰", 418, "🔭 architect", "대용량 ctx·리뷰", "#4285F4"),
        (620, 520, "설계", 538, "🧠 planner", "최상위 추론·설계", "#4285F4"),
        (860, 760, "검증", 658, "⚖ critic", "독립 적대 비평", "#475569"),
    ]
    for ex, bx, tag, tagx, name, desc, stripe in agents:
        s += (f'<line x1="500" y1="214" x2="{ex}" y2="300" stroke="#9AA0AE" '
              f'stroke-width="1.4" stroke-dasharray="5 3" marker-end="url(#ah)"/>\n')
        s += (f'<rect x="{tagx}" y="246" width="44" height="20" rx="6" fill="#33334a"/>'
              f'<text x="{tagx+22}" y="260" font-size="11" fill="#fff" '
              f'text-anchor="middle">{esc(tag)}</text>\n')
        s += (f'<rect x="{bx}" y="300" width="200" height="104" rx="12" fill="#FBFBFD" '
              f'stroke="#E6E6EE"/><rect x="{bx}" y="300" width="200" height="5" '
              f'rx="2.5" fill="{stripe}"/>\n')
        s += (f'<text x="{bx+18}" y="338" font-size="15" font-weight="700" '
              f'fill="#1A1A28">{esc(name)}</text>\n')
        s += (f'<text x="{bx+18}" y="362" font-size="11.5" fill="#5a5a6a">'
              f'{esc(desc)}</text>\n')
        s += (f'<text x="{bx+18}" y="385" font-size="10.5" fill="#9AA0AE">'
              f'서브에이전트 · fresh-context</text>\n')
    s += ('<text x="500" y="448" font-size="12" fill="#6B6B7B" text-anchor="middle">'
          '서브에이전트는 직렬화된 assignment만 받아 돌고, 결과는 본체(default)로 '
          '반환된다 — 본체가 단일 진실원천.</text>\n')
    s += "</svg>"
    return s


def main():
    ap = argparse.ArgumentParser(description="GJC 가이드 SVG 자산 재생성")
    default_out = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "assets")
    ap.add_argument("--out", default=default_out, help="출력 디렉터리 (기본: assets/)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    outputs = {
        "role-winners.svg": gen_role_winners(),
        "profiles-matrix.svg": gen_profiles_matrix(),
        "effort-ladder.svg": gen_effort_ladder(),
        "architecture.svg": gen_architecture(),
    }
    for name, svg in outputs.items():
        # 안전망: 더블 콜론 회귀 방지 (과거 버그)
        assert "::" not in svg, f"double colon in {name}"
        # 안전망: 병합 오표기 회귀 방지 (effort 라인 'low:high')
        assert not re.search(r'>low:high<', svg), f"merged 'low:high' effort in {name}"
        path = os.path.join(args.out, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg + "\n")
        print(f"wrote {path} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
