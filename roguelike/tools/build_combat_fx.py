#!/usr/bin/env python3
"""Combat overhaul C (tools/dev/plan/combat/plan.md, lane C): the player-side parry / dodge effect glyphs.

    python3 tools/build_combat_fx.py [--resourcepack <unpacked RP>]

Writes (this generator owns both; it empties its datapack folder first, so nothing stale survives):
  datapack  data/rlk/function/player/def/fx/g/**   the glyph commands (the code points live only here)
  RP        assets/rlk/font/cb.json + assets/rlk/textures/font/cb/*.png   (only with --resourcepack; vanilla sounds only,
            no atlas: font bitmaps are their own textures)

Font rlk:cb, U+EE00-EE0F (lane B's balance row is rlk:bal at U+ED00; the other fonts in the RP README 2):
  U+EE00 streak    the perfect parry's thin gold-orange streak across the whole screen width, just below the centre (the
                   contact point at the avatar's chest in the F5 view; video_notes 1.1), a title overlay (16:9, 144 tall)
  U+EE01 streak_s  tier 2: a shorter, dimmer streak segment in the middle
  U+EE02 wash      the perfect dodge's red-orange wash (video_notes 1.4): translucent, stronger at the edges
  U+EE03 star      the gold-white starburst at the blade (8 rays), an in-world text_display (billboard), 0.8 b
  U+EE04 glint     the unparriable-attack warning (video_notes 1.6 yellow): a gold sphere-ring with a long horizontal flare,
                   an in-world text_display on the boss's chest, 1.4 b tall, 7 b wide
  U+EE0F           a -1 space (the overlay root's trailing glyph, as the boss kits do)
Rules (README 0-6): every component names its font, the root text is empty and unstyled, lowercase ids, no sounds here.
"""
import argparse
import json
import math
import shutil
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DP_OUT = ROOT / 'data/rlk/function/player/def/fx/g'
FONT = 'rlk:cb'
CP = {'streak': 0xEE00, 'streak_s': 0xEE01, 'wash': 0xEE02, 'star': 0xEE03, 'glint': 0xEE04}
SP_NEG1 = 0xEE0F
OVL_H, OVL_ASC = 144, 69          # full-screen title overlay (the boss kits' value: centred on the screen, 16:9)
STAR_H, GLINT_H = 32, 56          # in-world glyphs, font units (a text_display draws 40 units per block)


# ------------------------------------------------------------------------------------------------- painting
def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def smooth(e0, e1, x):
    t = clamp01((x - e0) / (e1 - e0)) if e1 != e0 else (1.0 if x >= e1 else 0.0)
    return t * t * (3 - 2 * t)


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def over(top, bot):
    """premultiplied-free 'over' of two (r, g, b, a) colours"""
    ta, ba = top[3], bot[3]
    a = ta + ba * (1 - ta)
    if a <= 0:
        return (0.0, 0.0, 0.0, 0.0)
    return tuple((top[i] * ta + bot[i] * ba * (1 - ta)) / a for i in range(3)) + (a,)


def png(w, h, px):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            r, g, b, a = px(x, y)
            raw += bytes((int(round(clamp01(r) * 255)), int(round(clamp01(g) * 255)), int(round(clamp01(b) * 255)),
                          int(round(clamp01(a) * 255))))

    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))


CLEAR = (0.0, 0.0, 0.0, 0.0)
GOLD, ORANGE, CORE = hexc('#FFC24A'), hexc('#FF8A1E'), hexc('#FFF6DC')


def streak_px(w, h, row, x0, x1, core_a, glow_a, glow_px):
    """a horizontal line at texture row `row` from x0 to x1 (fractions of the width), bright core + gold-orange glow"""
    def px(x, y):
        u = (x + 0.5) / w
        d = abs(y + 0.5 - row)
        span = smooth(x0, x0 + 0.06, u) * (1 - smooth(x1 - 0.06, x1, u))
        if span <= 0:
            return CLEAR
        mid = 1 - 0.35 * abs(u - 0.5) * 2          # a little brighter round the middle
        glow = math.exp(-(d / glow_px) ** 2) * glow_a * span * mid
        core = (1 - smooth(0.8, 1.6, d)) * core_a * span * mid
        c = over(CORE + (core,), mix(GOLD, ORANGE, smooth(1.0, glow_px * 1.6, d)) + (glow,))
        return c if c[3] > 0.004 else CLEAR
    return px


