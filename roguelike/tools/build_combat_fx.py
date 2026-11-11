#!/usr/bin/env python3
"""Combat overhaul C (tools/dev/plan/combat/plan.md, lane C) + round V lane VP (v_brief.md): the player-side parry / dodge
effect glyphs.

    python3 tools/build_combat_fx.py [--resourcepack <unpacked RP>]

Writes (this generator owns both; it empties its datapack folder first, so nothing stale survives):
  datapack  data/rlk/function/player/def/fx/g/**   the glyph commands (the code points live only here)
  RP        assets/rlk/font/cb.json + assets/rlk/textures/font/cb/*.png   (only with --resourcepack; vanilla sounds only,
            no atlas: font bitmaps are their own textures)

Every bitmap cell is <= 256 x 256 px: the client's glyph atlas page is 256 x 256 and a larger source cell silently becomes
the missing-glyph box (review/v/client_facts.md 7; the 11-11b streak was 512 x 288 = the user's "네모 박스"). Wide things are
cut into several glyphs laid side by side with a -1 space between them (a bitmap glyph advances its width + 1).
tools/dev/rplint.py checks the rule for every font of the pack.

Font rlk:cb, U+EE00-EE1F (lane B's balance row is rlk:bal at U+ED00; the other fonts in the RP README 2):
  streak_0..3  the perfect parry's thin horizontal streak across the whole screen (ref_pd.md 2A: 6-10 px, pink-orange),
               four 256 x 64 strips at font height 16 (1 texel = 2 screen px at GUI scale 2); title overlay
  tint         the perfect parry's warm screen tint (toward #E1C7B9, a little stronger at the edges), 256 x 144, title overlay
  vig          the perfect dodge's overlay: a dark vignette on the top and the edges (#333843-like, reads on the crimson
               phase-2 field as well as on grass) with a faint red-pink wash toward the middle, 256 x 144, title overlay
  star         the perfect parry's starburst (core #FDF7D4, rays #F5C058), 256 x 256, in-world text_display, 1.2 b at scale 1
  spark        the normal guard's small yellow spark (tiers 2 / 1), 64 x 64, in-world, 0.4 b at scale 1
  bolt_1..3    thin white-yellow branching lightning (crawls over the parried attacker), 128 x 128, in-world, 1 b at scale 1
  burst        the perfect dodge's radial pink-red streak burst, 256 x 256, in-world, 1.4 b at scale 1
  glint_l/r    the unparriable-attack warning (video_notes 1.6 yellow): a gold sphere-ring with a long horizontal flare,
               two 160 x 64 halves (the 11-11b cell was 320 x 64: over the limit too), in-world, 1.4 b tall, 7 b wide
  neg1 / back  spaces: -1 (between the pieces of a cut glyph, and the overlay root's trailing glyph as the boss kits do) and
               -(tint advance) (to draw the streak over the tint in one title)
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
NAMES = ['streak_0', 'streak_1', 'streak_2', 'streak_3', 'tint', 'vig', 'star', 'spark', 'bolt_1', 'bolt_2', 'bolt_3',
         'burst', 'glint_l', 'glint_r']
CP = {n: 0xEE00 + i for i, n in enumerate(NAMES)}
SP_NEG1, SP_BACK = 0xEE1E, 0xEE1F
CELL_MAX = 256                    # the client's glyph atlas page (FontTexture.SIZE): a larger cell = the missing glyph
OVL_H, OVL_ASC = 144, 69          # full-screen title overlay (the boss kits' value: centred on the screen, 16:9)
STRIP_H, STRIP_ASC = 16, 1        # a streak strip: 64 x 16 font units, its middle row 7 units under the title baseline
STAR_H, SPARK_H, BOLT_H, BURST_H, GLINT_H = 48, 16, 40, 56, 56   # in-world glyphs (a text_display draws 40 units per block)


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
REF_CORE, REF_RAY, REF_STREAK, REF_STREAK_E = hexc('#FDF7D4'), hexc('#F5C058'), hexc('#F5D3CD'), hexc('#C1AAA8')
KEEP = (1.0, 1.0, 1.0, 1 / 255)   # an invisible texel that keeps a glyph's measured width (the advance) at the full cell


def lcg(seed):
    """deterministic pseudo-random floats in [0, 1) (no random module: the output must not depend on the Python build)"""
    state = [seed & 0x7fffffff or 1]

    def nxt():
        state[0] = (state[0] * 1103515245 + 12345) & 0x7fffffff
        return state[0] / 0x80000000
    return nxt


def strip_px(i, n=4, w=256, h=64):
    """piece i of n of the full-width streak: a thin near-white core (3 texels = 6 screen px) in a pink-orange glow,
    brightest in the middle of the screen, fading to nothing at both ends"""
    row = h / 2

    def px(x, y):
        u = (i * w + x + 0.5) / (n * w)                 # 0..1 across the whole screen
        d = abs(y + 0.5 - row)
        edge = abs(u - 0.5) * 2
        span = 1 - smooth(0.78, 1.0, edge)
        mid = 1 - 0.45 * edge
        core = (1 - smooth(0.9, 1.9, d)) * span * mid
        glow = math.exp(-(d / 3.2) ** 2) * 0.6 * span * mid
        flare = math.exp(-(d / 9.0) ** 2) * 0.22 * span * (1 - smooth(0.0, 0.5, edge))
        c = over(REF_CORE + (core,), mix(REF_STREAK, REF_RAY, smooth(1.5, 6.0, d)) + (max(glow, flare),))
        if c[3] > 0.004:
            return c
        return KEEP if (x == w - 1 and y == 0) else CLEAR
    return px


def tint_px(w, h):
    # round W (review T3-07): a saturated warm orange at about half the old cover (0.11-0.21 -> 0.06-0.12) - t3 measured +20 % (P1)
    # / +40 % (P2) brightness and no warmth on the red P2 field against the reference's +10 %, toward #E1C7B9
    warm, hot = hexc('#FFB45A'), hexc('#FF8C2E')

    def px(x, y):
        u, v = (x + 0.5) / w * 2 - 1, (y + 0.5) / h * 2 - 1
        e = math.hypot(u * 0.9, v)
        return mix(warm, hot, smooth(0.5, 1.4, e)) + (0.06 + 0.06 * smooth(0.4, 1.35, e),)
    return px


def vig_px(w, h):
    dark, pink = hexc('#0B0D16'), hexc('#E0667E')

    def px(x, y):
        u, v = (x + 0.5) / w * 2 - 1, (y + 0.5) / h * 2 - 1
        e = math.hypot(u * 0.92, v * 1.04)
        top = smooth(0.15, 1.0, -v) * 0.30               # the sky side goes darker (ref: #989EA9 -> #333843)
        a_dark = clamp01(0.80 * smooth(0.52, 1.28, e) + top * smooth(0.25, 1.0, e))
        a_pink = 0.10 * (1 - smooth(0.25, 0.95, e))      # the floor round the avatar reads pink
        c = over(dark + (a_dark,), pink + (a_pink,))
        return c if c[3] > 0.004 else KEEP
    return px


def star_px(n, rays=16, long_w=0.045, short_w=0.03):
    """the perfect parry's starburst: a white-hot core, long / short rays alternating, an orange-yellow halo"""
    c = (n - 1) / 2
    rnd = lcg(7)
    reach = [(1.0 if k % 4 == 0 else 0.78 if k % 2 == 0 else 0.42 + 0.2 * rnd()) for k in range(rays)]

    def px(x, y):
        dx, dy = x - c, y - c
        r = math.hypot(dx, dy) / c
        ang = math.atan2(dy, dx)
        a = 0.0
        for k in range(rays):
            th = k * 2 * math.pi / rays + 0.13
            da = math.atan2(math.sin(ang - th), math.cos(ang - th))
            if math.cos(da) <= 0 or r >= reach[k]:
                continue
            width = (long_w if k % 2 == 0 else short_w) * (1 - 0.8 * r / reach[k])
            off = abs(math.sin(da)) * r
            a = max(a, (1 - smooth(width * 0.35, width, off)) * (1 - smooth(reach[k] * 0.6, reach[k], r)))
        core = 1 - smooth(0.07, 0.22, r)
        halo = math.exp(-(r / 0.36) ** 2) * 0.62
        al = max(a, core, halo)
        if al < 0.004:
            return CLEAR
        return mix(REF_CORE, REF_RAY, smooth(0.06, 0.5, r) * (1 - core)) + (al,)
    return px


