#!/usr/bin/env python3
"""The forge. Reads profile.yml at the repo root, rebuilds every plate,
the serpent, and README.md. Run from anywhere:  python3 forge/build.py
Requires: fonttools, pyyaml  (pip install fonttools pyyaml)
"""
import os
import sys
import random

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from glyphs import load, glyph_path  # noqa: E402
import gen_serpent  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "profile.yml"), encoding="utf-8"))
AST = os.path.join(ROOT, "assets")
os.makedirs(AST, exist_ok=True)

P = CFG.get("palette", {})
INK = P.get("ink", "#0B0A0C")
INK_HI = P.get("ink_hi", "#131117")
BONE = P.get("bone", "#EAE4D6")
BONE_SH = P.get("bone_shade", "#B9B19E")
RED = P.get("red", "#C1272D")
ENG = P.get("etch", "#6E675C")
CAP = 700.0

cinzel = load(os.path.join(HERE, "fonts", "Cinzel.ttf"), 700)
mono5 = load(os.path.join(HERE, "fonts", "JetBrainsMono.ttf"), 500)
mono7 = load(os.path.join(HERE, "fonts", "JetBrainsMono.ttf"), 700)

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def measure(font, text, size, tracking=0.0):
    sc = size / CAP
    cmap, gs = font.getBestCmap(), font.getGlyphSet()
    x = 0.0
    for ch in text:
        g = cmap.get(ord(ch))
        x += (gs[g].width * sc if g else size * 0.5) + tracking
    return x - (tracking if text else 0)


def glyphs_of(font, text, size, tracking=0.0, x0=0.0):
    sc = size / CAP
    cmap, gs = font.getBestCmap(), font.getGlyphSet()
    parts, x = [], x0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            x += size * 0.5
            continue
        adv = gs[g].width * sc
        try:
            d, _, _ = glyph_path(font, ch, scale=sc, dx=x, dy=0)
            if d.strip():
                parts.append(d)
        except Exception:
            pass
        x += adv + tracking
    return parts, x - tracking


def fu(inner, delay=0.0):
    return f'<g class="fu" style="animation-delay:{delay:.2f}s">{inner}</g>'


def text_at(font, text, size, x, y, fill, tracking=0.0, anchor="start",
            max_w=None, delay=None, stagger=None):
    w = measure(font, text, size, tracking)
    if max_w and w > max_w:
        f = max_w / w
        size, tracking = size * f, tracking * f
        w = measure(font, text, size, tracking)
    dx = x - (w / 2 if anchor == "mid" else w if anchor == "end" else 0)
    parts, _ = glyphs_of(font, text, size, tracking, dx)
    if stagger is not None:
        inner = "".join(fu(f'<path d="{p}"/>', (delay or 0) + i * stagger)
                        for i, p in enumerate(parts))
    else:
        inner = "".join(f'<path d="{p}"/>' for p in parts)
        if delay is not None:
            inner = fu(inner, delay)
    return f'<g fill="{fill}" transform="translate(0,{y:.1f})">{inner}</g>', w, parts, dx


def parse_bold(line):
    """'plain **bold** plain' -> [(text, is_bold), ...]"""
    out, bold = [], False
    for chunk in line.split("**"):
        if chunk:
            out.append((chunk, bold))
        bold = not bold
    return out


def seg_line(line, x, y, size, delay=None):
    out, cx = "", x
    for text, bold in parse_bold(line):
        font = mono7 if bold else mono5
        fill = BONE if bold else BONE_SH
        parts, cx2 = glyphs_of(font, text, size, 0.0, cx)
        out += f'<g fill="{fill}">' + "".join(f'<path d="{p}"/>' for p in parts) + "</g>"
        cx = cx2
    core = fu(out, delay) if delay is not None else out
    return f'<g transform="translate(0,{y:.1f})">{core}</g>'


def sigil_inner():
    raw = open(os.path.join(HERE, "mark.svg"), encoding="utf-8").read()
    inner = raw.split(">", 1)[1].rsplit("</svg>", 1)[0]
    if "-->" in inner:
        inner = inner.split("-->", 1)[1]
    ground = ('<g inkscape:groupmode="layer" inkscape:label="ground" id="ground">'
              '<rect width="1000" height="1000" fill="url(#vig)"/></g>')
    return inner.replace(ground, "")