def wash_px(w, h):
    def px(x, y):
        u, v = (x + 0.5) / w * 2 - 1, (y + 0.5) / h * 2 - 1
        e = math.hypot(u * 0.9, v)
        a = 0.16 + 0.42 * smooth(0.35, 1.3, e)
        return mix(hexc('#FF5A2E'), hexc('#C4122C'), smooth(0.3, 1.2, e)) + (a,)
    return px


def star_px(n):
    c = (n - 1) / 2

    def px(x, y):
        dx, dy = x - c, y - c
        r = math.hypot(dx, dy) / c
        ang = math.atan2(dy, dx)
        a = 0.0
        for k in range(8):
            th = k * math.pi / 4
            long_ = k % 2 == 0
            reach = 1.0 if long_ else 0.55
            width = 0.07 if long_ else 0.05
            da = math.atan2(math.sin(ang - th), math.cos(ang - th))
            off = abs(math.sin(da)) * r
            if math.cos(da) > 0 and r < reach:
                a = max(a, (1 - smooth(width * 0.3, width, off)) * (1 - smooth(reach * 0.55, reach, r)))
        core = 1 - smooth(0.08, 0.26, r)
        glow = math.exp(-(r / 0.32) ** 2) * 0.55
        al = max(a, core, glow)
        if al < 0.004:
            return CLEAR
        col = mix(CORE, GOLD, smooth(0.05, 0.6, r) * (1 - core))
        return col + (al,)
    return px


def glint_px(w, h):
    cx, cy = (w - 1) / 2, (h - 1) / 2
    rr = h * 0.40

    def px(x, y):
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy)
        ring = math.exp(-((d - rr) / 1.6) ** 2)
        fill = (1 - smooth(rr - 2, rr, d)) * 0.16
        u = abs(dx) / cx
        flare = math.exp(-(abs(dy) / 1.1) ** 2) * (1 - smooth(0.35, 1.0, u)) + math.exp(-(abs(dy) / 3.5) ** 2) * 0.35 * (1 - smooth(0.1, 0.8, u))
        hot = math.exp(-(d / (rr * 0.35)) ** 2) * 0.6
        a = clamp01(max(ring, fill, flare, hot))
        if a < 0.004:
            return CLEAR
        col = mix(CORE, hexc('#FFD23C'), clamp01(1 - max(hot, flare * 0.6)))
        return col + (a,)
    return px


