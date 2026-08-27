#!/usr/bin/env python3
"""self-scan.svg: sdrtop pointed at its own source tree.

Modules are frequency bins, lines of code are signal strength, and the scale is
in dBc relative to the largest module. Numbers come from `find src -name '*.rs'`.
"""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "self-scan.svg")
random.seed(5003)

BG, PANEL, EDGE = "#1a1b26", "#16161e", "#292e42"
FG, DIM, DIMMER, NOTE = "#c0caf5", "#7c86ab", "#565f89", "#737d9e"
BLUE, CYAN, PURPLE, GREEN, YELLOW, RED, ORANGE = "#7aa2f7", "#7dcfff", "#bb9af7", "#9ece6a", "#e0af68", "#f7768e", "#ff9e64"

W, TITLE_H = 880, 34
PAD, CMD_Y, FS = 36, 70, 13.5
CHW = FS * 0.6
X0, X1 = 76, 636          # plot area
TOP, BOT = 96, 300
HEAD = 22                 # headroom above 0 dBc
DB_FLOOR = -20.0
PX, PW = 656, 196         # readout panel

MODULES = [
    ("ui",       21987, 335, 96),
    ("signal",    5003, 127,  8),
    ("state",     3132,  79, 15),
    ("app",       2801,  10, 10),
    ("hardware",  1751,  19,  9),
    ("main",      1648,  42,  4),
    ("tasks",     1371,  18,  9),
    ("theme",      600,  20,  2),
]
TOTAL = sum(m[1] for m in MODULES)
TESTS = sum(m[2] for m in MODULES)
FILES = sum(m[3] for m in MODULES)
REF = MODULES[0][1]
PITCH = (X1 - X0) / len(MODULES)
BW = 44

out, defs, css = [], [], []


def db(v):
    return 10 * math.log10(v / REF)


def y_of(d):
    return TOP + HEAD + (0 - d) / (0 - DB_FLOOR) * (BOT - TOP - HEAD)


def panel(x, y, w, h, title, colour=EDGE):
    tw = len(title) * 6.4 + 12
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="none" stroke="{colour}" stroke-width="1.5"/>'
            f'<rect x="{x+14}" y="{y-6}" width="{tw:.0f}" height="12" fill="{BG}"/>'
            f'<text x="{x+19}" y="{y+4}" fill="{DIM}" font-size="10.5" letter-spacing="0.5">{title}</text>')


# ---- command line, same shell colours as the hero --------------------------
out.append(f'<text x="{PAD}" y="{CMD_Y}" fill="{DIMMER}" font-size="{FS}" font-weight="600">~$</text>')
sx, cw, inner = PAD + 3 * CHW, 0.0, []
for txt, col, wt in [("sdrtop", GREEN, "600"), ("--scan", ORANGE, "400"), ("./src", FG, "400")]:
    inner.append(f'<text x="{sx+cw:.1f}" y="{CMD_Y}" fill="{col}" font-size="{FS}" font-weight="{wt}">{txt}</text>')
    cw += (len(txt) + 1) * CHW
cw -= CHW
defs.append(f'<clipPath id="cc"><rect x="{sx-1:.1f}" y="52" height="24" width="{cw+3:.1f}">'
            f'<animate attributeName="width" from="0" to="{cw+3:.1f}" dur="0.9s" fill="freeze"/></rect></clipPath>')
out.append(f'<g clip-path="url(#cc)">{"".join(inner)}</g>')
out.append(f'<text class="fade1" x="{sx+cw+18:.0f}" y="{CMD_Y}" fill="{DIMMER}" font-size="12.5">'
           f'# yes, I pointed the instrument at itself</text>')
css.append(".fade1 { animation: fade .5s 1.0s both; }")

