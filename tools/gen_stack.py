#!/usr/bin/env python3
"""stack-boot.svg: an 80-column BIOS POST screen that boots, hands off, and comes up as the stack.

Laid out in character cells, not pixels: the panel is exactly 80 columns wide at
FS*0.6 advance width, which is what makes it read as a real POST screen rather
than a terminal with BIOS-flavoured text in it.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "stack-boot.svg")

FS, LH = 16, 22
CH = FS * 0.6                      # Cascadia Code advance width
COLS = 80
PADX, PADY = 56, 40
W = int(COLS * CH + 2 * PADX)      # 880: the widest GitHub will not shrink

BG, PANEL, EDGE = "#1a1b26", "#16161e", "#292e42"
FG, DIM = "#c0caf5", "#565f89"
BLUE, CYAN, GREEN, YELLOW, ORANGE, PURPLE, RED = (
    "#7aa2f7", "#7dcfff", "#9ece6a", "#e0af68", "#ff9e64", "#bb9af7", "#f7768e")
# GREEN is the status colour (OK / Done) and RED is the leak, so neither drives a language.

# every status word right-aligns to this column, so the dot leaders line up
END = 78
DOTS_FROM = 32

# Every entry is something the README can back up: sdrtop is Rust, homescape is
# Go and Svelte ("the two languages"), the kernel work is C, tools/ is Python.
DRIVERS = [
    ("RUST.SYS",   "systems",  ORANGE, 2.15),
    ("GO.SYS",     "backend",  CYAN,   2.50),
    ("SVELTE.SYS", "frontend", PURPLE, 2.85),
    ("C.SYS",      "embedded", BLUE,   3.20),
    ("PYTHON.SYS", "tooling",  YELLOW, 3.55),
]
COUNTS = ["0064K", "0128K", "0192K", "0256K", "0320K", "0384K", "0448K", "0512K", "0576K"]

T_DMI, T_DONE, T_START = 4.05, 5.05, 5.35   # Done lands a beat late on purpose
T_BADGE, T_PROMPT = 5.75, 6.65
GLITCH_AT, GLITCH_FOR = 2.95, 0.17

# port 80h diagnostic codes. 0F is not part of the sequence.
POST = [("C0", 0.00, 0.70), ("C1", 0.70, 1.75), ("2A", 1.75, GLITCH_AT),
        ("0F", GLITCH_AT, GLITCH_AT + GLITCH_FOR),
        ("2A", GLITCH_AT + GLITCH_FOR, T_DMI), ("52", T_DMI, T_START)]
POST_FINAL = ("FF", T_START)

body = []


def X(col):
    return PADX + col * CH


def txt(col, y, s, fill, bold=False, size=None, cls=None, anim=None):
    a = [f'x="{X(col):.1f}"', f'y="{y:.1f}"', f'fill="{fill}"']
    if bold:
        a.append('font-weight="600"')
    if size:
        a.append(f'font-size="{size}"')
    if cls:
        a.append(f'class="{cls}"')
    if anim:
        a.append(f'style="animation:{anim}"')
    return f'<text {" ".join(a)}>{s}</text>'


def appear(t):
    """Hold at opacity 0 for t seconds, then revert to the element's own opacity 1.

    No fill-mode games: if the renderer ignores animation the line is simply there,
    which is the correct end state.
    """
    return f"hold0 {t:.2f}s linear" if t > 0 else None


def flash(a, b):
    """Visible only during [a, b). Base opacity is 0, so it is absent otherwise."""
    return f"hold1 {b - a:.2f}s linear {a:.2f}s"


def dots(frm, to):
    return "." * max(0, to - frm)


# ---- rows -------------------------------------------------------------------
y = PADY + FS
r_banner = y
y += LH
r_copy = y
y += LH * 2
r_mem = y
y += LH * 2
r_load = y
y += LH
r_drv = y
y += LH * len(DRIVERS) + LH
r_dmi = y
y += LH
r_start = y
badge_top = y + 18
BADGE_H, BADGE_FS, BADGE_GAP, BADGE_PADX = 34, 17, 18, 18
y = badge_top + BADGE_H + 26
rule_y = y
y += 24
r_press = y
y += LH
r_prompt = y
H = int(r_prompt + PADY - FS + 22)

# ---- banner ------------------------------------------------------------------
BANNER = "Nightshift BIOS v6139, An Energy Star Antagonist"
COPY = "Copyright (C) 2015-2026, MusiThang"
body.append(txt(0, r_banner, BANNER, FG))
body.append(txt(0, r_copy, COPY, DIM, anim=appear(0.20)))

# ---- memory test: counts for real, settles on the only number that matters ----
MEM = "Memory Test"
MEM_VAL = END - 2 - 1 - 5          # "0640K" then a space then "OK"
body.append(txt(0, r_mem, MEM, DIM, anim=appear(0.70)))
body.append(txt(len(MEM) + 1, r_mem, dots(len(MEM) + 1, MEM_VAL - 1), DIM, anim=appear(0.70)))
for i, n in enumerate(COUNTS):
    a = 0.70 + i * 0.055
    body.append(txt(MEM_VAL, r_mem, n, DIM, cls="t", anim=flash(a, a + 0.055)))
body.append(txt(MEM_VAL, r_mem, "0640K", GREEN, bold=True, anim=appear(1.25)))
body.append(txt(END - 2, r_mem, "OK", GREEN, bold=True, anim=appear(1.35)))

# ---- device drivers ----------------------------------------------------------
LOAD = "Loading device drivers..."
body.append(txt(0, r_load, LOAD, DIM, anim=appear(1.75)))
for i, (name, role, color, t) in enumerate(DRIVERS):
    ry = r_drv + i * LH
    body.append(txt(2, ry, f"DEVICE={name}", color, bold=True, anim=appear(t)))
    body.append(txt(22, ry, role, FG, anim=appear(t)))
    body.append(txt(DOTS_FROM, ry, dots(DOTS_FROM, END - 3), DIM, anim=appear(t)))
    body.append(txt(END - 2, ry, "OK", GREEN, bold=True, anim=appear(t)))

# ---- DMI, and the pause everyone who owned one of these machines remembers ----
DMI = "Verifying DMI Pool Data"
body.append(txt(0, r_dmi, DMI, DIM, anim=appear(T_DMI)))
body.append(txt(len(DMI) + 1, r_dmi, dots(len(DMI) + 1, END - 5), DIM, anim=appear(T_DMI)))
body.append(txt(END - 4, r_dmi, "Done", GREEN, bold=True, anim=appear(T_DONE)))
body.append(txt(0, r_start, "Starting MusiThang...", FG, anim=appear(T_START)))

# ---- what actually came up: the same list, so the two can never drift apart ---
LANGS = [(name.removesuffix(".SYS"), color) for name, _, color, _ in DRIVERS]
bw = [len(n) * BADGE_FS * 0.62 + 2 * BADGE_PADX for n, _ in LANGS]
bx = (W - (sum(bw) + BADGE_GAP * (len(LANGS) - 1))) / 2
for i, ((name, color), w) in enumerate(zip(LANGS, bw)):
    body.append(
        f'<g style="animation:{appear(T_BADGE + i * 0.12)}">'
        f'<rect x="{bx:.1f}" y="{badge_top}" width="{w:.1f}" height="{BADGE_H}" rx="4" '
        f'fill="{PANEL}" stroke="{color}" stroke-width="1.5"/>'
        f'<text x="{bx + w / 2:.1f}" y="{badge_top + BADGE_H / 2 + 6:.0f}" text-anchor="middle" '
        f'fill="{color}" font-weight="600" font-size="{BADGE_FS}" letter-spacing="1">{name}</text></g>'
    )
    bx += w + BADGE_GAP

# ---- the leak: it fills screen the boot has not written to yet ----------------
LEAK = "0x7FFF00  PARITY_CHECK: DEGRADED (0x04)"
body.append(
    f'<text x="{W / 2:.0f}" y="{badge_top + 22}" text-anchor="middle" fill="{RED}" '
    f'class="t" style="animation:{flash(GLITCH_AT, GLITCH_AT + GLITCH_FOR)}">{LEAK}</text>'
)

# ---- bottom bar: on screen from early on, the way it really is ---------------
PRESS = "Press DEL to enter SETUP. There is no SETUP."
body.append(txt(0, r_press, PRESS, DIM, anim=appear(0.45)))
body.append(txt(0, r_prompt, "~$", DIM, anim=appear(T_PROMPT)))

# ---- POST code display -------------------------------------------------------
pb_w, pb_h = 104, 28
pb_x, pb_y = W - PADX - pb_w, r_prompt - 20
body.append(
    f'<g style="animation:{appear(0.10)}">'
    f'<rect x="{pb_x}" y="{pb_y}" width="{pb_w}" height="{pb_h}" rx="3" fill="{PANEL}" stroke="{EDGE}"/>'
    f'<text x="{pb_x + 12}" y="{pb_y + 19}" fill="{DIM}" font-size="12">POST</text></g>'
)
code_x = pb_x + 58
for code, a, b in POST:
    body.append(
        f'<text x="{code_x}" y="{pb_y + 20}" fill="{YELLOW}" font-weight="600" font-size="15" '
        f'class="t" style="animation:{flash(a, b)}">{code}</text>'
    )
body.append(
    f'<text x="{code_x}" y="{pb_y + 20}" fill="{YELLOW}" font-weight="600" font-size="15" '
    f'style="animation:{appear(POST_FINAL[1])}">{POST_FINAL[0]}</text>'
)

# ---- the cursor sits after the last character written, and follows the boot ---
CUR = [
    (0.00, len(BANNER) + 1, r_banner),
    (0.20, len(COPY) + 1, r_copy),
    (0.70, MEM_VAL - 1, r_mem),
    (1.25, MEM_VAL + 6, r_mem),
    (1.35, END, r_mem),
    (1.75, len(LOAD) + 1, r_load),
] + [(t, END, r_drv + i * LH) for i, (_, _, _, t) in enumerate(DRIVERS)] + [
    (T_DMI, END - 5, r_dmi),          # parked in the dots while DMI hangs
    (T_DONE, END, r_dmi),
    (T_START, 22, r_start),
    (T_PROMPT, 3, r_prompt),
]
DUR = CUR[-1][0]
kt = ";".join(f"{t / DUR:.4f}" for t, _, _ in CUR)
xs = ";".join(f"{X(c):.1f}" for _, c, _ in CUR)
ys = ";".join(f"{ry - FS + 3:.1f}" for _, _, ry in CUR)
caret = (
    f'<rect id="caret" x="{X(3):.1f}" y="{r_prompt - FS + 3:.1f}" width="{CH:.0f}" height="{FS}" fill="{FG}">'
    f'<animate attributeName="x" values="{xs}" keyTimes="{kt}" calcMode="discrete" dur="{DUR}s" fill="freeze"/>'
    f'<animate attributeName="y" values="{ys}" keyTimes="{kt}" calcMode="discrete" dur="{DUR}s" fill="freeze"/>'
    f'</rect>'
)

CSS = """
@keyframes hold0 { from { opacity: 0 } to { opacity: 0 } }
@keyframes hold1 { from { opacity: 1 } to { opacity: 1 } }
.t { opacity: 0 }
#caret { animation: blink 1.06s steps(1) infinite; }
@keyframes blink { 0%,49% { opacity: 1 } 50%,99% { opacity: 0 } 100% { opacity: 1 } }
"""

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'Cascadia Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace" font-size="{FS}">
<defs>
<pattern id="scan" width="1" height="3" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="{EDGE}" opacity="0.45"/></pattern>
</defs>
<style>{CSS}</style>

<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="5" fill="{BG}" stroke="{EDGE}" stroke-width="2"/>
<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="url(#scan)" opacity="0.55"/>

{chr(10).join(body)}

<line x1="{PADX}" y1="{rule_y:.0f}" x2="{W-PADX}" y2="{rule_y:.0f}" stroke="{EDGE}" stroke-width="1"/>
{caret}
</svg>
'''
open(OUT, "w").write(svg)
print(f"wrote {OUT} ({W}x{H}, {COLS} cols)")