def spark_px(n):
    """the normal guard's small spark: four thin rays and four stubs, pale yellow-white (no orange: not the perfect star)"""
    c = (n - 1) / 2
    core_c, ray_c = hexc('#FFFBE0'), hexc('#FFE690')

    def px(x, y):
        dx, dy = x - c, y - c
        r = math.hypot(dx, dy) / c
        ang = math.atan2(dy, dx)
        a = 0.0
        for k in range(8):
            th = k * math.pi / 4 + 0.39
            reach = 0.95 if k % 2 == 0 else 0.45
            da = math.atan2(math.sin(ang - th), math.cos(ang - th))
            if math.cos(da) <= 0 or r >= reach:
                continue
            off = abs(math.sin(da)) * r
            a = max(a, (1 - smooth(0.03, 0.085, off)) * (1 - smooth(reach * 0.5, reach, r)))
        core = 1 - smooth(0.10, 0.30, r)
        al = max(a, core, math.exp(-(r / 0.28) ** 2) * 0.4)
        if al < 0.004:
            return CLEAR
        return mix(core_c, ray_c, smooth(0.1, 0.7, r)) + (al,)
    return px


def seg_dist(px_, py_, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    ll = vx * vx + vy * vy
    t = 0.0 if ll == 0 else clamp01(((px_ - ax) * vx + (py_ - ay) * vy) / ll)
    return math.hypot(px_ - ax - vx * t, py_ - ay - vy * t)


def bolt_px(n, seed):
    """a thin branching lightning arc from the top to the bottom of the cell"""
    rnd = lcg(seed)
    segs = []

    def walk(x, y, x1, y1, steps, jit, branch):
        px_, py_ = x, y
        for i in range(1, steps + 1):
            t = i / steps
            nx = x + (x1 - x) * t + (rnd() - 0.5) * jit * (1 if i < steps else 0)
            ny = y + (y1 - y) * t + (rnd() - 0.5) * jit * 0.4
            segs.append((px_, py_, nx, ny))
            if branch and rnd() < 0.4:
                walk(nx, ny, nx + (rnd() - 0.5) * n * 0.7, ny + n * (0.12 + 0.25 * rnd()), 3, jit * 0.7, False)
            px_, py_ = nx, ny
    walk(n * (0.3 + 0.4 * rnd()), 3, n * (0.3 + 0.4 * rnd()), n - 4, 9, n * 0.32, True)
    core_c, glow_c = hexc('#FFFDF0'), hexc('#FFE27A')

    def px(x, y):
        d = min(seg_dist(x, y, *s) for s in segs)
        core = 1 - smooth(0.7, 1.7, d)
        glow = math.exp(-(d / 3.0) ** 2) * 0.5
        al = max(core, glow)
        if al < 0.004 or x < 1 or y < 1 or x > n - 2 or y > n - 2:
            return CLEAR
        return mix(core_c, glow_c, 1 - core) + (al,)
    return px


def burst_px(n, count=34):
    """the perfect dodge's trigger burst: short pink-red streaks spraying outwards, a pale pink centre"""
    c = (n - 1) / 2
    rnd = lcg(31)
    rays = [(rnd() * 2 * math.pi, 0.22 + 0.3 * rnd(), 0.62 + 0.36 * rnd(), 0.012 + 0.014 * rnd()) for _ in range(count)]
    hot, red = hexc('#FFE3EA'), hexc('#FF3F62')

    def px(x, y):
        dx, dy = x - c, y - c
        r = math.hypot(dx, dy) / c
        ang = math.atan2(dy, dx)
        a = 0.0
        for th, r0, r1, wd in rays:
            if r < r0 or r > r1:
                continue
            da = math.atan2(math.sin(ang - th), math.cos(ang - th))
            if math.cos(da) <= 0:
                continue
            off = abs(math.sin(da)) * r
            t = (r - r0) / (r1 - r0)
            a = max(a, (1 - smooth(wd * 0.4, wd, off)) * smooth(0.0, 0.15, t) * (1 - smooth(0.55, 1.0, t)))
        glow = math.exp(-(r / 0.3) ** 2) * 0.35
        al = max(a, glow)
        if al < 0.004:
            return CLEAR
        return mix(hot, red, smooth(0.15, 0.85, r) * (0.4 + 0.6 * (1 - a))) + (al,)
    return px


def glint_half_px(side, w=320, h=64):
    """the left (side 0) or right (side 1) 160-px half of the 320 x 64 warning glint"""
    cx, cy = (w - 1) / 2, (h - 1) / 2
    rr = h * 0.40
    half = w // 2

    def px(xh, y):
        x = xh + side * half
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy)
        ring = math.exp(-((d - rr) / 1.6) ** 2)
        fill = (1 - smooth(rr - 2, rr, d)) * 0.16
        u = abs(dx) / cx
        flare = math.exp(-(abs(dy) / 1.1) ** 2) * (1 - smooth(0.35, 1.0, u)) + math.exp(-(abs(dy) / 3.5) ** 2) * 0.35 * (1 - smooth(0.1, 0.8, u))
        hot = math.exp(-(d / (rr * 0.35)) ** 2) * 0.6
        a = clamp01(max(ring, fill, flare, hot))
        if a < 0.004:
            return KEEP if (side == 0 and xh == half - 1 and y == 0) else CLEAR
        col = mix(CORE, hexc('#FFD23C'), clamp01(1 - max(hot, flare * 0.6)))
        return col + (a,)
    return px