ANIM = (
    '<style>'
    '@keyframes ember{0%,100%{opacity:.9}50%{opacity:.2}}'
    '@keyframes fu{from{opacity:0;transform:translateY(9px)}}'
    '@keyframes rl{from{stroke-dashoffset:1}}'
    '@keyframes gb{from{transform:scaleY(0)}}'
    '@keyframes gl{0%{transform:none}12%{transform:translateX(1200px)}'
    '100%{transform:translateX(1200px)}}'
    '@keyframes beat{0%,100%{opacity:1}50%{opacity:.5}}'
    '@keyframes rise{0%{transform:translateY(0);opacity:0}'
    '14%{opacity:.5}70%{opacity:.28}100%{transform:translateY(-210px);opacity:0}}'
    '@keyframes spark{0%{transform:none}100%{transform:translateX(1300px)}}'
    '.fu{animation:fu .65s cubic-bezier(.2,.7,.2,1) both}'
    '.rl{stroke-dasharray:1;stroke-dashoffset:0;animation:rl .85s ease-out both}'
    '.mote{animation:rise var(--d) linear var(--o) infinite;opacity:0}'
    '#ember{animation:ember 3.6s ease-in-out infinite}'
    '#glint{animation:gl 6s ease-in-out 1.4s infinite}'
    '@media(prefers-reduced-motion:reduce){*{animation:none!important}}'
    '</style>')

SPG = ('<linearGradient id="spg" x1="0" y1="0" x2="1" y2="0">'
       f'<stop offset="0" stop-color="{BONE}" stop-opacity="0"/>'
       f'<stop offset="0.5" stop-color="{BONE}" stop-opacity="0.8"/>'
       f'<stop offset="1" stop-color="{BONE}" stop-opacity="0"/></linearGradient>')
