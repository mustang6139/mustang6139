#!/usr/bin/env python3
"""story-terminal.svg: a life-sized htop where programming is PID 1."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "story-terminal.svg")

C = {
    "bg": "#1a1b26", "panel": "#16161e", "border": "#292e42",
    "fg": "#c0caf5", "dim": "#7c86ab", "dimmer": "#565f89", "note": "#737d9e",
    "blue": "#7aa2f7", "cyan": "#7dcfff", "purple": "#bb9af7",
    "green": "#9ece6a", "yellow": "#e0af68", "red": "#f7768e", "orange": "#ff9e64",
}

# 880 wide so GitHub does not scale it down and shrink the type
W, PAD, LH, FS, TITLE_H = 880, 30, 22, 13.5, 34
CW = FS * 0.6

X_PID_R = PAD + 40
X_USER = PAD + 52
X_STATE = PAD + 138
X_BAR = PAD + 156
BAR_W = 80
X_CPU_R = PAD + 275
X_TIME = PAD + 288
X_CMD = PAD + 362

X_MLBL_R, X_MBRK, X_MBAR = PAD + 40, PAD + 48, PAD + 58
MBAR_W = 150
X_MPCT_R, X_MBRK2, X_INFO = PAD + 320, PAD + 326, PAD + 350

TICK_W, TICK_PITCH = 3, 5
anims, defs, body, uid = [], [], [], [0]

nid = lambda p: (uid.__setitem__(0, uid[0] + 1), f"{p}{uid[0]}")[1]
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def reveal(cls, d):
    anims.append(f".{cls} {{ animation: reveal .45s {d:.2f}s both; }}")


def cmdline(x, y, prog, args, delay):
    """Shell colours shared with the hero: ~$ dim, program green, flags orange."""
    body.append(f'<text x="{x}" y="{y}" fill="{C["dimmer"]}" font-weight="600">~$</text>')
    sx, w, inner = x + 3 * CW, 0.0, []
    for txt, col, wt in [(prog, C["green"], "600")] + list(args):
        inner.append(f'<text x="{sx+w:.1f}" y="{y}" fill="{col}" font-weight="{wt}">{esc(txt)}</text>')
        w += (len(txt) + 1) * CW
    w -= CW
    cid = nid("clip")
    dur = max(0.35, (w / CW) * 0.045)
    defs.append(
        f'<clipPath id="{cid}"><rect x="{sx-1:.1f}" y="{y-FS}" height="{FS+8}" width="{w+3:.1f}">'
        f'<animate attributeName="width" from="0" to="{w+3:.1f}" dur="{dur:.2f}s" '
        f'begin="{delay:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    body.append(f'<g clip-path="url(#{cid})">{"".join(inner)}</g>')
    return delay + dur


def bar(x, y, width, color, level, delay, animate=None):
    n = int(width // TICK_PITCH)
    ticks = "".join(f'<rect x="{x+i*TICK_PITCH}" y="{y-FS+2}" width="{TICK_W}" height="{FS-1}"/>' for i in range(n))
    out = [f'<g fill="#3b4261">{ticks}</g>']
    if animate:
        cid = nid("bclip")
        vals = ";".join(f"{width*v:.1f}" for v in animate)
        dur = 2.2 + (uid[0] % 7) * 0.35
        defs.append(
            f'<clipPath id="{cid}"><rect x="{x}" y="{y-FS}" height="{FS+4}" width="{width*animate[0]:.1f}">'
            f'<animate attributeName="width" values="0;{vals.split(";")[0]}" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>'
            f'<animate attributeName="width" values="{vals}" dur="{dur:.2f}s" begin="{delay+0.5:.2f}s" repeatCount="indefinite"/>'
            f'</rect></clipPath>'
        )
        out.append(f'<g fill="{color}" clip-path="url(#{cid})">{ticks}</g>')
    elif level > 0:
        cid = nid("bclip")
        defs.append(
            f'<clipPath id="{cid}"><rect x="{x}" y="{y-FS}" height="{FS+4}" width="{width*level:.1f}">'
            f'<animate attributeName="width" from="0" to="{width*level:.1f}" dur="0.6s" begin="{delay:.2f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        out.append(f'<g fill="{color}" clip-path="url(#{cid})">{ticks}</g>')
    return "".join(out)


y, t = TITLE_H + 34, 0.0
t = cmdline(PAD, y, "lifetop", [("--user", C["orange"], "400"), ("musithang", C["fg"], "400")], 0.0)
y += LH + 12

meters = [
    ("1",   C["green"],  [0.42, 0.71, 0.55, 0.83, 0.48, 0.66, 0.42], "68.4%",       "Tasks: 18, 11 running, 6 sleeping, 1 stopped"),
    ("2",   C["green"],  [0.66, 0.38, 0.74, 0.44, 0.79, 0.35, 0.66], "44.1%",       "Load average: 0.71  1.42  3.09"),
    ("Mem", C["yellow"], None,                                        "11.4G/16.0G", "Uptime: 3 years, not counting the false starts"),
    ("Swp", C["red"],    None,                                        "0.6G/8.0G",   "Coffee: critically low"),
]
mt = t + 0.15
for label, col, ani, pct, info in meters:
    cls = nid("m"); reveal(cls, mt)
    level = 0.7 if label == "Mem" else (0.08 if label == "Swp" else 0)
    body.append(
        f'<g class="{cls}">'
        f'<text x="{X_MLBL_R}" y="{y}" text-anchor="end" fill="{C["dim"]}">{label}</text>'
        f'<text x="{X_MBRK}" y="{y}" fill="{C["dimmer"]}">[</text>'
        f'{bar(X_MBAR, y, MBAR_W, col, level, mt, animate=ani)}'
        f'<text x="{X_MPCT_R}" y="{y}" text-anchor="end" fill="{C["dim"]}">{pct}</text>'
        f'<text x="{X_MBRK2}" y="{y}" fill="{C["dimmer"]}">]</text>'
        f'<text x="{X_INFO}" y="{y}" fill="{C["dim"]}">{esc(info)}</text></g>'
    )
    y += LH; mt += 0.12

t = mt + 0.1
y += 14

cls = nid("h"); reveal(cls, t)
body.append(
    f'<g class="{cls}" fill="{C["bg"]}" font-weight="700">'
    f'<rect x="{PAD-8}" y="{y-FS-3}" width="{W-2*PAD+16}" height="{LH}" fill="{C["blue"]}" opacity="0.85"/>'
    f'<text x="{X_PID_R}" y="{y}" text-anchor="end">PID</text>'
    f'<text x="{X_USER}" y="{y}">USER</text>'
    f'<text x="{X_STATE}" y="{y}">S</text>'
    f'<text x="{X_BAR}" y="{y}">CPU%</text>'
    f'<text x="{X_TIME}" y="{y}">TIME+</text>'
    f'<text x="{X_CMD}" y="{y}">COMMAND</text></g>'
)
y += LH + 6
t += 0.25

D = C["dim"]
procs = [
    ("1",   "R", [.72,.9,.78,.95,.8,.88,.72],  "88.2", "3y",    "",           "programming",             C["green"],  "never exits. everything else is a child of it."),
    ("42",  "R", [.5,.75,.58,.82,.55,.7,.5],   "62.4", "6h 12m", "├─ ",        "rust",                    C["orange"], "daily driver. still argues with me, still wins."),
    ("77",  "R", [.35,.6,.42,.66,.4,.55,.35],  "31.8", "2h 04m", "│  └─ ",     "sdrtop",                  C["cyan"],   "keyboard only, built to survive a Pi"),
    ("128", "R", [.2,.42,.28,.5,.24,.38,.2],   "18.6", "0h 41m", "├─ ",        "REDACTED",                C["purple"], "writing its lore first, code comes later."),
    ("201", "T", None,                          "0.0",  "---",    "├─ ",        "homescape",               C["yellow"], "stopped, not killed. it gets its turn."),
    ("202", "S", None,                          "0.0",  "---",    "├─ ",        "go / svelte",             D,           ""),
    ("203", "S", None,                          "0.0",  "---",    "├─ ",        "python",                  D,           ""),
    ("204", "S", None,                          "0.0",  "---",    "├─ ",        "c, and whatever is next", D,           "new syntax is just a Tuesday"),
    ("305", "R", [.15,.3,.2,.35,.18,.28,.15],  "11.4", "3y",    "└─ ",        "hobby-scheduler",         C["blue"],   "rotates monthly. nobody approved this."),
    ("309", "R", [.25,.45,.3,.5,.28,.4,.25],   "22.7", "1h 18m", "   ├─ ",     "radio",                   C["cyan"],   "this month's obsession"),
    ("310", "R", [.08,.16,.1,.2,.12,.18,.08],  "6.2",  "312d",   "   ├─ ",     "homelab",                 C["green"],  "the only thing here with real uptime"),
    ("311", "R", [.05,.12,.07,.14,.06,.1,.05], "3.1",  "312d",   "   │  ├─ ",  "docker",                  D,           "runs everything, explains nothing"),
    ("312", "R", [.02,.05,.03,.06,.02,.04,.02],"0.4",  "312d",   "   │  ├─ ",  "wireguard",               D,           "the only tunnel I trust"),
    ("313", "R", [.03,.08,.05,.09,.04,.07,.03],"1.2",  "288d",   "   │  ├─ ",  "pihole",                  D,           "blocks ads, occasionally the internet"),
    ("314", "R", [.02,.06,.03,.07,.03,.05,.02],"0.8",  "288d",   "   │  └─ ",  "vaultwarden",             D,           "holds the password I never remember"),
    ("315", "S", None,                          "0.0",  "---",    "   ├─ ",     "ctf",                     D,           "passwords in places they had no business being"),
    ("316", "S", None,                          "0.0",  "---",    "   ├─ ",     "astronomy",               D,           ""),
    ("317", "S", None,                          "0.0",  "---",    "   └─ ",     "esp32 / m5stack",         D,           ""),
]
ST = {"R": C["green"], "S": C["dimmer"], "T": C["yellow"]}

for pid, st, lv, pct, tm, prefix, name, col, note in procs:
    cls = nid("p"); reveal(cls, t)
    sc = ST[st]
    row = [f'<g class="{cls}">',
           f'<text x="{X_PID_R}" y="{y}" text-anchor="end" fill="{C["dim"]}">{pid}</text>',
           f'<text x="{X_USER}" y="{y}" fill="{C["dim"]}">musithang</text>',
           f'<text x="{X_STATE}" y="{y}" fill="{sc}" font-weight="700">{st}</text>',
           bar(X_BAR, y, BAR_W, col if st == "R" else "#3b4261", 0, t, animate=lv),
           f'<text x="{X_CPU_R}" y="{y}" text-anchor="end" fill="{sc if st != "S" else "#3b4261"}">{pct}</text>',
           f'<text x="{X_TIME}" y="{y}" fill="{C["dimmer"]}">{tm}</text>']
    px = X_CMD
    if prefix:
        row.append(f'<text x="{px}" y="{y}" fill="{C["dimmer"]}" xml:space="preserve">{prefix}</text>')
        px += len(prefix) * CW
    if name == "REDACTED":
        row.append(f'<text class="redact" x="{px}" y="{y}" fill="{C["purple"]}">{"█"*11}</text>')
        row.append(f'<text class="secret" x="{px}" y="{y}" fill="{C["purple"]}" font-weight="600">lore/ (wip)</text>')
        px += 11 * CW
    else:
        row.append(f'<text x="{px}" y="{y}" fill="{col}" font-weight="{"700" if pid == "1" else "400"}">{esc(name)}</text>')
        px += len(name) * CW
    if note:
        row.append(f'<text x="{px+14}" y="{y}" fill="{C["note"]}" font-size="12">{esc(note)}</text>')
    row.append("</g>")
    body.append("".join(row))
    y += LH; t += 0.13

# htop's function key bar
y += 16
cls = nid("f"); reveal(cls, t + 0.2)
fkeys = [("1", "Help"), ("2", "Setup"), ("3", "Search"), ("4", "Filter"), ("5", "Tree"),
         ("6", "SortBy"), ("7", "Nice-"), ("8", "Nice+"), ("9", "Kill"), ("10", "Quit")]
fx, fbar = PAD, [f'<g class="{cls}" font-size="12.5">']
for num, label in fkeys:
    kw = len("F" + num) * 12.5 * 0.6
    lw = len(label) * 12.5 * 0.6 + 8
    plate = C["red"] if label == "Kill" else C["blue"]
    fbar.append(f'<text x="{fx}" y="{y}" fill="{C["dim"]}">F{num}</text>')
    fbar.append(f'<rect x="{fx+kw}" y="{y-13}" width="{lw:.0f}" height="18" fill="{plate}" opacity="0.85"/>')
    fbar.append(f'<text x="{fx+kw+4}" y="{y}" fill="{C["bg"]}" font-weight="600">{label}</text>')
    fx += kw + lw + 7
fbar.append("</g>")
body.append("".join(fbar))
y += LH + 18
t += 0.4

t = cmdline(PAD, y, "kill", [("-9", C["orange"], "400"), ("309", C["fg"], "400")], t + 0.3)
y += LH
cls = nid("k"); reveal(cls, t + 0.25)
body.append(f'<g class="{cls}"><text x="{PAD}" y="{y}" fill="{C["dim"]}">radio stopped. something else will spawn by spring.</text></g>')
y += LH + 12

t = cmdline(PAD, y, "kill", [("-9", C["orange"], "400"), ("1", C["fg"], "400")], t + 0.7)
y += LH
cls = nid("k"); reveal(cls, t + 0.25)
body.append(f'<g class="{cls}"><text x="{PAD}" y="{y}" fill="{C["red"]}" font-weight="600">kill: (1) programming - operation not permitted</text></g>')
y += LH + 14

t += 0.9
cls = nid("k"); reveal(cls, t)
body.append(f'<g class="{cls}"><text x="{PAD}" y="{y}" fill="{C["dimmer"]}" font-weight="600">~$</text>'
            f'<rect id="cur" x="{PAD+29}" y="{y-FS+1}" width="8" height="{FS+1}" fill="{C["fg"]}"/></g>')
anims.append(f"#cur {{ animation: blink 1s {t+0.4:.2f}s steps(1) infinite; }}")
y += 28
H = int(y)

svg = f'''<!-- rhadamanthys keeps: ba -->
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'Cascadia Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace" font-size="{FS}">
<defs>
{chr(10).join(defs)}
</defs>
<style>
@keyframes reveal {{ from {{ opacity:0; transform:translateY(6px); }} to {{ opacity:1; transform:translateY(0); }} }}
@keyframes blink  {{ 0%,49% {{ opacity:1 }} 50%,99% {{ opacity:0 }} 100% {{ opacity:1 }} }}
@keyframes peek   {{ 0%,95.5% {{ opacity:0 }} 96%,98.5% {{ opacity:1 }} 99%,100% {{ opacity:0 }} }}
@keyframes hide   {{ 0%,95.5% {{ opacity:1 }} 96%,98.5% {{ opacity:0 }} 99%,100% {{ opacity:1 }} }}
.secret {{ opacity:0; animation: peek 17s 9s infinite; }}
.redact {{ animation: hide 17s 9s infinite; }}
{chr(10).join(anims)}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{C['bg']}" stroke="{C['border']}" stroke-width="2"/>
<rect x="1" y="1" width="{W-2}" height="{TITLE_H}" rx="14" fill="{C['panel']}"/>
<rect x="1" y="20" width="{W-2}" height="{TITLE_H-19}" fill="{C['panel']}"/>
<circle cx="22" cy="18" r="5" fill="{C['red']}"/><circle cx="40" cy="18" r="5" fill="{C['yellow']}"/><circle cx="58" cy="18" r="5" fill="{C['green']}"/>
<text x="{W/2}" y="22" text-anchor="middle" fill="{C['dim']}" font-size="12">Nightty</text>
{chr(10).join(body)}
</svg>
'''
open(OUT, "w").write(svg)
print("wrote", OUT, f"({W}x{H}, build ends ~{t+1:.1f}s)")
