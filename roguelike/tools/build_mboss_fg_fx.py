#!/usr/bin/env python3
"""FX / audio / HUD kit of the third mid-boss, 실험성 역장 발생 장치 (nameplate 브레게 프로토타입), the field generator.

A renamed copy of the butterfly kit (tools/build_mboss_bf_fx.py) with the field generator's own art. Pattern authors
call it from their patterns; nothing here decides gameplay (hits, timings, hazards and the break meter's count stay
in the module core). Parts, all regenerated on every run:

  1. A tinted card engine: painted sprites on short-lived item_display cards, camera-facing or world-oriented,
     with spawn, delay, grow, move (from a static start offset), spin, a colour change at a chosen tick and a
     shrink-out fade. Item definitions carry a minecraft:custom_model_data tint (default white), so painted sprites
     keep their video colours and the neutral ones take any colour. Hard caps: CAP fx and TCAP telegraph cards.
     Card planes: face, flat, cross (two crossed quads along +y, for beams and columns), band (a flat strip with a
     standing flame wall on its front edge, for the expanding wave) and box (the thrown slab).
     The ager phase is fixed against the butterfly kit (its review perf-2): stages are counted from gametime + 1, so a
     card's main interpolation starts in the server tick after its spawn and the client animates it.
  2. Ground telegraph decals: disc, ring, sector, line, the expanding wave ring (synced to a hz/ring + hz/resize
     front), the moving line for the lasers (re-aimed per tick), the rim-only disc and the dark floor disc.
     Palettes: 5 Geo (amber), 9 field (violet), 0 physical, 6 the pale-gold rim; anything else draws Geo.
     Telegraph rule (10-20, user): the module draws a ground decal only where the reference footage shows a marker on
     the floor before the hit (C5 지면 충격: tele/rim + tele/dark; F1 감소 영역: tele/dark; the C1 / C2 slam point: the
     base flare p/column_base); every other attack is read from the boss's motion and sound. The other shapes stay in
     the kit's API (test/tele) but the field generator no longer calls them.
  3. A vanilla sound recipe library: fx/snd/<name>, mechanical / brass layers (anvil, chain, piston, vault, beacon,
     respawn anchor, amethyst, crafter, breeze...), with the per-layer minimum volume rule of mboss_lib.
  4. The HUD: font rlk:mboss_fg (U+E700-E7FF) with the 역장 badge, 20 meter pips (empty / full / just counted), the
     "N/20" digit style, the low-gravity icon, a big break badge and flat screen flashes; the meter, low-gravity and
     groggy flags for the boss-bar lines, the per-count feedback and the field banner.
  5. Presets per event of the plan (fx/p/<name>), prop looks (fx/prop/<name>), in-game test and demo functions.
  6. (Removed with the merge of the real rig, wip/fg-rig: the stub rig tools/mboss_fg_fx_stub_rig.py that wrote
     F:mboss/fieldgen/fx/rig_stub/**. The kit now needs the rig manifest; the text below is the stage-1 design.) A stub
     rig with the rig API, used by
     the kit's demos and meter crack calls only while the real rig manifest tools/mboss_fieldgen_rig_manifest.json
     does not exist. With the manifest present the kit calls rlk:mboss/fieldgen/rig/... and deletes the stub.

Outputs (owned; stale files in these places are removed):
  resource pack  assets/rlk/textures/mboss/fg_kit/<kind>.png      painted sprites (stdlib painter)
                 assets/rlk/models/item/mboss/fg_kit/<kind>.json    card / cross / band / box models (tintindex 0)
                 assets/rlk/items/mboss/fg_kit/<kind>.json          item definition, custom_model_data tint
                 assets/minecraft/atlases/items.json                adds rlk:mboss/fg_kit/* (merges)
                 assets/rlk/font/mboss_fg.json + textures/font/mboss_fg/*.png
  datapack       data/rlk/function/mboss/fieldgen/fx/{card,cardx,look,clear,uninstall}
                 data/rlk/function/mboss/fieldgen/fx/{e,p,tele,snd,hud,prop,test,rig_stub}/**
                 (other files under mboss/fieldgen/fx/ belong to the module core and are left alone)
  manifest       tools/mboss_fg_fx_manifest.json (kinds, presets, sounds, glyphs, owned paths, rig mode)

No hook in a shared file is needed: the engine ages its cards from a self-rescheduling function
(schedule ... 1t replace) that stops when no card is left. Cards carry rlk_room + rlk_mb_aux, so the mid-boss
cleanup, room clears and uninstall remove them too. The module's uninstall hook should call
rlk:mboss/fieldgen/fx/uninstall (objectives fkS fkG fkH fkK fkD, storage rlk:fgkit, the stub rig).

Run: python3 tools/build_mboss_fg_fx.py --resourcepack <unpacked RP> [--datapack <dp root>]   (or --skip-rp)
API reference: scratchpad mb3/fg_fx_api.md. Other generators import card(), tele_*(), snd(), fx(), look(), prop(),
hud() and the colour constants from this file.
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
import mboss_fg_fx_paint as P  # noqa: E402

FN = 'rlk:mboss/fieldgen/fx/'
FDIR = 'data/rlk/function/mboss/fieldgen/fx'
NS_TEX = 'rlk:mboss/fg_kit/'           # textures, models (rlk:item/mboss/fg_kit/*) and item ids
TEXDIR = 'mboss/fg_kit'
FONT = 'rlk:mboss_fg'
FONT_NAME = 'mboss_fg'
STO = 'rlk:fgkit'
CAP = 64            # live fx cards; further fx spawns are skipped until some expire
TCAP = 40           # live telegraph cards (counted apart, so busy fx never hide a telegraph)
TSKIP = 6           # telegraph calls are skipped from TCAP - TSKIP on (no shape is ever half drawn)
ATLAS_BUDGET = 1_000_000
OWNED_DIRS = ('e', 'p', 'tele', 'snd', 'hud', 'test', 'prop', 'rig_stub')
OWNED_FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')
OBJECTIVES = ('fkS', 'fkG', 'fkH', 'fkK', 'fkD')
TAG = 'rlk_fk'
BOX = (0.5, 0.135, 0.2)          # box kind half extents (x length, y thickness, z width) at scale 1
WALL_H = 0.5                     # band kind: wall height at scale 1

# The rig: the real rig's functions when its manifest exists, else the kit's removable stub.
RIG_MANIFEST = HERE / 'mboss_fieldgen_rig_manifest.json'
REAL_RIG = 'rlk:mboss/fieldgen/rig/'
STUB_RIG = FN + 'rig_stub/'


def rig_mode():
    return 'real' if RIG_MANIFEST.exists() else 'stub'


def RIG():
    return REAL_RIG if rig_mode() == 'real' else STUB_RIG


# ----------------------------------------------------------------------------- colours (RGB ints for tints)


def rgb(h):
    return int(h[1:], 16)


WHITE = 0xFFFFFF
BRASS = rgb('#E8C46A')         # registry colour
GOLD = rgb('#F5CF88')          # charge / glow gold
GOLD_PALE = rgb('#FDF3AA')
GOLD_WHITE = rgb('#FDFBD1')
GOLD_DEEP = rgb('#E2AE66')
AMBER = rgb('#E6A55F')
ORANGE = rgb('#D29253')
FLARE = rgb('#F0D19C')         # core lift flare
VIOLET = rgb('#8775EE')
VIOLET_DEEP = rgb('#6C64E3')
VIOLET_PALE = rgb('#CCB7E2')
CYAN = rgb('#C2E1F5')          # warp
CYAN_PALE = rgb('#DFF6FB')
DUST = rgb('#CAA376')
DUST_PALE = rgb('#E4BA87')
CRACK_GOLD = rgb('#F6DD8E')
RIM_PALE = rgb('#FDF4CD')      # 지면 충격 rim flare
SMOKE = rgb('#E2E8EC')

# telegraph tints per el: rim, fill, flash (saturated and darker than the fx palette: pale gold vanishes on the white
# marble; the baked dark outline carries them on the pink centre)
TELE_COL = {5: (rgb('#D27A0C'), rgb('#F0A93A'), rgb('#FFE8A0')),
            9: (rgb('#7046DC'), rgb('#A288F2'), rgb('#ECE2FF')),
            0: (rgb('#E5304A'), rgb('#FF6474'), rgb('#FFB8C4')),
            # 6: the pale-gold rim of 지면 충격 (C5; v4 2.70-4.95: a thin pale-gold rim at the final radius, the only
            # line on the floor; telegraph rule 10-20): drawn by tele/rim (no fill), flashing pale on the blast
            6: (rgb('#EFC566'), rgb('#F6DC96'), RIM_PALE)}
TELE_DEFAULT = 5

# ----------------------------------------------------------------------------- kinds
# name -> (plane, (w, h) px, card extent in blocks at scale 1 (a0, a1, b0, b1), painter box (a0, a1, b0, b1),
#          painter, supersampling, tinted-neutral?, description)
# planes: face = local XY plane (facing forward, or the camera with a billboard); flat = local XZ plane (horizontal for
# rot "~ 0", +b forward); cross = two crossed vertical quads along +y (XY and ZY planes; a across, b along y);
# band = a flat strip b in -1..0 (front edge at b = 0, the texture's top half) plus a vertical wall on the front edge,
# y 0..WALL_H (the bottom half); box = a cuboid (BOX half extents) with the full texture on every face.
SQ = (-0.5, 0.5, -0.5, 0.5)
UNIT = (-1, 1, -1, 1)
BX = (-1, 1, -1, 1)
FOOT = (-0.5, 0.5, 0.0, 1.0)
HANG = (-0.5, 0.5, -1.0, 0.0)
KINDS = {
    'bomb':          ('face', (64, 64), SQ, BX, P.paint_bomb, 2, False, 'gold bomb: dark core, glowing equator ring and ports, warm halo'),
    'bomb_burst':    ('face', (128, 128), SQ, BX, P.paint_bomb_burst, 2, False, 'gold spiky bomb burst with dark flecks'),
    'missile':       ('cross', (32, 112), (-0.14, 0.14, -0.5, 0.5), (-0.14, 0.14, -0.5, 0.5), P.paint_missile, 2, False, 'gold drill missile, nose at +b, hot nose glow, exhaust'),
    'smoke':         ('face', (64, 64), SQ, BX, P.paint_smoke, 2, False, 'blue-white missile smoke puff'),
    'column':        ('cross', (64, 256), FOOT, FOOT, P.paint_column, 2, False, 'gold light column / beam, foot at b 0, 1 block tall at scale 1'),
    'laser_core':    ('cross', (32, 128), HANG, HANG, P.paint_laser_core, 2, False, 'laser beam core, from the muzzle (b 0) along -b'),
    'laser_glow':    ('cross', (64, 128), HANG, HANG, P.paint_laser_glow, 2, False, 'laser beam glow sleeve, along -b'),
    'muzzle':        ('face', (64, 64), SQ, BX, P.paint_muzzle, 2, False, 'laser muzzle ring with a hot centre'),
    'scorch':        ('flat', (64, 64), SQ, BX, P.paint_scorch, 2, False, 'floor scorch with a glowing gold centre'),
    'slam_ring':     ('flat', (256, 256), UNIT, BX, P.paint_slam_ring, 2, False, 'slam shock ring (unit radius): gold band, dust fringe, flecks'),
    'dust':          ('face', (64, 64), SQ, BX, P.paint_dust, 2, False, 'tan dust puff'),
    'gold_shard':    ('face', (64, 128), (-0.25, 0.25, -0.5, 0.5), (-0.25, 0.25, -0.5, 0.5), P.paint_gold_shard, 2, False, 'gold crystal shard'),
    'glass_shard':   ('face', (64, 128), (-0.25, 0.25, -0.5, 0.5), (-0.25, 0.25, -0.5, 0.5), P.paint_glass_shard, 2, False, 'white-gold bubble glass shard (the break)'),
    'wave_band':     ('band', (256, 128), (-0.5, 0.5, -1.0, 0.0), (-0.5, 0.5, -1.0, 1.0), P.paint_wave_band, 2, False, 'gravity-wave band segment: gold-fire strip + flame wall'),
    'charge_sphere': ('face', (128, 128), SQ, BX, P.paint_charge_sphere, 2, False, 'gravity-wave charge sphere with orbit swirls'),
    'flare_dome':    ('face', (128, 64), (-0.5, 0.5, 0.0, 0.5), (-0.5, 0.5, 0.0, 0.5), P.paint_flare_dome, 2, False, 'burst flare dome (half dome, pivot at the base centre)'),
    'fire_disc':     ('flat', (128, 128), SQ, BX, P.paint_fire_disc, 2, False, 'filled fire disc (wave start, flame band)'),
    'erupt_disc':    ('flat', (128, 128), SQ, BX, P.paint_erupt_disc, 2, False, 'dark eruption disc with an amber rim and gold cracks'),
    'erupt_burst':   ('face', (128, 128), FOOT, FOOT, P.paint_erupt_burst, 2, False, 'gold eruption burst with floor chunks, pivot at the floor'),
    'chunk':         ('face', (32, 32), SQ, BX, P.paint_chunk, 3, False, 'floor chunk / rock with an orange crack'),
    'pebble':        ('face', (32, 32), SQ, BX, P.paint_pebble, 3, False, 'floating pebble (low-gravity cue)'),
    'spike_fan':     ('face', (128, 128), FOOT, FOOT, P.paint_spike_fan, 2, False, 'floor-burst crystal-spike fan, pivot at the floor'),
    'slab':          ('box', (64, 64), (-0.5, 0.5, -BOX[1], BOX[1]), BX, P.paint_slab, 2, False, 'glowing floor slab (box 1 x 0.27 x 0.4 at scale 1)'),
    'ousia_col':     ('cross', (64, 256), HANG, HANG, P.paint_ousia_col, 2, False, 'violet Ousia column hanging from b 0 along -b'),
    'glitch':        ('face', (64, 128), (-0.25, 0.25, -0.5, 0.5), (-0.25, 0.25, -0.5, 0.5), P.paint_glitch, 2, False, 'violet glitch streak'),
    'warp_pillar':   ('face', (64, 192), (-0.25, 0.25, 0.0, 1.5), (-0.25, 0.25, 0.0, 1.5), P.paint_warp_pillar, 2, False, 'white-cyan warp pillar, pivot at the floor, 1.5 tall at scale 1'),
    'warp_bloom':    ('face', (128, 128), SQ, BX, P.paint_warp_bloom, 2, False, 'white-cyan warp bloom'),
    'bubble0':       ('face', (128, 128), SQ, BX, P.make_bubble(0), 2, False, 'core bubble, crack stage 0'),
    'bubble1':       ('face', (128, 128), SQ, BX, P.make_bubble(1), 2, False, 'core bubble, crack stage 1'),
    'bubble2':       ('face', (128, 128), SQ, BX, P.make_bubble(2), 2, False, 'core bubble, crack stage 2'),
    'bubble3':       ('face', (128, 128), SQ, BX, P.make_bubble(3), 2, False, 'core bubble, crack stage 3'),
    'crack_ring':    ('flat', (256, 256), UNIT, BX, P.paint_crack_ring, 2, False, 'gold crack ring (unit radius)'),
    'crack_glint':   ('face', (64, 64), SQ, BX, P.paint_crack_glint, 2, False, 'per-hit crack glint'),
    'spark':         ('face', (64, 64), SQ, BX, P.paint_spark, 2, False, 'gold spark star'),
    'arc':           ('face', (128, 64), (-0.5, 0.5, -0.25, 0.25), (-0.5, 0.5, -0.25, 0.25), P.paint_arc, 2, False, 'electric gold arc'),
    'flame':         ('face', (64, 128), (-0.25, 0.25, 0.0, 1.0), (-0.25, 0.25, 0.0, 1.0), P.paint_flame, 2, False, 'gold flame tongue, pivot at its root'),
    'glow':          ('face', (64, 64), SQ, BX, P.paint_glow, 2, True, 'soft white glow disc (tint it)'),
    'glint':         ('face', (64, 64), SQ, BX, P.paint_glint, 3, True, 'white 4-point glint (tint it)'),
    'mote':          ('face', (32, 32), SQ, BX, P.paint_mote, 3, True, 'soft mote (tint it)'),
    'streak':        ('face', (256, 32), (-0.5, 0.5, -0.0625, 0.0625), BX, P.paint_streak, 2, True, 'long thin streak along a (tint it)'),
    'ripple':        ('face', (256, 256), SQ, BX, P.paint_ripple, 2, True, 'ripple / shock ring (near white, tint it)'),
    # telegraph decals (unit radius / unit length: the scale is the size in blocks)
    't_rim':         ('flat', (256, 256), UNIT, BX, P.paint_t_rim, 2, True, 'telegraph rim, unit radius'),
    't_rim_s':       ('flat', (128, 128), UNIT, BX, P.paint_t_rim_s, 2, True, 'thick telegraph rim (r <= 2.5)'),
    't_ring':        ('flat', (256, 256), UNIT, BX, P.paint_t_ring, 2, True, 'thin travelling wave ring'),
    't_fill':        ('flat', (128, 128), UNIT, BX, P.paint_t_fill, 2, True, 'telegraph progress fill, unit radius'),
    't_bar':         ('flat', (16, 64), (-0.5, 0.5, 0.0, 1.0), (-1, 1, 0, 1), P.paint_t_bar, 2, True, 'lane rail / cap bar'),
    't_lane':        ('flat', (64, 64), (-0.5, 0.5, 0.0, 1.0), (-1, 1, 0, 1), P.paint_t_lane, 2, True, 'lane progress fill, unit length'),
}
SECTORS = (30, 45, 60, 90)
for _h in SECTORS:
    KINDS[f't_sec{_h}'] = ('flat', (256, 144), (-1, 1, -0.125, 1), (-1, 1, -0.125, 1), P.make_t_sec(_h), 2, True,
                           f'sector telegraph rim, half-angle {_h}')
    KINDS[f't_secf{_h}'] = ('flat', (128, 80), (-1, 1, -0.25, 1), (-1, 1, -0.25, 1), P.make_t_secf(_h), 2, True,
                            f'sector progress fill, half-angle {_h}')
TELE_KINDS = [k for k in KINDS if k.startswith('t_')]
FX_KINDS = [k for k in KINDS if not k.startswith('t_')]
SPIN_Y = ('flat', 'cross', 'band', 'box')       # planes that spin about local y (their normal / long axis)

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


def r4(v):
    return round(v, 4)


def model_json(kind):
    """Zero-thickness double-sided quads (or a cuboid) with tintindex 0. Display-local p (blocks) is written at model
    m = (8 - 16 px, 8 + 16 py, 8 - 16 pz): the item renderer's 180-degree turn about Y maps it back to p, so the
    display's local axes are the summoning frame's (+x left, +y up, +z forward). Card +a = local -x = model +x."""
    plane, _s, (a0, a1, b0, b1), _box, _fn, _ss, _n, _d = KINDS[kind]
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1
    tex = NS_TEX + kind

    def q(frm, to, faces):
        return {'from': [r4(v) for v in frm], 'to': [r4(v) for v in to], 'shade': False, 'faces': faces}

    def f(uv):
        return {'uv': uv, 'texture': '#0', 'tintindex': 0}
    if plane == 'face':
        els = [q([x0, 8 + 16 * b0, 8], [x1, 8 + 16 * b1, 8], {'south': f([0, 0, 16, 16]), 'north': f([16, 0, 0, 16])})]
    elif plane == 'flat':
        els = [q([x0, 8, 8 - 16 * b1], [x1, 8, 8 - 16 * b0], {'up': f([0, 0, 16, 16]), 'down': f([0, 16, 16, 0])})]
    elif plane == 'cross':
        els = [q([x0, 8 + 16 * b0, 8], [x1, 8 + 16 * b1, 8], {'south': f([0, 0, 16, 16]), 'north': f([16, 0, 0, 16])}),
               q([8, 8 + 16 * b0, 8 - 16 * a1], [8, 8 + 16 * b1, 8 - 16 * a0],
                 {'east': f([0, 0, 16, 16]), 'west': f([16, 0, 0, 16])})]
    elif plane == 'band':
        els = [q([x0, 8, 8 - 16 * b1], [x1, 8, 8 - 16 * b0], {'up': f([0, 0, 16, 8]), 'down': f([0, 8, 16, 0])}),
               q([x0, 8, 8 - 16 * b1], [x1, 8 + 16 * WALL_H, 8 - 16 * b1],
                 {'north': f([16, 8, 0, 16]), 'south': f([0, 8, 16, 16])})]
    elif plane == 'box':
        hx, hy, hz = BOX
        full = f([0, 0, 16, 16])
        els = [q([8 - 16 * hx, 8 - 16 * hy, 8 - 16 * hz], [8 + 16 * hx, 8 + 16 * hy, 8 + 16 * hz],
                 {k: dict(full) for k in ('north', 'south', 'east', 'west', 'up', 'down')})]
    else:
        raise ValueError(plane)
    for e in els:
        for v in e['from'] + e['to']:
            assert -16 <= v <= 32, (kind, e)
    return {'ambientocclusion': False, 'textures': {'0': tex, 'particle': tex}, 'elements': els}


def item_json(kind):
    return {'model': {'type': 'minecraft:model', 'model': f'rlk:item/{TEXDIR}/{kind}',
                      'tints': [{'type': 'minecraft:custom_model_data', 'index': 0, 'default': WHITE}]}}


def atlas_px():
    return sum(v[1][0] * v[1][1] for v in KINDS.values())


# ----------------------------------------------------------------------------- HUD font
CP_LO, CP_HI = 0xE700, 0xE7FF
# name -> (codepoint, painter: analytic fn (x right, y up, -1..1) | ('pix', fn, arg) | flat (hex, alpha),
#          texture px (w, h), height, ascent)
GLYPHS = {
    'badge':     (0xE700, P.glyph_badge, (36, 36), 9, 8),
    'pip0':      (0xE701, ('pix', P.pixel_pip, 0), (8, 14), 7, 7),
    'pip1':      (0xE702, ('pix', P.pixel_pip, 1), (8, 14), 7, 7),
    'pip2':      (0xE703, ('pix', P.pixel_pip, 2), (8, 14), 7, 7),
    'break_big': (0xE704, P.glyph_break, (96, 96), 24, 18),
    'lowg':      (0xE705, P.glyph_lowg, (36, 36), 9, 8),
    'lowg_big':  (0xE706, P.glyph_lowg, (96, 96), 24, 18),
    'fl_white':  (0xE710, ('#FFFFFF', 0.92), (16, 9), 144, 69),
    'fl_gold':   (0xE711, ('#F9DFAD', 0.55), (16, 9), 144, 69),
    'fl_violet': (0xE712, ('#6C64E3', 0.45), (16, 9), 144, 69),
    'fl_amber':  (0xE713, ('#E6A55F', 0.45), (16, 9), 144, 69),
}
DIGIT_CHARS = '0123456789/'
for _k, _ch in enumerate(DIGIT_CHARS):
    GLYPHS['d_slash' if _ch == '/' else f'd{_ch}'] = (0xE720 + _k, ('pix', P.pixel_digit, _ch), (7, 9), 9, 8)
SPACES = {0xE7F0: -1, 0xE7F1: 2, 0xE7F2: 1}
SP_NEG1, SP_GAP, SP_ONE = chr(0xE7F0), chr(0xE7F1), chr(0xE7F2)


def glyph(name):
    return chr(GLYPHS[name][0])


def digits(text):
    """the 'N/20' glyph string of a text made of digits and '/'"""
    return ''.join(glyph('d_slash' if c == '/' else f'd{c}') for c in text)


def pips(n, flash=False):
    """20 meter pips in 4 groups of 5: n full (the n-th white when flash), the rest empty"""
    out = []
    for k in range(20):
        if k and k % 5 == 0:
            out.append(SP_GAP)
        if flash and k == n - 1:
            out.append(glyph('pip2'))
        else:
            out.append(glyph('pip1' if k < n else 'pip0'))
    return ''.join(out)


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


def glyph_raw(name):
    cp, painter, (w, h), _height, _ascent = GLYPHS[name]
    if callable(painter):
        return w, h, bytes(paint_glyph(painter, w, h))
    if painter[0] == 'pix':
        pw, ph, rows = painter[1](painter[2])
        assert (pw, ph) == (w, h), name
        raw = bytearray()
        for row in rows:
            for r, g, b, a in row:
                raw += bytes((round(r * 255), round(g * 255), round(b * 255), round(a * 255))) if a > 0 else b'\0\0\0\0'
        return w, h, bytes(raw)
    hx, al = painter
    c = P.hexc(hx)
    return w, h, bytes((round(c[0] * 255), round(c[1] * 255), round(c[2] * 255), round(al * 255))) * (w * h)


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
    tex = rp / f'assets/rlk/textures/font/{FONT_NAME}'
    font_path = rp / f'assets/rlk/font/{FONT_NAME}.json'
    ours = [g[0] for g in GLYPHS.values()] + list(SPACES)
    assert all(CP_LO <= c <= CP_HI for c in ours) and len(set(ours)) == len(ours)
    clash = font_used_elsewhere(rp, font_path)
    hit = [c for c in ours if c in clash]
    if hit:
        raise SystemExit(f'{FONT} glyphs collide with ' + ', '.join(f'U+{c:04X} ({clash[c]})' for c in hit))
    tex.mkdir(parents=True, exist_ok=True)
    for old in tex.glob('*.png'):
        if old.stem not in GLYPHS:
            old.unlink()
    providers = []
    for name, (cp, _painter, (w, h), height, ascent) in GLYPHS.items():
        gw, gh, raw = glyph_raw(name)
        rows = b''.join(b'\x00' + raw[y * gw * 4:(y + 1) * gw * 4] for y in range(gh))
        (tex / f'{name}.png').write_bytes(png_bytes(gw, gh, rows))
        providers.append({'type': 'bitmap', 'file': f'rlk:font/{FONT_NAME}/{name}.png', 'ascent': ascent,
                          'height': height, 'chars': [chr(cp)]})
    providers.append({'type': 'space', 'advances': {chr(k): v for k, v in SPACES.items()}})
    font_path.parent.mkdir(parents=True, exist_ok=True)
    font_path.write_text(json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return len(GLYPHS)


def build_resourcepack(rp):
    rp = Path(rp)
    px = atlas_px()
    assert px <= ATLAS_BUDGET, f'atlas budget: {px} px > {ATLAS_BUDGET}'
    for k, v in KINDS.items():
        w, h = v[1]
        assert w <= 256 and h <= 256 and w % 16 == 0 and h % 16 == 0, (k, w, h)
    n_glyphs = build_font(rp)
    root = rp / 'assets/rlk'
    dirs = {f'textures/{TEXDIR}': '.png', f'models/item/{TEXDIR}': '.json', f'items/{TEXDIR}': '.json'}
    for sub in dirs:
        d = root / sub
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob('*'):
            if old.stem not in KINDS:
                old.unlink()
    for kind in KINDS:
        w, h, raw = render(kind)
        (root / f'textures/{TEXDIR}' / f'{kind}.png').write_bytes(png_bytes(w, h, raw))
        (root / f'models/item/{TEXDIR}' / f'{kind}.json').write_text(
            json.dumps(model_json(kind), separators=(',', ':')) + '\n', encoding='utf-8')
        (root / f'items/{TEXDIR}' / f'{kind}.json').write_text(
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
    return len(KINDS), px, n_glyphs


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
         col=WHITE, dly=0, dur=0, hit=-1, col2=-1, off=None):
    """The function line that spawns one card (fx/card, or fx/cardx when an extended option is used).
    pos: summon point ('^x ^y ^z', '~x ~y ~z' or absolute); rot: rotation of the card, '~ ~' = the executor's,
    '~30 -90' = turned 30 degrees to the executor's right and pitched straight up (relative yaw, absolute pitch);
    bb: fixed | center | vertical | horizontal; roll: degrees about the card's local z (left_rotation, constant);
    spin: degrees turned about the card normal (y for flat / cross / band / box kinds) over the main interpolation
    (-170..170); s0 / s1: start / end size (float = uniform, or an (x, y, z) tuple); off: static start translation in
    the display frame (+x left, +y up, +z forward, blocks); move: translation added over the main interpolation (the
    end translation is off + move; with placeholders give the absolute end as move and off separately);
    life / fade: ticks; col: tint (RGB int, WHITE keeps the painted colours); dly: ticks hidden before it appears;
    dur: ticks of the main interpolation (0 = until the fade); hit / col2: `hit` ticks after the call the tint
    becomes col2. Any value may be a macro placeholder string such as '$(r)'."""
    assert kind in KINDS, kind
    assert bb in ('fixed', 'center', 'vertical', 'horizontal'), bb
    uni = (int, float, str)
    simple = isinstance(s0, uni) and isinstance(s1, uni) and not dly and not dur and hit == -1 and off is None
    if off is not None and all(isinstance(x, (int, float)) for x in tuple(off) + tuple(move)):
        end = tuple(a + b for a, b in zip(off, move))
    else:
        end = tuple(move)
    mv = vec(end)
    if simple:
        return (f'function {FN}card {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
                f'spin:{_i(spin)},s0:{_f(s0)},s1:{_f(s1)},move:"{mv}",life:{_i(life)},'
                f'fade:{_i(fade)},col:{_i(col)}}}')
    return (f'function {FN}cardx {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
            f'spin:{_i(spin)},s0:"{vec(s0)}",s1:"{vec(s1)}",off:"{vec(off if off is not None else (0, 0, 0))}",'
            f'move:"{mv}",life:{_i(life)},fade:{_i(fade)},col:{_i(col)},dly:{_i(dly)},dur:{_i(dur)},hit:{_i(hit)},'
            f'col2:{_i(col2)}}}')


cardx = card


def _tenths(v):
    return int(round(v * 10))


def tele_disc(r, tell, el=5, hold=3):
    """Disc telegraph decal of radius r blocks; the progress fill reaches the rim `tell` ticks after the call
    (the framework hz/* strike tick when created in the same tick with the same tell)."""
    return f'function {FN}tele/disc {{r:{_tenths(r)},tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}'


def tele_rim(r, tell, el=6, hold=3):
    """Rim-only disc telegraph decal (tele/disc without its fill / progress edge): the static rim of radius r, flashing
    on the strike tick (call + tell). Default palette 6 = the pale-gold rim of 지면 충격 (C5, telegraph rule 10-20)."""
    return f'function {FN}tele/rim {{r:{_tenths(r)},tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}'


def tele_dark(r0, r, tell, grow, hold=0):
    """The dark floor disc decal (erupt_disc: the floor about 35 % darker, an amber rim, gold cracks; the footage's own
    ground marker of 감소 영역 F1 and 지면 충격 C5, telegraph rule 10-20): its radius grows r0 -> r blocks over `grow` ticks
    from the tick after the call and it stays to the strike (call + tell) + hold. Painted colours, no flash; a
    telegraph card (TCAP, cleared by tele/clear, so a pause redraw draws it again with the ticks left)."""
    return (f'function {FN}tele/dark {{r0:{_tenths(r0)},r:{_tenths(r)},grow:{int(grow)},tell:{int(tell)},'
            f'hold:{int(hold)}}}')


def tele_ring(r0, r, tell, el=5, hold=3):
    return f'function {FN}tele/ring {{r0:{_tenths(r0)},r:{_tenths(r)},tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}'


def tele_sector(r, half_angle, tell, el=5, hold=3):
    return (f'function {FN}tele/sector {{r:{_tenths(r)},a:{int(round(half_angle))},tell:{int(tell)},el:{int(el)},'
            f'hold:{int(hold)}}}')


def tele_line(length, width, tell, el=5, hold=3, back=0.0):
    return (f'function {FN}tele/line {{len:{_tenths(length)},w:{_tenths(width)},back:{_tenths(back)},'
            f'tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}')


def tele_wave(r0, r1, w, tell, dur, el=9, hold=2):
    """Expanding wave ring: the start disc (r0) fills over the tell, then from the strike the front ring travels
    r0 -> r1 in dur ticks with the band's inner edge w behind it (pair with hz/ring + hz/resize at
    (r1 - r0) / dur blocks per tick)."""
    return (f'function {FN}tele/wave {{r0:{_tenths(r0)},r1:{_tenths(r1)},w:{_tenths(w)},tell:{int(tell)},'
            f'dur:{int(dur)},el:{int(el)},hold:{int(hold)}}}')


def tele_mline(mid, length, width, tell, el=5, hold=0, back=0.0):
    """Moving line (laser lanes) id 0-7: as tele/line from the pivot (the executing point), re-aimed later with
    tele_mline_aim / tele_mline_turn; covers -back..length along the aim (negative back starts beyond the pivot)."""
    return (f'function {FN}tele/mline {{id:{int(mid)},len:{_tenths(length)},w:{_tenths(width)},back:{_tenths(back)},'
            f'tell:{int(tell)},el:{int(el)},hold:{int(hold)}}}')


def tele_mline_aim(mid):
    return f'function {FN}tele/mline_aim {{id:{int(mid)}}}'


def tele_mline_turn(mid, d):
    return f'function {FN}tele/mline_turn {{id:{int(mid)},d:{num(float(d), 2)}}}'


def tele_mline_end(mid):
    return f'function {FN}tele/mline_end {{id:{int(mid)}}}'


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
    """As @s = an item_display prop: dress it as a kit projectile / prop look (fx/prop/<name>)."""
    assert name in PROPS, name
    return f'function {FN}prop/{name}'


def hud(name, **args):
    assert name in HUD_FUNCS, name
    if args:
        return f'function {FN}hud/{name} {{' + ','.join(f'{k}:{v}' for k, v in args.items()) + '}'
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


def flash(c, pos='~ ~ ~', alpha=1.0):
    cl = colour_list(c)[:-1] + f',{num(float(alpha), 2)}f]'
    return part(f'flash{{color:{cl}}}', pos, (0, 0, 0), 0, 1)


def blockp(block, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    return part(f'block{{block_state:"minecraft:{block}"}}', pos, delta, speed, n)


# ----------------------------------------------------------------------------- sound recipes
# name -> (comment, [(event, volume, pitch), ...]); one tick each, vanilla events only, mechanical / brass, no
# creature voices (no roars, cries or mob ambient sounds).
SOUNDS = {
    # entrance
    'awake_clank': ('Activation clank (entrance E0): a sharp metallic clank with a bright tail.',
                    [('block.vault.activate', 0.9, 0.8), ('block.iron_trapdoor.close', 0.8, 0.7),
                     ('entity.zombie.attack_iron_door', 0.35, 1.4), ('block.anvil.place', 0.3, 1.6),
                     ('block.beacon.activate', 0.3, 1.3)]),
    'unfold': ('Pods unfold and the crown assembles (entrance +8..+30): low thumps and gear clicks.',
               [('block.piston.extend', 0.8, 0.8), ('block.crafter.craft', 0.7, 0.9), ('block.chain.place', 0.7, 0.9),
                ('block.copper_trapdoor.open', 0.6, 0.8)]),
    'gear_click': ('Crown gear clicks (call 2-3 times while the crown assembles; quiet).',
                   [('block.crafter.craft', 0.6, 1.25), ('block.copper_bulb.turn_on', 0.4, 1.5),
                    ('block.chain.hit', 0.35, 1.4)]),
    'eye_open': ('The eye opens and the core drum turns (entrance +32..+64): a low mechanical groan and a click.',
                 [('block.vault.open_shutter', 0.9, 0.9), ('block.grindstone.use', 0.3, 0.6),
                  ('block.beacon.power_select', 0.4, 1.6), ('block.amethyst_block.resonate', 0.4, 1.2)]),
    'rise_hum': ('The device rises to cruise height (entrance +64..+94; also field lift-offs): whirring hum.',
                 [('block.beacon.ambient', 0.9, 1.4), ('block.conduit.ambient', 0.6, 1.2),
                  ('entity.minecart.riding', 0.3, 1.6), ('entity.breeze.whirl', 0.4, 0.7)]),
    # C1 / C2
    'bomb_port': ('Underside bomb ports light up (C1 +10): shutters and a rising charge.',
                  [('block.vault.open_shutter', 0.6, 1.3), ('block.respawn_anchor.charge', 0.4, 1.8),
                   ('block.dispenser.dispense', 0.4, 0.7)]),
    'bomb_drop': ('A bomb leaves a port (C1, every 2-4 t; quiet).',
                  [('block.dispenser.launch', 0.55, 0.8), ('entity.tnt.primed', 0.15, 1.6)]),
    'bomb_fall': ('Falling whistle of a bomb (C1, once per volley group).',
                  [('item.trident.riptide_1', 0.25, 2.0), ('entity.firework_rocket.launch', 0.3, 1.6)]),
    'bomb_burst': ('A bomb bursts on the floor (C1, per landing): short crack and crystal.',
                   [('entity.generic.explode', 0.35, 1.5), ('block.amethyst_cluster.break', 0.6, 0.8),
                    ('block.basalt.break', 0.5, 1.1), ('entity.firework_rocket.blast', 0.3, 0.9)]),
    'column_tell': ('Gold slam column projects to the floor (C1 / C2, 13 t tell): rising hum.',
                    [('block.respawn_anchor.charge', 0.8, 1.0), ('block.beacon.power_select', 0.7, 0.8),
                     ('block.beacon.activate', 0.4, 1.5)]),
    'plunge': ('The device plunges core first (C1 / C2, 3-4 t): whoosh and a hydraulic drop.',
               [('entity.breeze.wind_burst', 0.7, 0.6), ('item.trident.riptide_3', 0.4, 0.8),
                ('block.piston.contract', 0.6, 0.6)]),
    'slam': ('Slam impact r 5 (C1 / C2): heavy boom, anvil and debris.',
             [('entity.generic.explode', 1.0, 0.7), ('item.mace.smash_ground_heavy', 0.8, 0.8),
              ('block.anvil.land', 0.6, 0.5), ('block.heavy_core.place', 0.7, 0.7),
              ('block.amethyst_cluster.break', 0.6, 0.7)]),
    # C3
    'pods_drop': ('The medallions dock and drop beside the core (C3 +0..+4): clank.',
                  [('block.chain.place', 0.8, 0.9), ('block.piston.contract', 0.7, 0.8),
                   ('block.vault.close_shutter', 0.5, 1.2)]),
    'laser_charge': ('Laser spark charge (C3, 18 t): bright rising whine.',
                     [('block.beacon.activate', 0.8, 1.8), ('block.amethyst_block.resonate', 0.7, 1.5),
                      ('block.respawn_anchor.charge', 0.5, 1.7), ('entity.guardian.attack', 0.3, 1.8)]),
    'laser_fire': ('The two beams fire (C3 +24): hissing burst.',
                   [('block.beacon.power_select', 0.8, 1.4), ('entity.warden.sonic_boom', 0.3, 1.9),
                    ('entity.blaze.shoot', 0.5, 1.4), ('item.trident.thunder', 0.2, 2.0)]),
    'laser_loop': ('Beam loop (C3, every 10 t while firing, at the floor spots): hum and crackle.',
                   [('block.beacon.ambient', 0.7, 2.0), ('block.fire.ambient', 0.5, 1.6),
                    ('block.campfire.crackle', 0.4, 1.4)]),
    'laser_stop': ('Beams off and pods retract (C3 end): power-down.',
                   [('block.beacon.deactivate', 0.8, 1.2), ('block.piston.contract', 0.6, 0.9),
                    ('block.fire.extinguish', 0.3, 1.6)]),
    # C4
    'tip_flare': ('Spike-tip flare (C4 tell 1; also the next-pattern tell): crackle.',
                  [('entity.breeze.charge', 0.7, 1.4), ('block.respawn_anchor.charge', 0.6, 1.6),
                   ('block.amethyst_block.chime', 0.5, 1.6)]),
    'missile_vent': ('Top vents open with the vertical gold shaft (C4 tell 2): roaring hiss.',
                     [('block.blastfurnace.fire_crackle', 0.9, 0.9), ('entity.blaze.shoot', 0.7, 0.7),
                      ('block.vault.open_shutter', 0.6, 0.8), ('block.fire.ambient', 0.8, 0.9)]),
    'missile_launch': ('A drill missile launches (C4, per missile).',
                       [('entity.firework_rocket.launch', 0.7, 0.9), ('entity.breeze.shoot', 0.4, 0.8)]),
    'missile_dive': ('Missiles turn over and dive (C4, once per volley group): falling whistle.',
                     [('item.trident.riptide_1', 0.45, 1.8), ('entity.phantom.swoop', 0.35, 1.6)]),
    'missile_impact': ('A missile hits the floor (C4, per impact): crack and boom.',
                       [('entity.generic.explode', 0.4, 1.4), ('block.amethyst_cluster.break', 0.6, 0.9),
                        ('block.deepslate.break', 0.5, 1.0)]),
    # C5
    'core_flip': ('The core flips (C5 lift, the field core flip, groggy recover): clank and whoosh.',
                  [('block.vault.open_shutter', 0.8, 0.9), ('entity.breeze.wind_burst', 0.5, 0.8),
                   ('block.crafter.craft', 0.5, 0.8)]),
    'core_spark': ('Gold spark on the core (C5 tell 1): dense crackle.',
                   [('block.respawn_anchor.charge', 0.7, 1.3), ('block.amethyst_block.chime', 0.6, 1.6),
                    ('block.amethyst_block.chime', 0.5, 1.9), ('entity.blaze.burn', 0.2, 1.6)]),
    'core_lift': ('The core lifts with a gold flare (C5 +5, "번쩍"): bright flare.',
                  [('block.beacon.activate', 0.8, 1.4), ('block.respawn_anchor.set_spawn', 0.5, 0.6),
                   ('entity.firework_rocket.twinkle', 0.3, 1.2)]),
    'up_beam': ('Upward gold beam from the raised core (C5 +29..+40): rising crackle.',
                [('block.beacon.ambient', 0.8, 1.6), ('entity.warden.sonic_charge', 0.4, 1.4),
                 ('block.conduit.activate', 0.6, 1.2)]),
    'column_down': ('The column switches down to the floor centre (C5 +41): zap.',
                    [('item.trident.thunder', 0.3, 1.8), ('entity.breeze.wind_burst', 0.6, 0.6),
                     ('block.amethyst_cluster.break', 0.6, 0.7)]),
    'blast': ('Full-area gravity blast (C5 +48): big broadband boom, rocks launched.',
              [('entity.generic.explode', 1.2, 0.6), ('entity.warden.sonic_boom', 0.6, 0.8),
               ('entity.dragon_fireball.explode', 0.6, 0.9), ('block.basalt.break', 0.8, 0.8),
               ('block.pointed_dripstone.land', 0.6, 0.9)]),
    'rocks_hover': ('Rocks hover after the blast (C5 +54..+77, every 6-10 t; quiet): low rumble.',
                    [('block.amethyst_block.resonate', 0.4, 0.6), ('block.gravel.fall', 0.4, 0.7),
                     ('entity.ravager.step', 0.25, 0.5)]),
    # C6 / F2
    'dip': ('Dip and roll toward the player (C6 +0): whoosh.',
            [('entity.breeze.whirl', 0.8, 0.8), ('block.chain.step', 0.5, 0.8)]),
    'vent_flare': ('Vent flare, the medallions flung up (C6 +12): roaring hiss.',
                   [('block.blastfurnace.fire_crackle', 0.8, 1.0), ('entity.blaze.shoot', 0.6, 0.6),
                    ('block.beacon.power_select', 0.5, 1.4)]),
    'tower_up': ('The tower telescopes up (C6 +20, 18 t): ratchet clicks.',
                 [('block.crafter.craft', 0.8, 1.0), ('block.vault.open_shutter', 0.6, 1.1),
                  ('block.iron_trapdoor.open', 0.6, 0.9), ('block.piston.extend', 0.6, 1.2)]),
    'flame_charge': ('The flame band flares under the ring (C6 charge, 17 t): rising roar.',
                     [('item.firecharge.use', 0.8, 0.7), ('block.respawn_anchor.charge', 0.6, 1.3),
                      ('block.fire.ambient', 0.9, 0.9), ('block.campfire.crackle', 0.5, 0.9)]),
    'floor_burst': ('A floor burst erupts (C6 / F2, per burst): crystal crack and thump.',
                    [('block.amethyst_cluster.break', 0.9, 0.8), ('entity.generic.explode', 0.3, 1.4),
                     ('block.stone.break', 0.8, 0.6), ('block.tuff.break', 0.6, 0.8)]),
    'slab_lift': ('A slab tears out and rises (C6 / F2, after each burst; quiet): grinding rise.',
                  [('block.piston.extend', 0.35, 0.6), ('block.grindstone.use', 0.3, 0.5),
                   ('block.deepslate.break', 0.4, 0.7)]),
    'slab_throw': ('A slab is flung at the player (C6 / F2, per throw): heavy whoosh.',
                   [('entity.breeze.shoot', 0.7, 0.7), ('item.trident.throw', 0.7, 0.6),
                    ('entity.wind_charge.throw', 0.4, 0.6)]),
    'slab_impact': ('A slab lands (C6 / F2): crash.',
                    [('entity.generic.explode', 0.5, 0.9), ('block.anvil.land', 0.4, 0.6),
                     ('block.stone.break', 0.8, 0.7), ('block.deepslate.break', 0.6, 0.8)]),
    'revert': ('The tower collapses back into the ring (C6 end): clunk.',
               [('block.piston.contract', 0.7, 0.9), ('block.chain.place', 0.7, 1.0), ('block.crafter.craft', 0.5, 1.1)]),
    # field
    'halo_flip': ('The halo flips upright before the warp (field +0): whoosh.',
                  [('entity.breeze.whirl', 0.8, 0.8), ('block.vault.close_shutter', 0.5, 1.0)]),
    'warp_out': ('Warp-out flash (field +13): bright zap and a low whoomp.',
                 [('entity.enderman.teleport', 0.8, 0.6), ('entity.illusioner.mirror_move', 0.7, 1.0),
                  ('block.beacon.deactivate', 0.5, 1.6), ('entity.breeze.wind_burst', 0.4, 1.2)]),
    'glitch': ('Violet glitch crackle (field +14..+33 over the old spot, field idle; quiet).',
               [('block.sculk.charge', 0.6, 1.2), ('block.respawn_anchor.ambient', 0.4, 1.8),
                ('entity.evoker.prepare_summon', 0.2, 1.6)]),
    'warp_in': ('Warp-in at the arena centre (field +34).',
                [('entity.enderman.teleport', 0.8, 0.8), ('block.beacon.activate', 0.7, 1.2),
                 ('entity.illusioner.mirror_move', 0.6, 0.8), ('entity.warden.sonic_charge', 0.3, 1.6)]),
    'field_unfold': ('The stack unfolds into the field form (field +35..+51): springs and chains.',
                     [('block.vault.open_shutter', 0.7, 0.7), ('block.piston.extend', 0.7, 0.7),
                      ('block.chain.place', 0.6, 0.8), ('block.respawn_anchor.set_spawn', 0.6, 0.7)]),
    'field_hum': ('Low-gravity field drone (every 40 t while the field is up; quiet).',
                  [('block.conduit.ambient', 0.5, 0.6), ('block.beacon.ambient', 0.4, 0.6)]),
    'field_banner': ('The banner "중력이 감소하고 점프 능력이 향상됩니다" appears (field +57).',
                     [('block.respawn_anchor.set_spawn', 0.7, 0.7), ('block.beacon.power_select', 0.5, 0.6),
                      ('block.amethyst_block.resonate', 0.5, 0.5)]),
    'wave_charge': ('「인력 충격파」 charge, start (24 t / 40 t): rising airy hiss.',
                    [('block.beacon.power_select', 0.7, 0.7), ('block.conduit.activate', 0.6, 1.0),
                     ('block.respawn_anchor.charge', 0.5, 1.0), ('entity.warden.sonic_charge', 0.3, 1.6)]),
    'wave_charge2': ('「인력 충격파」 charge, the last 10 t: higher.',
                     [('block.beacon.power_select', 0.7, 1.4), ('block.respawn_anchor.charge', 0.6, 1.5),
                      ('block.amethyst_block.resonate', 0.5, 1.6)]),
    'wave_beam': ('「인력 충격파」 1-tick beam core -> floor: thump and zap.',
                  [('item.trident.thunder', 0.3, 1.6), ('block.beacon.deactivate', 0.6, 0.6),
                   ('entity.breeze.wind_burst', 0.5, 0.9)]),
    'wave_burst': ('「인력 충격파」 burst flare dome: boom and roar.',
                   [('entity.generic.explode', 0.7, 0.7), ('entity.dragon_fireball.explode', 0.4, 1.0),
                    ('block.fire.ambient', 0.8, 0.8), ('item.firecharge.use', 0.6, 0.6)]),
    'wave_ring': ('「인력 충격파」 front travelling (every 2-3 t at the front point nearest the player; quiet): rumble.',
                  [('block.fire.ambient', 0.3, 1.0), ('block.lava.pop', 0.25, 0.9), ('entity.ravager.step', 0.25, 0.5)]),
    'erupt_tell': ('감소 영역 dark discs appear (F1, per event; quiet).',
                   [('block.respawn_anchor.charge', 0.4, 1.6), ('block.sculk_sensor.clicking', 0.4, 0.8),
                    ('block.gravel.hit', 0.3, 0.6)]),
    'erupt': ('감소 영역 gold eruption (F1, per event): crack and gravel burst.',
              [('block.basalt.break', 0.9, 0.9), ('block.pointed_dripstone.land', 0.6, 1.0),
               ('block.pointed_dripstone.land', 0.5, 1.3), ('entity.generic.explode', 0.4, 1.4),
               ('block.deepslate.break', 0.6, 0.7)]),
    'debris_land': ('Debris settles after an eruption or the blast (quiet).',
                    [('block.gravel.fall', 0.3, 0.8), ('block.stone.fall', 0.25, 0.8)]),
    # meter, break, groggy, end
    'meter_tick': ('A break-meter count (each counted hit): crystalline ping on brass (hud/meter_hit adds a note '
                   'that rises with the count).',
                   [('block.amethyst_block.hit', 0.9, 1.4), ('block.chain.hit', 0.5, 1.2)]),
    'bubble_crack': ('The core bubble cracks a stage further (counts 5, 10, 15).',
                     [('block.glass.break', 0.6, 1.6), ('block.sniffer_egg.crack', 0.7, 1.2),
                      ('block.amethyst_cluster.break', 0.5, 1.4)]),
    'break_glow': ('The bubble lights up before the burst (break +0..+5).',
                   [('block.beacon.activate', 0.7, 1.6), ('block.respawn_anchor.charge', 0.6, 1.9),
                    ('block.amethyst_block.resonate', 0.6, 1.8)]),
    'break_burst': ('The bubble bursts: the field is broken (break +5).',
                    [('block.respawn_anchor.deplete', 0.9, 0.8), ('block.glass.break', 1.0, 0.8),
                     ('block.amethyst_cluster.break', 1.0, 0.8), ('entity.generic.explode', 0.5, 1.2),
                     ('block.beacon.deactivate', 0.7, 0.8)]),
    'groggy_wobble': ('Tilt and damped wobble (break +5..+34): metallic groan.',
                      [('block.anvil.place', 0.4, 0.5), ('block.chain.step', 0.6, 0.6),
                       ('block.heavy_core.place', 0.4, 0.6), ('block.respawn_anchor.deplete', 0.4, 0.6)]),
    'groggy_spark': ('Slow sparks while groggy (every 30-40 t; quiet).',
                     [('block.copper_bulb.turn_off', 0.3, 1.4), ('entity.blaze.burn', 0.2, 1.8),
                      ('block.amethyst_block.step', 0.3, 1.6)]),
    'recover': ('Re-level and core flip back to cruise (groggy end): clockwork.',
                [('block.piston.contract', 0.7, 0.9), ('block.crafter.craft', 0.7, 1.0), ('block.chain.place', 0.7, 1.0),
                 ('block.vault.activate', 0.5, 1.1), ('block.beacon.power_select', 0.4, 1.2)]),
    'lift_off': ('Lift-off pulse when the field ends unbroken (field end +23).',
                 [('entity.breeze.wind_burst', 0.8, 0.7), ('block.beacon.activate', 0.6, 1.2)]),
    'pack_up': ('Lances deploy and the device packs into the compact form (field end): mechanical whirr.',
                [('block.piston.extend', 0.6, 1.3), ('item.spyglass.use', 0.5, 0.8), ('block.chain.place', 0.6, 0.9),
                 ('block.vault.close_shutter', 0.6, 0.9)]),
    'death': ('Death: the seam flickers out and the stack collapses (no voices).',
              [('block.beacon.deactivate', 1.0, 0.7), ('block.respawn_anchor.deplete', 0.8, 0.6),
               ('block.vault.deactivate', 0.8, 0.8), ('block.chain.break', 0.6, 0.7)]),
    'death_fall': ('Halo, pods and ring hit the floor (death).',
                   [('block.anvil.land', 0.7, 0.6), ('block.heavy_core.place', 0.8, 0.5), ('block.chain.fall', 0.6, 0.8),
                    ('block.copper.fall', 0.5, 0.8)]),
    'death_fade': ('The device scales out with gold sparks (death tail).',
                   [('block.amethyst_block.chime', 0.6, 1.4), ('entity.firework_rocket.twinkle', 0.4, 1.2),
                    ('block.beacon.deactivate', 0.5, 1.6)]),
}
METER_PITCH = [round(2 ** ((k - 10) / 12), 3) for k in range(1, 21)]     # rising note per count 1..20


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
SOFT = 40           # ambient presets (AMBIENT) are skipped from SOFT live fx cards on, keeping room for the hits' fx
AMBIENT = ('pebbles', 'gold_streaks', 'field_idle', 'groggy_sparks', 'death_fade', 'missile_trail', 'slab_trail',
           'laser_spot', 'glitch', 'crown_flare', 'debris')


def preset(name, doc, args=()):
    def deco(f):
        PRESETS[name] = (doc, list(args), f)
        return f
    return deco


def ang(deg):
    return num(float(deg), 2)


def radial(n, start=0.0):
    return [start + 360.0 * k / n for k in range(n)]


def ring_xz(r, yaw):
    """^x ^z offsets of the point at radius r, yaw degrees to the executor's right (x = left)"""
    return -r * math.sin(math.radians(yaw)), r * math.cos(math.radians(yaw))


def p3(x, y, z, rel='^'):
    return f'{rel}{num(x, 2)} {rel}{num(y, 2)} {rel}{num(z, 2)}'


# Radial trick: a fixed face / cross card with rot "~<yaw> <90 - elev>" has its local +y pointing outward along yaw /
# elevation, so move (0, d, 0) flies outward and a shard or streak's long axis points along the flight.

# --- generic
@preset('spark', 'A small gold spark burst (tells, clicks, impacts). Billboard.')
def _p_spark():
    return [card('spark', bb='center', spin=60, s0=0.2, s1=1.1, life=5, fade=2),
            part('electric_spark', '~ ~ ~', (0.2, 0.2, 0.2), 0.15, 4)]


@preset('flash', 'A white-gold glow flash (any bright moment). Billboard.')
def _p_flash():
    return [card('glow', bb='center', s0=1.0, s1=4.0, life=5, fade=3, col=GOLD_WHITE)]


@preset('dust_puff', 'A tan dust puff on the floor (landings, scrapes). At the floor point.')
def _p_dust_puff():
    return [card('dust', '~0.4 ~0.4 ~', bb='center', s0=0.5, s1=1.4, move=(0, 0.3, 0), life=12, fade=6),
            card('dust', '~-0.5 ~0.3 ~0.2', bb='center', s0=0.4, s1=1.2, move=(0, 0.25, 0), life=11, fade=6, dly=1),
            dust(DUST, 1.6, '~ ~0.2 ~', (0.5, 0.1, 0.5), 6)]


# --- entrance
@preset('awake', 'Entrance E0 activation: gold flare and electric arcs at the top hub, small ring lights. At the hub.')
def _p_awake():
    return [card('spark', bb='center', spin=45, s0=0.3, s1=2.2, life=6, fade=2),
            card('glow', bb='center', s0=0.5, s1=2.4, life=7, fade=3, col=GOLD),
            card('arc', bb='center', roll=20, s0=0.6, s1=2.2, life=5, fade=2),
            card('arc', bb='center', roll=-50, s0=0.5, s1=1.8, life=5, fade=2, dly=2),
            part('electric_spark', '~ ~ ~', (0.5, 0.3, 0.5), 0.3, 10), part('end_rod', '~ ~ ~', (0.3, 0.3, 0.3), 0.08, 6)]


@preset('unfold', 'Entrance +8..+14: the four pods unfold under the ring (sparks and dust at each pod). At the ring '
        'centre, rotated as the device.')
def _p_unfold():
    out = []
    for yaw in (45, 135, 225, 315):
        x, z = ring_xz(2.95, yaw)
        out.append(card('spark', p3(x, -0.95, z), bb='center', spin=40, s0=0.2, s1=0.9, life=5, fade=2))
        out.append(card('dust', p3(x, -1.1, z), bb='center', s0=0.3, s1=0.9, move=(0, -0.3, 0), life=9, fade=5,
                        col=DUST_PALE))
    out += [part('crit', '~ ~-1 ~', (2.0, 0.2, 2.0), 0.2, 12)]
    return out


@preset('crown_flare', 'Entrance +12..+30: a gold flare as the crown assembles (call 2-3 times). At the hub top.')
def _p_crown_flare():
    return [card('spark', bb='center', spin=60, s0=0.3, s1=1.7, life=5, fade=2),
            card('ripple', bb='center', spin=40, s0=0.5, s1=2.4, life=6, fade=3, col=GOLD),
            card('glint', '~0.3 ~0.2 ~', bb='center', spin=90, s0=0.2, s1=0.7, life=5, fade=2, col=GOLD_PALE, dly=1),
            part('wax_on', '~ ~ ~', (0.4, 0.2, 0.4), 0, 6)]


@preset('eye_open', 'Entrance +38: the red-gold eye opens (glint and glow). At the eye.')
def _p_eye_open():
    return [card('glint', bb='center', spin=45, s0=0.2, s1=1.2, life=8, fade=3, col=rgb('#F6E998')),
            card('glow', bb='center', s0=0.4, s1=1.6, life=10, fade=4, col=rgb('#E2BA78')),
            part('wax_off', '~ ~ ~', (0.2, 0.2, 0.2), 0, 4)]


@preset('rise', 'Entrance +64..+94 (and other lift-offs): a soft gold ground ring and dust under the rising device. At '
        'the floor point under it.')
def _p_rise():
    return [card('ripple', '~ ~0.05 ~', '~ 90', spin=30, s0=0.8, s1=5.5, life=14, fade=6, col=GOLD),
            card('glow', '~ ~0.04 ~', '~ 90', s0=1.0, s1=4.0, life=12, fade=6, col=GOLD_DEEP),
            card('dust', '~1.2 ~0.3 ~0.4', bb='center', s0=0.5, s1=1.6, move=(0, 0.4, 0), life=14, fade=7),
            card('dust', '~-1.0 ~0.3 ~-0.6', bb='center', s0=0.5, s1=1.5, move=(0, 0.35, 0), life=13, fade=7, dly=2),
            dust(DUST, 1.5, '~ ~0.2 ~', (1.2, 0.05, 1.2), 10), part('end_rod', '~ ~1 ~', (0.8, 0.8, 0.8), 0.03, 6)]


# --- C1 bombs and slam
@preset('ports_glow', 'C1 +10: gold dust under the ring as the bomb ports light up (the rig\'s charge look lights the '
        'ports themselves; the module adds a glow card on each port anchor of its rig). At the ring centre, rotated as the '
        'device.')
def _p_ports_glow():
    # review FID-3 (mb3 fix round): no fixed ring of glow cards (it sat at r 1.9 inside the ring hole, 0.7-1.4 b from the
    # real ports at r 2.5-2.8 in the nose-down pose); the module places the port glows at the rig's anchors
    return [dust(rgb('#FCE8AE'), 0.8, '~ ~-0.8 ~', (1.6, 0.1, 1.6), 10)]


@preset('bomb_drop', 'C1: a bomb falls {h} blocks from its port onto the floor point in 5 t with a short gold streak '
        '(call at the floor point; the bomb starts h above).', ('h',))
def _p_bomb_drop():
    return ['$' + card('bomb', '~ ~$(h) ~', bb='vertical', s0=0.75, s1=0.9, move=(0, '-$(h)', 0), life=6, dur=5),
            '$' + card('streak', '~ ~$(h) ~', bb='vertical', roll=90, s0=(0.4, 0.6, 0.6), s1=(1.4, 0.6, 0.6),
                       move=(0, '-$(h)', 0), life=6, dur=5, col=GOLD_PALE)]


@preset('bomb_burst', 'C1 bomb burst r 1.3: gold spiky burst, scorch mark, dust and sparks. At the floor point.')
def _p_bomb_burst():
    return [card('bomb_burst', '~ ~0.6 ~', bb='vertical', spin=0, s0=0.6, s1=2.7, life=5, fade=2),
            card('scorch', '~ ~0.03 ~', '~ 0', s0=1.8, s1=2.4, life=26, fade=10),
            card('dust', '~0.3 ~0.4 ~', bb='center', s0=0.5, s1=1.5, move=(0, 0.35, 0), life=12, fade=6),
            dust(rgb('#CAA481'), 1.8, '~ ~0.5 ~', (0.5, 0.3, 0.5), 8), part('crit', '~ ~0.5 ~', (0.3, 0.3, 0.3), 0.4, 6),
            dust(rgb('#793D15'), 1.0, '~ ~0.4 ~', (0.6, 0.3, 0.6), 4)]


@preset('column_tell', 'C1 / C2 slam tell (13 t): the gold column from the face-down core to the floor, a floor glow '
        'and a base flare. At the floor point under the core; {h} = the core height above the floor.', ('h',))
def _p_column_tell():
    return ['$' + card('column', '~ ~ ~', '~ 0', s0=(0.3, '$(h)', 0.3), s1=(1.15, '$(h)', 1.15), life=15, fade=2,
                       dur=4),
            card('glow', '~ ~0.04 ~', '~ 90', s0=0.6, s1=2.6, life=15, fade=3, col=GOLD),
            card('spark', '~ ~0.3 ~', bb='center', spin=60, s0=0.3, s1=1.6, life=6, fade=3, dly=9),
            part('end_rod', '~ ~1.5 ~', (0.15, 1.2, 0.15), 0.02, 8)]


@preset('column_base', 'C1 / C2 slam point: the late base flare where the rig\'s gold column meets the floor (the footage\'s '
        'flare at the column foot, v1 9.10, about 5 t before the impact). At the floor point.')
def _p_column_base():
    # review FID-5 (mb3 fix round): the rig draws the column under the device. Telegraph rule 10-20 (the footage shows no
    # area marker for the slam, only the face-down core's column): the 15 t floor glow at the not yet reached lock and
    # the end rods are gone; the base flare stays (called 12 t into the slam, 5 t before its impact)
    return [card('spark', '~ ~0.3 ~', bb='center', spin=60, s0=0.3, s1=1.6, life=6, fade=3)]


@preset('plunge', 'C1 / C2 plunge (3-4 t): speed lines streaming up past the dropping device. At the ring centre.')
def _p_plunge():
    out = []
    for yaw in radial(6, 15):
        x, z = ring_xz(2.6, yaw)
        out.append(card('streak', p3(x, 0.5, z), bb='vertical', roll=90, s0=(1.5, 1, 1), s1=(3.0, 1, 1),
                        move=(0, 3.0, 0), life=5, fade=2, col=GOLD_PALE))
    out.append(part('cloud', '~ ~-1 ~', (1.2, 0.3, 1.2), 0.05, 6))
    return out


@preset('slam', 'C1 / C2 slam impact r 5: gold crystal-shard burst, shock ring, flash, dust ring. At the floor point.')
def _p_slam():
    rnd = random.Random(186)
    out = [card('slam_ring', '~ ~0.06 ~', '~ 0', spin=30, s0=1.0, s1=5.2, life=10, fade=4, dur=5),
           card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=6.0, life=6, fade=3, col=rgb('#F9DFAD')),
           card('spike_fan', '~ ~ ~', bb='vertical', s0=0.6, s1=3.2, life=7, fade=3, dur=3),
           card('glow', '~ ~1 ~', bb='center', s0=1.5, s1=5.0, life=4, fade=2, col=GOLD_WHITE)]
    for yaw in radial(10, 9):
        el = rnd.uniform(15, 60)
        out.append(card('gold_shard', '~ ~0.5 ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(-20, 20),
                        s0=0.6, s1=rnd.uniform(1.1, 1.7), move=(0, rnd.uniform(2.4, 3.6), 0), life=9, fade=4))
    for yaw in radial(4, 30):
        x, z = ring_xz(3.6, yaw)
        out.append(card('dust', p3(x, 0.5, z, '~'), bb='center', s0=0.8, s1=2.3, move=(0, 0.4, 0), life=14, fade=7,
                        dly=1))
    out += [part('explosion', '~ ~0.5 ~', (0.3, 0.1, 0.3), 0, 1), dust(DUST, 2.6, '~ ~0.4 ~', (3.0, 0.2, 3.0), 24),
            part('crit', '~ ~0.6 ~', (1.5, 0.4, 1.5), 0.5, 14), blockp('smooth_sandstone', '~ ~0.3 ~', (2, 0.2, 2), 0.2, 20)]
    return out


# --- C3 lasers
@preset('pods_drop', 'C3 +0..+4: a medallion drops beside the core (clank sparks). At the medallion.')
def _p_pods_drop():
    return [card('spark', bb='center', spin=60, s0=0.2, s1=1.0, life=5, fade=2),
            card('dust', '~ ~-0.3 ~', bb='center', s0=0.3, s1=0.8, move=(0, -0.2, 0), life=8, fade=4, col=DUST_PALE),
            part('crit', '~ ~ ~', (0.3, 0.3, 0.3), 0.3, 6)]


@preset('laser_charge', 'C3 spark charge (18 t): gold glints spin on a pod, an arc and a growing glow (call 3-4 '
        'times). At the medallion.')
def _p_laser_charge():
    rnd = random.Random(18)
    out = [card('glow', bb='center', s0=0.3, s1=1.1, life=10, fade=3, col=GOLD)]
    for k in range(3):
        x, y, z = rnd.uniform(-0.5, 0.5), rnd.uniform(-0.4, 0.4), rnd.uniform(-0.5, 0.5)
        out.append(card('glint', p3(x, y, z, '~'), bb='center', spin=120, s0=0.2, s1=0.9, life=6, fade=3,
                        col=GOLD_PALE, dly=k * 2))
    out.append(card('arc', bb='center', roll=rnd.randint(0, 179), s0=0.4, s1=1.3, life=4, fade=2, dly=3))
    out += [part('electric_spark', '~ ~ ~', (0.4, 0.4, 0.4), 0.2, 6), part('wax_on', '~ ~ ~', (0.5, 0.5, 0.5), 0, 4)]
    return out


@preset('aim_line', 'C3 +22: a thin white aim line flickers from the muzzle along the beam for 2 t ({len} = the beam '
        'length). At the muzzle, rotated as the beam (yaw and pitch).', ('len',))
def _p_aim_line():
    return ['$' + card('laser_core', '~ ~ ~', '~ ~-90', s0=(0.07, '$(len)', 0.07), s1=(0.07, '$(len)', 0.07), life=2,
                       col=rgb('#FFF6DA'))]


@preset('laser_fire', 'C3 +24 fire: the muzzle ring and the beam bloom (about 1 b wide for 3 t, {len} = the beam '
        'length). At the muzzle, rotated as the beam.', ('len',))
def _p_laser_fire():
    return [card('muzzle', bb='center', spin=60, s0=0.4, s1=1.5, life=5, fade=2),
            '$' + card('laser_glow', '~ ~ ~', '~ ~-90', s0=(0.8, '$(len)', 0.8), s1=(1.7, '$(len)', 1.7), life=4,
                       fade=1, dur=2),
            card('spark', bb='center', spin=45, s0=0.4, s1=1.6, life=4, fade=2),
            part('electric_spark', '~ ~ ~', (0.2, 0.2, 0.2), 0.3, 6)]


@preset('laser_spot', 'C3 beam floor spot (call every 2-3 t at each spot): scorch, a gold glow and sparks.')
def _p_laser_spot():
    return [card('scorch', '~ ~0.03 ~', '~ 0', spin=40, s0=0.8, s1=1.2, life=16, fade=8),
            card('glow', '~ ~0.06 ~', '~ 90', s0=0.6, s1=1.5, life=4, fade=2, col=rgb('#FADEA8')),
            part('electric_spark', '~ ~0.2 ~', (0.2, 0.1, 0.2), 0.25, 3), part('smoke', '~ ~0.2 ~', (0.15, 0.1, 0.15), 0.01, 1),
            part('small_flame', '~ ~0.1 ~', (0.2, 0.05, 0.2), 0.01, 1)]


@preset('laser_end', 'C3 beams off: a power-down spark and smoke at the muzzle.')
def _p_laser_end():
    return [card('spark', bb='center', spin=-60, s0=0.6, s1=0.2, life=5, fade=2),
            card('smoke', bb='center', s0=0.3, s1=0.9, move=(0, 0.4, 0), life=10, fade=5),
            part('smoke', '~ ~ ~', (0.15, 0.15, 0.15), 0.02, 4)]


# --- C4 missiles
@preset('tip_flare', 'C4 tell 1 (8 t; also the next-pattern tell): a gold 4-point starburst with electric arcs. At a '
        'spike tip.')
def _p_tip_flare():
    return [card('spark', bb='center', spin=45, s0=0.4, s1=2.5, life=8, fade=3),
            card('glow', bb='center', s0=0.5, s1=1.7, life=8, fade=3, col=GOLD),
            card('arc', bb='center', roll=30, s0=0.5, s1=1.9, life=5, fade=2),
            card('arc', bb='center', roll=-70, s0=0.5, s1=1.6, life=5, fade=2, dly=3),
            part('electric_spark', '~ ~ ~', (0.3, 0.3, 0.3), 0.25, 8), part('end_rod', '~ ~ ~', (0.1, 0.1, 0.1), 0.05, 3)]


@preset('vent_shaft', 'C4 tell 2 (13 t): the vertical gold light shaft vents up from the hub, vent flames. At the hub '
        'top.')
def _p_vent_shaft():
    return [card('column', '~ ~ ~', '~ 0', s0=(0.3, 6.0, 0.3), s1=(1.5, 7.0, 1.5), life=13, fade=3, dur=4,
                 col=GOLD_PALE),
            card('flame', '~0.6 ~ ~', bb='vertical', s0=0.4, s1=1.5, life=10, fade=3),
            card('flame', '~-0.6 ~ ~0.1', bb='vertical', s0=0.4, s1=1.4, life=10, fade=3, dly=2),
            card('glow', '~ ~0.5 ~', bb='center', s0=1.0, s1=3.0, life=6, fade=3, col=GOLD),
            part('flame', '~ ~0.3 ~', (0.4, 0.2, 0.4), 0.04, 8), part('end_rod', '~ ~3 ~', (0.3, 2.5, 0.3), 0.05, 10)]


@preset('missile_launch', 'C4 launch (each missile): vent flame and smoke puffs. At the vent.')
def _p_missile_launch():
    return [card('flame', bb='vertical', s0=0.3, s1=1.1, life=4, fade=2),
            card('smoke', '~ ~0.2 ~', bb='center', s0=0.3, s1=1.0, move=(0, 0.4, 0), life=12, fade=6),
            part('flame', '~ ~ ~', (0.15, 0.1, 0.15), 0.05, 3), part('cloud', '~ ~0.2 ~', (0.2, 0.2, 0.2), 0.02, 2)]


@preset('missile_trail', 'C4 smoke trail puff left behind a missile (call every 3 t at the missile prop).')
def _p_missile_trail():
    return [card('smoke', bb='center', roll=30, s0=0.35, s1=0.85, life=7, fade=4),
            part('firework', '~ ~ ~', (0.05, 0.05, 0.05), 0.01, 1)]


@preset('missile_impact', 'C4 impact r 1.5: gold crystal-spike burst, a floor glow and dust. At the floor point.')
def _p_missile_impact():
    return [card('spike_fan', '~ ~ ~', bb='vertical', s0=0.4, s1=2.0, life=6, fade=3, dur=3),
            card('glow', '~ ~0.05 ~', '~ 90', s0=0.5, s1=2.0, life=6, fade=3, col=rgb('#F8E0B0')),
            card('dust', '~0.3 ~0.4 ~', bb='center', s0=0.4, s1=1.4, move=(0, 0.3, 0), life=11, fade=6),
            dust(rgb('#D7AE89'), 1.6, '~ ~0.5 ~', (0.5, 0.3, 0.5), 8), part('crit', '~ ~0.5 ~', (0.3, 0.3, 0.3), 0.4, 5)]


# --- C5 지면 충격 / 중력 폭발
@preset('core_spark', 'C5 tell 1: a gold spark on the core with arcs. At the core.')
def _p_core_spark():
    return [card('spark', bb='center', spin=60, s0=0.3, s1=1.7, life=6, fade=2),
            card('arc', bb='center', roll=10, s0=0.4, s1=1.4, life=4, fade=2),
            card('arc', bb='center', roll=100, s0=0.4, s1=1.2, life=4, fade=2, dly=2),
            part('electric_spark', '~ ~ ~', (0.4, 0.4, 0.4), 0.3, 8), part('wax_on', '~ ~ ~', (0.4, 0.4, 0.4), 0, 4)]


@preset('core_lift', 'C5 +5 "번쩍": a gold flame burst around the core as it lifts. At the core.')
def _p_core_lift():
    out = [card('glow', bb='center', s0=1.0, s1=4.2, life=6, fade=3, col=FLARE),
           card('spark', bb='center', spin=45, s0=0.5, s1=2.8, life=5, fade=2)]
    for yaw in radial(4, 20):
        x, z = ring_xz(0.8, yaw)
        out.append(card('flame', p3(x, -0.4, z, '~'), bb='vertical', s0=0.4, s1=1.5, life=7, fade=3))
    out += [flash(FLARE, '~ ~ ~', 0.9), part('end_rod', '~ ~ ~', (0.4, 0.4, 0.4), 0.15, 10)]
    return out


@preset('up_beam', 'C5 +29..+40: the upward gold beam from the raised core with crawling arcs. At the core.')
def _p_up_beam():
    return [card('column', '~ ~ ~', '~ 0', s0=(0.3, 8.0, 0.3), s1=(1.3, 9.0, 1.3), life=11, fade=3, dur=3,
                 col=rgb('#FBE3B1')),
            card('arc', '~ ~0.6 ~', bb='center', roll=80, s0=0.5, s1=1.6, life=4, fade=2),
            card('arc', '~ ~1.4 ~', bb='center', roll=95, s0=0.5, s1=1.8, life=4, fade=2, dly=3),
            card('arc', '~ ~2.4 ~', bb='center', roll=70, s0=0.5, s1=1.8, life=4, fade=2, dly=6),
            part('electric_spark', '~ ~1 ~', (0.3, 1.0, 0.3), 0.2, 10), part('end_rod', '~ ~3 ~', (0.15, 2.0, 0.15), 0.05, 8)]


@preset('rim_flare', 'C5 +36..+41: the rim at the final radius {r} flares bright (last warning). At the floor centre.',
        ('r',))
def _p_rim_flare():
    # the ripple sprite is 1 b across at scale 1 (a -0.5..0.5), so a ring of radius r needs the scale 2 r (telegraph rule
    # 10-20: with the fill decal gone the flare must sit on the kept rim; it was drawn at r / 2)
    return [f'$data modify storage {STO} fl.r set value $(r)d',
            f'execute store result storage {STO} fl.d double 0.02 run data get storage {STO} fl.r 100',
            f'function {FN}p/e/rim_flare with storage {STO} fl']


def _p_e_rim_flare():
    return ['$' + card('ripple', '~ ~0.07 ~', '~ 90', spin=20, s0='$(d)', s1='$(d)', life=7, fade=3, col=RIM_PALE),
            '$' + card('ripple', '~ ~0.08 ~', '~ 90', spin=-25, s0='$(d)', s1='$(d)', life=6, fade=3,
                       col=rgb('#F9E6C2'), dly=1)]


@preset('column_down', 'C5 +41..+44: the gold column down from the core through the violet pendulum glow. At the floor '
        'point under the core; {h} = the core height.', ('h',))
def _p_column_down():
    return ['$' + card('column', '~ ~ ~', '~ 0', s0=(0.5, '$(h)', 0.5), s1=(1.0, '$(h)', 1.0), life=5, fade=2, dur=2,
                       col=rgb('#F5D9A6')),
            '$' + card('column', '~ ~ ~', '~45 0', s0=(0.25, '$(h)', 0.25), s1=(0.5, '$(h)', 0.5), life=5, fade=2,
                       dur=2, col=rgb('#D9BCD1')),
            part('end_rod', '~ ~1.5 ~', (0.1, 1.2, 0.1), 0.05, 6)]


@preset('floor_hit', 'C5 +44: the column hits the floor centre: gold crystal-shard burst. At the floor centre.')
def _p_floor_hit():
    rnd = random.Random(44)
    out = [card('spike_fan', '~ ~ ~', bb='vertical', s0=0.5, s1=3.0, life=6, fade=3, dur=3),
           card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=3.5, life=6, fade=3, col=rgb('#FDE8A2'))]
    for yaw in radial(8, 12):
        el = rnd.uniform(20, 65)
        out.append(card('gold_shard', '~ ~0.4 ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(-20, 20), s0=0.5,
                        s1=rnd.uniform(0.9, 1.4), move=(0, rnd.uniform(1.6, 2.6), 0), life=8, fade=4))
    out.append(part('crit', '~ ~0.5 ~', (0.5, 0.3, 0.5), 0.5, 10))
    return out


@preset('blast', 'C5 +48 full-area blast over radius {r}: a white-gold flash over the disc, the jagged gold crack ring at '
        'the rim, a shock ring (pair with p/rocks). At the floor centre.', ('r',))
def _p_blast():
    return ['$' + card('glow', '~ ~0.06 ~', '~ 90', s0=0.5, s1='$(r)', life=6, fade=3, dur=3, col=rgb('#FDF1D1')),
            '$' + card('crack_ring', '~ ~0.04 ~', '~ 0', s0='$(r)', s1='$(r)', life=30, fade=10),
            '$' + card('ripple', '~ ~0.08 ~', '~ 90', spin=40, s0=1.0, s1='$(r)', life=7, fade=2, dur=4,
                       col=rgb('#FCEFB2')),
            card('glow', '~ ~1 ~', bb='center', s0=2.0, s1=8.0, life=5, fade=3, col=WHITE),
            part('explosion', '~ ~0.5 ~', (3.0, 0.2, 3.0), 0, 4), dust(rgb('#FDF1D1'), 3.0, '~ ~0.6 ~', (6, 0.3, 6), 40),
            part('firework', '~ ~0.5 ~', (4, 0.3, 4), 0.05, 20), blockp('smooth_sandstone', '~ ~0.4 ~', (5, 0.3, 5), 0.3, 30)]


@preset('rocks', 'C5 +48..+77: about a dozen floor rocks launched across the disc hover, then drift down. At the floor '
        'centre (spread r 2-11).')
def _p_rocks():
    rnd = random.Random(4877)
    out = []
    for k in range(12):
        r = rnd.uniform(2.0, 11.0)
        yaw = rnd.uniform(0, 360)
        x, z = ring_xz(r, yaw)
        h = rnd.uniform(1.0, 2.6)
        out.append(card('chunk', p3(x, 0.3, z, '~'), bb='center', roll=rnd.randint(0, 90), spin=rnd.choice((-1, 1)) * 90,
                        s0=0.25, s1=rnd.uniform(0.5, 0.9), move=(0, h, 0), life=rnd.randint(34, 42), fade=12,
                        dur=8, dly=rnd.randint(0, 3)))
    return out


# --- C6 / F2 파쇄
@preset('dip', 'C6 +0: the dip and roll toward the player (dust kicked up and two speed lines). At the floor point '
        'under the device, rotated as it.')
def _p_dip():
    return [card('streak', '^ ^2.5 ^-1', '~90 0', s0=1.0, s1=3.5, life=5, fade=2, col=GOLD_PALE),
            card('streak', '^1 ^3.2 ^-0.5', '~90 0', s0=0.8, s1=3.0, life=5, fade=2, col=GOLD_PALE, dly=1),
            card('dust', '^ ^0.3 ^1', bb='center', s0=0.5, s1=1.6, move=(0, 0.3, 0), life=12, fade=6),
            dust(DUST, 1.4, '^ ^0.2 ^1', (1.0, 0.05, 1.0), 6)]


@preset('vent_flare', 'C6 +12 (8 t): the vent flare bursts up from the top centre as the medallions are flung. At the '
        'hub top.')
def _p_vent_flare():
    return [card('column', '~ ~ ~', '~ 0', s0=(0.4, 4.0, 0.4), s1=(1.5, 5.0, 1.5), life=8, fade=3, dur=3,
                 col=GOLD_PALE),
            card('spark', '~ ~0.6 ~', bb='center', spin=60, s0=0.5, s1=2.2, life=5, fade=2),
            card('flame', '~0.5 ~ ~', bb='vertical', s0=0.4, s1=1.3, life=7, fade=3),
            card('flame', '~-0.5 ~ ~', bb='vertical', s0=0.4, s1=1.2, life=7, fade=3, dly=1),
            part('flame', '~ ~0.4 ~', (0.3, 0.3, 0.3), 0.06, 10)]


@preset('tower_up', 'C6 +20 (18 t): gold sparks race up the telescoping tower. At the ring centre.')
def _p_tower_up():
    out = [card('glow', '~ ~0.4 ~', bb='center', s0=0.8, s1=2.0, life=10, fade=4, col=GOLD)]
    for k in range(6):
        yaw = 60 * k
        x, z = ring_xz(0.5, yaw)
        out.append(card('glint', p3(x, 0.2, z, '~'), bb='center', spin=90, s0=0.15, s1=0.4, move=(0, 3.6, 0), life=9,
                        fade=3, col=GOLD_PALE, dly=k * 2))
    out.append(part('wax_on', '~ ~1.5 ~', (0.3, 1.2, 0.3), 0, 6))
    return out


@preset('flame_band', 'C6 charge (17 t): the horizontal gold flame band flares and pulses under the ring (Ø 4.5 -> 8 '
        'b) with standing flame licks. At the ring underside.')
def _p_flame_band():
    out = [card('fire_disc', '~ ~ ~', '~ 0', spin=60, s0=2.2, s1=4.1, life=18, fade=3, dur=15),
           card('fire_disc', '~ ~0.02 ~', '~ 0', spin=-80, s0=2.8, s1=3.7, life=14, fade=3, dly=4, col=rgb('#FEF5AD'))]
    for yaw in radial(6, 10):
        x, z = ring_xz(3.1, yaw)
        out.append(card('flame', p3(x, 0, z, '~'), bb='vertical', s0=0.3, s1=1.0, life=10, fade=3, dly=int(yaw) % 5))
    out += [part('flame', '~ ~ ~', (2.4, 0.1, 2.4), 0.02, 14), part('small_flame', '~ ~ ~', (3.0, 0.1, 3.0), 0.01, 10)]
    return out


@preset('floor_burst', 'C6 / F2 floor burst r 1.8: a gold crystal-spike fan, rock chips and a white dust ring. At the '
        'floor point.')
def _p_floor_burst():
    rnd = random.Random(1800)
    out = [card('spike_fan', '~ ~ ~', bb='vertical', s0=0.5, s1=2.7, life=9, fade=3, dur=2),
           card('spike_fan', '~ ~ ~', bb='vertical', roll=12, s0=0.4, s1=1.8, life=7, fade=3, dur=2, dly=1),
           card('ripple', '~ ~0.06 ~', '~ 90', spin=50, s0=0.6, s1=3.8, life=8, fade=3, col=rgb('#D5C4C0')),
           card('glow', '~ ~0.05 ~', '~ 90', s0=0.6, s1=2.2, life=5, fade=2, col=rgb('#FBEEC8'))]
    for yaw in radial(4, 20):
        el = rnd.uniform(35, 70)
        out.append(card('chunk', '~ ~0.4 ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(0, 90), s0=0.25, s1=0.4,
                        move=(0, rnd.uniform(1.4, 2.4), 0), life=9, fade=4, col=rgb('#C9B4A8')))
    out += [part('crit', '~ ~0.4 ~', (0.4, 0.3, 0.4), 0.4, 8), part('cloud', '~ ~0.2 ~', (0.6, 0.1, 0.6), 0.04, 4)]
    return out


@preset('slab_rise', 'C6 / F2: a slab tears out of the floor (gold rim glow, dust, chips). At the floor point.')
def _p_slab_rise():
    return [card('glow', '~ ~0.05 ~', '~ 90', s0=0.8, s1=2.4, life=8, fade=4, col=rgb('#FDEE89')),
            card('dust', '~0.4 ~0.3 ~', bb='center', s0=0.5, s1=1.4, move=(0, 0.3, 0), life=11, fade=6),
            card('dust', '~-0.4 ~0.3 ~0.2', bb='center', s0=0.4, s1=1.2, move=(0, 0.3, 0), life=10, fade=6, dly=1),
            card('chunk', '~0.3 ~0.2 ~', bb='center', s0=0.2, s1=0.35, move=(0, 1.6, 0), life=10, fade=4),
            card('chunk', '~-0.2 ~0.2 ~-0.3', bb='center', s0=0.2, s1=0.3, move=(0, 1.3, 0), life=9, fade=4),
            dust(DUST, 1.4, '~ ~0.2 ~', (0.6, 0.05, 0.6), 6)]


@preset('slab_throw', 'C6 / F2 throw: white-gold streaks as the slab is flung. At the slab, rotated along the throw.')
def _p_slab_throw():
    return [card('streak', '^ ^ ^-1', '~90 0', s0=1.0, s1=3.5, life=5, fade=2, col=rgb('#FDE59E')),
            card('streak', '^0.3 ^0.2 ^-1.2', '~90 0', s0=0.8, s1=2.6, life=4, fade=2, col=WHITE, dly=1),
            card('spark', bb='center', spin=45, s0=0.4, s1=1.5, life=4, fade=2)]


@preset('slab_trail', 'C6 / F2: a short white-gold streak behind a flying slab (call every 2 t at the slab prop, '
        'rotated along its flight).')
def _p_slab_trail():
    return [card('streak', '^ ^ ^-0.8', '~90 0', s0=1.4, s1=0.6, life=5, fade=3, col=rgb('#FDE59E')),
            part('end_rod', '~ ~ ~', (0.1, 0.1, 0.1), 0.01, 1)]


@preset('slab_glint', 'C6 / F2 throw tell (10 t before the throw, when the feet are locked): the hovering slab flares on '
        'itself, a gold glow and a white-gold glint on the slab, not on the floor (telegraph rule 10-20: the throw lanes '
        'are gone). At the slab.')
def _p_slab_glint():
    return [card('glow', bb='center', s0=1.4, s1=2.8, life=10, fade=4, col=GOLD),
            card('glint', bb='center', spin=90, s0=0.4, s1=2.4, life=7, fade=3, col=GOLD_WHITE),
            part('electric_spark', '~ ~ ~', (0.6, 0.2, 0.6), 0.1, 6)]


@preset('slab_impact', 'C6 / F2: a slab crashes onto the floor (dust, chunks, a gold glow). At the floor point.')
def _p_slab_impact():
    rnd = random.Random(11)
    out = [card('glow', '~ ~0.05 ~', '~ 90', s0=0.8, s1=2.6, life=5, fade=2, col=rgb('#FBD377')),
           card('dust', '~ ~0.5 ~', bb='center', s0=0.6, s1=2.0, move=(0, 0.4, 0), life=13, fade=6),
           card('dust', '~0.6 ~0.3 ~0.3', bb='center', s0=0.4, s1=1.5, move=(0, 0.3, 0), life=12, fade=6, dly=1)]
    for yaw in radial(4, 40):
        el = rnd.uniform(30, 60)
        out.append(card('chunk', '~ ~0.4 ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(0, 90), s0=0.3, s1=0.45,
                        move=(0, rnd.uniform(1.2, 2.0), 0), life=9, fade=4, col=rgb('#C59B91')))
    out += [blockp('tuff', '~ ~0.3 ~', (0.6, 0.2, 0.6), 0.2, 10), part('crit', '~ ~0.4 ~', (0.4, 0.2, 0.4), 0.3, 5)]
    return out


@preset('revert', 'C6 end: the tower folds back (sparks and a small dust ring). At the ring centre.')
def _p_revert():
    return [card('spark', '~ ~0.5 ~', bb='center', spin=60, s0=0.3, s1=1.4, life=5, fade=2),
            card('spark', '~0.5 ~1.4 ~', bb='center', spin=-60, s0=0.3, s1=1.1, life=5, fade=2, dly=3),
            card('ripple', '~ ~ ~', '~ 90', spin=40, s0=1.0, s1=4.0, life=7, fade=3, col=GOLD),
            part('crit', '~ ~0.5 ~', (0.6, 0.6, 0.6), 0.2, 6)]


# --- field: warp, unfold, idle
@preset('halo_flip', 'Field +0..+12: the halo flips upright (whirling gold streaks). At the halo.')
def _p_halo_flip():
    return [card('streak', bb='center', roll=20, spin=170, s0=2.0, s1=3.6, life=6, fade=3, col=rgb('#E2C1B8')),
            card('streak', bb='center', roll=110, spin=170, s0=1.8, s1=3.2, life=6, fade=3, col=GOLD_PALE, dly=2),
            card('glint', '~1.5 ~ ~', bb='center', spin=90, s0=0.2, s1=0.8, life=5, fade=2, col=GOLD_PALE),
            card('glint', '~-1.5 ~ ~', bb='center', spin=90, s0=0.2, s1=0.8, life=5, fade=2, col=GOLD_PALE, dly=2)]


@preset('warp_out', 'Field +13 warp-out: the 1-2 frame white-cyan pillar where the device was, glitch streaks start, '
        'gold dust on the floor. At the floor point under it.')
def _p_warp_out():
    rnd = random.Random(1313)
    out = [card('warp_pillar', '~ ~ ~', bb='vertical', s0=(3.2, 3.4, 3.2), s1=(2.2, 3.6, 2.2), life=4, fade=2),
           card('warp_bloom', '~ ~4.5 ~', bb='center', s0=2.0, s1=7.0, life=4, fade=2)]
    for k in range(4):
        x, z = rnd.uniform(-2.2, 2.2), rnd.uniform(-2.2, 2.2)
        out.append(card('glitch', p3(x, rnd.uniform(1.5, 4.5), z, '~'), bb='vertical', roll=rnd.randint(-25, 25),
                        s0=0.8, s1=1.6, move=(0, 1.4, 0), life=9, fade=3, dly=1 + k * 2))
    out += [dust(BRASS, 1.2, '~ ~0.1 ~', (1.5, 0.02, 1.5), 16), part('reverse_portal', '~ ~3 ~', (1.2, 1.5, 1.2), 0.05, 30),
            flash(CYAN_PALE, '~ ~3 ~', 1.0)]
    return out


@preset('glitch', 'Field +14..+33: violet glitch streaks drift up and out over the old spot (call every 4-5 t). At '
        'the old spot (floor).')
def _p_glitch():
    rnd = random.Random(1433)
    out = []
    for k in range(3):
        x, z = rnd.uniform(-2.6, 2.6), rnd.uniform(-2.6, 2.6)
        out.append(card('glitch', p3(x, rnd.uniform(1.0, 5.0), z, '~'), bb='vertical', roll=rnd.randint(-30, 30),
                        s0=0.6, s1=1.4, move=(0, 1.0, 0), life=6, fade=2, dly=k))
    out += [part('witch', '~ ~3 ~', (1.5, 1.5, 1.5), 0, 4), dust(VIOLET_DEEP, 1.2, '~ ~3 ~', (1.8, 1.8, 1.8), 6)]
    return out


@preset('warp_in', 'Field +34 warp-in at the arena centre: a white-cyan bloom and a violet ring. At the core.')
def _p_warp_in():
    return [card('warp_bloom', bb='center', s0=2.0, s1=9.0, life=5, fade=3),
            card('ripple', bb='center', spin=60, s0=1.0, s1=8.0, life=7, fade=3, col=rgb('#969CFE')),
            card('glint', bb='center', spin=45, s0=0.5, s1=3.0, life=4, fade=2, col=WHITE),
            flash(CYAN_PALE, '~ ~ ~', 1.0), part('end_rod', '~ ~ ~', (0.8, 0.8, 0.8), 0.2, 16)]


@preset('warp_pillar', 'A white-cyan warp pillar standing on the floor (warp-in, the field arrival). At the floor point.')
def _p_warp_pillar():
    return [card('warp_pillar', '~ ~ ~', bb='vertical', s0=(2.4, 3.0, 2.4), s1=(1.6, 3.4, 1.6), life=5, fade=3),
            card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=3.5, life=6, fade=3, col=CYAN)]


@preset('field_unfold', 'Field +35..+51: the violet column grows under the core, violet tendrils whip out, a violet '
        'glow. At the core.')
def _p_field_unfold():
    rnd = random.Random(3551)
    out = [card('ousia_col', '~ ~ ~', '~ 0', s0=(0.3, 3.4, 0.3), s1=(1.0, 3.8, 1.0), life=16, fade=6, dur=6),
           card('glow', bb='center', s0=1.0, s1=4.2, life=8, fade=3, col=VIOLET)]
    for yaw in radial(4, 25):
        el = rnd.uniform(-30, 30)
        out.append(card('glitch', '~ ~ ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(-15, 15), s0=0.8, s1=1.8,
                        move=(0, rnd.uniform(1.6, 2.6), 0), life=8, fade=3, dly=rnd.randint(0, 3)))
    out += [part('reverse_portal', '~ ~ ~', (1.0, 1.0, 1.0), 0.1, 30), part('witch', '~ ~-1 ~', (0.6, 1.0, 0.6), 0, 8)]
    return out


@preset('field_idle', 'Field idle (every 10-20 t): violet crackle under the core. At the core.')
def _p_field_idle():
    rnd = random.Random(10)
    return [card('glitch', p3(rnd.uniform(-0.5, 0.5), -1.2, rnd.uniform(-0.5, 0.5), '~'), bb='vertical',
                 roll=rnd.randint(-30, 30), s0=0.4, s1=0.85, life=6, fade=2),
            part('witch', '~ ~-1.4 ~', (0.4, 0.6, 0.4), 0, 2), dust(VIOLET, 0.9, '~ ~-1.2 ~', (0.4, 0.6, 0.4), 3)]


@preset('pebbles', 'Field (every 20 t around the player): pebbles float up slowly, the low-gravity cue (r 1.5-5 '
        'around, never at the eyes). At the player\'s feet.')
def _p_pebbles():
    rnd = random.Random(2020)
    out = []
    for k in range(6):
        r = rnd.uniform(1.5, 5.0)
        x, z = ring_xz(r, rnd.uniform(0, 360))
        out.append(card('pebble', p3(x, rnd.uniform(0.1, 0.9), z, '~'), bb='center', roll=rnd.randint(0, 90),
                        spin=rnd.choice((-1, 1)) * rnd.randint(40, 120), s0=0.14, s1=rnd.uniform(0.16, 0.26),
                        move=(0, rnd.uniform(0.6, 1.3), 0), life=rnd.randint(40, 56), fade=10, dly=rnd.randint(0, 10)))
    out.append(part('white_ash', '~ ~0.8 ~', (3.0, 0.6, 3.0), 0.01, 6))
    return out


@preset('gold_streaks', 'Field charge cue: gold streaks rise from the floor around the device (r 2-6). At the floor '
        'point under it.')
def _p_gold_streaks():
    rnd = random.Random(750)
    out = []
    for k in range(5):
        x, z = ring_xz(rnd.uniform(2.0, 6.0), rnd.uniform(0, 360))
        out.append(card('streak', p3(x, 0.4, z, '~'), bb='vertical', roll=90, s0=(1.2, 0.8, 0.8), s1=(2.2, 0.8, 0.8),
                        move=(0, 2.6, 0), life=10, fade=3, col=GOLD_PALE, dly=rnd.randint(0, 8)))
    out.append(part('end_rod', '~ ~0.5 ~', (3.0, 0.2, 3.0), 0.04, 6))
    return out


# --- field: 「인력 충격파」
@preset('wave_charge', '「인력 충격파」 charge: the yellow sphere grows around the lower core over {t} ticks with a glow '
        'and arcs (24 t, the third 40 t). At the core.', ('t',))
def _p_wave_charge():
    return ['$' + card('charge_sphere', bb='center', spin=60, s0=0.4, s1=3.9, life='$(t)', fade=1, dur='$(t)'),
            '$' + card('glow', bb='center', s0=1.0, s1=5.0, life='$(t)', fade=2, dur='$(t)', col=GOLD),
            card('arc', bb='center', roll=40, s0=0.6, s1=2.2, life=5, fade=2, dly=4),
            card('arc', bb='center', roll=-30, s0=0.6, s1=2.2, life=5, fade=2, dly=10),
            part('electric_spark', '~ ~ ~', (0.8, 0.8, 0.8), 0.2, 8)]


@preset('wave_pulse', '「인력 충격파」 charge pulse (call every 8 t of the charge): streaks converge on the sphere and a '
        'glint flares. At the core.')
def _p_wave_pulse():
    out = [card('glint', bb='center', spin=90, s0=0.5, s1=2.4, life=5, fade=2, col=GOLD_WHITE)]
    for k, roll in enumerate((15, 75, 135)):
        out.append(card('streak', bb='center', roll=roll, s0=5.0, s1=0.6, life=7, fade=1, col=GOLD_PALE, dly=k))
    return out


@preset('wave_beam', '「인력 충격파」 the 1-2 tick vertical gold beam core -> floor with a floor splash ({h} = the core '
        'height). At the floor point under the core.', ('h',))
def _p_wave_beam():
    return ['$' + card('column', '~ ~ ~', '~ 0', s0=(0.45, '$(h)', 0.45), s1=(0.55, '$(h)', 0.55), life=2,
                       col=GOLD_WHITE),
            card('glow', '~ ~0.05 ~', '~ 90', s0=0.6, s1=2.2, life=3, fade=1, col=GOLD_WHITE)]


@preset('wave_burst', '「인력 충격파」 burst: the white-gold flare dome (4 b wide, 2 b tall), then the filled fire disc r '
        '1.8 (5 t) where the ring starts. At the floor point.')
def _p_wave_burst():
    return [card('flare_dome', '~ ~ ~', bb='vertical', s0=1.0, s1=4.3, life=6, fade=2, dur=3),
            card('fire_disc', '~ ~0.05 ~', '~ 0', spin=40, s0=1.0, s1=1.8, life=9, fade=3, dur=3),
            card('glow', '~ ~0.06 ~', '~ 90', s0=1.0, s1=3.2, life=4, fade=2, col=GOLD_WHITE),
            card('spark', '~ ~1 ~', bb='center', spin=45, s0=0.6, s1=2.6, life=4, fade=2),
            flash(GOLD_PALE, '~ ~1 ~', 0.9), part('flame', '~ ~0.3 ~', (1.0, 0.2, 1.0), 0.05, 14),
            part('lava', '~ ~0.2 ~', (0.8, 0.1, 0.8), 0, 4)]


@preset('wave_band', '「인력 충격파」 the expanding gold-fire ring: 16 band segments (flat burning strip + standing flame '
        'wall) travel from radius {r0} to {r1} in {dur} ticks keeping the band {w} deep (tenths of a block / ticks, '
        'like the hazards). Call it on the tick BEFORE the strike: it then starts moving in the strike tick, with the '
        'tele/wave front and the hz/ring front. At the floor centre.', ('r0', 'r1', 'w', 'dur'))
def _p_wave_band():
    k = 2 * math.sin(math.radians(360 / 32)) * 1.18          # chord of a 22.5-degree segment, 18 % overlap
    return ['$scoreboard players set #fkWr0 mb $(r0)', '$scoreboard players set #fkWr1 mb $(r1)',
            '$scoreboard players set #fkWw mb $(w)', '$scoreboard players set #fkWt mb $(dur)',
            'execute if score #fkWr0 mb matches ..4 run scoreboard players set #fkWr0 mb 5',
            'execute if score #fkWr1 mb <= #fkWr0 mb run scoreboard players operation #fkWr1 mb = #fkWr0 mb',
            'execute if score #fkWw mb matches ..1 run scoreboard players set #fkWw mb 2',
            'execute if score #fkWt mb matches ..0 run scoreboard players set #fkWt mb 1',
            f'execute store result storage {STO} w.r0 float 0.1 run scoreboard players get #fkWr0 mb',
            f'execute store result storage {STO} w.r1 float 0.1 run scoreboard players get #fkWr1 mb',
            f'execute store result storage {STO} w.w float 0.1 run scoreboard players get #fkWw mb',
            f'execute store result storage {STO} w.c0 float {num(k / 10, 6)} run scoreboard players get #fkWr0 mb',
            f'execute store result storage {STO} w.c1 float {num(k / 10, 6)} run scoreboard players get #fkWr1 mb',
            f'execute store result storage {STO} w.d int 1 run scoreboard players get #fkWt mb',
            'scoreboard players operation #fkWl mb = #fkWt mb', 'scoreboard players add #fkWl mb 4',
            f'execute store result storage {STO} w.l int 1 run scoreboard players get #fkWl mb',
            f'function {FN}p/e/wave_band with storage {STO} w']


def _p_e_wave_band():
    return ['$' + card('wave_band', '~ ~0.04 ~', f'~{ang(yaw)} 0', s0=('$(c0)', 1.6, '$(w)'), s1=('$(c1)', 1.6, '$(w)'),
                       off=(0, 0, '$(r0)'), move=(0, 0, '$(r1)'), life='$(l)', fade=4, dur='$(d)')
            for yaw in radial(16, 0)]


@preset('wave_fire', '「인력 충격파」 flames and embers on the travelling front at radius {r} blocks (particles only; call '
        'every 3 t with the front radius). At the floor centre.', ('r',))
def _p_wave_fire():
    out = []
    for yaw in radial(12, 7.5):
        out.append(f'$execute rotated ~{ang(yaw)} 0 run particle minecraft:flame ^ ^0.3 ^$(r) 0.5 0.15 0.5 0.01 2 '
                   f'force @a[tag=player]')
    for yaw in radial(6, 30):
        out.append(f'$execute rotated ~{ang(yaw)} 0 run particle minecraft:dust{{color:{colour_list(ORANGE)},scale:1.6}} '
                   f'^ ^0.4 ^$(r) 0.6 0.2 0.6 0 2 force @a[tag=player]')
    return out


# --- field: 감소 영역 eruptions
@preset('erupt_tell', 'F1 감소 영역: dark dust settling over a zone as its dark disc appears (the disc itself is the '
        'telegraph decal tele/dark r 2.8, 15 t lead). At the zone floor point.')
def _p_erupt_tell():
    # telegraph rule 10-20: the dark disc (the footage's marker) moved to tele/dark (a decal card, at the zone's true radius:
    # the erupt_disc sprite is 1 b across at scale 1, so the old s1 2.8 drew r 1.4); the violet tele_disc is gone
    return [dust(rgb('#3A2C24'), 1.2, '~ ~0.2 ~', (1.2, 0.05, 1.2), 6)]


@preset('erupt', 'F1 eruption r 2.8: the gold burst mound with floor chunks, a crack ring, flung rocks and dust. At the '
        'zone floor point.')
def _p_erupt():
    rnd = random.Random(2828)
    out = [card('erupt_burst', '~ ~ ~', bb='vertical', s0=0.6, s1=3.4, life=8, fade=3, dur=3),
           card('erupt_burst', '~0.5 ~ ~0.3', bb='vertical', roll=10, s0=0.5, s1=2.4, life=7, fade=3, dur=3, dly=1),
           card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=3.4, life=6, fade=3, col=rgb('#FCEBBC')),
           card('crack_ring', '~ ~0.035 ~', '~ 0', spin=20, s0=2.4, s1=2.8, life=20, fade=8, dur=3)]
    for yaw in radial(4, 15):
        el = rnd.uniform(50, 80)
        out.append(card('chunk', '~ ~0.5 ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(0, 90), s0=0.3,
                        s1=rnd.uniform(0.45, 0.7), move=(0, rnd.uniform(2.4, 3.8), 0), life=12, fade=5))
    out += [card('dust', '~ ~0.6 ~', bb='center', s0=0.8, s1=2.4, move=(0, 0.5, 0), life=14, fade=7, dly=1),
            part('explosion', '~ ~0.4 ~', (0.4, 0.1, 0.4), 0, 1), dust(rgb('#E3C794'), 2.2, '~ ~0.8 ~', (1.4, 0.6, 1.4), 16),
            blockp('smooth_sandstone', '~ ~0.4 ~', (1.2, 0.3, 1.2), 0.25, 16)]
    return out


@preset('debris', 'After an eruption: a few chunks hover 0.3-2.5 b over the zone, then drift down. At the zone floor '
        'point.')
def _p_debris():
    rnd = random.Random(1630)
    out = []
    for k in range(5):
        x, z = rnd.uniform(-1.8, 1.8), rnd.uniform(-1.8, 1.8)
        out.append(card('chunk', p3(x, rnd.uniform(0.6, 2.4), z, '~'), bb='center', roll=rnd.randint(0, 90),
                        spin=rnd.choice((-1, 1)) * 60, s0=rnd.uniform(0.3, 0.5), s1=rnd.uniform(0.3, 0.5),
                        move=(0, -rnd.uniform(0.4, 1.0), 0), life=rnd.randint(24, 32), fade=8))
    return out


# --- meter and break
@preset('meter_glint', 'Break meter: the crack glint on the bubble at each count. At the core.')
def _p_meter_glint():
    return [card('crack_glint', bb='center', spin=30, s0=0.3, s1=1.0, life=6, fade=3),
            card('glint', bb='center', spin=60, s0=0.2, s1=0.7, life=4, fade=2, col=WHITE),
            part('wax_off', '~ ~ ~', (0.3, 0.3, 0.3), 0, 3)]


@preset('bubble_crack', 'Break meter stage (counts 5, 10, 15): a big crack flash, glass flakes and a glow. At the core.')
def _p_bubble_crack():
    rnd = random.Random(51015)
    out = [card('crack_glint', bb='center', spin=40, s0=0.6, s1=1.8, life=8, fade=3),
           card('glow', bb='center', s0=1.0, s1=2.8, life=4, fade=2, col=rgb('#FFFAF9'))]
    for yaw in radial(3, 40):
        el = rnd.uniform(-20, 40)
        out.append(card('glass_shard', '~ ~ ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(-20, 20), s0=0.3,
                        s1=0.5, move=(0, rnd.uniform(1.0, 1.6), 0), life=8, fade=3))
    out.append(part('end_rod', '~ ~ ~', (0.4, 0.4, 0.4), 0.08, 6))
    return out


@preset('bubble_glow', 'Break +0..+5: the cracked bubble lights up white-gold before it bursts. At the core.')
def _p_bubble_glow():
    return [card('bubble3', bb='center', s0=2.2, s1=2.9, life=6, fade=1),
            card('glow', bb='center', s0=2.0, s1=4.2, life=6, fade=1, col=rgb('#FFFAF9'))]


@preset('break_burst', 'Break +5: the bubble bursts: a white flash, flying glass shards, a big crack glint and a thin '
        'ring. At the core.')
def _p_break_burst():
    rnd = random.Random(55)
    out = [card('glow', bb='center', s0=2.0, s1=7.5, life=4, fade=2, col=WHITE),
           card('crack_glint', bb='center', spin=60, s0=1.0, s1=3.6, life=5, fade=2),
           card('ripple', bb='center', spin=60, s0=1.5, s1=6.5, life=6, fade=2, col=rgb('#FFFAF9'))]
    for yaw in radial(12, 7):
        el = rnd.uniform(-35, 55)
        out.append(card('glass_shard', '~ ~ ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(-25, 25), s0=0.6,
                        s1=rnd.uniform(0.7, 1.1), move=(0, rnd.uniform(2.4, 4.0), 0), life=10, fade=4))
    out += [part('end_rod', '~ ~ ~', (0.6, 0.6, 0.6), 0.25, 20), part('wax_off', '~ ~ ~', (1.2, 1.2, 1.2), 0, 10),
            flash(rgb('#FFFAF9'), '~ ~ ~', 1.0)]
    return out


@preset('break_ring', 'Break +5: the horizontal gold spark ring expands at floor level (r 9 in 9 t). At the floor point '
        'under the core.')
def _p_break_ring():
    return [card('ripple', '~ ~0.07 ~', '~ 90', spin=50, s0=1.0, s1=9.0, life=11, fade=3, dur=9, col=CRACK_GOLD),
            card('crack_ring', '~ ~0.04 ~', '~ 0', s0=1.5, s1=2.4, life=16, fade=6, dur=4),
            part('electric_spark', '~ ~0.3 ~', (2.0, 0.1, 2.0), 0.2, 16)]


@preset('groggy_sparks', 'Groggy (every 30-40 t): slow sparks drip from the slumped core with a wisp of smoke. At the '
        'core.')
def _p_groggy_sparks():
    return [card('spark', '~0.3 ~ ~', bb='center', s0=0.3, s1=0.5, move=(0, -0.7, 0), life=12, fade=5),
            card('spark', '~-0.4 ~-0.2 ~0.2', bb='center', s0=0.25, s1=0.4, move=(0, -0.8, 0), life=12, fade=5, dly=5),
            part('smoke', '~ ~0.3 ~', (0.3, 0.2, 0.3), 0.01, 3)]


@preset('sink_dust', 'Break +34: the device sinks low (dust ring under it). At the floor point under it.')
def _p_sink_dust():
    out = [card('ripple', '~ ~0.05 ~', '~ 90', spin=30, s0=1.0, s1=5.0, life=10, fade=4, col=DUST_PALE)]
    for yaw in radial(4, 45):
        x, z = ring_xz(2.4, yaw)
        out.append(card('dust', p3(x, 0.4, z, '~'), bb='center', s0=0.6, s1=1.8, move=(0, 0.3, 0), life=14, fade=7))
    out.append(dust(DUST, 1.8, '~ ~0.2 ~', (2.0, 0.05, 2.0), 12))
    return out


@preset('recover', 'Groggy end: re-level and the core flips to the top (a gold ring flash and sparks). At the core.')
def _p_recover():
    return [card('glow', bb='center', s0=1.0, s1=3.2, life=6, fade=3, col=GOLD),
            card('ripple', bb='center', spin=60, s0=1.0, s1=4.2, life=7, fade=3, col=GOLD),
            card('spark', '~0.6 ~0.3 ~', bb='center', spin=45, s0=0.3, s1=1.3, life=5, fade=2),
            card('spark', '~-0.6 ~-0.2 ~', bb='center', spin=-45, s0=0.3, s1=1.2, life=5, fade=2, dly=2),
            part('wax_on', '~ ~ ~', (0.6, 0.6, 0.6), 0, 8)]


@preset('lift_off', 'Field end (unbroken) +23: the lift-off pulse under the device (white-gold burst, r 3 ring, dust). '
        'At the floor point under it.')
def _p_lift_off():
    return [card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=5.0, life=4, fade=2, col=GOLD_WHITE),
            card('ripple', '~ ~0.07 ~', '~ 90', spin=40, s0=1.0, s1=6.0, life=7, fade=3, col=GOLD),
            card('dust', '~1 ~0.4 ~', bb='center', s0=0.5, s1=1.6, move=(0, 0.4, 0), life=12, fade=6),
            card('dust', '~-1 ~0.4 ~0.5', bb='center', s0=0.5, s1=1.5, move=(0, 0.4, 0), life=12, fade=6, dly=1),
            card('glow', '~ ~1.2 ~', bb='center', s0=1.0, s1=3.5, life=3, fade=1, col=WHITE)]


@preset('pack_up', 'Field end: sparks as the lances dock and the device packs into the compact form. At the ring '
        'centre, rotated as the device.')
def _p_pack_up():
    return [card('spark', '^3.4 ^ ^', bb='center', spin=60, s0=0.3, s1=1.3, life=5, fade=2),
            card('spark', '^-3.4 ^ ^', bb='center', spin=-60, s0=0.3, s1=1.3, life=5, fade=2, dly=2),
            card('glint', '^ ^0.5 ^', bb='center', spin=90, s0=0.2, s1=0.9, life=5, fade=2, col=GOLD_PALE, dly=4),
            part('crit', '~ ~ ~', (2.5, 0.3, 2.5), 0.2, 10)]


# --- death
@preset('death_flicker', 'Death: one flicker of the dying seam (call 3 times, 4-6 t apart). At the core.')
def _p_death_flicker():
    return [card('glow', bb='center', s0=1.5, s1=2.6, life=3, fade=1, col=GOLD),
            card('spark', bb='center', spin=45, s0=0.4, s1=1.2, life=3, fade=1),
            part('electric_spark', '~ ~ ~', (0.6, 0.3, 0.6), 0.2, 6)]


@preset('death_fall', 'Death: the ring lands tilted on the floor (dust ring, chunks). At the floor point under it.')
def _p_death_fall():
    rnd = random.Random(40)
    out = [card('ripple', '~ ~0.05 ~', '~ 90', spin=30, s0=1.0, s1=6.0, life=12, fade=5, col=DUST_PALE)]
    for yaw in radial(5, 10):
        x, z = ring_xz(rnd.uniform(1.8, 3.2), yaw)
        out.append(card('dust', p3(x, 0.4, z, '~'), bb='center', s0=0.6, s1=2.0, move=(0, 0.4, 0), life=16, fade=8,
                        dly=rnd.randint(0, 2)))
    for yaw in radial(3, 50):
        el = rnd.uniform(40, 70)
        out.append(card('chunk', '~ ~0.4 ~', f'~{ang(yaw)} {ang(90 - el)}', roll=rnd.randint(0, 90), s0=0.3, s1=0.45,
                        move=(0, rnd.uniform(1.2, 2.0), 0), life=10, fade=4))
    out += [dust(DUST, 2.2, '~ ~0.3 ~', (2.5, 0.1, 2.5), 16), blockp('smooth_sandstone', '~ ~0.3 ~', (2, 0.2, 2), 0.2, 16)]
    return out


@preset('death_fade', 'Death tail (every 10-15 t while it scales out): gold motes and sparks rise. Around the core.')
def _p_death_fade():
    rnd = random.Random(110)
    out = []
    for k in range(6):
        x, y, z = rnd.uniform(-1.2, 1.2), rnd.uniform(-1.0, 0.6), rnd.uniform(-1.2, 1.2)
        out.append(card('mote', p3(x, y, z, '~'), bb='center', s0=0.14, s1=0.24, move=(0, rnd.uniform(1.6, 2.6), 0),
                        life=rnd.randint(16, 22), fade=6, col=GOLD_PALE if k % 2 else BRASS, dly=rnd.randint(0, 6)))
    for k in range(2):
        out.append(card('spark', p3(rnd.uniform(-0.8, 0.8), rnd.uniform(-0.5, 0.5), rnd.uniform(-0.8, 0.8), '~'),
                        bb='center', spin=60, s0=0.3, s1=0.8, move=(0, 1.2, 0), life=12, fade=5, dly=rnd.randint(0, 6)))
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
                if p.is_dir() and not any(p.iterdir()):
                    p.rmdir()
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


HEADER = '# Generated by tools/build_mboss_fg_fx.py (field generator fx kit) - edit the generator, not this file.\n'
E = FN + 'e/'
SEL = f'@e[type=minecraft:item_display,tag={TAG}'
DEF_A = 'tg:"rlk_fk_c",tpd:0'          # storage a defaults: an extra tag, teleport_duration


def engine(W):
    W.w('card', [
        '# Spawn one painted card at pos, rotated rot (fixed cards), seen from the executing context.',
        '# {kind, pos:"^x ^y ^z", rot:"~ ~", bb:fixed|center|vertical|horizontal, roll:<deg, about local z>,',
        '#  spin:<deg over the main interpolation, -170..170, about the card normal (y for flat / cross / band / box)>,',
        '#  s0:<start size>, s1:<end size>, move:"dx,dy,dz" (end offset, display frame: +x left, +y up, +z forward),',
        '#  life:<ticks>, fade:<shrink-out ticks>, col:<RGB int tint, 16777215 = the painted colours>}. fg_fx_api.md.',
        f'# Skipped (no error) while {CAP} fx cards are alive.',
        f'execute if score #fkN mb matches {CAP}.. run return 0',
        f'$data modify storage {STO} a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)f,$(s0)f,$(s0)f",s1:"$(s1)f,$(s1)f,$(s1)f",off:"0f,0f,0f",move:"$(move)",col:$(col),col2:-1,'
        f'ax:"0f,0f,1f",{DEF_A}}}',
        f'execute unless data storage {STO} ax.bomb run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #fkRoll mb $(roll)',
        '$scoreboard players set #fkSpin mb $(spin)',
        '$scoreboard players set #fkLife mb $(life)',
        '$scoreboard players set #fkFade mb $(fade)',
        'scoreboard players set #fkDly mb 0',
        'scoreboard players set #fkDur mb 0',
        'scoreboard players set #fkHit mb -1',
        'scoreboard players set #fkTel mb 0',
        f'function {E}make',
    ])
    W.w('cardx', [
        '# card with every option: s0 / s1 as "xf,yf,zf" vectors, off:"xf,yf,zf" (static start translation), move',
        '# (the END translation), dly:<ticks hidden before it shows>, dur:<ticks of the main interpolation, 0 = up to',
        '# the fade>, hit:<ticks after the call when the tint becomes col2, -1 = never>, col2:<RGB int>. Same cap.',
        f'execute if score #fkN mb matches {CAP}.. run return 0',
        f'$data modify storage {STO} a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)",s1:"$(s1)",off:"$(off)",move:"$(move)",col:$(col),col2:$(col2),ax:"0f,0f,1f",' + DEF_A + '}',
        f'execute unless data storage {STO} ax.bomb run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #fkRoll mb $(roll)',
        '$scoreboard players set #fkSpin mb $(spin)',
        '$scoreboard players set #fkLife mb $(life)',
        '$scoreboard players set #fkFade mb $(fade)',
        '$scoreboard players set #fkDly mb $(dly)',
        '$scoreboard players set #fkDur mb $(dur)',
        '$scoreboard players set #fkHit mb $(hit)',
        'scoreboard players set #fkTel mb 0',
        f'function {E}make',
    ])
    W.w('e/make', [
        f'# Internal: storage {STO} a (kind pos rot bb s0 s1 off move col col2 ax tg tpd) + #fkRoll #fkSpin #fkLife',
        '# #fkFade #fkDly #fkDur #fkHit #fkTel -> one card. The stage clock is gametime + 1: the ager (fx/e/world, a',
        '# 1t schedule) runs at the END of this server tick with gametime already + 1, so counting from it starts the',
        '# main interpolation in the next server tick and the client animates it (the butterfly kit\'s perf-2 fix).',
        '# Stages: shows at clock + dly, interpolates from clock + dly + 1 over dur ticks, recolours at clock + hit,',
        '# shrinks over the last fade ticks, removed at clock + dly + life.',
        f'execute unless score #fkInit mb matches 1 run function {E}init',
        'execute if score #fkTel mb matches 1 run scoreboard players add #fkTN mb 1',
        'execute unless score #fkTel mb matches 1 run scoreboard players add #fkN mb 1',
        'execute if score #fkLife mb matches ..1 run scoreboard players set #fkLife mb 2',
        'execute if score #fkFade mb matches ..-1 run scoreboard players set #fkFade mb 0',
        'execute if score #fkDly mb matches ..-1 run scoreboard players set #fkDly mb 0',
        'scoreboard players operation #fkWd mb = #fkLife mb',
        'scoreboard players remove #fkWd mb 2',
        'scoreboard players operation #fkFade mb < #fkWd mb',
        'scoreboard players operation #fkWd mb = #fkLife mb',
        'scoreboard players operation #fkWd mb -= #fkFade mb',
        'scoreboard players remove #fkWd mb 1',
        'execute if score #fkDur mb matches 1.. run scoreboard players operation #fkWd mb = #fkDur mb',
        'execute if score #fkWd mb matches ..0 run scoreboard players set #fkWd mb 1',
        'execute if score #fkSpin mb matches 171.. run scoreboard players set #fkSpin mb 170',
        'execute if score #fkSpin mb matches ..-171 run scoreboard players set #fkSpin mb -170',
        f'execute store result storage {STO} a.rr float 0.017453292 run scoreboard players get #fkRoll mb',
        f'execute store result storage {STO} a.sr float 0.017453292 run scoreboard players get #fkSpin mb',
        f'execute store result storage {STO} a.d int 1 run scoreboard players get #fkWd mb',
        f'execute store result storage {STO} a.f int 1 run scoreboard players get #fkFade mb',
        f'execute store result score #fkC2 mb run data get storage {STO} a.col2',
        f'data modify storage {STO} a.z set from storage {STO} a.s0',
        f'execute if score #fkDly mb matches 1.. run data modify storage {STO} a.z set value "0f,0f,0f"',
        f'function {E}spawn with storage {STO} a',
        f'execute if score #fkTel mb matches 1 run tag {SEL}_new] add {TAG}_t',
        'execute store result score #fkNow mb run time query gametime',
        'scoreboard players add #fkNow mb 1',
        f'execute as {SEL}_new,limit=1] run function {E}born',
        f'tag {SEL}_new] remove {TAG}_new',
        f'schedule function {E}world 1t replace',
    ])
    end_tr = ('translation:[$(move)],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(s1)],'
              'right_rotation:{angle:$(sr)f,axis:[$(ax)]}')
    W.w('e/spawn', [
        f'# Internal (macro, storage {STO} a): the item_display; the stage snapshots ride on its item.',
        f'$summon minecraft:item_display $(pos) {{Tags:["{TAG}","{TAG}_new","rlk_room","rlk_mb_aux","$(tg)"],'
        'billboard:"$(bb)",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
        'teleport_duration:$(tpd),interpolation_duration:0,transformation:{translation:[$(off)],'
        'left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(z)],right_rotation:[0f,0f,0f,1f]},'
        f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{NS_TEX}$(kind)",'
        '"minecraft:custom_model_data":{colors:[$(col)]},"minecraft:custom_data":{'
        'fkS:{start_interpolation:0,interpolation_duration:0,transformation:{scale:[$(s0)]}},'
        'fkG:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'fkF:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}},'
        'fkC:$(col2)}}}}',
        f'$execute positioned $(pos) rotated $(rot) run tp {SEL}_new,limit=1] ~ ~ ~ ~ ~',
    ])
    W.w('e/born', [
        '# Internal, as the new card: stage clock values (gametime + 1 based) in fkS fkG fkH fkK fkD.',
        'scoreboard players operation @s fkS = #fkNow mb',
        'scoreboard players operation @s fkS += #fkDly mb',
        'scoreboard players operation @s fkG = @s fkS',
        'scoreboard players add @s fkG 1',
        'scoreboard players operation @s fkD = @s fkS',
        'scoreboard players operation @s fkD += #fkLife mb',
        'scoreboard players operation @s fkK = @s fkD',
        'scoreboard players operation @s fkK -= #fkFade mb',
        'scoreboard players operation @s fkH = #fkNow mb',
        'scoreboard players operation @s fkH += #fkHit mb',
        f'tag @s add {TAG}_go',
        f'execute if score #fkDly mb matches 1.. run tag @s add {TAG}_sh',
        f'execute if score #fkFade mb matches 1.. run tag @s add {TAG}_fd',
        f'execute if score #fkHit mb matches 0.. if score #fkC2 mb matches 0.. run tag @s add {TAG}_hit',
    ])
    W.w('e/world', [
        '# Ages the kit\'s cards once per tick while any is alive (scheduled from e/make and from itself, so it runs at',
        '# the end of the server tick; no hook in rlk:tick). A dead or reviving player clears them.',
        f'execute unless entity {SEL},limit=1] run return run function {E}zero',
        f'execute if entity @a[tag=player,scores={{dead=1}}] run return run function {FN}clear',
        f'execute if entity @a[tag=player,scores={{rnDie=1..}}] run return run function {FN}clear',
        'execute store result score #fkNow mb run time query gametime',
        f'execute as {SEL}] run function {E}age',
        f'execute store result score #fkN mb if entity {SEL},tag=!{TAG}_t]',
        f'execute store result score #fkTN mb if entity {SEL}_t]',
        f'execute if entity {SEL},limit=1] run schedule function {E}world 1t replace',
    ])
    W.w('e/zero', ['scoreboard players set #fkN mb 0', 'scoreboard players set #fkTN mb 0'])
    W.w('e/age', [
        '# As one card (the stage clock in #fkNow).',
        'execute unless score @s fkD = @s fkD run return run kill @s',
        'execute if score #fkNow mb >= @s fkD run return run kill @s',
        f'execute if entity @s[tag={TAG}_sh] if score #fkNow mb >= @s fkS run function {E}show',
        f'execute if entity @s[tag={TAG}_go] if score #fkNow mb >= @s fkG run function {E}go',
        f'execute if entity @s[tag={TAG}_hit] if score #fkNow mb >= @s fkH run function {E}hit',
        f'execute if entity @s[tag={TAG}_fd] if score #fkNow mb >= @s fkK run function {E}fade',
    ])
    W.w('e/show', ['# a delayed card appears at its start size',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".fkS',
                   f'tag @s remove {TAG}_sh'])
    W.w('e/go', ['# start -> end transformation over dur ticks (client interpolation)',
                 'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".fkG',
                 f'tag @s remove {TAG}_go'])
    W.w('e/hit', ['# the tint changes (telegraph flash on the hit tick)',
                  'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set from entity @s '
                  'item.components."minecraft:custom_data".fkC',
                  f'tag @s remove {TAG}_hit'])
    W.w('e/fade', ['# shrink to nothing over the last fade ticks',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".fkF',
                   f'tag @s remove {TAG}_fd'])
    W.w('e/init', ['# Objectives of the kit (created on the first card; removed by fx/uninstall).',
                   *[f'scoreboard objectives add {o} dummy' for o in OBJECTIVES],
                   'scoreboard players set #fkInit mb 1',
                   'scoreboard players set #fkN mb 0', 'scoreboard players set #fkTN mb 0'])
    W.w('clear', ['# Remove every card of the kit (fx and telegraphs). Safe to call any time.',
                  f'kill {SEL}]', f'function {E}zero'])
    fake = ('#fkInit', '#fkN', '#fkTN', '#fkNow', '#fkWd', '#fkC2', '#fkRoll', '#fkSpin', '#fkLife', '#fkFade',
            '#fkDly', '#fkDur', '#fkHit', '#fkTel', '#fkTr', '#fkTr0', '#fkTa', '#fkTl', '#fkTw', '#fkTb', '#fkTd',
            '#fkTell', '#fkTEl', '#fkThold', '#fkWr0', '#fkWr1', '#fkWw', '#fkWl', '#fkWt', '#fkM', '#fkMF', '#fkHudV',
            '#fkDemo', '#fkDT', '#fkMT', '#fkMinus1')
    W.w('uninstall', ['# Remove the kit\'s cards, objectives, storage, schedules and the stub rig (call from the module\'s',
                      '# uninstall hook).',
                      f'kill {SEL}]', 'kill @e[type=minecraft:marker,tag=rlk_fk_demo]',
                      *[f'scoreboard objectives remove {o}' for o in OBJECTIVES],
                      *[f'scoreboard players reset {s} mb' for s in fake],
                      f'data remove storage {STO} a', f'data remove storage {STO} t', f'data remove storage {STO} w',
                      f'data remove storage {STO} hud', f'data remove storage {STO} ax', f'data remove storage {STO} fl',
                      f'schedule clear {E}world', f'schedule clear {FN}hud/e/unflash', f'schedule clear {FN}test/e/tick',
                      f'schedule clear {FN}test/e/mturn']
                + ([f'function {STUB_RIG}uninstall'] if rig_mode() == 'stub' else []))
    spin_y = ','.join(f'{k}:"0f,1f,0f"' for k, v in KINDS.items() if v[0] in SPIN_Y)
    W.w('e/axes', ['# Spin axis (= the card normal / long axis) of the flat, cross, band and box kinds; face kinds keep z.',
                   f'data modify storage {STO} ax set value {{{spin_y}}}',
                   f'data modify storage {STO} ax.bomb set value "0f,0f,1f"'])
    W.w('look', [
        '# Dress @s (an item_display prop, e.g. a projectile) as a kit sprite: {kind, col:<RGB int>}. Full bright;',
        '# the caller keeps its own transformation / billboard (see fg_fx_api.md for the prop recipes).',
        '$data merge entity @s {item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        f'"{NS_TEX}$(kind)","minecraft:custom_model_data":{{colors:[$(col)]}}}}}},brightness:{{sky:15,block:15}}}}',
    ])


def telegraphs(W):
    T = FN + 'tele/e/'
    cols = []
    for el, (c1, c2, c3) in sorted(TELE_COL.items()):
        cols.append(f'execute if score #fkTEl mb matches {el} run data modify storage {STO} t merge value '
                    f'{{c1:{c1},c2:{c2},c3:{c3}}}')
    d1, d2, d3 = TELE_COL[TELE_DEFAULT]
    W.w('tele/e/prep', [
        '# Internal: common telegraph setup from #fkTell #fkTEl #fkThold (colours by el: 5 Geo amber, 9 the field\'s',
        '# violet, 0 physical; anything else draws Geo). Life = tell + hold + 1, the fill grows over tell - 1 ticks from',
        '# the tick after the call, so its edge reaches the rim on call + tell (the framework hz strike tick when',
        '# both are made in the same tick with the same tell); every card flashes (col2) on that tick.',
        'execute if score #fkTell mb matches ..1 run scoreboard players set #fkTell mb 2',
        'execute if score #fkThold mb matches ..-1 run scoreboard players set #fkThold mb 0',
        f'data modify storage {STO} t merge value {{c1:{d1},c2:{d2},c3:{d3},tg:"rlk_fk_c",tpd:0}}',
        *cols,
        'scoreboard players operation #fkLife mb = #fkTell mb',
        'scoreboard players operation #fkLife mb += #fkThold mb',
        'scoreboard players add #fkLife mb 1',
        'scoreboard players operation #fkDur mb = #fkTell mb',
        'scoreboard players remove #fkDur mb 1',
        'scoreboard players operation #fkHit mb = #fkTell mb',
        'scoreboard players set #fkFade mb 0',
        'scoreboard players set #fkDly mb 0',
        'scoreboard players set #fkRoll mb 0',
        'scoreboard players set #fkSpin mb 0',
        'scoreboard players set #fkTel mb 1',
    ])

    def head(extra):
        return [f'execute if score #fkTN mb matches {TCAP - TSKIP}.. run return 0',
                '$scoreboard players set #fkTell mb $(tell)',
                '$scoreboard players set #fkTEl mb $(el)',
                '$scoreboard players set #fkThold mb $(hold)',
                *extra,
                f'function {T}prep']

    def mk(kind, pos, s0, s1, colkey, rot='~ 0', off='0f,0f,0f', move=None, flash=True, tg='$(tg)'):
        """one telegraph card inside a macro reading storage t (static cards have s0 = s1)"""
        mv = move if move is not None else off
        c2 = '$(c3)' if flash else '-1'
        return [f'$data modify storage {STO} a set value {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"fixed",'
                f's0:"{s0}",s1:"{s1}",off:"{off}",move:"{mv}",col:$({colkey}),col2:{c2},ax:"0f,1f,0f",'
                f'tg:"{tg}",tpd:$(tpd)}}',
                f'function {E}make']

    # disc
    W.w('tele/disc', [
        '# Disc telegraph decal: {r:<radius, tenths of a block>, tell:<ticks to the hit>, el:<palette>, hold:<ticks',
        '# it stays after the hit>}. Positioned on the floor point. Visual only: pair it with hz/disc (same tell,',
        f'# #hzQuiet 1 to drop the framework particles). 2 cards; skipped while {TCAP - TSKIP}+ telegraph cards live.',
        *head(['$scoreboard players set #fkTr mb $(r)']),
        'execute if score #fkTr mb matches ..1 run scoreboard players set #fkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #fkTr mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #fkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc with storage {STO} t',
    ])
    W.w('tele/e/disc', [
        '# Internal (macro, storage t): the progress fill (0 -> r) under the static rim.',
        *mk('t_fill', '~ ~0.03 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', 'c2'),
        *mk('$(rim)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1'),
    ])
    # rim only (telegraph rule 10-20: 지면 충격 C5 keeps the footage's thin pale-gold rim, without the fill / progress edge)
    W.w('tele/rim', [
        '# Rim-only disc telegraph decal: {r:<radius, tenths>, tell, el, hold}. tele/disc without its progress fill: the',
        '# static rim (thick under r 2.5), flashing on the strike tick (call + tell), gone hold ticks later. Positioned on',
        '# the floor point. Palette 6 = the pale-gold rim of 지면 충격 (C5). 1 card.',
        *head(['$scoreboard players set #fkTr mb $(r)']),
        'execute if score #fkTr mb matches ..1 run scoreboard players set #fkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #fkTr mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #fkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}rim with storage {STO} t',
    ])
    W.w('tele/e/rim', [
        '# Internal (macro, storage t): the static rim.',
        *mk('$(rim)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1'),
    ])
    # the dark floor disc (the footage's own marker of 감소 영역 F1 and 지면 충격 C5) as a decal card: cleared on a pause with
    # the other decals and redrawn by the pattern with the ticks left; the erupt_disc sprite is 1 b across at scale 1
    W.w('tele/dark', [
        '# The dark floor disc decal (erupt_disc: the floor about 35 % darker, an amber rim, gold cracks): {r0, r (radii,',
        '# tenths), grow (ticks), tell, hold}. Positioned on the floor point. Its radius grows r0 -> r over grow ticks from',
        '# the tick after the call; it stays to the strike (call + tell) + hold. Painted colours, no flash. A telegraph',
        f'# card (counted in the {TCAP} cap, removed by tele/clear). 1 card.',
        f'execute if score #fkTN mb matches {TCAP - TSKIP}.. run return 0',
        '$scoreboard players set #fkTell mb $(tell)',
        'scoreboard players set #fkTEl mb 5',
        '$scoreboard players set #fkThold mb $(hold)',
        '$scoreboard players set #fkTr0 mb $(r0)',
        '$scoreboard players set #fkTr mb $(r)',
        '$scoreboard players set #fkTd mb $(grow)',
        f'function {T}prep',
        'execute if score #fkTr mb matches ..1 run scoreboard players set #fkTr mb 2',
        'execute if score #fkTr0 mb matches ..0 run scoreboard players set #fkTr0 mb 1',
        'execute if score #fkTr0 mb > #fkTr mb run scoreboard players operation #fkTr0 mb = #fkTr mb',
        '# the card scale is the diameter (2 r)',
        f'execute store result storage {STO} t.d float 0.2 run scoreboard players get #fkTr mb',
        f'execute store result storage {STO} t.d0 float 0.2 run scoreboard players get #fkTr0 mb',
        'execute if score #fkTd mb matches ..0 run scoreboard players set #fkTd mb 1',
        'scoreboard players operation #fkDur mb = #fkTd mb',
        f'data modify storage {STO} t.cw set value {WHITE}',
        f'function {T}dark with storage {STO} t',
    ])
    W.w('tele/e/dark', [
        '# Internal (macro, storage t): the dark disc, diameter d0 -> d over #fkDur ticks.',
        *mk('erupt_disc', '~ ~0.025 ~', '$(d0)f,1f,$(d0)f', '$(d)f,1f,$(d)f', 'cw', flash=False),
    ])
    # ring
    W.w('tele/ring', [
        '# Ring telegraph decal (safe hole inside r0): {r0, r (tenths), tell, el, hold}. Positioned on the floor',
        '# point. Outer and inner rims, and a progress ring that travels from r0 to r. 3 cards.',
        *head(['$scoreboard players set #fkTr mb $(r)', '$scoreboard players set #fkTr0 mb $(r0)']),
        'execute if score #fkTr0 mb matches ..1 run scoreboard players set #fkTr0 mb 2',
        'execute if score #fkTr mb <= #fkTr0 mb run scoreboard players operation #fkTr mb = #fkTr0 mb',
        'execute if score #fkTr mb = #fkTr0 mb run scoreboard players add #fkTr mb 5',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #fkTr mb',
        f'execute store result storage {STO} t.r0 float 0.1 run scoreboard players get #fkTr0 mb',
        f'function {T}ring with storage {STO} t',
    ])
    W.w('tele/e/ring', [
        *mk('t_rim', '~ ~0.035 ~', '$(r0)f,1f,$(r0)f', '$(r)f,1f,$(r)f', 'c2'),
        *mk('t_rim', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1'),
        *mk('t_rim', '~ ~0.046 ~', '$(r0)f,1f,$(r0)f', '$(r0)f,1f,$(r0)f', 'c1'),
    ])
    # sector
    sel = []
    for lo, hi, h in ((0, 37, 30), (38, 52, 45), (53, 75, 60), (76, 135, 90)):
        sel.append(f'execute if score #fkTa mb matches {lo}..{hi} run data modify storage {STO} t merge value '
                   f'{{sk:"t_sec{h}",sf:"t_secf{h}"}}')
    W.w('tele/sector', [
        '# Sector (arc) telegraph decal: {r (tenths), a:<half-angle deg>, tell, el, hold}. Positioned on the',
        '# apex, rotated = aim (yaw). Half-angles snap to 30 / 45 / 60 / 90 (a >= 136 draws a disc). 2 cards.',
        *head(['$scoreboard players set #fkTr mb $(r)', '$scoreboard players set #fkTa mb $(a)']),
        'execute if score #fkTa mb matches 136.. run return run function ' + T + 'sector_disc',
        'execute if score #fkTr mb matches ..1 run scoreboard players set #fkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #fkTr mb',
        *sel,
        f'execute if score #fkTa mb matches ..0 run data modify storage {STO} t merge value {{sk:"t_sec30",sf:"t_secf30"}}',
        f'function {T}sector with storage {STO} t',
    ])
    W.w('tele/e/sector_disc', [
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #fkTr mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #fkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc with storage {STO} t',
    ])
    W.w('tele/e/sector', [
        *mk('$(sf)', '~ ~0.03 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', 'c2'),
        *mk('$(sk)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1'),
    ])

    # line + moving line (shared arithmetic)
    def line_math():
        return [
            'execute if score #fkTl mb matches ..1 run scoreboard players set #fkTl mb 2',
            'execute if score #fkTw mb matches ..1 run scoreboard players set #fkTw mb 2',
            '# a negative back starts the lane beyond the pivot (hz/line with a negative #hzBack); keep 0.2 b of length',
            'scoreboard players operation #fkTd mb = #fkTl mb',
            'scoreboard players remove #fkTd mb 2',
            'scoreboard players operation #fkTd mb *= #fkMinus1 mb',
            'scoreboard players operation #fkTb mb > #fkTd mb',
            f'execute store result storage {STO} t.len float 0.1 run scoreboard players get #fkTl mb',
            f'execute store result storage {STO} t.w float 0.1 run scoreboard players get #fkTw mb',
            f'execute store result storage {STO} t.hw float 0.05 run scoreboard players get #fkTw mb',
            f'execute store result storage {STO} t.nhw float -0.05 run scoreboard players get #fkTw mb',
            f'execute store result storage {STO} t.nb float -0.1 run scoreboard players get #fkTb mb',
            'scoreboard players operation #fkTl mb += #fkTb mb',
            f'execute store result storage {STO} t.lb float 0.1 run scoreboard players get #fkTl mb',
        ]
    lhead = ['$scoreboard players set #fkTl mb $(len)', '$scoreboard players set #fkTw mb $(w)',
             '$scoreboard players set #fkTb mb $(back)', 'scoreboard players set #fkMinus1 mb -1']
    W.w('tele/line', [
        '# Line / lane telegraph decal: {len, w, back (tenths), tell, el, hold}. Positioned on the start point',
        '# (floor), rotated = aim (yaw); covers -back..len along the aim, w wide (as hz/line + #hzBack; a negative back',
        '# starts it beyond the point). Two rails, two caps and the fill growing toward the far end (its bright edge',
        '# reaches it on the hit). 5 cards.',
        *head(lhead), *line_math(),
        f'function {T}line with storage {STO} t',
    ])
    W.w('tele/e/line', [
        *mk('t_lane', '^ ^0.03 ^$(nb)', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', 'c2'),
        *mk('t_bar', '^$(hw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1'),
        *mk('t_bar', '^$(nhw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(nb)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(len)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0'),
    ])
    W.w('tele/mline', [
        '# Moving line (the C3 laser lanes): {id:<0-7>, len, w, back (tenths), tell, el, hold}. Like tele/line, but',
        '# every card sits on the pivot (the executing point, e.g. the device axis on the floor) with its offset in',
        '# its own transformation, and carries teleport_duration 1 and the tag rlk_fk_ml<id>: tele/mline_aim (run',
        '# rotated as the new aim) or tele/mline_turn {id, d} turns the whole lane about the pivot, smoothly. The fill',
        '# reaches the far end on call + tell (the beam fires); the lane then stays `hold` ticks in the flash colour',
        '# (the firing time), or until tele/mline_end {id}. 5 cards.',
        *head(lhead), *line_math(),
        f'$data modify storage {STO} t merge value {{tg:"rlk_fk_ml$(id)",tpd:1}}',
        f'function {T}mline with storage {STO} t',
    ])
    W.w('tele/e/mline', [
        *mk('t_lane', '~ ~0.03 ~', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', 'c2', off='0f,0f,$(nb)f'),
        *mk('t_bar', '~ ~0.045 ~', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1', off='$(hw)f,0f,$(nb)f'),
        *mk('t_bar', '~ ~0.045 ~', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1', off='$(nhw)f,0f,$(nb)f'),
        '# the caps are turned 90 degrees right (in their frame +x = the lane forward, +z = the lane right) and tagged',
        '# rlk_fk_ml<id>c, so mline_aim keeps that turn',
        *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0', off='$(nb)f,0f,$(nhw)f',
            tg='$(tg)c'),
        *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0', off='$(len)f,0f,$(nhw)f',
            tg='$(tg)c'),
    ])
    W.w('tele/mline_aim', [
        '# Turn moving line {id} to the executing yaw (run it rotated as the re-aimed hazard marker, after hz/aim).',
        f'$execute as {SEL}_ml$(id)] positioned as @s run tp @s ~ ~ ~ ~ 0',
        f'$execute as {SEL}_ml$(id)c] positioned as @s run tp @s ~ ~ ~ ~90 0',
    ])
    W.w('tele/mline_turn', [
        '# Turn moving line {id} by {d} degrees (positive = clockwise seen from above, like a yaw).',
        f'$execute as {SEL}_ml$(id)] at @s run tp @s ~ ~ ~ ~$(d) 0',
        f'$execute as {SEL}_ml$(id)c] at @s run tp @s ~ ~ ~ ~$(d) 0',
    ])
    W.w('tele/mline_end', [
        '# Remove moving line {id} now (the beam stops early or the pattern is cancelled).',
        f'$kill {SEL}_ml$(id)]',
        f'$kill {SEL}_ml$(id)c]',
        f'execute store result score #fkTN mb if entity {SEL}_t]',
    ])
    # the expanding wave ring
    W.w('tele/wave', [
        '# Expanding wave ring (「인력 충격파」): {r0, r1, w (tenths), tell, dur (ticks), el, hold}. At the floor centre.',
        '# Over the tell (the charge) a disc decal fills to r0, the start radius of the front, and flashes on the',
        '# strike tick; from the strike the front ring travels r0 -> r1 in dur ticks (a constant (r1 - r0) / dur b/t:',
        '# 25 -> 210 in 34 t = 0.55 b/t) with the band\'s inner edge w behind it, then stays `hold` ticks. Pair with',
        '# hz/ring {r0:0, r:<r0>, tell} + hz/resize each tick (r = r0 + spd x (T - strike), inner = r - w). The rings',
        '# start interpolating at the end of the strike tick, so the drawn front matches the hazard each tick. 4 cards.',
        *head(['$scoreboard players set #fkTr0 mb $(r0)', '$scoreboard players set #fkTr mb $(r1)',
               '$scoreboard players set #fkTw mb $(w)', '$scoreboard players set #fkTd mb $(dur)']),
        'execute if score #fkTr0 mb matches ..4 run scoreboard players set #fkTr0 mb 5',
        'execute if score #fkTr mb <= #fkTr0 mb run scoreboard players operation #fkTr mb = #fkTr0 mb',
        'execute if score #fkTr mb = #fkTr0 mb run scoreboard players add #fkTr mb 5',
        'execute if score #fkTw mb matches ..1 run scoreboard players set #fkTw mb 2',
        'execute if score #fkTd mb matches ..0 run scoreboard players set #fkTd mb 1',
        f'execute store result storage {STO} t.r0 float 0.1 run scoreboard players get #fkTr0 mb',
        f'execute store result storage {STO} t.r1 float 0.1 run scoreboard players get #fkTr mb',
        'scoreboard players operation #fkTb mb = #fkTr mb',
        'scoreboard players operation #fkTb mb -= #fkTw mb',
        f'execute store result storage {STO} t.ri1 float 0.1 run scoreboard players get #fkTb mb',
        'scoreboard players operation #fkTb mb = #fkTr0 mb',
        'scoreboard players operation #fkTb mb -= #fkTw mb',
        'execute if score #fkTb mb matches ..0 run scoreboard players set #fkTb mb 1',
        f'execute store result storage {STO} t.ri0 float 0.1 run scoreboard players get #fkTb mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #fkTr0 mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}wave with storage {STO} t',
    ])
    W.w('tele/e/wave', [
        '# Internal (macro, storage t). 1-2: the start disc (fill reaches r0 on the strike, stays 1 tick).',
        'scoreboard players operation #fkLife mb = #fkTell mb',
        'scoreboard players add #fkLife mb 2',
        *mk('t_fill', '~ ~0.03 ~', '0.02f,1f,0.02f', '$(r0)f,1f,$(r0)f', 'c2'),
        *mk('$(rim)', '~ ~0.045 ~', '$(r0)f,1f,$(r0)f', '$(r0)f,1f,$(r0)f', 'c1'),
        '# 3-4: the travelling rings: shown on the tick before the strike, moving from its end over dur ticks.',
        'scoreboard players operation #fkDly mb = #fkTell mb',
        'scoreboard players remove #fkDly mb 1',
        'scoreboard players operation #fkDur mb = #fkTd mb',
        'scoreboard players operation #fkLife mb = #fkTd mb',
        'scoreboard players operation #fkLife mb += #fkThold mb',
        'scoreboard players add #fkLife mb 1',
        'scoreboard players set #fkHit mb -1',
        *mk('t_ring', '~ ~0.05 ~', '$(r0)f,1f,$(r0)f', '$(r1)f,1f,$(r1)f', 'c1', flash=False),
        *mk('t_ring', '~ ~0.048 ~', '$(ri0)f,1f,$(ri0)f', '$(ri1)f,1f,$(ri1)f', 'c2', flash=False),
    ])
    W.w('tele/clear', ['# Remove every telegraph decal of the kit (a cancelled pattern, a pause); fx cards stay.',
                       f'kill {SEL}_t]', f'execute store result score #fkTN mb if entity {SEL}_t]'])


PROPS = {
    # name -> (comment, item kind, tint, billboard, transformation SNBT)
    'bomb': ('C1 bomb: the camera-facing gold bomb, 0.9 across (vertical billboard, so a falling bomb stays upright).',
             'bomb', WHITE, 'vertical', '[0.9f,0.9f,0.9f]'),
    'missile': ('C4 drill missile: nose along the prop\'s facing (local +z; aim it with tp ... facing), 1.3 long.',
                'missile', WHITE, 'fixed', None),
    'slab': ('C6 / F2 glowing slab: a box 2.2 x 0.6 x 0.9 b (length along local x), full bright rim.', 'slab', WHITE,
             'fixed', '[2.2f,2.2f,2.2f]'),
    'pebble': ('Floating pebble (field ambience), 0.35 across.', 'pebble', WHITE, 'center', '[0.35f,0.35f,0.35f]'),
    'chunk': ('Floor chunk / rock, 0.6 across.', 'chunk', WHITE, 'center', '[0.6f,0.6f,0.6f]'),
    'laser_core': ('C3 beam core: hangs from the prop along local -y (pitch the prop down the beam: rotation pitch = beam '
                   'pitch - 90), 0.45 wide; set scale y = the beam length.', 'laser_core', WHITE, 'fixed',
                   '[0.45f,5f,0.45f]'),
    'laser_glow': ('C3 beam glow sleeve: as laser_core, 1 b wide; scale x / z 0.5 -> 1.0 -> 0.5 for the bloom.',
                   'laser_glow', WHITE, 'fixed', '[1f,5f,1f]'),
    'column': ('Gold column standing on the prop (local +y), 1.1 wide; set scale y = the height.', 'column', WHITE,
               'fixed', '[1.1f,4f,1.1f]'),
    'ousia_col': ('Violet Ousia column hanging from the prop (local -y), 1 wide; set scale y = the length.', 'ousia_col',
                  WHITE, 'fixed', '[1f,3.5f,1f]'),
    'charge': ('Gravity-wave charge sphere look, 2 across (camera-facing).', 'charge_sphere', WHITE, 'center',
               '[2f,2f,2f]'),
    'muzzle': ('Laser muzzle ring, 0.8 across (camera-facing).', 'muzzle', WHITE, 'center', '[0.8f,0.8f,0.8f]'),
}
for _k in range(4):
    PROPS[f'bubble{_k}'] = (f'Core bubble overlay, crack stage {_k} (meter counts {5 * _k}-{5 * _k + 4}), 2.4 across, '
                            'camera-facing; swap stages with this prop as the meter climbs.', f'bubble{_k}', WHITE,
                            'center', '[2.4f,2.4f,2.4f]')
MISSILE_TR = ('{translation:[0f,0f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[1.3f,1.3f,1.3f],'
              'right_rotation:[0f,0f,0f,1f]}')


def prop_tr(scale):
    return ('{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:' + scale + ',right_rotation:[0f,0f,0f,1f]}')


def props(W):
    for name, (doc, kind, col, bb, sc) in PROPS.items():
        tr = MISSILE_TR if name == 'missile' else prop_tr(sc)
        W.w(f'prop/{name}', [f'# {doc}', '# As @s = an item_display the module owns (a pj prop or a marker look): item, tint, billboard,',
                             '# full bright, transformation. Keep teleport_duration 1 on moving props for smooth flight.',
                             f'data merge entity @s {{item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":'
                             f'"{NS_TEX}{kind}","minecraft:custom_model_data":{{colors:[{col}]}}}}}},billboard:"{bb}",'
                             f'brightness:{{sky:15,block:15}},view_range:2f,shadow_radius:0f,transformation:{tr}}}'])


def sounds(W):
    for name, (doc, layers) in SOUNDS.items():
        W.w(f'snd/{name}', [f'# {doc}', '# Layers: event volume pitch minVolume (per-layer minimum, mboss_lib.sound rule).'] +
            [sound_line(*l) for l in layers])


HUD_FUNCS = ('meter_open', 'meter_close', 'meter', 'meter_n', 'meter_hit', 'hint_on', 'hint_off', 'lowg_on', 'lowg_off',
             'groggy_on', 'groggy_off', 'clear', 'put_extra', 'put_sub', 'banner_field', 'banner_end', 'ab_lowg',
             'pop_break', 'pop_lowg', 'flash_white', 'flash_gold', 'flash_violet', 'flash_amber', 'flash_end')
METER_LABEL = '#C9B6F2'
FIELD_HEX = '#9C86E8'
GROGGY_HEX = '#A8E07A'


def gl(name, extra=''):
    return '{text:"' + glyph(name) + '",font:"' + FONT + '",color:"white"' + extra + '}'


def gls(text, extra=''):
    return '{text:"' + text + '",font:"' + FONT + '",color:"white"' + extra + '}'


def hud_funcs(W):
    H = FN + 'hud/'
    W.w('hud/meter_open', ['# The field opened: the meter shows 0/20 on the boss-bar lines (put_extra / put_sub).',
                           f'data modify storage {STO} hud.open set value 1b', 'scoreboard players set #fkM mb 0',
                           'scoreboard players set #fkMF mb 0', f'function {H}e/rebuild'])
    W.w('hud/meter_close', ['# The field closed (break, end, death, abort): the meter leaves the lines.',
                            f'data modify storage {STO} hud.open set value 0b', 'scoreboard players set #fkMF mb 0',
                            f'function {H}e/rebuild'])
    W.w('hud/meter', ['# Redraw the meter from #fkM mb (0-20; the module sets it from its count), no flash.',
                      'scoreboard players set #fkMF mb 0', f'function {H}e/rebuild'])
    W.w('hud/meter_n', ['# Macro form of hud/meter: {n:<0-20>}.', '$scoreboard players set #fkM mb $(n)',
                        f'function {H}meter'])
    hit = ['# One meter count, all its feedback (the module calls it once per counted hit, with #fkM mb = the new',
           '# count 1-20): the newest pip flashes white for 4 t, the crack glint at the executing position (run it at',
           '# the core), the brass ping plus a note that rises with the count, and on 5 / 10 / 15 the bubble cracks a',
           f'# stage: a bigger crack flash, the crack sound and {RIG()}crack/<1-3> as @s (run it as the',
           '# rig anchor, the body; without an anchor the rig call does nothing). Does not count anything itself.',
           'execute if score #fkM mb matches ..0 run scoreboard players set #fkM mb 1',
           'execute if score #fkM mb matches 21.. run scoreboard players set #fkM mb 20',
           'scoreboard players set #fkMF mb 1', f'function {H}e/rebuild',
           f'schedule function {H}e/unflash 4t replace',
           f'function {FN}p/meter_glint', f'function {FN}snd/meter_tick']
    for k, p in enumerate(METER_PITCH, 1):
        hit.append(f'execute if score #fkM mb matches {k} run playsound minecraft:block.note_block.chime hostile '
                   f'@a[tag=player] ~ ~ ~ 0.5 {p} 0.17')
    for k, st in ((5, 1), (10, 2), (15, 3)):
        hit.append(f'execute if score #fkM mb matches {k} run function {H}e/stage{st}')
    W.w('hud/meter_hit', hit)
    for st in (1, 2, 3):
        W.w(f'hud/e/stage{st}', [f'# Crack stage {st} (count {5 * st}).', f'function {FN}p/bubble_crack',
                                 f'function {FN}snd/bubble_crack',
                                 f'execute if entity @s[type=!minecraft:player] run function {RIG()}crack/{st}'])
    W.w('hud/e/unflash', ['# 4 t after a count: the white pip turns gold (bumps #fkHudV for the module).',
                          'scoreboard players set #fkMF mb 0', f'function {H}e/rebuild'])
    W.w('hud/hint_on', ['# Add the first-field hint "코어를 공격해 역장을 깨뜨리세요" after the meter on the sub-line.',
                        f'data modify storage {STO} hud.hint set value 1b', f'function {H}e/rebuild'])
    W.w('hud/hint_off', [f'data modify storage {STO} hud.hint set value 0b', f'function {H}e/rebuild'])
    W.w('hud/lowg_on', ['# Low gravity is on: the low-gravity icon on the name line.',
                        f'data modify storage {STO} hud.lowg set value 1b', f'function {H}e/rebuild'])
    W.w('hud/lowg_off', [f'data modify storage {STO} hud.lowg set value 0b', f'function {H}e/rebuild'])
    W.w('hud/groggy_on', ['# Groggy: " · 그로기" on the name line.',
                          f'data modify storage {STO} hud.grog set value 1b', f'function {H}e/rebuild'])
    W.w('hud/groggy_off', [f'data modify storage {STO} hud.grog set value 0b', f'function {H}e/rebuild'])
    W.w('hud/clear', ['# Every flag off (fight end, death, abort, uninstall).',
                      f'data modify storage {STO} hud merge value {{open:0b,lowg:0b,grog:0b,hint:0b}}',
                      'scoreboard players set #fkMF mb 0', f'function {H}e/rebuild'])
    rb = ['# Storage rlk:fgkit hud.ex (name-line suffix) and hud.sub (sub-line: badge, 역장, 20 pips, N/20, hint) from',
          '# the flags and #fkM / #fkMF. Bumps #fkHudV mb: a module that rebuilds its lines only on change should also',
          '# rebuild when #fkHudV changed (the pip flash ends 4 t after a count, from a schedule).',
          'execute if score #fkM mb matches ..-1 run scoreboard players set #fkM mb 0',
          'execute if score #fkM mb matches 21.. run scoreboard players set #fkM mb 20',
          f'data modify storage {STO} hud.ex set value []',
          f'data modify storage {STO} hud.sub set value []',
          f'execute if data storage {STO} hud{{open:1b}} run data modify storage {STO} hud.ex append value '
          f'{{text:"  · 역장",color:"{FIELD_HEX}",bold:false}}',
          f'execute if data storage {STO} hud{{open:1b}} run data modify storage {STO} hud.ex append value {{text:" "}}',
          f'execute if data storage {STO} hud{{open:1b}} run data modify storage {STO} hud.ex append value {gl("badge")}',
          f'execute if data storage {STO} hud{{lowg:1b}} run data modify storage {STO} hud.ex append value {{text:" "}}',
          f'execute if data storage {STO} hud{{lowg:1b}} run data modify storage {STO} hud.ex append value {gl("lowg")}',
          f'execute if data storage {STO} hud{{grog:1b}} run data modify storage {STO} hud.ex append value '
          f'{{text:"  · 그로기",color:"{GROGGY_HEX}",bold:false}}',
          f'execute unless data storage {STO} hud{{open:1b}} run return run function {H}e/bump']
    for n in range(21):
        rb.append(f'execute if score #fkM mb matches {n} run data modify storage {STO} hud.pc set value {gls(pips(n))}')
        if n:
            rb.append(f'execute if score #fkM mb matches {n} if score #fkMF mb matches 1 run data modify storage {STO} '
                      f'hud.pc set value {gls(pips(n, True))}')
        rb.append(f'execute if score #fkM mb matches {n} run data modify storage {STO} hud.nc set value '
                  f'{gls(digits(f"{n}/20"))}')
    rb += [f'data modify storage {STO} hud.sub append value {{text:"     "}}',
           f'data modify storage {STO} hud.sub append value {gl("badge")}',
           f'data modify storage {STO} hud.sub append value {{text:" 역장  ",color:"{METER_LABEL}",bold:true}}',
           f'data modify storage {STO} hud.sub append from storage {STO} hud.pc',
           f'data modify storage {STO} hud.sub append value {{text:"  "}}',
           f'data modify storage {STO} hud.sub append from storage {STO} hud.nc',
           f'execute if data storage {STO} hud{{hint:1b}} run data modify storage {STO} hud.sub append value '
           '{text:"   코어를 공격해 역장을 깨뜨리세요",color:"#B9AEDA"}',
           f'function {H}e/bump']
    W.w('hud/e/rebuild', rb)
    W.w('hud/e/bump', ['scoreboard players add #fkHudV mb 1'])
    W.w('hud/put_extra', ['# Append the flags to the boss-bar name line: call at the end of the module\'s line-1 build',
                          '# (after it resets rlk:mboss extra). Same as the component',
                          f'# {{nbt:"hud.ex[]",storage:"{STO}",interpret:true,separator:""}}.',
                          f'data modify storage rlk:mboss extra append from storage {STO} hud.ex[]'])
    W.w('hud/put_sub', ['# Append the meter (badge, 역장, 20 pips, N/20, hint) to the boss-bar third line (rlk:mboss sub),',
                        '# after the module\'s own text.',
                        f'data modify storage rlk:mboss sub append from storage {STO} hud.sub[]'])
    red, white = '#FC5050', '#F4F0FF'
    banner = (f'[{gl("lowg")},{{text:" 중력",color:"{red}",bold:true}},{{text:"이 감소하고 ",color:"{white}"}},'
              f'{{text:"점프",color:"{red}",bold:true}},{{text:" 능력이 향상됩니다",color:"{white}"}}]')
    W.w('hud/banner_field', ['# The field banner (field +57): the actionbar line "중력이 감소하고 점프 능력이 향상됩니다" with 중력 and',
                             '# 점프 in red (the video\'s banner) for 4 s, holding the regular actionbar HUD (hudHold), the',
                             '# big low-gravity icon on the title line for 1.5 s, and its sound. Typed captions on the',
                             '# subtitle line (mboss/line/say) are not touched.',
                             f'title @a[tag=player] actionbar {banner}', 'scoreboard players set @a[tag=player] hudHold 80',
                             f'function {H}pop_lowg', f'function {FN}snd/field_banner'])
    W.w('hud/banner_end', ['# Drop the banner early (cancel, break).', 'title @a[tag=player] actionbar ""',
                           'scoreboard players set @a[tag=player] hudHold 0'])
    W.w('hud/ab_lowg', ['# One-shot actionbar notice (2 s): low gravity and what it means.',
                        f'title @a[tag=player] actionbar [{gl("lowg")},{{text:" 중력 감소",color:"#C9B6F2",bold:true}},'
                        '{text:" — 점프 강화 · 낙하 피해 감소 · 충격파는 점프로 피하기",color:"#B9AEDA"}]',
                        'scoreboard players set @a[tag=player] hudHold 40'])
    for name, g, t in (('pop_break', 'break_big', '2 18 8'), ('pop_lowg', 'lowg_big', '3 24 8')):
        W.w(f'hud/{name}', ['# The big glyph pops on the title line and fades; the F5 crosshair title rests (vBig).',
                            'scoreboard players set @a[tag=player] vBig 34',
                            f'title @a[tag=player] times {t}',
                            'title @a[tag=player] title [' + gl(g, ',shadow_color:0') + ']'])
    for name, g, t in (('flash_white', 'fl_white', '0 2 5'), ('flash_gold', 'fl_gold', '1 3 8'),
                       ('flash_violet', 'fl_violet', '1 4 9'), ('flash_amber', 'fl_amber', '0 3 8')):
        W.w(f'hud/{name}', ['# Full-screen flat flash on the title line (any view mode); vBig rests the F5 crosshair.',
                            'scoreboard players set @a[tag=player] vBig 16',
                            f'title @a[tag=player] times {t}',
                            'title @a[tag=player] title [' + gl(g, ',shadow_color:0') + ',' + gls(SP_NEG1) + ']'])
    W.w('hud/flash_end', ['# Drop a title overlay at once (pause, cancel).',
                          'scoreboard players set @a[tag=player] vBig 0',
                          'title @a[tag=player] times 0 1 2', 'title @a[tag=player] title ""'])


def presets_dp(W):
    assert set(AMBIENT) <= set(PRESETS), set(AMBIENT) - set(PRESETS)
    for name, (doc, args, f) in PRESETS.items():
        lines = f()
        head = [f'# {doc}']
        if args:
            head.append('# {' + ', '.join(args) + '} (macro)')
            assert any(l.startswith('$') for l in lines), name
        else:
            assert not any(l.startswith('$') for l in lines), name
        if name in AMBIENT:
            head += [f'# Ambient: skipped while {SOFT}+ fx cards live (room for the fx of the hits).',
                     f'execute if score #fkN mb matches {SOFT}.. run return 0']
        W.w(f'p/{name}', head + lines)
    W.w('p/e/wave_band', ['# Internal (macro, storage rlk:fgkit w): the 16 band segments of p/wave_band.'] + _p_e_wave_band())
    W.w('p/e/rim_flare', ['# Internal (macro, storage rlk:fgkit fl: d = the ring\'s diameter): the two ripples of p/rim_flare.']
        + _p_e_rim_flare())


def preset_cards(name):
    """fx cards a preset spawns (card / cardx lines; the wave band's internal macro counts its 16 segments)"""
    if name == 'wave_band':
        return 16
    if name == 'rim_flare':
        return 2
    return sum(1 for l in PRESETS[name][2]() if f'{FN}card' in l)


# ----------------------------------------------------------------------------- tests and demos
TEST_ARGS = {'h': 4.0, 'len': 4.5, 'r0': 3.0, 'r': 8.0, 'grow': 26, 'life': 45, 't': 24, 'r1': 210, 'w': 25,
             'dur': 34}


def _test_call(name):
    args = PRESETS[name][1]
    vals = dict(TEST_ARGS)
    if name == 'wave_band':
        vals.update(r0=25, r1=210, w=25, dur=34)
    return fx(name, **{a: vals[a] for a in args})


# Demo timelines (in-game previews with the rig API; F:fx/test/demo/<name>): (tick, where, line). `where` is
# 'floor' (the anchor's floor point), 'ring' / 'core' / 'hub' (above the anchor at the cruise / field heights below)
# or 'player' (at the player's feet). Heights are model.md §8 rest poses (cruise ring 4.5, field core 3.84).
H_RING, H_HUB, H_CORE_C, H_CORE_F, H_CORE_UP = 4.5, 5.2, 4.6, 3.84, 7.8
DEMOS = {
    'entrance': ('dormant', 'entrance', [
        (0, 'ring2', fx('awake')), (0, 'ring2', snd('awake_clank')), (8, 'ring2', fx('unfold')), (8, 'ring2', snd('unfold')),
        (14, 'ring2', fx('crown_flare')), (20, 'ring2', snd('gear_click')), (22, 'ring2', fx('crown_flare')),
        (30, 'ring2', snd('gear_click')), (38, 'ring2', fx('eye_open')), (38, 'ring2', snd('eye_open')),
        (64, 'floor', fx('rise')), (64, 'ring', snd('rise_hum'))]),
    'bombs': ('cruise', 'bomb_run', [
        (10, 'ring', fx('ports_glow')), (10, 'ring', snd('bomb_port'))] +
        [(14 + 4 * k, 'line%d' % k, fx('bomb_drop', h=3.8)) for k in range(8)] +
        [(19 + 4 * k, 'line%d' % k, fx('bomb_burst')) for k in range(8)] +
        [(19 + 4 * k, 'line%d' % k, snd('bomb_burst')) for k in range(0, 8, 2)] +
        [(54, 'floor', fx('column_tell', h=H_CORE_C)), (54, 'floor', snd('column_tell')), (67, 'ring', fx('plunge')),
         (67, 'ring', snd('plunge')), (70, 'floor', fx('slam')), (70, 'floor', snd('slam'))]),
    'laser': ('laser', 'laser', [
        (0, 'medl', fx('pods_drop')), (0, 'medr', fx('pods_drop')), (0, 'ring', snd('pods_drop')),
        (4, 'medl', fx('laser_charge')), (4, 'medr', fx('laser_charge')), (4, 'ring', snd('laser_charge')),
        (10, 'medl', fx('laser_charge')), (10, 'medr', fx('laser_charge')), (16, 'medl', fx('laser_charge')),
        (16, 'medr', fx('laser_charge')), (24, 'medl', fx('spark')), (24, 'medr', fx('spark')), (24, 'ring', snd('laser_fire'))] +
        [(26 + 3 * k, 'spotl', fx('laser_spot')) for k in range(10)] + [(26 + 3 * k, 'spotr', fx('laser_spot')) for k in range(10)] +
        [(56, 'medl', fx('laser_end')), (56, 'medr', fx('laser_end')), (56, 'ring', snd('laser_stop'))]),
    'missiles': ('cruise', 'missiles', [
        (0, 'tipl', fx('tip_flare')), (0, 'tipr', fx('tip_flare')), (0, 'ring', snd('tip_flare')),
        (8, 'hub', fx('vent_shaft')), (8, 'hub', snd('missile_vent'))] +
        [(25 + 2 * k, 'hub', fx('missile_launch')) for k in range(5)] + [(25 + 2 * k, 'hub', snd('missile_launch')) for k in range(5)] +
        [(53 + 2 * k, 'line%d' % k, fx('missile_impact')) for k in range(5)] +
        [(53 + 2 * k, 'line%d' % k, snd('missile_impact')) for k in range(5)]),
    'blast': ('coreup', 'coreup', [
        (0, 'coreup', fx('core_spark')), (0, 'coreup', snd('core_spark')), (5, 'coreup', fx('core_lift')),
        (5, 'coreup', snd('core_lift')), (3, 'floor', tele_rim(12.0, 45)), (7, 'floor', tele_dark(3.5, 12.0, 41, 26)),
        (29, 'coreup', fx('up_beam')), (29, 'coreup', snd('up_beam')), (36, 'floor', fx('rim_flare', r=12.0)),
        (41, 'floor', fx('column_down', h=H_CORE_UP)), (41, 'floor', snd('column_down')), (44, 'floor', fx('floor_hit')),
        (48, 'floor', fx('blast', r=12.0)), (48, 'floor', fx('rocks')), (48, 'floor', snd('blast')),
        (60, 'floor', snd('rocks_hover'))]),
    'rocks': ('tower', 'tower_throw', [
        (0, 'floor', fx('dip')), (0, 'ring', snd('dip')), (12, 'hub', fx('vent_flare')), (12, 'hub', snd('vent_flare')),
        (20, 'ring', fx('tower_up')), (20, 'ring', snd('tower_up')), (40, 'under', fx('flame_band')),
        (40, 'ring', snd('flame_charge'))] +
        [(60 + 6 * k, 'arc%d' % k, fx('floor_burst')) for k in range(6)] +
        [(60 + 6 * k, 'arc%d' % k, snd('floor_burst')) for k in range(6)] +
        [(62 + 6 * k, 'arc%d' % k, fx('slab_rise')) for k in range(6)] +
        [(110, 'ring', fx('revert')), (110, 'ring', snd('revert'))]),
    'field': ('cruise', 'warp_out', [
        (0, 'halo', fx('halo_flip')), (0, 'halo', snd('halo_flip')), (13, 'floor', fx('warp_out')),
        (13, 'floor', snd('warp_out'))] + [(14 + 5 * k, 'floor', fx('glitch')) for k in range(4)] +
        [(16, 'floor', snd('glitch')), (34, 'corefield', fx('warp_in')), (34, 'floor', fx('warp_pillar')),
         (34, 'corefield', snd('warp_in')), (35, 'corefield', fx('field_unfold')), (35, 'corefield', snd('field_unfold')),
         (57, 'player', hud('banner_field')), (57, 'player', fx('pebbles')), (60, 'floor', fx('gold_streaks')),
         (70, 'corefield', fx('field_idle')), (77, 'player', fx('pebbles'))]),
    'waves': ('field', 'wave', [
        (0, 'corefield', fx('wave_charge', t=24)), (0, 'corefield', snd('wave_charge')), (8, 'corefield', fx('wave_pulse')),
        (16, 'corefield', fx('wave_pulse')), (14, 'corefield', snd('wave_charge2')),
        (24, 'floor', fx('wave_beam', h=H_CORE_F)),
        (24, 'floor', snd('wave_beam')), (25, 'floor', fx('wave_burst')), (25, 'floor', snd('wave_burst')),
        (23, 'floor', fx('wave_band', r0=25, r1=210, w=25, dur=34))] +
        [(24 + 3 * k, 'floor', fx('wave_fire', r=round(2.5 + 0.55 * 3 * k, 2))) for k in range(11)]),
    'erupt': ('field', 'field_erupt', [
        (0, 'zone0', fx('erupt_tell')), (0, 'zone0', tele_dark(0.8, 2.8, 15, 6)), (0, 'zone0', snd('erupt_tell')),
        (0, 'zone1', fx('erupt_tell')), (0, 'zone1', tele_dark(0.8, 2.8, 15, 6)),
        (15, 'zone0', fx('erupt')), (15, 'zone1', fx('erupt')), (15, 'zone0', snd('erupt')),
        (18, 'zone0', fx('debris')), (18, 'zone1', fx('debris')), (40, 'zone0', snd('debris_land'))]),
    'break': ('field', 'break', [
        (0, 'corefield', fx('bubble_glow')), (0, 'corefield', snd('break_glow')), (5, 'corefield', fx('break_burst')),
        (5, 'floor', fx('break_ring')), (5, 'corefield', snd('break_burst')), (5, 'player', hud('pop_break')),
        (5, 'player', hud('flash_gold')), (14, 'ring', snd('groggy_wobble')), (34, 'floor', fx('sink_dust')),
        (60, 'corefield', fx('groggy_sparks')), (60, 'corefield', snd('groggy_spark'))]),
    'death': ('cruise', 'death', [
        (0, 'core', fx('death_flicker')), (0, 'core', snd('death')), (5, 'core', fx('death_flicker')),
        (10, 'core', fx('death_flicker')), (50, 'floor', fx('death_fall')), (50, 'floor', snd('death_fall')),
        (70, 'core', fx('death_fade')), (85, 'core', fx('death_fade')), (85, 'core', snd('death_fade'))]),
}
DEMO_LEN = {k: max(t for t, _w, _l in v[2]) + 20 for k, v in DEMOS.items()}


def demo_where(where):
    """execute sub-commands of a demo event (run as the demo anchor marker): its point, rotated as the anchor"""
    if where == 'floor':
        return 'at @s rotated as @s rotated ~ 0'
    if where == 'player':
        return 'at @p[tag=player] rotated as @s rotated ~ 0'
    hts = {'ring': H_RING, 'ring2': 2.15, 'hub': H_HUB, 'core': H_CORE_C, 'corefield': H_CORE_F, 'coreup': H_CORE_UP,
           'halo': H_RING + 1.6, 'under': H_RING - 0.5}
    if where in hts:
        return f'at @s rotated as @s rotated ~ 0 positioned ~ ~{num(hts[where], 2)} ~'
    pts = {'medl': (2.8, 2.5, 0.0), 'medr': (-2.8, 2.5, 0.0), 'tipl': (4.5, H_RING, 0.0), 'tipr': (-4.5, H_RING, 0.0),
           'spotl': (3.5, 0.0, 3.0), 'spotr': (-3.5, 0.0, 3.0), 'zone0': (3.5, 0.0, 5.0), 'zone1': (-3.0, 0.0, 6.5)}
    if where in pts:
        x, y, z = pts[where]
        return f'at @s rotated as @s rotated ~ 0 positioned ^{num(x)} ^{num(y)} ^{num(z)}'
    if where.startswith('line'):
        k = int(where[4:])
        return f'at @s rotated as @s rotated ~ 0 positioned ^{num(0.6 * (-1) ** k)} ^ ^{num(2 + 1.4 * k)}'
    if where.startswith('arc'):
        k = int(where[3:])
        x, z = ring_xz(5.5, -50 + 20 * k)
        return f'at @s rotated as @s rotated ~ 0 positioned ^{num(x, 2)} ^ ^{num(z, 2)}'
    raise ValueError(where)


def tests(W):
    t = ['# Every fx kind in rows in front of the executor (3 s each):',
         '# /execute as @p at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/test/kinds']
    for i, kind in enumerate(FX_KINDS):
        row, colm = divmod(i, 7)
        x = 4.5 - 1.5 * colm
        z = 4 + 2.2 * row
        plane = KINDS[kind][0]
        if plane in ('flat', 'band'):
            t.append(card(kind, f'^{num(x)} ^0.05 ^{num(z)}', '~ 0', s0=0.3, s1=1.4, life=60, fade=10))
        else:
            t.append(card(kind, f'^{num(x)} ^1.2 ^{num(z)}', '~180 0', s0=0.3, s1=1.2, life=60, fade=10))
    W.w('test/kinds', t)
    W.w('test/tele', ['# One telegraph of each shape around the executor (tell 40 t; Geo / violet / physical), the wave',
                      '# ring and a moving line that turns for the next 84 t (test/e/mturn):',
                      '# /execute as @p at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/test/tele',
                      'execute positioned ^4 ^ ^5 run ' + tele_disc(2.8, 40, 5),
                      'execute positioned ^-4 ^ ^5 run ' + tele_disc(1.5, 40, 9),
                      'execute positioned ^ ^ ^11 run ' + tele_ring(1.5, 3.5, 40, 5),
                      'execute positioned ^6 ^ ^12 run ' + tele_sector(4.5, 90, 40, 9),
                      'execute positioned ^-6 ^ ^12 run ' + tele_sector(4.0, 45, 40, 0),
                      'execute positioned ^ ^ ^3 run ' + tele_line(6.0, 2.0, 40, 5),
                      'execute positioned ^9 ^ ^5 run ' + tele_rim(2.8, 40),
                      'execute positioned ^-9 ^ ^5 run ' + tele_dark(0.8, 2.8, 40, 6),
                      'execute positioned ^ ^ ^20 run ' + tele_wave(2.5, 12.0, 2.5, 40, 17),
                      'execute positioned ^-8 ^ ^20 run ' + tele_mline(0, 5.8, 0.8, 24, 5, hold=60, back=-2.8),
                      'scoreboard players set #fkMT mb 0',
                      f'schedule function {FN}test/e/mturn 1t replace'])
    W.w('test/e/mturn', ['# Turn the test moving line 5 degrees a tick for 84 t.',
                         'scoreboard players add #fkMT mb 1', tele_mline_turn(0, 5),
                         f'execute if score #fkMT mb matches ..83 run schedule function {FN}test/e/mturn 1t replace'])
    W.w('test/sounds', ['# Click through the sound recipes (tellraw list).',
                        'tellraw @s [{"text":"역장 발생 장치 sounds: ","color":"#E8C46A"}' +
                        ''.join(f',{{"text":"[{n}] ","color":"#F5E0A0","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}"}}}}' for n in SOUNDS) + ']'])
    W.w('test/hud', ['# The meter (12 / 20, a fresh count), low gravity and the banner (run during a fight to see the lines).',
                     f'function {FN}hud/meter_open', 'scoreboard players set #fkM mb 12', f'function {FN}hud/meter_hit',
                     f'function {FN}hud/lowg_on', f'function {FN}hud/banner_field'])
    W.w('test/presets', ['# Click through the presets (tellraw list; macro presets use test values).',
                         'tellraw @s [{"text":"역장 발생 장치 fx: ","color":"#E8C46A"}' +
                         ''.join(f',{{"text":"[{n}] ","color":"#F5E0A0","click_event":{{"action":"run_command",'
                                 f'"command":"/execute at @s rotated ~ 0 positioned ^ ^ ^6 run {_test_call(n)}"}}}}'
                                 for n in PRESETS) + ']'])
    # demos: a marker anchor 9 b ahead, the rig (real or stub) on it, a scheduled ticker
    R = RIG()
    W.w('test/stage', ['# Spawn the demo anchor 9 b in front of the executor, facing it, with the rig on it (the real rig',
                       '# when its manifest exists, else the kit\'s stub). /execute as @p at @s rotated ~ 0 run function',
                       '# rlk:mboss/fieldgen/fx/test/stage, then test/demo/<name>. test/stop removes it.',
                       f'function {FN}test/stop',
                       'execute positioned ^ ^ ^9 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_fk_demo","rlk_room","rlk_mb_aux"]}',
                       'execute as @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0',
                       f'execute as @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] at @s rotated as @s run function {R}spawn',
                       'scoreboard players set #fkDemo mb 0', 'scoreboard players set #fkDT mb 0',
                       f'schedule function {FN}test/e/tick 1t replace'])
    W.w('test/stop', ['# Remove the demo anchor and its rig.',
                      f'execute as @e[type=minecraft:marker,tag=rlk_fk_demo] run function {R}kill',
                      'kill @e[type=minecraft:marker,tag=rlk_fk_demo]', f'schedule clear {FN}test/e/tick',
                      'scoreboard players set #fkDemo mb 0'])
    tick = ['# Demo ticker (scheduled): the rig tick as the anchor, then the running demo\'s events.',
            'execute unless entity @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] run return 0',
            f'execute as @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] at @s run function {R}tick',
            'execute if score #fkDemo mb matches 1.. run scoreboard players add #fkDT mb 1']
    for k, name in enumerate(DEMOS, 1):
        tick.append(f'execute if score #fkDemo mb matches {k} as @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] '
                    f'run function {FN}test/demo/e/{name}')
        tick.append(f'execute if score #fkDemo mb matches {k} if score #fkDT mb matches {DEMO_LEN[name]}.. run '
                    'scoreboard players set #fkDemo mb 0')
    tick.append(f'schedule function {FN}test/e/tick 1t replace')
    W.w('test/e/tick', tick)
    for k, (name, (form, clip, events)) in enumerate(DEMOS.items(), 1):
        W.w(f'test/demo/{name}', [f'# Demo "{name}": the rig in form {form} plays {clip}, the kit fires the events of the plan.',
                                  '# Needs test/stage first.',
                                  'execute unless entity @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] run '
                                  f'function {FN}test/stage',
                                  f'execute as @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] at @s run function {R}form/{form}',
                                  f'execute as @e[type=minecraft:marker,tag=rlk_fk_demo,limit=1] at @s run function {R}play/{clip}',
                                  f'scoreboard players set #fkDemo mb {k}', 'scoreboard players set #fkDT mb -1'])
        lines = [f'# Demo "{name}" events (as the anchor; #fkDT = the demo tick).']
        for tk, where, line in sorted(events, key=lambda e: e[0]):
            lines.append(f'execute if score #fkDT mb matches {tk} {demo_where(where)} run {line}')
        W.w(f'test/demo/e/{name}', lines)


def build_datapack(dp):
    W = Writer(dp)
    engine(W)
    telegraphs(W)
    sounds(W)
    hud_funcs(W)
    presets_dp(W)
    props(W)
    tests(W)
    # The kit's stand-in rig (tools/mboss_fg_fx_stub_rig.py) was removed when the real rig was merged (fg_fx_api.md
    # section 9): the kit drives rlk:mboss/fieldgen/rig/ and still cleans its old fx/rig_stub/ (an owned dir).
    assert rig_mode() == 'real', f'{RIG_MANIFEST} is missing: build the field generator rig first (tools/build_mboss_fieldgen_rig.mjs)'
    removed = W.flush()
    return len(W.files), removed


def manifest():
    return {
        'generator': 'tools/build_mboss_fg_fx.py',
        'functions': FN, 'item_models': NS_TEX, 'font': FONT, 'storage': STO,
        'rig': {'mode': rig_mode(), 'functions': RIG(), 'manifest': RIG_MANIFEST.name},
        'owned': {'dirs': [f'{FDIR}/{d}' for d in OWNED_DIRS], 'files': [f'{FDIR}/{f}.mcfunction' for f in OWNED_FILES],
                  'rp': [f'assets/rlk/textures/{TEXDIR}', f'assets/rlk/models/item/{TEXDIR}', f'assets/rlk/items/{TEXDIR}',
                         f'assets/rlk/font/{FONT_NAME}.json', f'assets/rlk/textures/font/{FONT_NAME}']},
        'caps': {'fx': CAP, 'telegraph': TCAP},
        'objectives': list(OBJECTIVES),
        'tags': [TAG, f'{TAG}_t', f'{TAG}_ml<id>', 'rlk_fk_demo', 'rlk_fk_rs (stub rig)'],
        'kinds': {k: {'plane': v[0], 'px': list(v[1]), 'extent': list(v[2]), 'tint': 'neutral' if v[6] else 'painted',
                      'desc': v[7]} for k, v in KINDS.items()},
        'atlas_px': atlas_px(),
        'presets': {k: {'args': v[1], 'doc': v[0], 'cards': preset_cards(k)} for k, v in PRESETS.items()},
        'props': {k: v[0] for k, v in PROPS.items()},
        'sounds': {k: v[0] for k, v in SOUNDS.items()},
        'glyphs': {k: f'U+{v[0]:04X}' for k, v in GLYPHS.items()},
        'telegraph_colours': {str(k): [f'#{c:06X}' for c in v] for k, v in TELE_COL.items()},
        'demos': {k: {'form': v[0], 'clip': v[1], 'len': DEMO_LEN[k]} for k, v in DEMOS.items()},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--resourcepack', help='unpacked resource pack root (assets/...)')
    ap.add_argument('--datapack', default=str(HERE.parent), help='datapack root (data/...)')
    ap.add_argument('--skip-rp', action='store_true', help='only write the datapack functions')
    a = ap.parse_args()
    n, removed = build_datapack(a.datapack)
    (HERE / 'mboss_fg_fx_manifest.json').write_text(json.dumps(manifest(), ensure_ascii=False, indent=1) + '\n',
                                                     encoding='utf-8')
    msg = (f'field generator fx kit: {n} functions ({removed} stale removed), {len(PRESETS)} presets, {len(SOUNDS)} '
           f'sounds, rig {rig_mode()}')
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error('--resourcepack is required unless --skip-rp')
        k, px, g = build_resourcepack(a.resourcepack)
        msg += f', {k} sprites ({px / 1e6:.2f} M px of atlas), {g} glyphs in {FONT}'
    print(msg)


if __name__ == '__main__':
    main()
