#!/usr/bin/env python3
"""FX / audio / HUD kit of the second mid-boss, 달빛 환영 나비 (title 달빛의 화신).

Pattern authors call it from their patterns; nothing here decides gameplay (hits, timings and hazards stay in
the module core). Four parts, all regenerated on every run:

  1. A tinted card engine (Navia's card idea, tools/build_navia_fx_cards.py, generalised): painted sprites on
     short-lived item_display cards, camera-facing or world-oriented, with spawn, delay, grow, move, spin,
     a colour change at a chosen tick and a shrink-out fade. Every card's item definition carries a
     minecraft:custom_model_data tint (default white), so painted sprites keep their video colours and the
     neutral ones take any colour per spawn. Hard caps: CAP fx cards and TCAP telegraph cards alive at once.
  2. Ground telegraph decals (disc, ring, sector, line / lane): a dark outline around a saturated rim and a
     translucent progress fill whose bright edge reaches the rim exactly on the hit tick, then a flash. The module's
     patterns draw none since the user's telegraph rule (10-20: a ground telegraph only where the reference footage
     shows one, and the footage shows none for her; scratchpad tele/bf/audit.md); the API and its sprites stay (the
     pause / death hooks still clear them as a safety net).
  3. A vanilla sound recipe library: fx/snd/<name>, layered playsound lines with pitch, volume and the
     per-layer minimum volume of mboss_lib.sound (no creature voices).
  4. The HUD: font rlk:mboss_bf (U+E600-E6FF) with the 달빛 고치 debuff badge, the reward-buff badge, big
     pop versions, a moon-dew icon and flat screen-flash glyphs, plus show / hide / put functions for the
     boss-bar lines and the actionbar.

Outputs (owned; stale files in these places are removed):
  resource pack  assets/rlk/textures/mboss/bf_kit/<kind>.png      painted sprites (stdlib painter)
                 assets/rlk/models/item/mboss/bf_kit/<kind>.json    one zero-thickness card (tintindex 0)
                 assets/rlk/items/mboss/bf_kit/<kind>.json          item definition, custom_model_data tint
                 assets/minecraft/atlases/items.json                adds rlk:mboss/bf_kit/* (merges)
                 assets/rlk/font/mboss_bf.json + textures/font/mboss_bf/*.png
  datapack       data/rlk/function/mboss/butterfly/fx/{card,cardx,look,clear,uninstall}
                 data/rlk/function/mboss/butterfly/fx/{e,p,tele,snd,hud,test}/**
                 (other files under mboss/butterfly/fx/ belong to the module core and are left alone)
  manifest       tools/mboss_bf_fx_manifest.json (kinds, presets, sounds, glyphs, owned paths)

No hook in a shared file is needed: the engine ages its cards from a self-rescheduling function
(schedule ... 1t replace) that stops when no card is left. Cards carry rlk_room + rlk_mb_aux, so the mid-boss
cleanup, room clears and uninstall remove them too. The module's uninstall hook should call
rlk:mboss/butterfly/fx/uninstall (objectives bkS bkG bkH bkK bkD, storage rlk:bfkit).

Run: python3 tools/build_mboss_bf_fx.py --resourcepack <unpacked RP> [--datapack <dp root>]
API reference: scratchpad mb2/bf_fx_api.md. Other generators import card(), cardx(), tele_*(), snd(), fx(),
look() and the colour constants from this file.
"""
from pathlib import Path
import argparse
import json
import math
import random
import struct
import sys
import zlib

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mboss_bf_fx_paint as P  # noqa: E402

FN = 'rlk:mboss/butterfly/fx/'
FDIR = 'data/rlk/function/mboss/butterfly/fx'
NS_TEX = 'rlk:mboss/bf_kit/'           # textures, models (rlk:item/mboss/bf_kit/*) and item ids
FONT = 'rlk:mboss_bf'
STO = 'rlk:bfkit'
CAP = 64            # live fx cards; further fx spawns are skipped until some expire
TCAP = 40           # live telegraph cards (counted apart, so busy fx never hide a telegraph)
ATLAS_BUDGET = 1_000_000
OWNED_DIRS = ('e', 'p', 'tele', 'snd', 'hud', 'test', 'prop')
OWNED_FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')
SEG_D = 0.94        # dome segment: distance of the quad from the card origin at scale 1

# ----------------------------------------------------------------------------- colours (RGB ints for tints)


def rgb(h):
    return int(h[1:], 16)


WHITE = 0xFFFFFF
LIME = rgb('#B6E35A')          # registry colour, Dendro look
LIME_PALE = rgb('#D9F5A8')
LIME_DEEP = rgb('#74C93C')
MINT = rgb('#C9F2D8')
CYAN = rgb('#8DEAF0')          # X glint
OPAL = rgb('#CDE8F4')
GOLD = rgb('#F2D27A')
GOLD_PALE = rgb('#F4EDC9')
AMBER = rgb('#E2BF5F')
FIRE = rgb('#FAD77C')          # Pyro orange-gold
MAGENTA = rgb('#C680A2')
ORANGE = rgb('#F88F39')
MAROON = rgb('#8C525C')        # 달빛 고치
SALMON = rgb('#D06A60')

# telegraph tints per #elem: rim, fill, flash (saturated, darker than the fx palette: pale lime and pale gold
# vanish on the white marble; the baked dark outline carries them on the pink centre)
TELE_COL = {7: (rgb('#3FBE16'), rgb('#7BE639'), rgb('#EEFF6A')),
            1: (rgb('#FF5612'), rgb('#FF8A2A'), rgb('#FFE04A')),
            0: (rgb('#E5304A'), rgb('#FF6474'), rgb('#FFB8C4'))}

# ----------------------------------------------------------------------------- kinds
# name -> (plane, (w, h) px, card extent in blocks at scale 1 (a0, a1, b0, b1), painter box (a0, a1, b0, b1),
#          painter, supersampling, tinted-neutral?, description)
# plane: face = local XY plane (facing forward, or the camera with a billboard), flat = local XZ plane (lies in
# the executor's horizontal plane, +b forward), seg = a face quad pushed SEG_D forward (dome segments).
SQ = (-0.5, 0.5, -0.5, 0.5)
BOX = (-1, 1, -1, 1)
CRES = ('flat', (256, 128), (-0.5, 0.5, 0.0, 0.5), (-1, 1, 0, 1))
KINDS = {
    'cres_lime':    CRES + (P.paint_cres_lime, 2, False, 'lime kick / vacuum-blade crescent ribbon (swing plane, head at the left)'),
    'cres_cyan':    CRES + (P.paint_cres_cyan, 2, False, 'cyan-white crescent (cocoon burst, wind crescents)'),
    'cres_fire':    CRES + (P.paint_cres_fire, 2, False, 'fire crescent / flame sheet, orange-gold to magenta'),
    'fire_claw':    ('face', (128, 128), SQ, BOX, P.paint_fire_claw, 2, False, 'camera-facing fire crescent projectile (claw / feather)'),
    'star4':        ('face', (128, 128), SQ, BOX, P.paint_star4, 2, False, 'lime 4-point star flare, white core'),
    'glint':        ('face', (64, 64), SQ, BOX, P.paint_glint, 3, True, 'white 4-point glint (tint it)'),
    'burst':        ('face', (128, 128), SQ, BOX, P.paint_burst, 2, False, 'lime-white spiky starburst'),
    'glow':         ('face', (64, 64), SQ, BOX, P.paint_glow, 2, True, 'soft white glow disc (tint it)'),
    'mote':         ('face', (32, 32), SQ, BOX, P.paint_mote, 3, True, 'moonlight mote (tint it)'),
    'streak':       ('face', (256, 32), (-0.5, 0.5, -0.0625, 0.0625), BOX, P.paint_streak, 2, True, 'long thin streak along a (tint it)'),
    'leaf':         ('face', (32, 32), SQ, BOX, P.paint_leaf, 3, True, 'leaf / petal flake (tint lime or amber)'),
    'bfly':         ('face', (64, 64), SQ, BOX, P.paint_bfly, 3, True, 'small butterfly outline glyph (tint it)'),
    'disc_lime':    ('flat', (256, 256), SQ, BOX, P.paint_disc_lime, 2, False, 'Dendro disc decal: lime swirl, bright rim'),
    'ripple':       ('face', (256, 256), SQ, BOX, P.paint_ripple, 2, True, 'ripple / wind ring (near white, tint it)'),
    'gyro':         ('face', (256, 256), SQ, BOX, P.paint_gyro, 2, False, 'lime gyroscope ring with beads'),
    'sphere':       ('face', (128, 128), SQ, BOX, P.paint_sphere, 2, False, 'translucent light sphere, limb-brightened'),
    'dome_lo':      ('seg', (128, 112), (-0.42, 0.42, -0.36, 0.36), BOX, P.paint_dome_lo, 2, False, 'dome shell segment, lower band (ground ring)'),
    'dome_hi':      ('seg', (128, 112), (-0.42, 0.42, -0.36, 0.36), BOX, P.paint_dome_hi, 2, False, 'dome shell segment, upper band (narrow top)'),
    'fan_fire':     ('flat', (256, 128), (-0.5, 0.5, 0.0, 0.5), (-1, 1, 0, 1), P.paint_fan_fire, 2, False, '180-degree flame fan sheet on the floor'),
    'flame_tongue': ('face', (64, 128), (-0.25, 0.25, 0.0, 1.0), (-1, 1, 0, 1), P.paint_flame_tongue, 2, False, 'vertical flame tongue, pivot at its root'),
    'flame_puff':   ('face', (64, 64), SQ, BOX, P.paint_flame_puff, 2, False, 'flame trail puff'),
    'blade':        ('face', (64, 128), (-0.25, 0.25, 0.0, 1.0), (-1, 1, 0, 1), P.paint_blade, 2, False, 'radial ground blade, pivot at its root'),
    'shard':        ('face', (64, 128), (-0.25, 0.25, -0.5, 0.5), BOX, P.paint_shard, 2, False, 'white / cyan crystal shard'),
    'cure_beam':    ('face', (64, 192), (-0.25, 0.25, 0.0, 1.5), (-1, 1, 0, 1), P.paint_cure_beam, 2, False, 'pale-gold beam, pivot at its foot'),
    'cure_burst':   ('face', (128, 128), SQ, BOX, P.paint_cure_burst, 2, False, 'white-gold burst sphere with a gold ring'),
    'cure_emblem':  ('face', (128, 192), (-0.5, 0.5, -0.75, 0.75), (-1, 1, -1.5, 1.5), P.paint_cure_emblem, 2, False, 'gold emblem: spire, star, scroll arms, crescent'),
    'dew_orb':      ('face', (128, 128), SQ, BOX, P.paint_dew_orb, 2, False, '"달빛 이슬" moon-dew heal orb look'),
    # telegraph decals (unit radius / unit length: the scale is the radius in blocks)
    't_rim':        ('flat', (256, 256), (-1, 1, -1, 1), BOX, P.paint_t_rim, 2, True, 'telegraph rim, unit radius'),
    't_rim_s':      ('flat', (128, 128), (-1, 1, -1, 1), BOX, P.paint_t_rim_s, 2, True, 'thick telegraph rim (r <= 2.5)'),
    't_fill':       ('flat', (128, 128), (-1, 1, -1, 1), BOX, P.paint_t_fill, 2, True, 'telegraph progress fill, unit radius'),
    't_bar':        ('flat', (16, 64), (-0.5, 0.5, 0.0, 1.0), (-1, 1, 0, 1), P.paint_t_bar, 2, True, 'lane rail / cap bar'),
    't_lane':       ('flat', (64, 64), (-0.5, 0.5, 0.0, 1.0), (-1, 1, 0, 1), P.paint_t_lane, 2, True, 'lane progress fill, unit length'),
}
SECTORS = (30, 45, 60, 90)
for _h in SECTORS:
    KINDS[f't_sec{_h}'] = ('flat', (256, 144), (-1, 1, -0.125, 1), (-1, 1, -0.125, 1), P.make_t_sec(_h), 2, True,
                           f'sector telegraph rim, half-angle {_h}')
    KINDS[f't_secf{_h}'] = ('flat', (128, 80), (-1, 1, -0.25, 1), (-1, 1, -0.25, 1), P.make_t_secf(_h), 2, True,
                            f'sector progress fill, half-angle {_h}')
TELE_KINDS = [k for k in KINDS if k.startswith('t_')]
FX_KINDS = [k for k in KINDS if not k.startswith('t_')]

# ----------------------------------------------------------------------------- textures


def render(kind):
    plane, (w, h), _ext, (a0, a1, b0, b1), fn, ss, _n, _d = KINDS[kind]
    px = bytearray()
    for j in range(h):
        px.append(0)
        for i in range(w):
            ar = ag = ab = aa = 0.0
            for sj in range(ss):
                bb = b1 - (j + (sj + 0.5) / ss) / h * (b1 - b0)
                for si in range(ss):
                    r, g, bl, al = fn(a0 + (i + (si + 0.5) / ss) / w * (a1 - a0), bb)
                    ar += r * al
                    ag += g * al
                    ab += bl * al
                    aa += al
            alpha = aa / (ss * ss)
            if alpha < 0.1:                     # vanilla item shaders discard < 0.1
                px += b'\x00\x00\x00\x00'
                continue
            px += bytes((round(255 * P.clamp01(ar / aa)), round(255 * P.clamp01(ag / aa)),
                         round(255 * P.clamp01(ab / aa)), round(255 * P.clamp01(alpha))))
    return w, h, bytes(px)


def png_bytes(w, h, raw):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def model_json(kind):
    """One zero-thickness double-sided card with tintindex 0. Display-local p (blocks) is written at model
    m = (8 - 16 px, 8 + 16 py, 8 - 16 pz): the item renderer's 180-degree turn about Y maps it back to p, so the
    display's local axes are the summoning frame's (+x left, +y up, +z forward). Card +a = local -x = model +x."""
    plane, _s, (a0, a1, b0, b1), _box, _fn, _ss, _n, _d = KINDS[kind]
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1
    if plane in ('face', 'seg'):
        z = 8 if plane == 'face' else 8 - 16 * SEG_D
        frm, to = [x0, 8 + 16 * b0, z], [x1, 8 + 16 * b1, z]
        faces = {'south': {'uv': [0, 0, 16, 16], 'texture': '#0', 'tintindex': 0},
                 'north': {'uv': [16, 0, 0, 16], 'texture': '#0', 'tintindex': 0}}
    else:
        frm, to = [x0, 8, 8 - 16 * b1], [x1, 8, 8 - 16 * b0]
        faces = {'up': {'uv': [0, 0, 16, 16], 'texture': '#0', 'tintindex': 0},
                 'down': {'uv': [0, 16, 16, 0], 'texture': '#0', 'tintindex': 0}}
    for v in frm + to:
        assert -16 <= v <= 32, (kind, frm, to)
    tex = NS_TEX + kind
    return {'ambientocclusion': False, 'textures': {'0': tex, 'particle': tex},
            'elements': [{'from': [round(v, 4) for v in frm], 'to': [round(v, 4) for v in to],
                          'shade': False, 'faces': faces}]}


def item_json(kind):
    return {'model': {'type': 'minecraft:model', 'model': f'rlk:item/mboss/bf_kit/{kind}',
                      'tints': [{'type': 'minecraft:custom_model_data', 'index': 0, 'default': WHITE}]}}


def atlas_px():
    return sum(v[1][0] * v[1][1] for v in KINDS.values())


# ----------------------------------------------------------------------------- HUD font
CP0, CP_SPACE = 0xE600, 0xE6F0
# name -> (codepoint, painter (x right, y up, -1..1) or flat (hex, alpha), texture px (w, h), height, ascent)
GLYPHS = {
    'coc':       (0xE600, P.glyph_coc, (36, 36), 9, 8),
    'buff':      (0xE601, P.glyph_buff, (36, 36), 9, 8),
    'coc_big':   (0xE602, P.glyph_coc, (96, 96), 24, 18),
    'buff_big':  (0xE603, P.glyph_buff, (96, 96), 24, 18),
    'dew':       (0xE604, P.glyph_dew, (28, 36), 9, 8),
    'fl_white':  (0xE610, ('#FFFFFF', 0.92), (16, 9), 144, 69),
    'fl_lime':   (0xE611, ('#B6FC9D', 0.62), (16, 9), 144, 69),
    'fl_gold':   (0xE612, ('#F4EDC9', 0.55), (16, 9), 144, 69),
    'fl_maroon': (0xE613, ('#8C525C', 0.45), (16, 9), 144, 69),
}
SPACES = {CP_SPACE: -1}


