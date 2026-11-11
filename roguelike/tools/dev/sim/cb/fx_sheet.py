#!/usr/bin/env python3
"""fx_sheet.py: offline picture of lane VP's rlk:cb glyphs as the client would draw them (README 0-8 drawing tools).

    python3 fx_sheet.py <unpacked RP> <out.png> [<1920x1080 background frame> ...]

For each background frame (default: flat grass-grey and flat crimson) three panels: the perfect parry's title overlay (warm
tint + the streak) with the starburst at the contact point, the perfect dodge's vignette with the burst, and the normal
guard's small spark; then one row with every in-world glyph at 1 block = 120 px. Title overlays are drawn at GUI scale 2 on
1080p: 1 font unit = 4 GUI px = 8 screen px (the title's x4), nearest-neighbour like the client. Needs Pillow.
"""
import json
import sys
from pathlib import Path

from PIL import Image

rp, out = Path(sys.argv[1]), Path(sys.argv[2])
font = json.loads((rp / 'assets/rlk/font/cb.json').read_text(encoding='utf-8'))
G = {}
SP = {}
for pv in font['providers']:
    if pv['type'] == 'bitmap':
        img = Image.open(rp / 'assets/rlk/textures' / pv['file'].split(':')[1]).convert('RGBA')
        G[pv['chars'][0]] = (img, pv['height'], pv['ascent'])
    elif pv['type'] == 'space':
        SP.update(pv['advances'])
NAMES = {Path(pv['file']).stem: pv['chars'][0] for pv in font['providers'] if pv['type'] == 'bitmap'}


def run_title(frame, run, k=8):
    """draw a title run centred on the frame (k screen px per font unit); the baseline sits 3 units above the centre"""
    adv = 0
    for c in run:
        adv += SP[c] if c in SP else int(0.5 + G[c][0].width * G[c][1] / G[c][0].height) + 1
    x = frame.width / 2 - adv * k / 2
    base = frame.height / 2 - 3 * k
    for c in run:
        if c in SP:
            x += SP[c] * k
            continue
        img, h, asc = G[c]
        sc = h / img.height * k
        big = img.resize((round(img.width * sc), round(img.height * sc)), Image.NEAREST)
        frame.alpha_composite(big, (round(x), round(base - asc * k)))
        x += (int(0.5 + img.width * h / img.height) + 1) * k
    return frame


def card(frame, name, cx, cy, blocks_px, scale=1.0):
    img, h, asc = G[NAMES[name]]
    px = h / 40 * blocks_px * scale
    big = img.resize((round(img.width * px / img.height), round(px)), Image.BILINEAR)
    frame.alpha_composite(big, (round(cx - big.width / 2), round(cy - big.height / 2)))


def title_run(fn):
    src = (Path(__file__).resolve().parents[4] / 'data/rlk/function/player/def/fx/g' / f't_{fn}.mcfunction').read_text(encoding='utf-8')
    return src.split('text:"')[2].split('"')[0]


bgs = [Image.open(p).convert('RGBA').resize((1920, 1080)) for p in sys.argv[3:]] or [
    Image.new('RGBA', (1920, 1080), (120, 150, 110, 255)), Image.new('RGBA', (1920, 1080), (120, 22, 30, 255))]
rows = []
for bg in bgs:
    a = run_title(bg.copy(), title_run('parry'))
    card(a, 'star', 960, 470, 190, 1.5)
    b = run_title(bg.copy(), title_run('vig'))
    card(b, 'burst', 960, 560, 190, 1.0)
    c = bg.copy()
    card(c, 'spark', 960, 500, 190, 1.2)
    row = Image.new('RGBA', (1920 * 3 // 2 + 8, 540), (0, 0, 0, 255))
    for i, im in enumerate((a, b, c)):
        row.paste(im.resize((960, 540)), (i * 964, 0))
    rows.append(row)
strip = Image.new('RGBA', (rows[0].width, 300), (70, 74, 82, 255))
x = 20
for name, sc in (('star', 1.5), ('spark', 1.2), ('spark', 0.9), ('bolt_1', 1.3), ('bolt_2', 1.3), ('bolt_3', 1.3), ('burst', 1.0), ('glint_l', 0.5), ('glint_r', 0.5)):
    img, h, asc = G[NAMES[name]]
    wpx = img.width / img.height * h / 40 * 120 * sc
    card(strip, name, x + wpx / 2, 150, 120, sc)
    x += wpx + (0 if name == 'glint_l' else 24)
sheet = Image.new('RGBA', (rows[0].width, sum(r.height for r in rows) + 300), (0, 0, 0, 255))
y = 0
for r in rows + [strip]:
    sheet.paste(r, (0, y))
    y += r.height
sheet.convert('RGB').save(out, quality=88)
print(f'fx_sheet: {out} {sheet.size}')
