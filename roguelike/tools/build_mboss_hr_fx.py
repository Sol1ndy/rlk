#!/usr/bin/env python3
"""FX / audio / HUD kit of the special boss 홍련 (Scarlet; module boss/scarlet, PLAN scratchpad hr/PLAN.md §9.2).

The Arlecchino kit's card engine (tools/build_mboss_kn_fx.py: the fg kit engine with its first-tick fix, the
self-rescheduling ager, no shared-file hooks) copied and renamed, with the call list frozen in tools/mboss_scarlet/api.py
§8 (KIT_PRESETS, KIT_PROPS, KIT_SOUND_RECIPES, KIT_HUD, OVERLAYS, VIG, KIT_FIXED, KIT_SPRITES; contract §3.3). The module
(S3 core / phase 1, S4 ghost patterns, S2b sequences, the §7 event coda) calls it only through api.K; nothing here
decides gameplay (hits, hazards, projectiles, timings stay in the module). Parts, all regenerated on every run:

  1. The tinted card engine: painted sprites on short-lived item_display cards (planes face, flat, cross, lance, lancex).
     Three pools, each capped, the ager killing the OLDEST cards of a pool over its cap (a spawn serial, hrFxQ): fx
     (CAP_FX 96), ambient (CAP_AMB 48: the drifting petals / leaves / motes) and the afterimages (CAP_AI 4: one lilac
     silhouette card per frame, fading over 6 t). Nothing is ever skipped: new effects always show.
  2. Presets fx/p/<name> (macro args in tenths of a block / degrees / ticks; c 1 lilac, 2 pink-magenta, 3 yellow,
     4 crimson, 5 white; every pitch > 0 = up, yaw > 0 = to the executor's right), props fx/prop/<name> (@s = the
     item_display the caller summoned and rotated: dressed in place, exactly one card; seat_rock also keeps its bottle
     / cup as kit followers), sound recipes fx/snd/<name> (api.KIT_SOUND_RECIPES: vanilla events only, the mboss_lib.sound
     min-volume rule).
  3. The HUD: font rlk:mboss_hr (U+EC00-ECFF): the six full-screen overlay glyphs U+EC10-EC15 (api.OVERLAYS, 144 x 81,
     sized as Apep's) and `vig` U+EC16 (api.VIG, the edge vignette SR's item code titles); fx/hud/line {id} (api.LINES
     1-25, Raiden's letter reveal, held api.LINE_AT[id][2] t, overlay-aware), fx/hud/ovl {g,in,hold,out}, fx/hud/warn {on}
     (bossbar rlk:hr_warn = api.WARN_TEXT), fx/hud/skip {s} (the intro's actionbar prompt), fx/hud/clear. Glyph roots
     are empty and unstyled, every text component names its font, the font ends with a reference to minecraft:default.
  4. In-game demos fx/test/<preset>, fx/test/prop/<name> on a vanilla stand-in (an armour stand with an iron sword),
     fx/test/{stage,stop,sounds,hud,kinds}.

Outputs (owned; stale files in these places are removed):
  resource pack  assets/rlk/textures/mboss/hr_kit/<sprite>.png       painted sprites (stdlib painter, api.KIT_SPRITES)
                 assets/rlk/models/item/mboss/hr_kit/<kind>.json      card models (tintindex 0)
                 assets/rlk/items/mboss/hr_kit/<kind>.json            item definitions, custom_model_data tint
                 assets/minecraft/atlases/items.json                  adds rlk:mboss/hr_kit/* (filter-then-push by id)
                 assets/rlk/font/mboss_hr.json + textures/font/mboss_hr/*.png
  datapack       data/rlk/function/boss/scarlet/fx/{card,cardx,look,clear,uninstall}
                 data/rlk/function/boss/scarlet/fx/{e,p,prop,snd,hud,test}/**
  manifest       tools/mboss_hr_fx_manifest.json   (its presence switches api.K on)

Cards carry rlk_hr_fx + rlk_room + rlk_mb_aux. Objectives hrFx (fake players) and hrFxS hrFxG hrFxH hrFxK hrFxD (the
card stage clock), hrFxL (prop follower links), hrFxQ (the spawn serial of the cull); storage rlk:hr fx.*; bossbar
rlk:hr_warn. The module wires cleanup -> fx/clear + fx/hud/clear, pause / death_start -> fx/clear, uninstall ->
fx/uninstall (contract §3.3).

Run: python3 tools/build_mboss_hr_fx.py --resourcepack <unpacked RP>   (or --skip-rp: the datapack + manifest only)
"""
from pathlib import Path
import argparse
import json
import math
import random
import re
import struct
import sys
import zlib

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mboss_hr_fx_paint as P  # noqa: E402
import mboss_lib as L  # noqa: E402
from mboss_scarlet import api  # noqa: E402

ROOT = api.ROOT                        # boss/scarlet
FN = f'rlk:{ROOT}/fx/'
FDIR = f'data/rlk/function/{ROOT}/fx'
NS_TEX = api.RP_KIT                    # rlk:mboss/hr_kit/
TEXDIR = 'mboss/hr_kit'
FONT = api.FONT                        # rlk:mboss_hr
FONT_NAME = 'mboss_hr'
STO = api.STORAGE                      # rlk:hr; kit keys fx.* (contract §2)
CAP_FX, CAP_AMB, CAP_AI = api.FX_CARD_CAP, api.AMBIENT_CARD_CAP, api.AFTERIMAGE_MAX     # 96 / 48 / 4
AI_FADE = api.AFTERIMAGE_FADE          # 6
OWNED_DIRS = ('e', 'p', 'prop', 'snd', 'hud', 'test')
OWNED_FILES = tuple(api.KIT_FIXED)     # card cardx look clear uninstall
OBJ = 'hrFx'                           # the kit's fake players
OBJECTIVES = ('hrFxS', 'hrFxG', 'hrFxH', 'hrFxK', 'hrFxD', 'hrFxL', 'hrFxQ')
assert OBJ.startswith(api.KIT_OBJ_PREFIX) and all(o.startswith(api.KIT_OBJ_PREFIX) for o in OBJECTIVES)
TAG = api.TAGS['fx']                   # rlk_hr_fx
DEMO = f'{TAG}_demo'
ANIM = f'{TAG}a'                       # props the anim chain turns (rlk_hr_fxa + _d disc / _p petal)
FOLLOW = f'{TAG}f'                     # follower displays (the seat rock's bottle and cup)
LEAD = f'{TAG}l'                       # the entities followers stay with
BEAM = f'{TAG}_bm'                     # the ev_beam column markers (aged by the ager)
WARN_BAR = api.WARN_BOSSBAR            # rlk:hr_warn
FLOOR = api.CY                         # the arena floor top (hr_field: y 201); demos store their own in fx.fl
MANIFEST = HERE / 'mboss_hr_fx_manifest.json'
assert MANIFEST == api.KIT_MANIFEST


def rgb(h):
    return int(h[1:], 16)


# ----------------------------------------------------------------------------- colours (RGB ints for tints)
WHITE = 0xFFFFFF
LILAC = rgb('#C97EDD')
LILAC_PALE = rgb('#E8C2F6')
LILAC_DEEP = rgb('#7A4AA8')
MAGENTA = rgb('#E040A0')
YELLOW = rgb('#FFE14A')
CRIMSON = rgb('#E0203E')
CRIMSON_DEEP = rgb('#801028')
GOLD = rgb('#FFC84A')
ORANGE = rgb('#FF9A3A')
PINKW = rgb('#FFD6E6')
LEAF_RED = rgb('#7A1426')
LEAF_BLACK = rgb('#2A1018')
WARM = rgb('#EAC5AF')
RIFT_RIM = rgb('#C9C0FF')
C_ALL = (api.C_LILAC, api.C_MAGENTA, api.C_YELLOW, api.C_CRIMSON, api.C_WHITE)     # 1..5
TINT = {1: LILAC, 2: MAGENTA, 3: YELLOW, 4: CRIMSON, 5: WHITE}          # neutral (white / grey) sprites x this
QTINT = {1: WHITE, 2: rgb('#FF94E0'), 3: rgb('#FFF070'), 4: rgb('#FF6A80'), 5: WHITE}   # the lilac sword-qi sprites x this
QFADE = {1: rgb('#A890B8'), 2: rgb('#C07098'), 3: rgb('#C0B060'), 4: rgb('#B05060'), 5: rgb('#C0C0C8')}
DUSTC = {1: (0.79, 0.49, 0.87), 2: (0.88, 0.25, 0.63), 3: (1.0, 0.88, 0.29), 4: (0.88, 0.13, 0.24), 5: (1.0, 0.95, 0.98)}
DUST_PETAL = (0.84, 0.36, 0.53)        # #D55D87 (arena.md §4)
DUST_SILVER = (0.87, 0.90, 1.0)
DUST_LILAC_EV = (0.79, 0.63, 1.0)

# ----------------------------------------------------------------------------- sprites (the items atlas; = api.KIT_SPRITES)
# sprite -> [(texture stem, (w, h), painter box (a0, a1, b0, b1), painter, supersampling)]
ARC_BOX = (-1, 1, 0, 1)
UNIT = (-1, 1, -1, 1)
STRIP = (-1, 1, -0.25, 0.25)
TRAIL = (0, 1, -0.125, 0.125)
TALL = (-0.125, 0.125, 0, 1)
SPARK = (-0.125, 0.125, -0.5, 0.5)
SPRITES = {
    'qi_arc': [(f'qi_arc_{k}', (128, 64), ARC_BOX, P.make_arc(k), 2) for k in range(4)],
    'qi_ring': [('qi_ring_0', (128, 128), UNIT, P.paint_ring, 2), ('qi_ring_1', (128, 128), UNIT, P.paint_ring_rim, 2)],
    'qi_band': [('qi_band_0', (128, 32), STRIP, P.paint_band, 2), ('qi_band_1', (128, 32), STRIP, P.paint_band_edge, 2)],
    'qi_ribbon': [(f'qi_ribbon_{k}', (128, 32), STRIP, P.make_ribbon(k), 2) for k in range(2)],
    'ghost_trail': [('ghost_trail_0', (128, 32), TRAIL, P.paint_trail, 2), ('ghost_trail_1', (128, 32), TRAIL, P.paint_speedlines, 2)],
    'qi_dome': [('qi_dome', (128, 64), ARC_BOX, P.paint_dome, 2)],
    'qi_wedge': [('qi_wedge', (64, 128), (-0.25, 0.25, 0, 1), P.paint_wedge, 2)],
    'glint': [('glint_0', (32, 32), UNIT, P.paint_glint, 3), ('glint_1', (32, 32), UNIT, P.paint_star4, 3)],
    'shards': [(f'shards_{k}', (32, 32), UNIT, P.make_shard(k), 3) for k in range(2)],
    'lotus': [('lotus_0', (32, 32), UNIT, P.paint_lotus_bud, 3), ('lotus_1', (32, 32), UNIT, P.paint_lotus_bloom, 3)],
    'yellow_tell': [('yellow_tell_0', (64, 64), UNIT, P.paint_tell_sphere, 2),
                    ('yellow_tell_1', (128, 16), (-1, 1, -0.125, 0.125), P.paint_tell_flare, 2)],
    'ghost_burst': [(f'ghost_burst_{k}', (64, 64), UNIT, P.make_ghost(k), 2) for k in range(3)],
    'ghost_flash': [('ghost_flash', (64, 64), UNIT, P.paint_ghost_flash, 2)],
    'blink_bubble': [('blink_bubble', (64, 64), UNIT, P.paint_bubble, 2)],
    'afterimage': [('afterimage', (64, 128), (-0.25, 0.25, 0, 1), P.paint_afterimage, 2)],
    'dive_impact': [('dive_impact', (128, 128), UNIT, P.paint_impact, 2)],
    'light_column': [('light_column', (32, 128), TALL, P.paint_column, 2)],
    'claw_streaks': [('claw_streaks', (32, 128), TALL, P.paint_claw, 2)],
    'deco_bolt': [('deco_bolt', (32, 128), TALL, P.paint_bolt, 2)],
    'clash_gold': [(f'clash_gold_{k}', (64, 64), UNIT, P.make_clash(k), 2) for k in range(2)],
    'clash_spark': [(f'clash_spark_{k}', (32, 128), SPARK, P.make_spark(k), 2) for k in range(2)],
    'scarlet_line': [('scarlet_line', (256, 16), (-1, 1, -0.0625, 0.0625), P.paint_scarlet_line, 2)],
    'petal_big': [(f'petal_big_{k}', (64, 64), UNIT, P.make_petal_big(k), 2) for k in range(3)],
    'petals_small': [(f'petals_small_{k}', (16, 16), UNIT, P.make_small(k), 4) for k in range(8)],
    'moon_halo': [(f'moon_halo_{k}', (96, 96), UNIT, P.make_halo(k), 2) for k in range(2)],
    'disc': [(f'disc_{k}', (64, 64), UNIT, P.make_disc(k), 2) for k in range(2)],
    'seat_rock': [],                    # vanilla items (tuff, a potion bottle, a flower-pot cup): 0 px
}
GATE_ICON = ('gate_icon', (64, 64), UNIT, P.paint_gate_icon, 2)      # rlk:mboss/hr_kit/gate_icon (api.GATE_ICON_MODEL)
TEXTURES = {stem: (wh, box, fn, ss) for rows in SPRITES.values() for stem, wh, box, fn, ss in rows}
TEXTURES[GATE_ICON[0]] = GATE_ICON[1:]


def sprite_table():
    """{sprite: ((frames, w, h), ...)} of SPRITES, grouped as api.KIT_SPRITES writes it"""
    out = {}
    for name, rows in SPRITES.items():
        groups = []
        for _stem, (w, h), *_ in rows:
            if groups and groups[-1][1:] == (w, h):
                groups[-1] = (groups[-1][0] + 1, w, h)
            else:
                groups.append((1, w, h))
        out[name] = tuple(groups)
    return out


assert sprite_table() == api.KIT_SPRITES, {k: (v, api.KIT_SPRITES.get(k)) for k, v in sprite_table().items()
                                           if api.KIT_SPRITES.get(k) != v}
SPRITE_PX = sum(w * h for rows in SPRITES.values() for _s, (w, h), *_ in rows)
assert SPRITE_PX == api.KIT_SPRITE_PX <= api.KIT_SPRITE_CAP, SPRITE_PX
GATE_PX = GATE_ICON[1][0] * GATE_ICON[1][1]
assert GATE_PX <= api.GATE_ICON_PX_CAP, GATE_PX

# ----------------------------------------------------------------------------- card kinds (item models)
# kind -> (plane, texture stem, card extent in blocks at scale 1 (a0, a1, b0, b1), neutral (tinted)?, description).
# Planes: face (an x-y quad facing +z), flat (an x-z quad, +b forward), cross (two vertical quads), lance (a flat and a
# vertical quad along local +z: beams seen from any side), lancex (a flat and a face quad along local x: long strips
# whose texture width is their length; the kit yaws them -90 so +a points along the aim).
SQ = (-0.5, 0.5, -0.5, 0.5)
KINDS = {
    **{f'qi_arc_{k}': ('flat', f'qi_arc_{k}', ARC_BOX, False, f'sword-qi crescent sweep frame {k} (rim at r 0.8)') for k in range(4)},
    'qi_ring_0': ('flat', 'qi_ring_0', UNIT, False, 'flat lilac sword-qi ring (unit radius)'),
    'qi_ring_1': ('flat', 'qi_ring_1', UNIT, False, 'thin white-pink rim ring with swirls'),
    'qi_band_0': ('face', 'qi_band_0', (-0.5, 0.5, -0.125, 0.125), False, 'broad sword-qi band (length 1 along a)'),
    'qi_band_1': ('face', 'qi_band_1', (-0.5, 0.5, -0.125, 0.125), False, 'the band\'s leading streak'),
    'qi_ribbon_0': ('flat', 'qi_ribbon_0', STRIP, False, 'sword-qi ribbon strip (centred)'),
    'qi_ribbon_1': ('flat', 'qi_ribbon_1', STRIP, False, 'fading ribbon strip'),
    'ghost_trail_0': ('lancex', 'ghost_trail_0', TRAIL, False, 'lilac flame trail (from the executor along +a)'),
    'ghost_trail_1': ('lancex', 'ghost_trail_1', TRAIL, False, 'white speed lines'),
    'qi_dome': ('face', 'qi_dome', ARC_BOX, False, 'translucent dome silhouette (base at b 0)'),
    'qi_wedge': ('flat', 'qi_wedge', (-0.25, 0.25, 0, 1), False, 'sword-qi wedge, the point at b 1'),
    'glint_0': ('face', 'glint_0', SQ, True, 'four-ray glint (tinted)'),
    'glint_1': ('face', 'glint_1', SQ, True, 'four-point star in a circle (tinted)'),
    'shards_0': ('face', 'shards_0', SQ, True, 'crystal shard (tinted)'),
    'shards_1': ('face', 'shards_1', SQ, True, 'broken shard splinter (tinted)'),
    'lotus_0': ('face', 'lotus_0', (-0.5, 0.5, 0, 1), False, 'lotus bud on its pads, base at b 0'),
    'lotus_1': ('face', 'lotus_1', (-0.5, 0.5, 0, 1), False, 'open crimson lotus, base at b 0'),
    'yellow_tell_0': ('face', 'yellow_tell_0', SQ, False, 'yellow tell sphere'),
    'yellow_tell_1': ('face', 'yellow_tell_1', (-1, 1, -0.125, 0.125), False, 'yellow tell flare line (2 b at scale 1)'),
    **{f'ghost_burst_{k}': ('face', f'ghost_burst_{k}', SQ, False, ('ghost mist puff', 'ghost ribbons', 'ghost sparkles')[k])
       for k in range(3)},
    'ghost_flash': ('face', 'ghost_flash', SQ, False, 'white-violet electric flash'),
    'blink_bubble': ('face', 'blink_bubble', SQ, False, 'pale blue-white bubble'),
    'afterimage': ('face', 'afterimage', (-0.25, 0.25, 0, 1), False, 'lilac silhouette, feet at b 0'),
    'dive_impact': ('flat', 'dive_impact', UNIT, False, 'shock ring with radial spikes (unit radius)'),
    'light_column': ('cross', 'light_column', TALL, True, 'light column (two crossed quads, base at b 0; tinted)'),
    'col_face': ('face', 'light_column', TALL, True, 'one light-column quad (vertical billboard; tinted)'),
    'qline': ('lance', 'light_column', (-0.5, 0.5, 0, 1), True, 'thin light beam along +z (tinted)'),
    'claw_streaks': ('face', 'claw_streaks', TALL, False, 'claw streak, its point at b 0'),
    'deco_bolt': ('face', 'deco_bolt', TALL, False, 'thin yellow bolt, base at b 0'),
    'clash_gold_0': ('face', 'clash_gold_0', SQ, False, 'gold starburst'),
    'clash_gold_1': ('face', 'clash_gold_1', SQ, False, 'cyan-gold kick flash'),
    'clash_spark_0': ('face', 'clash_spark_0', SPARK, True, 'spark streak (tinted)'),
    'clash_spark_1': ('face', 'clash_spark_1', SPARK, True, 'lightning arc (tinted)'),
    'scarlet_line': ('lancex', 'scarlet_line', (-0.5, 0.5, -0.03125, 0.03125), False, 'the red slash line (centred, length 1)'),
    **{f'petal_big_{k}': ('face', f'petal_big_{k}', SQ, False, f'big red petal ({("whole", "cut", "split")[k]})') for k in range(3)},
    **{f'petal_{k}': ('face', f'petals_small_{k}', SQ, k >= 4, ('cherry petal', 'cherry petal', 'cherry petal', 'heart petal',
                                                                  'leaf (tinted)', 'leaf (tinted)', 'leaf (tinted)', 'mote (tinted)')[k])
       for k in range(8)},
    **{f'moon_halo_{k}': ('face', f'moon_halo_{k}', SQ, False, ('white-blue halo (P1)', 'red halo (P2)')[k]) for k in range(2)},
    **{f'disc_{k}': ('flat', f'disc_{k}', UNIT, False, f'moon disc spin frame {k} (unit radius)') for k in range(2)},
    'gate_icon': ('face', 'gate_icon', SQ, False, 'gate label icon: a red lotus over a long blade'),
}
# The arrival tear: the dungeon rift's item models (tools/build_rift.py), referenced (no px of ours); without them in the
# pack the item definitions fall back to the ghost flash card.
RIFT = {'rift_void': 'void', 'rift_rim': 'rim', **{f'rift_arc{k}': f'arc_{k}' for k in range(4)}}
RIFT_MODEL = 'rlk:item/rift/'
RIFT_FALLBACK = 'ghost_flash'
ALL_KINDS = list(KINDS) + list(RIFT)
SPIN_Y = ('flat', 'cross')             # planes that spin about local y; face / lance / lancex spin about z
assert all(k == k.lower() and re.fullmatch(r'[a-z0-9_]+', k) for k in ALL_KINDS)


def kind_info(kind):
    """(plane, (w, h), extent, neutral, texture id, description) of a kind (rift kinds: their fallback look)"""
    if kind in RIFT:
        plane, stem, ext, neu, _d = KINDS[RIFT_FALLBACK]
        return 'face', TEXTURES[stem][0], (-0.5, 0.5, -0.5, 0.5), False, NS_TEX + stem, \
            f'arrival tear part (rift/{RIFT[kind]}; fallback {RIFT_FALLBACK})'
    plane, stem, ext, neu, desc = KINDS[kind]
    return plane, TEXTURES[stem][0], ext, neu, NS_TEX + stem, desc


# ----------------------------------------------------------------------------- textures


def render(stem):
    (w, h), (a0, a1, b0, b1), fn, ss = TEXTURES[stem]
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


def png_size(path):
    data = Path(path).read_bytes()[:24]
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    return struct.unpack('>II', data[16:24])


def r4(v):
    return round(v, 4)


def model_json(kind):
    """Zero-thickness double-sided quads with tintindex 0 (fg kit convention: display-local p is written at model
    m = (8 - 16 px, 8 + 16 py, 8 - 16 pz); card +a = local -x). The lance's vertical quad maps the texture rows along z
    (face rotation), so a beam texture runs along the beam on both quads; the lancex quads share the a axis (local x)."""
    plane, _wh, (a0, a1, b0, b1), _n, tex, _d = kind_info(kind)
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1

    def q(frm, to, faces):
        return {'from': [r4(v) for v in frm], 'to': [r4(v) for v in to], 'shade': False, 'faces': faces}

    def f(uv, rot=0):
        d = {'uv': uv, 'texture': '#0', 'tintindex': 0}
        if rot:
            d['rotation'] = rot
        return d
    face = q([x0, 8 + 16 * b0, 8], [x1, 8 + 16 * b1, 8], {'south': f([0, 0, 16, 16]), 'north': f([16, 0, 0, 16])})
    flat = q([x0, 8, 8 - 16 * b1], [x1, 8, 8 - 16 * b0], {'up': f([0, 0, 16, 16]), 'down': f([0, 16, 16, 0])})
    if plane == 'face':
        els = [face]
    elif plane == 'flat':
        els = [flat]
    elif plane == 'cross':
        els = [face, q([8, 8 + 16 * b0, 8 - 16 * a1], [8, 8 + 16 * b1, 8 - 16 * a0],
                       {'east': f([0, 0, 16, 16]), 'west': f([16, 0, 0, 16])})]
    elif plane == 'lance':
        els = [flat, q([8, 8 + 16 * a0, 8 - 16 * b1], [8, 8 + 16 * a1, 8 - 16 * b0],
                       {'east': f([0, 0, 16, 16], 90), 'west': f([0, 0, 16, 16], 270)})]
    elif plane == 'lancex':
        els = [flat, face]
    else:
        raise ValueError(plane)
    for e in els:
        for v in e['from'] + e['to']:
            assert -16 <= v <= 32, (kind, e)
    return {'ambientocclusion': False, 'textures': {'0': tex, 'particle': tex}, 'elements': els}


