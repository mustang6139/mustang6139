#!/usr/bin/env python3
"""judges.svg: three dead build badges that quietly say something else every 30s."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, ".thalos", "judges.svg")

FS = 11
CH = FS * 0.6      # monospace advance
H = 22
PADX = 9
GAP = 8

PLATE_L = "#131620"   # label plate
PLATE_V = "#1a1b26"   # value plate
EDGE = "#222533"
TXT_L = "#4a5169"
TXT_V = "#6b7390"
TXT_S = "#7dcfff"     # the signal breaking through

badges = [
    ("target", "minos_exec-thalos_v4",     "origin: it will not say"),
    ("eval",   "rhadamanthys_strict-0x04", "three walls, one word, our order"),
    ("vec",    "aeacus_bypass-unlocked",   "the door is a dot. it wears our name."),
]

parts, x, rules = [], 0, []
for i, (label, value, secret) in enumerate(badges):
    lw = len(label) * CH + PADX * 2
    vw = max(len(value), len(secret)) * CH + PADX * 2
    parts.append(
        f'<g transform="translate({x:.1f},0)">'
        f'<rect x="0" y="0" width="{lw+vw:.1f}" height="{H}" fill="{PLATE_V}" stroke="{EDGE}"/>'
        f'<rect x="0" y="0" width="{lw:.1f}" height="{H}" fill="{PLATE_L}"/>'
        f'<line x1="{lw:.1f}" y1="0" x2="{lw:.1f}" y2="{H}" stroke="{EDGE}"/>'
        f'<text x="{lw/2:.1f}" y="15" text-anchor="middle" fill="{TXT_L}">{label}</text>'
        f'<text class="p{i}" x="{lw+vw/2:.1f}" y="15" text-anchor="middle" fill="{TXT_V}">{value}</text>'
        f'<text class="s{i}" x="{lw+vw/2:.1f}" y="15" text-anchor="middle" fill="{TXT_S}">{secret}</text>'
        f'</g>'
    )
    d = i * 0.7
    rules.append(f".p{i} {{ animation: plain 30s {d}s infinite; }}")
    rules.append(f".s{i} {{ opacity:0; animation: secret 30s {d}s infinite; }}")
    x += lw + vw + GAP

W = x - GAP

svg = f'''<!-- aeacus keeps: sis -->
<svg width="{W:.0f}" height="{H}" viewBox="0 0 {W:.0f} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'Cascadia Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace" font-size="{FS}">
<style>
@keyframes plain  {{ 0%,78% {{opacity:1}} 80%,90% {{opacity:0}} 92%,100% {{opacity:1}} }}
@keyframes secret {{ 0%,78% {{opacity:0}} 80%,90% {{opacity:1}} 92%,100% {{opacity:0}} }}
{chr(10).join(rules)}
</style>
{chr(10).join(parts)}
</svg>
'''
open(OUT, "w").write(svg)
print("wrote", OUT, f"({W:.0f}x{H})")
