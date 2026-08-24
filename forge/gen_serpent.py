#!/usr/bin/env python3
"""Generate an animated 'serpent consumes the year' contribution SVG.

Usage: python3 gen_serpent.py <github-username> <output.svg> [local-html]
Self-contained: stdlib only, safe to run inside a GitHub Action.
"""
import re
import sys
import datetime
import urllib.request

INK, INK_HI = "#0B0A0C", "#131117"
BONE, BONE_SH = "#EAE4D6", "#B9B19E"
RED, ENG = "#C1272D", "#6E675C"
EMPTY = "#191820"
LEVEL_OP = {1: 0.30, 2: 0.52, 3: 0.76, 4: 1.0}

CELL, GAP = 11, 3
PITCH = CELL + GAP
T = 32.0  # seconds per full consumption cycle


def fetch(user, local=None):
    if local:
        html = open(local, encoding="utf-8").read()
    else:
        req = urllib.request.Request(
            f"https://github.com/users/{user}/contributions",
            headers={"User-Agent": "serpent-svg"})
        html = urllib.request.urlopen(req, timeout=30).read().decode()
    cells = []
    for m in re.finditer(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?data-level="(\d)"', html):
        cells.append((m.group(1), int(m.group(2))))
    if not cells:  # attribute order can flip
        for m in re.finditer(r'data-level="(\d)"[^>]*?data-date="(\d{4}-\d{2}-\d{2})"', html):
            cells.append((m.group(2), int(m.group(1))))
    if not cells:
        raise SystemExit("could not parse contribution cells")
    return sorted(set(cells))


def layout(cells):
    d0 = datetime.date.fromisoformat(cells[0][0])
    sunday0 = d0 - datetime.timedelta(days=(d0.weekday() + 1) % 7)
    grid = {}
    for iso, lvl in cells:
        d = datetime.date.fromisoformat(iso)
        col = (d - sunday0).days // 7
        row = (d.weekday() + 1) % 7
        grid[(col, row)] = (iso, lvl)
    ncols = max(c for c, _ in grid) + 1
    return grid, ncols


def generate(user, out, local=None):
    grid, ncols = layout(fetch(user, local))
    gw, gh = ncols * PITCH - GAP, 7 * PITCH - GAP
    W = 1200
    gx, gy = (W - gw) / 2, 42
    H = int(gy + gh + 26)

    # serpent path: vertical boustrophedon through every cell centre
    order, pts = [], []
    for c in range(ncols):
        rows = range(7) if c % 2 == 0 else range(6, -1, -1)
        for r in rows:
            order.append((c, r))
            pts.append((gx + c * PITCH + CELL / 2, gy + r * PITCH + CELL / 2))
    N = len(order)
    p0x, p0y = pts[0]
    path_d = "M" + " L".join(f"{x - p0x:.1f},{y - p0y:.1f}" for x, y in pts)

    css = [
        f"@keyframes trav{{to{{offset-distance:100%}}}}",
        f"@keyframes eaten{{0%,2.4%{{opacity:1}}5%{{opacity:.14}}"
        f"80%{{opacity:.14}}92%,100%{{opacity:1}}}}",
        f"@keyframes flash{{0%,2.2%{{opacity:0}}3.4%{{opacity:.95}}"
        f"9%{{opacity:0}}100%{{opacity:0}}}}",
        ".seg{offset-path:path('" + path_d + "');offset-rotate:auto;"
        f"animation:trav {T}s linear infinite}}".replace("}}", "}"),
        "@media(prefers-reduced-motion:reduce){*{animation:none!important}"
        ".seg{display:none}}",
    ]

    body = []
    # month labels
    seen = set()
    for (c, r), (iso, _) in sorted(grid.items()):
        d = datetime.date.fromisoformat(iso)
        if r == 0 and d.day <= 7 and d.month not in seen:
            seen.add(d.month)
            body.append(
                f'<text x="{gx + c * PITCH:.0f}" y="{gy - 14:.0f}" fill="{ENG}" '
                f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" '
                f'font-size="11" letter-spacing="2">{d.strftime("%b").upper()}</text>')

    # cells + flashes
    idx = {cr: i for i, cr in enumerate(order)}
    for (c, r), (iso, lvl) in grid.items():
        x, y = gx + c * PITCH, gy + r * PITCH
        t = idx[(c, r)] / max(N - 1, 1) * T
        if lvl == 0:
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" '
                        f'height="{CELL}" fill="{EMPTY}"/>')
        else:
            body.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" '
                f'fill="{BONE}" fill-opacity="{LEVEL_OP[lvl]}" '
                f'style="animation:eaten {T}s linear {t:.2f}s infinite"/>')
            body.append(
                f'<rect x="{x - 1:.1f}" y="{y - 1:.1f}" width="{CELL + 2}" '
                f'height="{CELL + 2}" fill="{RED}" opacity="0" '
                f'style="animation:flash {T}s linear {t:.2f}s infinite"/>')

    # the serpent: chisel head with red eye + trailing diamond body
    body.append(f'<g transform="translate({p0x:.1f},{p0y:.1f})">')
    for j in range(8, 0, -1):
        s = 2.6 + j * 0.55
        op = 0.28 + j * 0.08
        body.append(
            f'<g class="seg" style="animation-delay:{-j * 0.14:.2f}s">'
            f'<path d="M0,{-s:.1f} L{s * 1.25:.1f},0 L0,{s:.1f} L{-s * 1.25:.1f},0 Z" '
            f'fill="{BONE}" fill-opacity="{op:.2f}"/></g>')
    body.append(
        '<g class="seg">'
        f'<path d="M-7,-6.5 L10,0 L-7,6.5 L-3,0 Z" fill="{BONE}"/>'
        f'<circle cx="1.5" cy="-2" r="1.7" fill="{RED}"/></g></g>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}" role="img" '
           f'aria-label="Contribution calendar for {user}, consumed by a serpent">'
           f'<style>{"".join(css)}</style>'
           f'<defs><radialGradient id="v" cx="0.5" cy="0.4" r="1">'
           f'<stop offset="0" stop-color="{INK_HI}"/>'
           f'<stop offset="1" stop-color="{INK}"/></radialGradient></defs>'
           f'<rect width="{W}" height="{H}" fill="url(#v)"/>'
           + "".join(body) + "</svg>")
    open(out, "w").write(svg)
    print(f"wrote {out}: {N} cells, {ncols} weeks")


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else "TaiyoRay"
    out = sys.argv[2] if len(sys.argv) > 2 else "serpent.svg"
    local = sys.argv[3] if len(sys.argv) > 3 else None
    generate(user, out, local)


if __name__ == "__main__":
    main()