TEXTURES = {
    # name: (w, h, painter, font height, ascent)
    **{f'streak_{i}': (256, 64, strip_px(i), STRIP_H, STRIP_ASC) for i in range(4)},
    'tint': (256, 144, tint_px(256, 144), OVL_H, OVL_ASC),
    'vig': (256, 144, vig_px(256, 144), OVL_H, OVL_ASC),
    'star': (256, 256, star_px(256), STAR_H, STAR_H // 2 + 4),
    'spark': (64, 64, spark_px(64), SPARK_H, SPARK_H // 2 + 4),
    **{f'bolt_{i}': (128, 128, bolt_px(128, 11 * i + 3), BOLT_H, BOLT_H // 2 + 4) for i in (1, 2, 3)},
    'burst': (256, 256, burst_px(256), BURST_H, BURST_H // 2 + 4),
    'glint_l': (160, 64, glint_half_px(0), GLINT_H, GLINT_H // 2 + 4),
    'glint_r': (160, 64, glint_half_px(1), GLINT_H, GLINT_H // 2 + 4),
}
assert list(TEXTURES) == NAMES
for _n, (_w, _h, _p, _fh, _asc) in TEXTURES.items():
    assert _w <= CELL_MAX and _h <= CELL_MAX, f'{_n}: a font cell over {CELL_MAX} px becomes the missing glyph'
    assert _asc <= _fh, f'{_n}: ascent > height fails the font codec'
TINT_ADV = int(0.5 + 256 * OVL_H / 144) + 1          # the tint glyph's advance (width * scale + 1)


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
    providers.append({'type': 'space', 'advances': {chr(SP_NEG1): -1, chr(SP_BACK): -TINT_ADV}})
    providers.append({'type': 'reference', 'id': 'minecraft:default'})
    font = rp / 'assets/rlk/font/cb.json'
    font.parent.mkdir(parents=True, exist_ok=True)
    font.write_text(json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'build_combat_fx: RP font rlk:cb ({len(TEXTURES)} glyphs) -> {font}')


# ------------------------------------------------------------------------------------------------- datapack
HEAD = '# Generated by tools/build_combat_fx.py (combat overhaul C, round V) - edit the generator, not this file.'


def gl(name):
    return chr(CP[name])


NEG1, BACK = chr(SP_NEG1), chr(SP_BACK)
# title overlays: the glyph run of each (the pieces overlap through the negative spaces; every run advances 256 = the screen)
TITLES = {
    'parry': gl('tint') + BACK + NEG1.join(gl(f'streak_{i}') for i in range(4)) + NEG1,   # warm tint + the streak over it
    'vig': gl('vig') + NEG1,
}


def title_comp(run):
    return f'{{text:"",extra:[{{text:"{run}",font:"{FONT}",color:"white",shadow_color:0}}]}}'


def glyph_comp(run, color='white'):
    return f'{{text:"",extra:[{{text:"{run}",font:"{FONT}",color:"{color}"}}]}}'


def text_display(run, tag, scale, rot='[0f,0f,0f,1f]', dy='-0.12f', color='white'):
    s = f'{scale}f'
    return ('summon minecraft:text_display ~ ~ ~ {Tags:["rlk_cb_fx","' + tag + '","rlk_cb_new"],billboard:"center",'
            'background:0,shadow:0b,see_through:0b,line_width:400,brightness:{sky:15,block:15},view_range:2f,'
            'text:' + glyph_comp(run, color) + ',transformation:{translation:[0f,' + dy + ',0f],left_rotation:' + rot + ','
            f'scale:[{s},{s},{s}],right_rotation:[0f,0f,0f,1f]}}}}')


def card(run, tag, cb, scale='$(s)', **kw):
    """summon one glyph card and start its age (cb = shown ticks + 1: player/def/fx/tick ages it once in its spawn tick)"""
    macro = '$' in str(scale) or '$' in str(kw.get('color', ''))
    return [('$' if macro else '') + text_display(run, tag, scale, **kw),
            f'scoreboard players set @e[type=minecraft:text_display,tag=rlk_cb_new] cb {cb}',
            'tag @e[type=minecraft:text_display,tag=rlk_cb_new] remove rlk_cb_new']


BOLT_ROLLS = (-42, -12, 16, 47)       # degrees about the view axis: three sprites x four rolls = twelve looks (g/bolt_0..11)


def write_dp():
    if DP_OUT.exists():
        shutil.rmtree(DP_OUT)
    DP_OUT.mkdir(parents=True)
    files = {
        'title': [
            '# {g,in,hold,out,t}: a full-screen overlay of the font rlk:cb on the title line (g = parry: the warm tint with the',
            '# thin streak over it / vig: the perfect dodge\'s dark vignette) for every player; vBig = t (= in + hold + out) rests',
            '# the F5 crosshair title meanwhile. The caller checks that no other big title or bottom line (vBig / ttlT) is up',
            '# (player/def/fx/ovl).',
            '$title @a[tag=player] times $(in) $(hold) $(out)',
            '$function rlk:player/def/fx/g/t_$(g)',
            '$scoreboard players set @a[tag=player] vBig $(t)'],
    }
    for g, run in TITLES.items():
        files[f't_{g}'] = [f'# Internal: the {g} overlay.', f'title @a[tag=player] title {title_comp(run)}']
    files['star'] = [
        '# {s}: the perfect parry\'s starburst (rlk:cb star, 1.2 b at scale 1) as a billboard text_display here (tags rlk_cb_fx',
        '# rlk_cb_star; aged by player/def/fx/tick, the first time in the tick it is made: cb 6 = full size at once, static for',
        '# the 4 freeze ticks, then gone in 2 t while the sparks fly: the shrink is sent at the end of the last freeze tick).',
        *card(gl('star'), 'rlk_cb_star', 6)]
    files['spark'] = [
        '# {s, c}: the normal guard\'s spark (rlk:cb spark, 0.4 b at scale 1; tiers 2 and 1, the perfect parry\'s contact) in the',
        '# text colour c (round W: a colour per tier - the glyph is pale yellow-white, the colour multiplies it), tags rlk_cb_fx',
        '# rlk_cb_spark: cb 4 = shown 1 t, gone in 2 t.',
        *card(gl('spark'), 'rlk_cb_spark', 4, color='$(c)')]
    files['burst'] = [
        '# {s}: the perfect dodge\'s radial pink-red burst (rlk:cb burst, 1.4 b at scale 1), tags rlk_cb_fx rlk_cb_burst:',
        '# cb 4 = it grows for 2 t and is gone on the third.',
        *card(gl('burst'), 'rlk_cb_burst', 4, dy='-0.4f')]
    n = 0
    for v in (1, 2, 3):
        for deg in BOLT_ROLLS:
            h = math.radians(deg) / 2
            rot = f'[0f,0f,{math.sin(h):.4f}f,{math.cos(h):.4f}f]'
            files[f'bolt_{n}'] = [
                f'# {{s}}: lightning look {n} (rlk:cb bolt_{v} rolled {deg} degrees), tags rlk_cb_fx rlk_cb_bolt: cb 3 = 2 t.',
                *card(gl(f'bolt_{v}'), 'rlk_cb_bolt', 3, rot=rot, dy='-0.3f')]
            n += 1
    files['glint'] = [
        '# The unparriable warning glint (rlk:cb glint_l + glint_r: a gold sphere-ring with a long horizontal flare, 1.4 b x 7 b)',
        '# as a billboard text_display here (tags rlk_cb_fx rlk_cb_glint; aged by player/def/fx/tick, the first time in the tick',
        '# it is made: cb 6 = bright 2 t, fading 4 t).',
        *card(gl('glint_l') + NEG1 + gl('glint_r') + NEG1, 'rlk_cb_glint', 6, scale=1)]
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
