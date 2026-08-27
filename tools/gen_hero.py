#!/usr/bin/env python3
"""hero-tui.svg: a terminal that runs fastfetch --me and fastfetch --machine on a loop."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "hero-tui.svg")

W, H, TITLE_H = 800, 360, 34
PAD = 36
LOGO_X, LOGO_Y, CELL = 46, 116, 6
KEY_X, VAL_X = 178, 276
FS, CYCLE = 14, 32
CH = FS * 0.6

BG, PANEL, EDGE = "#1a1b26", "#16161e", "#292e42"
FG, DIM = "#c0caf5", "#565f89"
BLUE, CYAN, PURPLE, GREEN, YELLOW, RED, ORANGE = "#7aa2f7", "#7dcfff", "#bb9af7", "#9ece6a", "#e0af68", "#f7768e", "#ff9e64"

ME = [
    ("Name",      "MusiThang (mustang6139 to machines)"),
    ("Daylight",  "turning shipping docs and customs chaos into order"),
    ("Nightfall", "loose wires, blinking LEDs, and just one more compile"),
    ("Base",      "Hungary, GMT+2, awake at hours I will not defend"),
    ("Humor",     "dry, mildly dark, still safe to show your boss"),
    ("Reading",   "sci-fi, the bleaker the ending the better"),
    ("Hobbies",   "on monthly rotation, currently orbiting"),
]
ORBIT = ["astronomy", "ESP32 and M5Stack builds", "the homelab, again",
         "worldbuilding lore", "drawing, with harsh self review",
         "radio, when it is radio's turn"]
MACHINE = [
    ("OS",      "a penguin distro with very strong opinions"),
    ("Host",    "a laptop that swears the fan noise is normal"),
    ("CPU",     "enough cores to compile hope in parallel"),
    ("GPU",     "renders waveforms far more often than frags"),
    ("RAM",     "permanently four browser tabs from disaster"),
    ("Shell",   "the one with the fish, obviously"),
    ("Editor",  "modal, and I will not be elaborating"),
    ("Uptime",  "since the last update I was brave enough to run"),
    ("Coolant", "coffee, then tea, then quiet panic"),
]

defs, css, out = [], [], []

# ---- logos, drawn as a pixel grid so they read like block art --------------
def arch_grid(W=17, H=20):
    """Taller than wide, like the real mark."""
    c, g = (W - 1) / 2, []
    for y in range(H):
        t = y / (H - 1)
        half = c * (t ** 0.92)
        g.append([1 if (abs(x - c) <= half and ((x-c)/3.7)**2 + ((y-(H-1))/8.6)**2 > 1) else 0
                  for x in range(W)])
    return g


def moon_grid(W=19, H=19):
    return [[1 if ((x-9)**2 + (y-9)**2 <= 9.2**2 and (x-14.6)**2 + (y-9)**2 > 9.2**2) else 0
             for x in range(W)] for y in range(H)]


CRATERS = {(3, 6), (2, 10), (4, 13), (5, 8)}


def mix(a, b, f):
    a, b = a.lstrip("#"), b.lstrip("#")
    v = [round(int(a[i:i+2], 16) + (int(b[i:i+2], 16) - int(a[i:i+2], 16)) * f) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(v)


def render_logo(grid, top, bot, craters=None):
    rows, cells = len(grid), []
    for y, row in enumerate(grid):
        shade = mix(top, bot, y / (rows - 1))     # smooth gradient down the logo
        for x, v in enumerate(row):
            if not v:
                continue
            col, op = (shade, 0.92)
            if craters and (x, y) in craters:
                col, op = mix(shade, "#1a1b26", 0.55), 1.0
            cells.append(f'<rect x="{LOGO_X + x*CELL}" y="{LOGO_Y + y*CELL}" '
                         f'width="{CELL-1}" height="{CELL-1}" fill="{col}" opacity="{op}"/>')
    return "".join(cells)


LOGO_ME = render_logo(moon_grid(), "#ffd479", "#b8863f", CRATERS)
LOGO_MACHINE = render_logo(arch_grid(), CYAN, "#3d59a1")



# one 32s session: type, run, backspace, type the other, run, backspace
CMD_Y = 66
X0 = PAD + 3 * CH                      # right after the prompt
KT1 = "0;0.009;0.047;0.453;0.475;1"
KT2 = "0;0.484;0.528;0.953;0.975;1"


def command(idx, flag, keytimes):
    """Only the command types itself in. The prompt stays put."""
    body = f"fastfetch {flag}"
    wpx = len(body) * CH
    cid = f"cmd{idx}"
    defs.append(
        f'<clipPath id="{cid}"><rect x="{X0-1:.1f}" y="{CMD_Y-FS}" height="{FS+8}" width="0">'
        f'<animate attributeName="width" values="0;0;{wpx:.1f};{wpx:.1f};0;0" '
        f'keyTimes="{keytimes}" dur="{CYCLE}s" repeatCount="indefinite"/></rect></clipPath>'
    )
    return (f'<g clip-path="url(#{cid})" font-size="{FS}">'
            f'<text x="{X0:.1f}" y="{CMD_Y}" fill="{GREEN}" font-weight="600">fastfetch</text>'
            f'<text x="{X0 + 10*CH:.1f}" y="{CMD_Y}" fill="{ORANGE}">{flag}</text></g>'), wpx


# the prompt is drawn once and never erased
out.append(f'<text x="{PAD}" y="{CMD_Y}" fill="{DIM}" font-size="{FS}">~$</text>')

c1, w1 = command(1, "--me", KT1)
c2, w2 = command(2, "--machine", KT2)
out += [c1, c2]

# a single caret that rides the typing edge through the whole session
cx = [X0, X0, X0 + w1, X0 + w1, X0, X0, X0 + w2, X0 + w2, X0, X0]
ckt = "0;0.009;0.047;0.453;0.475;0.484;0.528;0.953;0.975;1"
out.append(
    f'<rect id="caret" x="{X0:.1f}" y="{CMD_Y-FS+2}" width="{CH:.0f}" height="{FS}" fill="{FG}">'
    f'<animate attributeName="x" values="{";".join(f"{v:.1f}" for v in cx)}" '
    f'keyTimes="{ckt}" dur="{CYCLE}s" repeatCount="indefinite"/></rect>'
)

css += [
    "#s1 { opacity:0; animation: run1 %ds infinite; }" % CYCLE,
    "#s2 { opacity:0; animation: run2 %ds infinite; }" % CYCLE,
    "@keyframes run1 { 0%,4.8% {opacity:0} 5.6%,45.0% {opacity:1} 45.8%,100% {opacity:0} }",
    "@keyframes run2 { 0%,52.9% {opacity:0} 53.7%,95.0% {opacity:1} 95.8%,100% {opacity:0} }",
    "#caret { animation: blink 1s steps(1) infinite; }",
    "@keyframes blink { 0%,49% {opacity:1} 50%,99% {opacity:0} 100% {opacity:1} }",
]

# ---- output blocks ---------------------------------------------------------
def block(items, y0, step=24):
    return "".join(
        f'<text x="{KEY_X}" y="{y0+i*step}" class="key">{k}</text>'
        f'<text x="{VAL_X}" y="{y0+i*step}" class="val">{v}</text>'
        for i, (k, v) in enumerate(items)
    ), y0 + len(items) * step


s1, y1 = block(ME, 100)
tick = ""
for i, word in enumerate(ORBIT):
    tick += f'<text x="{VAL_X+20}" y="{y1+4}" class="w w{i+1}">&#187; {word}</text>'
    css.append(".w%d { animation-delay: %ss }" % (i + 1, i * 2.5))
s1 += f'<g fill="{YELLOW}" font-weight="600">{tick}</g>'
s1 = LOGO_ME + s1

s2, y2 = block(MACHINE, 100)
s2 += '<g transform="translate(%d,%d)">%s</g>' % (VAL_X, y2 + 4, "".join(
    f'<rect x="{i*20}" y="0" width="16" height="16" fill="{c}"'
    + (f' stroke="{EDGE}"' if i == 0 else "") + "/>"
    for i, c in enumerate(["#15161e", RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, FG])))
s2 = LOGO_MACHINE + s2

svg = f'''<!-- minos keeps: kata -->
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'Cascadia Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace">
<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{EDGE}"/></pattern>
{chr(10).join(defs)}
</defs>
<style>
.key {{ fill: {BLUE}; font-weight: 600; font-size: {FS}px; }}
.val {{ fill: {FG}; font-size: {FS}px; }}
.dim {{ fill: {DIM}; }}
.w   {{ opacity: 0; font-size: {FS}px; animation: wcycle 15s infinite; }}
@keyframes wcycle {{ 0% {{opacity:0}} 2% {{opacity:1}} 15% {{opacity:1}} 17% {{opacity:0}} 100% {{opacity:0}} }}
#live {{ animation: pulse 2.4s ease-in-out infinite; }}
@keyframes pulse {{ 0%,100% {{opacity:1}} 50% {{opacity:0.2}} }}
{chr(10).join(css)}
</style>

<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BG}" stroke="{EDGE}" stroke-width="2"/>
<rect x="2" y="35" width="{W-4}" height="{H-37}" fill="url(#grid)" opacity="0.5"/>
<rect x="1" y="1" width="{W-2}" height="{TITLE_H}" rx="14" fill="{PANEL}"/>
<rect x="1" y="20" width="{W-2}" height="15" fill="{PANEL}"/>
<circle cx="22" cy="18" r="5" fill="{RED}"/><circle cx="40" cy="18" r="5" fill="{YELLOW}"/><circle cx="58" cy="18" r="5" fill="{GREEN}"/>
<text x="{W/2}" y="22" text-anchor="middle" class="dim" font-size="12">Nightty</text>
<circle id="live" cx="752" cy="18" r="4" fill="{GREEN}"/>
<text x="742" y="22" text-anchor="end" class="dim" font-size="11">awake</text>

{chr(10).join(out)}

<g id="s1">{s1}</g>
<g id="s2">{s2}</g>

<!-- nothing to see here -->
<text x="782" y="346" text-anchor="end" fill="#242938" font-size="16">i use arch btw</text>
</svg>
'''
open(OUT, "w").write(svg)
print("wrote", OUT)