# ---- plot frame ------------------------------------------------------------
out.append(panel(X0 - 8, TOP - 10, X1 - X0 + 16, BOT - TOP + 38, "spectrum  ./src"))
for d in range(0, -21, -5):
    yy = y_of(d)
    out.append(f'<line x1="{X0}" y1="{yy:.1f}" x2="{X1}" y2="{yy:.1f}" stroke="{EDGE}" stroke-width="1" stroke-dasharray="2 4"/>')
    out.append(f'<text x="{X0-12}" y="{yy+4:.1f}" text-anchor="end" fill="{DIMMER}" font-size="10.5">{d}</text>')
out.append(f'<text x="{X0-12}" y="{TOP-14}" text-anchor="end" fill="{DIMMER}" font-size="10.5">dBc</text>')

# ---- bars ------------------------------------------------------------------
delay = 1.2
for i, (name, loc, tests, files) in enumerate(MODULES):
    d = db(loc)
    bx = X0 + i * PITCH + (PITCH - BW) / 2
    top = y_of(d)
    h = BOT - top
    col = CYAN if name == "signal" else BLUE
    cls = f"b{i}"
    # a live instrument never sits perfectly still
    j = 0.012 * h
    hs = f"{h:.1f};{h-j:.1f};{h+j*0.6:.1f};{h-j*0.4:.1f};{h:.1f}"
    ys = f"{top:.1f};{top+j:.1f};{top-j*0.6:.1f};{top+j*0.4:.1f};{top:.1f}"
    out.append(
        f'<g class="{cls}"><rect x="{bx:.1f}" y="{top:.1f}" width="{BW}" height="{h:.1f}" fill="{col}" opacity="0.82">'
        f'<animate attributeName="height" values="{hs}" dur="{2.4+i*0.31:.2f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{ys}" dur="{2.4+i*0.31:.2f}s" repeatCount="indefinite"/></rect>'
        f'<rect x="{bx:.1f}" y="{top-2:.1f}" width="{BW}" height="2" fill="{col}"/>'
        f'<text x="{bx+BW/2:.1f}" y="{top-8:.1f}" text-anchor="middle" fill="{DIM}" font-size="10.5">{loc:,}</text>'.replace(",", " ") +
        f'<text x="{bx+BW/2:.1f}" y="{BOT+18:.1f}" text-anchor="middle" fill="{CYAN if name == "signal" else DIM}" font-size="11.5">{name}</text>'
        f'</g>'
    )
    css.append(f".{cls} {{ animation: rise .5s {delay:.2f}s both; }}")
    if name == "signal":
        mx, my = bx + BW / 2, top - 24
        out.append(f'<g class="mk"><path d="M{mx-5},{my-8} L{mx+5},{my-8} L{mx},{my} Z" fill="{YELLOW}"/>'
                   f'<text x="{mx}" y="{my-12}" text-anchor="middle" fill="{YELLOW}" font-size="10.5" font-weight="700">M1</text></g>')
        css.append(f".mk {{ animation: fade .5s {delay+0.5:.2f}s both; }}")
    delay += 0.13

# ---- waterfall -------------------------------------------------------------
WF_TOP, WF_H, RH = BOT + 62, 54, 3
ROWS = WF_H // RH
CW = 7
COLS = int((X1 - X0) / CW)
out.append(panel(X0 - 8, WF_TOP - 10, X1 - X0 + 16, WF_H + 20, "waterfall"))
HEAT = [None, "#1e2233", "#26304f", "#33477e", "#4b6bb5", BLUE, CYAN]
defs.append(f'<clipPath id="wf"><rect x="{X0}" y="{WF_TOP}" width="{COLS*CW}" height="{WF_H}"/></clipPath>')

levels = []
for c in range(COLS):
    x = (c + 0.5) * CW
    i = min(len(MODULES) - 1, int(x / PITCH))
    base = (db(MODULES[i][1]) - DB_FLOOR) / -DB_FLOOR      # 0..1
    edge = abs(((x % PITCH) / PITCH) - 0.5) * 2            # 0 centre, 1 edge
    levels.append(max(0.0, base * (1 - 0.55 * edge ** 2)))

pattern = []
for r in range(ROWS):
    pattern.append([max(0, min(6, int(l * 6 + random.uniform(-0.7, 0.7)))) for l in levels])