def glyph(name):
    return chr(GLYPHS[name][0])


def paint_glyph(fn, w, h, ss=4):
    px = bytearray()
    for j in range(h):
        for i in range(w):
            ar = ag = ab = aa = 0.0
            for sj in range(ss):
                y = 1 - 2 * (j + (sj + 0.5) / ss) / h
                for si in range(ss):
                    x = -1 + 2 * (i + (si + 0.5) / ss) / w
                    if w != h:
                        x *= w / h
                    r, g, b, a = fn(x, y)
                    ar, ag, ab, aa = ar + r * a, ag + g * a, ab + b * a, aa + a
            al = aa / (ss * ss)
            if al < 0.1:
                px += b'\x00\x00\x00\x00'
            else:
                px += bytes((round(255 * P.clamp01(ar / aa)), round(255 * P.clamp01(ag / aa)),
                             round(255 * P.clamp01(ab / aa)), round(255 * P.clamp01(al))))
    return px


def font_used_elsewhere(rp, own):
    """codepoint -> font file, over every font of the resource pack except our own."""
    used = {}
    assets = Path(rp) / 'assets'
    if not assets.exists():
        return used
    for f in sorted(assets.glob('*/font/*.json')):
        if f.resolve() == Path(own).resolve():
            continue
        data = json.loads(f.read_text(encoding='utf-8'))
        for p in data.get('providers', []):
            for row in p.get('chars', []):
                for ch in row:
                    used[ord(ch)] = f'{f.parts[-3]}:{f.stem}'
            for ch in p.get('advances', {}):
                used[ord(ch)] = f'{f.parts[-3]}:{f.stem}'
    return used