def item_json(kind, model=None):
    return {'model': {'type': 'minecraft:model', 'model': model or f'rlk:item/{TEXDIR}/{kind}',
                      'tints': [{'type': 'minecraft:custom_model_data', 'index': 0, 'default': WHITE}]}}


def atlas_px():
    """new px this kit adds to the items atlas: the sprites (api.KIT_SPRITES) + the gate icon"""
    return SPRITE_PX + GATE_PX


def rift_models_present(rp):
    rp = Path(rp)
    return all((rp / f'assets/rlk/models/item/rift/{v}.json').exists() for v in RIFT.values())


# ----------------------------------------------------------------------------- HUD font
CP_LO, CP_HI = api.FONT_RANGE
SP_NEG1 = 0xEC1F                       # a -1 advance space after a full-screen glyph (keeps it centred)
OVL_PX = api.OVERLAY_GLYPH             # (144, 81) texture px of the full-screen glyphs (16:9)
OVL_H, OVL_ASC = 144, 69               # glyph height / ascent (Apep's full-screen flashes)
GLYPHS = {
    # name -> (codepoint, painter (x right, y up, -1..1 over the 16:9 screen), texture px (w, h), height, ascent)
    'black': (api.OVERLAYS['black'], P.glyph_flat('#000000', 1.0), OVL_PX, OVL_H, OVL_ASC),
    'negative': (api.OVERLAYS['negative'], P.glyph_negative, OVL_PX, OVL_H, OVL_ASC),
    'pinkwhite': (api.OVERLAYS['pinkwhite'], P.glyph_pinkwhite, OVL_PX, OVL_H, OVL_ASC),
    'red_tint': (api.OVERLAYS['red_tint'], P.glyph_red_tint, OVL_PX, OVL_H, OVL_ASC),
    'magenta': (api.OVERLAYS['magenta'], P.glyph_flat('#E040A0', 0.55), OVL_PX, OVL_H, OVL_ASC),
    'white': (api.OVERLAYS['white'], P.glyph_flat('#FFFFFF', 0.92), OVL_PX, OVL_H, OVL_ASC),
    'vig': (api.VIG, P.glyph_vignette, OVL_PX, OVL_H, OVL_ASC),
}
assert {k: v[0] for k, v in GLYPHS.items() if k != 'vig'} == api.OVERLAYS and GLYPHS['vig'][0] == api.VIG
LINE_COL = api.LINE_COLOR              # #F2D0E8
LINE_GAP = 2                           # ticks per typing step (two syllables per step, Raiden)
LINE_FADE = 6                          # the last step fades over these ticks after its hold
SKIP_COLS = ('#A8A8B0', '#BEBEC5', '#D3D3D9', '#E9E9EC', '#FFFFFF')     # the prompt brightening in api.SKIP_STEPS steps
assert len(SKIP_COLS) == api.SKIP_STEPS + 1 and SKIP_COLS[0] == api.SKIP_COLOR
WARN_SPLIT = api.WARN_TEXT.index(api.WARN_HL[0])


def glyph(name):
    return chr(GLYPHS[name][0])


def _jstr(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def glyph_title(ch):
    """the SNBT title component of a full-screen glyph (string ch, may be a macro placeholder): an empty unstyled root,
    the glyph and the -1 space each naming the kit font, no text shadow"""
    return (f'{{text:"",extra:[{{text:"{ch}",font:"{FONT}",color:"white",shadow_color:0}},'
            f'{{text:"{chr(SP_NEG1)}",font:"{FONT}"}}]}}')


def warn_component():
    """api.WARN_TEXT in white with 「즉사」 in #FF3A55 (api.WARN_HL); an empty unstyled root, every part naming its font"""
    a = api.WARN_TEXT[:WARN_SPLIT]
    hl, col = api.WARN_HL
    b = api.WARN_TEXT[WARN_SPLIT + len(hl):]
    return (f'{{text:"",extra:[{{text:"{_jstr(a)}",color:"white",font:"minecraft:default"}},'
            f'{{text:"{_jstr(hl)}",color:"{col}",bold:true,font:"minecraft:default"}},'
            f'{{text:"{_jstr(b)}",color:"white",font:"minecraft:default"}}]}}')


def skip_component(s):
    """the intro's actionbar prompt at brightness step s: 「⊙ 건너뛰기」 (api.SKIP_TEXT, verbatim) brightening, the hint
    「 · Shift 길게」 (api.SKIP_HINT) grey"""
    return (f'{{text:"",extra:[{{text:"{_jstr(api.SKIP_TEXT)}",color:"{SKIP_COLS[s]}",font:"minecraft:default"}},'
            f'{{text:"{_jstr(api.SKIP_HINT)}",color:"{api.SKIP_COLOR}",font:"minecraft:default"}}]}}')


def paint_glyph(fn, w, h, ss=3):
    """screen-proportion painter: x and y both -1..1 over the w x h texture"""
    px = bytearray()
    for j in range(h):
        for i in range(w):
            ar = ag = ab = aa = 0.0
            for sj in range(ss):
                y = 1 - 2 * (j + (sj + 0.5) / ss) / h
                for si in range(ss):
                    x = -1 + 2 * (i + (si + 0.5) / ss) / w
                    r, g, b, a = fn(x, y)
                    ar, ag, ab, aa = ar + r * a, ag + g * a, ab + b * a, aa + a
            al = aa / (ss * ss)
            if aa <= 0 or al < 0.004:
                px += b'\x00\x00\x00\x00'
            else:
                px += bytes((round(255 * P.clamp01(ar / aa)), round(255 * P.clamp01(ag / aa)),
                             round(255 * P.clamp01(ab / aa)), round(255 * P.clamp01(al))))
    return px


def font_used_elsewhere(rp, own):
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


def font_json():
    providers = [{'type': 'bitmap', 'file': f'rlk:font/{FONT_NAME}/{name}.png', 'ascent': asc, 'height': hgt,
                  'chars': [chr(cp)]} for name, (cp, _p, _wh, hgt, asc) in GLYPHS.items()]
    providers.append({'type': 'space', 'advances': {chr(SP_NEG1): -1}})
    # every char the kit does not draw falls back to the default font (a component that inherits this font by mistake
    # still shows its text)
    providers.append({'type': 'reference', 'id': 'minecraft:default'})
    return {'providers': providers}


def build_font(rp):
    rp = Path(rp)
    tex = rp / f'assets/rlk/textures/font/{FONT_NAME}'
    font_path = rp / f'assets/rlk/font/{FONT_NAME}.json'
    ours = [g[0] for g in GLYPHS.values()] + [SP_NEG1]
    assert all(CP_LO <= c <= CP_HI for c in ours) and len(set(ours)) == len(ours)
    clash = font_used_elsewhere(rp, font_path)
    hit = [c for c in ours if c in clash]
    if hit:
        raise SystemExit(f'{FONT} glyphs collide with ' + ', '.join(f'U+{c:04X} ({clash[c]})' for c in hit))
    tex.mkdir(parents=True, exist_ok=True)
    for old in tex.glob('*'):
        if old.stem not in GLYPHS or old.suffix != '.png':
            old.unlink()
    for name, (cp, painter, (w, h), _height, _ascent) in GLYPHS.items():
        raw = paint_glyph(painter, w, h)
        rows = b''.join(b'\x00' + bytes(raw[y * w * 4:(y + 1) * w * 4]) for y in range(h))
        data = png_bytes(w, h, rows)
        p = tex / f'{name}.png'
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
    text = json.dumps(font_json(), ensure_ascii=False, indent=1) + '\n'
    font_path.parent.mkdir(parents=True, exist_ok=True)
    if not font_path.exists() or font_path.read_text(encoding='utf-8') != text:
        font_path.write_text(text, encoding='utf-8')
    return len(GLYPHS)


def build_resourcepack(rp):
    rp = Path(rp)
    px = atlas_px()
    for stem, ((w, h), _b, _f, _s) in TEXTURES.items():
        assert w <= 256 and h <= 256 and w % 16 == 0 and h % 16 == 0, (stem, w, h)
        assert re.fullmatch(r'[a-z0-9_]+', stem), stem
    s1 = rift_models_present(rp)
    n_glyphs = build_font(rp)
    root = rp / 'assets/rlk'
    tex_dir = root / f'textures/{TEXDIR}'
    dirs = {tex_dir: (TEXTURES, '.png'), root / f'models/item/{TEXDIR}': (KINDS, '.json'),
            root / f'items/{TEXDIR}': (ALL_KINDS, '.json')}
    for d, (keep, suf) in dirs.items():
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob('*'):
            if old.stem not in keep or old.suffix != suf:
                old.unlink()
    for stem in TEXTURES:
        w, h, raw = render(stem)
        data = png_bytes(w, h, raw)
        p = tex_dir / f'{stem}.png'
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)

    def put(p, obj):
        text = json.dumps(obj, separators=(',', ':')) + '\n'
        if not p.exists() or p.read_text(encoding='utf-8') != text:
            p.write_text(text, encoding='utf-8')
    for kind in KINDS:
        put(root / f'models/item/{TEXDIR}' / f'{kind}.json', model_json(kind))
        put(root / f'items/{TEXDIR}' / f'{kind}.json', item_json(kind))
    for kind, name in RIFT.items():
        put(root / f'items/{TEXDIR}' / f'{kind}.json',
            item_json(kind, RIFT_MODEL + name if s1 else f'rlk:item/{TEXDIR}/{RIFT_FALLBACK}'))
    atlaspath = rp / 'assets/minecraft/atlases/items.json'
    atlas = json.loads(atlaspath.read_text(encoding='utf-8')) if atlaspath.exists() else {'sources': []}
    atlas['sources'] = [s for s in atlas['sources'] if not str(s.get('resource', '')).startswith(NS_TEX)
                        or s['resource'][len(NS_TEX):] in TEXTURES]
    have = {s.get('sprite', s.get('resource')) for s in atlas['sources']}
    for stem in TEXTURES:
        if NS_TEX + stem not in have:
            atlas['sources'].append({'type': 'minecraft:single', 'resource': NS_TEX + stem})
    text = json.dumps(atlas, indent=2) + '\n'
    if not atlaspath.exists() or atlaspath.read_text(encoding='utf-8') != text:
        atlaspath.parent.mkdir(parents=True, exist_ok=True)
        atlaspath.write_text(text, encoding='utf-8')
    return len(TEXTURES), px, n_glyphs, s1


# ----------------------------------------------------------------------------- call builders


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


# pool -> (index, tag): fx (CAP_FX), ambient (CAP_AMB), afterimage (CAP_AI)
POOLS = {'fx': (0, f'{TAG}_c'), 'am': (1, f'{TAG}_a'), 'ai': (2, f'{TAG}_i')}
CAPS = {'fx': CAP_FX, 'am': CAP_AMB, 'ai': CAP_AI}
POOL_FP = {'fx': '#n', 'am': '#na', 'ai': '#ni'}


def card(kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8, fade=0,
         col=WHITE, dly=0, dur=0, hit=-1, col2=-1, off=None, pool='fx'):
    """The function line that spawns one card (fx/card, or fx/cardx when an extended option is used): pos / rot of the
    card (relative to the executor; rot may be absolute), billboard, roll (left_rotation about local z), spin over the
    main interpolation, s0 -> s1 (float or (x, y, z)), off (static start translation) + move (its end translation: off
    + move), life / fade ticks, col tint, dly hidden ticks, dur main-interpolation ticks (0 = to the fade), hit / col2 the
    second tint, pool 'fx' / 'am' (ambient) / 'ai' (afterimage). Any value may be a macro placeholder such as '$(r)'."""
    assert kind in ALL_KINDS, kind
    assert bb in ('fixed', 'center', 'vertical', 'horizontal'), bb
    assert pool in POOLS, pool
    if all(isinstance(v, int) for v in (life, fade, dur)) and dur > life - fade - 1:
        life = dur + fade + 1              # the main interpolation always completes before the fade starts
    uni = (int, float, str)
    simple = (isinstance(s0, uni) and isinstance(s1, uni) and not dly and not dur and hit == -1 and off is None
              and pool == 'fx')
    if off is not None and all(isinstance(x, (int, float)) for x in tuple(off) + tuple(move)):
        end = tuple(a + b for a, b in zip(off, move))
    else:
        end = tuple(move)
    mv = vec(end)
    if simple:
        return (f'function {FN}card {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
                f'spin:{_i(spin)},s0:{_f(s0)},s1:{_f(s1)},move:"{mv}",life:{_i(life)},'
                f'fade:{_i(fade)},col:{_i(col)}}}')
    pl, tg = POOLS[pool]
    return (f'function {FN}cardx {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
            f'spin:{_i(spin)},s0:"{vec(s0)}",s1:"{vec(s1)}",off:"{vec(off if off is not None else (0, 0, 0))}",'
            f'move:"{mv}",life:{_i(life)},fade:{_i(fade)},col:{_i(col)},dly:{_i(dly)},dur:{_i(dur)},hit:{_i(hit)},'
            f'col2:{_i(col2)},pl:{pl},tg:"{tg}"}}')


# ----------------------------------------------------------------------------- particles (vanilla; 26.3 ids)


def colour_list(c):
    if isinstance(c, int):
        c = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
    return '[' + ','.join(num(float(x), 3) + 'f' for x in c) + ']'


def _d(v):
    return v if isinstance(v, str) else num(float(v), 3)