TEXTURES = {
    # name: (w, h, painter, font height, ascent)
    'streak': (512, 288, streak_px(512, 288, 288 * 0.53, 0.0, 1.0, 1.0, 0.65, 5.0), OVL_H, OVL_ASC),
    'streak_s': (512, 288, streak_px(512, 288, 288 * 0.53, 0.30, 0.70, 0.75, 0.40, 3.5), OVL_H, OVL_ASC),
    'wash': (256, 144, wash_px(256, 144), OVL_H, OVL_ASC),
    'star': (128, 128, star_px(128), STAR_H, STAR_H // 2 + 4),
    'glint': (320, 64, glint_px(320, 64), GLINT_H, GLINT_H // 2 + 4),
}


def write_rp(rp):
    tex = rp / 'assets/rlk/textures/font/cb'
    if tex.exists():
        shutil.rmtree(tex)
    tex.mkdir(parents=True)
    providers = []
    for name, (w, h, painter, fh, asc) in TEXTURES.items():
        (tex / f'{name}.png').write_bytes(png(w, h, painter))
        providers.append({'type': 'bitmap', 'file': f'rlk:font/cb/{name}.png', 'ascent': asc, 'height': fh,
                          'chars': [chr(CP[name])]})
    providers.append({'type': 'space', 'advances': {chr(SP_NEG1): -1}})
    providers.append({'type': 'reference', 'id': 'minecraft:default'})
    font = rp / 'assets/rlk/font/cb.json'
    font.parent.mkdir(parents=True, exist_ok=True)
    font.write_text(json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'build_combat_fx: RP font rlk:cb ({len(TEXTURES)} glyphs) -> {font}')


# ------------------------------------------------------------------------------------------------- datapack
HEAD = '# Generated by tools/build_combat_fx.py (combat overhaul C) - edit the generator, not this file.'


def title_comp(name):
    return (f'{{text:"",extra:[{{text:"{chr(CP[name])}",font:"{FONT}",color:"white",shadow_color:0}},'
            f'{{text:"{chr(SP_NEG1)}",font:"{FONT}"}}]}}')


def glyph_comp(name):
    return f'{{text:"",extra:[{{text:"{chr(CP[name])}",font:"{FONT}",color:"white"}}]}}'


def text_display(name, tag, scale):
    s = f'{scale}f'
    return ('summon minecraft:text_display ~ ~ ~ {Tags:["rlk_cb_fx","' + tag + '","rlk_cb_new"],billboard:"center",'
            'background:0,shadow:0b,see_through:0b,line_width:400,brightness:{sky:15,block:15},view_range:2f,'
            'text:' + glyph_comp(name) + ',transformation:{translation:[0f,-0.12f,0f],left_rotation:[0f,0f,0f,1f],'
            f'scale:[{s},{s},{s}],right_rotation:[0f,0f,0f,1f]}}}}')


def write_dp():
    if DP_OUT.exists():
        shutil.rmtree(DP_OUT)
    DP_OUT.mkdir(parents=True)
    files = {
        'title': [
            '# {g,in,hold,out,t}: a full-screen glyph of the font rlk:cb on the title line (g = streak / streak_s / wash) for every',
            '# player; vBig = t (= in + hold + out) rests the F5 crosshair title meanwhile. The caller checks that no other big title',
            '# or bottom line (vBig / ttlT) is up (player/def/fx/ovl).',
            '$title @a[tag=player] times $(in) $(hold) $(out)',
            '$function rlk:player/def/fx/g/t_$(g)',
            '$scoreboard players set @a[tag=player] vBig $(t)'],
    }
    for g in ('streak', 'streak_s', 'wash'):
        files[f't_{g}'] = [f'# Internal: the {g} overlay.', f'title @a[tag=player] title {title_comp(g)}']
    files['star'] = [
        '# {s}: the gold-white starburst (rlk:cb star, 0.8 b at scale 1) as a billboard text_display here (tags rlk_cb_fx',
        '# rlk_cb_star; aged by player/def/fx/tick: it grows 2 t, then shrinks away 2 t).',
        '$' + text_display('star', 'rlk_cb_star', '$(s)'),
        'scoreboard players set @e[type=minecraft:text_display,tag=rlk_cb_new] cb 5',
        'tag @e[type=minecraft:text_display,tag=rlk_cb_new] remove rlk_cb_new']
    files['glint'] = [
        '# The unparriable warning glint (rlk:cb glint: a gold sphere-ring with a long horizontal flare, 1.4 b x 7 b) as a',
        '# billboard text_display here (tags rlk_cb_fx rlk_cb_glint; aged by player/def/fx/tick: bright 2 t, fading 4 t).',
        text_display('glint', 'rlk_cb_glint', '1'),
        'scoreboard players set @e[type=minecraft:text_display,tag=rlk_cb_new] cb 6',
        'tag @e[type=minecraft:text_display,tag=rlk_cb_new] remove rlk_cb_new']
    for name, lines in files.items():
        (DP_OUT / f'{name}.mcfunction').write_text('\n'.join([HEAD] + lines) + '\n', encoding='utf-8')
    print(f'build_combat_fx: {len(files)} datapack functions -> {DP_OUT.relative_to(ROOT)}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--resourcepack', type=Path, default=None)
    a = ap.parse_args()
    write_dp()
    if a.resourcepack is not None:
        write_rp(a.resourcepack.resolve())


if __name__ == '__main__':
    main()