def build_font(rp):
    rp = Path(rp)
    tex = rp / 'assets/rlk/textures/font/mboss_bf'
    font_path = rp / 'assets/rlk/font/mboss_bf.json'
    tex.mkdir(parents=True, exist_ok=True)
    for old in tex.glob('*.png'):
        if old.stem not in GLYPHS:
            old.unlink()
    providers = []
    for name, (cp, painter, (w, h), height, ascent) in GLYPHS.items():
        if callable(painter):
            raw = paint_glyph(painter, w, h)
        else:
            hx, al = painter
            c = P.hexc(hx)
            raw = bytes((round(c[0] * 255), round(c[1] * 255), round(c[2] * 255), round(al * 255))) * (w * h)
        rows = b''.join(b'\x00' + raw[y * w * 4:(y + 1) * w * 4] for y in range(h))
        (tex / f'{name}.png').write_bytes(png_bytes(w, h, rows))
        providers.append({'type': 'bitmap', 'file': f'rlk:font/mboss_bf/{name}.png', 'ascent': ascent,
                          'height': height, 'chars': [chr(cp)]})
    providers.append({'type': 'space', 'advances': {chr(k): v for k, v in SPACES.items()}})
    # Banner text components put the kit glyph first and the Korean text after it in one list, so the
    # text inherits this font: fall back to the default font for every char the kit does not draw.
    providers.append({'type': 'reference', 'id': 'minecraft:default'})
    ours = [g[0] for g in GLYPHS.values()] + list(SPACES)
    assert all(0xE600 <= c <= 0xE6FF for c in ours) and len(set(ours)) == len(ours)
    clash = font_used_elsewhere(rp, font_path)
    hit = [c for c in ours if c in clash]
    if hit:
        raise SystemExit('rlk:mboss_bf glyphs collide with ' + ', '.join(f'U+{c:04X} ({clash[c]})' for c in hit))
    font_path.parent.mkdir(parents=True, exist_ok=True)
    font_path.write_text(json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return len(GLYPHS)


def build_resourcepack(rp):
    rp = Path(rp)
    px = atlas_px()
    assert px <= ATLAS_BUDGET, f'atlas budget: {px} px > {ATLAS_BUDGET}'
    for k, v in KINDS.items():
        w, h = v[1]
        assert w <= 512 and h <= 512 and w % 16 == 0 and h % 16 == 0, (k, w, h)
    root = rp / 'assets/rlk'
    dirs = {'textures/mboss/bf_kit': '.png', 'models/item/mboss/bf_kit': '.json', 'items/mboss/bf_kit': '.json'}
    for sub in dirs:
        d = root / sub
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob('*'):
            if old.stem not in KINDS:
                old.unlink()
    for kind in KINDS:
        w, h, raw = render(kind)
        (root / 'textures/mboss/bf_kit' / f'{kind}.png').write_bytes(png_bytes(w, h, raw))
        (root / 'models/item/mboss/bf_kit' / f'{kind}.json').write_text(
            json.dumps(model_json(kind), separators=(',', ':')) + '\n', encoding='utf-8')
        (root / 'items/mboss/bf_kit' / f'{kind}.json').write_text(
            json.dumps(item_json(kind), separators=(',', ':')) + '\n', encoding='utf-8')
    atlaspath = rp / 'assets/minecraft/atlases/items.json'
    atlas = json.loads(atlaspath.read_text(encoding='utf-8')) if atlaspath.exists() else {'sources': []}
    atlas['sources'] = [s for s in atlas['sources'] if not str(s.get('resource', '')).startswith(NS_TEX)
                        or s['resource'][len(NS_TEX):] in KINDS]
    have = {s.get('sprite', s.get('resource')) for s in atlas['sources']}
    for kind in KINDS:
        if NS_TEX + kind not in have:
            atlas['sources'].append({'type': 'minecraft:single', 'resource': NS_TEX + kind})
    atlaspath.parent.mkdir(parents=True, exist_ok=True)
    atlaspath.write_text(json.dumps(atlas, indent=2) + '\n', encoding='utf-8')
    return len(KINDS), px, build_font(rp)


# ----------------------------------------------------------------------------- call builders (Python API)


def num(v, nd=4):
    if isinstance(v, int):
        return str(v)
    s = f'{v:.{nd}f}'.rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def _f(v):
    """a float field; a str is a macro placeholder such as '$(r)' (written as is)"""
    return v if isinstance(v, str) else num(float(v))


def _i(v):
    return v if isinstance(v, str) else str(int(v))


def vec(v):
    if isinstance(v, (int, float, str)):
        v = (v, v, v)
    return ','.join(_f(x) + 'f' for x in v)


def card(kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8, fade=0,
         col=WHITE, dly=0, dur=0, hit=-1, col2=-1):
    """The function line that spawns one card (fx/card, or fx/cardx when an extended option is used).
    pos: summon point ('^x ^y ^z', '~x ~y ~z' or absolute); rot: rotation of the card, '~ ~' = the executor's,
    '~30 -90' = turned 30 degrees to the executor's right and pitched straight up (relative yaw, absolute pitch);
    bb: fixed | center | vertical | horizontal; roll: degrees about the card's local z (left_rotation, constant);
    spin: degrees turned about the card normal over the main interpolation (-170..170); s0 / s1: start / end size
    (float = uniform, or an (x, y, z) tuple); move: end translation in the display frame (+x left, +y up,
    +z forward, blocks); life / fade: ticks; col: tint (RGB int, WHITE keeps the painted colours); dly: ticks
    hidden before it appears; dur: ticks of the main interpolation (0 = until the fade); hit / col2: `hit` ticks
    after the call the tint becomes col2. Any value may be a macro placeholder string such as '$(r)'."""
    assert kind in KINDS, kind
    assert bb in ('fixed', 'center', 'vertical', 'horizontal'), bb
    uni = (int, float, str)
    simple = isinstance(s0, uni) and isinstance(s1, uni) and not dly and not dur and hit == -1
    mv = vec(tuple(move))
    if simple:
        return (f'function {FN}card {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
                f'spin:{_i(spin)},s0:{_f(s0)},s1:{_f(s1)},move:"{mv}",life:{_i(life)},'
                f'fade:{_i(fade)},col:{_i(col)}}}')
    return (f'function {FN}cardx {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
            f'spin:{_i(spin)},s0:"{vec(s0)}",s1:"{vec(s1)}",move:"{mv}",life:{_i(life)},fade:{_i(fade)},'
            f'col:{_i(col)},dly:{_i(dly)},dur:{_i(dur)},hit:{_i(hit)},col2:{_i(col2)}}}')


cardx = card


def _tenths(v):
    return int(round(v * 10))


def tele_disc(r, tell, el=7, hold=3):
    """Disc telegraph decal of radius r blocks; the progress fill reaches the rim `tell` ticks after the call
    (the framework hz/* strike tick when created in the same tick with the same tell)."""
    return f'function {FN}tele/disc {{r:{_tenths(r)},tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}'


def tele_ring(r0, r, tell, el=7, hold=3):
    return f'function {FN}tele/ring {{r0:{_tenths(r0)},r:{_tenths(r)},tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}'


def tele_sector(r, half_angle, tell, el=7, hold=3):
    return (f'function {FN}tele/sector {{r:{_tenths(r)},a:{int(round(half_angle))},tell:{int(tell)},el:{int(el)},'
            f'hold:{int(hold)}}}')


def tele_line(length, width, tell, el=7, hold=3, back=0.0):
    return (f'function {FN}tele/line {{len:{_tenths(length)},w:{_tenths(width)},back:{_tenths(back)},'
            f'tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}')


def snd(name):
    assert name in SOUNDS, name
    return f'function {FN}snd/{name}'


def fx(name, **args):
    """A preset (fx/p/<name>); macro presets take their documented arguments."""
    assert name in PRESETS, name
    need = PRESETS[name][1]
    assert set(args) == set(need), (name, sorted(args), need)
    if not need:
        return f'function {FN}p/{name}'
    body = ','.join(f'{k}:{num(float(v)) if isinstance(v, float) else v}' for k, v in args.items())
    return f'function {FN}p/{name} {{{body}}}'


def look(kind, col=WHITE):
    assert kind in KINDS, kind
    return f'function {FN}look {{kind:"{kind}",col:{int(col)}}}'


def prop(name):
    """As @s = an item_display prop: dress it as a kit projectile / pickup look (fx/prop/<name>)."""
    assert name in PROPS, name
    return f'function {FN}prop/{name}'


def hud(name):
    assert name in HUD_FUNCS, name
    return f'function {FN}hud/{name}'


# ----------------------------------------------------------------------------- particles (vanilla)


def colour_list(c):
    if isinstance(c, int):
        c = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
    return '[' + ','.join(num(float(x), 3) + 'f' for x in c) + ']'


def part(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    d = ' '.join(num(float(v), 3) for v in delta)
    return f'particle minecraft:{name} {pos} {d} {num(float(speed), 3)} {int(n)} force @a[tag=player]'


def dust(c, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1, speed=0.0):
    return part(f'dust{{color:{colour_list(c)},scale:{num(float(scale), 2)}}}', pos, delta, speed, n)


def dust_fade(c0, c1, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1):
    return part(f'dust_color_transition{{from_color:{colour_list(c0)},to_color:{colour_list(c1)},'
                f'scale:{num(float(scale), 2)}}}', pos, delta, 0.0, n)


# ----------------------------------------------------------------------------- sound recipes
# name -> (comment, [(event, volume, pitch), ...]); one tick each, vanilla events only, no creature voices.
SOUNDS = {
    'cocoon_glow': ('Cocoon core brightens (entrance t57+, transformation start): rising glassy shimmer.',
                    [('block.beacon.power_select', 0.8, 1.4), ('block.amethyst_block.resonate', 0.7, 1.2),
                     ('block.respawn_anchor.charge', 0.35, 1.6), ('block.conduit.activate', 0.3, 1.8)]),
    'cocoon_burst': ('Cocoon bursts into crystal shards (entrance about t79): bright shatter + wind.',
                     [('block.amethyst_cluster.break', 1.0, 1.0), ('block.glass.break', 0.8, 1.3),
                      ('entity.breeze.wind_burst', 0.9, 1.2), ('block.amethyst_block.chime', 0.8, 1.5),
                      ('block.amethyst_block.chime', 0.6, 1.9), ('entity.firework_rocket.twinkle', 0.4, 1.4)]),
    'cocoon_tail': ('Glittering tail of the burst (2-8 t after cocoon_burst).',
                    [('block.amethyst_block.chime', 0.6, 1.7), ('block.amethyst_block.chime', 0.45, 2.0),
                     ('entity.firework_rocket.twinkle_far', 0.35, 1.6)]),
    'land': ('Soft landing (entrance t90, revert landing, backflip landings).',
             [('block.moss.break', 0.8, 0.9), ('entity.iron_golem.step', 0.4, 1.4), ('entity.breeze.land', 0.5, 0.9)]),
    'kick_whoosh': ('Burst-run / kick wind-up whoosh with a leafy crack (H1 hit 1 lead-in): bright air '
                    'attack, a rising swish and a glint tick on top.',
                    [('entity.breeze.wind_burst', 0.55, 1.5), ('entity.player.attack.sweep', 0.45, 1.6),
                     ('item.trident.riptide_1', 0.3, 1.9), ('block.azalea_leaves.break', 0.55, 1.25),
                     ('block.amethyst_block.chime', 0.22, 1.9)]),
    'kick_impact': ('Kick crescent lands (H1 hits, H3 kick): a thump transient, a big low airy swoosh '
                    '(pitched down so it rings longer), a leafy crackle and a short airy tail.',
                    [('entity.player.attack.strong', 0.55, 0.9), ('entity.player.attack.sweep', 1.0, 0.75),
                     ('entity.breeze.wind_burst', 0.9, 0.95), ('block.big_dripleaf.tilt_down', 0.6, 0.9),
                     ('block.azalea.break', 0.75, 0.85), ('block.azalea_leaves.break', 0.65, 1.15),
                     ('item.trident.riptide_1', 0.3, 1.7)]),
    'crescent_fly': ('A crescent wave travels (H1 ground wave, B1 trailing crescent).',
                     [('entity.phantom.swoop', 0.6, 1.4), ('item.trident.riptide_1', 0.35, 1.6),
                      ('block.azalea_leaves.hit', 0.5, 1.2)]),
    'shard_tell': ('Arm shard glows lime (H2 tell, the chain glow): shimmer chime.',
                   [('block.amethyst_block.chime', 0.8, 1.6), ('block.beacon.ambient', 0.5, 1.8),
                    ('block.amethyst_cluster.hit', 0.4, 1.9)]),
    'sweep': ('360-degree low sweep kick (H2): thump then a whirling swish and leaf debris.',
              [('entity.player.attack.sweep', 1.0, 1.1), ('block.moss.break', 0.7, 0.9),
               ('entity.breeze.whirl', 0.45, 1.4), ('entity.breeze.charge', 0.4, 1.5),
               ('entity.iron_golem.attack', 0.3, 1.6), ('block.cherry_leaves.break', 0.4, 1.2)]),
    'spiral_jump': ('Spiral jump (H2): rising whirl and a low rumble.',
                    [('entity.breeze.charge', 0.8, 1.1), ('entity.breeze.jump', 0.6, 1.0),
                     ('item.elytra.flying', 0.15, 1.6)]),
    'disc_kick': ('Orb kicked down as the Dendro disc (H2 star flash + kick): bright sparkle and a crack.',
                  [('block.conduit.activate', 0.4, 1.8), ('entity.firework_rocket.twinkle', 0.6, 1.4),
                   ('entity.player.attack.strong', 0.7, 1.2), ('entity.breeze.shoot', 0.6, 1.3)]),
    'disc_impact': ('Dendro disc hits the floor (H2 impact): boom with a leafy crackle.',
                    [('entity.generic.explode', 0.4, 1.4), ('entity.breeze.wind_burst', 0.8, 0.8),
                     ('block.azalea_leaves.break', 0.8, 1.0), ('block.moss.break', 0.8, 0.9)]),
    'dash_charge': ('Mote charge before the dash (H3): rustling glittery shimmer.',
                    [('block.azalea_leaves.break', 0.35, 1.6), ('block.amethyst_block.chime', 0.5, 1.8),
                     ('entity.breeze.charge', 0.6, 1.4)]),
    'dash': ('Dash lunge (H3, burst-runs): short airy whoosh.',
             [('entity.breeze.jump', 0.8, 1.3), ('item.trident.riptide_1', 0.5, 1.5), ('block.moss.place', 0.5, 1.0)]),
    'dash_kick': ('Dash kick impact + ring (H3): deep thump, a bright air pop, a leafy burst and a crackling '
                  'low tail.',
                  [('entity.player.attack.strong', 0.6, 0.85), ('entity.breeze.wind_burst', 1.0, 1.0),
                   ('item.mace.smash_ground', 0.6, 1.3), ('entity.wind_charge.wind_burst', 0.5, 1.2),
                   ('block.azalea_leaves.break', 0.8, 1.1), ('block.cherry_leaves.break', 0.6, 1.3),
                   ('block.cherry_sapling.place', 0.6, 0.8), ('entity.player.attack.sweep', 0.8, 0.7)]),
    'vacuum_glint': ('Vacuum blade tell glint (H4): sharp crystalline ping.',
                     [('block.amethyst_cluster.hit', 0.8, 1.8), ('block.note_block.chime', 0.35, 2.0),
                      ('entity.firework_rocket.twinkle', 0.3, 1.9)]),
    'vacuum_blade': ('Foot stomp + blade rise (H4): whoosh and leafy roar.',
                     [('entity.breeze.wind_burst', 1.0, 1.0), ('item.trident.riptide_2', 0.8, 1.2),
                      ('block.big_dripleaf.tilt_down', 0.7, 1.0), ('entity.phantom.swoop', 0.5, 1.4)]),
    'vacuum_pass': ('The blade rushes past (H4 travel): hiss and a low thump.',
                    [('entity.phantom.swoop', 0.7, 1.4), ('item.trident.riptide_1', 0.4, 1.3),
                     ('block.azalea_leaves.break', 0.5, 1.2)]),
    'transform_glow': ('Transformation: the cocoon sheath glows and the folded wings open.',
                       [('block.beacon.power_select', 0.9, 1.6), ('block.respawn_anchor.charge', 0.5, 1.6),
                        ('block.amethyst_block.resonate', 0.6, 1.4)]),
    'transform_swell': ('Light sphere + ripple rings + wings unfurl: broad airy swell.',
                        [('entity.ender_dragon.flap', 0.8, 1.5), ('entity.breeze.wind_burst', 0.8, 0.8),
                         ('block.amethyst_block.resonate', 0.9, 1.0), ('block.beacon.activate', 0.6, 1.8)]),
    'debuff': ('달빛 고치 lands on the player (with the light sphere): curse-like chime burst.',
               [('item.totem.use', 0.45, 1.4), ('block.beacon.deactivate', 0.6, 1.5),
                ('block.respawn_anchor.deplete', 0.6, 1.6), ('entity.illusioner.prepare_mirror', 0.5, 1.2)]),
    'flap_big': ('Big wing flap (B3 tell, B5 flight, the glide settle): a deep whump, the membrane body, a '
                 'low air push and a soft rustle.',
                 [('entity.ender_dragon.flap', 0.75, 1.35), ('entity.phantom.flap', 0.55, 0.75),
                  ('entity.breeze.wind_burst', 0.3, 0.7), ('item.armor.equip_elytra', 0.35, 1.3)]),
    'flap_small': ('Small hover flap (every 13-20 t in butterfly form; quiet): a soft flap and a feathery '
                   'flutter.',
                   [('entity.phantom.flap', 0.3, 1.55), ('entity.parrot.fly', 0.22, 1.2)]),
    'wing_dive': ('Bank + dive before the wing strike (B1), the release swoop (B5): a high flap, the swoop '
                  'and a rushing air tail.',
                  [('entity.ender_dragon.flap', 0.5, 1.75), ('entity.phantom.swoop', 0.8, 1.25),
                   ('item.trident.riptide_2', 0.35, 1.4), ('entity.phantom.flap', 0.3, 1.1)]),
    'wing_strike': ('Wing edge hits and sweeps on (B1): solid hit then a long airy swish with leaf crackle.',
                    [('entity.player.attack.strong', 0.5, 0.95), ('entity.player.attack.sweep', 1.0, 0.8),
                     ('entity.breeze.wind_burst', 0.9, 1.0), ('block.azalea_leaves.break', 0.7, 1.0),
                     ('item.trident.riptide_1', 0.5, 1.6), ('entity.phantom.swoop', 0.35, 1.5)]),
    'pyro_switch': ('Wings turn Pyro (1 t swap, 5-12 t before B2 / B3): a soft fire whump, a glassy shimmer '
                    'as the wing glass recolours, a bright hiss and a crackling tail.',
                    [('item.firecharge.use', 0.55, 1.35), ('block.fire.ambient', 0.7, 1.3),
                     ('block.respawn_anchor.set_spawn', 0.3, 1.6), ('block.amethyst_block.resonate', 0.3, 1.8),
                     ('entity.blaze.shoot', 0.22, 1.7), ('block.campfire.crackle', 0.5, 1.2)]),
    'dendro_switch': ('Wings turn back to Dendro (before B1 / B4 / B5).',
                      [('block.amethyst_block.resonate', 0.6, 1.4), ('block.azalea_leaves.place', 0.6, 1.0)]),
    'fire_cres_launch': ('Wing swing throws the fire crescents (B2, each swing): a low whoosh attack, the '
                         'roaring flame burst, a wing whump, air and a crackling tail.',
                         [('entity.player.attack.sweep', 0.9, 0.65), ('entity.blaze.shoot', 0.85, 0.85),
                          ('item.firecharge.use', 0.75, 0.75), ('entity.ender_dragon.flap', 0.5, 1.4),
                          ('entity.breeze.wind_burst', 0.45, 1.3), ('block.fire.ambient', 0.7, 1.4),
                          ('block.campfire.crackle', 0.6, 1.0)]),
    'fire_cres_fly': ('Crescents turn and dive (B2): crackling hiss with an airy streak.',
                      [('block.fire.ambient', 0.7, 1.5), ('block.campfire.crackle', 0.45, 1.4),
                       ('entity.blaze.burn', 0.25, 1.4), ('item.trident.riptide_1', 0.3, 1.6)]),
    'fire_cres_land': ('A fire crescent lands (B2, per landing): a sharp pop and crack, a fire puff and a '
                       'short hiss.',
                       [('block.lava.pop', 0.55, 1.1), ('entity.generic.burn', 0.6, 1.2),
                        ('entity.firework_rocket.blast', 0.5, 0.8), ('item.firecharge.use', 0.35, 1.3),
                        ('block.fire.extinguish', 0.3, 1.6)]),
    'flame_slam': ('Wing slam (B3 slam): low thump.',
                   [('entity.ender_dragon.flap', 0.9, 0.9), ('entity.generic.explode', 0.4, 1.6),
                    ('item.mace.smash_ground', 0.5, 0.9)]),
    'flame_fan': ('180-degree flame eruption (B3): crackling roar, a low boom under it and a long crackling '
                  'rumble.',
                  [('entity.blaze.shoot', 1.0, 0.8), ('item.firecharge.use', 0.9, 0.6),
                   ('block.fire.ambient', 1.0, 1.0), ('entity.generic.explode', 0.35, 0.7),
                   ('entity.blaze.burn', 0.4, 0.9), ('block.campfire.crackle', 0.8, 0.8),
                   ('block.lava.pop', 0.45, 0.9)]),
    'flame_trail': ('Flame line under the low glide (B3 trail, every 4-6 t; quiet).',
                    [('block.fire.ambient', 0.45, 1.2), ('entity.blaze.burn', 0.15, 1.5)]),
    'orb_charge': ('Wing-wrap core charge (B4 before each orb): a thin rising sparkle over a quiet hum.',
                   [('block.beacon.power_select', 0.5, 1.85), ('block.conduit.activate', 0.4, 1.6),
                    ('block.amethyst_block.resonate', 0.5, 1.8), ('block.enchantment_table.use', 0.45, 1.5),
                    ('block.respawn_anchor.charge', 0.25, 1.9), ('block.amethyst_block.chime', 0.22, 2.0)]),
    'orb_launch': ('Orb released (B4 t19 / t46): soft launch whir.',
                   [('entity.breeze.shoot', 0.8, 1.2), ('block.amethyst_block.chime', 0.6, 1.4),
                    ('item.trident.riptide_1', 0.4, 1.8), ('block.beacon.ambient', 0.5, 2.0)]),
    'orb_fly': ('Orb flight loop (every 10-12 t while it homes; quiet).',
                [('block.beacon.ambient', 0.35, 2.0), ('block.amethyst_block.step', 0.2, 1.8)]),
    'orb_burst': ('Orb bursts into radial ground blades (B4): an airy boom, a low thump, a leafy crackle and '
                  'a glassy sparkle tail.',
                  [('entity.breeze.wind_burst', 1.0, 0.95), ('entity.wind_charge.wind_burst', 0.6, 0.8),
                   ('entity.generic.explode', 0.4, 1.5), ('block.azalea_leaves.break', 1.0, 0.9),
                   ('block.cherry_leaves.break', 0.5, 1.2), ('block.big_dripleaf.tilt_down', 0.6, 0.9),
                   ('block.moss.break', 0.6, 0.8), ('block.amethyst_block.chime', 0.35, 1.6)]),
    'cocoon_ball': ('Wings curl into the ball (B4 t30-42): swirling rustle.',
                    [('item.elytra.flying', 0.25, 1.4), ('block.moss.place', 0.6, 1.0),
                     ('entity.breeze.charge', 0.4, 1.5)]),
    'release_swoop': ('달빛 해제 fold + swoop (B5 start): low swoosh.',
                      [('entity.phantom.swoop', 1.0, 1.0), ('entity.ender_dragon.flap', 0.8, 1.2)]),
    'release_whirl': ('달빛 해제 whirl / cup (B5): airy swishes.',
                      [('item.trident.riptide_1', 0.5, 1.3), ('entity.player.attack.sweep', 0.4, 1.6),
                       ('entity.player.attack.sweep', 0.35, 1.9)]),
    'release_charge': ('달빛 해제 charge (flare, X glint, ring cage): rising hum + sparkle; call 2-3 times '
                       'rising.',
                       [('block.respawn_anchor.charge', 0.9, 1.4), ('block.beacon.activate', 0.8, 1.6),
                        ('entity.warden.sonic_charge', 0.35, 1.8), ('block.beacon.power_select', 0.6, 1.4),
                        ('block.enchantment_table.use', 0.5, 1.2)]),
    'release_wrap': ('달빛 해제 wings wrap into the pod (E-9): pressure builds.',
                     [('block.respawn_anchor.charge', 0.8, 1.8), ('entity.breeze.inhale', 0.7, 1.2),
                      ('block.conduit.activate', 0.5, 1.4), ('entity.illusioner.prepare_mirror', 0.4, 1.6)]),
    'release_boom': ('달빛 해제 detonation (E): a broadband boom pitched down for a long body, an airy blast, the '
                     'sonic crack, a falling beacon tone, crystal and leaf crackle and a low glassy tail.',
                     [('entity.generic.explode', 1.6, 0.65), ('entity.dragon_fireball.explode', 1.0, 0.8),
                      ('entity.breeze.wind_burst', 1.2, 0.55), ('entity.warden.sonic_boom', 0.6, 1.4),
                      ('entity.firework_rocket.large_blast', 0.7, 0.7), ('block.beacon.deactivate', 0.8, 1.3),
                      ('block.amethyst_cluster.break', 0.9, 0.8), ('block.azalea_leaves.break', 1.0, 0.75),
                      ('block.amethyst_block.chime', 0.5, 0.6)]),
    'wing_shatter': ('Wings shrink, go flat lime and shatter (B5 E+38 / death).',
                     [('block.amethyst_cluster.break', 0.7, 1.5), ('block.glass.break', 0.4, 1.6),
                      ('entity.illusioner.mirror_move', 0.6, 1.4), ('block.beacon.deactivate', 0.5, 1.8)]),
    'groggy': ('Groggy starts (after the revert landing): spent, deflating cue.',
               [('block.respawn_anchor.deplete', 0.6, 1.2), ('block.beacon.deactivate', 0.4, 0.9)]),
    'chain_reform': ('Crescent chain re-forms at her side (after the groggy turn): plates clink into place.',
                     [('block.chain.place', 0.8, 0.8), ('block.amethyst_block.place', 0.6, 1.2),
                      ('block.amethyst_block.chime', 0.5, 1.5)]),
    'dew_spawn': ('A 달빛 이슬 heal orb appears.',
                  [('block.amethyst_block.chime', 0.6, 1.8), ('block.bubble_column.upwards_inside', 0.3, 1.6),
                   ('entity.experience_orb.pickup', 0.25, 0.7)]),
    'cure_chime': ('달빛 고치 removed by a heal: bright rising chime burst (beam, burst, emblem): an A-major '
                   'chord of note-block bell and chimes (pitch 1.19 / 1.5 / 1.78) and amethyst chimes over the '
                   'beacon swell, with a sparkle and a shimmering tail.',
                   [('block.beacon.activate', 0.75, 1.6), ('entity.player.levelup', 0.35, 1.5),
                    ('block.amethyst_block.chime', 0.9, 1.19), ('block.amethyst_block.chime', 0.8, 1.5),
                    ('block.note_block.bell', 0.45, 1.19), ('block.note_block.chime', 0.5, 1.5),
                    ('block.note_block.chime', 0.4, 1.78), ('entity.experience_orb.pickup', 0.3, 1.2),
                    ('block.amethyst_block.resonate', 0.5, 1.5)]),
    'death': ('Death: stagger, the wings shatter, she kneels and dissolves (no voices).',
              [('block.amethyst_cluster.break', 1.0, 0.9), ('block.beacon.deactivate', 0.9, 1.0),
               ('entity.breeze.wind_burst', 0.8, 0.7), ('block.amethyst_block.resonate', 0.8, 0.6),
               ('block.respawn_anchor.deplete', 0.6, 1.2)]),
    'death_motes': ('Death tail: the last motes rise.',
                    [('block.amethyst_block.chime', 0.6, 2.0), ('entity.firework_rocket.twinkle', 0.4, 1.8),
                     ('block.beacon.ambient', 0.4, 1.6)]),
}


def min_volume(vol):
    """mboss_lib.min_volume (the Guardian's L.sound): quiet layers (<= 0.25) fade out completely past their range,
    louder ones keep a third of their volume there, at most 0.4."""
    if vol <= 0.25:
        return 0.0
    return round(min(0.4, vol / 3), 2)


def sound_line(event, vol, pitch):
    return (f'playsound minecraft:{event} hostile @a[tag=player] ~ ~ ~ {num(float(vol))} {num(float(pitch))} '
            f'{num(float(min_volume(vol)), 2)}')


# ----------------------------------------------------------------------------- presets
PRESETS = {}


def preset(name, doc, args=()):
    def deco(f):
        PRESETS[name] = (doc, list(args), f)
        return f
    return deco


def ang(deg):
    return num(float(deg), 2)


def radial(n, start=0.0):
    return [start + 360.0 * k / n for k in range(n)]


# Radial trick: a fixed face card with rot "~<yaw> <90 - elev>" has its local +y pointing outward along yaw /
# elevation, so move (0, d, 0) flies outward and a blade or shard's long axis points along the flight.


@preset('cocoon_disc', 'Entrance: the glowing lime floor disc under the cocoon (at the floor point). {life}', ('life',))
def _p_cocoon_disc():
    return [
        '$' + card('disc_lime', '~ ~0.04 ~', '~ 0', s0=4.2, s1=4.6, life='$(life)', fade=8),
        '$' + card('glow', '~ ~0.06 ~', '~ 90', s0=6.0, s1=6.4, life='$(life)', fade=8, col=LIME_PALE),
        dust(LIME_PALE, 1.4, '~ ~0.3 ~', (1.2, 0.1, 1.2), 6),
    ]


@preset('cocoon_glow', 'Entrance / transformation: the cocoon core brightens (glow ramp, 18 t). At the core.')
def _p_cocoon_glow():
    return [
        card('glow', '~ ~ ~', bb='center', s0=0.8, s1=3.0, life=18, fade=3, col=rgb('#E4F59A')),
        card('star4', '~ ~ ~', bb='center', spin=90, s0=0.3, s1=1.8, life=18, fade=5),
        card('streak', '^ ^ ^', bb='center', roll=35, s0=0.5, s1=3.5, life=14, fade=4, col=rgb('#F8FFC0')),
        card('streak', '^ ^ ^', bb='center', roll=-55, s0=0.5, s1=3.0, life=14, fade=4, col=rgb('#F8FFC0')),
        part('end_rod', '~ ~ ~', (0.4, 0.8, 0.4), 0.02, 6),
        dust(rgb('#CADE48'), 1.2, '~ ~ ~', (0.5, 1.0, 0.5), 8),
    ]


@preset('whiteout', 'Entrance whiteout / big flash: a white-yellow glow ball (8 t). At the core.')
def _p_whiteout():
    return [card('glow', '~ ~ ~', bb='center', s0=2.5, s1=7.0, life=9, fade=3, col=rgb('#F8FFC0')),
            card('sphere', '~ ~ ~', bb='center', s0=1.5, s1=3.5, life=8, fade=3)]


@preset('cocoon_burst', 'Entrance t79: crystal shard star, two lime wing crescents, cyan wind ring. At the core.')
def _p_cocoon_burst():
    rnd = random.Random(79)
    out = [card('burst', '~ ~ ~', bb='center', roll=10, spin=20, s0=1.2, s1=6.5, life=6, fade=2),
           card('glow', '~ ~ ~', bb='center', s0=3, s1=7, life=5, fade=2, col=WHITE),
           card('cres_lime', '^0.6 ^ ^', '~-90 0', roll=90, s0=3.5, s1=5.5, life=8, fade=3),
           card('cres_lime', '^-0.6 ^ ^', '~90 0', roll=90, s0=3.5, s1=5.5, life=8, fade=3),
           card('ripple', '~ ~ ~', '~ 0', s0=1.5, s1=8, spin=40, life=8, fade=3, col=rgb('#E2FAF4'))]
    for yaw in radial(12, 7):
        el = rnd.uniform(-35, 55)
        out.append(card('shard', '~ ~ ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(-20, 20),
                        s0=0.5, s1=rnd.uniform(1.1, 1.8), move=(0, rnd.uniform(2.6, 3.6), 0), life=9, fade=4))
    out += [part('end_rod', '~ ~ ~', (0.6, 0.8, 0.6), 0.25, 18), part('wax_off', '~ ~ ~', (1.5, 1.5, 1.5), 0.0, 8),
            dust(rgb('#BAF3E3'), 1.6, '~ ~ ~', (1.2, 1.2, 1.2), 14)]
    return out


@preset('motes', 'Moonlight motes rising around the point (idle sparkle, charge, death). 6 cards.')
def _p_motes():
    rnd = random.Random(6)
    out = []
    for k in range(6):
        x, z, y = rnd.uniform(-0.8, 0.8), rnd.uniform(-0.8, 0.8), rnd.uniform(0.2, 1.6)
        out.append(card('mote', f'~{num(x, 2)} ~{num(y, 2)} ~{num(z, 2)}', bb='center', s0=0.12, s1=0.2,
                        move=(0, rnd.uniform(0.8, 1.4), 0), life=rnd.randint(14, 22), fade=6,
                        col=LIME_PALE if k % 2 else OPAL, dly=rnd.randint(0, 6)))
    return out


@preset('land', 'Landing: a mint ripple on the floor, drifting leaves, moss dust. At the floor point.')
def _p_land():
    return [card('ripple', '~ ~0.05 ~', '~ 90', s0=0.6, s1=4.0, spin=30, life=8, fade=3, col=MINT),
            part('cherry_leaves', '~ ~0.4 ~', (0.8, 0.2, 0.8), 0, 4),
            dust(rgb('#A8DF74'), 1.4, '~ ~0.15 ~', (0.7, 0.05, 0.7), 8),
            part('composter', '~ ~0.2 ~', (0.6, 0.1, 0.6), 0, 5)]


@preset('glint', 'A small white-lime glint (tells, foot sparkles). Billboard.')
def _p_glint():
    return [card('glint', '~ ~ ~', bb='center', spin=60, s0=0.1, s1=0.9, life=6, fade=3, col=LIME_PALE)]


@preset('kick_rise', 'H1 hit 1: the tall rising flip-kick crescent (sagittal, sweeping up and back) + ground '
        'splash. At her feet, rotated as her (yaw).')
def _p_kick_rise():
    return [card('cres_lime', '^ ^0.9 ^0.9', '~ -90', roll=90, spin=-70, s0=5.5, s1=8.8, life=8, fade=3),
            card('burst', '^ ^0.2 ^1.2', bb='center', roll=15, s0=0.5, s1=2.6, life=4, fade=2),
            card('glow', '^ ^0.05 ^1.2', '~ 90', s0=1, s1=3.4, life=6, fade=3, col=rgb('#9BE84A')),
            dust(rgb('#C1F788'), 1.5, '^ ^0.3 ^1.2', (0.5, 0.1, 0.5), 8),
            dust_fade(rgb('#E5FBC8'), rgb('#297272'), 1.2, '^ ^2.5 ^0.6', (0.3, 1.6, 0.6), 10),
            part('end_rod', '^ ^0.4 ^1.2', (0.3, 0.2, 0.3), 0.08, 5),
            part('cherry_leaves', '^ ^1 ^1', (0.6, 1.0, 0.6), 0, 5)]


@preset('kick_axe', 'H1 hit 2: the huge diagonal axe-kick crescent from above-behind down to the floor ahead '
        '(r about 5). At her feet, rotated as the kick.')
def _p_kick_axe():
    return [card('cres_lime', '^ ^1.2 ^0.4', '~15 -45', roll=90, spin=-60, s0=7.0, s1=10.5, life=8, fade=3),
            card('cres_lime', '^ ^1.0 ^0.4', '~15 -40', roll=90, spin=-50, s0=6.0, s1=9.0, life=7, fade=3,
                 col=rgb('#E6F4E0')),
            card('burst', '^ ^0.3 ^3', bb='center', roll=20, s0=1, s1=3.8, life=5, fade=2),
            part('explosion', '^ ^0.3 ^3', (0.3, 0.1, 0.3), 0, 1),
            dust_fade(rgb('#EDF9DA'), rgb('#4F9C81'), 1.6, '^ ^0.4 ^3', (1.2, 0.2, 1.2), 12),
            part('end_rod', '^ ^0.5 ^3', (0.8, 0.3, 0.8), 0.12, 6)]


@preset('ground_wave', 'H1 hit 2 ground wave: lime blades erupt one after another along 6 blocks ahead, plus a '
        'streak on the floor. At the floor point, rotated as the line.')
def _p_ground_wave():
    rnd = random.Random(40)
    out = [card('streak', '^ ^0.1 ^3', '~90 90', s0=1.0, s1=6.5, life=8, fade=4, col=LIME_PALE, dur=3)]
    for k in range(8):
        z = 0.6 + 0.75 * k
        x = rnd.uniform(-0.6, 0.6)
        out.append(card('blade', f'^{num(x, 2)} ^ ^{num(z, 2)}', f'~{rnd.randint(-40, 40)} {rnd.randint(-8, 12)}',
                        roll=rnd.randint(-22, 22), s0=0.3, s1=rnd.uniform(1.6, 2.4), life=9, fade=3,
                        dly=k // 2, dur=3))
    out += [dust(rgb('#A8DF74'), 1.6, '^ ^0.3 ^3', (0.4, 0.2, 2.0), 14), part('composter', '^ ^0.4 ^3', (0.4, 0.3, 2.2), 0, 8)]
    return out


@preset('shard_tell', 'H2 tell: one arm shard glows into a lime crescent blade (13 t). At the shard.')
def _p_shard_tell():
    return [card('star4', '~ ~ ~', bb='center', spin=60, s0=0.2, s1=1.0, life=13, fade=4),
            card('glow', '~ ~ ~', bb='center', s0=0.5, s1=1.4, life=13, fade=4, col=LIME),
            dust(rgb('#B8F060'), 0.9, '~ ~ ~', (0.15, 0.4, 0.15), 4)]


@preset('sweep', 'H2 360-degree low sweep (r 3, active 6 t): two knee-high lime crescents turning around her. '
        'At her feet.')
def _p_sweep():
    return [card('cres_lime', '^ ^0.5 ^', '~ 0', spin=170, s0=5.0, s1=6.2, life=8, fade=3),
            card('cres_lime', '^ ^0.55 ^', '~180 0', spin=170, s0=5.0, s1=6.2, life=8, fade=3),
            part('sweep_attack', '^ ^0.6 ^2', (1.2, 0.1, 1.2), 0, 3),
            dust(rgb('#D6FAC5'), 1.3, '^ ^0.4 ^', (2.0, 0.1, 2.0), 14)]


@preset('spiral_jump', 'H2 spiral jump: two lime spiral ribbons wind up around her. At her feet.')
def _p_spiral_jump():
    return [card('cres_lime', '^ ^0.4 ^', '~ 0', spin=170, s0=2.0, s1=3.4, move=(0, 1.6, 0), life=8, fade=3),
            card('cres_lime', '^ ^1.2 ^', '~180 0', spin=170, s0=2.0, s1=3.0, move=(0, 1.8, 0), life=8, fade=3,
                 dly=2),
            dust(rgb('#AADB84'), 1.2, '~ ~1 ~', (0.6, 1.0, 0.6), 10)]


@preset('orb_star', 'H2 star flash at the orb (and any white 4-point flash). Billboard.')
def _p_orb_star():
    return [card('star4', '~ ~ ~', bb='center', spin=45, s0=0.4, s1=3.4, life=5, fade=2),
            card('glow', '~ ~ ~', bb='center', s0=1.2, s1=3.2, life=4, fade=2, col=WHITE),
            part('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.15, 8)]


@preset('orb_kick', 'H2 orb burst as it is kicked down: lime starburst and two white wind crescents circling it.')
def _p_orb_kick():
    return [card('burst', '~ ~ ~', bb='center', spin=30, s0=1, s1=4.2, life=5, fade=2),
            card('cres_cyan', '~ ~ ~', '~ -20', spin=170, s0=3.4, s1=4.4, life=7, fade=3, col=rgb('#EEF6F2')),
            card('cres_cyan', '~ ~ ~', '~180 20', spin=170, s0=3.4, s1=4.4, life=7, fade=3, col=rgb('#EEF6F2')),
            part('end_rod', '~ ~ ~', (0.4, 0.4, 0.4), 0.18, 8)]


@preset('disc_fall', 'H2 the Dendro disc drops {h} blocks onto the floor point in 3 t (call at the floor point; '
        'the disc starts h above).', ('h',))
def _p_disc_fall():
    return ['$' + card('disc_lime', '~ ~$(h) ~', '~ 0', s0=(2.6, 1, 2.6), s1=(3.0, 1, 3.0),
                       move=(0, '-$(h)', 0), life=4, fade=0, dur=3)]


@preset('disc_impact', 'H2 disc impact (r 2.5): lime disc splash, burst, ripple, dust puffs and leaves. At the '
        'floor point.')
def _p_disc_impact():
    return [card('disc_lime', '~ ~0.05 ~', '~ 0', spin=40, s0=2.0, s1=5.4, life=12, fade=6),
            card('burst', '~ ~0.6 ~', bb='center', s0=1, s1=4, life=5, fade=2),
            card('ripple', '~ ~0.07 ~', '~ 90', s0=1, s1=6.5, life=8, fade=3, col=LIME_PALE),
            dust(rgb('#A8DF74'), 3.0, '~ ~0.8 ~', (1.0, 0.6, 1.0), 14),
            dust(rgb('#8DC07E'), 2.4, '~ ~0.5 ~', (1.2, 0.3, 1.2), 10),
            part('cherry_leaves', '~ ~1 ~', (1.2, 0.8, 1.2), 0, 8), part('composter', '~ ~0.3 ~', (1.0, 0.2, 1.0), 0, 8)]


@preset('dash_charge', 'H3 mote charge (10 t): motes converge on her and a faint floor glow. At her feet.')
def _p_dash_charge():
    rnd = random.Random(10)
    out = [card('glow', '~ ~0.05 ~', '~ 90', s0=1.5, s1=3.8, life=12, fade=3, col=LIME)]
    for yaw in radial(8, 11):
        y = rnd.uniform(0.3, 2.2)
        x, z = -1.7 * math.sin(math.radians(yaw)), 1.7 * math.cos(math.radians(yaw))
        out.append(card('glint', f'^{num(x, 2)} ^{num(y, 2)} ^{num(z, 2)}', f'~{ang(yaw)} 0', s0=0.3, s1=0.12,
                        move=(0, 0, -1.5), roll=rnd.randint(0, 45), life=10, fade=2, col=rgb('#C7DB75')))
    return out


@preset('dash_streak', 'H3 dash: a 5.5-block speed streak along the dash path. At her start point, rotated '
        'along the dash.')
def _p_dash_streak():
    return [card('streak', '^ ^0.9 ^2.75', '~90 0', s0=2.0, s1=5.5, life=6, fade=3, col=LIME_PALE),
            card('streak', '^ ^1.4 ^2.5', '~90 0', s0=1.5, s1=4.5, life=5, fade=3, col=WHITE),
            dust(rgb('#E6F6F8'), 1.0, '^ ^1 ^2.5', (0.2, 0.3, 2.2), 10)]


@preset('kick_burst', 'H3 kick + Dendro ring r 3.5: white-lime burst at the foot, flung blades, a floor ripple and '
        'the all-around crescent ring. At her feet.')
def _p_kick_burst():
    rnd = random.Random(15)
    out = [card('burst', '^ ^1.2 ^1', bb='center', roll=20, s0=1.2, s1=5.0, life=5, fade=2),
           card('glow', '^ ^1.2 ^1', bb='center', s0=2, s1=5, life=4, fade=2, col=rgb('#F9FDE0')),
           card('ripple', '~ ~0.06 ~', '~ 90', s0=1.5, s1=7.6, spin=60, life=8, fade=3, col=LIME_PALE),
           card('cres_lime', '~ ~0.8 ~', '~ 0', spin=170, s0=5.5, s1=7.2, life=7, fade=3),
           card('cres_lime', '~ ~0.9 ~', '~180 0', spin=170, s0=5.5, s1=7.2, life=7, fade=3)]
    for yaw in radial(8, 9):
        out.append(card('blade', '~ ~0.8 ~', f'~{ang(yaw)} {ang(90 - rnd.uniform(5, 30))}', roll=rnd.randint(-15, 15),
                        s0=0.4, s1=1.3, move=(0, rnd.uniform(1.8, 2.8), 0), life=8, fade=3))
    out += [part('explosion', '^ ^1 ^1', (0.2, 0.2, 0.2), 0, 1), dust(rgb('#74E542'), 1.6, '~ ~0.8 ~', (2.0, 0.3, 2.0), 16)]
    return out


@preset('vac_crouch', 'H4 crouch: the kicking leg glows lime (9 t). At the foot.')
def _p_vac_crouch():
    return [card('glow', '~ ~0.3 ~', bb='center', s0=0.4, s1=1.4, life=10, fade=3, col=LIME),
            dust(rgb('#C9F2AD'), 0.9, '~ ~0.4 ~', (0.15, 0.3, 0.15), 5)]


@preset('vac_glint', 'H4 tell: a green spike flares behind her, a horizontal cyan-white glint line and a 4-point '
        'flare at the foot. At the foot, rotated as her.')
def _p_vac_glint():
    return [card('blade', '^ ^ ^-0.7', '~ 0', s0=0.5, s1=3.0, life=8, fade=3),
            card('streak', '^ ^0.5 ^0.3', '~ 0', bb='center', s0=1.0, s1=4.0, life=6, fade=3, col=CYAN),
            card('star4', '^ ^0.5 ^0.3', bb='center', spin=45, s0=0.3, s1=1.6, life=6, fade=3)]


@preset('vac_stomp', 'H4 stomp: yellow-green ground flare at the foot as the blade rises. At the floor point.')
def _p_vac_stomp():
    return [card('burst', '~ ~0.5 ~', bb='center', s0=0.6, s1=2.4, life=4, fade=2),
            card('glow', '~ ~0.05 ~', '~ 90', s0=0.8, s1=2.6, life=6, fade=3, col=rgb('#E2FC88')),
            dust(rgb('#FBFDE1'), 1.4, '~ ~0.4 ~', (0.4, 0.3, 0.4), 8)]


@preset('vac_trail', 'H4 travelling blade, every 2 t at the blade prop: small blades and leaves left behind, a '
        'dark-green scar. At the prop (floor height).')
def _p_vac_trail():
    return [card('blade', '^ ^ ^-0.5', '~ 0', roll=12, s0=0.3, s1=0.8, life=6, fade=3),
            dust(rgb('#2F5A3A'), 1.2, '~ ~0.05 ~', (0.4, 0.0, 0.4), 3),
            dust(rgb('#A9E97D'), 1.4, '~ ~1.5 ~', (0.4, 1.2, 0.4), 4),
            part('cherry_leaves', '~ ~1 ~', (0.5, 0.8, 0.5), 0, 1)]


@preset('tf_sheath', 'Transformation: the green vertical glow sheath wraps her lower body. At her chest.')
def _p_tf_sheath():
    return [card('glow', '~ ~ ~', bb='vertical', s0=(1.2, 2.2, 1), s1=(2.0, 3.4, 1), life=8, fade=3,
                 col=rgb('#C2FA72')),
            dust(rgb('#B5F089'), 1.2, '~ ~-0.4 ~', (0.4, 0.8, 0.4), 10)]


@preset('tf_sphere', 'Transformation: core flash, then the light sphere r 2.5 (6 t). At her chest.')
def _p_tf_sphere():
    return [card('sphere', '~ ~ ~', bb='center', spin=20, s0=0.8, s1=5.2, life=7, fade=2),
            card('glow', '~ ~ ~', bb='center', s0=1.5, s1=6.0, life=5, fade=2, col=rgb('#F8FDBB')),
            card('star4', '~ ~ ~', bb='center', spin=45, s0=0.5, s1=2.4, life=4, fade=2)]


@preset('tf_ripples', 'Transformation: concentric ripple rings r 4-5 (a floor ring and two vertical arcs) and '
        'radial speed lines. At her chest; the floor ring is drawn 1.6 below.')
def _p_tf_ripples():
    out = [card('ripple', '~ ~-1.55 ~', '~ 90', spin=50, s0=2, s1=10, life=9, fade=3, col=rgb('#D0F2B9')),
           card('ripple', '~ ~ ~', '~ 0', spin=40, s0=2, s1=8.5, life=8, fade=3, col=rgb('#BDE592')),
           card('ripple', '~ ~ ~', '~90 0', spin=-40, s0=2, s1=9, life=8, fade=3, col=rgb('#D0F2B9'))]
    for yaw in radial(8, 22):
        out.append(card('streak', '~ ~ ~', f'~{ang(yaw + 90)} 0', s0=1.0, s1=2.4, move=(3.6, 0, 0), life=6, fade=2,
                        col=rgb('#5BEAA0')))
    return out


@preset('wing_band', 'B1 hit: the bright yellow-green ground slash band along the wing path (r 4 arc on the '
        'floor). At the floor under her, rotated as the strike.')
def _p_wing_band():
    return [card('cres_lime', '~ ~0.12 ~', '~ 0', spin=-60, s0=6.5, s1=8.5, life=8, fade=4, col=rgb('#F2FFD8')),
            dust(rgb('#D4FA88'), 1.5, '^ ^0.3 ^3', (2.0, 0.1, 1.0), 12)]


@preset('wing_flare', 'B1 trailing vertical crescent flare (2-3 b) at the end of the arc. At the wing tip.')
def _p_wing_flare():
    return [card('cres_lime', '~ ~0.2 ~', '~ -90', roll=90, spin=-60, s0=3.5, s1=5.5, life=7, fade=3),
            part('cherry_leaves', '~ ~1 ~', (0.5, 1.0, 0.5), 0, 4)]


@preset('pyro_switch', 'Wings turn Pyro: a magenta-pink rim glow pulse around her (1 t swap). At her chest.')
def _p_pyro_switch():
    return [card('glow', '~ ~0.4 ~', bb='center', s0=2.0, s1=5.5, life=6, fade=3, col=rgb('#E26E50')),
            card('glow', '~ ~0.4 ~', bb='center', s0=1.0, s1=3.0, life=5, fade=2, col=rgb('#F2C3A8')),
            part('small_flame', '~ ~0.5 ~', (1.6, 1.2, 1.6), 0.01, 10)]


@preset('dendro_switch', 'Wings turn back to Dendro: a lime glow pulse. At her chest.')
def _p_dendro_switch():
    return [card('glow', '~ ~0.4 ~', bb='center', s0=2.0, s1=5.5, life=6, fade=3, col=LIME),
            dust(rgb('#D4F298'), 1.2, '~ ~0.5 ~', (1.6, 1.2, 1.6), 10)]


@preset('fire_swing', 'B2 swing: a giant flame sheet in the swing plane (r 4) with white wind streaks. At her '
        'chest, rotated as the swing (roll the plane with an execute rotated / the diagonal variant).')
def _p_fire_swing():
    return [card('cres_fire', '~ ~ ~', '~ -32', roll=12, spin=150, s0=6.5, s1=8.8, life=7, fade=3),
            card('cres_fire', '~ ~0.3 ~', '~25 -20', roll=-10, spin=140, s0=5.5, s1=7.6, life=6, fade=3,
                 col=rgb('#FFE8C8')),
            card('streak', '^ ^0.3 ^2', '~90 0', s0=2, s1=6, life=5, fade=2, col=rgb('#FBF9F9')),
            part('flame', '^ ^ ^2.5', (2.0, 0.4, 2.0), 0.05, 14), part('small_flame', '^ ^ ^3', (2.5, 0.6, 2.5), 0.02, 10),
            dust_fade(rgb('#F9E38E'), rgb('#C680A2'), 1.8, '^ ^0.2 ^3', (2.4, 0.6, 2.4), 12)]


@preset('fire_swing_d', 'B2 swing, diagonal plane (upper-left to lower-right). At her chest, rotated as her.')
def _p_fire_swing_d():
    return [card('cres_fire', '~ ~0.3 ~', '~ 0', roll=-38, spin=150, s0=6.5, s1=8.5, life=7, fade=3),
            card('cres_fire', '~ ~0.5 ~', '~20 0', roll=-30, spin=140, s0=5.5, s1=7.5, life=6, fade=3,
                 col=rgb('#FFE8C8')),
            part('flame', '^ ^ ^2.5', (2.0, 1.2, 2.0), 0.05, 14),
            dust_fade(rgb('#F9E38E'), rgb('#C680A2'), 1.8, '^ ^0.3 ^3', (2.4, 1.2, 2.4), 12)]


@preset('fire_spawn', 'B2: a fire crescent appears in the air (small puff + embers). At the crescent.')
def _p_fire_spawn():
    return [card('flame_puff', '~ ~ ~', bb='center', spin=90, s0=0.3, s1=1.2, life=5, fade=2),
            part('small_flame', '~ ~ ~', (0.2, 0.2, 0.2), 0.03, 4)]


@preset('fire_trail', 'B2 / B3: a short flame puff left behind a moving fire crescent (call every 1-2 t at the '
        'prop).')
def _p_fire_trail():
    return [card('flame_puff', '~ ~ ~', bb='center', roll=40, spin=-60, s0=0.6, s1=0.25, life=6, fade=3),
            part('small_flame', '~ ~ ~', (0.08, 0.08, 0.08), 0.01, 1)]


@preset('fire_land', 'B2 crescent landing: fire splash r 1.2 with a 2.5-block vertical flame streak. At the '
        'floor point.')
def _p_fire_land():
    # 5 cards (2 radial tongues, was 4): five landings of a swing plus a cure and the dew pulses stay under the 64-card
    # cap in a real fight (review fix FX-2)
    out = [card('flame_tongue', '~ ~ ~', bb='vertical', s0=(0.5, 0.8, 0.5), s1=(1.1, 3.2, 1.1), life=8, fade=3),
           card('flame_puff', '~ ~0.4 ~', bb='center', s0=0.8, s1=2.2, life=6, fade=3),
           card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=2.6, life=8, fade=4, col=ORANGE)]
    for yaw in radial(2, 30):
        out.append(card('flame_tongue', '^ ^ ^', f'~{ang(yaw)} 0', s0=0.2, s1=1.1, move=(0, 0, 0.9), life=7, fade=3))
    out += [part('lava', '~ ~0.2 ~', (0.3, 0.1, 0.3), 0, 3), part('flame', '~ ~0.3 ~', (0.6, 0.2, 0.6), 0.04, 8)]
    return out


@preset('flame_slam', 'B3 slam: two vertical flame crescents rise at the wing tips. At her chest, rotated as her.')
def _p_flame_slam():
    return [card('cres_fire', '^2.6 ^-0.4 ^0.6', '~ -90', roll=90, spin=-50, s0=2.8, s1=4.8, life=6, fade=3),
            card('cres_fire', '^-2.6 ^-0.4 ^0.6', '~ -90', roll=90, spin=-50, s0=2.8, s1=4.8, life=6, fade=3),
            part('flame', '^ ^-1 ^1.5', (2.0, 0.2, 0.8), 0.06, 10)]


@preset('flame_fan', 'B3 eruption: the 180-degree front flame fan r 4.5, 2.5 tall (t28-32) with a scorched floor '
        'sheet. At the floor under her, rotated as her.')
def _p_flame_fan():
    rnd = random.Random(28)
    out = [card('fan_fire', '~ ~0.06 ~', '~ 0', s0=2.0, s1=9.6, life=14, fade=5, dur=3)]
    for ring, (r, n, h) in enumerate(((2.0, 6, 2.3), (3.6, 8, 3.0))):
        for k in range(n):
            a = -80 + 160 * (k + rnd.uniform(0.2, 0.8)) / n
            x, z = -r * math.sin(math.radians(a)), r * math.cos(math.radians(a))
            out.append(card('flame_tongue', f'^{num(x, 2)} ^ ^{num(z, 2)}', f'~{ang(a)} 0', roll=rnd.randint(-10, 10),
                            s0=0.3, s1=(h * 1.6, h * rnd.uniform(0.85, 1.15), 1), life=8, fade=3,
                            dly=ring, dur=3))
    out += [part('flame', '^ ^0.4 ^2.5', (2.4, 0.6, 1.4), 0.06, 22), part('lava', '^ ^0.3 ^2.5', (2.0, 0.2, 1.2), 0, 6),
            part('large_smoke', '^ ^1.2 ^2.5', (2.0, 0.6, 1.2), 0.02, 4)]
    return out


@preset('flame_trail', 'B3 low glide: a flame line on the floor (call every 2 t at the wing-tip floor point).')
def _p_flame_trail():
    return [card('flame_puff', '~ ~0.06 ~', '~ 90', spin=60, s0=1.8, s1=1.1, life=16, fade=7, col=rgb('#F7A090')),
            card('flame_tongue', '~ ~ ~', bb='vertical', s0=0.4, s1=1.0, life=8, fade=4),
            part('small_flame', '~ ~0.2 ~', (0.3, 0.1, 0.3), 0.01, 2)]


@preset('orb_charge', 'B4 wing-wrap charge (14 t): a lime core grows at her chest with converging streaks.')
def _p_orb_charge():
    out = [card('glow', '~ ~ ~', bb='center', s0=0.3, s1=1.6, life=14, fade=3, col=rgb('#D2FA8E')),
           card('star4', '~ ~ ~', bb='center', spin=90, s0=0.2, s1=1.0, life=14, fade=4)]
    for k, roll in enumerate((0, 60, 120)):
        out.append(card('streak', '~ ~ ~', bb='center', roll=roll, s0=3.0, s1=0.3, life=12, fade=2,
                        col=LIME_PALE, dly=k * 2))
    return out


@preset('orb_launch', 'B4 orb release: a lime ring flash and sparkle where the orb leaves her. At the orb.')
def _p_orb_launch():
    return [card('ripple', '~ ~ ~', bb='center', s0=1.2, s1=4.0, spin=60, life=6, fade=2, col=rgb('#D0F0C0')),
            card('glint', '~ ~ ~', bb='center', spin=45, s0=0.4, s1=1.6, life=5, fade=2, col=WHITE)]


@preset('orb_burst', 'B4 orb burst r 2.5-3: starburst, radial V-shaped ground blades, a floor ripple, leaves. At '
        'the floor under the orb.')
def _p_orb_burst():
    rnd = random.Random(46)
    out = [card('burst', '~ ~0.8 ~', bb='center', roll=12, s0=1.2, s1=5.4, life=5, fade=2),
           card('glow', '~ ~0.8 ~', bb='center', s0=2, s1=5.5, life=4, fade=2, col=rgb('#EAFDD9')),
           card('ripple', '~ ~0.06 ~', '~ 90', s0=1, s1=6.6, spin=40, life=8, fade=3, col=rgb('#B4F7B6'))]
    for k, yaw in enumerate(radial(10, 5)):
        r = rnd.uniform(1.0, 2.6)
        x, z = -r * math.sin(math.radians(yaw)), r * math.cos(math.radians(yaw))
        out.append(card('blade', f'^{num(x, 2)} ^ ^{num(z, 2)}', f'~{ang(yaw)} {rnd.randint(15, 30)}',
                        roll=rnd.randint(-12, 12), s0=0.3, s1=rnd.uniform(1.9, 2.9), life=10, fade=3,
                        dly=k % 3, dur=3))
    out += [part('cherry_leaves', '~ ~1 ~', (1.4, 0.8, 1.4), 0, 8), part('composter', '~ ~0.4 ~', (1.4, 0.3, 1.4), 0, 10),
            dust(rgb('#83D394'), 2.0, '~ ~0.5 ~', (1.4, 0.3, 1.4), 10)]
    return out


@preset('cocoon_ball', 'B4 wing ball (12 t): a lime glow inside the ball. At its centre.')
def _p_cocoon_ball():
    return [card('glow', '~ ~ ~', bb='center', s0=2.2, s1=3.2, life=12, fade=3, col=rgb('#CCF39C')),
            dust(rgb('#DEF6D9'), 1.2, '~ ~ ~', (0.9, 0.9, 0.9), 8)]


@preset('rel_fold', 'B5 fold: small lime butterfly glyphs float up around her (20 t). At her chest.')
def _p_rel_fold():
    rnd = random.Random(5)
    out = []
    for k in range(4):
        x, y, z = rnd.uniform(-1.5, 1.5), rnd.uniform(-0.5, 1.0), rnd.uniform(-1.5, 1.5)
        out.append(card('bfly', f'~{num(x, 2)} ~{num(y, 2)} ~{num(z, 2)}', bb='center', roll=rnd.randint(-25, 25),
                        s0=0.2, s1=0.42, move=(0, 0.8, 0), life=20, fade=6, col=rgb('#B8E04C'), dly=k * 3))
    return out


@preset('rel_flare', 'B5 whirl: the pulsing lime 4-point star flare at her side with converging lines (call '
        '2-3 times over the 20 t whirl). At the flare point.')
def _p_rel_flare():
    out = [card('star4', '~ ~ ~', bb='center', spin=90, s0=0.5, s1=2.6, life=9, fade=3),
           card('glow', '~ ~ ~', bb='center', s0=0.8, s1=2.4, life=8, fade=3, col=rgb('#AEE76F'))]
    for k, roll in enumerate((15, 75, 135)):
        out.append(card('streak', '~ ~ ~', bb='center', roll=roll, s0=4.0, s1=0.4, life=7, fade=2, col=LIME_PALE))
    return out


@preset('rel_slashes', 'B5 whirl: thin lime slash streaks whip around her (4 cards). At her chest.')
def _p_rel_slashes():
    rnd = random.Random(22)
    out = []
    for k in range(4):
        out.append(card('streak', '~ ~ ~', f'~{rnd.randint(0, 359)} {rnd.randint(-50, 50)}', roll=rnd.randint(0, 179),
                        spin=170, s0=3.0, s1=5.5, life=5, fade=2, col=rgb('#9FD57F'), dly=k))
    return out


@preset('rel_ground_flash', 'B5 E-18: a lime mist cone bursts from the floor under her. At the floor point.')
def _p_rel_ground_flash():
    return [card('glow', '~ ~0.06 ~', '~ 90', s0=1, s1=5.5, life=7, fade=3, col=rgb('#D3F0B8')),
            card('burst', '~ ~0.3 ~', bb='center', s0=0.8, s1=3.0, life=4, fade=2),
            part('cloud', '~ ~0.4 ~', (0.8, 0.3, 0.8), 0.04, 10)]


@preset('rel_xglint', 'B5 E-16: two long cyan-white lines cross through her chest as an X (8 blocks each). At '
        'her chest (camera-facing).')
def _p_rel_xglint():
    return [card('streak', '~ ~ ~', bb='center', roll=40, s0=2.5, s1=8.5, life=4, fade=2, col=CYAN),
            card('streak', '~ ~ ~', bb='center', roll=-40, s0=2.5, s1=8.5, life=4, fade=2, col=CYAN),
            card('glint', '~ ~ ~', bb='center', spin=45, s0=0.5, s1=1.6, life=4, fade=2, col=WHITE)]


@preset('rel_cage', 'B5 E-15..-10: the gyroscope ring cage r 4 (three spinning lime rings). At her chest.')
def _p_rel_cage():
    s = 4.0 / 0.45
    return [card('gyro', '~ ~ ~', '~ 0', spin=170, s0=s * 0.7, s1=s, life=10, fade=2),
            card('gyro', '~ ~ ~', '~60 -55', spin=-170, s0=s * 0.7, s1=s * 0.96, life=10, fade=2),
            card('gyro', '~ ~ ~', '~-60 50', spin=170, s0=s * 0.7, s1=s * 0.92, life=10, fade=2)]


@preset('rel_pod', 'B5 E-9..-1: the white-lime core glow grows inside the wrapped pod with inward streaks. At '
        'her chest.')
def _p_rel_pod():
    out = [card('glow', '~ ~ ~', bb='center', s0=0.6, s1=3.2, life=10, fade=1, col=rgb('#DFF99C'))]
    for k, roll in enumerate((20, 80, 140)):
        out.append(card('streak', '~ ~ ~', bb='center', roll=roll, spin=90, s0=5.0, s1=0.6, life=8, fade=1,
                        col=rgb('#E5F6DC'), dly=k * 2))
    return out


@preset('rel_dome', 'B5 detonation E: white flash, then the lime dome grows to radius {r} blocks in 5 t (16 shell '
        'segments + cap) and lingers, with a floor shock ring. At the floor under her.', ('r',))
def _p_rel_dome():
    out = ['$' + card('glow', '~ ~1.5 ~', bb='center', s0=3.0, s1='$(r)', life=4, fade=2, col=WHITE)]
    for k, yaw in enumerate(radial(8)):
        for kind, el in (('dome_lo', 20), ('dome_hi', 60)):
            out.append('$' + card(kind, '~ ~ ~', f'~{ang(yaw + (0 if kind == "dome_lo" else 22.5))} {-el}',
                                  s0=0.5, s1='$(r)', life=13, fade=4, dur=5))
    out.append('$' + card('glow', '~ ~ ~', '~ 90', s0=0.5, s1='$(r)', move=(0, 0, 0), life=13, fade=4, dur=5,
                          col=rgb('#A1EB7E')))
    out.append('$' + card('ripple', '~ ~0.08 ~', '~ 90', spin=60, s0=2.0, s1='$(r)', life=10, fade=3, dur=6,
                          col=rgb('#B6FC9D')))
    out += [part('explosion', '~ ~1 ~', (2.0, 1.0, 2.0), 0, 4), part('end_rod', '~ ~2 ~', (3.0, 2.0, 3.0), 0.3, 30),
            part('cherry_leaves', '~ ~3 ~', (4.0, 2.0, 4.0), 0, 16)]
    return out


@preset('rel_tendrils', 'B5 E+7: long lime flame-like tendrils stream out radially as she re-emerges. At her chest.')
def _p_rel_tendrils():
    out = []
    for yaw in radial(8, 15):
        out.append(card('streak', '~ ~ ~', f'~{ang(yaw + 90)} {random.Random(int(yaw)).randint(-25, 25)}', s0=1.5,
                        s1=6.0, move=(4.5, 0, 0), life=9, fade=4, col=rgb('#99E358')))
    return out


@preset('embers', 'After the blast: amber ember petals and lime motes drift down (E+10..+34). Around her chest.')
def _p_embers():
    rnd = random.Random(34)
    out = []
    for k in range(6):
        x, y, z = rnd.uniform(-2.5, 2.5), rnd.uniform(0.5, 2.5), rnd.uniform(-2.5, 2.5)
        out.append(card('leaf', f'~{num(x, 2)} ~{num(y, 2)} ~{num(z, 2)}', bb='center', roll=rnd.randint(0, 90),
                        spin=150, s0=0.18, s1=0.14, move=(0, -1.2, 0), life=26, fade=6,
                        col=AMBER if k % 2 else rgb('#FFEBB5'), dly=rnd.randint(0, 10)))
    return out


@preset('wing_shatter', 'B5 E+38 / death: the shrunken lime wings break into shards (12 cards). At her back.')
def _p_wing_shatter():
    rnd = random.Random(38)
    out = [card('glow', '~ ~ ~', bb='center', s0=2.0, s1=4.5, life=4, fade=2, col=rgb('#E7FD7A'))]
    for yaw in radial(10, 3):
        el = rnd.uniform(-20, 50)
        out.append(card('shard', '~ ~ ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(-30, 30), s0=0.8,
                        s1=rnd.uniform(0.9, 1.4), move=(0, rnd.uniform(2.0, 3.2), 0), life=10, fade=5,
                        col=rgb('#DBF796')))
    out += [part('cherry_leaves', '~ ~ ~', (1.5, 1.0, 1.5), 0, 8), dust(rgb('#E7FD7A'), 1.5, '~ ~ ~', (1.8, 1.0, 1.8), 14)]
    return out


@preset('chain_reform', 'After the groggy turn: lime streaks converge on her side as the crescent chain re-forms '
        '(18 t). At the chain point.')
def _p_chain_reform():
    out = [card('glow', '~ ~ ~', bb='vertical', s0=(0.4, 1.0, 1), s1=(0.8, 2.6, 1), life=18, fade=5,
                col=rgb('#C2E18C'))]
    for k, roll in enumerate((10, 70, 130)):
        out.append(card('streak', '~ ~ ~', bb='center', roll=roll, s0=3.0, s1=0.3, life=8, fade=2, col=LIME_PALE,
                        dly=k * 3))
    return out


@preset('coc_apply', '달빛 고치 applied: a maroon swirl ring closes on the player and a salmon glow. At the '
        'player\'s feet.')
def _p_coc_apply():
    return [card('ripple', '~ ~0.06 ~', '~ 90', spin=-120, s0=4.0, s1=1.2, life=10, fade=3, col=rgb('#A8545E')),
            card('glow', '~ ~1 ~', bb='center', s0=2.4, s1=1.0, life=10, fade=3, col=rgb('#E8858A')),
            card('bfly', '~ ~2.3 ~', bb='center', s0=0.5, s1=0.7, move=(0, 0.3, 0), life=14, fade=4, col=SALMON),
            dust(rgb('#8C525C'), 1.4, '~ ~1 ~', (0.4, 0.8, 0.4), 12)]


@preset('cure', '달빛 고치 removed (about 20 t): gold beam down (6 t), gold burst + ring (5 t), gold emblem with '
        'sparkles (9 t). At the player\'s feet.')
def _p_cure():
    rnd = random.Random(20)
    out = [card('cure_beam', '~ ~ ~', bb='vertical', s0=(0.6, 4.0, 1), s1=(1.6, 3.2, 1), life=9, fade=3),
           card('glint', '~ ~5 ~', bb='center', spin=45, s0=0.4, s1=1.2, move=(0, -2.5, 0), life=6, fade=2, col=GOLD_PALE),
           card('cure_burst', '~ ~1 ~', bb='center', spin=30, s0=0.6, s1=3.4, life=7, fade=3, dly=6),
           card('ripple', '~ ~0.07 ~', '~ 90', spin=50, s0=1.2, s1=5.2, life=8, fade=3, col=rgb('#E0DD9C'), dly=6),
           card('cure_emblem', '~ ~2.6 ~', bb='vertical', s0=0.6, s1=1.45, life=12, fade=4, dly=11, dur=3)]
    for k in range(6):
        x, z = rnd.uniform(-1.2, 1.2), rnd.uniform(-1.2, 1.2)
        out.append(card('glint', f'~{num(x, 2)} ~{num(rnd.uniform(2.5, 3.6), 2)} ~{num(z, 2)}', bb='center', spin=60,
                        s0=0.15, s1=0.35, move=(0, -1.6, 0), life=10, fade=4, col=GOLD, dly=11 + k))
    out += [part('end_rod', '~ ~2 ~', (0.15, 1.5, 0.15), 0.01, 10), part('wax_on', '~ ~1 ~', (0.8, 0.8, 0.8), 0, 10)]
    return out


@preset('dew_spawn', 'A 달빛 이슬 orb appears: a cyan-lime floor ripple, a glow and motes. At the orb\'s floor point.')
def _p_dew_spawn():
    return [card('ripple', '~ ~0.06 ~', '~ 90', spin=60, s0=0.5, s1=3.2, life=10, fade=4, col=rgb('#BFF5E4')),
            card('glow', '~ ~1 ~', bb='center', s0=0.4, s1=2.0, life=8, fade=3, col=rgb('#C8F5E6')),
            part('end_rod', '~ ~1 ~', (0.2, 0.4, 0.2), 0.04, 6)]


@preset('dew_pulse', 'Idle pulse of a 달빛 이슬 orb (call every 20 t at the orb): a soft ring on the floor and two '
        'rising motes, so it reads on the marble.')
def _p_dew_pulse():
    return [card('ripple', '~ ~-0.94 ~', '~ 90', s0=0.6, s1=2.0, life=12, fade=5, col=rgb('#9FE2C8')),
            card('mote', '~0.2 ~0.1 ~', bb='center', s0=0.14, s1=0.2, move=(0, 1.0, 0), life=16, fade=5, col=OPAL),
            card('mote', '~-0.2 ~-0.2 ~0.1', bb='center', s0=0.12, s1=0.18, move=(0, 1.2, 0), life=18, fade=5,
                 col=LIME_PALE, dly=6)]


@preset('death_motes', 'Death: rising moonlight motes and crystal shards (call every 10-20 t of the 100 t death). '
        'Around her chest.')
def _p_death_motes():
    rnd = random.Random(100)
    out = []
    for k in range(7):
        x, y, z = rnd.uniform(-0.7, 0.7), rnd.uniform(-1.2, 0.6), rnd.uniform(-0.7, 0.7)
        out.append(card('mote', f'~{num(x, 2)} ~{num(y, 2)} ~{num(z, 2)}', bb='center', s0=0.14, s1=0.22,
                        move=(0, rnd.uniform(1.8, 2.8), 0), life=rnd.randint(16, 24), fade=6,
                        col=LIME_PALE if k % 2 else OPAL, dly=rnd.randint(0, 8)))
    for k in range(3):
        out.append(card('shard', f'~{num(rnd.uniform(-0.6, 0.6), 2)} ~{num(rnd.uniform(-0.8, 0.4), 2)} ~', bb='center',
                        roll=rnd.randint(-40, 40), spin=90, s0=0.3, s1=0.5, move=(0, 2.2, 0), life=18, fade=6,
                        dly=rnd.randint(0, 8)))
    return out


# ----------------------------------------------------------------------------- datapack


class Writer:
    def __init__(self, dp):
        self.root = Path(dp) / FDIR
        self.files = {}

    def w(self, rel, lines):
        text = '\n'.join(lines) if not isinstance(lines, str) else lines.strip('\n')
        for i, line in enumerate(text.split('\n'), 1):
            s = line.lstrip()
            if s.startswith('$'):
                assert '$(' in s, f'{rel}:{i} macro line without $(var): {s[:90]}'
            elif '$(' in s and not s.startswith('#'):
                raise AssertionError(f'{rel}:{i} $(var) in a non-macro line: {s[:90]}')
        assert rel not in self.files, rel
        self.files[rel] = HEADER + text + '\n'

    def flush(self):
        removed = 0
        for d in OWNED_DIRS:
            p = self.root / d
            if p.exists():
                for f in sorted(p.rglob('*.mcfunction')):
                    if f.relative_to(self.root).with_suffix('').as_posix() not in self.files:
                        f.unlink()
                        removed += 1
                for f in sorted(p.rglob('*'), reverse=True):
                    if f.is_dir() and not any(f.iterdir()):
                        f.rmdir()
        for name in OWNED_FILES:
            f = self.root / f'{name}.mcfunction'
            if f.exists() and name not in self.files:
                f.unlink()
                removed += 1
        for rel, text in self.files.items():
            top = rel.split('/')[0]
            assert top in OWNED_DIRS or rel in OWNED_FILES, rel
            p = self.root / f'{rel}.mcfunction'
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists() or p.read_text(encoding='utf-8') != text:
                p.write_text(text, encoding='utf-8')
        return removed


HEADER = '# Generated by tools/build_mboss_bf_fx.py (butterfly fx kit) - edit the generator, not this file.\n'
E = FN + 'e/'
SEL = '@e[type=minecraft:item_display,tag=rlk_bk'


def engine(W):
    W.w('card', [
        '# Spawn one painted card at pos, rotated rot (fixed cards), seen from the executing context.',
        '# {kind, pos:"^x ^y ^z", rot:"~ ~", bb:fixed|center|vertical|horizontal, roll:<deg, about local z>,',
        '#  spin:<deg over the main interpolation, -170..170, about the card normal>, s0:<start size>, s1:<end size>,',
        '#  move:"dx,dy,dz" (end offset, display frame: +x left, +y up, +z forward), life:<ticks>, fade:<shrink-out',
        '#  ticks>, col:<RGB int tint, 16777215 = the painted colours>}. Kinds and presets: bf_fx_api.md.',
        f'# Skipped (no error) while {CAP} fx cards are alive.',
        f'execute if score #bkN mb matches {CAP}.. run return 0',
        '$data modify storage rlk:bfkit a set value {kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)f,$(s0)f,$(s0)f",s1:"$(s1)f,$(s1)f,$(s1)f",move:"$(move)",col:$(col),col2:-1,ax:"0f,0f,1f"}',
        f'execute unless data storage {STO} ax.cres_lime run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #bkRoll mb $(roll)',
        '$scoreboard players set #bkSpin mb $(spin)',
        '$scoreboard players set #bkLife mb $(life)',
        '$scoreboard players set #bkFade mb $(fade)',
        'scoreboard players set #bkDly mb 0',
        'scoreboard players set #bkDur mb 0',
        'scoreboard players set #bkHit mb -1',
        'scoreboard players set #bkTel mb 0',
        f'function {E}make',
    ])
    W.w('cardx', [
        '# card with every option: s0 / s1 as "xf,yf,zf" vectors, dly:<ticks hidden before it shows>, dur:<ticks',
        '# of the main interpolation, 0 = up to the fade>, hit:<ticks after the call when the tint becomes col2,',
        '# -1 = never>, col2:<RGB int>. Same cap as card.',
        f'execute if score #bkN mb matches {CAP}.. run return 0',
        '$data modify storage rlk:bfkit a set value {kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)",s1:"$(s1)",move:"$(move)",col:$(col),col2:$(col2),ax:"0f,0f,1f"}',
        f'execute unless data storage {STO} ax.cres_lime run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #bkRoll mb $(roll)',
        '$scoreboard players set #bkSpin mb $(spin)',
        '$scoreboard players set #bkLife mb $(life)',
        '$scoreboard players set #bkFade mb $(fade)',
        '$scoreboard players set #bkDly mb $(dly)',
        '$scoreboard players set #bkDur mb $(dur)',
        '$scoreboard players set #bkHit mb $(hit)',
        'scoreboard players set #bkTel mb 0',
        f'function {E}make',
    ])
    W.w('e/make', [
        '# Internal: storage rlk:bfkit a (kind pos rot bb s0 s1 move col col2 ax) + #bkRoll #bkSpin #bkLife #bkFade',
        '# #bkDly #bkDur #bkHit #bkTel -> one card. Stages (gametime): show at +dly (hidden until then), main',
        '# interpolation from +dly+1 over dur ticks, colour change at +hit, shrink-out over the last fade ticks,',
        '# removal at +dly+life.',
        f'execute unless score #bkInit mb matches 1 run function {E}init',
        'execute if score #bkTel mb matches 1 run scoreboard players add #bkTN mb 1',
        'execute unless score #bkTel mb matches 1 run scoreboard players add #bkN mb 1',
        'execute if score #bkLife mb matches ..1 run scoreboard players set #bkLife mb 2',
        'execute if score #bkFade mb matches ..-1 run scoreboard players set #bkFade mb 0',
        'execute if score #bkDly mb matches ..-1 run scoreboard players set #bkDly mb 0',
        'scoreboard players operation #bkWd mb = #bkLife mb',
        'scoreboard players remove #bkWd mb 2',
        'scoreboard players operation #bkFade mb < #bkWd mb',
        'scoreboard players operation #bkWd mb = #bkLife mb',
        'scoreboard players operation #bkWd mb -= #bkFade mb',
        'scoreboard players remove #bkWd mb 1',
        'execute if score #bkDur mb matches 1.. run scoreboard players operation #bkWd mb = #bkDur mb',
        'execute if score #bkWd mb matches ..0 run scoreboard players set #bkWd mb 1',
        'execute if score #bkSpin mb matches 171.. run scoreboard players set #bkSpin mb 170',
        'execute if score #bkSpin mb matches ..-171 run scoreboard players set #bkSpin mb -170',
        'execute store result storage rlk:bfkit a.rr float 0.017453292 run scoreboard players get #bkRoll mb',
        'execute store result storage rlk:bfkit a.sr float 0.017453292 run scoreboard players get #bkSpin mb',
        'execute store result storage rlk:bfkit a.d int 1 run scoreboard players get #bkWd mb',
        'execute store result storage rlk:bfkit a.f int 1 run scoreboard players get #bkFade mb',
        'execute store result score #bkC2 mb run data get storage rlk:bfkit a.col2',
        'data modify storage rlk:bfkit a.z set from storage rlk:bfkit a.s0',
        'execute if score #bkDly mb matches 1.. run data modify storage rlk:bfkit a.z set value "0f,0f,0f"',
        f'function {E}spawn with storage rlk:bfkit a',
        f'execute if score #bkTel mb matches 1 run tag {SEL}_new] add rlk_bk_t',
        'execute store result score #bkNow mb run time query gametime',
        '# The ager (e/world, scheduled 1t) runs at the end of this same server tick, when the game time already',
        '# reads +1: count the stages from that tick, so the main interpolation starts one tick after the summon (the',
        '# client first gets the start state; merged in the summon tick it would never animate) and every stage, the',
        '# telegraph flash on the strike tick included, lands on its documented tick (review fix perf-2).',
        'scoreboard players add #bkNow mb 1',
        f'execute as {SEL}_new,limit=1] run function {E}born',
        f'tag {SEL}_new] remove rlk_bk_new',
        f'schedule function {E}world 1t replace',
    ])
    end_tr = ('translation:[$(move)],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(s1)],'
              'right_rotation:{angle:$(sr)f,axis:[$(ax)]}')
    W.w('e/spawn', [
        '# Internal (macro, storage rlk:bfkit a): the item_display; the stage snapshots ride on its item.',
        '$summon minecraft:item_display $(pos) {Tags:["rlk_bk","rlk_bk_new","rlk_room","rlk_mb_aux"],'
        'billboard:"$(bb)",item_display:"none",brightness:{sky:15,block:15},view_range:1.5f,shadow_radius:0f,'
        'teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],'
        'left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(z)],right_rotation:[0f,0f,0f,1f]},'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/bf_kit/$(kind)",'
        '"minecraft:custom_model_data":{colors:[$(col)]},"minecraft:custom_data":{'
        'bkS:{start_interpolation:0,interpolation_duration:0,transformation:{scale:[$(s0)]}},'
        'bkG:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'bkF:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}},'
        'bkC:$(col2)}}}}',
        f'$execute positioned $(pos) rotated $(rot) run tp {SEL}_new,limit=1] ~ ~ ~ ~ ~',
    ])
    W.w('e/born', [
        '# Internal, as the new card: stage ticks (gametime) in bkS bkG bkH bkK bkD.',
        'scoreboard players operation @s bkS = #bkNow mb',
        'scoreboard players operation @s bkS += #bkDly mb',
        'scoreboard players operation @s bkG = @s bkS',
        'scoreboard players add @s bkG 1',
        'scoreboard players operation @s bkD = @s bkS',
        'scoreboard players operation @s bkD += #bkLife mb',
        'scoreboard players operation @s bkK = @s bkD',
        'scoreboard players operation @s bkK -= #bkFade mb',
        'scoreboard players operation @s bkH = #bkNow mb',
        'scoreboard players operation @s bkH += #bkHit mb',
        'tag @s add rlk_bk_go',
        'execute if score #bkDly mb matches 1.. run tag @s add rlk_bk_sh',
        'execute if score #bkFade mb matches 1.. run tag @s add rlk_bk_fd',
        'execute if score #bkHit mb matches 0.. if score #bkC2 mb matches 0.. run tag @s add rlk_bk_hit',
    ])
    W.w('e/world', [
        '# Ages the kit\'s cards once per tick while any is alive (scheduled from e/make and from itself; no hook in',
        '# rlk:tick). A dead or reviving player clears them, like Navia\'s cards.',
        f'execute unless entity {SEL},limit=1] run return run function {E}zero',
        f'execute if entity @a[tag=player,scores={{dead=1}}] run return run function {FN}clear',
        f'execute if entity @a[tag=player,scores={{rnDie=1..}}] run return run function {FN}clear',
        'execute store result score #bkNow mb run time query gametime',
        f'execute as {SEL}] run function {E}age',
        f'execute store result score #bkN mb if entity {SEL},tag=!rlk_bk_t]',
        f'execute store result score #bkTN mb if entity {SEL}_t]',
        f'execute if entity {SEL},limit=1] run schedule function {E}world 1t replace',
    ])
    W.w('e/zero', ['scoreboard players set #bkN mb 0', 'scoreboard players set #bkTN mb 0'])
    W.w('e/age', [
        '# As one card (gametime in #bkNow).',
        'execute unless score @s bkD = @s bkD run return run kill @s',
        'execute if score #bkNow mb >= @s bkD run return run kill @s',
        f'execute if entity @s[tag=rlk_bk_sh] if score #bkNow mb >= @s bkS run function {E}show',
        f'execute if entity @s[tag=rlk_bk_go] if score #bkNow mb >= @s bkG run function {E}go',
        f'execute if entity @s[tag=rlk_bk_hit] if score #bkNow mb >= @s bkH run function {E}hit',
        f'execute if entity @s[tag=rlk_bk_fd] if score #bkNow mb >= @s bkK run function {E}fade',
    ])
    W.w('e/show', ['# a delayed card appears at its start size',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".bkS',
                   'tag @s remove rlk_bk_sh'])
    W.w('e/go', ['# start -> end transformation over dur ticks (client interpolation)',
                 'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".bkG',
                 'tag @s remove rlk_bk_go'])
    W.w('e/hit', ['# the tint changes (telegraph flash on the hit tick)',
                  'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set from entity @s '
                  'item.components."minecraft:custom_data".bkC',
                  'tag @s remove rlk_bk_hit'])
    W.w('e/fade', ['# shrink to nothing over the last fade ticks',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".bkF',
                   'tag @s remove rlk_bk_fd'])
    W.w('e/init', ['# Objectives of the kit (created on the first card; removed by fx/uninstall).',
                   *[f'scoreboard objectives add {o} dummy' for o in ('bkS', 'bkG', 'bkH', 'bkK', 'bkD')],
                   'scoreboard players set #bkInit mb 1',
                   'scoreboard players set #bkN mb 0', 'scoreboard players set #bkTN mb 0'])
    W.w('clear', ['# Remove every card of the kit (fx and telegraphs). Safe to call any time.',
                  f'kill {SEL}]', f'function {E}zero'])
    W.w('uninstall', ['# Remove the kit\'s cards, objectives and storage (call from the module\'s uninstall hook).',
                      f'kill {SEL}]',
                      *[f'scoreboard objectives remove {o}' for o in ('bkS', 'bkG', 'bkH', 'bkK', 'bkD')],
                      *[f'scoreboard players reset {s} mb' for s in
                        ('#bkInit', '#bkN', '#bkTN', '#bkNow', '#bkWd', '#bkC2', '#bkRoll', '#bkSpin', '#bkLife',
                         '#bkFade', '#bkDly', '#bkDur', '#bkHit', '#bkTel', '#bkTr', '#bkTr0', '#bkTa', '#bkTl',
                         '#bkTw', '#bkTb', '#bkTell', '#bkTEl', '#bkThold')],
                      f'data remove storage {STO} a', f'data remove storage {STO} t', f'data remove storage {STO} hud',
                      f'data remove storage {STO} ax',
                      f'schedule clear {E}world'])
    flat = ','.join(f'{k}:"0f,1f,0f"' for k, v in KINDS.items() if v[0] == 'flat')
    W.w('e/axes', ['# Spin axis (= card normal) of the flat kinds; face and seg kinds keep the default z axis.',
                   f'data modify storage {STO} ax set value {{{flat}}}'])
    W.w('look', [
        '# Dress @s (an item_display prop, e.g. a projectile) as a kit sprite: {kind, col:<RGB int>}. Full bright;',
        '# the caller keeps its own transformation / billboard (see bf_fx_api.md for the prop recipes).',
        '$data merge entity @s {item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        '"rlk:mboss/bf_kit/$(kind)","minecraft:custom_model_data":{colors:[$(col)]}}},brightness:{sky:15,block:15}}',
    ])