def part(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    d = ' '.join(_d(v) for v in delta)
    return f'particle minecraft:{name} {pos} {d} {num(float(speed), 3)} {_i(n)} force @a[tag=player]'


def dust(c, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1, speed=0.0):
    return part(f'dust{{color:{colour_list(c)},scale:{num(float(scale), 2)}}}', pos, delta, speed, n)


def blockp(block, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    return part(f'block{{block_state:"minecraft:{block}"}}', pos, delta, speed, n)


def c_parts(c, pos='~ ~ ~', delta=(0.3, 0.3, 0.3), n=8):
    """the colour's particle signature: dust of colour c + electric sparks (her Electro) for the sword-qi colours, end
    rods for the yellow / white ones"""
    out = [dust(DUSTC[c], 1.1, pos, delta, n)]
    if c in (api.C_YELLOW, api.C_WHITE):
        out.append(part('end_rod', pos, delta, 0.02, max(1, n // 4)))
    else:
        out.append(part('electric_spark', pos, delta, 0.05, max(1, n // 3)))
    return out


# ----------------------------------------------------------------------------- sound recipes (api.KIT_SOUND_RECIPES)
SOUNDS = dict(api.KIT_SOUND_RECIPES)
assert tuple(SOUNDS) == tuple(api.KIT_SOUNDS)


def sound_line(event, vol, pitch):
    return L.sound(event, vol, pitch)


# ----------------------------------------------------------------------------- presets (api.KIT_PRESETS)
# name -> (doc, args, fn, conv, split_c, pre, pool). A preset with arguments is a public macro p/<name> that turns its
# arguments into storage rlk:hr fx.pa (conv: [(key, src, scale or None (int x 1), add, frac)], src = a macro arg or a
# '#score' of hrFx) and runs p/e/<name>[_<c>] with that storage; pre = lines run before the conv (floor clamps).
PRESETS = {}
PA = f'{STO} fx.pa'
AMBIENT = ('ambient_p1', 'ambient_p2', 'petals_drift', 'petals_wind', 'petals_heart', 'motes_warm', 'leaves_dark',
           'leaves_swirl')
PTCL = ('dust_ring', 'ev_trail', 'ev_petals', 'ev_leave', 'ev_beam', 'ev_wind', 'ev_palm', 'ev_take', 'ambient_p2')


def preset(name, doc, conv=(), split_c=False, pre=()):
    args = api.KIT_PRESETS[name]

    def deco(f):
        PRESETS[name] = (doc, list(args), f, list(conv), split_c, list(pre))
        return f
    return deco


def ang(deg):
    return num(float(deg), 2)


def radial(n, start=0.0):
    return [start + 360.0 * k / n for k in range(n)]


def xz(r, yaw):
    """^x ^z offsets of the point at radius r, yaw degrees to the executor's right"""
    return -r * math.sin(math.radians(yaw)), r * math.cos(math.radians(yaw))


def fly(kind, yaw, el, dist, h=0.0, s0=0.5, s1=1.0, life=8, fade=3, col=WHITE, dly=0, roll=0, dur=0, pos=None, spin=0,
        pool='fx', bb='fixed'):
    """the fg radial trick: a fixed face card whose local +y points out along (yaw, elevation) flies dist outward
    (el 0..90: the game clamps an entity's pitch to [-90, 90])."""
    assert 0 <= el <= 90, (kind, el)
    return card(kind, pos or f'~ ~{num(h, 2)} ~', f'~{ang(yaw)} {ang(90 - el)}', roll=roll, s0=s0, s1=s1,
                move=(0, dist if isinstance(dist, str) else round(dist, 2), 0), life=life, fade=fade, col=col, dly=dly,
                dur=dur, spin=spin, pool=pool, bb=bb)


def inward(kind, yaw, r, h, dist, s0=0.5, s1=0.3, life=10, fade=3, col=WHITE, dly=0, dur=0):
    """a fixed face card at radius r (bearing yaw, height h) flying dist toward the centre"""
    x, z = xz(r, yaw)
    return card(kind, f'^{num(x, 3)} ^{num(h, 2)} ^{num(z, 3)}', f'~{ang(yaw + 180)} 90', s0=s0, s1=s1,
                move=(0, round(dist, 2), 0), life=life, fade=fade, col=col, dly=dly, dur=dur)


def mac(line):
    return '$' + line


RND = random.Random

# --- the floor clamp of the crescents ----------------------------------------------------------------------------------
# fx/e/hgt: #h = the executor's height over the floor (hundredths; storage fx.fl = floor y x 100, the arena's by default)
# and #pt = the executor's pitch (degrees, Minecraft: + down). The crescents: LOW[ip * 36 + ir] = the lowest point of
# the arc (bearings +-80 deg from the aim, unit radius) below the pivot, per mille, for the pitch cell ip (centre
# -90 + 10 ip, Minecraft pitch) and roll cell ir (centre -180 + 10 ir), the max over the cell; the reach is clamped to
# 100 (h - 10 + lift) / LOW (tenths) so no frame reaches below the floor.
ARC_BEAR = 80.0
ARC_LIFT = 100                         # hundredths: a low crescent rises up to 1 b before it shrinks


def arc_low(p, ro):
    pr, rr = math.radians(p), math.radians(ro)
    A = math.sin(rr) * math.cos(pr)            # the y component of the card's a axis (rolled about the aim)
    B = -math.sin(pr)                          # the aim's y component (Minecraft pitch: down = positive)
    lo = 0.0
    for k in range(0, 161):
        phi = math.radians(90 - ARC_BEAR + k * (2 * ARC_BEAR) / 160)
        lo = min(lo, A * math.cos(phi) + B * math.sin(phi))
    return -lo


def _low_table():
    out = []
    for ip in range(19):
        for ir in range(36):
            pc, rc = -90 + 10 * ip, -180 + 10 * ir
            m = 0.0
            for dp in range(-5, 6):
                for dr in range(-5, 6):
                    m = max(m, arc_low(max(-90, min(90, pc + dp)), rc + dr))
            out.append(int(math.ceil(m * 1000)))
    return out


LOW = _low_table()
SIN = [round(1000 * math.sin(math.radians(d))) for d in range(91)]
# the crescents' pitch arg is an elevation (+ up): #p = - pitch (Minecraft) for the clamp, storage pa.p the card pitch
ARC_CLAMP = [f'$data modify storage {PA}.yaw set value $(yaw)', f'$data modify storage {PA}.roll set value $(roll)',
             '$scoreboard players set #r hrFx $(r)', '$scoreboard players set #p hrFx $(pitch)',
             'scoreboard players operation #p hrFx *= #cm1 hrFx', '$scoreboard players set #o hrFx $(roll)',
             f'execute store result storage {PA}.p int 1 run scoreboard players get #p hrFx',
             f'function {FN}e/clamp_arc']
QI_CONV = (('s', '#r', 0.1), ('s9', '#r', 0.09), ('f', '#r', 0.08), ('pd', '#r', 0.025), ('ly', '#ly', 0.01))
ARC_LIFE = (2, 2, 2, 8)


def qi_frames(c, pos, rot, roll, s0, s1, flip=False, life=ARC_LIFE, fade_last=6):
    """the four crescent sweep frames (1 t apart; the last fades), tinted for colour c"""
    out = []
    for k in range(4):
        fr = 3 - k if flip else k
        out.append(mac(card(f'qi_arc_{fr}', pos, rot, roll=roll, s0=s0, s1=s1, life=life[k], fade=fade_last if k == 3 else 0,
                            dly=k, dur=2, col=QTINT[c], hit=k + 3 if k == 3 else -1, col2=QFADE[c] if k == 3 else -1)))
    return out


# --- sword-qi ---------------------------------------------------------------------------------------------------------------
@preset('qi_arc', 'A sword-qi crescent of reach {r} (tenths) about the executor (S3: the body + 1.0, rotated as the body; S4: '
        'the cut spot + h, rotated as the player; S2b: at her): {yaw} / {pitch} the aim\'s offsets from the executor rotation '
        '(yaw + = right, pitch + = up), {roll} the blade plane about the aim (0 a flat crescent, 90 vertical). Four sweep frames '
        '1 t apart (the last fades over 6 t): the lilac body, the white-pink cutting rim; c tints it (1 lilac .. 5 white). '
        'A crescent that would reach below the floor rises up to 1 b, then shrinks (fx/e/clamp_arc): no frame below the floor.',
        conv=QI_CONV, split_c=True, pre=ARC_CLAMP)
def _p_qi_arc(c):
    out = qi_frames(c, '^ ^$(ly) ^', '~$(yaw) ~$(p)', '$(roll)', ('$(s9)', 1, '$(s9)'), ('$(s)', 1, '$(s)'))
    front = 'positioned ^ ^$(ly) ^ rotated ~$(yaw) ~$(p) positioned ^ ^ ^$(f)'
    out += [mac(f'execute {front} run ' + l) for l in c_parts(c, '~ ~ ~', ('$(pd)', 0.2, '$(pd)'), 12)]
    return out


@preset('qi_ring', 'A flat sword-qi ring of radius {r} (tenths) about the executor (S3: the body + 0.8 / 1.55; S4: the cut '
        'spot + 0.8 / 0.1; the vanish: the body + 0.8), horizontal: the lilac ring spreading and turning, a white-pink rim ring '
        'behind it, particles round its edge; c tints it.',
        conv=(('s', 'r', 0.1), ('s3', 'r', 0.035), ('s5', 'r', 0.05), ('sr', 'r', 0.108), ('pd', 'r', 0.055)), split_c=True)
def _p_qi_ring(c):
    return [mac(card('qi_ring_0', '^ ^ ^', '~ 0', spin=150, s0=('$(s3)', 1, '$(s3)'), s1=('$(s)', 1, '$(s)'), life=9, fade=4,
                     dur=4, col=QTINT[c])),
            mac(card('qi_ring_1', '^ ^0.05 ^', '~45 0', spin=-130, s0=('$(s5)', 1, '$(s5)'), s1=('$(sr)', 1, '$(sr)'), life=8,
                     fade=4, dly=1, dur=4, col=QTINT[c]))] + \
        [mac(l) for l in c_parts(c, '~ ~0.1 ~', ('$(pd)', 0.05, '$(pd)'), 16)]


@preset('qi_band', 'A broad sword-qi band of length {len} (tenths) across the aim, centred on the executor (S4 A8.2: the cut spot '
        '+ 0.3, rotated as the player; S2b CS4 E1b: her + 1.1 facing the player): an upright sheet whose long axis runs to the '
        'aim\'s left and right, rising by {pitch} degrees toward its right end, {roll} leaning its top forward; {yaw} turns '
        'the aim. It sweeps 2.5 b forward along the aim over 6 t and fades (lilac, the white-pink upper rim). '
        'Near the floor it rises (fx/e/clamp_band) so no part of it reaches below the floor; under a lean the sweep stays '
        'level.',
        conv=(('l', 'len', 0.1), ('hy', 'len', 0.06), ('q', 'len', 0.025), ('mq', 'len', -0.025), ('ly', '#ly', 0.01),
              ('my', '#my', 0.01), ('mz', '#mz', 0.01), ('ny', '#ny', 0.01), ('nz', '#nz', 0.01)),
        pre=['$scoreboard players set #a hrFx $(pitch)', 'scoreboard players operation #a hrFx *= #cm1 hrFx',
             f'execute store result storage {PA}.tl int 1 run scoreboard players get #a hrFx',
             f'$data modify storage {PA}.yaw set value $(yaw)', f'$data modify storage {PA}.roll set value $(roll)',
             '$scoreboard players set #l hrFx $(len)', '$scoreboard players set #p hrFx $(pitch)',
             '$scoreboard players set #o hrFx $(roll)', f'function {FN}e/clamp_band'])
def _p_qi_band():
    return [mac(card('qi_band_0', '^ ^$(ly) ^', '~$(yaw) $(roll)', roll='$(tl)', s0=('$(l)', '$(hy)', 1),
                     s1=('$(l)', '$(hy)', 1), off=(0, 0, 0), move=(0, '$(my)', '$(mz)'), life=10, fade=4, dur=6)),
            mac(card('qi_band_1', '^ ^$(ly) ^', '~$(yaw) $(roll)', roll='$(tl)', s0=('$(l)', '$(hy)', 1),
                     s1=('$(l)', '$(hy)', 1), off=(0, 0, 0), move=(0, '$(ny)', '$(nz)'), life=6, fade=3, dur=4)),
            mac('execute rotated ~$(yaw) 0 run ' + dust(DUSTC[1], 1.1, '^$(q) ^$(ly) ^1', (0.3, 0.3, 0.3), 8)),
            mac('execute rotated ~$(yaw) 0 run ' + dust(DUSTC[1], 1.1, '^$(mq) ^$(ly) ^1', (0.3, 0.3, 0.3), 8)),
            mac('execute rotated ~$(yaw) 0 run ' + part('electric_spark', '^ ^$(ly) ^1.2', (0.5, 0.3, 0.5), 0.05, 4))]


@preset('qi_x', 'The X of two crossed sword-qi slashes of reach {r} (tenths) lying flat at the executor (S4 A8.5: the cut spot + '
        '0.1, rotated as the player: a hit effect at the contact tick, never shown before it): two flattened crescents at '
        '+-45 deg crossing on the executor, lilac.',
        conv=(('s', 'r', 0.1), ('s9', 'r', 0.085), ('sb', 'r', 0.045), ('o', 'r', -0.022), ('pd', 'r', 0.04)))
def _p_qi_x():
    out = []
    for k, y in enumerate((45, -45)):
        out.append(mac(card('qi_arc_3', '^ ^ ^', f'~{y} 0', s0=('$(s9)', 1, '$(sb)'), s1=('$(s)', 1, '$(sb)'),
                            off=(0, 0, '$(o)'), move=(0, 0, '$(o)'), life=10, fade=5, dly=k, dur=2, col=WHITE, hit=6,
                            col2=QFADE[1])))
    return out + [mac(dust(DUSTC[1], 1.2, '~ ~0.2 ~', ('$(pd)', 0.05, '$(pd)'), 20)),
                  part('electric_spark', '~ ~0.3 ~', (0.8, 0.1, 0.8), 0.05, 6)]


@preset('qi_dome', 'A8.7 the spin dome of radius {r} (tenths) at the executor (S4: the cut spot on the floor): the white-pink rim '
        'ring at waist height (+0.9 b) turning out, and a translucent lilac dome that expands from the floor to radius r, '
        'turns into a thin white outline and fades.',
        conv=(('s', 'r', 0.1), ('s4', 'r', 0.04), ('s5', 'r', 0.05), ('pd', 'r', 0.05), ('ph', 'r', 0.05)))
def _p_qi_dome():
    return [mac(card('qi_ring_1', '^ ^0.9 ^', '~ 0', spin=140, s0=('$(s4)', 1, '$(s4)'), s1=('$(s)', 1, '$(s)'), life=10,
                     fade=5, dur=4)),
            mac(card('qi_dome', '~ ~ ~', bb='vertical', s0=('$(s5)', '$(s5)', 1), s1=('$(s)', '$(s)', 1), life=12, fade=4,
                     dur=5, hit=6, col2=PINKW)),
            mac(dust(DUSTC[5], 1.0, '~ ~$(ph) ~', ('$(pd)', '$(ph)', '$(pd)'), 20)),
            part('end_rod', '~ ~1 ~', (1.2, 0.8, 1.2), 0.02, 6)]


@preset('qi_vert', 'A vertical sword-qi crescent of height {h} (tenths) standing on the executor (S3 A3: the body + 0.15, 1.4 '
        'ahead; S4 A8.8: the cut spot on the floor, rotated as the player): the crescent in the vertical plane along the aim '
        '(executor yaw + {yaw}), from the executor up to h, the sweep rising (four frames), and a thin glowing upright line '
        'at its foot facing the viewer; c tints it (A8.8: 2 magenta).',
        conv=(('hh', 'h', 0.0616), ('s', 'h', 0.0625), ('s9', 'h', 0.055), ('hl', 'h', 0.1), ('pd', 'h', 0.05)), split_c=True,
        pre=[f'$data modify storage {PA}.yaw set value $(yaw)'])
def _p_qi_vert(c):
    out = qi_frames(c, '^ ^$(hh) ^', '~$(yaw) 0', -90, ('$(s9)', 1, '$(s9)'), ('$(s)', 1, '$(s)'))
    out.append(mac(card('col_face', '~ ~ ~', bb='vertical', s0=(2.0, '$(hl)', 2.0), s1=(3.2, '$(hl)', 3.2), life=6, fade=3,
                        dur=2, col=TINT[c] if c != 1 else LILAC_PALE)))
    out += [mac('execute rotated ~$(yaw) 0 run ' + l) for l in c_parts(c, '^ ^$(hh) ^0.6', (0.15, '$(pd)', 0.15), 14)]
    return out


@preset('qi_fan', 'A rising vertical fan of sword-qi of height {h} (tenths) centred on the executor (S3 A1: the body + 0.85, 1.2 b '
        'ahead; cosmetic): the four sweep frames in the vertical plane along the executor\'s facing, rising; c tints it (A1: 2).',
        conv=(('s', 'h', 0.0625), ('s9', 'h', 0.055), ('pd', 'h', 0.04)), split_c=True)
def _p_qi_fan(c):
    out = qi_frames(c, '^ ^ ^', '~ 0', -90, ('$(s9)', 1, '$(s9)'), ('$(s)', 1, '$(s)'), life=(2, 2, 2, 6), fade_last=4)
    out += [mac(l) for l in c_parts(c, '^ ^ ^0.5', ('$(pd)', '$(pd)', 0.1), 10)]
    return out


@preset('qi_wedge', 'A sword-qi wedge of length {r} (tenths) from the executor along its facing (S3 A3 h5: the body + 1.0; S4 A7: '
        'the body + 0.85), rolled {roll} degrees about the aim (the rising diagonal): a lilac spearhead widening behind its point, '
        'white edges; particles at the point.',
        conv=(('s', 'r', 0.1), ('s6', 'r', 0.06), ('pd', 'r', 0.03)), pre=[f'$data modify storage {PA}.roll set value $(roll)'])
def _p_qi_wedge():
    return [mac(card('qi_wedge', '^ ^ ^', '~ 0', roll='$(roll)', s0=('$(s6)', 1, '$(s6)'), s1=('$(s)', 1, '$(s)'), life=8,
                     fade=4, dur=2, hit=5, col2=QFADE[1])),
            mac(dust(DUSTC[1], 1.2, '^ ^ ^$(s)', ('$(pd)', '$(pd)', '$(pd)'), 10)),
            mac(part('electric_spark', '^ ^ ^$(s)', (0.2, 0.2, 0.2), 0.05, 4))]


@preset('qi_ribbon', 'A4 the sword-qi ribbon wrapping round her (S3: the body + 1.0): three lilac ribbon strips tilted at '
        'different angles turning round her (one fading), lilac motes swirling.')
def _p_qi_ribbon():
    out = []
    for k, (y, p, ro, sp, kd) in enumerate(((0, -18, 25, 170, 'qi_ribbon_0'), (120, 14, -30, -160, 'qi_ribbon_1'),
                                           (240, -6, 12, 150, 'qi_ribbon_0'))):
        out.append(card(kd, '^ ^ ^', f'~{y} {p}', roll=ro, spin=sp, s0=1.2, s1=1.5, life=9, fade=4, dly=k, dur=5))
    return out + [dust(DUSTC[1], 1.0, '~ ~ ~', (0.9, 0.7, 0.9), 16), part('electric_spark', '~ ~ ~', (0.7, 0.6, 0.7), 0.05, 5)]


QLINE_CLAMP = [f'function {FN}e/hgt', '$scoreboard players set #r hrFx $(len)', f'function {FN}e/clamp_line']


@preset('qi_line', 'A thin straight sword-qi line of length {len} (tenths) from the executor along its full facing (pitch '
        'counts: S3 A5 the body + 0.95, 1.5 b ahead, level; S4 A8.9 the dive line: her + 0.8, rotated ~ 90 = straight down): a '
        'white core inside a lilac glow; a line pointing down is clamped to end above the floor.',
        conv=(('l', '#r', 0.1),), pre=QLINE_CLAMP)
def _p_qi_line():
    return [mac(card('qline', '^ ^ ^', '~ ~', s0=(0.05, 0.05, '$(l)'), s1=(0.18, 0.18, '$(l)'), life=4, fade=2, dur=1,
                     col=rgb('#F6E8FF'))),
            mac(card('qline', '^ ^ ^', '~ ~', s0=(0.25, 0.25, '$(l)'), s1=(0.6, 0.6, '$(l)'), life=4, fade=2, dur=1, col=LILAC)),
            dust(DUSTC[5], 0.8, '^ ^ ^0.3', (0.05, 0.05, 0.05), 3)]


@preset('qi_cut', 'A9 the iai cut along the dash: a long pink-magenta slash line of length {len} (tenths) from the executor along '
        'its yaw (S3: the dash start + 0.8, rotated along the dash), a white-hot core, magenta sparks along it.',
        conv=(('l', 'len', 0.1), ('p1', 'len', 0.033), ('p2', 'len', 0.066), ('p3', 'len', 0.095)))
def _p_qi_cut():
    return [mac(card('qline', '^ ^ ^', '~ 0', s0=(0.4, 0.4, '$(l)'), s1=(0.9, 0.9, '$(l)'), life=7, fade=4, dur=1,
                     col=MAGENTA)),
            mac(card('qline', '^ ^ ^', '~ 0', s0=(0.1, 0.1, '$(l)'), s1=(0.25, 0.25, '$(l)'), life=6, fade=3, dur=1,
                     col=rgb('#FFE6F4'))),
            mac(dust(DUSTC[2], 1.3, '^ ^ ^$(p1)', (0.3, 0.2, 0.3), 8)), mac(dust(DUSTC[2], 1.3, '^ ^ ^$(p2)', (0.3, 0.2, 0.3), 8)),
            mac(dust(DUSTC[2], 1.3, '^ ^ ^$(p3)', (0.3, 0.2, 0.3), 8)),
            mac(part('sweep_attack', '^ ^ ^$(p2)', (0.4, 0.1, 0.4), 0, 2))]


# --- glints, the yellow tell ------------------------------------------------------------------------------------------------
@preset('glint', 'A blade glint at the executor (the blade_tip / hat_crown / chest anchors): a four-ray sparkle flaring and '
        'turning, a smaller one crossing it; c tints it (1 lilac, 2 pink-magenta, 3 yellow, 4 crimson, 5 white).', split_c=True)
def _p_glint(c):
    return [card('glint_0', '~ ~ ~', bb='center', spin=90, s0=0.2, s1=1.1, life=6, fade=3, col=TINT[c]),
            card('glint_0', '~ ~ ~', bb='center', roll=45, spin=-60, s0=0.15, s1=0.6, life=5, fade=2, col=WHITE)] + \
        c_parts(c, '~ ~ ~', (0.08, 0.08, 0.08), 4)


@preset('star4', 'A9 the four-point star in a thin circle at her chest (the chest anchor, facing the viewer, 1.3 b): lilac, a '
        'white glint inside, for 6 t.')
def _p_star4():
    return [card('glint_1', '~ ~ ~', bb='center', spin=30, s0=0.6, s1=1.3, life=6, fade=2, col=LILAC_PALE),
            card('glint_0', '~ ~ ~', bb='center', s0=0.3, s1=0.8, life=5, fade=2, col=WHITE),
            dust(DUSTC[1], 1.0, '~ ~ ~', (0.3, 0.3, 0.3), 6)]


@preset('yellow_tell', 'The yellow tell for {t} ticks at the executor (S3 A9 / A10: the body + 1.0, in the air for A10; S4 A7: '
        'her): the yellow sphere (1.6 b) and the horizontal flare line through it (4 b), yellow motes.',
        conv=(('t', 't', None),))
def _p_yellow_tell():
    return [mac(card('yellow_tell_0', '~ ~ ~', bb='center', s0=0.4, s1=1.6, life='$(t)', fade=2, dur=3)),
            mac(card('yellow_tell_1', '~ ~ ~', bb='center', s0=(0.6, 1.0, 1.0), s1=(2.0, 1.4, 1.0), life='$(t)', fade=2, dur=3)),
            dust(DUSTC[3], 1.4, '~ ~ ~', (0.5, 0.5, 0.5), 12), part('end_rod', '~ ~ ~', (1.2, 0.05, 0.05), 0.0, 6)]


# --- the ghost ---------------------------------------------------------------------------------------------------------------
@preset('ghost_burst', 'The lilac switch / the vanish (the body + 0.8-1.1): the body bursts into lilac-white mist (four puffs '
        'flung out), white-lilac ribbons tracing the silhouette rise, sparkles linger to 12 t.')
def _p_ghost_burst():
    rnd = RND(13)
    out = [fly('ghost_burst_0', yaw, rnd.uniform(15, 45), rnd.uniform(0.7, 1.2), s0=0.7, s1=1.5, life=10, fade=5, bb='center')
           for yaw in radial(4, 20)]
    out += [card('ghost_burst_1', '~ ~ ~', bb='center', s0=1.0, s1=1.7, move=(0, 0.6, 0), life=9, fade=5, dur=4),
            card('ghost_burst_2', '~ ~0.2 ~', bb='center', s0=1.0, s1=1.6, life=12, fade=6, dly=2, dur=6)]
    return out + [dust(DUSTC[1], 1.2, '~ ~ ~', (0.4, 0.8, 0.4), 20), dust(DUSTC[5], 0.9, '~ ~ ~', (0.4, 0.8, 0.4), 10),
                  part('end_rod', '~ ~ ~', (0.3, 0.7, 0.3), 0.04, 8)]


@preset('ghost_trail', 'A ghost dash / glide / run (S4: the body + 0.45-0.95, rotated toward its target, at the move\'s start): a '
        'lilac flame trail and white speed lines along the aim over {len} (tenths), drawn out over 4 t as she passes, fading '
        'after 12 t; lilac motes along it.',
        conv=(('l', 'len', 0.1), ('l1', 'len', 0.012), ('p1', 'len', 0.033), ('p2', 'len', 0.066), ('p3', 'len', 0.1)))
def _p_ghost_trail():
    return [mac(card('ghost_trail_0', '^ ^ ^', '~-90 0', s0=('$(l1)', 2.8, 2.8), s1=('$(l)', 2.8, 2.8), life=12, fade=6,
                     dur=4)),
            mac(card('ghost_trail_1', '^ ^0.2 ^', '~-90 0', s0=('$(l1)', 3.1, 3.1), s1=('$(l)', 3.1, 3.1), life=8, fade=4,
                     dur=4)),
            mac(dust(DUSTC[1], 1.1, '^ ^ ^$(p1)', (0.2, 0.3, 0.2), 6)), mac(dust(DUSTC[1], 1.1, '^ ^ ^$(p2)', (0.2, 0.3, 0.2), 6)),
            mac(dust(DUSTC[1], 1.1, '^ ^ ^$(p3)', (0.2, 0.3, 0.2), 6))]


@preset('ghost_flash', 'D3 the flash-blink (the body + 0.95): a white-violet electric flash, sparks.')
def _p_ghost_flash():
    return [card('ghost_flash', '~ ~ ~', bb='center', spin=40, s0=0.6, s1=1.9, life=5, fade=2, dur=2),
            part('electric_spark', '~ ~ ~', (0.4, 0.8, 0.4), 0.1, 12), dust(DUSTC[5], 1.0, '~ ~ ~', (0.3, 0.7, 0.3), 8)]


AI_CLAMP = [f'function {FN}e/hgt', 'scoreboard players set #m hrFx -120', 'scoreboard players operation #a hrFx = #h hrFx',
            'scoreboard players operation #a hrFx *= #cm1 hrFx', 'scoreboard players operation #m hrFx > #a hrFx',
            'scoreboard players operation #s hrFx = #m hrFx', 'scoreboard players add #s hrFx 120']


@preset('afterimage', 'One translucent lilac silhouette of her at the executor (S3: the body + 1.2; S2b: her feet: the card '
        'stands 1.2 b below the executor, never below the floor), turned to the viewer, fading over 6 t (at most 4 alive: the '
        'ager removes the oldest), and a lilac streak of {len} (tenths) behind her along her facing.',
        conv=(('oy', '#m', 0.01), ('sy', '#s', 0.01), ('l', 'len', 0.1)), pre=AI_CLAMP)
def _p_afterimage():
    return [mac(card('afterimage', '~ ~$(oy) ~', bb='vertical', s0=2.65, s1=2.65, life=api.AFTERIMAGE_FADE, fade=2, hit=3,
                     col=WHITE, col2=rgb('#B898C8'), pool='ai')),
            mac(card('qline', '^ ^$(sy) ^', '~180 0', s0=(0.12, 0.12, '$(l)'), s1=(0.04, 0.04, '$(l)'), life=6, fade=3,
                     col=LILAC)),
            mac(dust(DUSTC[1], 1.0, '~ ~$(sy) ~', (0.25, 0.6, 0.25), 6))]


@preset('blink_bubble', 'A6 the back-blink (the body + 1.0): a pale blue-white translucent bubble swelling and gone, white motes.')
def _p_blink_bubble():
    return [card('blink_bubble', '~ ~ ~', bb='center', s0=1.4, s1=2.4, life=7, fade=3, dur=3),
            part('end_rod', '~ ~ ~', (0.6, 0.8, 0.6), 0.03, 10), part('snowflake', '~ ~ ~', (0.6, 0.8, 0.6), 0.02, 6)]


# --- the shield --------------------------------------------------------------------------------------------------------------
@preset('shield_refill', 'The lead-ins\' refill beat (at her, the body + 1.1): eight lilac crystal shards fly in to her and a '
        'flash closes them, a thin rim ring.')
def _p_shield_refill():
    out = [inward('shards_0', yaw, 1.8, 0.4 * ((k % 3) - 1), 1.6, s0=0.5, s1=0.25, life=8, fade=2, col=LILAC_PALE, dly=k % 2,
                  dur=6) for k, yaw in enumerate(radial(8, 10))]
    out += [card('glint_0', '~ ~ ~', bb='center', s0=0.4, s1=1.6, life=5, fade=2, dly=6, col=WHITE),
            card('qi_ring_1', '^ ^ ^', '~ 0', spin=120, s0=0.4, s1=1.0, life=7, fade=3, dly=6, dur=3)]
    return out + [part('end_rod', '~ ~ ~', (0.8, 0.8, 0.8), 0.02, 8), dust(DUSTC[1], 1.0, '~ ~ ~', (0.8, 0.8, 0.8), 10)]


@preset('pip_break', 'A pip removed (at the player\'s chest): lilac shards burst out, a white flash, amethyst chips, sparks.')
def _p_pip_break():
    rnd = RND(29)
    out = [fly('shards_1', yaw, rnd.uniform(0, 50), rnd.uniform(1.0, 1.6), s0=0.35, s1=0.5, life=9, fade=4, col=LILAC_PALE,
               roll=rnd.randint(-60, 60)) for yaw in radial(8, 15)]
    out += [card('glint_0', '~ ~ ~', bb='center', s0=0.5, s1=1.4, life=4, fade=2, col=WHITE)]
    return out + [blockp('amethyst_block', '~ ~ ~', (0.3, 0.3, 0.3), 0.1, 12), part('electric_spark', '~ ~ ~', (0.3, 0.3, 0.3), 0.1, 6)]


# --- impacts, columns, streaks -----------------------------------------------------------------------------------------------
@preset('dive_impact', 'A dive landing of radius {r} (tenths) at the executor (S3 A4: the lock + 0.1; S4 the A8 fail: the '
        'impact point): a flat lilac shock ring with radial spikes spreading (a hit effect at the contact tick), the rim ring, '
        'a white flash, lilac dust and sparks.',
        conv=(('s', 'r', 0.1), ('s2', 'r', 0.025), ('s3', 'r', 0.03), ('sr', 'r', 0.115), ('pd', 'r', 0.04)))
def _p_dive_impact():
    return [mac(card('dive_impact', '^ ^ ^', '~ 0', spin=40, s0=('$(s2)', 1, '$(s2)'), s1=('$(s)', 1, '$(s)'), life=10, fade=5,
                     dur=4)),
            mac(card('qi_ring_1', '^ ^0.05 ^', '~30 0', spin=-90, s0=('$(s3)', 1, '$(s3)'), s1=('$(sr)', 1, '$(sr)'), life=9,
                     fade=4, dly=1, dur=4)),
            card('glint_0', '~ ~0.6 ~', bb='center', s0=0.8, s1=2.4, life=4, fade=2, col=WHITE),
            mac(dust(DUSTC[1], 1.4, '~ ~0.2 ~', ('$(pd)', 0.1, '$(pd)'), 30)),
            part('electric_spark', '~ ~0.3 ~', (0.8, 0.2, 0.8), 0.1, 10), part('explosion', '~ ~0.4 ~', (0, 0, 0), 0, 1)]


@preset('burst_radial', 'A10 the landing burst of radius {r} (tenths) at the executor (the lock + 0.1): the lilac shock ring turning '
        'the other way, six claw streaks flung out radially, motes rising.',
        conv=(('s', 'r', 0.1), ('s3', 'r', 0.03), ('d', 'r', 0.075), ('pd', 'r', 0.04)))
def _p_burst_radial():
    out = [mac(card('dive_impact', '^ ^ ^', '~ 0', spin=-60, s0=('$(s3)', 1, '$(s3)'), s1=('$(s)', 1, '$(s)'), life=9, fade=4,
                    dur=4))]
    out += [mac(fly('claw_streaks', yaw, 25, '$(d)', h=0.3, s0=0.6, s1=1.0, life=8, fade=3)) for yaw in radial(6, 0)]
    return out + [mac(dust(DUSTC[1], 1.3, '~ ~0.3 ~', ('$(pd)', 0.2, '$(pd)'), 24)),
                  part('end_rod', '~ ~0.5 ~', (0.3, 1.0, 0.3), 0.05, 10)]


@preset('light_column', 'A lilac light column from the executor (the player\'s spot on the floor: the deflect, the A8 fail) up 9 b: '
        'two crossed glowing quads widening, a white core, motes rising.')
def _p_light_column():
    return [card('light_column', '~ ~ ~', bb='fixed', s0=(2.4, 2.0, 2.4), s1=(6.0, 9.0, 6.0), life=14, fade=8, dur=3,
                 col=rgb('#E8C8FF')),
            card('light_column', '~ ~ ~', '~45 0', s0=(0.8, 2.0, 0.8), s1=(2.0, 9.5, 2.0), life=12, fade=6, dur=3, col=WHITE),
            part('end_rod', '~ ~1 ~', (0.2, 2.0, 0.2), 0.05, 16), dust(DUSTC[1], 1.2, '~ ~2 ~', (0.3, 2.0, 0.3), 14)]


CLAW_PTS = [(-0.45, 0.2), (0.1, -0.35), (0.5, 0.25), (-0.05, 0.55)]


@preset('claw_streaks', 'A10 the claw streaks (the lock spot + 2.0): four lilac claw-like streaks inside radius {r} (tenths) fall '
        'from 5 b above the executor onto it in 2 t (their points ending at the executor), then fade.',
        conv=tuple((f'x{k}', 'r', 0.1 * x) for k, (x, _z) in enumerate(CLAW_PTS)) +
        tuple((f'z{k}', 'r', 0.1 * z) for k, (_x, z) in enumerate(CLAW_PTS)))
def _p_claw_streaks():
    out = []
    for k in range(len(CLAW_PTS)):
        out.append(mac(card('claw_streaks', f'^$(x{k}) ^ ^$(z{k})', bb='vertical', s0=(3.2, 2.6, 3.2), s1=(3.2, 2.6, 3.2),
                            off=(0, 5.0, 0), move=(0, -5.0, 0), life=7, fade=3, dly=k % 2, dur=2)))
    return out + [dust(DUSTC[1], 1.2, '~ ~1 ~', (0.6, 1.0, 0.6), 12)]


RING8 = [xz(1.0, yaw) for yaw in radial(8)]


@preset('dust_ring', 'CS2 R6 the dust ring of radius {r} (tenths) where she lands on her back (at her feet + 0.1): ground chips '
        'in a ring of eight puffs, a soft cloud, grey dust (particles only).',
        conv=tuple((f'x{k}', 'r', 0.1 * x) for k, (x, _z) in enumerate(RING8)) +
        tuple((f'z{k}', 'r', 0.1 * z) for k, (_x, z) in enumerate(RING8)) + (('pd', 'r', 0.05),))
def _p_dust_ring():
    out = [mac(blockp('mycelium', f'^$(x{k}) ^0.1 ^$(z{k})', (0.2, 0.1, 0.2), 0.1, 4)) for k in range(len(RING8))]
    return out + [mac(part('cloud', '~ ~0.2 ~', ('$(pd)', 0.05, '$(pd)'), 0.02, 6)),
                  mac(dust((0.55, 0.52, 0.55), 1.4, '~ ~0.2 ~', ('$(pd)', 0.1, '$(pd)'), 12))]


@preset('kick_flash', 'CS2 / CS3 R8 the kick on her head (the head anchor): the cyan-gold impact flash (the only cyan-gold flash), '
        'a white glint, sparks.')
def _p_kick_flash():
    return [card('clash_gold_1', '~ ~ ~', bb='center', spin=50, s0=0.5, s1=2.2, life=5, fade=2, dur=2),
            card('glint_0', '~ ~ ~', bb='center', s0=0.4, s1=1.2, life=4, fade=2, col=WHITE),
            part('electric_spark', '~ ~ ~', (0.3, 0.3, 0.3), 0.15, 10), part('crit', '~ ~ ~', (0.3, 0.3, 0.3), 0.3, 6)]


@preset('clash_gold', 'Blade on blade (the blade_mid / hat_crown anchors, the midpoint between them; the deflect at the player): the '
        'gold starburst, six gold sparks flung out, crits.')
def _p_clash_gold():
    rnd = RND(37)
    out = [card('clash_gold_0', '~ ~ ~', bb='center', spin=60, s0=0.6, s1=2.6, life=6, fade=3, dur=2)]
    out += [fly('clash_spark_0', yaw, rnd.uniform(10, 50), 1.2, s0=0.6, s1=0.9, life=5, fade=2, col=GOLD)
            for yaw in radial(6, 25)]
    return out + [part('crit', '~ ~ ~', (0.3, 0.3, 0.3), 0.4, 10), dust((1.0, 0.8, 0.3), 1.0, '~ ~ ~', (0.3, 0.3, 0.3), 8),
                  part('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.08, 4)]


@preset('clash_spark', 'A small blade spark (the blade_mid / blade_tip anchors, every few ticks of a blade lock): four gold-white '
        'spark streaks, pink-violet embers.')
def _p_clash_spark():
    rnd = RND(41)
    out = [fly('clash_spark_0', rnd.uniform(0, 360), rnd.uniform(0, 60), rnd.uniform(0.8, 1.1), s0=0.4, s1=0.6, life=4, fade=2,
               col=rgb('#FFE8A0')) for _ in range(4)]
    return out + [dust((0.85, 0.45, 0.85), 0.8, '~ ~ ~', (0.15, 0.15, 0.15), 4), part('crit', '~ ~ ~', (0.1, 0.1, 0.1), 0.25, 4)]


@preset('clash_arc', 'CS1 C1 the orange lightning arcs between her blade and the player (the blade_mid anchor, every 2 t): two '
        'jagged arcs facing the viewer, orange dust.')
def _p_clash_arc():
    return [card('clash_spark_1', '~ ~ ~', bb='center', roll=30, s0=0.8, s1=1.2, life=3, fade=1, col=ORANGE),
            card('clash_spark_1', '~ ~ ~', bb='center', roll=-50, s0=0.7, s1=1.0, life=3, fade=1, col=rgb('#FFC070')),
            dust((1.0, 0.6, 0.2), 0.9, '~ ~ ~', (0.3, 0.3, 0.3), 6)]


@preset('deco_bolt', 'A decoration bolt (the gauntlets\' thin yellow lightning; no hit box) standing on the executor (a floor '
        'spot 3-6 b from the player) up 7 b: two flickering bolts, sparks.')
def _p_deco_bolt():
    return [card('deco_bolt', '~ ~ ~', bb='vertical', s0=(2.4, 7.0, 2.4), s1=(2.4, 7.0, 2.4), life=4),
            card('deco_bolt', '~ ~ ~', bb='vertical', spin=0, s0=(2.0, 6.4, 2.0), s1=(2.0, 6.4, 2.0), life=3, dly=2,
                 col=rgb('#FFF6C0')),
            card('glint_0', '~ ~0.2 ~', bb='center', s0=0.4, s1=1.0, life=3, fade=1, col=YELLOW),
            part('electric_spark', '~ ~2 ~', (0.1, 2.0, 0.1), 0.05, 8), dust(DUSTC[3], 1.0, '~ ~3 ~', (0.1, 3.0, 0.1), 6)]


@preset('scarlet_line', '홍련일섬\'s red slash line (CS1 C8, the 5 % instant death; S2b: the player\'s chest point, facing her): a '
        'line of length {len} (tenths) through the executor along the executor\'s yaw + {yaw} (90 = across a viewer looking '
        'along the executor\'s facing, its + end on their right), ' + api.SCARLET_LINE_ROLL.replace(' (', ': ').rstrip(')') +
        '; it opens in 2 t, darkens after 12 t, closes by 30 t.',
        conv=(('l', 'len', 0.1),),
        pre=['$scoreboard players set #a hrFx $(yaw)', 'scoreboard players remove #a hrFx 90',
             f'execute store result storage {PA}.yy int 1 run scoreboard players get #a hrFx',
             '$scoreboard players set #a hrFx $(roll)', 'scoreboard players operation #a hrFx *= #cm1 hrFx',
             f'execute store result storage {PA}.rr int 1 run scoreboard players get #a hrFx'])
def _p_scarlet_line():
    return [mac(card('scarlet_line', '^ ^ ^', '~$(yy) 0', roll='$(rr)', s0=('$(l)', 1.5, 1.5), s1=('$(l)', 6.0, 6.0), life=30,
                     fade=10, dur=2, hit=12, col2=rgb('#C04050'))),
            dust(DUSTC[4], 1.6, '~ ~ ~', (2.0, 0.1, 2.0), 30), part('sweep_attack', '~ ~ ~', (0.6, 0.1, 0.6), 0, 2)]


# --- petals, leaves, motes ---------------------------------------------------------------------------------------------------
@preset('petal_burst', 'A burst of petals of radius {r} (tenths) at the executor (CS1 C8 at her, CS2 R7, the 5 % instant death at the '
        'player): eight pink petals flung out turning, cherry leaves, pink dust.',
        conv=(('d', 'r', 0.1), ('pd', 'r', 0.04)))
def _p_petal_burst():
    rnd = RND(43)
    out = [mac(fly(f'petal_{k % 4}', yaw, rnd.uniform(5, 55), '$(d)', s0=0.25, s1=0.4, life=14, fade=6, roll=rnd.randint(-80, 80),
                   spin=120)) for k, yaw in enumerate(radial(8, 10))]
    return out + [mac(part('cherry_leaves', '~ ~ ~', ('$(pd)', 0.6, '$(pd)'), 0, 20)),
                  mac(dust(DUST_PETAL, 1.2, '~ ~ ~', ('$(pd)', 0.6, '$(pd)'), 12))]


DRIFT_PTS = [(-2.6, 0.6, 1.0), (1.4, 1.4, 2.2), (2.8, 0.2, -0.6), (-1.2, 1.8, -1.8), (0.4, 0.9, 3.0), (-3.0, 1.2, -0.4)]


@preset('petals_drift', 'CS0 E8 the petals drifting across the field as she sweeps her hand (at her chest, rotated as her): six '
        'pink petals drifting slowly to her right and down, turning, for 40 t; cherry leaves (ambient pool).')
def _p_petals_drift():
    out = [card(f'petal_{k % 3}', f'^{num(x)} ^{num(y)} ^{num(z)}', bb='fixed', rot=f'~{k * 53} {k * 17 - 30}', spin=150,
                s0=0.3, s1=0.3, move=(-2.6, -0.8, 0.5), life=40, fade=8, dly=k * 2, pool='am')
           for k, (x, y, z) in enumerate(DRIFT_PTS)]
    return out + [part('cherry_leaves', '~ ~1 ~', (3.0, 1.0, 3.0), 0, 8)]


@preset('petals_wind', 'CS4 S4 thin petal streaks in the wind (at her + 0.8, rotated as her): petals and two thin pink streaks '
        'whipping across from her left to her right (ambient pool).')
def _p_petals_wind():
    out = [card(f'petal_{k % 3}', f'^{num(3.5 - 0.4 * k)} ^{num(0.3 * k - 0.4)} ^{num(1.5 - 0.7 * k)}', f'~{20 * k} 10',
                spin=170, s0=0.28, s1=0.28, move=(-8.0, 0.6, 0.4), life=10, fade=3, dly=k, pool='am') for k in range(5)]
    out += [card('qline', f'^{num(3.0)} ^{num(0.6 + 0.5 * k)} ^{num(0.5 - k)}', '~-90 0', s0=(0.04, 0.04, 2.6),
                 s1=(0.02, 0.02, 3.4), move=(-7.0, 0, 0), life=8, fade=3, dly=2 * k, col=PINKW, pool='am') for k in range(2)]
    return out + [part('cherry_leaves', '~ ~ ~', (2.0, 0.6, 2.0), 0.2, 10)]


@preset('petals_heart', 'CS4 big pink heart-shaped petals crossing near her (at her chest, rotated as her): three slow, turning '
        'heart petals for 30 t (ambient pool), cherry leaves.')
def _p_petals_heart():
    out = [card('petal_3', f'^{num(x)} ^{num(y)} ^{num(z)}', f'~{25 * k} 0', spin=60, s0=0.8 + 0.2 * k, s1=0.9 + 0.2 * k,
                move=(-1.6, -0.5, 0.2), life=30, fade=8, dly=4 * k, pool='am')
           for k, (x, y, z) in enumerate(((1.6, 0.8, 1.2), (-0.8, 1.4, 1.8), (0.4, 0.4, 2.4)))]
    return out + [part('cherry_leaves', '~ ~ ~', (1.5, 0.8, 1.5), 0, 6)]


MOTE_PTS = [(-2.2, 0.2, 1.4), (1.8, 0.5, 0.6), (0.6, 0.3, -2.0), (-1.0, 0.7, -1.2), (2.6, 0.4, 2.2)]


@preset('motes_warm', 'CS4 warm firefly-like motes low over the grass (at her + 0.4): five small warm motes rising slowly for 40 t '
        '(ambient pool), fireflies.')
def _p_motes_warm():
    out = [card('petal_7', f'^{num(x)} ^{num(y)} ^{num(z)}', bb='center', s0=0.14, s1=0.18, move=(0, 0.8, 0), life=40, fade=10,
                dly=3 * k, col=WARM, pool='am') for k, (x, y, z) in enumerate(MOTE_PTS)]
    return out + [part('firefly', '~ ~0.3 ~', (3.0, 0.3, 3.0), 0, 2)]


LEAF_N = 40
_LF = random.Random(59)
LEAF_PTS = [(_LF.uniform(5.0, 10.0), _LF.uniform(-1.5, 3.0), _LF.uniform(-5.0, 8.0), _LF.choice((LEAF_RED, LEAF_BLACK)), 4 + k % 3)
            for k in range(LEAF_N)]


@preset('leaves_dark', 'Dark-red / black leaves blowing across the sky (S2b CS1: her + 6, rotated as her): {n} leaves (up to 40; '
        'n < 0: the last -n of them, so {n:20} and then {n:-20} spread the 40 over two ticks) from her left across to her right '
        'over 30 t, turning (ambient pool).',
        pre=['$scoreboard players set #n2 hrFx $(n)'])
def _p_leaves_dark():
    out = []
    for k, (x, y, z, col, fr) in enumerate(LEAF_PTS):
        c = card(f'petal_{fr}', f'^{num(x, 2)} ^{num(y, 2)} ^{num(z, 2)}', f'~{(k * 37) % 360} {(k * 23) % 90 - 45}', spin=170,
                 s0=0.32, s1=0.32, move=(-14.0, -2.0, 0.5), life=30, fade=6, dly=k % 10, col=col, pool='am')
        # leaf k (0-based) comes with the first n (n >= k + 1) or the last -n (n <= k - 40), i.e. unless n is in k - 39 .. k
        # (I1b verification round 1: a CS1 burst of 40 in one tick cost 3.2 k commands; S2b's call is now split in two)
        out.append(f'execute unless score #n2 hrFx matches {k - LEAF_N + 1}..{k} run {c}')
    return out


@preset('leaves_swirl', 'Dark-red leaves swirling round her (CS1 C8 / SQ1: her + 1.1): ten leaves flung round and up, turning, '
        'dark-red dust (ambient pool).')
def _p_leaves_swirl():
    rnd = RND(61)
    out = [fly(f'petal_{4 + k % 3}', yaw, rnd.uniform(25, 70), rnd.uniform(1.2, 2.4), s0=0.3, s1=0.4, life=18, fade=6,
               col=LEAF_RED if k % 3 else LEAF_BLACK, spin=170, pool='am', roll=rnd.randint(-90, 90))
           for k, yaw in enumerate(radial(10, 7))]
    return out + [dust((0.5, 0.08, 0.15), 1.2, '~ ~ ~', (1.0, 0.8, 1.0), 16)]


@preset('ambient_p1', 'Arena ambience, P1 (the module, every ~10 t near the player; at the player): a pink petal drifting down '
        '(ambient pool), cherry leaves, one dark ash speck further out (arena.md §5: sparse).')
def _p_ambient_p1():
    return [card('petal_1', '^2.5 ^3.2 ^3', '~40 -20', spin=120, s0=0.26, s1=0.26, move=(-1.6, -2.4, 0.4), life=40, fade=8,
                 pool='am'),
            part('cherry_leaves', '~ ~4 ~', (8.0, 2.0, 8.0), 0, 3), part('ash', '~ ~3 ~', (11.0, 3.0, 11.0), 0, 1)]


@preset('ambient_p2', 'Arena ambience, P2 (the module, every ~6 t near the player; at the player): crimson spores, a pink mote, '
        'a firefly low over the grass about every 20 t (particles only).')
def _p_ambient_p2():
    return [part('crimson_spore', '~ ~2 ~', (8.0, 2.0, 8.0), 0, 2), dust(DUST_PETAL, 1.2, '~ ~2 ~', (8.0, 2.0, 8.0), 1),
            'execute store result score #g hrFx run time query gametime', 'scoreboard players operation #g hrFx %= #c20 hrFx',
            'execute if score #g hrFx matches ..5 run ' + part('firefly', '~ ~0.4 ~', (6.0, 0.2, 6.0), 0, 1)]


# --- the arrival --------------------------------------------------------------------------------------------------------------
RIFT_POS = '^ ^1.45 ^'      # the void centre above the tear point (S1's rift: CENTRE 1.45, VOID_H 2.6)
RIFT_ARCS = [(0.75, 1.9), (-0.8, 1.6), (0.55, 0.8), (-0.6, 2.4)]


@preset('arrive_rift', 'The arrival tear (S2b CS0 E0: the floor point 1.5 b behind the player, facing the arena): the dungeon '
        'rift\'s void, rim and four lightning arcs (the rlk:rift models of tools/build_rift.py when the pack has them) shrink '
        'shut over 30 t, portal motes.')
def _p_arrive_rift():
    out = [card('rift_rim', RIFT_POS, bb='vertical', s0=2.88, s1=0.1, life=30, fade=4, dur=26, col=RIFT_RIM),
           card('rift_void', RIFT_POS, bb='vertical', s0=2.6, s1=0.1, life=30, fade=4, dur=26)]
    for k, (x, y) in enumerate(RIFT_ARCS):
        out.append(card(f'rift_arc{k}', f'^{num(x, 2)} ^{num(y, 2)} ^0.05', bb='center', s0=1.1, s1=0.4,
                        life=8 + 4 * (k % 2), fade=3, dly=4 * k, dur=6))
    return out + [part('reverse_portal', '~ ~1.4 ~', (0.5, 1.0, 0.5), 0.05, 30), part('end_rod', '~ ~1.4 ~', (0.4, 0.9, 0.4), 0.05, 8)]


# --- the event coda (PLAN §7.3.2; particles except the glint) -----------------------------------------------------------------
@preset('ev_glint', 'E12 the glint running along the scabbard (S2b: at the hand_r anchor): three small white glints along her '
        'facing 0 / 0.4 / 0.8 b, 2 t apart, end-rod motes (the fight kit\'s blade glint).')
def _p_ev_glint():
    return [card('glint_0', f'^ ^ ^{num(0.4 * k)}', bb='center', spin=60, s0=0.2, s1=0.7, life=5, fade=2, dly=2 * k, col=WHITE)
            for k in range(3)] + [part('end_rod', '^ ^ ^0.4', (0.1, 0.1, 0.3), 0.01, 3)]


@preset('ev_trail', 'The thrown sword\'s trail (each flight tick, at the sword): 2 cherry leaves + 1 lilac mote.')
def _p_ev_trail():
    return [part('cherry_leaves', '~ ~ ~', (0.1, 0.1, 0.1), 0, 2), dust(DUST_LILAC_EV, 1.0, '~ ~ ~', (0.05, 0.05, 0.05), 1)]


@preset('ev_petals', 'Petals round the point (E56-E108 round the player every 4 t): {n} cherry leaves + {n} petal motes (#D55D87).',
        conv=(('n', 'n', None),))
def _p_ev_petals():
    return [mac(part('cherry_leaves', '~ ~ ~', (0.7, 0.6, 0.7), 0, '$(n)')),
            mac(dust(DUST_PETAL, 1.0, '~ ~ ~', (0.7, 0.6, 0.7), '$(n)'))]


@preset('ev_leave', 'E34 she leaves in petals and wind (at her chest): 60 cherry leaves + 30 petal motes + a gust, spread 0.5 / '
        '0.95 / 0.5.')
def _p_ev_leave():
    return [part('cherry_leaves', '~ ~ ~', (0.5, 0.95, 0.5), 0.05, 60), dust(DUST_PETAL, 1.2, '~ ~ ~', (0.5, 0.95, 0.5), 30),
            part('gust', '~ ~ ~', (0, 0, 0), 0, 1)]


@preset('ev_beam', 'A silver moonbeam (E44 onto the sword / E42 onto the player): a column from {h} (tenths) above the executor down '
        'to it, drawn over {t} ticks by the ager (a marker the kit ages): end rods + silver dust at the falling front, silver '
        'dust along the lit column, a flash at the point when it arrives.',
        pre=[f'execute summon minecraft:marker run function {FN}e/beam_new', '$scoreboard players set #a hrFx $(h)',
             f'scoreboard players operation @e[type=minecraft:marker,tag={BEAM}_n] hrFxG = #a hrFx',
             '$scoreboard players set #a hrFx $(t)',
             f'execute if score #a hrFx matches ..0 run scoreboard players set #a hrFx 1',
             f'scoreboard players operation @e[type=minecraft:marker,tag={BEAM}_n] hrFxS = #a hrFx',
             f'scoreboard players operation @e[type=minecraft:marker,tag={BEAM}_n] hrFxD = #a hrFx',
             f'tag @e[type=minecraft:marker,tag={BEAM}_n] remove {BEAM}_n', f'schedule function {FN}e/world 1t replace'])
def _p_ev_beam():
    return []


RING16 = [xz(1.0, yaw) for yaw in radial(16)]


@preset('ev_wind', 'E42 the wind round the player: a 16-point ring of small white dust of radius {r} (tenths), a gust, 6 cherry '
        'leaves.', conv=tuple((f'x{k}', 'r', 0.1 * x) for k, (x, _z) in enumerate(RING16)) +
        tuple((f'z{k}', 'r', 0.1 * z) for k, (_x, z) in enumerate(RING16)))
def _p_ev_wind():
    out = [mac(dust((1.0, 1.0, 1.0), 0.6, f'^$(x{k}) ^0.6 ^$(z{k})', (0, 0, 0), 1)) for k in range(16)]
    return out + [part('gust', '~ ~0.6 ~', (0, 0, 0), 0, 1), part('cherry_leaves', '~ ~1 ~', (1.0, 0.6, 1.0), 0, 6)]


@preset('ev_palm', 'The moonlight "cup" in her palm / the orb (every tick): 2 end rods + 3 silver motes at the point.')
def _p_ev_palm():
    return [part('end_rod', '~ ~ ~', (0.05, 0.05, 0.05), 0.0, 2), dust(DUST_SILVER, 0.8, '~ ~ ~', (0.08, 0.08, 0.08), 3)]


@preset('ev_take', 'E56 the grant (at the player\'s chest): 20 end rods (speed 0.15) and a 16-point ring (r 1.2) of lilac (c 1, the '
        'item) or silver (c 2, the buff) dust.', split_c=True)
def _p_ev_take(c):
    col = DUST_LILAC_EV if c == 1 else DUST_SILVER
    out = [part('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.15, 20)]
    out += [dust(col, 1.0, f'^{num(1.2 * x, 3)} ^ ^{num(1.2 * z, 3)}', (0, 0, 0), 1) for x, z in RING16]
    return out


assert set(PRESETS) == set(api.KIT_PRESETS), set(PRESETS) ^ set(api.KIT_PRESETS)
PRESETS = {k: PRESETS[k] for k in api.KIT_PRESETS}   # api order
SPLIT_CS = {'ev_take': (1, 2)}         # the c variants a split preset has (default: all five)

# ----------------------------------------------------------------------------- props (api.KIT_PROPS)
FOLLOW_STAY = f'{TAG}fs'               # followers that keep their own spot and go with their lead (the seat rock's items)
DISC_SCALE = api.DISC['hr']            # the flat unit-radius disc card x 1.4 = the hazard's half width
# I1b (requests s1k-3 / s2b-4): the halo's bright looks p1b / p2b are the same sprites HALO_BRIGHT x brighter than p1 / p2.
# A custom_model_data tint only multiplies (white = the sprite as painted), so p1 / p2 carry the tint 1 / HALO_BRIGHT
# (212 = 0xD4D4D4) and p1b / p2b the white one.
HALO_BRIGHT = 1.2
HALO_TINT = round(255 / HALO_BRIGHT) * 0x010101
PROPS = {
    # name -> (doc, {look: (kind or None (hidden), scale[, tint])}, billboard, anim ('d' disc spin / 'p' petal rock / None))
    'disc': ('A7 moon disc (R2, A13): one flat lilac disc card on the projectile display (radius 1.4 = the hazard\'s half '
             'width), horizontal, spinning 30 deg per tick (quarter turns over 3 t), facing its flight (the display\'s yaw).',
             {None: ('disc_0', DISC_SCALE)}, 'fixed', 'd'),
    'petal_big': ('CS1 the big red petal (0.8 b, the caller turns it to face the player each tick; it rocks slowly): {look} '
                  'whole / cut (a glowing line across) / split (the halves apart).',
                  {'whole': ('petal_big_0', 0.8), 'cut': ('petal_big_1', 0.8), 'split': ('petal_big_2', 0.8)}, 'fixed', 'p'),
    'moon_halo': ('The halo card 1 b in front of the block moon (12.4 b, facing the arena as the caller turned it; its centre '
                  'clear, the block disc shows through): {look} p1 white-blue / p2 red / off (hidden) / p1b, p2b = p1, p2 about '
                  '20 % brighter (CS0 E3, the CS4 moon gaze).',
                  {'p1': ('moon_halo_0', 12.4, HALO_TINT), 'p2': ('moon_halo_1', 12.4, HALO_TINT), 'off': (None, 0.0),
                   'p1b': ('moon_halo_0', 12.4), 'p2b': ('moon_halo_1', 12.4)}, 'fixed', None),
    'lotus': ('A lotus flower on the pond (the water surface; 0.9 b, standing, turning to the viewer): {look} bud (closed, pale '
              'pink, P1) / bloom (open crimson, P2).', {'bud': ('lotus_0', 0.9), 'bloom': ('lotus_1', 0.9)}, 'vertical', None),
    'seat_rock': ('CS0 her seat: a low flat stone (vanilla tuff, 1.2 x 0.24 x 0.64 b, its top 0.24 b over the display (under her '
                  'thighs, behind her heels): no collision) and on it {look}: bottle = the rice-wine bottle on her left, bare = the stone alone, set = the bottle '
                  'and the cup on her right (vanilla item displays the kit keeps with the stone and removes with it).',
                  {'bottle': ('rock', 1.0), 'bare': ('rock', 1.0), 'set': ('rock', 1.0)}, 'fixed', None),
}
assert set(PROPS) == set(api.KIT_PROPS) and all(set(v[1]) == set(api.KIT_PROPS[k].get('look', (None,))) or k == 'disc'
                                                for k, v in PROPS.items())
# S2d (request s2d-2): the stone under her thighs (top 0.24 b = their underside, hip 0.385 b), its front face 0.135 b in front
# of her anchor (clear of her shins), its back 0.505 b behind; the bottle / cup scales match the rig's (0.30 tall, 0.15 wide)
SEAT = {'rock': ('minecraft:tuff', (0.0, 0.12, -0.185), (1.2, 0.24, 0.64)),
        'bottle': ('minecraft:potion', (0.42, 0.24, -0.15), 0.42),
        'cup': ('minecraft:bowl', (-0.42, 0.24, -0.15), 0.26)}
BOTTLE_COLOR = rgb('#E8E2D2')          # a milky rice wine (potion_contents custom_color)
DISC_Q = ['[0f,0f,0f,1f]', '[0f,0.7071068f,0f,0.7071068f]', '[0f,1f,0f,0f]', '[0f,0.7071068f,0f,-0.7071068f]']

# ----------------------------------------------------------------------------- writer
HEADER = '# Generated by tools/build_mboss_hr_fx.py (홍련 fx kit) - edit the generator, not this file.\n'
E = FN + 'e/'
SEL = f'@e[type=minecraft:item_display,tag={TAG}'
FAKE = ('#n', '#na', '#ni', '#ser', '#now', '#now2', '#wd', '#c2', '#col', '#roll', '#spin', '#life', '#fade', '#dly', '#dur', '#hit',
        '#pool', '#a', '#b', '#c', '#k', '#t', '#it', '#f', '#h', '#pt', '#fl', '#m', '#r', '#p', '#o', '#i', '#j', '#ly',
        '#n2', '#g', '#on', '#sk', '#l', '#lid', '#at', '#af', '#lnW', '#lnA', '#lnE', '#ovH', '#ovE', '#oi', '#oh', '#oo',
        '#demo', '#dt', '#s', '#d', '#my', '#mz', '#ny', '#nz', '#cm1', '#c3', '#c4', '#c26', '#c90', '#c10', '#c20', '#c36', '#c100', '#c115', '#c360', '#c1000')
INIT = f'execute unless data storage {STO} fx{{init:1b}} run function {E}init'
NEG_LIT = re.compile(r'scoreboard players (add|remove) \S+ \S+ -')


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
            assert not NEG_LIT.search(s), f'{rel}:{i} negative add/remove literal: {s[:90]}'
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


def engine(W):
    W.w('card', [
        '# Spawn one painted fx card at pos, rotated rot (relative to the executing context), into the fx pool.',
        '# {kind, pos:"^x ^y ^z", rot:"~ ~", bb:fixed|center|vertical|horizontal, roll:<deg, about local z>,',
        '#  spin:<deg over the main interpolation, -170..170, about the card normal (y for flat / cross)>,',
        '#  s0:<start size>, s1:<end size>, move:"dx,dy,dz" (end offset, display frame: +x left, +y up, +z forward),',
        '#  life:<ticks>, fade:<shrink-out ticks>, col:<RGB int tint, 16777215 = the painted colours>}.',
        f'# Never skipped: the ager keeps the newest {CAP_FX} fx cards (the oldest go).', INIT,
        f'$data modify storage {STO} fx.a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)f,$(s0)f,$(s0)f",s1:"$(s1)f,$(s1)f,$(s1)f",off:"0f,0f,0f",move:"$(move)",col:$(col),col2:-1,'
        f'ax:"0f,0f,1f",tg:"{TAG}_c",tpd:0}}',
        f'$data modify storage {STO} fx.a.ax set from storage {STO} fx.ax.$(kind)',
        f'$scoreboard players set #roll {OBJ} $(roll)',
        f'$scoreboard players set #spin {OBJ} $(spin)',
        f'$scoreboard players set #life {OBJ} $(life)',
        f'$scoreboard players set #fade {OBJ} $(fade)',
        f'scoreboard players set #dly {OBJ} 0',
        f'scoreboard players set #dur {OBJ} 0',
        f'scoreboard players set #hit {OBJ} -1',
        f'scoreboard players set #pool {OBJ} 0',
        f'function {E}make',
    ])
    W.w('cardx', [
        '# card with every option: s0 / s1 as "xf,yf,zf" vectors, off:"xf,yf,zf" (static start translation), move',
        '# (the END translation), dly:<ticks hidden before it shows>, dur:<ticks of the main interpolation, 0 = up to',
        '# the fade>, hit:<ticks after the call when the tint becomes col2, -1 = never>, col2:<RGB int>, pl:<pool: 0 fx',
        f'# (cap {CAP_FX}), 1 ambient (cap {CAP_AMB}), 2 afterimage (cap {CAP_AI})>, tg:<the pool tag {TAG}_c / _a / _i>.',
        INIT, f'$scoreboard players set #pool {OBJ} $(pl)',
        f'$data modify storage {STO} fx.a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)",s1:"$(s1)",off:"$(off)",move:"$(move)",col:$(col),col2:$(col2),ax:"0f,0f,1f",tg:"$(tg)",tpd:0}',
        f'$data modify storage {STO} fx.a.ax set from storage {STO} fx.ax.$(kind)',
        f'$scoreboard players set #roll {OBJ} $(roll)',
        f'$scoreboard players set #spin {OBJ} $(spin)',
        f'$scoreboard players set #life {OBJ} $(life)',
        f'$scoreboard players set #fade {OBJ} $(fade)',
        f'$scoreboard players set #dly {OBJ} $(dly)',
        f'$scoreboard players set #dur {OBJ} $(dur)',
        f'$scoreboard players set #hit {OBJ} $(hit)',
        f'function {E}make',
    ])
    W.w('e/make', [
        f'# Internal: storage {STO} fx.a (kind pos rot bb s0 s1 off move col col2 ax tg tpd) + #roll #spin #life #fade',
        '# #dly #dur #hit #pool (0 fx, 1 ambient, 2 afterimage) -> one card with the next spawn serial (hrFxQ). The stage',
        '# clock is gametime + 1 (the fg kit\'s first-tick fix): the ager (fx/e/world, a 1t schedule) runs at the END of',
        '# this server tick with gametime already + 1, so the main interpolation starts in the next server tick and the',
        '# client animates it. Stages: shows at clock + dly, interpolates from clock + dly + 1 over dur ticks, recolours',
        '# at clock + hit, shrinks over the last fade ticks, removed at clock + dly + life.',
        f'scoreboard players add #ser {OBJ} 1',
        f'execute if score #pool {OBJ} matches 0 run scoreboard players add #n {OBJ} 1',
        f'execute if score #pool {OBJ} matches 1 run scoreboard players add #na {OBJ} 1',
        f'execute if score #pool {OBJ} matches 2 run scoreboard players add #ni {OBJ} 1',
        f'execute if score #life {OBJ} matches ..1 run scoreboard players set #life {OBJ} 2',
        f'execute if score #fade {OBJ} matches ..-1 run scoreboard players set #fade {OBJ} 0',
        f'execute if score #dly {OBJ} matches ..-1 run scoreboard players set #dly {OBJ} 0',
        f'scoreboard players operation #wd {OBJ} = #life {OBJ}',
        f'scoreboard players remove #wd {OBJ} 2',
        f'scoreboard players operation #fade {OBJ} < #wd {OBJ}',
        f'scoreboard players operation #wd {OBJ} = #life {OBJ}',
        f'scoreboard players operation #wd {OBJ} -= #fade {OBJ}',
        f'scoreboard players remove #wd {OBJ} 1',
        f'execute if score #dur {OBJ} matches 1.. run scoreboard players operation #wd {OBJ} = #dur {OBJ}',
        f'execute if score #wd {OBJ} matches ..0 run scoreboard players set #wd {OBJ} 1',
        f'execute if score #spin {OBJ} matches 171.. run scoreboard players set #spin {OBJ} 170',
        f'execute if score #spin {OBJ} matches ..-171 run scoreboard players set #spin {OBJ} -170',
        f'execute store result storage {STO} fx.a.rr float 0.017453292 run scoreboard players get #roll {OBJ}',
        f'execute store result storage {STO} fx.a.sr float 0.017453292 run scoreboard players get #spin {OBJ}',
        f'execute store result storage {STO} fx.a.d int 1 run scoreboard players get #wd {OBJ}',
        f'execute store result storage {STO} fx.a.f int 1 run scoreboard players get #fade {OBJ}',
        f'execute store result score #col {OBJ} run data get storage {STO} fx.a.col2',
        f'data modify storage {STO} fx.a.z set from storage {STO} fx.a.s0',
        f'execute if score #dly {OBJ} matches 1.. run data modify storage {STO} fx.a.z set value "0f,0f,0f"',
        f'function {E}spawn with storage {STO} fx.a',
        'execute store result score #now ' + OBJ + ' run time query gametime',
        f'scoreboard players add #now {OBJ} 1',
        f'execute as {SEL}_new,limit=1] run function {E}born',
        f'tag {SEL}_new] remove {TAG}_new',
        f'schedule function {E}world 1t replace',
    ])
    end_tr = ('translation:[$(move)],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(s1)],'
              'right_rotation:{angle:$(sr)f,axis:[$(ax)]}')
    W.w('e/spawn', [
        f'# Internal (macro, storage {STO} fx.a): the item_display; the stage snapshots ride on its item.',
        f'$summon minecraft:item_display $(pos) {{Tags:["{TAG}","{TAG}_new","rlk_room","rlk_mb_aux","$(tg)"],'
        'billboard:"$(bb)",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
        'teleport_duration:$(tpd),interpolation_duration:0,transformation:{translation:[$(off)],'
        'left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(z)],right_rotation:[0f,0f,0f,1f]},'
        f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{NS_TEX}$(kind)",'
        '"minecraft:custom_model_data":{colors:[$(col)]},"minecraft:custom_data":{'
        'hrS:{start_interpolation:0,interpolation_duration:0,transformation:{scale:[$(s0)]}},'
        'hrG:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'hrF:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}},'
        'hrC:$(col2)}}}}',
        f'$execute positioned $(pos) rotated $(rot) run tp {SEL}_new,limit=1] ~ ~ ~ ~ ~',
    ])
    W.w('e/born', [
        '# Internal, as the new card: stage clock values (gametime + 1 based) in hrFxS hrFxG hrFxH hrFxK hrFxD, the serial.',
        f'scoreboard players operation @s hrFxQ = #ser {OBJ}',
        f'scoreboard players operation @s hrFxS = #now {OBJ}',
        f'scoreboard players operation @s hrFxS += #dly {OBJ}',
        'scoreboard players operation @s hrFxG = @s hrFxS',
        'scoreboard players add @s hrFxG 1',
        'scoreboard players operation @s hrFxD = @s hrFxS',
        f'scoreboard players operation @s hrFxD += #life {OBJ}',
        'scoreboard players operation @s hrFxK = @s hrFxD',
        f'scoreboard players operation @s hrFxK -= #fade {OBJ}',
        f'scoreboard players operation @s hrFxH = #now {OBJ}',
        f'scoreboard players operation @s hrFxH += #hit {OBJ}',
        f'tag @s add {TAG}_go',
        f'execute if score #dly {OBJ} matches 1.. run tag @s add {TAG}_sh',
        f'execute if score #fade {OBJ} matches 1.. run tag @s add {TAG}_fd',
        f'execute if score #hit {OBJ} matches 0.. if score #col {OBJ} matches 0.. run tag @s add {TAG}_hit',
    ])
    W.w('e/world', [
        '# Ages the kit\'s cards and moonbeams once per tick while any is alive (scheduled from e/make and itself, so it runs',
        '# at the end of the server tick; no hook in rlk:tick), then keeps every pool at its cap (the oldest go). A dead or',
        '# reviving player clears every card (fx/clear).',
        f'execute unless entity @e[tag={TAG},limit=1] run return run function {E}zero',
        f'execute if entity @a[tag=player,scores={{dead=1}}] run function {FN}clear',
        f'execute if entity @a[tag=player,scores={{rnDie=1..}}] run function {FN}clear',
        f'execute store result score #now {OBJ} run time query gametime',
        f'execute as {SEL}] run function {E}age',
        f'execute as @e[type=minecraft:marker,tag={BEAM}] at @s run function {E}beam',
        f'execute store result score #n {OBJ} if entity {SEL}_c]',
        f'execute store result score #na {OBJ} if entity {SEL}_a]',
        f'execute store result score #ni {OBJ} if entity {SEL}_i]',
        f'execute if score #n {OBJ} matches {CAP_FX + 1}.. run function {E}cull_fx',
        f'execute if score #na {OBJ} matches {CAP_AMB + 1}.. run function {E}cull_am',
        f'execute if score #ni {OBJ} matches {CAP_AI + 1}.. run function {E}cull_ai',
        f'execute if entity @e[tag={TAG},limit=1] run schedule function {E}world 1t replace',
    ])
    W.w('e/zero', [f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #na {OBJ} 0',
                   f'scoreboard players set #ni {OBJ} 0'])
    for pool, (_ix, ptag) in POOLS.items():
        cap = CAPS[pool]
        W.w(f'e/cull_{pool}', [
            f'# The {pool} pool is over its cap {cap}: the oldest cards go (the newest {cap} spawn serials stay). #k = the cards',
            '# to remove; the serial threshold #t starts at #ser - cap and steps down by the surplus while cards in the',
            '# window above it already expired (exact: #b = the cards at or below #t equals #k), at most 24 steps.',
            f'scoreboard players operation #k {OBJ} = {POOL_FP[pool]} {OBJ}', f'scoreboard players remove #k {OBJ} {cap}',
            f'scoreboard players operation #t {OBJ} = #ser {OBJ}', f'scoreboard players remove #t {OBJ} {cap}',
            f'scoreboard players set #it {OBJ} 0', f'function {E}cull_{pool}_i'])
        W.w(f'e/cull_{pool}_i', [
            f'# Internal: one threshold step of e/cull_{pool}.',
            f'execute store result storage {STO} fx.cu.t int 1 run scoreboard players get #t {OBJ}',
            f'function {E}cull_{pool}_n with storage {STO} fx.cu',
            f'scoreboard players add #it {OBJ} 1',
            f'execute if score #b {OBJ} <= #k {OBJ} run return run function {E}cull_{pool}_k with storage {STO} fx.cu',
            f'execute if score #it {OBJ} matches 24.. run return run function {E}cull_{pool}_k with storage {STO} fx.cu',
            f'scoreboard players operation #b {OBJ} -= #k {OBJ}',
            f'scoreboard players operation #t {OBJ} -= #b {OBJ}',
            f'function {E}cull_{pool}_i'])
        W.w(f'e/cull_{pool}_n', [f'# Internal (macro {{t}}): #b = the {pool} cards with a serial <= t.',
                                 f'$execute store result score #b {OBJ} if entity {SEL}_{ptag[len(TAG) + 1:]},'
                                 'scores={hrFxQ=..$(t)}]'])
        W.w(f'e/cull_{pool}_k', [f'# Internal (macro {{t}}): remove the {pool} cards with a serial <= t, recount.',
                                 f'$kill {SEL}_{ptag[len(TAG) + 1:]},scores={{hrFxQ=..$(t)}}]',
                                 f'execute store result score {POOL_FP[pool]} {OBJ} if entity {SEL}_{ptag[len(TAG) + 1:]}]'])
    W.w('e/age', [
        '# As one card (the stage clock in #now).',
        'execute unless score @s hrFxD = @s hrFxD run return run kill @s',
        f'execute if score #now {OBJ} >= @s hrFxD run return run kill @s',
        f'execute if entity @s[tag={TAG}_sh] if score #now {OBJ} >= @s hrFxS run function {E}show',
        f'execute if entity @s[tag={TAG}_go] if score #now {OBJ} >= @s hrFxG run function {E}go',
        f'execute if entity @s[tag={TAG}_hit] if score #now {OBJ} >= @s hrFxH run function {E}hit',
        f'execute if entity @s[tag={TAG}_fd] if score #now {OBJ} >= @s hrFxK run function {E}fade',
    ])
    W.w('e/show', ['# a delayed card appears at its start size',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".hrS',
                   f'tag @s remove {TAG}_sh'])
    W.w('e/go', ['# start -> end transformation over dur ticks (client interpolation)',
                 'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".hrG',
                 f'tag @s remove {TAG}_go'])
    W.w('e/hit', ['# the tint changes (the second colour: a dimming fade, a white-hot close)',
                  'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set from entity @s '
                  'item.components."minecraft:custom_data".hrC',
                  f'tag @s remove {TAG}_hit'])
    W.w('e/fade', ['# shrink to nothing over the last fade ticks',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".hrF',
                   f'tag @s remove {TAG}_fd'])
    spin_y = ','.join(f'{k}:"0f,1f,0f"' for k in ALL_KINDS if kind_info(k)[0] in SPIN_Y)
    gl = ','.join(f'{k}:"{glyph(k)}"' for k in GLYPHS)
    W.w('e/init', ['# Objectives, constants and tables of the kit (made by the first call; removed by fx/uninstall).',
                   f'scoreboard objectives add {OBJ} dummy', *[f'scoreboard objectives add {o} dummy' for o in OBJECTIVES],
                   *[f'scoreboard players set {fp} {OBJ} 0' for fp in ('#n', '#na', '#ni', '#lnA', '#ovH', '#ovE')],
                   f'execute unless score #ser {OBJ} matches 1.. run scoreboard players set #ser {OBJ} 0',
                   *[f'scoreboard players set #c{v} {OBJ} {v}' for v in (2, 10, 20, 36, 100, 115, 360, 1000)],
                   f'scoreboard players set #cm1 {OBJ} -1', f'scoreboard players set #c3 {OBJ} 3',
                   f'scoreboard players set #c4 {OBJ} 4', f'scoreboard players set #c26 {OBJ} 26',
                   f'scoreboard players set #c90 {OBJ} 90',
                   '# spin axes (= the card normal) of the flat and cross kinds; face / lance kinds keep z (storage a default)',
                   f'data modify storage {STO} fx.ax set value {{{spin_y}}}',
                   f'# the floor (y x 100) the clamps measure from: the arena\'s ({FLOOR}); test/stage sets the demo floor',
                   f'data modify storage {STO} fx.fl set value {FLOOR * 100}',
                   '# the crescent floor clamp: the lowest point per mille per (pitch cell, roll cell), fx/e/clamp_arc',
                   f'data modify storage {STO} fx.low set value [I;{",".join(str(v) for v in LOW)}]',
                   '# sin(0..90 deg) per mille (fx/e/sinf: the band clamp and its level sweep)',
                   f'data modify storage {STO} fx.sin set value [I;{",".join(str(v) for v in SIN)}]',
                   '# the full-screen glyphs of fx/hud/ovl (font rlk:mboss_hr)',
                   f'data modify storage {STO} fx.gl set value {{{gl}}}',
                   f'data modify storage {STO} fx.hud set value {{warn:0b,skip:0b}}',
                   f'data modify storage {STO} fx.init set value 1b'])
    W.w('e/hgt', ['# #h = the executor\'s height over the floor in hundredths (storage fx.fl = the floor y x 100), #pt = its',
                  '# pitch (degrees, + down).',
                  f'execute summon minecraft:marker run function {E}hgt_m',
                  f'execute store result score #fl {OBJ} run data get storage {STO} fx.fl',
                  f'scoreboard players operation #h {OBJ} -= #fl {OBJ}'])
    W.w('e/hgt_m', ['# Internal: as a marker summoned at the executor (summon takes no rotation: tp gives it the context\'s):',
                    'tp @s ~ ~ ~ ~ ~',
                    f'execute store result score #h {OBJ} run data get entity @s Pos[1] 100',
                    f'execute store result score #pt {OBJ} run data get entity @s Rotation[1]', 'kill @s'])
    W.w('e/clamp_arc', [
        '# Crescent floor clamp: #r reach (tenths), #p pitch (Minecraft), #o roll (degrees) -> #ly the lift (hundredths,',
        '# <= ARC_LIFT) and #r = min(#r, 100 (h - 10 + ly) / LOW) so the crescent (bearings +-80 deg from the aim, unit',
        '# radius x reach) stays above the floor; LOW per mille from the table.',
        f'scoreboard players operation #i {OBJ} = #p {OBJ}', f'scoreboard players add #i {OBJ} 95',
        f'scoreboard players operation #i {OBJ} /= #c10 {OBJ}',
        f'execute if score #i {OBJ} matches ..-1 run scoreboard players set #i {OBJ} 0',
        f'execute if score #i {OBJ} matches 19.. run scoreboard players set #i {OBJ} 18',
        f'scoreboard players operation #j {OBJ} = #o {OBJ}', f'scoreboard players add #j {OBJ} 3785',
        f'execute if score #j {OBJ} matches ..-1 run scoreboard players set #j {OBJ} 0',
        f'scoreboard players operation #j {OBJ} %= #c360 {OBJ}', f'scoreboard players operation #j {OBJ} /= #c10 {OBJ}',
        f'scoreboard players operation #i {OBJ} *= #c36 {OBJ}', f'scoreboard players operation #i {OBJ} += #j {OBJ}',
        f'execute store result storage {STO} fx.q.i int 1 run scoreboard players get #i {OBJ}',
        f'function {E}lowf with storage {STO} fx.q',
        f'scoreboard players set #ly {OBJ} 0',
        f'execute if score #f {OBJ} matches ..0 run return 0',
        f'function {E}hgt', f'scoreboard players remove #h {OBJ} 10',
        f'execute if score #h {OBJ} matches ..0 run scoreboard players set #h {OBJ} 1',
        '# the lift: the crescent rises (up to ARC_LIFT hundredths) by what it would reach below the floor, the rest shrinks it',
        f'scoreboard players operation #ly {OBJ} = #r {OBJ}', f'scoreboard players operation #ly {OBJ} *= #f {OBJ}',
        f'scoreboard players operation #ly {OBJ} /= #c100 {OBJ}', f'scoreboard players operation #ly {OBJ} -= #h {OBJ}',
        f'execute if score #ly {OBJ} matches ..-1 run scoreboard players set #ly {OBJ} 0',
        f'execute if score #ly {OBJ} matches {ARC_LIFT + 1}.. run scoreboard players set #ly {OBJ} {ARC_LIFT}',
        f'scoreboard players operation #h {OBJ} += #ly {OBJ}',
        f'scoreboard players operation #m {OBJ} = #h {OBJ}', f'scoreboard players operation #m {OBJ} *= #c100 {OBJ}',
        f'scoreboard players operation #m {OBJ} /= #f {OBJ}', f'scoreboard players operation #r {OBJ} < #m {OBJ}',
        f'execute if score #r {OBJ} matches ..4 run scoreboard players set #r {OBJ} 5'])
    W.w('e/sinf', ['# Internal (macro {i}): #f = sin(i deg) per mille, i 0..90.',
                   f'$execute store result score #f {OBJ} run data get storage {STO} fx.sin[$(i)]'])
    W.w('e/clamp_band', [
        '# qi_band clamp: #l len (tenths), #p pitch (the in-plane rise, degrees), #o roll (the lean, degrees) -> #ly the lift',
        '# (hundredths) so the band\'s lowest point (half its length x sin |pitch| + its half height) stays 0.05 b over the',
        '# floor; #my #mz / #ny #nz = the 2.5 / 2.6 b sweep in the leaning display frame (level in the world).',
        f'scoreboard players operation #i {OBJ} = #p {OBJ}',
        f'execute if score #i {OBJ} matches ..-1 run scoreboard players operation #i {OBJ} *= #cm1 {OBJ}',
        f'execute if score #i {OBJ} matches 91.. run scoreboard players set #i {OBJ} 90',
        f'execute store result storage {STO} fx.q.i int 1 run scoreboard players get #i {OBJ}',
        f'function {E}sinf with storage {STO} fx.q',
        f'scoreboard players operation #d {OBJ} = #l {OBJ}', f'scoreboard players operation #d {OBJ} *= #f {OBJ}',
        f'scoreboard players operation #d {OBJ} /= #c100 {OBJ}', f'scoreboard players operation #d {OBJ} /= #c2 {OBJ}',
        f'scoreboard players operation #a {OBJ} = #l {OBJ}', f'scoreboard players operation #a {OBJ} *= #c3 {OBJ}',
        f'scoreboard players operation #a {OBJ} /= #c4 {OBJ}', f'scoreboard players operation #d {OBJ} += #a {OBJ}',
        f'scoreboard players add #d {OBJ} 5',
        f'function {E}hgt',
        f'scoreboard players operation #ly {OBJ} = #d {OBJ}', f'scoreboard players operation #ly {OBJ} -= #h {OBJ}',
        f'execute if score #ly {OBJ} matches ..-1 run scoreboard players set #ly {OBJ} 0',
        '# the level sweep: sin / cos of the lean',
        f'scoreboard players operation #i {OBJ} = #o {OBJ}',
        f'execute if score #i {OBJ} matches ..-1 run scoreboard players operation #i {OBJ} *= #cm1 {OBJ}',
        f'execute if score #i {OBJ} matches 91.. run scoreboard players set #i {OBJ} 90',
        f'execute store result storage {STO} fx.q.i int 1 run scoreboard players get #i {OBJ}',
        f'function {E}sinf with storage {STO} fx.q',
        f'scoreboard players operation #my {OBJ} = #f {OBJ}',
        f'execute if score #o {OBJ} matches ..-1 run scoreboard players operation #my {OBJ} *= #cm1 {OBJ}',
        f'scoreboard players operation #ny {OBJ} = #my {OBJ}',
        f'scoreboard players operation #my {OBJ} /= #c4 {OBJ}', f'scoreboard players operation #ny {OBJ} *= #c26 {OBJ}',
        f'scoreboard players operation #ny {OBJ} /= #c100 {OBJ}',
        f'scoreboard players operation #j {OBJ} = #i {OBJ}', f'scoreboard players operation #i {OBJ} = #c90 {OBJ}',
        f'scoreboard players operation #i {OBJ} -= #j {OBJ}',
        f'execute store result storage {STO} fx.q.i int 1 run scoreboard players get #i {OBJ}',
        f'function {E}sinf with storage {STO} fx.q',
        f'scoreboard players operation #mz {OBJ} = #f {OBJ}', f'scoreboard players operation #nz {OBJ} = #f {OBJ}',
        f'scoreboard players operation #mz {OBJ} /= #c4 {OBJ}', f'scoreboard players operation #nz {OBJ} *= #c26 {OBJ}',
        f'scoreboard players operation #nz {OBJ} /= #c100 {OBJ}'])
    W.w('e/lowf', ['# Internal (macro {i}): #f = the floor-clamp table entry i.',
                   f'$execute store result score #f {OBJ} run data get storage {STO} fx.low[$(i)]'])
    W.w('e/clamp_line', [
        '# qi_line clamp (after e/hgt): a line pointing down (pitch >= 30) ends 0.1 b above the floor: #r (tenths) <= the',
        '# height over the floor / sin(pitch) (taken at the low edge of the pitch band: 30 -> x 2, 60 -> x 1.15, 80 -> x 1).',
        f'execute if score #pt {OBJ} matches ..29 run return 0',
        f'scoreboard players operation #m {OBJ} = #h {OBJ}', f'scoreboard players remove #m {OBJ} 10',
        f'execute if score #m {OBJ} matches ..9 run scoreboard players set #m {OBJ} 10',
        f'scoreboard players operation #m {OBJ} /= #c10 {OBJ}',
        f'execute if score #pt {OBJ} matches 30..59 run scoreboard players operation #m {OBJ} *= #c2 {OBJ}',
        f'execute if score #pt {OBJ} matches 60..79 run scoreboard players operation #m {OBJ} *= #c115 {OBJ}',
        f'execute if score #pt {OBJ} matches 60..79 run scoreboard players operation #m {OBJ} /= #c100 {OBJ}',
        f'scoreboard players operation #r {OBJ} < #m {OBJ}',
        f'execute if score #r {OBJ} matches ..0 run scoreboard players set #r {OBJ} 1'])
    W.w('e/beam_new', ['# Internal: as the new moonbeam marker (summoned at the beam\'s foot).', f'tag @s add {TAG}',
                       f'tag @s add {BEAM}', f'tag @s add {BEAM}_n', 'tag @s add rlk_room', 'tag @s add rlk_mb_aux'])
    W.w('e/beam', [
        '# As / at a moonbeam marker (each ager tick): the front at h x D / S (tenths over the foot) falls from h to 0;',
        '# particles at the front and along the lit column above it; a flash at the foot when it arrives; then gone.',
        f'scoreboard players operation #f {OBJ} = @s hrFxG', f'scoreboard players operation #f {OBJ} *= @s hrFxD',
        f'scoreboard players operation #f {OBJ} /= @s hrFxS',
        f'execute store result storage {STO} fx.bm.f float 0.1 run scoreboard players get #f {OBJ}',
        f'scoreboard players operation #c {OBJ} = @s hrFxG', f'scoreboard players operation #c {OBJ} += #f {OBJ}',
        f'execute store result storage {STO} fx.bm.c float 0.05 run scoreboard players get #c {OBJ}',
        f'scoreboard players operation #c {OBJ} = @s hrFxG', f'scoreboard players operation #c {OBJ} -= #f {OBJ}',
        f'execute store result storage {STO} fx.bm.d float 0.05 run scoreboard players get #c {OBJ}',
        f'function {E}beam_d with storage {STO} fx.bm',
        'execute if score @s hrFxD matches ..0 run ' + part('end_rod', '~ ~0.2 ~', (0.3, 0.3, 0.3), 0.05, 8),
        'scoreboard players remove @s hrFxD 1',
        'execute if score @s hrFxD matches ..-1 run kill @s'])
    W.w('e/beam_d', ['# Internal (macro {f c d}): one moonbeam frame.',
                     mac(part('end_rod', '~ ~$(f) ~', (0.05, 0.05, 0.05), 0.0, 2)),
                     mac(dust(DUST_SILVER, 1.4, '~ ~$(f) ~', (0.08, 0.08, 0.08), 3)),
                     mac(dust(DUST_SILVER, 1.0, '~ ~$(c) ~', (0.06, '$(d)', 0.06), 4))])
    W.w('clear', ['# Remove every kit card (all pools) and moonbeam. Safe to call any time (pause, death_start, cleanup).',
                  '# Props (the module\'s displays and the seat rock\'s items) are not cards: they stay.',
                  f'kill {SEL}]', f'kill @e[type=minecraft:marker,tag={BEAM}]', INIT,
                  f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #na {OBJ} 0', f'scoreboard players set #ni {OBJ} 0'])
    W.w('uninstall', ['# Remove the kit\'s cards, moonbeams, followers, demo stand-ins, the HUD lines, the warn bossbar, the',
                      '# objectives, storage rlk:hr fx (other keys kept) and the schedules (the module\'s uninstall hook).',
                      f'execute if data storage {STO} fx{{init:1b}} run function {FN}hud/clear',
                      f'kill {SEL}]', f'kill @e[type=minecraft:marker,tag={BEAM}]',
                      f'kill @e[type=minecraft:item_display,tag={FOLLOW}]', f'kill @e[type=minecraft:item_display,tag={FOLLOW_STAY}]',
                      f'kill @e[tag={DEMO}]', f'tag @e[tag={LEAD}] remove {LEAD}',
                      *[f'tag @e[tag={t}] remove {t}' for t in (f'{ANIM}_d', f'{ANIM}_p', ANIM)],
                      f'bossbar remove {WARN_BAR}',
                      f'scoreboard objectives remove {OBJ}', *[f'scoreboard objectives remove {o}' for o in OBJECTIVES],
                      f'data remove storage {STO} fx',
                      f'schedule clear {E}world', f'schedule clear {E}anim', f'schedule clear {FN}hud/e/ln',
                      f'schedule clear {FN}test/e/tick', f'schedule clear {FN}test/e/hud2', f'schedule clear {FN}test/e/hud3'])
    W.w('look', [
        '# Dress @s (an item_display the module owns) as a kit sprite: {kind, col:<RGB int>}. Full bright; the caller',
        '# keeps its own transformation / billboard.',
        '$data merge entity @s {item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        f'"{NS_TEX}$(kind)","minecraft:custom_model_data":{{colors:[$(col)]}}}}}},brightness:{{sky:15,block:15}}}}',
    ])
    # --- the prop chain: followers, the disc spin, the petal rock
    spin = []
    for k, q in enumerate(DISC_Q):
        spin.append(f'execute if score #af {OBJ} matches {k} as @e[type=minecraft:item_display,tag={ANIM}_d] run data merge '
                    f'entity @s {{start_interpolation:0,interpolation_duration:3,transformation:{{left_rotation:{q}}}}}')
        spin.append(f'execute if score #af {OBJ} matches {k} as @e[type=minecraft:item_display,tag={ANIM}_d] run data modify '
                    f'entity @s item.components."minecraft:item_model" set value "{NS_TEX}disc_{k % 2}"')
    rock = [f'execute if score #af {OBJ} matches {t} as @e[type=minecraft:item_display,tag={ANIM}_p] run data merge entity @s '
            f'{{start_interpolation:0,interpolation_duration:20,transformation:{{left_rotation:{{angle:{a}f,axis:[0f,0f,1f]}}}}}}'
            for t, a in ((0, '0.17'), (20, '-0.17'))]
    W.w('e/anim', [
        '# The prop chain (scheduled every tick while a kit-animated prop or a follower exists; no hook in rlk:tick):',
        '# followers stay on their lead (or keep their spot) and go with it, the discs turn a quarter every 3 t (30 deg / t)',
        '# swapping their two frames, the big petals rock slowly.',
        f'execute unless entity @e[type=minecraft:item_display,tag={ANIM},limit=1] unless entity @e[type=minecraft:item_display,'
        f'tag={FOLLOW},limit=1] unless entity @e[type=minecraft:item_display,tag={FOLLOW_STAY},limit=1] run return 0',
        f'scoreboard players add #at {OBJ} 1',
        f'execute as @e[type=minecraft:item_display,tag={FOLLOW}] run function {E}follow',
        f'execute as @e[type=minecraft:item_display,tag={FOLLOW_STAY}] run function {E}stay',
        f'function {E}anim_d',
        *spin,
        f'function {E}anim_p',
        *rock,
        f'execute if entity @e[type=minecraft:item_display,tag={ANIM},limit=1] run schedule function {E}anim 1t replace',
        f'execute if entity @e[type=minecraft:item_display,tag={FOLLOW},limit=1] run schedule function {E}anim 1t replace',
        f'execute if entity @e[type=minecraft:item_display,tag={FOLLOW_STAY},limit=1] run schedule function {E}anim 1t replace'])
    W.w('e/anim_d', [
        '# Internal: #af = the disc quarter turn (#at / 3) % 4 on the ticks with #at % 3 = 0, else -1 (no change).',
        f'scoreboard players operation #g {OBJ} = #at {OBJ}', f'scoreboard players set #k {OBJ} 3',
        f'scoreboard players operation #g {OBJ} %= #k {OBJ}',
        f'execute unless score #g {OBJ} matches 0 run return run scoreboard players set #af {OBJ} -1',
        f'scoreboard players operation #af {OBJ} = #at {OBJ}', f'scoreboard players operation #af {OBJ} /= #k {OBJ}',
        f'scoreboard players set #k {OBJ} 4', f'scoreboard players operation #af {OBJ} %= #k {OBJ}'])
    W.w('e/anim_p', [
        '# Internal: #af = #at % 40 when it is 0 or 20 (the petal rock\'s turns), else -1.',
        f'scoreboard players operation #af {OBJ} = #at {OBJ}', f'scoreboard players set #k {OBJ} 40',
        f'scoreboard players operation #af {OBJ} %= #k {OBJ}',
        f'execute unless score #af {OBJ} matches 0 unless score #af {OBJ} matches 20 run scoreboard players set #af {OBJ} -1'])
    W.w('e/follow', [
        '# As a follower display: on its lead (the same hrFxL), or gone with it.',
        f'scoreboard players operation #l {OBJ} = @s hrFxL',
        f'execute as @e[tag={LEAD}] if score @s hrFxL = #l {OBJ} run tag @s add {TAG}_t',
        f'execute unless entity @e[tag={TAG}_t,limit=1] run return run kill @s',
        f'execute at @e[tag={TAG}_t,limit=1] run tp @s ~ ~ ~',
        f'tag @e[tag={TAG}_t] remove {TAG}_t'])
    W.w('e/stay', [
        '# As a staying follower (the seat rock\'s bottle / cup): it keeps its spot and goes when its lead is gone.',
        f'scoreboard players operation #l {OBJ} = @s hrFxL',
        f'execute as @e[tag={LEAD}] if score @s hrFxL = #l {OBJ} run tag @s add {TAG}_t',
        f'execute unless entity @e[tag={TAG}_t,limit=1] run return run kill @s',
        f'tag @e[tag={TAG}_t] remove {TAG}_t'])


def _dress(kind, sc, bb, anim=None, item='minecraft:paper', bright=True, trans=(0, 0, 0), extra='', tint=WHITE):
    """the data merge that dresses @s as a kit card (tinted: white = as painted) / a vanilla item display"""
    sx, sy, sz = sc if isinstance(sc, tuple) else (sc, sc, sc)
    tr = (f'transformation:{{translation:[{num(trans[0])}f,{num(trans[1])}f,{num(trans[2])}f],left_rotation:[0f,0f,0f,1f],'
          f'scale:[{num(sx)}f,{num(sy)}f,{num(sz)}f],right_rotation:[0f,0f,0f,1f]}}')
    if kind:
        it = (f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{NS_TEX}{kind}",'
              f'"minecraft:custom_model_data":{{colors:[{tint}]}}}}}}')
    else:
        it = f'item:{{id:"{item}",count:1{extra}}}'
    br = ',brightness:{sky:15,block:15}' if bright else ''
    out = [f'data merge entity @s {{{it},item_display:"none",billboard:"{bb}"{br},view_range:2f,shadow_radius:0f,{tr}}}']
    if anim:
        out += [f'tag @s add {ANIM}', f'tag @s add {ANIM}_{anim}', f'schedule function {E}anim 1t replace']
    return out


def props(W):
    P_ = FN + 'prop/'
    sel_new = f'@e[type=minecraft:item_display,tag={TAG}_nf]'
    W.w('prop/e/link', ['# Internal: @s (the lead) gets a link id (once) and the lead tag; its old followers go (#l = the id).',
                        f'execute unless score @s hrFxL matches 1.. run scoreboard players add #lid {OBJ} 1',
                        f'execute unless score @s hrFxL matches 1.. run scoreboard players operation @s hrFxL = #lid {OBJ}',
                        f'scoreboard players operation #l {OBJ} = @s hrFxL', f'tag @s add {LEAD}',
                        f'execute as @e[type=minecraft:item_display,tag={FOLLOW}] if score @s hrFxL = #l {OBJ} run kill @s',
                        f'execute as @e[type=minecraft:item_display,tag={FOLLOW_STAY}] if score @s hrFxL = #l {OBJ} run kill @s'])
    for name, (doc, looks, bb, anim) in PROPS.items():
        head = [f'# {doc}', '# @s = the item_display the caller summoned and rotated (dressed in place, idempotent; calling it',
                '# again with another look re-looks it); any other entity (a marker) gets one follower display the kit keeps',
                '# on it and removes with it.', INIT]
        if name == 'seat_rock':
            continue
        if None in looks:                     # no look arg (the disc)
            kind, sc = looks[None]
            W.w(f'prop/e/{name}_d', [f'# Internal: dress @s as {name}.'] + _dress(kind, sc, bb, anim))
            W.w(f'prop/{name}', head + [
                f'execute if entity @s[type=minecraft:item_display] run return run function {P_}e/{name}_d',
                f'function {P_}e/link',
                f'execute at @s run summon minecraft:item_display ~ ~ ~ {{Tags:["{FOLLOW}","{TAG}_nf","rlk_room","rlk_mb_aux"],'
                'teleport_duration:1}',
                f'execute as {sel_new} at @s rotated as @s run function {P_}e/{name}_f'])
            W.w(f'prop/e/{name}_f', ['# Internal: as the new follower display: linked to the lead (#l), dressed.',
                                     f'tag @s remove {TAG}_nf', f'scoreboard players operation @s hrFxL = #l {OBJ}',
                                     f'function {P_}e/{name}_d', f'schedule function {E}anim 1t replace'])
            continue
        disp = []
        for lk, (kind, sc, *tint) in looks.items():
            if kind is None:
                body = [f'data merge entity @s {{transformation:{{scale:[0f,0f,0f]}}}}']
            else:
                body = _dress(kind, sc, bb, anim, tint=tint[0] if tint else WHITE)
            W.w(f'prop/e/{name}_{lk}', [f'# Internal: dress @s as {name}, look {lk}.'] + body)
            disp.append(f'execute if data storage {STO} fx{{lk:"{lk}"}} run return run function {P_}e/{name}_{lk}')
        W.w(f'prop/e/{name}_x', [f'# Internal: dress @s as {name} in the look of storage fx.lk.'] + disp)
        W.w(f'prop/{name}', head + [
            f'$data modify storage {STO} fx.lk set value "$(look)"',
            f'execute if entity @s[type=minecraft:item_display] run return run function {P_}e/{name}_x',
            f'function {P_}e/link',
            f'execute at @s run summon minecraft:item_display ~ ~ ~ {{Tags:["{FOLLOW}","{TAG}_nf","rlk_room","rlk_mb_aux"],'
            'teleport_duration:1}',
            f'execute as {sel_new} at @s run function {P_}e/{name}_f'])
        W.w(f'prop/e/{name}_f', ['# Internal: as the new follower display: linked to the lead (#l), dressed.',
                                 f'tag @s remove {TAG}_nf', f'scoreboard players operation @s hrFxL = #l {OBJ}',
                                 f'function {P_}e/{name}_x', f'schedule function {E}anim 1t replace'])
    # the seat rock: the stone (vanilla tuff) on @s, the bottle / cup as staying followers
    rk, rtr, rsc = SEAT['rock']
    W.w('prop/e/seat_rock_d', ['# Internal: dress @s as the seat stone (vanilla tuff, natural light), then its items for fx.lk.']
        + _dress(None, rsc, 'fixed', item=rk, bright=False, trans=rtr)
        + [f'function {P_}e/link',
           f'execute if data storage {STO} fx{{lk:"bottle"}} at @s rotated as @s rotated ~ 0 run function {P_}e/seat_bottle',
           f'execute if data storage {STO} fx{{lk:"set"}} at @s rotated as @s rotated ~ 0 run function {P_}e/seat_bottle',
           f'execute if data storage {STO} fx{{lk:"set"}} at @s rotated as @s rotated ~ 0 run function {P_}e/seat_cup',
           f'schedule function {E}anim 1t replace'])
    for part_, (it, (x, y, z), sc) in (('bottle', SEAT['bottle']), ('cup', SEAT['cup'])):
        extra = (f',components:{{"minecraft:potion_contents":{{custom_color:{BOTTLE_COLOR}}}}}' if part_ == 'bottle' else '')
        W.w(f'prop/e/seat_{part_}', [
            f'# Internal (at / rotated as the stone, #l = its link): the {part_} on the stone\'s top ({"her left" if part_ == "bottle" else "her right"}),',
            '# a vanilla item display turning to the viewer, standing on the top.',
            f'summon minecraft:item_display ^{num(x)} ^{num(y)} ^{num(z)} {{Tags:["{FOLLOW_STAY}","{TAG}_nf","{api.TAGS["deco"]}",'
            f'"rlk_room","rlk_mb_aux"],item:{{id:"{it}",count:1{extra}}},item_display:"none",billboard:"vertical",'
            f'view_range:2f,shadow_radius:0f,transformation:{{translation:[0f,{num(sc / 2)}f,0f],left_rotation:[0f,0f,0f,1f],'
            f'scale:[{num(sc)}f,{num(sc)}f,{num(sc)}f],right_rotation:[0f,0f,0f,1f]}}}}',
            f'scoreboard players operation {sel_new} hrFxL = #l {OBJ}', f'tag {sel_new} remove {TAG}_nf'])
    W.w('prop/seat_rock', [f'# {PROPS["seat_rock"][0]}',
                           '# @s = the item_display the caller summoned at the floor point and rotated toward the moon (dressed',
                           '# in place; calling it again re-looks it: the old items go). Any other entity: nothing.', INIT,
                           f'$data modify storage {STO} fx.lk set value "$(look)"',
                           f'execute if entity @s[type=minecraft:item_display] run function {P_}e/seat_rock_d'])


def sounds(W):
    for name, layers in SOUNDS.items():
        W.w(f'snd/{name}', ['# Layers: event volume pitch minVolume (mboss_lib.sound rule; api.KIT_SOUND_RECIPES).'] +
            [sound_line(*l) for l in layers])


# ----------------------------------------------------------------------------- HUD
def typed(text):
    """Raiden's typewriter steps (tools/raiden_enc/lines.py): each word grows at most two syllables at a time;
    punctuation stays on its syllable, except the closing punctuation, which lands as the last step."""
    PUNCT = '.,!?…'
    body = text.rstrip(PUNCT)
    tail = text[len(body):]
    steps, done = [], ''
    for word in body.split(' '):
        sylls = []
        for ch in word:
            if ch in PUNCT and sylls:
                sylls[-1] += ch
            else:
                sylls.append(ch)
        for k in range(0, len(sylls), 2):
            steps.append(done + ''.join(sylls[:k + 2]))
        done = steps[-1] + ' '
    if tail:
        steps.append(text)
    return steps


def line_steps(lid):
    """[(text, stay, fade, ttl, gap)] of api.LINES[lid]: two syllables per LINE_GAP t; the full line holds until
    api.LINE_AT[lid][2] t after the line started (its ticks on screen), then fades over LINE_FADE t"""
    steps = typed(api.LINES[lid])
    hold = api.LINE_AT[lid][2]
    out = []
    for k, text in enumerate(steps):
        last = k == len(steps) - 1
        stay = hold - LINE_GAP * k if last else LINE_GAP + 6
        fade = LINE_FADE if last else 0
        assert not last or stay >= 10, (lid, stay)
        out.append((text, stay, fade, stay + fade, LINE_GAP))
    return out


def hud_funcs(W):
    H = FN + 'hud/'
    sub = '{text:"$(t)",color:"' + LINE_COL + '",font:"minecraft:default"}'
    W.w('hud/line', [f'# {{id}}: her line api.LINES[id] (ids {min(api.LINES)}..{max(api.LINES)}) on the subtitle slot, Raiden\'s letter',
                     f'# reveal (two syllables per {LINE_GAP} t, block.note_block.hat 0.3 each), colour {LINE_COL}, held until',
                     '# api.LINE_AT[id][2] t after it started, then gone; a new line replaces a running one. Overlay-aware: while',
                     '# a full-screen overlay (fx/hud/ovl) is up, each step re-sends the overlay glyph as the title with its',
                     '# remaining hold instead of view/ttl_blank, and when the overlay ends the line comes back on a blank title.',
                     f'$function {H}l/$(id)'])
    for lid in api.LINES:
        steps = line_steps(lid)
        q = []
        for text, stay, fade, ttl, gap in steps:
            assert '"' not in text and '\\' not in text, text
            q.append(f'{{t:"{text}",s:{stay},f:{fade},n:{ttl},g:{gap}}}')
        W.w(f'hud/l/{lid}', [f'# Line {lid}: 「{api.LINES[lid]}」 ({len(steps)} steps, {api.LINE_AT[lid][2]} t on screen).', INIT,
                             f'data modify storage {STO} fx.ln set value {{q:[{",".join(q)}]}}',
                             f'scoreboard players set #lnW {OBJ} 0', f'scoreboard players set #lnA {OBJ} 1',
                             f'execute store result score #lnE {OBJ} run time query gametime',
                             f'scoreboard players add #lnE {OBJ} {api.LINE_AT[lid][2]}',
                             f'function {H}e/ln'])
    W.w('hud/e/ln', ['# Internal: the running line (a 1 t chain to the line\'s end): the next step when its gap is over; when an',
                     '# overlay ends while the line is still up, the line again on a blank title.',
                     f'execute unless score #lnA {OBJ} matches 1 run return 0',
                     f'execute if entity @a[tag=player,scores={{dead=1}}] run return run function {H}e/ln_stop',
                     f'execute store result score #now2 {OBJ} run time query gametime',
                     f'execute if score #ovE {OBJ} = #now2 {OBJ} if score #lnE {OBJ} > #now2 {OBJ} unless data storage {STO} fx.ln.q[0] '
                     f'run function {H}e/ln_again',
                     f'execute if data storage {STO} fx.ln.q[0] run scoreboard players remove #lnW {OBJ} 1',
                     f'execute if data storage {STO} fx.ln.q[0] if score #lnW {OBJ} matches ..0 run function {H}e/ln_step',
                     f'execute if score #lnE {OBJ} <= #now2 {OBJ} run return run scoreboard players set #lnA {OBJ} 0',
                     f'schedule function {H}e/ln 1t replace'])
    W.w('hud/e/ln_step', ['# Internal: show the first queued step and drop it.',
                          f'execute store result score #lnW {OBJ} run data get storage {STO} fx.ln.q[0].g',
                          f'data modify storage {STO} fx.ln.cur set from storage {STO} fx.ln.q[0].t',
                          f'function {H}e/ln_show with storage {STO} fx.ln.q[0]',
                          f'data remove storage {STO} fx.ln.q[0]'])
    W.w('hud/e/ln_show', ['# Internal (macro: t text, s stay, f fade, n ttlT): one typing step on the subtitle line.',
                          f'$title @a[tag=player] subtitle {sub}',
                          'execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0',
                          f'execute store result score #now2 {OBJ} run time query gametime',
                          f'execute if score #ovE {OBJ} > #now2 {OBJ} run return run function {H}e/ov_keep',
                          '$title @a[tag=player] times 0 $(s) $(f)',
                          'execute as @a[tag=player] run function rlk:view/ttl_blank',
                          '$scoreboard players set @a[tag=player] ttlT $(n)'])
    W.w('hud/e/ov_keep', ['# Internal: an overlay is up: re-send its glyph as the title with its remaining hold / fade-out (the new',
                          '# subtitle shows on it).',
                          f'scoreboard players operation #a {OBJ} = #ovH {OBJ}', f'scoreboard players operation #a {OBJ} -= #now2 {OBJ}',
                          f'execute if score #a {OBJ} matches ..-1 run scoreboard players set #a {OBJ} 0',
                          f'scoreboard players operation #b {OBJ} = #ovE {OBJ}', f'scoreboard players operation #b {OBJ} -= #now2 {OBJ}',
                          f'scoreboard players operation #b {OBJ} -= #a {OBJ}',
                          f'execute store result storage {STO} fx.ov.hl int 1 run scoreboard players get #a {OBJ}',
                          f'execute store result storage {STO} fx.ov.ol int 1 run scoreboard players get #b {OBJ}',
                          f'scoreboard players operation #a {OBJ} += #b {OBJ}',
                          f'execute store result score @a[tag=player] ttlT run scoreboard players get #a {OBJ}',
                          f'function {H}e/ov_re with storage {STO} fx.ov'])
    W.w('hud/e/ov_re', ['# Internal (macro: ch the glyph, hl hold left, ol fade-out left).',
                        '$title @a[tag=player] times 0 $(hl) $(ol)',
                        f'$title @a[tag=player] title {glyph_title("$(ch)")}'])
    W.w('hud/e/ln_again', ['# Internal: the overlay just ended and the line is still up: show it again on a blank title for the rest.',
                           f'scoreboard players operation #a {OBJ} = #lnE {OBJ}', f'scoreboard players operation #a {OBJ} -= #now2 {OBJ}',
                           f'execute store result storage {STO} fx.ln.rs int 1 run scoreboard players get #a {OBJ}',
                           f'function {H}e/ln_again_m with storage {STO} fx.ln'])
    W.w('hud/e/ln_again_m', ['# Internal (macro: cur the line text, rs the ticks left).',
                             f'$title @a[tag=player] times 0 $(rs) {LINE_FADE}',
                             '$title @a[tag=player] subtitle {text:"$(cur)",color:"' + LINE_COL + '",font:"minecraft:default"}',
                             'execute as @a[tag=player] run function rlk:view/ttl_blank',
                             '$scoreboard players set @a[tag=player] ttlT $(rs)'])
    W.w('hud/e/ln_stop', ['# Internal: stop the running line and blank it.', f'data remove storage {STO} fx.ln',
                          f'schedule clear {H}e/ln', f'execute unless score #lnA {OBJ} matches 1 run return 0',
                          f'scoreboard players set #lnA {OBJ} 0', f'scoreboard players set #lnE {OBJ} 0',
                          'title @a[tag=player] subtitle ""',
                          'scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0'])
    W.w('hud/ovl', [
        '# {g,in,hold,out}: a full-screen overlay glyph on the title (g = black / negative / pinkwhite / red_tint / magenta /',
        '# white; font rlk:mboss_hr, an empty unstyled root, no text shadow): fade-in in, hold, fade-out out ticks; vBig =',
        '# in + hold + out rests the F5 crosshair title meanwhile. A running line keeps its text on the overlay (else the',
        '# subtitle is blanked first). `negative` is an approximation (titles can only paint over the screen).', INIT,
        f'$data modify storage {STO} fx.ov set value {{g:"$(g)"}}',
        f'$data modify storage {STO} fx.ov.ch set from storage {STO} fx.gl.$(g)',
        f'$scoreboard players set #oi {OBJ} $(in)', f'$scoreboard players set #oh {OBJ} $(hold)',
        f'$scoreboard players set #oo {OBJ} $(out)',
        f'execute store result score #ovH {OBJ} run time query gametime',
        f'scoreboard players operation #ovH {OBJ} += #oi {OBJ}', f'scoreboard players operation #ovH {OBJ} += #oh {OBJ}',
        f'scoreboard players operation #ovE {OBJ} = #ovH {OBJ}', f'scoreboard players operation #ovE {OBJ} += #oo {OBJ}',
        f'scoreboard players operation #a {OBJ} = #oi {OBJ}', f'scoreboard players operation #a {OBJ} += #oh {OBJ}',
        f'scoreboard players operation #a {OBJ} += #oo {OBJ}',
        f'execute store result score @a[tag=player] vBig run scoreboard players get #a {OBJ}',
        f'execute unless score #lnA {OBJ} matches 1 run title @a[tag=player] subtitle ""',
        '$title @a[tag=player] times $(in) $(hold) $(out)',
        f'function {H}e/ov_t with storage {STO} fx.ov',
        f'execute if score #lnA {OBJ} matches 1 run schedule function {H}e/ln 1t replace'])
    W.w('hud/e/ov_t', ['# Internal (macro: ch the glyph).', f'$title @a[tag=player] title {glyph_title("$(ch)")}'])
    W.w('hud/e/ov_off', ['# Internal: an overlay still up goes at once (cleanup).',
                         f'execute store result score #now2 {OBJ} run time query gametime',
                         f'execute unless score #ovE {OBJ} > #now2 {OBJ} run return run scoreboard players set #ovE {OBJ} 0',
                         f'scoreboard players set #ovE {OBJ} 0', f'scoreboard players set #ovH {OBJ} 0',
                         'scoreboard players set @a[tag=player] vBig 0', 'title @a[tag=player] clear'])
    W.w('hud/warn', [
        f'# {{on}}: the instant-death warning (PLAN §5.5) on its own line under the boss bars: bossbar {WAR_BAR_DOC} named',
        f'# api.WARN_TEXT, white with 「{api.WARN_HL[0]}」 in {api.WARN_HL[1]} (no bar: the pack\'s white progress is invisible); 0 = off.',
        '# Only while a gauntlet whose fail is lethal runs (the callers check the switch).', INIT,
        f'$scoreboard players set #on {OBJ} $(on)',
        f'execute unless score #on {OBJ} matches 1 run return run function {H}e/warn_off',
        f'bossbar add {WARN_BAR} {{text:""}}', f'bossbar set {WARN_BAR} name {warn_component()}',
        f'bossbar set {WARN_BAR} color white', f'bossbar set {WARN_BAR} style progress', f'bossbar set {WARN_BAR} max 1',
        f'bossbar set {WARN_BAR} value 0', f'bossbar set {WARN_BAR} players @a[tag=player]',
        f'bossbar set {WARN_BAR} visible true', f'data modify storage {STO} fx.hud.warn set value 1b'])
    W.w('hud/e/warn_off', ['# Internal: the warning off (no error when it was never made).',
                           f'execute unless data storage {STO} fx.hud{{warn:1b}} run return 0',
                           f'bossbar set {WARN_BAR} visible false', f'bossbar set {WARN_BAR} players',
                           f'data modify storage {STO} fx.hud.warn set value 0b'])
    skip = [f'# {{s}}: the intro\'s skip prompt on the actionbar (PLAN §3.1): 「{api.SKIP_TEXT}」 (the original\'s, verbatim) at',
            f'# brightness step s 0..{api.SKIP_STEPS} (grey {api.SKIP_COLOR} -> white while Shift is held) and the hint 「{api.SKIP_HINT}」',
            '# (grey); hudHold 2 (the caller sends it every tick, so the regular actionbar HUD rests); s 5 clears it.', INIT,
            f'$scoreboard players set #sk {OBJ} $(s)',
            f'execute if score #sk {OBJ} matches 5.. run return run function {H}e/skip_off']
    for k in range(api.SKIP_STEPS + 1):
        rng = '..0' if k == 0 else str(k)
        skip.append(f'execute if score #sk {OBJ} matches {rng} run title @a[tag=player] actionbar {skip_component(k)}')
    skip += ['scoreboard players set @a[tag=player] hudHold 2', f'data modify storage {STO} fx.hud.skip set value 1b']
    W.w('hud/skip', skip)
    W.w('hud/e/skip_off', ['# Internal: the skip prompt off.', 'title @a[tag=player] actionbar ""',
                           'scoreboard players set @a[tag=player] hudHold 0', f'data modify storage {STO} fx.hud.skip set value 0b'])
    W.w('hud/clear', ['# The line, an overlay still up, the warning and the skip prompt off (cleanup, the coda, uninstall).', INIT,
                      f'function {H}e/ln_stop', f'function {H}e/ov_off', f'function {H}e/warn_off',
                      f'execute if data storage {STO} fx.hud{{skip:1b}} run function {H}e/skip_off'])


WAR_BAR_DOC = api.WARN_BOSSBAR


# ----------------------------------------------------------------------------- presets -> datapack
def preset_variants(name):
    _d, _a, f, _c, split, _p = PRESETS[name]
    if not split:
        return {None: f()}
    return {c: f(c) for c in SPLIT_CS.get(name, C_ALL)}


def presets_dp(W):
    for name, (doc, args, f, conv, split, pre) in PRESETS.items():
        head = [f'# {doc}']
        if args:
            head.append('# {' + ', '.join(args) + '} (macro: tenths of a block, degrees, ticks; c 1 lilac 2 pink-magenta 3 yellow '
                        '4 crimson 5 white)')
        if name in AMBIENT:
            head.append(f'# Ambient: its cards go to the ambient pool (cap {CAP_AMB}; the ager removes the oldest).')
        variants = preset_variants(name)
        if name in PTCL and name != 'ev_beam':
            assert not any(f'{FN}card' in l for b in variants.values() for l in b), name
        if not args and not pre and not conv:
            body = variants[None]
            assert not any(l.startswith('$') for l in body), name
            W.w(f'p/{name}', head + [INIT] + body)
            continue
        pub = list(head) + [INIT]
        if 'c' in args:
            pub.append(f'$scoreboard players set #c {OBJ} $(c)')
        pub.append(f'data modify storage {PA} set value {{}}')
        pub += pre
        for cv in conv:
            key, src, scale = cv[0], cv[1], cv[2]
            add = cv[3] if len(cv) > 3 else 0
            frac = cv[4] if len(cv) > 4 else None
            if src.startswith('#'):
                pub.append(f'execute store result storage {PA}.{key} float {num(scale, 7)} run scoreboard players get {src} {OBJ}')
            elif frac is not None:
                pub.append(f'$execute store result storage {PA}.{key} int {num(frac, 5)} run scoreboard players set #a {OBJ} $({src})')
            elif scale is None:
                if add:
                    pub.append(f'$scoreboard players set #a {OBJ} $({src})')
                    pub.append(f'execute store result storage {PA}.{key} int 1 run scoreboard players add #a {OBJ} {add}')
                else:
                    pub.append(f'$data modify storage {PA}.{key} set value $({src})')
            else:
                pub.append(f'$execute store result storage {PA}.{key} float {num(scale, 7)} run scoreboard players set #a '
                           f'{OBJ} $({src})')
        if split:
            cs = list(variants)
            for c in cs[1:]:
                body = variants[c]
                w = f' with storage {PA}' if any(l.startswith('$') for l in body) else ''
                pub.append(f'execute if score #c {OBJ} matches {c} run return run function {FN}p/e/{name}_{c}{w}')
            body1 = variants[cs[0]]
            w1 = f' with storage {PA}' if any(l.startswith('$') for l in body1) else ''
            pub.append(f'function {FN}p/e/{name}_{cs[0]}{w1}')
            for c, body in variants.items():
                W.w(f'p/e/{name}_{c}', [f'# Internal of p/{name}, c {c}' + (f' (macro, storage {PA}).' if
                                                                              any(l.startswith('$') for l in body) else '.')] + body)
        else:
            body = variants[None]
            if any(l.startswith('$') for l in body):
                pub.append(f'function {FN}p/e/{name} with storage {PA}')
                W.w(f'p/e/{name}', [f'# Internal (macro, storage {PA}) of p/{name}.'] + body)
            else:
                pub += body
        W.w(f'p/{name}', pub)


def preset_cards(name):
    """fx cards one call spawns at most (the larger c variant)"""
    return max(sum(1 for l in b if f'{FN}card' in l) for b in preset_variants(name).values())


# ----------------------------------------------------------------------------- tests and demos
TEST_ARGS = {'r': 36, 'yaw': 0, 'pitch': 0, 'roll': 0, 'c': 1, 'len': 70, 't': 20, 'h': 34, 'n': 12}


def fx(name, **args):
    """A preset call line (fx/p/<name>), args as api.KIT_PRESETS (ints)."""
    assert name in PRESETS, name
    need = PRESETS[name][1]
    assert sorted(args) == sorted(need), (name, sorted(args), need)
    if not need:
        return f'function {FN}p/{name}'
    return f'function {FN}p/{name} {{' + ','.join(f'{k}:{int(args[k])}' for k in need) + '}'


def snd(name):
    assert name in SOUNDS, name
    return f'function {FN}snd/{name}'


def hud(name, **args):
    assert name in api.KIT_HUD and sorted(args) == sorted(api.KIT_HUD[name]), name
    if not args:
        return f'function {FN}hud/{name}'
    return f'function {FN}hud/{name} {{' + ','.join(f'{k}:{(chr(34) + v + chr(34)) if isinstance(v, str) else int(v)}'
                                                     for k, v in args.items()) + '}'


def _ev(t, where, *lines):
    return [(t, where, l) for l in lines]


def _demos():
    f = fx
    D = {}
    D['qi_arc'] = sum([_ev(5 + 12 * i, 'chest', f('qi_arc', r=r, yaw=0, pitch=p, roll=ro, c=c), snd(s))
                       for i, (r, p, ro, c, s) in enumerate(((40, 0, 0, 1, 'a1_hit'), (36, 0, 35, 1, 'a2_hit'),
                                                             (40, 0, -35, 1, 'a3_h2'), (45, 0, -40, 1, 'g_leap_cut'),
                                                             (40, 0, 15, 4, 'g_wrap'), (18, 0, 0, 2, 'draw')))], [])
    D['qi_ring'] = _ev(5, 'waist', f('qi_ring', r=30, c=1), snd('a5_spin')) + _ev(25, 'low', f('qi_ring', r=40, c=2), snd('a9_cut'))
    D['qi_band'] = _ev(5, 'chest1', f('qi_band', len=120, yaw=0, pitch=0, roll=0), snd('band_sweep')) + \
        _ev(30, 'spot3', f('qi_band', len=70, yaw=0, pitch=35, roll=0), snd('g_rise'))
    D['qi_x'] = _ev(5, 'spotf', f('qi_x', r=25), snd('g_x'))
    D['qi_dome'] = _ev(5, 'spot', f('qi_dome', r=35), snd('g_dome'))
    D['qi_vert'] = _ev(5, 'front', f('qi_vert', h=34, yaw=0, c=1), snd('a3_h1')) + _ev(25, 'front', f('qi_vert', h=34, yaw=0, c=2),
                                                                                         snd('g_vert'))
    D['qi_fan'] = _ev(5, 'fan', f('qi_fan', h=16, c=2), snd('a1_fan'))
    D['qi_wedge'] = _ev(5, 'chest', f('qi_wedge', r=46, roll=40), snd('a3_h5'))
    D['qi_ribbon'] = _ev(5, 'chest', f('qi_ribbon'), snd('a4_flip'))
    D['qi_line'] = _ev(5, 'line', f('qi_line', len=40)) + _ev(20, 'high', 'execute rotated ~ 90 run ' + f('qi_line', len=40))
    D['qi_cut'] = _ev(5, 'waist', f('qi_cut', len=120), snd('a9_cut'))
    D['glint'] = sum([_ev(5 + 6 * i, 'tip', f('glint', c=c)) for i, c in enumerate(C_ALL)], []) + _ev(5, 'tip', snd('glint_ring'))
    D['star4'] = _ev(5, 'chest', f('star4'), snd('a9_star'))
    D['yellow_tell'] = _ev(5, 'chest', f('yellow_tell', t=12), snd('yellow_chime'))
    D['ghost_burst'] = _ev(5, 'chest', f('ghost_burst'), snd('g_tell'))
    D['ghost_trail'] = _ev(5, 'chest', f('ghost_trail', len=125), snd('g_dash'))
    D['ghost_flash'] = _ev(5, 'chest', f('ghost_flash'), snd('g_flash'))
    D['afterimage'] = sum([_ev(5 + 2 * i, 'chest', f('afterimage', len=20)) for i in range(6)], []) + _ev(5, 'chest', snd('lunge'))
    D['blink_bubble'] = _ev(5, 'chest', f('blink_bubble'), snd('a6_blink'))
    D['shield_refill'] = _ev(5, 'chest', f('shield_refill'), snd('shield_refill'))
    D['pip_break'] = _ev(5, 'chest1', f('pip_break'), snd('pip_break'))
    D['dive_impact'] = _ev(5, 'spot', f('dive_impact', r=26), snd('a4_impact'))
    D['burst_radial'] = _ev(5, 'spot', f('burst_radial', r=35), snd('a10_impact'))
    D['light_column'] = _ev(5, 'spot', f('light_column'), snd('deflect'))
    D['claw_streaks'] = _ev(5, 'spot2', f('claw_streaks', r=15), snd('a10_dive'))
    D['dust_ring'] = _ev(5, 'low', f('dust_ring', r=15), snd('land_back'))
    D['kick_flash'] = _ev(5, 'head', f('kick_flash'), snd('kick'))
    D['clash_gold'] = _ev(5, 'chest1', f('clash_gold'), snd('clash'))
    D['clash_spark'] = sum([_ev(5 + 3 * i, 'chest1', f('clash_spark')) for i in range(5)], []) + _ev(5, 'chest1', snd('blade_tick'))
    D['clash_arc'] = sum([_ev(5 + 2 * i, 'chest1', f('clash_arc')) for i in range(5)], []) + _ev(5, 'chest1', snd('arc_crackle'))
    D['deco_bolt'] = _ev(5, 'spot', f('deco_bolt'), snd('deco_bolt'))
    D['scarlet_line'] = _ev(5, 'chest', f('scarlet_line', len=600, yaw=90, roll=13), snd('iai_slash'))
    D['petal_burst'] = _ev(5, 'chest', f('petal_burst', r=20), snd('petal_break'))
    D['petals_drift'] = _ev(5, 'chest', f('petals_drift'), snd('cs0_petals'))
    D['petals_wind'] = _ev(5, 'waist', f('petals_wind'))
    D['petals_heart'] = _ev(5, 'chest', f('petals_heart'))
    D['motes_warm'] = _ev(5, 'low', f('motes_warm'))
    D['leaves_dark'] = _ev(5, 'high', f('leaves_dark', n=24), snd('cs0_wind'))
    D['leaves_swirl'] = _ev(5, 'chest', f('leaves_swirl'))
    D['ambient_p1'] = sum([_ev(t, 'body', f('ambient_p1')) for t in range(0, 80, 10)], [])
    D['ambient_p2'] = sum([_ev(t, 'body', f('ambient_p2')) for t in range(0, 80, 6)], [])
    D['arrive_rift'] = _ev(5, 'rift', f('arrive_rift'))
    D['ev_glint'] = _ev(5, 'hand', f('ev_glint'), snd('ev_chime'))
    D['ev_trail'] = sum([_ev(5 + i, 'chest', f('ev_trail')) for i in range(10)], [])
    D['ev_petals'] = sum([_ev(5 + 4 * i, 'chest', f('ev_petals', n=2)) for i in range(8)], [])
    D['ev_leave'] = _ev(5, 'chest', f('ev_leave'), snd('ev_leave'))
    D['ev_beam'] = _ev(5, 'spot', f('ev_beam', h=80, t=10), snd('ev_beam'))
    D['ev_wind'] = _ev(5, 'spot', f('ev_wind', r=15))
    D['ev_palm'] = sum([_ev(5 + i, 'hand', f('ev_palm')) for i in range(16)], [])
    D['ev_take'] = _ev(5, 'chest1', f('ev_take', c=1), snd('ev_take_i')) + _ev(30, 'chest1', f('ev_take', c=2), snd('ev_take_b'))
    assert set(D) == set(PRESETS), set(D) ^ set(PRESETS)
    return D


DEMOS = _demos()
DEMO_LEN = {k: max(t for t, _w, _l in v) + 45 for k, v in DEMOS.items()}
DEMO_WHERE = {
    'body': 'at @s rotated as @s rotated ~ 0',
    'low': 'at @s rotated as @s rotated ~ 0 positioned ~ ~0.1 ~',
    'waist': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~',
    'chest': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~',
    'chest1': 'at @s rotated as @s rotated ~ 0 positioned ^ ^1.2 ^2',
    'fan': 'at @s rotated as @s rotated ~ 0 positioned ^ ^1.1 ^1.2',
    'front': 'at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^1.4',
    'line': 'at @s rotated as @s rotated ~ 0 positioned ^ ^1.2 ^1.5',
    'tip': 'at @s rotated as @s rotated ~ 0 positioned ^-0.4 ^1.9 ^1.0',
    'hand': 'at @s rotated as @s rotated ~ 0 positioned ^-0.4 ^1.1 ^0.4',
    'head': 'at @s rotated as @s rotated ~ 0 positioned ~ ~2.4 ~',
    'high': 'at @s rotated as @s rotated ~ 0 positioned ~ ~5 ~',
    'spot': 'at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4.5',
    'spotf': 'at @s rotated as @s rotated ~ 0 positioned ^ ^0.1 ^4.5',
    'spot2': 'at @s rotated as @s rotated ~ 0 positioned ^ ^2 ^4.5',
    'spot3': 'at @s rotated as @s rotated ~ 0 positioned ^ ^0.3 ^4.5',
    'rift': 'at @s rotated as @s rotated ~ 0 positioned ^-3 ^ ^1',
}


def demo_lens():
    # a prop demo shows its looks 25 t apart: 90 t, longer for the halo's five looks (I1b: p1b / p2b)
    return dict(DEMO_LEN, **{f'prop/{p}': max(90, 25 * len(PROPS[p][1]) + 15) for p in PROPS})


def tests(W):
    T = FN + 'test/'
    stand = (f'summon minecraft:armor_stand ~ ~ ~ {{Tags:["{DEMO}","rlk_room","rlk_mb_aux"],NoGravity:1b,Invulnerable:1b,'
             'ShowArms:1b,NoBasePlate:1b,equipment:{mainhand:{id:"minecraft:iron_sword",count:1},'
             'head:{id:"minecraft:black_carpet",count:1},chest:{id:"minecraft:leather_chestplate",count:1}}}')
    STAND = f'@e[type=minecraft:armor_stand,tag={DEMO},limit=1]'
    W.w('test/stage', ['# The demo stand-in: an armour stand with an iron sword 6 b in front of the executor, facing it (a vanilla',
                       '# stand-in for her body; no rig calls). Its feet are the demo floor (storage fx.fl).',
                       f'# /execute as @p at @s rotated ~ 0 run function {T}stage, then {T}<preset>.',
                       f'function {T}stop',
                       f'execute positioned ^ ^ ^6 run {stand}',
                       f'execute as {STAND} at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0',
                       INIT, f'execute store result storage {STO} fx.fl int 100 run data get entity {STAND} Pos[1]',
                       f'scoreboard players set #demo {OBJ} 0', f'scoreboard players set #dt {OBJ} 0',
                       f'schedule function {T}e/tick 1t replace'])
    W.w('test/stop', ['# Remove the demo stand-in and the test props; the floor back to the arena\'s.', f'kill @e[tag={DEMO}]',
                      f'schedule clear {T}e/tick', f'execute if data storage {STO} fx{{init:1b}} run scoreboard players set #demo {OBJ} 0',
                      f'execute if data storage {STO} fx{{init:1b}} run data modify storage {STO} fx.fl set value {FLOOR * 100}'])
    tick = ['# Demo ticker (scheduled): the running demo\'s events as the stand-in.',
            f'execute unless entity {STAND} run return 0',
            f'execute if score #demo {OBJ} matches 1.. run scoreboard players add #dt {OBJ} 1',
            f'execute as @e[type=minecraft:item_display,tag={DEMO}_mv] at @s run tp @s ^ ^ ^0.6']
    allk = list(DEMOS) + [f'prop/{p}' for p in PROPS]
    lens = demo_lens()
    for k, name in enumerate(allk, 1):
        tick.append(f'execute if score #demo {OBJ} matches {k} as {STAND} run function {T}e/{name}')
        tick.append(f'execute if score #demo {OBJ} matches {k} if score #dt {OBJ} matches {lens.get(name, 80)}.. run '
                    f'function {T}e/end')
    tick.append(f'schedule function {T}e/tick 1t replace')
    W.w('test/e/tick', tick)
    W.w('test/e/end', [f'scoreboard players set #demo {OBJ} 0', f'kill @e[type=minecraft:item_display,tag={DEMO}]',
                       f'kill @e[type=minecraft:marker,tag={DEMO}]'])

    def demo_entry(k, name, doc):
        return [f'# Demo of fx/{name} on the vanilla stand-in (made by test/stage when missing): {doc}',
                f'execute unless entity {STAND} run function {T}stage',
                INIT, f'scoreboard players set #demo {OBJ} {k}', f'scoreboard players set #dt {OBJ} -1',
                f'schedule function {T}e/tick 1t replace']
    for k, (name, events) in enumerate(DEMOS.items(), 1):
        W.w(f'test/{name}', demo_entry(k, f'p/{name}', 'the preset at its executor point with test values, next to the '
                                                      'calls that go with it in the fight.'))
        lines = [f'# Demo "{name}" events (as the stand-in; #dt = the demo tick).']
        for tk, where, line in sorted(events, key=lambda e: e[0]):
            lines.append(f'execute if score #dt {OBJ} matches {tk} {DEMO_WHERE[where]} run {line}')
        W.w(f'test/e/{name}', lines)
    base = len(DEMOS)
    for i, name in enumerate(PROPS):
        k = base + i + 1
        W.w(f'test/prop/{name}', demo_entry(k, f'prop/{name}', 'one display summoned in front of it and dressed, its looks in turn.'))
        looks = [lk for lk in PROPS[name][1] if lk is not None]
        mv = name == 'disc'
        tags = f'["{DEMO}","rlk_room","rlk_mb_aux"{"," + chr(34) + DEMO + "_mv" + chr(34) if mv else ""}]'
        up = {'moon_halo': '^ ^7 ^6', 'seat_rock': '^ ^ ^2', 'lotus': '^ ^ ^2'}.get(name, '^ ^1.2 ^1.5')
        lines = [f'# Demo prop "{name}" (as the stand-in).',
                 f'execute if score #dt {OBJ} matches 1 at @s rotated as @s rotated ~ 0 positioned {up} run summon '
                 f'minecraft:item_display ~ ~ ~ {{Tags:{tags},teleport_duration:1}}',
                 f'execute if score #dt {OBJ} matches 1 as @e[type=minecraft:item_display,tag={DEMO},limit=1,sort=nearest] at @s '
                 f'rotated as {STAND} run tp @s ~ ~ ~ ~ 0']
        if looks:
            for j, lk in enumerate(looks):
                lines.append(f'execute if score #dt {OBJ} matches {1 + 25 * j} as @e[type=minecraft:item_display,tag={DEMO},'
                             f'limit=1,sort=nearest] run function {FN}prop/{name} {{look:"{lk}"}}')
        else:
            lines.append(f'execute if score #dt {OBJ} matches 1 as @e[type=minecraft:item_display,tag={DEMO},limit=1,sort=nearest] '
                         f'run function {FN}prop/{name}')
        W.w(f'test/e/prop/{name}', lines)
    W.w('test/sounds', ['# Click through the sound recipes (tellraw list).',
                        'tellraw @s [{"text":"홍련 sounds: ","color":"#E8466A","font":"minecraft:default"}' +
                        ''.join(f',{{"text":"[{n}] ","color":"#E8C2F6","font":"minecraft:default","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}"}}}}' for n in SOUNDS) + ']'])
    W.w('test/hud', ['# The HUD: line 1, the black overlay over line 15, the warning, the skip prompt; all off after 6 s.',
                     hud('line', id=1), f'schedule function {T}e/hud2 60t replace'])
    W.w('test/e/hud2', [hud('ovl', g='black', **{'in': 0, 'hold': 10, 'out': 3}), hud('line', id=15), hud('warn', on=1),
                        hud('skip', s=2), f'schedule function {T}e/hud3 60t replace'])
    W.w('test/e/hud3', [hud('clear')])
    kinds = ['# Every fx kind in rows in front of the executor (3 s each):',
             f'# /execute as @p at @s rotated ~ 0 run function {T}kinds']
    for i, kind in enumerate(ALL_KINDS):
        row, colm = divmod(i, 8)
        x = 7.0 - 2.0 * colm
        z = 5 + 2.6 * row
        plane = kind_info(kind)[0]
        if plane == 'flat':
            kinds.append(card(kind, f'^{num(x)} ^0.3 ^{num(z)}', '~ 0', s0=0.3, s1=1.0, life=60, fade=10))
        elif plane in ('lance', 'lancex'):
            kinds.append(card(kind, f'^{num(x)} ^1.2 ^{num(z)}', '~90 0', s0=0.3, s1=1.5, life=60, fade=10))
        else:
            kinds.append(card(kind, f'^{num(x)} ^1.2 ^{num(z)}', '~180 0', s0=0.3, s1=1.0, life=60, fade=10))
    W.w('test/kinds', kinds)


def build_datapack(dp):
    W = Writer(dp)
    engine(W)
    sounds(W)
    hud_funcs(W)
    presets_dp(W)
    props(W)
    tests(W)
    removed = W.flush()
    return len(W.files), removed, W


def manifest():
    return {
        'generator': 'tools/build_mboss_hr_fx.py', 'api': 'tools/mboss_scarlet/api.py §8; scratchpad hr/contract.md §3.3',
        'functions': FN, 'item_models': NS_TEX, 'font': FONT, 'font_range': [f'U+{CP_LO:04X}', f'U+{CP_HI:04X}'],
        'storage': f'{STO} fx.*', 'bossbar': WARN_BAR,
        'owned': {'dirs': [f'{FDIR}/{d}' for d in OWNED_DIRS], 'files': [f'{FDIR}/{f}.mcfunction' for f in OWNED_FILES],
                  'rp': [f'assets/rlk/textures/{TEXDIR}', f'assets/rlk/models/item/{TEXDIR}', f'assets/rlk/items/{TEXDIR}',
                         f'assets/rlk/font/{FONT_NAME}.json', f'assets/rlk/textures/font/{FONT_NAME}']},
        'caps': {'fx': CAP_FX, 'ambient': CAP_AMB, 'afterimage': CAP_AI,
                 'rule': 'never skipped: the ager keeps the newest cards of a pool over its cap (the oldest go, hrFxQ serial)'},
        'objectives': [OBJ] + list(OBJECTIVES), 'fake_players': f'{", ".join(FAKE)} (objective {OBJ})',
        'tags': [TAG, f'{TAG}_c', f'{TAG}_a', f'{TAG}_i', f'{TAG}_new', f'{TAG}_go', f'{TAG}_sh', f'{TAG}_fd', f'{TAG}_hit',
                 f'{TAG}_t', f'{TAG}_nf', BEAM, ANIM, f'{ANIM}_d', f'{ANIM}_p', FOLLOW, FOLLOW_STAY, LEAD, DEMO, f'{DEMO}_mv'],
        'conventions': {'yaw': '+ = to the executor\'s right (offset from its rotation)', 'pitch': '+ = up (elevation)',
                        'roll': 'about the aim (qi_arc 0 flat / 90 vertical); qi_band: lean (+ = top forward); scarlet_line: '
                                '+ lifts the + (right) end', 'units': 'tenths of a block / degrees / ticks',
                        'c': {str(k): v for k, v in {1: 'lilac', 2: 'pink-magenta', 3: 'yellow', 4: 'crimson', 5: 'white'}.items()}},
        'floor': {'clamp_floor_storage': f'{STO} fx.fl (y x 100, default {FLOOR * 100})', 'arc_bearings': ARC_BEAR,
                  'arc_lift_max': ARC_LIFT / 100},
        'sprites': {k: [list(g) for g in v] for k, v in sprite_table().items()},
        'textures': {stem: list(wh) for stem, (wh, _b, _f, _s) in TEXTURES.items()},
        'kinds': {k: {'plane': kind_info(k)[0], 'px': list(kind_info(k)[1]), 'extent': [r4(v) for v in kind_info(k)[2]],
                      'tint': 'neutral' if kind_info(k)[3] else 'painted', 'texture': kind_info(k)[4],
                      'source': 'rift (the rlk:rift model or the fallback)' if k in RIFT else 'own', 'desc': kind_info(k)[5]}
                  for k in ALL_KINDS},
        'rift_models': {k: RIFT_MODEL + v for k, v in RIFT.items()},
        'atlas_px_new': atlas_px(), 'sprite_px': SPRITE_PX, 'sprite_cap': api.KIT_SPRITE_CAP, 'gate_icon_px': GATE_PX,
        'presets': {k: {'args': v[1], 'doc': v[0], 'cards': preset_cards(k), 'c_split': list(SPLIT_CS.get(k, C_ALL)) if v[4] else [],
                        'ambient': k in AMBIENT, 'particles_only': k in PTCL} for k, v in PRESETS.items()},
        'props': {k: {'doc': v[0], 'looks': {str(lk): (list(x) if isinstance(x, tuple) else x) for lk, x in v[1].items()},
                      'billboard': v[2], 'anim': v[3]} for k, v in PROPS.items()},
        'seat_items': {k: {'item': v[0], 'at': list(v[1]), 'scale': list(v[2]) if isinstance(v[2], tuple) else v[2]}
                       for k, v in SEAT.items()},
        'sounds': {k: [list(l) for l in v] for k, v in SOUNDS.items()},
        'hud': {k: list(v) for k, v in api.KIT_HUD.items()},
        'lines': {str(k): {'text': v, 'steps': len(typed(v)), 'on_screen': api.LINE_AT[k][2], 'colour': LINE_COL}
                  for k, v in api.LINES.items()},
        'glyphs': {k: {'cp': f'U+{v[0]:04X}', 'px': list(v[2]), 'height': v[3], 'ascent': v[4]} for k, v in GLYPHS.items()},
        'space': f'U+{SP_NEG1:04X} (-1)',
        'warn': {'bossbar': WARN_BAR, 'text': api.WARN_TEXT, 'component': warn_component()},
        'skip': {'text': api.SKIP_TEXT, 'hint': api.SKIP_HINT, 'steps': list(SKIP_COLS)},
        'gate_icon': api.GATE_ICON_MODEL,
        'demos': demo_lens(),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--resourcepack', help='unpacked resource pack root (assets/...)')
    ap.add_argument('--datapack', default=str(HERE.parent), help='datapack root (data/...)')
    ap.add_argument('--skip-rp', action='store_true', help='only write the datapack functions and the manifest')
    a = ap.parse_args()
    n, removed, _W = build_datapack(a.datapack)
    text = json.dumps(manifest(), ensure_ascii=False, indent=1) + '\n'
    if not MANIFEST.exists() or MANIFEST.read_text(encoding='utf-8') != text:
        MANIFEST.write_text(text, encoding='utf-8')
    msg = (f'scarlet fx kit: {n} functions ({removed} stale removed), {len(PRESETS)} presets, {len(PROPS)} props, '
           f'{len(SOUNDS)} sounds, {len(api.KIT_HUD)} hud calls, {len(api.LINES)} lines')
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error('--resourcepack is required unless --skip-rp')
        k, px, g, s1 = build_resourcepack(a.resourcepack)
        msg += (f', {k} textures ({px / 1e6:.3f} M new px: sprites {SPRITE_PX} + gate icon {GATE_PX}), {g} glyphs in {FONT}, '
                f'arrival tear: {"the rift models" if s1 else "fallback"}')
    print(msg)


if __name__ == '__main__':
    main()