cells = []
for k, row in enumerate(pattern * 2):
    for c, v in enumerate(row):
        if not v:
            continue
        cells.append(f'<rect x="{X0 + c*CW}" y="{k*RH}" width="{CW}" height="{RH}" fill="{HEAT[v]}"/>')
out.append(f'<g class="wfg" clip-path="url(#wf)">'
           f'<g id="wfs" transform="translate(0,{WF_TOP-ROWS*RH})">{"".join(cells)}</g></g>')
css.append("#wfs { animation: wfscroll 8s linear infinite; }")
css.append(f"@keyframes wfscroll {{ from {{transform:translateY({WF_TOP-ROWS*RH}px)}} to {{transform:translateY({WF_TOP}px)}} }}")
css.append(f".wfg {{ animation: fade .6s {delay+0.6:.2f}s both; }}")

# ---- readout ---------------------------------------------------------------
PTOP = TOP - 10
PH = WF_TOP + WF_H + 10 - PTOP
out.append(panel(PX, PTOP, PW, PH, "readout", EDGE))
ry = PTOP + 34
for k, v, c in [("TOTAL", f"{TOTAL:,}".replace(",", " ") + " lines", FG),
                ("TESTS", f"{TESTS}", FG),
                ("FILES", f"{FILES}", FG)]:
    out.append(f'<text class="ro" x="{PX+16}" y="{ry}" fill="{DIMMER}" font-size="11.5">{k}</text>'
               f'<text x="{PX+PW-16}" y="{ry}" text-anchor="end" fill="{c}" font-size="12.5" font-weight="600">{v}</text>')
    ry += 24

ry += 12
out.append(f'<line class="ro" x1="{PX+16}" y1="{ry-14}" x2="{PX+PW-16}" y2="{ry-14}" stroke="{EDGE}"/>')
out.append(f'<text class="ro" x="{PX+16}" y="{ry}" fill="{YELLOW}" font-size="11.5" font-weight="700">MARKER M1</text>')
ry += 24
for line, col in [("signal", CYAN), ("5 003 lines", FG), ("-6.4 dBc", DIM),
                  ("", None), ("hand written.", NOTE), ("no DSP crate.", NOTE)]:
    if line:
        out.append(f'<text class="ro" x="{PX+16}" y="{ry}" fill="{col}" font-size="12">{line}</text>')
    ry += 21
css.append(f".ro {{ animation: fade .5s {delay+0.3:.2f}s both; }}")

out.append(f'<text class="fnote" x="{X0-8}" y="{WF_TOP+WF_H+38}" fill="{NOTE}" font-size="12">'
           f'ui is 57% of the tree. drawing boxes in a terminal is not as simple as it looks.</text>')
css.append(f".fnote {{ animation: fade .5s {delay+0.8:.2f}s both; }}")

H = WF_TOP + WF_H + 60

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'Cascadia Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace">
<defs>
{chr(10).join(defs)}
</defs>
<style>
@keyframes fade {{ from {{opacity:0}} to {{opacity:1}} }}
@keyframes rise {{ from {{opacity:0; transform:translateY(10px)}} to {{opacity:1; transform:translateY(0)}} }}
{chr(10).join(css)}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BG}" stroke="{EDGE}" stroke-width="2"/>
<rect x="1" y="1" width="{W-2}" height="{TITLE_H}" rx="14" fill="{PANEL}"/>
<rect x="1" y="20" width="{W-2}" height="{TITLE_H-19}" fill="{PANEL}"/>
<circle cx="22" cy="18" r="5" fill="{RED}"/><circle cx="40" cy="18" r="5" fill="{YELLOW}"/><circle cx="58" cy="18" r="5" fill="{GREEN}"/>
<text x="{W/2}" y="22" text-anchor="middle" fill="{DIM}" font-size="12">sdrtop: self-analysis</text>
{chr(10).join(out)}
</svg>
'''
open(OUT, "w").write(svg)
print("wrote", OUT, f"({W}x{H})", "|", TOTAL, "lines,", TESTS, "tests,", FILES, "files")