def telegraphs(W):
    T = FN + 'tele/e/'
    cols = []
    for el, (c1, c2, c3) in sorted(TELE_COL.items()):
        cols.append(f'execute if score #bkTEl mb matches {el} run data modify storage {STO} t merge value '
                    f'{{c1:{c1},c2:{c2},c3:{c3}}}')
    W.w('tele/e/prep', [
        '# Internal: common telegraph setup from #bkTell #bkTEl #bkThold (colours by #elem: 7 Dendro, 1 Pyro, 0',
        '# physical; anything else draws Dendro). Life = tell + hold + 1, the fill grows over tell - 1 ticks from',
        '# the tick after the call, so its edge reaches the rim on call + tell (the framework hz strike tick when',
        '# both are made in the same tick with the same tell); every card flashes (col2) on that tick.',
        'execute if score #bkTell mb matches ..1 run scoreboard players set #bkTell mb 2',
        'execute if score #bkThold mb matches ..-1 run scoreboard players set #bkThold mb 0',
        f'data modify storage {STO} t merge value {{c1:{TELE_COL[7][0]},c2:{TELE_COL[7][1]},c3:{TELE_COL[7][2]}}}',
        *cols,
        'scoreboard players operation #bkLife mb = #bkTell mb',
        'scoreboard players operation #bkLife mb += #bkThold mb',
        'scoreboard players add #bkLife mb 1',
        'scoreboard players operation #bkDur mb = #bkTell mb',
        'scoreboard players remove #bkDur mb 1',
        'scoreboard players operation #bkHit mb = #bkTell mb',
        'scoreboard players set #bkFade mb 0',
        'scoreboard players set #bkDly mb 0',
        'scoreboard players set #bkRoll mb 0',
        'scoreboard players set #bkSpin mb 0',
        'scoreboard players set #bkTel mb 1',
    ])
    head = lambda extra: [  # noqa: E731
        f'execute if score #bkTN mb matches {TCAP - 6}.. run return 0',
        '$scoreboard players set #bkTell mb $(tell)',
        '$scoreboard players set #bkTEl mb $(el)',
        '$scoreboard players set #bkThold mb $(hold)',
        *extra,
        f'function {T}prep',
    ]

    def mk(kind, pos, s0, s1, colkey, rot='~ 0', move='0f,0f,0f', grow=True):
        """one telegraph card inside a macro reading storage t (static cards have s0 = s1)"""
        return [f'$data modify storage {STO} a set value {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"fixed",'
                f's0:"{s0}",s1:"{s1}",move:"{move}",col:$({colkey}),col2:$(c3),ax:"0f,1f,0f"}}',
                f'function {E}make']

    # disc
    W.w('tele/disc', [
        '# Disc telegraph decal: {r:<radius, tenths of a block>, tell:<ticks to the hit>, el:<#elem>, hold:<ticks',
        '# it stays after the hit>}. Positioned on the floor point. Visual only: pair it with hz/disc (same tell,',
        f'# #hzQuiet 1 to drop the framework particles). 2 cards; skipped while {TCAP - 6}+ telegraph cards live.',
        *head(['$scoreboard players set #bkTr mb $(r)']),
        'execute if score #bkTr mb matches ..1 run scoreboard players set #bkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #bkTr mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #bkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc with storage {STO} t',
    ])
    W.w('tele/e/disc', [
        '# Internal (macro, storage t): the progress fill (0 -> r) under the static rim.',
        *mk('t_fill', '~ ~0.03 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', 'c2'),
        *mk('$(rim)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1', grow=False),
    ])
    # ring
    W.w('tele/ring', [
        '# Ring telegraph decal (safe hole inside r0): {r0, r (tenths), tell, el, hold}. Positioned on the floor',
        '# point. Outer and inner rims, and a progress ring that travels from r0 to r. 3 cards.',
        *head(['$scoreboard players set #bkTr mb $(r)', '$scoreboard players set #bkTr0 mb $(r0)']),
        'execute if score #bkTr0 mb matches ..1 run scoreboard players set #bkTr0 mb 2',
        'execute if score #bkTr mb <= #bkTr0 mb run scoreboard players operation #bkTr mb = #bkTr0 mb',
        'execute if score #bkTr mb = #bkTr0 mb run scoreboard players add #bkTr mb 5',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #bkTr mb',
        f'execute store result storage {STO} t.r0 float 0.1 run scoreboard players get #bkTr0 mb',
        f'function {T}ring with storage {STO} t',
    ])
    W.w('tele/e/ring', [
        *mk('t_rim', '~ ~0.035 ~', '$(r0)f,1f,$(r0)f', '$(r)f,1f,$(r)f', 'c2'),
        *mk('t_rim', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1', grow=False),
        *mk('t_rim', '~ ~0.046 ~', '$(r0)f,1f,$(r0)f', '$(r0)f,1f,$(r0)f', 'c1', grow=False),
    ])
    # sector
    sel = []
    for lo, hi, h in ((0, 37, 30), (38, 52, 45), (53, 75, 60), (76, 135, 90)):
        sel.append(f'execute if score #bkTa mb matches {lo}..{hi} run data modify storage {STO} t merge value '
                   f'{{sk:"t_sec{h}",sf:"t_secf{h}"}}')
    W.w('tele/sector', [
        '# Sector (arc) telegraph decal: {r (tenths), a:<half-angle deg>, tell, el, hold}. Positioned on the',
        '# apex, rotated = aim (yaw). Half-angles snap to 30 / 45 / 60 / 90 (a >= 136 draws a disc). 2 cards.',
        *head(['$scoreboard players set #bkTr mb $(r)', '$scoreboard players set #bkTa mb $(a)']),
        'execute if score #bkTa mb matches 136.. run return run function ' + T + 'sector_disc',
        'execute if score #bkTr mb matches ..1 run scoreboard players set #bkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #bkTr mb',
        *sel,
        f'execute if score #bkTa mb matches ..0 run data modify storage {STO} t merge value {{sk:"t_sec30",sf:"t_secf30"}}',
        f'function {T}sector with storage {STO} t',
    ])
    W.w('tele/e/sector_disc', [
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #bkTr mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #bkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc with storage {STO} t',
    ])
    W.w('tele/e/sector', [
        *mk('$(sf)', '~ ~0.03 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', 'c2'),
        *mk('$(sk)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1', grow=False),
    ])
    # line
    W.w('tele/line', [
        '# Line / lane telegraph decal: {len, w, back (tenths), tell, el, hold}. Positioned on the start point',
        '# (floor), rotated = aim (yaw); covers -back..len along the aim, w wide (as hz/line + #hzBack). Two',
        '# rails, two caps and the fill growing toward the far end (its bright edge reaches it on the hit). 5 cards.',
        *head(['$scoreboard players set #bkTl mb $(len)', '$scoreboard players set #bkTw mb $(w)',
               '$scoreboard players set #bkTb mb $(back)']),
        'execute if score #bkTl mb matches ..1 run scoreboard players set #bkTl mb 2',
        'execute if score #bkTw mb matches ..1 run scoreboard players set #bkTw mb 2',
        'execute if score #bkTb mb matches ..-1 run scoreboard players set #bkTb mb 0',
        f'execute store result storage {STO} t.len float 0.1 run scoreboard players get #bkTl mb',
        f'execute store result storage {STO} t.w float 0.1 run scoreboard players get #bkTw mb',
        f'execute store result storage {STO} t.hw float 0.05 run scoreboard players get #bkTw mb',
        f'execute store result storage {STO} t.nhw float -0.05 run scoreboard players get #bkTw mb',
        f'execute store result storage {STO} t.nb float -0.1 run scoreboard players get #bkTb mb',
        'scoreboard players operation #bkTl mb += #bkTb mb',
        f'execute store result storage {STO} t.lb float 0.1 run scoreboard players get #bkTl mb',
        f'function {T}line with storage {STO} t',
    ])
    W.w('tele/clear', ['# Remove every telegraph decal of the kit (a cancelled pattern, a pause); fx cards stay.',
                       f'kill {SEL}_t]', f'execute store result score #bkTN mb if entity {SEL}_t]'])
    W.w('tele/e/line', [
        *mk('t_lane', '^ ^0.03 ^$(nb)', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', 'c2'),
        *mk('t_bar', '^$(hw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1', grow=False),
        *mk('t_bar', '^$(nhw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1', grow=False),
        *mk('t_bar', '^$(hw) ^0.046 ^$(nb)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0', grow=False),
        *mk('t_bar', '^$(hw) ^0.046 ^$(len)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0', grow=False),
    ])


PROPS = {
    # name -> (comment, item kind, tint, billboard, transformation SNBT)
    'fire': ('B2 fire crescent projectile: the camera-facing golden claw, 1.4 blocks.', 'fire_claw', WHITE, 'center',
             '{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]}'),
    'vblade': ('H4 vacuum blade: a vertical lime crescent wall facing the flight (in the plane across it, where the '
               'blade hit line is), 4 tall from its lower tip 0.9 below the prop (the pj hit row on the floor) and '
               'about 2.7 across (x -1.33..+1.33 of the hr 1.5 hit), the thick bright head on top, bulging to the '
               'prop\'s left; fly the prop 0.9 above the floor. Cyclic turn x->y, y->z, z->x of the flat card, '
               'chord x4.4, bulge x6.8 (measured by scratchpad mb2/integ/vblade_check.py).', 'cres_lime', WHITE, 'fixed',
               '{translation:[-1.9f,1.02f,0f],left_rotation:[0.5f,0.5f,0.5f,0.5f],scale:[4.4f,1f,6.8f],'
               'right_rotation:[0f,0f,0f,1f]}'),
    'orb': ('B4 coco orb fallback look (when the rig has no orb prop): a lime light sphere 1.7 across.', 'sphere',
            rgb('#D2FA8E'), 'center',
            '{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.7f,1.7f,1.7f],right_rotation:[0f,0f,0f,1f]}'),
    'orb_ring': ('B4 gyroscope ring around an orb (fixed; turn it from the module tick), 2.2 across.', 'gyro', WHITE,
                 'fixed', '{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],'
                 'right_rotation:[0f,0f,0f,1f]}'),
    'dew': ('달빛 이슬 heal orb look (camera-facing, 0.9 across).', 'dew_orb', WHITE, 'center',
            '{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f],right_rotation:[0f,0f,0f,1f]}'),
}


def props(W):
    for name, (doc, kind, col, bb, tr) in PROPS.items():
        W.w(f'prop/{name}', [f'# {doc}', '# As @s = an item_display the module owns (a pj prop or a marker look): item, tint, billboard,',
                             '# full bright, transformation. Keep teleport_duration 1 on moving props for smooth flight.',
                             f'data merge entity @s {{item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":'
                             f'"rlk:mboss/bf_kit/{kind}","minecraft:custom_model_data":{{colors:[{col}]}}}}}},billboard:"{bb}",'
                             f'brightness:{{sky:15,block:15}},view_range:1.5f,shadow_radius:0f,transformation:{tr}}}'])


def sounds(W):
    for name, (doc, layers) in SOUNDS.items():
        W.w(f'snd/{name}', [f'# {doc}', '# Layers: event volume pitch minVolume (per-layer minimum, mboss_lib.sound rule).'] +
            [sound_line(*l) for l in layers])


HUD_FUNCS = ('coc_on', 'coc_off', 'buff_on', 'buff_off', 'clear', 'put_extra', 'put_sub', 'ab_coc', 'ab_buff', 'ab_cure',
             'pop_coc', 'pop_buff', 'flash_white', 'flash_lime', 'flash_gold', 'flash_maroon', 'flash_end')
# The 달빛 고치 cure meter readout (user: "일정 체력 이상 회복해야 하게"): score components of these fake players in objective mb,
# set by the module (the meter and the target in % of max HP); the boss bar re-reads them every tick.
CURE_P, CURE_T = '#bkCureP', '#bkCureT'


def gl(name, extra=''):
    return '{text:"' + glyph(name) + '",font:"' + FONT + '",color:"white"' + extra + '}'


def hud_funcs(W):
    sp = chr(CP_SPACE)
    W.w('hud/coc_on', ['# Show the 달빛 고치 badge (maroon, salmon swirl) on the boss-bar lines (put_extra / put_sub).',
                       f'data modify storage {STO} hud.coc set value 1b', f'function {FN}hud/e/rebuild'])
    W.w('hud/coc_off', [f'data modify storage {STO} hud.coc set value 0b', f'function {FN}hud/e/rebuild'])
    W.w('hud/buff_on', ['# Show the 달빛 축복 받음 reward badge (gold).',
                        f'data modify storage {STO} hud.buff set value 1b', f'function {FN}hud/e/rebuild'])
    W.w('hud/buff_off', [f'data modify storage {STO} hud.buff set value 0b', f'function {FN}hud/e/rebuild'])
    W.w('hud/clear', ['# Both badges off (fight end, death, abort, uninstall).',
                      f'data modify storage {STO} hud merge value {{coc:0b,buff:0b}}', f'function {FN}hud/e/rebuild'])
    W.w('hud/e/rebuild', [
        '# Storage rlk:bfkit hud.ex (name-line suffix: badges) and hud.sub (sub-line: badge + label) from the flags.',
        f'data modify storage {STO} hud.ex set value []',
        f'data modify storage {STO} hud.sub set value []',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.ex append value {{text:"  "}}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.ex append value {gl("coc")}',
        f'execute if data storage {STO} hud{{buff:1b}} run data modify storage {STO} hud.ex append value {{text:"  "}}',
        f'execute if data storage {STO} hud{{buff:1b}} run data modify storage {STO} hud.ex append value {gl("buff")}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value {{text:"     "}}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value {gl("coc")}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value '
        '{text:" 달빛 고치",color:"#E8A0A6"}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value '
        '{text:" — 회복 ",color:"#C9A3A6"}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value '
        f'{{score:{{name:"{CURE_P}",objective:"mb"}},color:"#F2C4C8",bold:true}}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value '
        '{text:"/",color:"#C9A3A6"}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value '
        f'{{score:{{name:"{CURE_T}",objective:"mb"}},color:"#C9A3A6"}}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value '
        '{text:"% ",color:"#C9A3A6"}',
        f'execute if data storage {STO} hud{{coc:1b}} run data modify storage {STO} hud.sub append value {gl("dew")}',
        f'execute if data storage {STO} hud{{buff:1b}} run data modify storage {STO} hud.sub append value {{text:"     "}}',
        f'execute if data storage {STO} hud{{buff:1b}} run data modify storage {STO} hud.sub append value {gl("buff")}',
        f'execute if data storage {STO} hud{{buff:1b}} run data modify storage {STO} hud.sub append value '
        '{text:" 달빛 축복 받음",color:"#F2D27A"}',
        f'execute if data storage {STO} hud{{buff:1b}} run data modify storage {STO} hud.sub append value '
        '{text:" (치명타 +15% · 치명타 피해 +50%)",color:"#BDB38A"}',
    ])
    W.w('hud/put_extra', ['# Append the badges to the boss-bar name line: call at the end of the module\'s line-1 build',
                          '# (after it resets rlk:mboss extra). Same as the component',
                          f'# {{nbt:"hud.ex[]",storage:"{STO}",interpret:true,separator:""}}.',
                          f'data modify storage rlk:mboss extra append from storage {STO} hud.ex[]'])
    W.w('hud/put_sub', ['# Append badge + label(s) to the boss-bar third line (rlk:mboss sub), after the module\'s own text.',
                        f'data modify storage rlk:mboss sub append from storage {STO} hud.sub[]'])
    W.w('hud/ab_coc', ['# One-shot actionbar notice (2 s) for every player: the badge and the hint. Holds the regular',
                       '# actionbar HUD (hudHold) meanwhile.',
                       'title @a[tag=player] actionbar [' + gl('coc') + ',{text:" 달빛 고치",color:"#E8A0A6",bold:true},'
                       '{text:" — 체력 15% 회복하면 해제 · 피해 −50% · 치명타 −100% · 받는 치유 −40%",color:"#C9A3A6"}]',
                       'scoreboard players set @a[tag=player] hudHold 40'])
    W.w('hud/ab_buff', ['# One-shot actionbar notice (2 s): the reward badge and its numbers.',
                        'title @a[tag=player] actionbar [' + gl('buff') + ',{text:" 달빛 축복 받음",color:"#F2D27A",bold:true},'
                        '{text:" — 치명타 +15% · 치명타 피해 +50%",color:"#BDB38A"}]',
                        'scoreboard players set @a[tag=player] hudHold 40'])
    W.w('hud/ab_cure', ['# One-shot actionbar notice (2 s) after a heal that filled the 달빛 고치 cure meter but not to its target:',
                        f'# the badge and "회복 <{CURE_P}>/<{CURE_T}>%" (score components, set by the module).',
                        'title @a[tag=player] actionbar [' + gl('coc') + ',{text:" 달빛 고치",color:"#E8A0A6",bold:true},'
                        '{text:" — 회복 ",color:"#C9A3A6"},'
                        f'{{score:{{name:"{CURE_P}",objective:"mb"}},color:"#F2C4C8",bold:true}},{{text:"/",color:"#C9A3A6"}},'
                        f'{{score:{{name:"{CURE_T}",objective:"mb"}},color:"#C9A3A6"}},{{text:"%",color:"#C9A3A6"}}]',
                        'scoreboard players set @a[tag=player] hudHold 40'])
    for name, g in (('pop_coc', 'coc_big'), ('pop_buff', 'buff_big')):
        W.w(f'hud/{name}', ['# The badge pops big on the title line (1.2 s) and fades; the F5 crosshair title rests (vBig).',
                            'scoreboard players set @a[tag=player] vBig 30',
                            'title @a[tag=player] times 2 18 8',
                            'title @a[tag=player] title [' + gl(g, ',shadow_color:0') + ']'])
    for name, g, t in (('flash_white', 'fl_white', '0 2 5'), ('flash_lime', 'fl_lime', '0 3 9'),
                       ('flash_gold', 'fl_gold', '1 3 8'), ('flash_maroon', 'fl_maroon', '1 4 8')):
        W.w(f'hud/{name}', ['# Full-screen flat flash on the title line (any view mode); vBig rests the F5 crosshair.',
                            'scoreboard players set @a[tag=player] vBig 16',
                            f'title @a[tag=player] times {t}',
                            'title @a[tag=player] title [' + gl(g, ',shadow_color:0') + ',{text:"' + sp + '",font:"' + FONT + '"}]'])
    W.w('hud/flash_end', ['# Drop a title overlay at once (pause, cancel).',
                          'scoreboard players set @a[tag=player] vBig 0',
                          'title @a[tag=player] times 0 1 2', 'title @a[tag=player] title ""'])


def presets_dp(W):
    for name, (doc, args, f) in PRESETS.items():
        lines = f()
        head = [f'# {doc}']
        if args:
            head.append('# {' + ', '.join(args) + '} (macro)')
            assert any(l.startswith('$') for l in lines), name
        else:
            assert not any(l.startswith('$') for l in lines), name
        W.w(f'p/{name}', head + lines)


def tests(W):
    t = ['# Every kind in rows in front of the executor (3 s each):',
         '# /execute as @p at @s rotated ~ 0 run function rlk:mboss/butterfly/fx/test/kinds']
    fx_kinds = [k for k in FX_KINDS if KINDS[k][0] != 'seg']
    for i, kind in enumerate(fx_kinds):
        row, colm = divmod(i, 7)
        x = 4.5 - 1.5 * colm
        z = 4 + 2.2 * row
        plane = KINDS[kind][0]
        if plane == 'flat':
            t.append(card(kind, f'^{num(x)} ^0.05 ^{num(z)}', '~ 0', s0=0.3, s1=1.4, life=60, fade=10))
        else:
            t.append(card(kind, f'^{num(x)} ^1.2 ^{num(z)}', '~180 0', s0=0.3, s1=1.2, life=60, fade=10))
    W.w('test/kinds', t)
    W.w('test/dome', ['# The release dome (r 6) 8 blocks ahead: /execute as @p at @s rotated ~ 0 run function '
                      'rlk:mboss/butterfly/fx/test/dome',
                      'execute positioned ^ ^ ^8 run ' + fx('rel_dome', r=6.0)])
    W.w('test/tele', ['# One telegraph of each shape around the executor (tell 40 t, Dendro / Pyro / physical):',
                      '# /execute as @p at @s rotated ~ 0 run function rlk:mboss/butterfly/fx/test/tele',
                      'execute positioned ^4 ^ ^5 run ' + tele_disc(2.5, 40, 7),
                      'execute positioned ^-4 ^ ^5 run ' + tele_disc(1.2, 40, 1),
                      'execute positioned ^ ^ ^11 run ' + tele_ring(1.5, 3.5, 40, 7),
                      'execute positioned ^5 ^ ^11 run ' + tele_sector(4.5, 90, 40, 1),
                      'execute positioned ^-5 ^ ^11 run ' + tele_sector(4.0, 45, 40, 0),
                      'execute positioned ^ ^ ^3 run ' + tele_line(6.0, 2.0, 40, 7)])
    W.w('test/sounds', ['# Click through the sound recipes (tellraw list).',
                        'tellraw @s [{"text":"달빛 환영 나비 sounds: ","color":"#B6E35A"}' +
                        ''.join(f',{{"text":"[{n}] ","color":"#D9F5A8","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}"}}}}' for n in SOUNDS) + ']'])
    W.w('test/hud', ['# Both badges on the boss-bar lines (the cure meter at 9 of 15 %) and the actionbar (run during a fight), then pops.',
                     f'scoreboard players set {CURE_P} mb 9', f'scoreboard players set {CURE_T} mb 15',
                     f'function {FN}hud/coc_on', f'function {FN}hud/buff_on', f'function {FN}hud/ab_coc',
                     f'function {FN}hud/pop_coc'])
    W.w('test/presets', ['# Click through the presets (tellraw list; macro presets use test values).',
                         'tellraw @s [{"text":"달빛 환영 나비 fx: ","color":"#B6E35A"}' +
                         ''.join(f',{{"text":"[{n}] ","color":"#D9F5A8","click_event":{{"action":"run_command",'
                                 f'"command":"/execute at @s rotated ~ 0 positioned ^ ^ ^4 run {_test_call(n)}"}}}}'
                                 for n in PRESETS) + ']'])


def _test_call(name):
    args = PRESETS[name][1]
    vals = {'life': 60, 'h': 4.0, 'r': 6.0}
    return fx(name, **{a: vals[a] for a in args})


def build_datapack(dp):
    W = Writer(dp)
    engine(W)
    telegraphs(W)
    sounds(W)
    hud_funcs(W)
    presets_dp(W)
    props(W)
    tests(W)
    removed = W.flush()
    return len(W.files), removed


def manifest():
    return {
        'generator': 'tools/build_mboss_bf_fx.py',
        'functions': FN, 'item_models': NS_TEX, 'font': FONT, 'storage': STO,
        'owned': {'dirs': [f'{FDIR}/{d}' for d in OWNED_DIRS], 'files': [f'{FDIR}/{f}.mcfunction' for f in OWNED_FILES],
                  'rp': ['assets/rlk/textures/mboss/bf_kit', 'assets/rlk/models/item/mboss/bf_kit',
                         'assets/rlk/items/mboss/bf_kit', 'assets/rlk/font/mboss_bf.json',
                         'assets/rlk/textures/font/mboss_bf']},
        'caps': {'fx': CAP, 'telegraph': TCAP},
        'objectives': ['bkS', 'bkG', 'bkH', 'bkK', 'bkD'],
        'kinds': {k: {'plane': v[0], 'px': list(v[1]), 'extent': list(v[2]), 'tint': 'neutral' if v[6] else 'painted',
                      'desc': v[7]} for k, v in KINDS.items()},
        'atlas_px': atlas_px(),
        'presets': {k: {'args': v[1], 'doc': v[0]} for k, v in PRESETS.items()},
        'props': {k: v[0] for k, v in PROPS.items()},
        'sounds': {k: v[0] for k, v in SOUNDS.items()},
        'glyphs': {k: f'U+{v[0]:04X}' for k, v in GLYPHS.items()},
        'telegraph_colours': {str(k): [f'#{c:06X}' for c in v] for k, v in TELE_COL.items()},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--resourcepack', help='unpacked resource pack root (assets/...)')
    ap.add_argument('--datapack', default=str(HERE.parent), help='datapack root (data/...)')
    ap.add_argument('--skip-rp', action='store_true', help='only write the datapack functions')
    a = ap.parse_args()
    n, removed = build_datapack(a.datapack)
    (HERE / 'mboss_bf_fx_manifest.json').write_text(json.dumps(manifest(), ensure_ascii=False, indent=1) + '\n',
                                                     encoding='utf-8')
    msg = f'butterfly fx kit: {n} functions ({removed} stale removed), {len(PRESETS)} presets, {len(SOUNDS)} sounds'
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error('--resourcepack is required unless --skip-rp')
        k, px, g = build_resourcepack(a.resourcepack)
        msg += f', {k} sprites ({px / 1e6:.2f} M px of atlas), {g} glyphs in {FONT}'
    print(msg)


if __name__ == '__main__':
    main()