EMBERG = (f'<radialGradient id="emberg" cx="0.5" cy="0.5" r="0.5">'
          f'<stop offset="0" stop-color="{RED}" stop-opacity="0.42"/>'
          f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>')


def plate(name, w, h, body, extra_defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
           f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{ANIM}'
           f'<defs><radialGradient id="bnvig" cx="0.5" cy="0.42" r="0.95">'
           f'<stop offset="0" stop-color="{INK_HI}"/>'
           f'<stop offset="1" stop-color="{INK}"/></radialGradient>'
           f'{SPG}{EMBERG}{extra_defs}</defs>'
           f'<rect width="{w}" height="{h}" fill="url(#bnvig)"/>{body}</svg>')
    open(os.path.join(AST, f"{name}.svg"), "w", encoding="utf-8").write(svg)


def diamond(x, y, r, fill=RED):
    return (f'<path d="M{x},{y-r} L{x+r*1.28:.1f},{y} L{x},{y+r} '
            f'L{x-r*1.28:.1f},{y} Z" fill="{fill}"/>')


def motes(zone_x, zone_w, base_y, n, seed):
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        x = zone_x + rnd.random() * zone_w
        s = 2.0 + rnd.random() * 2.6
        dur = 8 + rnd.random() * 7
        dly = -rnd.random() * dur
        col = RED if rnd.random() < 0.45 else BONE_SH
        cap = 0.5 if col == RED else 0.32
        out += (f'<path class="mote" style="--d:{dur:.1f}s;--o:{dly:.1f}s" '
                f'd="M{x:.0f},{base_y - s:.0f} L{x + s:.1f},{base_y:.0f} '
                f'L{x:.0f},{base_y + s:.0f} L{x - s:.1f},{base_y:.0f} Z" '
                f'fill="{col}" fill-opacity="{cap}"/>')
    return out


def rule_spark(x0, x1, y, delay=0.0, dur=6.5):
    cid = f"rc{int(x0)}{int(y)}{int(delay*10)}"
    return (f'<clipPath id="{cid}"><rect x="{x0}" y="{y-3}" '
            f'width="{x1-x0}" height="6"/></clipPath>'
            f'<g clip-path="url(#{cid})">'
            f'<rect x="{x0-70:.0f}" y="{y-1.4:.1f}" width="46" height="2.8" '
            f'fill="url(#spg)" style="animation:spark {dur}s linear {delay}s infinite"/></g>')


def banner():
    c = CFG["banner"]
    mark = f'<g transform="translate(60,30) scale(0.24)">{fu(sigil_inner(), 0.05)}</g>'
    glg = ('<linearGradient id="glg" x1="0" y1="0" x2="1" y2="0">'
           '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
           '<stop offset="0.5" stop-color="#fff" stop-opacity="0.32"/>'
           '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    ember = '<circle id="ember" cx="209.3" cy="90.5" r="26" fill="url(#emberg)"/>'
    name_g, nw, nparts, ndx = text_at(cinzel, c["name"].upper(), 74, 348, 158, BONE,
                                      6, max_w=800, delay=0.22, stagger=0.022)
    mask = ('<mask id="nm" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" '
            'height="300"><g fill="#fff" transform="translate(0,158)">'
            + "".join(f'<path d="{p}"/>' for p in nparts) + '</g></mask>')
    glint = ('<g mask="url(#nm)"><g transform="skewX(-18)">'
             '<rect id="glint" x="200" y="60" width="150" height="130" '
             'fill="url(#glg)"/></g></g>')
    rule = (f'<path pathLength="1" d="M350,192 L404,192" stroke="{RED}" '
            f'stroke-width="4" style="stroke-dasharray:1;animation:'
            f'rl .85s ease-out .5s both, beat 3.4s ease-in-out 1.6s infinite"/>')
    sub, _, _, _ = text_at(mono7, c["tagline"].upper(), 21, 420, 200,
                           BONE_SH, 4.4, max_w=724, delay=0.6)
    m = motes(48, 270, 294, 7, seed=12)
    plate("banner", 1200, 300, m + mark + ember + name_g + mask + glint + rule + sub, glg)


def intro():
    lines = CFG["intro"]["lines"]
    y, lh, size = 58, 37, 20
    b = ""
    for i, line in enumerate(lines):
        b += seg_line(line, 48, y, size, delay=0.05 + i * 0.1)
        y += lh
    y += 12
    t, _, _, _ = text_at(mono5, CFG["intro"]["eyebrow"].upper(), 16, 48, y, ENG,
                         2.4, delay=0.05 + len(lines) * 0.1)
    plate("intro", 1200, y + 28, motes(980, 190, y + 22, 3, seed=31) + b + t)


def header(name, title, seed):
    b = fu(diamond(50, 36, 7), 0.05)
    t, w, _, _ = text_at(cinzel, title.upper(), 27, 76, 45, BONE, 8, delay=0.12)
    b += t
    rx = 76 + w + 26
    b += (f'<path class="rl" pathLength="1" d="M{rx:.0f},36 L1152,36" '
          f'stroke="{BONE_SH}" stroke-width="1.4" opacity="0.32" '
          f'style="animation-delay:.25s"/>')
    b += rule_spark(rx, 1152, 36, delay=seed * 1.3)
    plate(name, 1200, 72, b)


def cards():
    cs = CFG["cards"]
    df = min(1.0, min(1000 / measure(mono5, c["desc"], 17, 0.8) for c in cs))
    kf = min(1.0, min(1000 / measure(mono5, " · ".join(c["tech"]).upper(), 14, 2.6)
                      for c in cs))
    for i, c in enumerate(cs):
        base = 0.05 + i * 0.15
        H = 148
        b = (f'<rect x="0" y="0" width="5" height="{H}" fill="{RED}" '
             f'style="transform-box:fill-box;transform-origin:50% 0;animation:'
             f'gb .6s ease-out {base:.2f}s both, beat 5.2s ease-in-out '
             f'{base+1:.2f}s infinite"/>')
        ix, _, _, _ = text_at(cinzel, ROMAN[i], 30, 82, 88, ENG, 2,
                              anchor="mid", delay=base + 0.08)
        t, _, _, _ = text_at(mono7, c["title"].upper(), 24, 138, 56, BONE, 2.4,
                             max_w=1000, delay=base + 0.1)
        d, _, _, _ = text_at(mono5, c["desc"], 17 * df, 138, 92, BONE_SH,
                             0.8 * df, delay=base + 0.18)
        k, _, _, _ = text_at(mono5, " · ".join(c["tech"]).upper(), 14 * kf, 138,
                             124, ENG, 2.6 * kf, delay=base + 0.26)
        m = motes(1020, 150, 142, 2, seed=100 + i)
        plate(f"card-{i+1}", 1200, H, m + b + ix + t + d + k)


def stack():
    rows = [(r["label"], " · ".join(r["items"]).upper()) for r in CFG["stack"]]
    f = min(1.0, min(938 / measure(mono7, v, 20, 2.6) for _, v in rows))
    size, track = 20 * f, 2.6 * f
    b, y, d = "", 52, 0.05
    for label, val in rows:
        lg, _, _, _ = text_at(mono5, label.upper(), 17, 48, y, ENG, 5, delay=d)
        vg, _, _, _ = text_at(mono7, val, size, 218, y, BONE, track, delay=d + 0.07)
        b += lg + vg
        y += 46
        d += 0.13
    plate("stack", 1200, y + 30, motes(1050, 120, y + 24, 3, seed=44) + b)


def chips():
    for i, l in enumerate(CFG["links"]):
        pad, size, track = 24, 15, 3
        label = l["label"].upper()
        w = measure(mono7, label, size, track)
        W = int(pad + 16 + w + pad)
        inner = (f'<rect x="1" y="1" width="{W-2}" height="50" fill="none" '
                 f'stroke="{BONE_SH}" stroke-width="1.2" opacity="0.4"/>'
                 f'<g style="animation:beat 3.8s ease-in-out {i*0.9:.1f}s infinite">'
                 f'{diamond(pad + 2, 26, 5)}</g>')
        t, _, _, _ = text_at(mono7, label, size, pad + 16, 31, BONE, track)
        plate(f"chip-{i+1}", W, 52, fu(inner + t, 0.1))


def footer():
    W, H = 1200, 178
    y = 22
    b = (f'<path class="rl" pathLength="1" d="M{W/2-26},{y} L28,{y}" '
         f'stroke="{BONE_SH}" stroke-width="1.4" opacity="0.42" '
         f'style="animation-delay:.1s"/>'
         f'<path class="rl" pathLength="1" d="M{W/2+26},{y} L{W-28},{y}" '
         f'stroke="{BONE_SH}" stroke-width="1.4" opacity="0.42" '
         f'style="animation-delay:.1s"/>')
    b += rule_spark(int(W/2+26), W-28, y, delay=0.4)
    b += f'<g style="animation:beat 3.4s ease-in-out infinite">{diamond(W/2, y, 7)}</g>'
    sec = CFG.get("secret", {})
    left, right = sec.get("left", ""), sec.get("right", "")
    if left:
        xii, _, _, _ = text_at(mono5, left, 10, W/2 - 74, y + 3.5, ENG, 1.5,
                               anchor="end", delay=1.2)
        b += xii
    if right:
        iv, _, _, _ = text_at(mono5, right, 10, W/2 + 74, y + 3.5, ENG, 1.5, delay=1.2)
        b += iv
    b += (f'<g transform="translate({W/2 - 42},46) scale(0.084)">'
          f'{fu(sigil_inner(), 0.2)}</g>')
    b += (f'<circle id="ember" cx="{W/2 + 10.3:.1f}" cy="67.1" r="11" '
          f'fill="url(#emberg)"/>')
    t, _, _, _ = text_at(mono5, CFG["footer_tagline"].upper(), 12, W / 2, 160, ENG,
                         6, anchor="mid", delay=0.55)
    plate("footer", W, H, motes(W/2-120, 240, H-4, 5, seed=7) + b + t)


def readme():
    g = CFG["github_user"]
    L = ['<div align="center">',
         f'  <img src="./assets/banner.svg" width="100%" alt="{CFG["banner"]["name"]} — {CFG["banner"]["tagline"]}" />',
         '  <img src="./assets/intro.svg" width="100%" alt="Intro" />',
         '  <img src="./assets/h-1.svg" width="100%" alt="Selected work" />']
    for i, c in enumerate(CFG["cards"]):
        img = f'<img src="./assets/card-{i+1}.svg" width="100%" alt="{c["title"]} — {c["desc"]}" />'
        L.append(f'  <a href="{c["link"]}">{img}</a>' if c.get("link") else f'  {img}')
    L += [f'  <img src="./assets/h-2.svg" width="100%" alt="{CFG["serpent_title"]}" />',
          '  <img src="./assets/serpent.svg" width="100%" alt="Contribution calendar, consumed daily by the serpent." />',
          '  <img src="./assets/h-3.svg" width="100%" alt="Stack" />',
          '  <img src="./assets/stack.svg" width="100%" alt="Stack" />',
          '  <img src="./assets/h-4.svg" width="100%" alt="Elsewhere" />',
          '  <p>']
    for i, l in enumerate(CFG["links"]):
        L.append(f'    <a href="{l["url"]}"><img src="./assets/chip-{i+1}.svg" '
                 f'height="52" alt="{l["label"]}" /></a>&nbsp;')
    L += ['  </p>',
          '  <img src="./assets/footer.svg" width="100%" alt="Footer" />',
          '</div>', '']
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(L))


def main():
    banner()
    intro()
    header("h-1", CFG.get("work_title", "Selected work"), 0)
    header("h-2", CFG.get("serpent_title", "The year, consumed"), 1)
    header("h-3", "Stack", 2)
    header("h-4", "Elsewhere", 3)
    cards()
    stack()
    chips()
    footer()
    try:
        gen_serpent.generate(CFG["github_user"],
                             os.path.join(AST, "serpent.svg"))
        print("serpent: fed")
    except Exception as e:
        print(f"serpent: skipped ({e})")
    readme()
    print("forge complete:", sorted(os.listdir(AST)))


if __name__ == "__main__":
    main()
