#!/usr/bin/env python3
"""FX / audio / HUD kit of the chapter-1 boss 야타용왕 (Azhdaha), the sealed rock-dragon king.

The field generator kit (tools/build_mboss_fg_fx.py, scratchpad mb3/fg_fx_api.md) copied and renamed, with the
extensions of the day-0 contract (scratchpad az/contract/fx.md = az_fx_api.md §0). Pattern authors call it from their
patterns; nothing here decides gameplay (hits, timings, hazards, the brand and every count stay in the module core).
Parts, all regenerated on every run:

  1. The tinted card engine (fg kit, first-tick fix kept): painted sprites on short-lived item_display cards; planes
     face, flat, cross, band, box (per-kind extents) and prism (an eight-walled glyph prism). Caps: CAP fx cards,
     TCAP attack-telegraph cards (calls skipped from TCAP - TSKIP on, so no shape is half drawn) and the separate
     field pool (FCAP cards, never counted against the other two).
  2. Ground telegraphs with every `#elem` palette (el 0-8) and the shared undodgeable look (nd 1 / 2: the red-amber
     rim and the 回 card, + a jump chevron): disc, ring, sector (7.5-degree steps, a fan of 15 / 30-degree slices),
     wedge (annular sectors at any angles: the P7 union), line, lane_side, wave (ids, wave_to, wave_end), mline (moving
     lanes), heptagram, hexagram, starseal, seal8, mask_wash + safe_rim / safe_beam / safe_end, crater, halo; the
     field pool (field, strip, field_end, field_clear).
  3. Vanilla sound recipes fx/snd/<name> (+ element families), with the per-layer minimum volume rule of mboss_lib.
  4. The HUD: font rlk:mboss_az (U+E800-E8FF): badges, element icons, flashes, the "점프!" cue, the 回 mark, banner
     ornaments; the transition / absorb / brand banners and the title-line cues.
  5. Presets fx/p/<name> (+ element families fx/p/<name>/<el> with a dispatcher), prop looks fx/prop/<name>, the
     in-game test functions and one demo per plan §5 pattern on a vanilla stand-in anchor.

Outputs (owned; stale files in these places are removed):
  resource pack  assets/rlk/textures/mboss/az_kit/<kind>.png      painted sprites (stdlib painter)
                 assets/rlk/models/item/mboss/az_kit/<kind>.json    card models (tintindex 0)
                 assets/rlk/items/mboss/az_kit/<kind>.json          item definitions, custom_model_data tint
                 assets/minecraft/atlases/items.json                adds rlk:mboss/az_kit/* (merges)
                 assets/rlk/font/mboss_az.json + textures/font/mboss_az/*
  datapack       data/rlk/function/mboss/azhdaha/fx/{card,cardx,look,clear,uninstall}
                 data/rlk/function/mboss/azhdaha/fx/{e,p,tele,snd,hud,prop,test}/**
                 (every other file under mboss/azhdaha/fx/ belongs to the module core and is left alone)
  manifest       tools/mboss_az_fx_manifest.json

No hook in a shared file: the engine ages its cards from a self-rescheduling function (schedule ... 1t replace).
Cards carry rlk_room + rlk_mb_aux. The module wires uninstall / clear / pause / death_start (az_fx_api.md §0.4).

Run: python3 tools/build_mboss_az_fx.py --resourcepack <unpacked RP> [--datapack <dp root>]   (or --skip-rp)
API: scratchpad az/az_fx_api.md (= tools-side copy). Other generators `import build_mboss_az_fx as K` (no files are
written on import).
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
import mboss_az_fx_paint as P  # noqa: E402

FN = 'rlk:mboss/azhdaha/fx/'
FDIR = 'data/rlk/function/mboss/azhdaha/fx'
NS_TEX = 'rlk:mboss/az_kit/'           # textures, models (rlk:item/mboss/az_kit/*) and item ids
TEXDIR = 'mboss/az_kit'
FONT = 'rlk:mboss_az'
FONT_NAME = 'mboss_az'
STO = 'rlk:azkit'
CAP = 64            # live fx cards; further fx spawns are skipped until some expire
TCAP = 40           # live attack-telegraph cards (counted apart, so busy fx never hide a telegraph)
TSKIP = 6           # attack-telegraph calls are skipped from TCAP - TSKIP on (no shape is ever half drawn)
FCAP = 16           # field-pool cards (8 field ids x 2 cards), never counted against CAP / TCAP
SOFT = 40           # ambient presets are skipped from SOFT live fx cards on (room for the hits' fx)
TSOFT = 36           # trail presets are skipped from TSOFT live fx cards on (FIX STATE-14: 28 cards kept for the hits)
ATLAS_BUDGET = 600_000
OWNED_DIRS = ('e', 'p', 'tele', 'snd', 'hud', 'prop', 'test')
OWNED_FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')
OBJECTIVES = ('akS', 'akG', 'akH', 'akK', 'akD')
TAG = 'rlk_ak'
WALL_H = 0.5                     # band kind: wall height at scale 1
EL_NAMES = {1: '불', 2: '물', 3: '번개', 4: '얼음', 5: '바위'}
EL_KEYS = {1: 'pyro', 2: 'hydro', 3: 'electro', 4: 'cryo', 5: 'geo'}


def rgb(h):
    return int(h[1:], 16)


# ----------------------------------------------------------------------------- colours (RGB ints for tints)
WHITE = 0xFFFFFF
GOLD = rgb('#F0C860')            # Geo crystal gold (blades, crown)
GOLD_PALE = rgb('#FFE8A0')
GOLD_DEEP = rgb('#C8781E')
GOLD_WHITE = rgb('#FFF6D0')
DUST = rgb('#9D8558')            # Geo dust walls (v3 §4.2)
DUST_KHAKI = rgb('#7A6F59')      # burrow dust (v6 §4.3)
HYDRO = rgb('#4FB8FF')
HYDRO_PALE = rgb('#CDEBFF')
HYDRO_DEEP = rgb('#1C74AC')
FOAM = rgb('#E5EAF1')
PYRO = rgb('#FF8A3D')
PYRO_PALE = rgb('#FFD2A0')
PYRO_DEEP = rgb('#CC4410')
EMBER = rgb('#F8CE0B')
CRYO = rgb('#9FE8F5')
CRYO_PALE = rgb('#E8FBFF')
CRYO_DEEP = rgb('#42BCF4')
ELECTRO = rgb('#C58BFF')
ELECTRO_PALE = rgb('#EEDDFF')
ELECTRO_DEEP = rgb('#6A3FC8')
MAGENTA = rgb('#D569E2')         # lightning (v6 §4.3)
STONE = rgb('#7A6A58')
SAFE_RIM = rgb('#2FCF5E')        # the 42 safe circles' own green
SAFE_FLASH = rgb('#B8FFC8')
ND_RIM = rgb('#FF5A1E')          # the shared undodgeable red-amber (plan rule 6)
SEAL_BROWN = rgb('#60391E')

# telegraph tints per el (#elem numbering): rim, fill, flash. 6-8 draw Geo.
TELE_COL = {0: (rgb('#E5304A'), rgb('#FF6474'), rgb('#FFB8C4')),
            1: (rgb('#C8461E'), rgb('#FF8A3D'), rgb('#FFD2A0')),
            2: (rgb('#1E6FC8'), rgb('#4FB8FF'), rgb('#CDEBFF')),
            3: (rgb('#6A3FC8'), rgb('#C58BFF'), rgb('#EEDDFF')),
            4: (rgb('#3AA6C0'), rgb('#9FE8F5'), rgb('#E8FBFF')),
            5: (rgb('#D27A0C'), rgb('#F0A93A'), rgb('#FFE8A0'))}
for _e in (6, 7, 8):
    TELE_COL[_e] = TELE_COL[5]
TELE_DEFAULT = 5
# fx colours per element (1..5): main, pale, deep, dust colour
EL_FX = {1: (PYRO, PYRO_PALE, PYRO_DEEP, rgb('#5A3A2A')), 2: (HYDRO, HYDRO_PALE, HYDRO_DEEP, FOAM),
         3: (ELECTRO, ELECTRO_PALE, ELECTRO_DEEP, rgb('#8A7AA8')), 4: (CRYO, CRYO_PALE, CRYO_DEEP, rgb('#DDF4FA')),
         5: (GOLD, GOLD_PALE, GOLD_DEEP, DUST)}
# HUD colours of the element names / badges
EL_HEX = {1: '#FF8A3D', 2: '#4FB8FF', 3: '#C58BFF', 4: '#9FE8F5', 5: '#F0A93A'}
DIM_HEX = '#707070'

# ----------------------------------------------------------------------------- kinds
# name -> (plane, (w, h) px, card extent in blocks at scale 1 (a0, a1, b0, b1), painter box (a0, a1, b0, b1),
#          painter, supersampling, tinted-neutral?, description)
# planes: face = local XY plane (facing forward, or the camera with a billboard); flat = local XZ plane (horizontal
# for rot "~ 0", +b forward); cross = two crossed vertical quads along +y; band = a flat strip b in -1..0 plus a wall
# on its front edge (y 0..WALL_H); box = a cuboid (BOXES half extents) with the full texture on every face; prism = an
# eight-walled prism (radius 1, height 0..1.5 at scale 1) with the texture on every wall, inside and out.
SQ = (-0.5, 0.5, -0.5, 0.5)
UNIT = (-1, 1, -1, 1)
BX = (-1, 1, -1, 1)
FOOT = (-0.5, 0.5, 0.0, 1.0)
LANE = (-0.5, 0.5, 0.0, 1.0)
BOXES = {'slab': (0.5, 0.135, 0.2), 'stele': (0.35, 1.0, 0.12)}
PRISM_R, PRISM_H = 1.0, 1.5


def _slice_box(half):
    s = math.sin(math.radians(half)) + 0.012
    return (-s, s, 0.0, 1.0)


KINDS = {
    # neutral (tint them)
    'glow':        ('face', (64, 64), SQ, BX, P.paint_glow, 2, True, 'soft white glow disc'),
    'glint':       ('face', (32, 32), SQ, BX, P.paint_glint, 3, True, 'white 4-point glint'),
    'mote':        ('face', (16, 16), SQ, BX, P.paint_mote, 4, True, 'soft mote (embers, motes, frost glints)'),
    'streak':      ('face', (128, 16), (-0.5, 0.5, -0.0625, 0.0625), BX, P.paint_streak, 2, True, 'long thin streak along a'),
    'ripple':      ('flat', (128, 128), UNIT, BX, P.paint_ripple, 2, True, 'ripple / shock ring (unit radius)'),
    'spark':       ('face', (32, 32), SQ, BX, P.paint_spark, 3, True, 'spark star'),
    'beam':        ('cross', (32, 128), FOOT, FOOT, P.paint_beam, 2, True, 'light beam / column, foot at b 0'),
    'vortex':      ('flat', (64, 64), UNIT, BX, P.paint_vortex, 2, True, 'absorb vortex swirl (unit radius)'),
    'cracks':      ('flat', (128, 128), UNIT, BX, P.paint_cracks, 2, True, 'radial floor cracks (unit radius)'),
    'crackfan':    ('flat', (64, 64), (-0.6, 0.6, -0.05, 1.0), (-0.6, 0.6, -0.05, 1.0), P.paint_crackfan, 2, True,
                    'crack fan from the apex forward, about +-32 degrees'),
    'blade':       ('face', (32, 64), (-0.25, 0.25, -0.5, 0.5), (-0.25, 0.25, -0.5, 0.5), P.paint_blade, 2, True,
                    'translucent crystal blade'),
    'dust':        ('face', (64, 64), SQ, BX, P.paint_dust, 2, True, 'dust puff (toon cloud)'),
    'arc':         ('face', (64, 32), (-0.5, 0.5, -0.25, 0.25), (-0.5, 0.5, -0.25, 0.25), P.paint_arc, 2, True,
                    'electric arc'),
    'crystal':     ('cross', (64, 128), FOOT, FOOT, P.paint_crystal, 2, True, 'arena crystal cluster, foot at b 0'),
    'water':       ('flat', (128, 128), SQ, SQ, P.paint_water, 1, True, 'shallow-water sheet tile (seamless)'),
    # Geo / rock
    'boulder':     ('face', (32, 32), SQ, BX, P.paint_boulder, 3, False, 'dark boulder / rubble chunk'),
    'slab':        ('box', (32, 32), (-0.5, 0.5, -0.135, 0.135), BX, P.paint_slab, 2, False,
                    'rock slab with a gold crack rim (box 1 x 0.27 x 0.4)'),
    'mound':       ('face', (64, 32), (-0.5, 0.5, 0.0, 0.5), (-0.5, 0.5, 0.0, 0.5), P.paint_mound, 2, False,
                    'dust mound, foot at b 0'),
    'cone':        ('face', (32, 64), FOOT, FOOT, P.paint_cone, 2, False, 'stone cone, foot at b 0'),
    'leaf':        ('face', (16, 16), SQ, BX, P.paint_leaf, 4, False, 'orange tail leaf'),
    'gold_leaf':   ('face', (16, 16), SQ, BX, P.paint_gold_leaf, 4, False, 'gold leaf'),
    # Hydro
    'splash':      ('face', (64, 64), FOOT, FOOT, P.paint_splash, 2, False, 'water splash crown, foot at b 0'),
    'geyser':      ('cross', (32, 128), FOOT, FOOT, P.paint_geyser, 2, False, 'water geyser column, foot at b 0'),
    'orb':         ('face', (64, 64), SQ, BX, P.paint_orb, 2, False, '격류 범람 Hydro orb'),
    # Pyro
    'flame':       ('face', (32, 64), FOOT, (-0.5, 0.5, 0.0, 1.0), P.paint_flame, 2, False, 'flame tongue, root at b 0'),
    'fire_dome':   ('face', (64, 32), (-0.5, 0.5, 0.0, 0.5), (-0.5, 0.5, 0.0, 0.5), P.paint_fire_dome, 2, False,
                    'impact fire dome (half dome, pivot at the base)'),
    'lava':        ('face', (32, 32), SQ, BX, P.paint_lava, 3, False, 'molten rock lump'),
    'meteor':      ('face', (64, 96), (-0.5, 0.5, -0.5, 1.0), (-0.5, 0.5, -0.5, 1.0), P.paint_meteor, 2, False,
                    '운석 meteor: molten head at the bottom, flame trail up'),
    'smoke':       ('face', (64, 64), SQ, BX, P.paint_smoke, 3, False, 'smoke / steam puff'),
    # Cryo
    'ice_spike':   ('cross', (32, 64), FOOT, FOOT, P.paint_ice_spike, 2, False, 'ice crystal spike, foot at b 0'),
    'frost':       ('face', (32, 32), SQ, BX, P.paint_frost, 3, False, 'frost mist puff'),
    'icicle':      ('cross', (16, 64), (-0.125, 0.125, -0.5, 0.5), (-0.125, 0.125, -0.5, 0.5), P.paint_icicle, 3, False,
                    'ice lance, tip at +b'),
    'ice_sphere':  ('face', (64, 64), SQ, BX, P.paint_ice_sphere, 2, False, '쏟아지는 천화 spiky ice sphere'),
    # Electro
    'bolt':        ('face', (32, 128), FOOT, (-0.5, 0.5, 0.0, 1.0), P.paint_bolt, 2, False,
                    'lightning bolt, foot at b 0'),
    'shell':       ('face', (64, 64), SQ, BX, P.paint_shell, 2, False, '번개의 가루 shell'),
    # props
    'spike_geo':   ('cross', (32, 128), FOOT, FOOT, P.make_spike('geo'), 2, False, 'Geo 천동만상 spike, tip at +b'),
    'spike_cryo':  ('cross', (32, 128), FOOT, FOOT, P.make_spike('cryo'), 2, False, 'Cryo dark spike, tip at +b'),
    'spike_electro': ('cross', (32, 128), FOOT, FOOT, P.make_spike('electro'), 2, False, 'Electro spike, tip at +b'),
    'stele':       ('box', (32, 64), (-0.35, 0.35, -1.0, 1.0), (-0.5, 0.5, -0.5, 0.5), P.paint_stele, 2, False,
                    'intro seal stele (box 0.7 x 2 x 0.24)'),
    'prism':       ('prism', (64, 64), (-0.5, 0.5, 0.0, 1.0), (-0.5, 0.5, 0.0, 1.0), P.paint_prism, 2, False,
                    'intro seal prism (8 walls, radius 1, height 1.5)'),
    'gate_icon':   ('face', (64, 64), SQ, BX, P.paint_gate_icon, 2, False, 'gate label icon'),
    'cure_burst':  ('face', (64, 64), SQ, BX, P.paint_cure_burst, 2, False, 'cleanse burst sphere'),
}
for _el in range(1, 6):
    _k = EL_KEYS[_el]
    KINDS[f'sigil_{_k}'] = ('face', (64, 64), SQ, BX, P.make_sigil(_el), 2, False, f'absorb sigil ({_k})')
    KINDS[f'glyph_{_k}'] = ('face', (64, 64), SQ, BX, P.make_glyph(_el), 2, False, f'stele / arrival glyph ({_k})')
    KINDS[f'front_{_k}'] = ('band', (64, 64), (-0.5, 0.5, -1.0, 0.0), (-0.5, 0.5, -1.0, 1.0), P.make_front(_el), 2,
                            False, f'wave front band segment ({_k})')
for _el in range(1, 5):
    _k = EL_KEYS[_el]
    KINDS[f'rune_{_k}'] = ('face', (64, 64), SQ, BX, P.make_rune(_el), 2, False, f'brand rune ({_k})')
    KINDS[f'shard_{_k}'] = ('face', (32, 64), (-0.4, 0.4, -0.5, 0.5), (-0.4, 0.4, -0.5, 0.5), P.make_shard(_el), 2,
                            False, f'응결 결정 ({_k})')
# telegraph decals (unit radius / unit length: the scale is the size in blocks)
KINDS.update({
    't_rim':   ('flat', (128, 128), UNIT, BX, P.paint_t_rim, 2, True, 'telegraph rim, unit radius'),
    't_rim_s': ('flat', (64, 64), UNIT, BX, P.paint_t_rim_s, 2, True, 'thick telegraph rim (r <= 2.5)'),
    # the shaped keep outlines (plan Change note 1; FIX FID-4): tele/crack_o, chev_o, swirl_o
    't_crack': ('flat', (96, 96), UNIT, BX, P.paint_t_crack, 2, True, 'P4 zig-zag crack ring outline (keep)'),
    't_chev':  ('flat', (96, 96), UNIT, BX, P.paint_t_chev, 2, True, 'P9 chevron ring outline (keep)'),
    't_swirl': ('flat', (96, 96), UNIT, BX, P.paint_t_swirl, 2, True, 'P1 Hydro geyser water-swirl outline (keep)'),
    't_ring':  ('flat', (192, 192), UNIT, BX, P.paint_t_ring, 2, True, 'thin travelling ring (fronts, halo)'),
    't_fill':  ('flat', (128, 128), UNIT, BX, P.paint_t_fill, 2, True, 'telegraph progress fill, unit radius'),
    't_bar':   ('flat', (16, 64), LANE, (-1, 1, 0, 1), P.paint_t_bar, 2, True, 'lane rail / cap bar'),
    't_lane':  ('flat', (64, 64), LANE, (-1, 1, 0, 1), P.paint_t_lane, 2, True, 'lane progress fill, unit length'),
    't_frame': ('flat', (32, 128), LANE, LANE, P.paint_t_frame, 2, True, 'strip outline (field pool)'),
    't_sf15':  ('flat', (32, 128), _slice_box(7.5), _slice_box(7.5), P.make_t_sf(7.5), 2, True, '15-degree slice fill'),
    't_sf30':  ('flat', (64, 128), _slice_box(15), _slice_box(15), P.make_t_sf(15), 2, True, '30-degree slice fill'),
    't_sa30':  ('flat', (64, 128), _slice_box(15), _slice_box(15), P.make_t_sa(15), 2, True, '30-degree slice arc rim'),
    't_nd':    ('flat', (64, 64), SQ, BX, P.paint_t_nd, 2, True, 'undodgeable 回 mark (tinted red-amber)'),
    't_ndj':   ('flat', (64, 64), SQ, BX, P.paint_t_ndj, 2, True, 'undodgeable + jump chevron mark'),
    't_hept':  ('flat', (192, 192), UNIT, BX, P.paint_t_hept, 2, True, '서리 습격 heptagram {7/2} + 大巛 rune'),
    't_hex':   ('flat', (128, 128), UNIT, BX, P.paint_t_hex, 2, True, '번개 가시 hexagram + 번개 rune'),
    't_star':  ('flat', (128, 128), UNIT, BX, P.paint_t_star, 2, True, '얼음 가시 star seal + rune'),
    't_seal8': ('flat', (128, 128), UNIT, BX, P.paint_t_seal8, 2, True, '운석 seal: two squares + 火 runes'),
    't_mask':  ('flat', (128, 128), UNIT, BX, P.paint_t_mask, 2, True, '벼락 습격 violet strike wash'),
    't_safe':  ('flat', (64, 64), UNIT, BX, P.paint_t_safe, 2, True, '벼락 습격 safe circle (rim + glyph)'),
    't_crater': ('flat', (64, 64), UNIT, BX, P.paint_t_crater, 3, False, 'B3 crater (also the crater prop)'),
    't_wall':  ('face', (64, 32), FOOT, FOOT, P.paint_t_wall, 2, True, 'dust wall on a flank strip rail'),
    't_gcircle': ('flat', (128, 128), UNIT, BX, P.paint_t_gcircle, 2, False, 'intro seal gold floor glyph circle'),
})
for _v in ('', 'l', 'r', 'b'):
    KINDS['t_sa15' + _v] = ('flat', (32, 128), _slice_box(7.5), _slice_box(7.5), P.make_t_sa(7.5, _v.replace('b', 'lr')),
                            2, True, '15-degree slice arc rim' + (f' + edge {_v}' if _v else ''))
BAND_RHO = {25: 0.25, 50: 0.5, 71: 0.7071, 84: 0.8409}
for _q, _rho in BAND_RHO.items():
    KINDS[f't_bo{_q}'] = ('flat', (32, 128), _slice_box(7.5), _slice_box(7.5), P.make_t_band(_rho, True), 2, True,
                          f'annular 15-degree fill, inner {_rho:g} (outer band)')
    KINDS[f't_bi{_q}'] = ('flat', (32, 128), _slice_box(7.5), _slice_box(7.5), P.make_t_band(_rho, False), 2, True,
                          f'annular 15-degree fill, inner {_rho:g} (inner band)')
for _el in range(1, 6):
    KINDS[f'fld{_el}'] = ('flat', (64, 64), UNIT, BX, P.make_fld(_el), 2, False, f'lingering field disc ({EL_KEYS[_el]})')
for _el in (3, 4):
    KINDS[f'fst{_el}'] = ('flat', (32, 128), LANE, LANE, P.make_fst(_el), 2, False, f'lingering strip ({EL_KEYS[_el]})')
TELE_KINDS = [k for k in KINDS if k.startswith(('t_', 'fld', 'fst'))]
FX_KINDS = [k for k in KINDS if k not in TELE_KINDS]
SPIN_Y = ('flat', 'cross', 'band', 'box', 'prism')       # planes that spin about local y

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
    """Zero-thickness double-sided quads (or cuboids / prism walls) with tintindex 0. Display-local p (blocks) is written
    at model m = (8 - 16 px, 8 + 16 py, 8 - 16 pz): the item renderer's 180-degree turn about Y maps it back to p, so the
    display's local axes are the summoning frame's (+x left, +y up, +z forward). Card +a = local -x = model +x."""
    plane, _s, (a0, a1, b0, b1), _box, _fn, _ss, _n, _d = KINDS[kind]
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1
    tex = NS_TEX + kind

    def q(frm, to, faces, rot=None):
        e = {'from': [r4(v) for v in frm], 'to': [r4(v) for v in to], 'shade': False, 'faces': faces}
        if rot is not None:
            e['rotation'] = {'origin': [8, 8, 8], 'axis': 'y', 'angle': rot, 'rescale': False}
        return e

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
        hx, hy, hz = BOXES[kind]
        full = f([0, 0, 16, 16])
        els = [q([8 - 16 * hx, 8 - 16 * hy, 8 - 16 * hz], [8 + 16 * hx, 8 + 16 * hy, 8 + 16 * hz],
                 {k: dict(full) for k in ('north', 'south', 'east', 'west', 'up', 'down')})]
    elif plane == 'prism':
        d = PRISM_R * math.cos(math.radians(22.5))
        hw = PRISM_R * math.sin(math.radians(22.5))
        y0, y1 = 8, 8 + 16 * PRISM_H
        ew = {'east': f([0, 0, 16, 16]), 'west': f([16, 0, 0, 16])}
        ns = {'south': f([0, 0, 16, 16]), 'north': f([16, 0, 0, 16])}
        els = []
        for rot in (None, 45):
            els += [q([8 - 16 * d, y0, 8 - 16 * hw], [8 - 16 * d, y1, 8 + 16 * hw], dict(ew), rot),
                    q([8 + 16 * d, y0, 8 - 16 * hw], [8 + 16 * d, y1, 8 + 16 * hw], dict(ew), rot),
                    q([8 - 16 * hw, y0, 8 - 16 * d], [8 + 16 * hw, y1, 8 - 16 * d], dict(ns), rot),
                    q([8 - 16 * hw, y0, 8 + 16 * d], [8 + 16 * hw, y1, 8 + 16 * d], dict(ns), rot)]
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
CP_LO, CP_HI = 0xE800, 0xE8FF
# name -> (codepoint, painter (x right, y up, -1..1) | flat (hex, alpha), texture px (w, h), height, ascent)
GLYPHS = {
    'badge':     (0xE800, P.glyph_badge, (36, 36), 8, 7),
    'brand':     (0xE801, P.glyph_brand, (36, 36), 9, 8),
    'el_pyro':   (0xE802, P.make_glyph_el(1), (36, 36), 9, 8),
    'el_hydro':  (0xE803, P.make_glyph_el(2), (36, 36), 9, 8),
    'el_electro': (0xE804, P.make_glyph_el(3), (36, 36), 9, 8),
    'el_cryo':   (0xE805, P.make_glyph_el(4), (36, 36), 9, 8),
    'el_geo':    (0xE806, P.make_glyph_el(5), (36, 36), 9, 8),
    'safe':      (0xE807, P.glyph_safe, (36, 36), 9, 8),
    'fl_white':  (0xE810, ('#FFFFFF', 0.92), (16, 9), 144, 69),
    'fl_gold':   (0xE811, ('#F9DFAD', 0.55), (16, 9), 144, 69),
    'fl_amber':  (0xE812, ('#E6A55F', 0.45), (16, 9), 144, 69),
    'fl_violet': (0xE813, ('#8F64E8', 0.45), (16, 9), 144, 69),
    'jump':      (0xE820, P.glyph_jump, (128, 64), 32, 22),
    'chevron':   (0xE821, P.glyph_chevron, (36, 36), 9, 8),
    'hui':       (0xE822, P.glyph_hui, (36, 36), 9, 8),
    'orn_l':     (0xE840, P.glyph_orn(1), (64, 32), 8, 7),
    'orn_r':     (0xE841, P.glyph_orn(-1), (64, 32), 8, 7),
}
SPACES = {0xE8F0: -1, 0xE8F1: 2, 0xE8F2: 1}
SP_NEG1, SP_TWO, SP_ONE = chr(0xE8F0), chr(0xE8F1), chr(0xE8F2)
EL_GLYPH = {1: 'el_pyro', 2: 'el_hydro', 3: 'el_electro', 4: 'el_cryo', 5: 'el_geo'}


def glyph(name):
    """The character of a kit glyph (use it in a text component with font rlk:mboss_az)."""
    assert name in GLYPHS or name in ('sp_neg1', 'sp_two', 'sp_one'), name
    if name.startswith('sp_'):
        return {'sp_neg1': SP_NEG1, 'sp_two': SP_TWO, 'sp_one': SP_ONE}[name]
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


def glyph_raw(name):
    cp, painter, (w, h), _height, _ascent = GLYPHS[name]
    if callable(painter):
        return w, h, bytes(paint_glyph(painter, w, h))
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


def check_sprites():
    for k, v in KINDS.items():
        w, h = v[1]
        assert w <= 512 and h <= 512 and w % 16 == 0 and h % 16 == 0, (k, w, h)
    px = atlas_px()
    assert px <= ATLAS_BUDGET, f'atlas budget: {px} px > {ATLAS_BUDGET}'
    return px


def build_resourcepack(rp):
    rp = Path(rp)
    px = check_sprites()
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
    bb: fixed | center | vertical | horizontal; roll: degrees about the card's local z (constant); spin: degrees turned
    about the card normal (y for flat / cross / band / box / prism kinds) over the main interpolation (-170..170);
    s0 / s1: start / end size (float = uniform, or an (x, y, z) tuple); off: static start translation in the display
    frame (+x left, +y up, +z forward, blocks); move: translation added over the main interpolation (the end translation
    is off + move; with placeholders give the absolute end as move and off separately); life / fade: ticks; col: tint
    (RGB int, WHITE keeps the painted colours); dly: ticks hidden before it appears; dur: ticks of the main interpolation
    (0 = until the fade); hit / col2: `hit` ticks after the call the tint becomes col2. Any value may be a macro
    placeholder string such as '$(r)'."""
    assert kind in KINDS or kind.startswith('$('), kind
    assert bb in ('fixed', 'center', 'vertical', 'horizontal'), bb
    uni = (int, float, str)
    simple = isinstance(s0, uni) and isinstance(s1, uni) and not dly and not dur and hit == -1 and off is None
    if off is not None and all(isinstance(x, (int, float)) for x in tuple(off) + tuple(move)):
        end = tuple(a + b for a, b in zip(off, move))
    else:
        end = tuple(move)
    mv = vec(end)
    consts = all(isinstance(v, (int, float)) for v in (roll, spin, fade, dly, hit, col2)) and not kind.startswith('$(')
    num_ld = isinstance(life, (int, float)) and isinstance(dur, (int, float))
    # life and dur both macro placeholders (the fronts, recolour, vortex: the preset's own tick arguments): the main
    # interpolation is dur, and the caller's life covers the fade (life >= fade + 2, dur >= 1: the presets' contract)
    ph_ld = isinstance(life, str) and isinstance(dur, str) and fade >= 0
    if consts and (num_ld or ph_ld):
        # (FIX STATE-2, the fast path) the stage numbers are known here: e/make's clamps and stage arithmetic done by
        # the generator, the card spawned by e/cardf (about 25 commands instead of 63; the stages are e/make's to the tick)
        if num_ld:
            lf = 2 if life <= 1 else int(life)
            fd = min(max(0, int(fade)), lf - 2)
            wd = int(dur) if dur >= 1 else lf - fd - 1
            wd = max(1, wd)
        else:
            lf, fd, wd = life, int(fade), dur
        dl = max(0, int(dly))
        sp = max(-170, min(170, int(spin)))
        ax = '0f,1f,0f' if KINDS[kind][0] in SPIN_Y else '0f,0f,1f'
        z = '0f,0f,0f' if dl >= 1 else vec(s0)
        thit = f'{TAG}_hit' if hit >= 0 and col2 >= 0 else f'{TAG}_c'
        return (f'function {FN}e/cardf {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",s0:"{vec(s0)}",s1:"{vec(s1)}",z:"{z}",'
                f'off:"{vec(off if off is not None else (0, 0, 0))}",move:"{mv}",col:{_i(col)},col2:{_i(col2)},ax:"{ax}",'
                f'rr:"{float(int(roll)) * 0.017453292:.8g}",sr:"{float(sp) * 0.017453292:.8g}",d:{wd},f:{fd},life:{lf},dly:{dl},'
                f'h1:{max(0, int(hit) + 1)},tsh:"{TAG}_{"sh" if dl >= 1 else "c"}",tfd:"{TAG}_{"fd" if fd >= 1 else "c"}",thit:"{thit}"}}')
    if simple:
        return (f'function {FN}card {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
                f'spin:{_i(spin)},s0:{_f(s0)},s1:{_f(s1)},move:"{mv}",life:{_i(life)},'
                f'fade:{_i(fade)},col:{_i(col)}}}')
    return (f'function {FN}cardx {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
            f'spin:{_i(spin)},s0:"{vec(s0)}",s1:"{vec(s1)}",off:"{vec(off if off is not None else (0, 0, 0))}",'
            f'move:"{mv}",life:{_i(life)},fade:{_i(fade)},col:{_i(col)},dly:{_i(dly)},dur:{_i(dur)},hit:{_i(hit)},'
            f'col2:{_i(col2)}}}')


cardx = card


def _t(v):
    """blocks -> tenths of a block (a str placeholder passes through)"""
    return v if isinstance(v, str) else str(int(round(float(v) * 10)))


def _n(v):
    return v if isinstance(v, str) else str(int(round(float(v))))


TELE_ARGS = {
    'disc': ('r', 'tell', 'el', 'nd', 'hold'), 'ring': ('r0', 'r', 'tell', 'el', 'nd', 'hold'),
    'sector': ('r', 'a', 'tell', 'el', 'nd', 'hold'), 'wedge': ('r0', 'r1', 'a0', 'a1', 'tell', 'el', 'nd', 'hold'),
    'line': ('len', 'w', 'back', 'tell', 'el', 'nd', 'hold'), 'lane_side': ('len', 'w', 'back', 'tell', 'el', 'hold'),
    'wave': ('id', 'r0', 'r1', 'w', 'tell', 'dur', 'el', 'nd', 'hold'), 'wave_to': ('id', 'r', 'dur'),
    'wave_end': ('id',), 'mline': ('id', 'len', 'w', 'back', 'tell', 'el', 'nd', 'hold'), 'mline_aim': ('id',),
    'mline_turn': ('id', 'd'), 'mline_end': ('id',), 'heptagram': ('r', 'tell', 'el', 'hold'),
    'hexagram': ('r', 'tell', 'el', 'hold'), 'starseal': ('r', 'tell', 'el', 'hold'), 'seal8': ('r', 'tell', 'el', 'hold'),
    # outline-only variants (plan Change note 1 "keep (trim)": no progress fill; requests Rpa-2 / Rpt-3), same arguments
    'disc_o': ('r', 'tell', 'el', 'nd', 'hold'), 'heptagram_o': ('r', 'tell', 'el', 'hold'),
    # the shaped keep outlines (FIX FID-4: P4 crack ring, P9 chevron ring, the P1 Hydro geyser swirl), disc_o's arguments
    'crack_o': ('r', 'tell', 'el', 'nd', 'hold'), 'chev_o': ('r', 'tell', 'el', 'nd', 'hold'), 'swirl_o': ('r', 'tell', 'el', 'nd', 'hold'),
    'hexagram_o': ('r', 'tell', 'el', 'hold'), 'starseal_o': ('r', 'tell', 'el', 'hold'), 'seal8_o': ('r', 'tell', 'el', 'hold'),
    'mask_wash': ('r', 'tell', 'hold'), 'safe_rim': ('id', 'r', 'tell', 'hold'), 'safe_beam': ('id',),
    'safe_end': ('id',), 'crater': ('r', 'tell', 'hold'), 'halo': ('r', 'h', 'tell', 'el', 'hold'),
    'glyph_circle': ('r', 'tell', 'hold'),
    'field': ('id', 'r', 'el', 'life'), 'strip': ('id', 'len', 'w', 'yaw', 'el', 'life'), 'field_end': ('id',),
    'field_clear': (), 'clear': ()}
SIZE_KEYS = ('r', 'r0', 'r1', 'w', 'len', 'back', 'h')


def tele(shape, **args):
    """Any telegraph call: sizes in blocks (converted to tenths), angles in degrees, ticks; strings pass through as
    macro placeholders. Every key of TELE_ARGS[shape] must be given."""
    assert shape in TELE_ARGS, shape
    need = TELE_ARGS[shape]
    assert set(args) == set(need), (shape, sorted(args), need)
    if not need:
        return f'function {FN}tele/{shape}'
    body = ','.join(f'{k}:{_t(args[k]) if k in SIZE_KEYS else (num(float(args[k]), 2) if k == "d" else _n(args[k]))}'
                    for k in need)
    return f'function {FN}tele/{shape} {{{body}}}'


def tele_disc(r, tell, el=5, nd=0, hold=3, fill=1, style=None):
    """Disc decal of radius r blocks; the fill reaches the rim `tell` ticks after the call (pair with hz/disc).
    fill=0: the outline-only variant tele/disc_o (the rim alone, flashing on the hit; same arguments); style 'crack' /
    'chev' / 'swirl': the shaped outline tele/<style>_o instead of the plain rim (FIX FID-4)."""
    if style:
        return tele(f'{style}_o', r=r, tell=tell, el=el, nd=nd, hold=hold)
    return tele('disc' if fill else 'disc_o', r=r, tell=tell, el=el, nd=nd, hold=hold)


def tele_ring(r0, r, tell, el=5, nd=0, hold=3):
    return tele('ring', r0=r0, r=r, tell=tell, el=el, nd=nd, hold=hold)


def tele_sector(r, a, tell, el=5, nd=0, hold=3):
    """Sector decal, half-angle a degrees (7.5-degree steps; a >= 175 = a disc), apex at the point, aim = rotation."""
    return tele('sector', r=r, a=a, tell=tell, el=el, nd=nd, hold=hold)


def tele_wedge(r0, r1, a0, a1, tell, el=5, nd=1, hold=3):
    """Annular-sector decal between yaws a0 < a1 (degrees relative to the executor, + = clockwise from above) and radii
    r0..r1 blocks. Annular wedges (r0 > 0) need r0 / r1 in [0.0625, 0.84] and a1 - a0 <= 105."""
    if not isinstance(a0, str) and not isinstance(a1, str):
        assert a0 < a1 <= a0 + 180, (a0, a1)
    if not isinstance(r0, str) and not isinstance(a0, str) and not isinstance(a1, str) and r0:
        assert a1 - a0 <= 105, 'annular wedges span at most 105 degrees'
    return tele('wedge', r0=r0, r1=r1, a0=a0, a1=a1, tell=tell, el=el, nd=nd, hold=hold)


def tele_line(length, w, tell, el=5, nd=0, hold=3, back=0.0):
    return tele('line', len=length, w=w, back=back, tell=tell, el=el, nd=nd, hold=hold)


def tele_lane_side(length, w, tell, el=5, hold=3, back=0.0):
    """Flank strip (성동격서): the line with the undodgeable look and a dust wall on the outer rail = the executor's
    LEFT (+x). Run the left flank's strip rotated as the body axis, the right flank's rotated 180 degrees."""
    return tele('lane_side', len=length, w=w, back=back, tell=tell, el=el, hold=hold)


def tele_wave(wid, r0, r1, w, tell, dur, el=5, nd=0, hold=2):
    """Expanding front id 0-7: the start disc fills to r0 over the tell, then the front ring travels r0 -> r1 in dur
    ticks with the band edge w behind it (pair with hz/ring + hz/resize_s; N10)."""
    return tele('wave', id=wid, r0=r0, r1=r1, w=w, tell=tell, dur=dur, el=el, nd=nd, hold=hold)


def tele_wave_to(wid, r, dur):
    """Retarget a live front from its current radius to r over dur ticks (eased fronts as linear segments)."""
    return tele('wave_to', id=wid, r=r, dur=dur)


def tele_wave_end(wid):
    return tele('wave_end', id=wid)


def tele_mline(mid, length, w, tell, el=5, nd=0, hold=0, back=0.0):
    return tele('mline', id=mid, len=length, w=w, back=back, tell=tell, el=el, nd=nd, hold=hold)


def tele_mline_aim(mid):
    return tele('mline_aim', id=mid)


def tele_mline_turn(mid, d):
    return tele('mline_turn', id=mid, d=d)


def tele_mline_end(mid):
    return tele('mline_end', id=mid)


def tele_heptagram(r, tell, el=4, hold=3, fill=1):
    """fill=0: the outline-only variant tele/heptagram_o (the seal art + rim, no progress fill; same arguments)."""
    return tele('heptagram' if fill else 'heptagram_o', r=r, tell=tell, el=el, hold=hold)


def tele_hexagram(r, tell, el=3, hold=3, fill=1):
    """fill=0: the outline-only variant tele/hexagram_o (the seal art + rim, no progress fill; same arguments)."""
    return tele('hexagram' if fill else 'hexagram_o', r=r, tell=tell, el=el, hold=hold)


def tele_starseal(r, tell, el=4, hold=3, fill=1):
    """fill=0: the outline-only variant tele/starseal_o (the seal art + rim, no progress fill; same arguments)."""
    return tele('starseal' if fill else 'starseal_o', r=r, tell=tell, el=el, hold=hold)


def tele_seal8(r, tell, el=1, hold=3, fill=1):
    """fill=0: the outline-only variant tele/seal8_o (the seal art + rim, no progress fill; same arguments)."""
    return tele('seal8' if fill else 'seal8_o', r=r, tell=tell, el=el, hold=hold)


def tele_mask_wash(r, tell, hold=3):
    return tele('mask_wash', r=r, tell=tell, hold=hold)


def tele_safe_rim(sid, r, tell, hold=3):
    return tele('safe_rim', id=sid, r=r, tell=tell, hold=hold)


def tele_safe_beam(sid):
    return tele('safe_beam', id=sid)


def tele_safe_end(sid):
    return tele('safe_end', id=sid)


def tele_crater(r, tell, hold):
    return tele('crater', r=r, tell=tell, hold=hold)


def tele_halo(r, h, tell, el=1, hold=2):
    return tele('halo', r=r, h=h, tell=tell, el=el, hold=hold)


def tele_glyph_circle(r, tell, hold):
    """The intro seal's gold floor glyph circle (decor; plan §2.2 / §5 E), drawn in over `tell`, staying `hold`."""
    return tele('glyph_circle', r=r, tell=tell, hold=hold)


def tele_field(fid, r, el, life):
    return tele('field', id=fid, r=r, el=el, life=life)


def tele_strip(fid, length, w, yaw, el, life):
    return tele('strip', id=fid, len=length, w=w, yaw=yaw, el=el, life=life)


def tele_field_end(fid):
    return tele('field_end', id=fid)


def tele_field_clear():
    return tele('field_clear')


def tele_clear():
    return tele('clear')


def snd(name):
    assert name in SOUNDS or name in SFAM, name
    return f'function {FN}snd/{name}'


def snde(name, el):
    """a sound family member fx/snd/<name>/<el> (el an int in the family's range); a '$(..)' placeholder el calls the
    dispatcher fx/snd/<name> {el} instead (static target names; out-of-range values follow the family rule)"""
    assert name in SFAM, name
    if isinstance(el, str):
        return f'function {FN}snd/{name} {{el:{el}}}'
    lo, hi = SFAM_RANGE[name]
    assert lo <= el <= hi, (name, el)
    return f'function {FN}snd/{name}/{el}'


ARG_SIZE = ('r', 'r0', 'r1', 'w', 'len', 'h')
ARG_TICK = ('t', 'dur')


def _parg(k, v):
    if isinstance(v, str):
        return v
    if k in ARG_SIZE:
        return _t(v)
    return str(int(v))


def fx(name, **args):
    """A preset fx/p/<name> (sizes in blocks are converted to tenths, ticks as ints; strings pass through as macro
    placeholders); a family name with el=... calls its dispatcher."""
    if name in EPRESETS:
        need = ['el'] + EPRESETS[name][1]
    else:
        assert name in PRESETS, name
        need = PRESETS[name][1]
    assert set(args) == set(need), (name, sorted(args), need)
    if not need:
        return f'function {FN}p/{name}'
    body = ','.join(f'{k}:{_parg(k, args[k]) if k != "el" else _i(args[k])}' for k in need)
    return f'function {FN}p/{name} {{{body}}}'


def fxe(name, el, **args):
    """A family preset member fx/p/<name>/<el> (el 1..5, 0 and 6-8 draw Geo); a '$(..)' placeholder el calls the
    dispatcher fx/p/<name> {el, ...} instead (static target names, same clamp)."""
    assert name in EPRESETS, name
    need = EPRESETS[name][1]
    assert set(args) == set(need), (name, sorted(args), need)
    if isinstance(el, str):
        return fx(name, el=el, **args)
    el = el if 1 <= el <= 5 else 5
    if not need:
        return f'function {FN}p/{name}/{el}'
    body = ','.join(f'{k}:{_parg(k, args[k])}' for k in need)
    return f'function {FN}p/{name}/{el} {{{body}}}'


def look(kind, col=WHITE):
    assert kind in KINDS, kind
    return f'function {FN}look {{kind:"{kind}",col:{int(col)}}}'


def prop(name):
    """As @s = an item_display prop: dress it as a kit prop look (fx/prop/<name>)."""
    assert name in PROPS or name in PFAM, name
    return f'function {FN}prop/{name}'


def prope(name, el):
    """a prop family member (as @s); a '$(..)' placeholder el calls the dispatcher fx/prop/<name> {el}"""
    assert name in PFAM, name
    if isinstance(el, str):
        return f'function {FN}prop/{name} {{el:{el}}}'
    lo, hi = PFAM[name][1]
    assert lo <= el <= hi, (name, el)
    return f'function {FN}prop/{name}/{el}'


def hud(name, **args):
    assert name in HUD_FUNCS or name in HFAM, name
    if args:
        return f'function {FN}hud/{name} {{' + ','.join(f'{k}:{v}' for k, v in args.items()) + '}'
    return f'function {FN}hud/{name}'


def hude(name, el):
    """a banner family member; a '$(..)' placeholder el calls the dispatcher fx/hud/<name> {el}"""
    assert name in HFAM, name
    if isinstance(el, str):
        return f'function {FN}hud/{name} {{el:{el}}}'
    assert 1 <= el <= 4, (name, el)
    return f'function {FN}hud/{name}/{el}'


def gl(name, extra=''):
    return '{text:"' + glyph(name) + '",font:"' + FONT + '",color:"white"' + extra + '}'


def badge(el, lit=True):
    """The name-line badge "◈물" as a text-component SNBT: dim #707070 until absorbed (lit False), then the element
    colour (Pyro #FF8A3D, Hydro #4FB8FF, Electro #C58BFF, Cryo #9FE8F5)."""
    col = EL_HEX[el] if lit else DIM_HEX
    return (f'{{text:"",extra:[{{text:" "}},{{text:"{glyph("badge")}",font:"{FONT}",color:"{col}"}},'
            f'{{text:"{EL_NAMES[el]}",color:"{col}"}}]}}')


def brand_badge(el):
    """The third badge "◈낙인" while branded (the brand badge glyph in the element colour)."""
    col = EL_HEX[el]
    return (f'{{text:"",extra:[{{text:" "}},{{text:"{glyph("brand")}",font:"{FONT}",color:"{col}"}},'
            f'{{text:"낙인",color:"{col}"}}]}}')


# ----------------------------------------------------------------------------- particles (vanilla)


def colour_list(c):
    if isinstance(c, int):
        c = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
    return '[' + ','.join(num(float(x), 3) + 'f' for x in c) + ']'


def part(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    d = ' '.join(v if isinstance(v, str) else num(float(v), 3) for v in delta)
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


def fdust(block, pos='~ ~ ~', delta=(0, 0, 0), n=1):
    return part(f'falling_dust{{block_state:"minecraft:{block}"}}', pos, delta, 0.0, n)


def el_parts(el, pos='~ ~0.3 ~', spread=0.6, n=6):
    """the element's vanilla particle signature (used by most family presets)"""
    s = (spread, spread * 0.5, spread)
    if el == 1:
        return [part('flame', pos, s, 0.04, n), part('lava', pos, s, 0, max(1, n // 3)),
                dust(rgb('#EB8029'), 1.6, pos, s, max(1, n // 2))]
    if el == 2:
        return [part('splash', pos, s, 0.2, n * 2), part('bubble_pop', pos, s, 0.05, n),
                dust(rgb('#12BDDE'), 1.5, pos, s, max(1, n // 2))]
    if el == 3:
        return [part('electric_spark', pos, s, 0.25, n), part('witch', pos, s, 0.05, max(1, n // 2)),
                dust(rgb('#DB8BE4'), 1.4, pos, s, max(1, n // 2))]
    if el == 4:
        return [part('snowflake', pos, s, 0.05, n), part('white_ash', pos, s, 0.02, n),
                dust(rgb('#ABF3FC'), 1.4, pos, s, max(1, n // 2))]
    return [dust(rgb('#F0D8A3'), 1.4, pos, s, n), part('wax_off', pos, s, 0, max(1, n // 2)),
            fdust('yellow_concrete_powder', pos, s, max(1, n // 3))]


# ----------------------------------------------------------------------------- sound recipes
# name -> (comment, [(event, volume, pitch), ...]); one tick each, vanilla events only. The creature layers (roars,
# growls, the warden's dig / emerge) are the dragon's own body sounds named by the plan's §5 rows; no speech-like
# voices (villagers, illagers' speech, witches, piglins, players' voices) are used.
SOUNDS = {
    # P1 chin slam
    'chin_rear': ('P1 rear-up (t0..t10): a deep roar and growl.',
                  [('entity.ravager.roar', 1.0, 0.6), ('entity.ender_dragon.growl', 0.5, 0.7)]),
    'chin_impact': ('P1 impact t35: heavy smash, boom and crystal crack.',
                    [('item.mace.smash_ground_heavy', 1.0, 0.5), ('entity.generic.explode', 1.0, 0.5),
                     ('block.amethyst_cluster.break', 1.0, 0.6)]),
    # P2 jump slam
    'jump_takeoff': ('P2 take-off t6: a heave and a whoosh.',
                     [('entity.ravager.attack', 1.0, 0.5), ('item.trident.riptide_3', 0.5, 0.5)]),
    'jump_land': ('P2 landing t21: smash, boom, anvil.',
                  [('item.mace.smash_ground_heavy', 1.0, 0.6), ('entity.generic.explode', 1.0, 0.6),
                   ('block.anvil.land', 0.5, 0.5)]),
    'jump_wave2': ('P2 second ground wave t32: deep crack and falling stone.',
                   [('block.deepslate.break', 1.0, 0.5), ('block.pointed_dripstone.land', 1.0, 0.6)]),
    # P3 charge
    'charge_growl': ('P3 growl and coil (t0): roar + growl.',
                     [('entity.ravager.roar', 1.0, 0.6), ('entity.ender_dragon.growl', 0.5, 0.8)]),
    'charge_gallop': ('P3 gallop step (every 4 t of the run): heavy steps and gravel.',
                      [('entity.ravager.step', 1.0, 0.5), ('entity.iron_golem.step', 1.0, 0.5),
                       ('block.gravel.break', 1.0, 0.6)]),
    'charge_skid': ('P3 skid stop: gravel scrape and grind.',
                    [('block.gravel.hit', 1.0, 0.5), ('block.grindstone.use', 1.0, 0.5)]),
    # P4 back spikes
    'spikes_bristle': ('P4 bristle (t0, gold glow): charge hum.',
                       [('entity.breeze.charge', 1.0, 0.6), ('block.respawn_anchor.charge', 1.0, 0.7)]),
    'spikes_launch': ('P4 launch t14: four rockets of spikes.',
                      [('entity.blaze.shoot', 1.0, 0.5), ('entity.firework_rocket.launch', 1.0, 0.6),
                       ('entity.firework_rocket.launch', 0.8, 0.65), ('entity.firework_rocket.launch', 0.7, 0.55),
                       ('entity.firework_rocket.launch', 0.6, 0.7)]),
    'spikes_land': ('P4 spike landing: crack, dripstone thud, crystal.',
                    [('entity.generic.explode', 0.5, 1.2), ('block.pointed_dripstone.land', 1.0, 1.0),
                     ('block.amethyst_cluster.break', 1.0, 0.8)]),
    'spikes_explode': ('P4 planted spike explodes: boom and crystal.',
                       [('entity.generic.explode', 1.0, 1.0), ('block.amethyst_block.break', 1.0, 1.0)]),
    # P5 / P5b stomp
    'stomp_slam': ('P5 / P5b paw slam: boom, golem thud, crystal.',
                   [('entity.generic.explode', 1.0, 0.6), ('entity.iron_golem.damage', 1.0, 0.5),
                    ('block.amethyst_block.break', 1.0, 1.0)]),
    'stomp_wave': ('P5 / P5b ground wave: deplete thrum and a sonic charge.',
                   [('block.respawn_anchor.deplete', 1.0, 0.6), ('entity.warden.sonic_charge', 0.3, 1.4)]),
    # P6 feint
    'feint_sway': ('P6 sway (call twice): heartbeat and a heavy step.',
                   [('entity.warden.heartbeat', 1.0, 0.6), ('block.deepslate.step', 1.0, 1.0)]),
    'feint_burst': ('P6 flank eruption t22: boom, crystal, basalt.',
                    [('entity.generic.explode', 1.0, 0.9), ('block.amethyst_block.break', 1.0, 0.6),
                     ('block.basalt.break', 1.0, 0.8), ('block.basalt.break', 1.0, 0.9), ('block.basalt.break', 0.9, 1.0),
                     ('block.basalt.break', 0.8, 0.7)]),
    # P7 tail whip
    'whip_raise': ('P7 tail raise: a low rumble.', [('entity.warden.ambient', 0.4, 0.6)]),
    'whip_sweep': ('P7 sweep t23: a wind burst and a riptide whoosh.',
                   [('entity.breeze.wind_burst', 1.0, 0.6), ('item.trident.riptide_3', 0.6, 0.7)]),
    'whip_erupt': ('P7 end-line eruption t33: boom and crystal.',
                   [('entity.generic.explode', 1.0, 1.0), ('block.amethyst_cluster.break', 1.0, 1.0)]),
    # P8 tail slam
    'tslam_raise': ('P8 tail raised high: dripping lava tick and a rumble.',
                    [('block.pointed_dripstone.drip_lava', 1.0, 1.0), ('entity.warden.ambient', 0.6, 0.8)]),
    'tslam_impact': ('P8 impact t39: boom, anvil, three dripstone thuds, leaves.',
                     [('entity.generic.explode', 1.0, 0.6), ('block.anvil.land', 0.5, 0.5),
                      ('block.pointed_dripstone.land', 1.0, 0.9), ('block.pointed_dripstone.land', 0.9, 1.1),
                      ('block.pointed_dripstone.land', 0.8, 0.8), ('block.cherry_leaves.break', 1.0, 0.7)]),
    # P9 burrow charge
    'burrow_dive': ('P9 dive: digging and roots tearing.',
                    [('entity.warden.dig', 1.0, 0.8), ('block.rooted_dirt.break', 1.0, 0.6)]),
    'burrow_loop': ('P9 underground loop (every 30 t): muffled digging.', [('entity.warden.dig', 0.4, 0.6)]),
    'burrow_ring': ('P9 rock-ring marker: rising charge and a chime.',
                    [('block.respawn_anchor.charge', 0.5, 1.4), ('block.amethyst_block.chime', 1.0, 0.8)]),
    'burrow_rock': ('P9 rock lands: smash and crystal.',
                    [('item.mace.smash_ground_heavy', 1.0, 0.8), ('block.amethyst_cluster.break', 1.0, 0.8)]),
    'burrow_rush': ('P9 surfacing rush / emergence: emerge, roar, boom.',
                    [('entity.warden.emerge', 1.0, 0.9), ('entity.ravager.roar', 0.6, 0.6),
                     ('entity.generic.explode', 1.0, 0.7)]),
    # T1 landslide
    'slide_lift': ('T1 lift (fore + hind paw rise): heavy step and deepslate.',
                   [('entity.ravager.step', 1.0, 0.5), ('block.deepslate.step', 1.0, 0.6)]),
    'slide_wave': ('T1 waves 1-5: a wide boom (volume 2 = heard across the arena), basalt, crystal, falling stone.',
                   [('entity.generic.explode', 2.0, 0.5), ('block.basalt.break', 1.0, 0.6),
                    ('block.amethyst_cluster.break', 1.0, 0.7), ('block.pointed_dripstone.land', 1.0, 0.8),
                    ('block.pointed_dripstone.land', 0.9, 1.0), ('block.pointed_dripstone.land', 0.8, 0.7)]),
    'slide_wave6': ('T1 wave 6 (the whole arena): the wave layers + the warden emerging.',
                    [('entity.generic.explode', 2.0, 0.5), ('block.basalt.break', 1.0, 0.6),
                     ('block.amethyst_cluster.break', 1.0, 0.7), ('block.pointed_dripstone.land', 1.0, 0.8),
                     ('entity.warden.emerge', 1.0, 0.8)]),
    'jump_cue': ('The "점프!" bell (wave - 8).', [('block.note_block.bell', 1.0, 1.2)]),
    # T2 / T3 absorbs, roar, the message
    'absorb_roar': ('Absorb roar (roar_rear): growl and roar.',
                    [('entity.ender_dragon.growl', 1.0, 0.55), ('entity.ravager.roar', 1.0, 0.5)]),
    'roar_ring': ('One roar shock-dome ring.', [('entity.warden.sonic_boom', 0.25, 1.6)]),
    'msg_chime': ('The transition message: resonating bell and a charge.',
                  [('block.bell.resonate', 1.0, 0.6), ('block.respawn_anchor.charge', 1.0, 0.5)]),
    # B3
    'b3_sink': ('B3 sink: dig and gravel.',
                [('entity.warden.dig', 1.0, 0.8), ('block.gravel.break', 1.0, 0.5), ('block.gravel.break', 0.9, 0.6),
                 ('block.gravel.break', 0.8, 0.55)]),
    'b3_rise': ('B3 tail rises: emerge and dripstone.',
                [('entity.warden.emerge', 1.0, 1.0), ('block.pointed_dripstone.break', 1.0, 0.6)]),
    'b3_emerge': ('B3 emergence burst t388: boom, emerge, basalt.',
                  [('entity.generic.explode', 1.0, 0.6), ('entity.warden.emerge', 1.0, 0.8),
                   ('block.basalt.break', 1.0, 0.8), ('block.basalt.break', 1.0, 0.9), ('block.basalt.break', 0.9, 0.7),
                   ('block.basalt.break', 0.8, 1.0)]),
    # 31 orbs
    'orb_spawn': ('31 orbs appear / pass: a riptide swirl and a splash.',
                  [('item.trident.riptide_1', 1.0, 0.8), ('entity.dolphin.splash', 1.0, 1.0)]),
    'orb_loop': ('31 orb loop (every 20-40 t): whirlpool and conduit hum.',
                 [('block.bubble_column.whirlpool_ambient', 1.0, 1.0), ('block.conduit.ambient', 1.0, 1.4)]),
    'orb_hit': ('31 orb hits a player: a splash.', [('entity.player.splash', 1.0, 1.0)]),
    # 32 meteors
    'meteor_glyph': ('32 seal glyph: charge and beacon.',
                     [('block.respawn_anchor.charge', 1.0, 0.7), ('block.beacon.activate', 1.0, 0.6)]),
    'meteor_fall': ('32 meteor falling.', [('entity.blaze.shoot', 1.0, 0.5)]),
    'meteor_impact': ('32 big meteor impact: boom, dragon fireball, sizzle.',
                      [('entity.generic.explode', 1.0, 0.6), ('entity.dragon_fireball.explode', 1.0, 1.0),
                       ('block.fire.extinguish', 1.0, 1.0)]),
    'meteor_small': ('32 small meteor: a blast and a light boom.',
                     [('entity.firework_rocket.blast', 1.0, 0.6), ('entity.generic.explode', 0.4, 1.1)]),
    # 33 fire fields
    'fire_loop': ('33 fire field loop (every 20 t): fire and crackle.',
                  [('block.fire.ambient', 1.0, 1.0), ('block.campfire.crackle', 1.0, 1.0)]),
    # 41 frost circles
    'frost_draw': ('41 star drawn: resonance and a thin beacon.',
                   [('block.amethyst_block.resonate', 1.0, 1.4), ('block.beacon.activate', 0.3, 1.8)]),
    'frost_icicle': ('41 icicle thrown and shattering.', [('item.trident.throw', 1.0, 0.6), ('block.glass.break', 1.0, 0.6)]),
    'frost_burst': ('41 burst: powder snow breaking and a light boom.',
                    [('block.powder_snow.break', 1.0, 1.0), ('block.powder_snow.break', 0.9, 0.8),
                     ('block.powder_snow.break', 0.8, 1.2), ('entity.generic.explode', 0.3, 1.6)]),
    # 42 lightning rounds
    'bolt_marker': ('42 round markers (48 t before): high charge and a select tone.',
                    [('block.respawn_anchor.charge', 0.5, 1.6), ('block.beacon.power_select', 0.4, 1.8)]),
    'bolt_strike': ('42 strike: thunder, bolt impacts (call again over 20 t for the 6-8 impacts), crystal.',
                    [('entity.lightning_bolt.thunder', 0.8, 1.0), ('entity.lightning_bolt.impact', 1.0, 1.1),
                     ('entity.lightning_bolt.impact', 1.0, 1.3), ('block.amethyst_cluster.break', 1.0, 1.0)]),
    'safe_chime': ('42 the player is inside a safe circle: a bright chime.',
                   [('block.amethyst_block.chime', 1.0, 1.6), ('block.note_block.bell', 0.6, 1.8)]),
    # 43 ice sphere
    'sphere_form': ('43 sphere forms: select tone and chimes.',
                    [('block.beacon.power_select', 1.0, 1.6), ('block.amethyst_block.chime', 1.0, 1.2),
                     ('block.amethyst_block.chime', 1.0, 1.5), ('block.amethyst_block.chime', 1.0, 1.8)]),
    'sphere_loop': ('43 sphere loop: conduit hum.', [('block.conduit.ambient', 1.0, 1.6)]),
    'lance': ('43 lance: riptide whoosh, glass and a light boom.',
              [('item.trident.riptide_1', 1.0, 1.6), ('block.glass.break', 1.0, 1.0), ('entity.generic.explode', 0.4, 1.4)]),
    # 44 shells
    'shell_spawn': ('44 shell spawn: spell cast and resonance.',
                    [('entity.evoker.cast_spell', 1.0, 1.6), ('block.amethyst_block.resonate', 1.0, 1.4)]),
    'shell_hover': ('44 shells hovering: high beacon hum.', [('block.beacon.ambient', 1.0, 1.8)]),
    'shell_dive': ('44 shell dives: a swoop.', [('entity.phantom.swoop', 0.4, 1.6)]),
    'shell_impact': ('44 shell impact: bolt impact and a light boom.',
                     [('entity.lightning_bolt.impact', 0.6, 1.3), ('entity.generic.explode', 0.35, 1.5)]),
    # 45 ice spikes
    'ice_launch': ('45 launch: three breeze shots and dripstone.',
                   [('entity.breeze.shoot', 1.0, 0.7), ('entity.breeze.shoot', 0.9, 0.75), ('entity.breeze.shoot', 0.8, 0.65),
                    ('block.pointed_dripstone.break', 1.0, 1.0)]),
    'ice_land': ('45 dark spike lands.', [('item.trident.hit_ground', 1.0, 0.5), ('block.basalt.break', 1.0, 0.6)]),
    'ice_erupt': ('45 ice eruption.', [('block.amethyst_cluster.place', 1.0, 0.6), ('block.glass.break', 1.0, 0.8)]),
    'hail': ('45 hail ticking (quiet).', [('block.powder_snow.step', 0.2, 1.5), ('block.glass.hit', 0.2, 1.5)]),
    # 46 electro spikes
    'hex_draw': ('46 hexagram drawn: spawn-point set and enchanting.',
                 [('block.respawn_anchor.set_spawn', 1.0, 1.6), ('block.enchantment_table.use', 1.0, 1.2)]),
    'hex_bolt': ('46 bolt before a lump: thin thunder.', [('entity.lightning_bolt.thunder', 0.25, 1.6)]),
    'hex_impact': ('46 lump impact: dripstone, crystal, bolt.',
                   [('block.pointed_dripstone.land', 1.0, 0.5), ('block.amethyst_block.break', 1.0, 0.8),
                    ('entity.lightning_bolt.impact', 0.5, 1.0)]),
    # E intro
    'intro_drone': ('E sealed drone (loop every 40 t).', [('block.respawn_anchor.ambient', 1.0, 0.5)]),
    'intro_thump': ('E heartbeat thump of the sealed body.', [('entity.ravager.step', 1.0, 0.5)]),
    'stele_break': ('E a seal stele shatters.',
                    [('block.deepslate_bricks.break', 1.0, 0.6), ('block.deepslate_bricks.break', 0.9, 0.55),
                     ('block.deepslate_bricks.break', 0.8, 0.65), ('entity.generic.explode', 0.4, 0.8)]),
    'seal_shatter': ('E the seal prism shatters (t112).',
                     [('block.glass.break', 1.0, 0.6), ('block.amethyst_block.break', 1.0, 0.7),
                      ('block.beacon.deactivate', 1.0, 1.0)]),
    'intro_roar': ('E the roar (t120).',
                   [('entity.ender_dragon.growl', 1.0, 0.6), ('entity.ravager.roar', 1.0, 0.5),
                    ('entity.warden.roar', 0.6, 0.8)]),
    # D death
    'death_sting': ('D music cut with a sting.', [('block.beacon.deactivate', 1.0, 0.6)]),
    'death_fall': ('D the body falls (chin t34 / tail t66 / head t92).',
                   [('entity.iron_golem.death', 1.0, 0.5), ('entity.ravager.death', 1.0, 0.6)]),
    'death_seal': ('D the seal re-forms.', [('block.amethyst_block.resonate', 1.0, 1.0)]),
    # brand, shards, hints
    'brand_apply': ('Brand applied: a searing tone and a crystal tick.',
                    [('block.respawn_anchor.set_spawn', 0.6, 1.4), ('block.fire.extinguish', 0.4, 1.6),
                     ('block.amethyst_block.hit', 1.0, 0.8)]),
    'brand_tick': ('A brand DoT tick (quiet).', [('block.amethyst_block.step', 0.4, 1.4), ('block.fire.extinguish', 0.2, 2.0)]),
    'cleanse': ('The brand is cleansed (butterfly-style cure chime).',
                [('block.amethyst_block.chime', 1.0, 1.4), ('block.beacon.power_select', 0.8, 1.8),
                 ('block.note_block.chime', 0.8, 1.6)]),
    'shard_spawn': ('응결 결정 sheds from the back.', [('block.amethyst_cluster.place', 1.0, 1.2), ('block.beacon.activate', 0.4, 1.6)]),
    'shard_pick': ('응결 결정 picked up (the shield).',
                   [('block.amethyst_block.resonate', 1.0, 1.6), ('entity.experience_orb.pickup', 0.8, 0.8),
                    ('block.beacon.power_select', 0.7, 1.4)]),
    'hint': ('A first-time hint line.', [('block.note_block.pling', 0.6, 1.2)]),
}
# element families: name -> (range, {el: (comment, layers)})
SFAM = {
    'absorb_vortex': ((1, 4), {
        1: ('T2 Pyro swirl.', [('item.firecharge.use', 1.0, 1.0), ('entity.blaze.shoot', 1.0, 0.6)]),
        2: ('T2 Hydro vortex.', [('block.bubble_column.whirlpool_ambient', 1.0, 1.0), ('entity.player.splash.high_speed', 1.0, 0.7)]),
        3: ('T3 Electro charge.', [('block.beacon.ambient', 1.0, 0.6), ('item.trident.thunder', 0.4, 1.4)]),
        4: ('T3 Cryo gather.', [('block.amethyst_block.chime', 1.0, 1.0), ('block.powder_snow.step', 1.0, 1.0)])}),
    'absorb_burst': ((1, 4), {
        1: ('T2 Pyro burst.', [('entity.ghast.shoot', 1.0, 0.5), ('block.lava.pop', 1.0, 1.0), ('block.lava.pop', 1.0, 0.8),
                               ('block.lava.pop', 1.0, 1.2)]),
        2: ('T2 Hydro burst.', [('block.conduit.activate', 1.0, 0.8), ('block.beacon.power_select', 1.0, 0.6)]),
        3: ('T3 Electro discharge.', [('entity.lightning_bolt.impact', 1.0, 1.0), ('entity.lightning_bolt.thunder', 0.8, 0.8)]),
        4: ('T3 Cryo burst.', [('block.glass.break', 1.0, 0.6), ('entity.player.hurt_freeze', 1.0, 1.0),
                               ('entity.generic.explode', 1.0, 1.2)])}),
    'footfall': ((1, 5), {
        1: ('Pyro footfall: a flame splash on the step.', [('entity.ravager.step', 0.5, 0.5), ('block.fire.ambient', 0.4, 1.2),
                                                         ('item.firecharge.use', 0.2, 1.6)]),
        2: ('Hydro footfall: a splash.', [('entity.ravager.step', 0.5, 0.5), ('entity.player.splash', 0.4, 0.8)]),
        3: ('Electro footfall: sparks.', [('entity.ravager.step', 0.5, 0.5), ('block.amethyst_block.step', 0.6, 1.4),
                                          ('entity.lightning_bolt.impact', 0.1, 2.0)]),
        4: ('Cryo footfall: frost crunch.', [('entity.ravager.step', 0.5, 0.5), ('block.powder_snow.step', 0.8, 0.8)]),
        5: ('Geo footfall: heavy stone step.', [('entity.ravager.step', 0.5, 0.5), ('block.deepslate.step', 0.6, 0.6)])}),
}
SFAM_RANGE = {k: v[0] for k, v in SFAM.items()}


def min_volume(vol):
    """mboss_lib.min_volume (the Guardian's L.sound): quiet layers (<= 0.25) fade out completely past their range,
    louder ones keep a third of their volume there, at most 0.4."""
    if vol <= 0.25:
        return 0.0
    return round(min(0.4, vol / 3), 2)


def sound_line(event, vol, pitch):
    return (f'playsound minecraft:{event} hostile @a[tag=player] ~ ~ ~ {num(float(vol))} {num(float(pitch))} '
            f'{num(float(min_volume(vol)), 2)}')


def all_sound_layers():
    out = []
    for _doc, layers in SOUNDS.values():
        out += layers
    for (_rng, mem) in SFAM.values():
        for _doc, layers in mem.values():
            out += layers
    return out


# ----------------------------------------------------------------------------- presets
PRESETS = {}        # name -> (doc, [args], fn() -> lines)
EPRESETS = {}       # family name -> (doc, [args], {el: fn() -> lines})  (fx/p/<name>/<el>, el 1..5)
# ambient presets: skipped from SOFT live fx cards on (trails, auras, ambience)
AMBIENT = ('blade_trail', 'lump_trail', 'icicle_trail', 'ice_sphere', 'orb_ribbon', 'hail', 'glyph_glow', 'gold_motes',
           'dust_trail', 'fire_field')
# trail presets (FIX STATE-14): kicked-up dust, thrown boulders and grit that run over several ticks are skipped from
# TSOFT live fx cards on, so the hit-tick visuals (impacts, bolts, eruptions) always find room under CAP
TRAIL = ('boulders', 'tail_lane', 'dust')


def preset(name, doc, args=()):
    def deco(f):
        PRESETS[name] = (doc, list(args), f)
        return f
    return deco


def epreset(name, doc, args=()):
    def deco(f):
        EPRESETS[name] = (doc, list(args), {el: (lambda el=el: f(el)) for el in range(1, 6)})
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


def rad(kind, yaw, elev, d0, d1, y=0.3, s0=0.5, s1=1.2, life=8, fade=3, col=WHITE, dly=0, dur=0, roll=0):
    """Radial trick: a fixed face card pointing outward along yaw / elevation, flying d0 -> d1 along it."""
    return card(kind, f'~ ~{num(y, 2)} ~', f'~{ang(yaw)} {ang(90 - elev)}', roll=roll, s0=s0, s1=s1,
                off=(0, d0, 0), move=(0, d1 - d0, 0), life=life, fade=fade, col=col, dly=dly, dur=dur)


def standing(kind, r, yaw, tilt, s0, s1, life, fade, col=WHITE, dly=0, dur=0, y=0.0):
    """A foot-pivot card (cross / face FOOT kinds) planted at radius r, yaw, leaning `tilt` degrees outward."""
    x, z = ring_xz(r, yaw)
    return card(kind, p3(x, y, z), f'~{ang(yaw)} {ang(tilt)}', s0=s0, s1=s1, life=life, fade=fade, col=col, dly=dly,
                dur=dur)


# --- element families -------------------------------------------------------------------------------------------
@epreset('impact', 'Impact burst at the floor point: Geo crystal-blade crown, Hydro splash, Pyro flame dome, Cryo ice '
         'spikes, Electro bolt and arcs; a flash and a shock ripple.')
def _e_impact(el):
    main, pale, deep, dcol = EL_FX[el]
    out = [card('glow', '~ ~0.6 ~', bb='center', s0=1.0, s1=3.5, life=5, fade=3, col=pale),
           card('ripple', '~ ~0.06 ~', '~ 0', spin=40, s0=0.6, s1=3.2, life=8, fade=4, dur=5, col=main)]
    rnd = random.Random(100 + el)
    if el == 5:
        for yaw in radial(6, 11):
            out.append(rad('blade', yaw, rnd.uniform(55, 75), 0.2, 1.1, s0=0.6, s1=rnd.uniform(1.8, 2.4), life=9,
                           fade=4, col=GOLD, roll=rnd.randint(-15, 15)))
        out += [card('dust', '~0.6 ~0.4 ~', bb='center', s0=0.6, s1=1.8, move=(0, 0.4, 0), life=12, fade=6, col=DUST),
                card('dust', '~-0.6 ~0.4 ~0.3', bb='center', s0=0.6, s1=1.7, move=(0, 0.35, 0), life=12, fade=6,
                     col=DUST, dly=1)]
    elif el == 2:
        out.append(card('splash', '~ ~ ~', bb='vertical', s0=1.0, s1=3.0, life=9, fade=4, dur=4))
        for yaw in radial(4, 45):
            out.append(rad('mote', yaw, 50, 0.2, 1.6, y=0.6, s0=0.3, s1=0.45, life=8, fade=3, col=HYDRO_PALE))
    elif el == 1:
        out.append(card('fire_dome', '~ ~ ~', bb='vertical', s0=1.0, s1=3.4, life=8, fade=4, dur=4))
        for yaw in radial(4, 0):
            out.append(standing('flame', 1.0, yaw, 15, 0.5, 1.6, 9, 4, dly=1, dur=4))
        out.append(card('smoke', '~ ~1.2 ~', bb='center', s0=0.6, s1=1.8, move=(0, 0.8, 0), life=14, fade=7))
    elif el == 4:
        for yaw in radial(6, 15):
            out.append(standing('ice_spike', 0.9, yaw, 25, 0.4, rnd.uniform(1.6, 2.2), 12, 5, dur=3))
        out += [card('frost', '~0.5 ~0.4 ~', bb='center', s0=0.6, s1=1.8, move=(0, 0.3, 0), life=12, fade=6),
                card('frost', '~-0.4 ~0.4 ~-0.3', bb='center', s0=0.6, s1=1.6, move=(0, 0.3, 0), life=12, fade=6, dly=1)]
    else:
        out += [card('bolt', '~ ~ ~', bb='vertical', s0=(1.2, 3.0, 1.2), s1=(1.8, 3.4, 1.8), life=4, fade=2),
                card('spark', '~ ~0.4 ~', bb='center', spin=60, s0=0.5, s1=2.0, life=5, fade=2, col=ELECTRO_PALE)]
        for k, roll in enumerate((20, 100, 160)):
            out.append(card('arc', '~ ~0.5 ~', bb='center', roll=roll, s0=0.6, s1=1.9, life=4, fade=2, dly=k,
                            col=ELECTRO))
    return out + el_parts(el, '~ ~0.4 ~', 0.7, 6)


@epreset('cracks', 'Crack fan along the executor yaw over radius {r} (tenths): glowing cracks in the element colour '
         '(Geo gold, Hydro white-cyan, Pyro lava, Cryo frost, Electro violet) with debris. At the impact point, rotated '
         'as the crack line.', ('r',))
def _e_cracks(el):
    main, pale, deep, dcol = EL_FX[el]
    out = [card('crackfan', '~ ~0.04 ~', '~ 0', s0='$(r_30)', s1='$(r)', life=40, fade=12, dur=3, col=pale),
           card('crackfan', '~ ~0.035 ~', '~ 0', s0='$(r)', s1='$(r)', life=14, fade=8, col=main)]
    if el in (5, 1):
        for k, (x, z) in enumerate(((0.6, 0.35), (-0.5, 0.6), (0.1, 0.85))):
            out.append(card('slab', f'^$(r_{int(x * 100) if x >= 0 else "m" + str(int(-x * 100))}) ^0.2 ^$(r_{int(z * 100)})',
                            f'~{20 * k} 0', spin=60, s0=0.5, s1=0.9, move=(0, 0.9, 0), life=14, fade=6, dur=6,
                            col=WHITE if el == 5 else rgb('#E0A080')))
    elif el == 2:
        out.append(card('splash', '^ ^ ^$(r_50)', bb='vertical', s0=0.8, s1=2.2, life=8, fade=4))
    elif el == 4:
        for z in (30, 60, 90):
            out.append(card('ice_spike', f'^ ^ ^$(r_{z})', '~ 15', s0=0.3, s1=1.2, life=12, fade=5, dur=3))
    else:
        for z, roll in ((40, 30), (75, 120)):
            out.append(card('arc', f'^ ^0.3 ^$(r_{z})', bb='center', roll=roll, s0=0.5, s1=1.6, life=5, fade=2,
                            col=ELECTRO))
    return out + el_parts(el, '^ ^0.3 ^$(r_50)', 0.8, 6)


@epreset('crown', 'Blade crown burst (P1 / the blade crowns): 10 element blades erupting out-and-up (Geo gold crystal, '
         'Hydro water, Pyro flame, Cryo ice, Electro violet crystal). At the floor point.')
def _e_crown(el):
    main, pale, deep, dcol = EL_FX[el]
    rnd = random.Random(200 + el)
    out = [card('glow', '~ ~0.8 ~', bb='center', s0=1.0, s1=4.0, life=6, fade=3, col=pale)]
    for k, yaw in enumerate(radial(10, 7)):
        if el == 1:
            out.append(standing('flame', 0.8, yaw, rnd.uniform(15, 35), 0.6, rnd.uniform(1.8, 2.6), 10, 4, dur=3))
        elif el == 4:
            out.append(standing('ice_spike', 0.8, yaw, rnd.uniform(15, 35), 0.5, rnd.uniform(2.0, 2.8), 12, 5, dur=3))
        elif el == 2:
            out.append(rad('blade', yaw, rnd.uniform(55, 75), 0.3, 1.2, s0=0.6, s1=rnd.uniform(1.8, 2.4), life=8,
                           fade=4, col=HYDRO_PALE))
        else:
            out.append(rad('blade', yaw, rnd.uniform(55, 78), 0.3, 1.2, s0=0.6, s1=rnd.uniform(2.0, 2.6), life=10,
                           fade=4, col=GOLD if el == 5 else ELECTRO, roll=rnd.randint(-12, 12)))
    return out + el_parts(el, '~ ~0.6 ~', 1.0, 8)


@epreset('dust_ring', 'Ring of element dust around the point at radius {r} (tenths): Geo khaki dust, Hydro spray, '
         'Pyro embers and smoke, Cryo frost, Electro sparks; a ripple out to r.', ('r',))
def _e_dust_ring(el):
    main, pale, deep, dcol = EL_FX[el]
    kind = {5: 'dust', 2: 'dust', 1: 'smoke', 4: 'frost', 3: 'dust'}[el]
    col = {5: DUST, 2: FOAM, 1: WHITE, 4: WHITE, 3: rgb('#B9A8D8')}[el]
    out = [card('ripple', '~ ~0.07 ~', '~ 0', spin=30, s0='$(r_30)', s1='$(r)', life=9, fade=4, dur=5, col=main)]
    for yaw in radial(8, 22.5):
        x, z = ring_xz(1.0, yaw)
        out.append(card(kind, f'^$(r_{int(-x * 80)}) ^0.5 ^$(r_{int(z * 80)})'.replace('_-', '_m'), bb='center',
                        s0=0.7, s1=2.0, move=(0, 0.5, 0), life=14, fade=7, col=col))
    return out + el_parts(el, '~ ~0.3 ~', 2.0, 8)


@epreset('slab_throw', 'Slab / boulder throw streaks (at the slab, rotated along the throw): speed streaks behind it and '
         'a trail in the element (Geo grit, Hydro water, Pyro embers, Cryo frost, Electro sparks).')
def _e_slab_throw(el):
    main, pale, deep, dcol = EL_FX[el]
    return [card('streak', '^0.3 ^0.1 ^-1.2', '~90 0', s0=(1.2, 1, 1), s1=(3.0, 1, 1), life=5, fade=2, col=pale),
            card('streak', '^-0.3 ^-0.2 ^-1.0', '~90 0', s0=(1.0, 1, 1), s1=(2.6, 1, 1), life=5, fade=2, col=main, dly=1),
            card('dust' if el != 1 else 'smoke', '^ ^ ^-0.8', bb='center', s0=0.4, s1=1.2, life=8, fade=4,
                 col=dcol if el != 1 else WHITE)] + el_parts(el, '^ ^ ^-0.6', 0.3, 3)


@epreset('footfall', 'Footfall at a planted foot (walk / turn plant events, plan §2.6): Geo dust, Hydro splash, Pyro '
         'flame splash, Cryo frost, Electro sparks.')
def _e_footfall(el):
    if el == 5:
        out = [card('dust', '~0.5 ~0.3 ~', bb='center', s0=0.6, s1=1.6, move=(0, 0.3, 0), life=10, fade=5, col=DUST),
               card('dust', '~-0.4 ~0.25 ~0.3', bb='center', s0=0.5, s1=1.4, move=(0, 0.25, 0), life=10, fade=5,
                    col=DUST_KHAKI)]
    elif el == 2:
        out = [card('splash', '~ ~ ~', bb='vertical', s0=0.6, s1=1.8, life=7, fade=3),
               card('ripple', '~ ~0.06 ~', '~ 0', s0=0.5, s1=2.0, life=8, fade=4, col=HYDRO_PALE)]
    elif el == 1:
        out = [card('flame', '~0.4 ~ ~', bb='vertical', s0=0.4, s1=1.4, life=8, fade=3),
               card('flame', '~-0.4 ~ ~0.2', bb='vertical', s0=0.4, s1=1.2, life=8, fade=3, dly=1),
               card('glow', '~ ~0.05 ~', '~ 90', s0=0.6, s1=2.0, life=6, fade=3, col=PYRO)]
    elif el == 4:
        out = [card('frost', '~0.4 ~0.3 ~', bb='center', s0=0.5, s1=1.4, move=(0, 0.2, 0), life=10, fade=5),
               card('frost', '~-0.4 ~0.3 ~0.2', bb='center', s0=0.5, s1=1.3, move=(0, 0.2, 0), life=10, fade=5, dly=1)]
    else:
        out = [card('arc', '~ ~0.3 ~', bb='center', roll=15, s0=0.5, s1=1.4, life=4, fade=2, col=ELECTRO),
               card('spark', '~ ~0.2 ~', bb='center', spin=45, s0=0.3, s1=1.0, life=4, fade=2, col=ELECTRO_PALE)]
    return out + el_parts(el, '~ ~0.2 ~', 0.5, 4)


@epreset('brand_rune', 'The brand rune over the player\'s chest (call every 4 t at the chest): the element rune card '
         '(Pyro ")火(", Hydro "ccc / |||", Electro square rune, Cryo "大巛"; Geo draws its sigil), life 5 t.')
def _e_brand_rune(el):
    kind = f'rune_{EL_KEYS[el]}' if el <= 4 else 'sigil_geo'
    return [card(kind, '~ ~ ~', bb='center', s0=0.62, s1=0.68, life=5, fade=0),
            dust(EL_FX[el][0], 0.8, '~ ~ ~', (0.25, 0.25, 0.25), 1)]


@epreset('vortex', 'Absorb vortex for {t} ticks around the body: a floor vortex spinning in, a smaller one at the '
         'chest, the element particles drawn inward (v4 A water vortex, v5 A Pyro swirl, v6 A Electro orb, v7 C Cryo).',
         ('t',))
def _e_vortex(el):
    main, pale, deep, dcol = EL_FX[el]
    return [card('vortex', '~ ~0.08 ~', '~ 0', spin=-170, s0=10.0, s1=6.0, life='$(t)', fade=8, col=main),
            card('vortex', '~ ~3 ~', '~ 0', spin=170, s0=3.0, s1=5.0, life='$(t)', fade=8, col=pale),
            card('glow', '~ ~3.2 ~', bb='center', s0=1.0, s1=3.5, life='$(t)', fade=8, col=pale)] + \
        el_parts(el, '~ ~2 ~', 4.0, 16)


@epreset('recolour', 'The recolour wave from the boss outward to {r} (tenths) over {t} ticks (absorb bursts, plan '
         '§2.6): an element ripple and a glow band sweeping the floor.', ('r', 't'))
def _e_recolour(el):
    main, pale, deep, dcol = EL_FX[el]
    return [card('ripple', '~ ~0.09 ~', '~ 0', spin=30, s0=1.0, s1='$(r)', life='$(t_p6)', fade=6, dur='$(t)', col=pale),
            card('ripple', '~ ~0.085 ~', '~ 0', spin=-30, s0=0.5, s1='$(r_90)', life='$(t_p6)', fade=6, dur='$(t)',
                 col=main),
            card('glow', '~ ~0.08 ~', '~ 90', s0=1.0, s1='$(r_60)', life='$(t)', fade=6, dur='$(t)', col=deep)] + \
        el_parts(el, '~ ~0.5 ~', 3.0, 10)


@epreset('sigils', 'Sigil cards around the body for the absorb (火 / 水 / ⚡ / ❄ / Geo emblem): six sigils rising and '
         'turning at 3-6 b (v5 A, v5 §4.2).')
def _e_sigils(el):
    kind = f'sigil_{EL_KEYS[el]}'
    rnd = random.Random(300 + el)
    out = []
    for k, yaw in enumerate(radial(6, 15)):
        x, z = ring_xz(rnd.uniform(3.0, 4.5), yaw)
        out.append(card(kind, p3(x, rnd.uniform(2.5, 5.0), z), bb='center', s0=0.4, s1=1.3, move=(0, 1.2, 0), life=30,
                        fade=8, dly=3 * k))
    return out + [dust(EL_FX[el][1], 1.2, '~ ~4 ~', (3, 1.5, 3), 12)]


@epreset('front', 'The 3-D wave front (N10) moving with tele/wave: 12 band segments (element strip + wall: Geo dust and '
         'slabs, Hydro water wall, Pyro fire wall, Cryo frost, Electro sparks) travel from {r0} to {r1} in {dur} ticks '
         'keeping {w} deep (tenths / ticks). Call it on the tick BEFORE the strike (the fg wave_band rule). At the floor '
         'centre.', ('r0', 'r1', 'w', 'dur'))
def _e_front(el):
    k = 2 * math.sin(math.radians(15)) * 1.18          # chord of a 30-degree segment, 18 % overlap
    kind = f'front_{EL_KEYS[el]}'
    out = []
    for yaw in radial(12, 0):
        out.append(card(kind, '~ ~0.04 ~', f'~{ang(yaw)} 0', s0=('$(r0_' + f'{int(k * 100)})', 1.6, '$(w)'),
                        s1=('$(r1_' + f'{int(k * 100)})', 1.6, '$(w)'), off=(0, 0, '$(r0)'), move=(0, 0, '$(r1)'),
                        life='$(dur_p4)', fade=4, dur='$(dur)'))
    return out


@epreset('dig', 'B3 dig in place: dust mounds and debris with the element (Geo slabs, Hydro water, Pyro embers, Cryo ice '
         'puffs, Electro violet slabs). At the body\'s floor point.')
def _e_dig(el):
    main, pale, deep, dcol = EL_FX[el]
    out = [card('mound', '~1.5 ~ ~1', bb='vertical', s0=1.0, s1=4.0, life=40, fade=12, dur=10),
           card('mound', '~-1.8 ~ ~-0.5', bb='vertical', s0=1.0, s1=3.5, life=40, fade=12, dur=10, dly=4),
           card('mound', '~0.2 ~ ~-2', bb='vertical', s0=1.0, s1=3.0, life=40, fade=12, dur=10, dly=8)]
    if el in (5, 3):
        for k, yaw in enumerate(radial(4, 30)):
            x, z = ring_xz(2.4, yaw)
            out.append(card('slab', p3(x, 0.2, z, '~'), f'~{ang(yaw)} 0', spin=90, s0=0.6, s1=1.4, move=(0, 1.4, 0),
                            life=20, fade=8, dur=10, dly=2 * k, col=WHITE if el == 5 else ELECTRO))
    elif el == 2:
        out += [card('splash', '~1 ~ ~', bb='vertical', s0=1.0, s1=2.8, life=10, fade=5),
                card('splash', '~-1 ~ ~0.5', bb='vertical', s0=1.0, s1=2.5, life=10, fade=5, dly=4)]
    elif el == 1:
        out += [card('flame', '~0.8 ~ ~', bb='vertical', s0=0.6, s1=1.8, life=12, fade=5),
                card('flame', '~-0.9 ~ ~0.4', bb='vertical', s0=0.6, s1=1.6, life=12, fade=5, dly=3),
                card('smoke', '~ ~1.5 ~', bb='center', s0=1.0, s1=3.0, move=(0, 1.0, 0), life=20, fade=10)]
    else:
        out += [card('frost', '~1 ~0.6 ~', bb='center', s0=0.8, s1=2.2, move=(0, 0.6, 0), life=16, fade=8),
                card('frost', '~-1 ~0.6 ~0.5', bb='center', s0=0.8, s1=2.0, move=(0, 0.6, 0), life=16, fade=8, dly=4)]
    return out + [dust(DUST_KHAKI, 2.4, '~ ~0.6 ~', (2.5, 0.4, 2.5), 20), blockp('tuff', '~ ~0.4 ~', (2, 0.3, 2), 0.2, 16)] + \
        el_parts(el, '~ ~0.5 ~', 2.0, 8)


@epreset('flank_blades', 'P6 element blades out-and-up along a flank strip of length {len} (tenths) from the point along '
         'the executor\'s forward axis, leaning to its left (+x, the outer side): Geo gold blades, Hydro water jets, '
         'Pyro flames, Cryo ice spikes, Electro violet crystals.', ('len',))
def _e_flank_blades(el):
    out = []
    rnd = random.Random(400 + el)
    for k in range(6):
        f = (k + 0.5) / 6
        z = f'$(len_{int(f * 100)})'
        x = rnd.uniform(0.6, 2.2)
        if el == 1:
            out.append(card('flame', f'^{num(x, 2)} ^ ^{z}', '~ 0', bb='vertical', s0=0.6, s1=rnd.uniform(2.0, 2.8),
                            life=12, fade=4, dur=3, dly=k // 2))
        elif el == 4:
            out.append(card('ice_spike', f'^{num(x, 2)} ^ ^{z}', '~-90 25', s0=0.5, s1=rnd.uniform(2.2, 3.0), life=14,
                            fade=5, dur=3, dly=k // 2))
        elif el == 2:
            out.append(card('splash', f'^{num(x, 2)} ^ ^{z}', bb='vertical', s0=0.8, s1=rnd.uniform(2.2, 3.0), life=10,
                            fade=4, dly=k // 2))
        else:
            out.append(card('blade', f'^{num(x, 2)} ^0.9 ^{z}', '~-90 30', roll=rnd.randint(-10, 10), s0=0.8,
                            s1=rnd.uniform(2.2, 3.0), life=11, fade=4, dur=3, dly=k // 2,
                            col=GOLD if el == 5 else ELECTRO))
    return out + el_parts(el, '^1.4 ^0.5 ^$(len_50)', 1.6, 8)


@epreset('spike_line', 'P8 spike line along the aim, length {len} (tenths): six element spikes bursting from the floor '
         'one after another (Geo gold blades, Hydro jets, Pyro flames, Cryo ice spikes, Electro crystals).', ('len',))
def _e_spike_line(el):
    out = []
    rnd = random.Random(500 + el)
    for k in range(6):
        z = f'$(len_{int((k + 0.6) / 6 * 100)})'
        x = rnd.uniform(-0.5, 0.5)
        if el == 1:
            c = card('flame', f'^{num(x, 2)} ^ ^{z}', '~ 0', bb='vertical', s0=0.6, s1=2.4, life=12, fade=4, dly=k)
        elif el == 4:
            c = card('ice_spike', f'^{num(x, 2)} ^ ^{z}', f'~{rnd.randint(0, 90)} {rnd.randint(-15, 15)}', s0=0.5,
                     s1=2.6, life=14, fade=5, dur=3, dly=k)
        elif el == 2:
            c = card('splash', f'^{num(x, 2)} ^ ^{z}', bb='vertical', s0=0.8, s1=2.6, life=10, fade=4, dly=k)
        else:
            c = card('blade', f'^{num(x, 2)} ^0.9 ^{z}', f'~{rnd.randint(-20, 20)} {rnd.randint(-15, 15)}', s0=0.8,
                     s1=2.8, life=12, fade=4, dur=3, dly=k, col=GOLD if el == 5 else ELECTRO)
        out.append(c)
    return out + el_parts(el, '^ ^0.5 ^$(len_50)', 1.2, 8)


@epreset('shard_rain', 'Absorb-2 cosmetic shard rain over radius {r} (tenths) for {t} ticks: falling element shards '
         '(Geo gold, Hydro drops, Pyro embers, Cryo icicles, Electro bolts) spread over the window. At the arena centre.',
         ('r', 't'))
def _e_shard_rain(el):
    main, pale, deep, dcol = EL_FX[el]
    rnd = random.Random(600 + el)
    out = []
    for k in range(8):
        x, z = ring_xz(rnd.uniform(0.2, 0.95), rnd.uniform(0, 360))
        pos = f'^$(r_{int(-x * 100)}) ^9 ^$(r_{int(z * 100)})'.replace('_-', '_m')
        dly = f'$(t_{int(100 * k / 8)})'
        if el == 3:
            out.append(card('bolt', pos.replace('^9', '^0'), bb='vertical', s0=(1.4, 9, 1.4), s1=(2.0, 9, 2.0), life=4,
                            fade=2, dly=dly))
        elif el == 4:
            out.append(card('icicle', pos, '~ 0', roll=180, s0=1.4, s1=1.6, move=(0, -8.5, 0), life=8, fade=1, dly=dly,
                            dur=7))
        else:
            out.append(card('blade' if el == 5 else 'mote', pos, bb='vertical', s0=0.8, s1=1.0, move=(0, -8.5, 0), life=8,
                            fade=1, dly=dly, dur=7, col=GOLD if el == 5 else pale))
    return out + el_parts(el, '~ ~5 ~', 6.0, 12)


# --- named presets ------------------------------------------------------------------------------------------------
@preset('geyser', 'P1 Hydro geyser (the chin addon): a water column erupting with spray and a ripple. At the floor '
        'point.')
def _p_geyser():
    return [card('geyser', '~ ~ ~', '~ 0', s0=(2.0, 0.5, 2.0), s1=(3.2, 6.5, 3.2), life=16, fade=6, dur=4),
            card('splash', '~ ~ ~', bb='vertical', s0=1.5, s1=3.6, life=10, fade=4),
            card('ripple', '~ ~0.06 ~', '~ 0', s0=1.0, s1=3.5, life=10, fade=5, col=HYDRO_PALE),
            part('splash', '~ ~3 ~', (1.2, 2, 1.2), 0.3, 40), part('falling_water', '~ ~5 ~', (1.5, 0.5, 1.5), 0, 12),
            part('bubble_pop', '~ ~0.5 ~', (1, 0.3, 1), 0.05, 8)]


@preset('blade_trail', 'Hydro water-blade trail (at the blade prop, every 2 t): a short water streak and spray.')
def _p_blade_trail():
    return [card('streak', '~ ~ ~', '~90 0', s0=(1.0, 1, 1), s1=(1.8, 1, 1), life=4, fade=2, col=HYDRO_PALE),
            part('splash', '~ ~ ~', (0.2, 0.1, 0.2), 0.1, 3)]


@preset('lump_trail', 'Pyro lump trail (at a flying lump, every 2 t): a flame lick and smoke.')
def _p_lump_trail():
    return [card('flame', '~ ~-0.2 ~', bb='vertical', s0=0.4, s1=0.9, life=4, fade=2),
            card('smoke', '~ ~ ~', bb='center', s0=0.3, s1=0.8, move=(0, 0.3, 0), life=7, fade=4),
            part('flame', '~ ~ ~', (0.1, 0.1, 0.1), 0.01, 1)]


@preset('meteor_big', '32 big meteor fall: the molten meteor drops from {h} (tenths) above onto the floor point in 6 t '
        'with a flame trail and a darkening floor glow.', ('h',))
def _p_meteor_big():
    return [card('meteor', '~ ~$(h) ~', bb='vertical', s0=3.0, s1=3.6, move=(0, '$(h_m100)', 0), life=7, dur=6),
            card('streak', '~ ~$(h) ~', bb='vertical', roll=90, s0=(3, 1.5, 1.5), s1=(6, 1.5, 1.5), move=(0, '$(h_m90)', 0),
                 life=7, dur=6, col=EMBER),
            card('glow', '~ ~0.06 ~', '~ 90', s0=1.0, s1=5.0, life=7, fade=1, dur=6, col=PYRO_DEEP),
            part('flame', '~ ~$(h_50) ~', (0.5, '$(h_30)', 0.5), 0.02, 10)]


@preset('meteor_small', '32 small meteor fall from {h} (tenths) in 4 t with a short flame trail.', ('h',))
def _p_meteor_small():
    return [card('meteor', '~ ~$(h) ~', bb='vertical', s0=1.4, s1=1.7, move=(0, '$(h_m100)', 0), life=5, dur=4),
            card('streak', '~ ~$(h) ~', bb='vertical', roll=90, s0=(2, 1, 1), s1=(3.5, 1, 1), move=(0, '$(h_m90)', 0),
                 life=5, dur=4, col=EMBER)]


@preset('fire_dome', '32 meteor impact: a fire dome of radius {r} (tenths) with flame tongues, a flash and a fire ring. '
        'At the floor point.', ('r',))
def _p_fire_dome():
    out = [card('fire_dome', '~ ~ ~', bb='vertical', s0='$(r_80)', s1='$(r_200)', life=10, fade=5, dur=5),
           card('glow', '~ ~1 ~', bb='center', s0=2.0, s1='$(r_150)', life=6, fade=3, col=PYRO_PALE),
           card('ripple', '~ ~0.07 ~', '~ 0', spin=40, s0='$(r_50)', s1='$(r_110)', life=10, fade=4, dur=5, col=PYRO)]
    for yaw in radial(6, 30):
        x, z = ring_xz(0.8, yaw)
        out.append(card('flame', f'^$(r_{int(-x * 100)}) ^ ^$(r_{int(z * 100)})'.replace('_-', '_m'), bb='vertical',
                        s0=0.8, s1=2.6, life=12, fade=5, dly=2))
    return out + [part('flame', '~ ~1 ~', ('$(r_40)', 0.8, '$(r_40)'), 0.08, 30), part('lava', '~ ~0.5 ~', (1, 0.3, 1), 0, 8),
                  part('explosion', '~ ~0.8 ~', (0.3, 0.1, 0.3), 0, 1)]


@preset('frost_burst', 'Cryo frost burst of radius {r} (tenths; Cryo rings, 41 bursts): a ring of ice spikes, frost '
        'mist and a white flash. At the floor point.', ('r',))
def _p_frost_burst():
    out = [card('glow', '~ ~0.8 ~', bb='center', s0=1.5, s1='$(r_120)', life=6, fade=3, col=CRYO_PALE),
           card('ripple', '~ ~0.07 ~', '~ 0', spin=30, s0='$(r_40)', s1='$(r)', life=9, fade=4, dur=4, col=CRYO)]
    # (FIX STATE-14) 6 spikes, life 12: 45's three bursts 6 t apart stay inside the 64-card fx cap
    for k, yaw in enumerate(radial(6, 10)):
        x, z = ring_xz(0.7, yaw)
        out.append(card('ice_spike', f'^$(r_{int(-x * 100)}) ^ ^$(r_{int(z * 100)})'.replace('_-', '_m'),
                        f'~{ang(yaw)} 22', s0=0.7, s1=2.6 + 0.3 * (k % 3), life=12, fade=5, dur=3))
    out += [card('frost', '~ ~0.8 ~', bb='center', s0=1.0, s1='$(r_60)', move=(0, 0.6, 0), life=12, fade=6),
            card('frost', '~0.8 ~0.6 ~-0.6', bb='center', s0=1.0, s1='$(r_50)', move=(0, 0.5, 0), life=12, fade=6, dly=2)]
    return out + [part('snowflake', '~ ~1 ~', ('$(r_40)', 0.8, '$(r_40)'), 0.05, 40),
                  blockp('packed_ice', '~ ~0.5 ~', ('$(r_30)', 0.3, '$(r_30)'), 0.2, 20)]


@preset('ice_wall', 'P7 Cryo ice-wall piece (on the swept arc): four tall ice spikes in a row along the executor\'s '
        'forward axis (the radial line of the piece, 5.0 .. 11.5 b from the tail root when called at 8.25 b), frost. '
        'At the floor point, rotated along the arc.')
def _p_ice_wall():
    # (FIX STATE-14) one call per wall piece (was two, at 6.5 / 10 b): 5 cards, so the four pieces + the eruption fit the cap
    return [card('ice_spike', '^-0.3 ^ ^-2.4', '~0 -12', s0=0.6, s1=3.2, life=20, fade=7, dur=3),
            card('ice_spike', '^0.3 ^ ^-0.8', '~40 8', s0=0.6, s1=3.8, life=20, fade=7, dur=3, dly=1),
            card('ice_spike', '^-0.2 ^ ^0.8', '~80 14', s0=0.6, s1=3.4, life=20, fade=7, dur=3, dly=1),
            card('ice_spike', '^0.3 ^ ^2.4', '~120 -6', s0=0.6, s1=3.0, life=20, fade=7, dur=3, dly=2),
            card('frost', '~ ~0.8 ~', bb='center', s0=1.0, s1=2.6, move=(0, 0.5, 0), life=14, fade=7),
            part('snowflake', '~ ~1.5 ~', (1.2, 1, 1.2), 0.04, 14), blockp('packed_ice', '~ ~0.5 ~', (1, 0.3, 1), 0.2, 10)]


@preset('hail', 'Hail falling in a field of radius {r} (tenths; ambient, call every 5-10 t): three ice pellets, snow.',
        ('r',))
def _p_hail():
    return [card('icicle', '^$(r_40) ^6 ^$(r_m20)', '~ 0', roll=180, s0=0.6, s1=0.6, move=(0, -5.8, 0), life=6, dur=5),
            card('icicle', '^$(r_m30) ^7 ^$(r_35)', '~ 0', roll=180, s0=0.5, s1=0.5, move=(0, -6.8, 0), life=7, dur=6,
                 dly=2),
            card('icicle', '^$(r_m10) ^6.5 ^$(r_m45)', '~ 0', roll=180, s0=0.55, s1=0.55, move=(0, -6.3, 0), life=7, dur=6,
                 dly=3),
            part('snowflake', '~ ~3 ~', ('$(r_50)', 1.5, '$(r_50)'), 0.02, 10)]


@preset('bolt', 'A single Electro sky bolt onto the floor point: the bolt, a flash, a spark and a scorch ripple.')
def _p_bolt():
    return [card('bolt', '~ ~ ~', bb='vertical', s0=(2.0, 12, 2.0), s1=(2.6, 12, 2.6), life=4, fade=2),
            card('glow', '~ ~0.6 ~', bb='center', s0=1.5, s1=4.0, life=5, fade=3, col=ELECTRO_PALE),
            card('ripple', '~ ~0.07 ~', '~ 0', spin=50, s0=0.6, s1=2.6, life=7, fade=3, col=MAGENTA),
            part('electric_spark', '~ ~0.5 ~', (0.6, 0.6, 0.6), 0.4, 14), flash(ELECTRO_PALE, '~ ~1 ~', 0.8)]


@preset('bolt_round', '42 floor-wide crackle over radius {r} (tenths): two waves of six bolts 8 t apart at spread '
        'points. At the arena centre.', ('r',))
def _p_bolt_round():
    rnd = random.Random(42)
    out = []
    for wave in (0, 8):
        for k in range(6):
            x, z = ring_xz(rnd.uniform(0.15, 0.95), rnd.uniform(0, 360))
            out.append(card('bolt', f'^$(r_{int(-x * 100)}) ^ ^$(r_{int(z * 100)})'.replace('_-', '_m'), bb='vertical',
                            s0=(1.6, 10, 1.6), s1=(2.2, 10, 2.2), life=4, fade=2, dly=wave + k % 3))
    return out + [part('electric_spark', '~ ~0.5 ~', ('$(r_60)', 0.4, '$(r_60)'), 0.3, 60),
                  dust(MAGENTA, 1.8, '~ ~0.4 ~', ('$(r_60)', 0.3, '$(r_60)'), 40)]


@preset('shell_dive', '44 shell impact: a violet dome flash, arcs and a crackle ring. At the floor point.')
def _p_shell_dive():
    return [card('glow', '~ ~1 ~', bb='center', s0=1.5, s1=5.0, life=6, fade=3, col=ELECTRO),
            card('ripple', '~ ~0.07 ~', '~ 0', spin=50, s0=1.0, s1=3.2, life=8, fade=4, dur=4, col=ELECTRO_PALE),
            card('arc', '~ ~0.6 ~', bb='center', roll=30, s0=0.8, s1=2.6, life=4, fade=2, col=ELECTRO),
            card('arc', '~ ~0.8 ~', bb='center', roll=120, s0=0.8, s1=2.4, life=4, fade=2, col=MAGENTA, dly=1),
            card('spark', '~ ~0.5 ~', bb='center', spin=60, s0=0.6, s1=2.2, life=5, fade=2, col=ELECTRO_PALE),
            part('electric_spark', '~ ~0.6 ~', (1, 0.5, 1), 0.4, 16), part('witch', '~ ~0.6 ~', (1, 0.5, 1), 0.1, 8)]


@preset('icicle_trail', 'Icicle / lance trail (at the icicle, every 2 t; 41, 43): frost motes and a pale streak.')
def _p_icicle_trail():
    return [card('mote', '~ ~ ~', bb='center', s0=0.3, s1=0.15, life=6, fade=3, col=CRYO_PALE),
            card('frost', '~ ~ ~', bb='center', s0=0.3, s1=0.7, life=6, fade=3),
            part('snowflake', '~ ~ ~', (0.1, 0.1, 0.1), 0.01, 1)]


@preset('ice_sphere', '43 ice-sphere aura (at the sphere prop, every 4-6 t): frost glints and snow around it.')
def _p_ice_sphere():
    return [card('glint', '~0.8 ~0.5 ~', bb='center', spin=90, s0=0.3, s1=0.9, life=6, fade=3, col=CRYO_PALE),
            card('frost', '~-0.6 ~-0.3 ~0.4', bb='center', s0=0.5, s1=1.2, move=(0, -0.3, 0), life=8, fade=4),
            part('snowflake', '~ ~ ~', (1.0, 1.0, 1.0), 0.02, 4)]


@preset('orb_ribbon', '31 orb ribbon (at an orb, every 2 t): a water ribbon streak and a drop.')
def _p_orb_ribbon():
    return [card('streak', '~ ~ ~', bb='center', s0=(1.4, 1.4, 1), s1=(2.2, 1.0, 1), life=5, fade=3, col=rgb('#79E3E5')),
            card('mote', '~ ~-0.2 ~', bb='center', s0=0.35, s1=0.2, move=(0, -0.4, 0), life=5, fade=2, col=HYDRO_PALE),
            part('dripping_water', '~ ~ ~', (0.3, 0.3, 0.3), 0, 1)]


@preset('spark_column', '44 tell: a violet spark column {h} (tenths) tall from the tail tip with crawling arcs. At the '
        'tip, foot of the column.', ('h',))
def _p_spark_column():
    return [card('beam', '~ ~ ~', '~ 0', s0=(0.5, '$(h)', 0.5), s1=(1.4, '$(h)', 1.4), life=30, fade=6, dur=4, col=ELECTRO),
            card('arc', '~ ~$(h_30) ~', bb='center', roll=80, s0=0.6, s1=1.8, life=5, fade=2, col=ELECTRO_PALE),
            card('arc', '~ ~$(h_60) ~', bb='center', roll=100, s0=0.6, s1=1.8, life=5, fade=2, col=MAGENTA, dly=3),
            card('spark', '~ ~$(h) ~', bb='center', spin=60, s0=0.5, s1=2.0, life=8, fade=3, col=ELECTRO_PALE),
            part('electric_spark', '~ ~$(h_50) ~', (0.3, '$(h_30)', 0.3), 0.2, 16)]


@preset('stele_shatter', 'E a seal stele shatters: red-brown chunks flung out, dust and a gold crack flash. At the '
        'stele foot.')
def _p_stele_shatter():
    rnd = random.Random(61)
    out = [card('glow', '~ ~2 ~', bb='center', s0=1.0, s1=3.5, life=5, fade=3, col=GOLD_PALE)]
    for yaw in radial(6, 20):
        out.append(rad('boulder', yaw, rnd.uniform(25, 60), 0.5, rnd.uniform(2.0, 3.2), y=rnd.uniform(1.0, 2.6), s0=0.5,
                       s1=0.7, life=14, fade=4, dur=10, col=rgb('#B07A5A'), roll=rnd.randint(0, 90)))
    return out + [card('dust', '~ ~1 ~', bb='center', s0=1.0, s1=3.0, move=(0, 0.6, 0), life=16, fade=8, col=DUST),
                  card('dust', '~0.6 ~0.5 ~', bb='center', s0=0.8, s1=2.4, move=(0, 0.4, 0), life=16, fade=8, col=DUST_KHAKI),
                  blockp('deepslate_bricks', '~ ~1.5 ~', (0.5, 1.2, 0.5), 0.2, 24), dust(rgb('#CBA340'), 1.4, '~ ~1.5 ~',
                                                                                         (0.4, 1.2, 0.4), 10)]


@preset('prism_shatter', 'E the seal prism shatters (t112): gold glass blades burst outward from the prism, a white flash '
        'and a gold ring. At the prism centre (floor).')
def _p_prism_shatter():
    rnd = random.Random(112)
    out = [card('glow', '~ ~4 ~', bb='center', s0=3.0, s1=12.0, life=6, fade=4, col=WHITE),
           card('ripple', '~ ~0.08 ~', '~ 0', spin=30, s0=4.0, s1=12.0, life=10, fade=5, dur=6, col=GOLD_PALE)]
    for k, yaw in enumerate(radial(12, 9)):
        out.append(rad('blade', yaw, rnd.uniform(-10, 50), 5.0, rnd.uniform(9, 12), y=rnd.uniform(1.0, 7.5), s0=1.2,
                       s1=1.6, life=12, fade=5, dur=10, col=GOLD_WHITE, roll=rnd.randint(-40, 40)))
    return out + [flash(GOLD_WHITE, '~ ~4 ~', 1.0), part('end_rod', '~ ~4 ~', (3, 3, 3), 0.15, 30),
                  blockp('yellow_stained_glass', '~ ~4 ~', (4, 3, 4), 0.3, 40)]


@preset('seal_reform', 'D the seal re-forms around the dying body: gold glass blades converging inward, a gold glow and '
        'rising motes. At the body\'s floor point.')
def _p_seal_reform():
    rnd = random.Random(96)
    out = [card('glow', '~ ~4 ~', bb='center', s0=2.0, s1=8.0, life=24, fade=10, dur=20, col=GOLD)]
    for yaw in radial(8, 0):
        out.append(rad('blade', yaw, rnd.uniform(0, 30), 10.0, 5.5, y=rnd.uniform(2.0, 6.0), s0=1.4, s1=1.2, life=22,
                       fade=6, dur=16, col=GOLD_PALE))
    return out + [part('end_rod', '~ ~4 ~', (4, 3, 4), 0.02, 20), dust(GOLD_PALE, 1.6, '~ ~3 ~', (5, 2, 5), 20)]


@preset('petrify_pulse', 'D petrify pulse (the rig turns to stone): a grey-gold ripple and dust. At the body\'s floor '
        'point.')
def _p_petrify_pulse():
    return [card('ripple', '~ ~0.09 ~', '~ 0', spin=30, s0=3.0, s1=10.0, life=12, fade=6, dur=8, col=rgb('#B8B0A0')),
            card('dust', '~ ~2 ~', bb='center', s0=2.0, s1=5.0, move=(0, 1, 0), life=18, fade=9, col=rgb('#A8A090')),
            card('glow', '~ ~3 ~', bb='center', s0=2.0, s1=6.0, life=6, fade=4, col=GOLD_PALE),
            blockp('stone', '~ ~2 ~', (2, 1.5, 2), 0.1, 20)]


@preset('splash', 'Water step splash (Hydro walk, water-sheet impacts): a small splash and ripple.')
def _p_splash():
    return [card('splash', '~ ~ ~', bb='vertical', s0=0.6, s1=1.6, life=7, fade=3),
            card('ripple', '~ ~0.06 ~', '~ 0', s0=0.4, s1=1.8, life=8, fade=4, col=HYDRO_PALE),
            part('splash', '~ ~0.3 ~', (0.3, 0.1, 0.3), 0.2, 10)]


@preset('splash_wall', 'P5b Hydro splash wall at the ring edge of radius {r} (tenths): ten water walls rising around '
        'the paw point.', ('r',))
def _p_splash_wall():
    out = []
    for yaw in radial(10, 18):
        x, z = ring_xz(1.0, yaw)
        out.append(card('splash', f'^$(r_{int(-x * 100)}) ^ ^$(r_{int(z * 100)})'.replace('_-', '_m'), bb='vertical',
                        s0=1.0, s1=3.2, life=10, fade=5, dur=4))
    return out + [part('splash', '~ ~1 ~', ('$(r_60)', 0.6, '$(r_60)'), 0.3, 40)]


@preset('dust', 'P9 dust puff (rock rings, rush trails): three khaki dust clouds. At the floor point.')
def _p_dust():
    return [card('dust', '~0.6 ~0.5 ~', bb='center', s0=0.8, s1=2.2, move=(0, 0.5, 0), life=14, fade=7, col=DUST_KHAKI),
            card('dust', '~-0.5 ~0.4 ~0.4', bb='center', s0=0.8, s1=2.0, move=(0, 0.4, 0), life=14, fade=7, col=DUST, dly=1),
            card('dust', '~ ~0.6 ~-0.6', bb='center', s0=0.7, s1=1.8, move=(0, 0.5, 0), life=14, fade=7, col=DUST_KHAKI,
                 dly=2),
            dust(DUST_KHAKI, 1.8, '~ ~0.4 ~', (0.8, 0.2, 0.8), 8)]


@preset('rock_rain', 'P9 rock rain: six rocks falling from above within radius {r} (tenths), dust. At the floor point.',
        ('r',))
def _p_rock_rain():
    rnd = random.Random(9)
    out = []
    for k in range(6):
        x, z = ring_xz(rnd.uniform(0.1, 0.9), rnd.uniform(0, 360))
        out.append(card('boulder', f'^$(r_{int(-x * 100)}) ^7 ^$(r_{int(z * 100)})'.replace('_-', '_m'), bb='center',
                        roll=rnd.randint(0, 90), s0=0.6, s1=0.8, move=(0, -6.8, 0), life=8, dur=7, dly=k * 2))
    return out + [fdust('gravel', '~ ~6 ~', ('$(r_50)', 0.5, '$(r_50)'), 12)]


@preset('mound', 'P9 / B3 dust mound plume at the dig / surfacing point.')
def _p_mound():
    return [card('mound', '~ ~ ~', bb='vertical', s0=1.0, s1=4.5, life=24, fade=10, dur=8),
            card('dust', '~ ~1.2 ~', bb='center', s0=1.0, s1=3.0, move=(0, 1.0, 0), life=18, fade=9, col=DUST_KHAKI),
            card('dust', '~0.8 ~0.6 ~0.4', bb='center', s0=0.8, s1=2.2, move=(0, 0.6, 0), life=16, fade=8, col=DUST, dly=2),
            blockp('rooted_dirt', '~ ~0.5 ~', (1, 0.4, 1), 0.2, 16)]


@preset('light_shaft', 'P9 gold light shaft over a rock-ring marker (8 b tall).')
def _p_light_shaft():
    return [card('beam', '~ ~ ~', '~ 0', s0=(0.6, 8, 0.6), s1=(2.2, 8, 2.2), life=20, fade=8, dur=5, col=GOLD_PALE),
            card('glow', '~ ~0.06 ~', '~ 90', s0=1.0, s1=3.4, life=20, fade=8, col=GOLD),
            part('end_rod', '~ ~3 ~', (0.4, 2.5, 0.4), 0.02, 8)]


@preset('gold_plume', 'P4 gold plume (the back flares and the spikes launch): a gold column up, rising glints, dust. At '
        'the back (launch point).')
def _p_gold_plume():
    out = [card('beam', '~ ~ ~', '~ 0', s0=(0.8, 6, 0.8), s1=(2.4, 10, 2.4), life=12, fade=5, dur=4, col=GOLD_PALE),
           card('glow', '~ ~1 ~', bb='center', s0=1.5, s1=4.5, life=6, fade=3, col=GOLD)]
    for k in range(5):
        out.append(card('glint', p3(0.6 * math.cos(k * 1.3), 1.0 + k * 0.6, 0.6 * math.sin(k * 1.3), '~'), bb='center',
                        spin=90, s0=0.3, s1=1.0, move=(0, 2.5, 0), life=12, fade=4, dly=k, col=GOLD_PALE))
    return out + [dust(rgb('#E6D682'), 2.0, '~ ~2 ~', (0.6, 1.5, 0.6), 16), part('end_rod', '~ ~3 ~', (0.3, 2, 0.3), 0.1, 10)]


@preset('shard_fall', 'P4 falling spike shard (the last 4 t before a landing): a dark gold shard dropping from {h} '
        '(tenths) with a glowing streak.', ('h',))
def _p_shard_fall():
    return [card('blade', '~ ~$(h) ~', '~ 0', roll=180, s0=1.6, s1=1.6, move=(0, '$(h_m100)', 0), life=5, dur=4,
                 col=rgb('#8D6C3F')),
            card('streak', '~ ~$(h) ~', bb='vertical', roll=90, s0=(2, 1, 1), s1=(3, 1, 1), move=(0, '$(h_m90)', 0), life=5,
                 dur=4, col=GOLD_PALE)]


@preset('dust_wall', 'P6 dust walls along a strip of length {len} (tenths) from the point along the executor\'s '
        'forward axis: five rising cream-gold walls.', ('len',))
def _p_dust_wall():
    out = []
    for k in range(5):
        z = f'$(len_{int((k + 0.5) / 5 * 100)})'
        out.append(card('t_wall', f'^ ^ ^{z}', '~90 0', s0=(1.5, 0.5, 1), s1=(3.0, 3.0, 1), life=18, fade=8, dur=4, dly=k,
                        col=rgb('#E8D4A8')))
    return out + [dust(DUST, 2.4, '^ ^1 ^$(len_50)', (0.6, 1, '$(len_40)'), 20)]


@preset('boulders', 'P7 boulders thrown up along the swept arc (five rocks fanning out from the point).')
def _p_boulders():
    rnd = random.Random(7)
    return [rad('boulder', yaw, rnd.uniform(35, 65), 0.3, rnd.uniform(2.5, 4.0), y=0.4, s0=0.8, s1=1.2, life=12, fade=4,
                dur=10, roll=rnd.randint(0, 90)) for yaw in (-40, 0, 40)] + \
        [blockp('tuff', '~ ~0.5 ~', (1, 0.3, 1), 0.3, 16)]


@preset('tail_lane', 'P7 / P8 tail lane: dust and grit kicked along the tail\'s path (a streak and puffs along the '
        'executor\'s forward axis, 6 b).')
def _p_tail_lane():
    return [card('streak', '^ ^0.4 ^3', '~90 0', s0=(3, 1.5, 1), s1=(6, 1.5, 1), life=6, fade=3, col=rgb('#C8B48A')),
            card('dust', '^ ^0.5 ^2', bb='center', s0=0.9, s1=2.2, move=(0, 0.4, 0), life=10, fade=5, col=DUST),
            card('dust', '^-0.3 ^0.5 ^5', bb='center', s0=0.9, s1=2.0, move=(0, 0.4, 0), life=10, fade=5, col=DUST_KHAKI,
                 dly=1),
            dust(DUST, 1.8, '^ ^0.4 ^3', (0.4, 0.2, 2.5), 12)]


@preset('leaf_burst', 'P8 orange leaf burst (the tail\'s leaves scatter at the impact): ten leaves flung out and up.')
def _p_leaf_burst():
    rnd = random.Random(8)
    return [rad('leaf', yaw, rnd.uniform(30, 70), 0.3, rnd.uniform(2.0, 3.5), y=0.8, s0=0.5, s1=0.6, life=18, fade=6,
                dur=16, roll=rnd.randint(0, 180)) for yaw in radial(6, 5)] + \
        [part('cherry_leaves', '~ ~1 ~', (1, 0.5, 1), 0.05, 10)]


@preset('cones', 'P8 planted stone cones along the line (five cones from 2 to 12 b, staying 60 t). At the tail root, '
        'rotated as the line.')
def _p_cones():
    rnd = random.Random(88)
    return [card('cone', f'^{num(rnd.uniform(-0.6, 0.6), 2)} ^ ^{num(2 + 2.5 * k, 2)}', bb='vertical', s0=0.5,
                 s1=rnd.uniform(1.6, 2.4), life=60, fade=10, dur=3, dly=k) for k in range(5)]


@preset('skid', 'P3 skid gouge: a crack fan behind the stop point, dust and slabs kicked forward.')
def _p_skid():
    return [card('crackfan', '~ ~0.04 ~', '~180 0', s0=1.0, s1=5.0, life=30, fade=10, dur=4, col=GOLD_PALE),
            card('dust', '^ ^0.6 ^1.5', bb='center', s0=1.0, s1=2.8, move=(0, 0.5, 0), life=16, fade=8, col=DUST),
            card('dust', '^1.2 ^0.5 ^0.5', bb='center', s0=1.0, s1=2.4, move=(0, 0.4, 0), life=16, fade=8, col=DUST_KHAKI),
            card('slab', '^-0.8 ^0.2 ^1.2', '~30 0', spin=70, s0=0.6, s1=1.0, move=(0, 1.0, 0), life=14, fade=6, dur=8),
            blockp('gravel', '~ ~0.4 ~', (1.2, 0.3, 1.2), 0.25, 20)]


@preset('dust_trail', 'P3 gallop dust (ambient, every 4 t of the run at the body): two dust puffs.')
def _p_dust_trail():
    return [card('dust', '~0.8 ~0.5 ~', bb='center', s0=0.8, s1=2.2, move=(0, 0.4, 0), life=12, fade=6, col=DUST),
            card('dust', '~-0.8 ~0.5 ~', bb='center', s0=0.8, s1=2.0, move=(0, 0.4, 0), life=12, fade=6, col=DUST_KHAKI)]


@preset('shock_dome', 'Roar shock dome of radius {r} (tenths): a floor ring and a camera-facing ring expanding (v6 roar '
        'shock domes, v7 C).', ('r',))
def _p_shock_dome():
    return [card('ripple', '~ ~0.1 ~', '~ 0', spin=40, s0=1.0, s1='$(r)', life=10, fade=4, dur=8, col=rgb('#F4F0E8')),
            card('ripple', '~ ~3 ~', '~ 90', spin=40, s0=1.0, s1='$(r_70)', life=10, fade=4, dur=8, col=rgb('#E8E4DC')),
            card('ripple', '~ ~3 ~', '~90 90', spin=-40, s0=1.0, s1='$(r_70)', life=10, fade=4, dur=8, col=rgb('#E8E4DC')),
            part('white_ash', '~ ~2 ~', ('$(r_40)', 1, '$(r_40)'), 0.1, 20)]


@preset('emerge_spikes', 'B3 emergence: an earth-spike cluster of radius {r} (tenths) bursting out of the floor with '
        'dust. At the surfacing point.', ('r',))
def _p_emerge_spikes():
    rnd = random.Random(388)
    out = []
    for k, yaw in enumerate(radial(10, 8)):
        x, z = ring_xz(rnd.uniform(0.2, 0.8), yaw)
        out.append(card('cone', f'^$(r_{int(-x * 100)}) ^ ^$(r_{int(z * 100)})'.replace('_-', '_m'), bb='vertical',
                        s0=0.6, s1=rnd.uniform(3.0, 4.6), life=18, fade=6, dur=3, dly=k % 3, col=rgb('#8C8270')))
    return out + [card('dust', '~ ~1.5 ~', bb='center', s0=1.5, s1='$(r_80)', move=(0, 1.2, 0), life=20, fade=10,
                       col=DUST_KHAKI),
                  card('glow', '~ ~1 ~', bb='center', s0=1.5, s1=5.0, life=6, fade=3, col=GOLD_PALE),
                  blockp('tuff', '~ ~1 ~', ('$(r_40)', 0.6, '$(r_40)'), 0.3, 30)]


@preset('glyph_glow', 'Entrance stele / arrival glyph glow (ambient, every 10 t at a glyph): a soft glow and motes.')
def _p_glyph_glow():
    return [card('glow', '~ ~ ~', bb='center', s0=0.8, s1=1.4, life=10, fade=5, col=GOLD_PALE),
            card('mote', '~0.2 ~0.1 ~', bb='center', s0=0.2, s1=0.1, move=(0, 0.6, 0), life=10, fade=4, col=GOLD),
            part('end_rod', '~ ~ ~', (0.15, 0.2, 0.15), 0.01, 1)]


@preset('gold_leaves', 'E the intro roar (t120): twelve gold leaves flung radially from the head height.')
def _p_gold_leaves():
    rnd = random.Random(120)
    return [rad('gold_leaf', yaw, rnd.uniform(-5, 35), 0.5, rnd.uniform(6, 9), y=rnd.uniform(2.0, 4.0), s0=0.4, s1=0.6,
                life=22, fade=6, dur=20, roll=rnd.randint(0, 180)) for yaw in radial(12, 0)] + \
        [dust(GOLD_PALE, 1.4, '~ ~3 ~', (2, 1, 2), 16)]


@preset('gold_motes', 'Drifting gold motes (arena ambience; ambient, every 20 t at a mote point): three slow motes.')
def _p_gold_motes():
    return [card('mote', '~0.6 ~0.5 ~0.2', bb='center', s0=0.15, s1=0.3, move=(0.3, 1.2, 0), life=40, fade=12, col=GOLD),
            card('mote', '~-0.5 ~1.0 ~-0.4', bb='center', s0=0.15, s1=0.25, move=(-0.2, 1.0, 0.2), life=40, fade=12,
                 col=GOLD_PALE),
            card('mote', '~0.1 ~1.6 ~0.6', bb='center', s0=0.1, s1=0.2, move=(0.1, 0.8, -0.2), life=40, fade=12, col=GOLD)]


@preset('cure', 'The brand cleanse (butterfly-style cure fx, about 16 t): a pale-gold beam down, a white-gold burst and '
        'glints. At the player\'s feet.')
def _p_cure():
    return [card('beam', '~ ~ ~', '~ 0', s0=(0.6, 4.0, 0.6), s1=(1.6, 3.2, 1.6), life=9, fade=3, col=GOLD_PALE),
            card('cure_burst', '~ ~1 ~', bb='center', spin=30, s0=0.6, s1=3.2, life=7, fade=3, dly=4),
            card('glint', '~0.4 ~1.6 ~', bb='center', spin=90, s0=0.3, s1=1.0, life=8, fade=3, dly=6, col=GOLD_WHITE),
            card('glint', '~-0.4 ~1.2 ~', bb='center', spin=-90, s0=0.3, s1=0.9, life=8, fade=3, dly=8, col=GOLD_PALE),
            part('end_rod', '~ ~1 ~', (0.4, 0.6, 0.4), 0.05, 10), part('happy_villager', '~ ~1 ~', (0.5, 0.6, 0.5), 0, 6)]


@preset('fire_field', 'Fire-field ambience (ambient; every 10-20 t at a live fire field of radius {r} tenths): flames, '
        'lava pops and embers over the field (33).', ('r',))
def _p_fire_field():
    return [card('flame', '^$(r_40) ^ ^$(r_m30)', bb='vertical', s0=0.5, s1=1.4, life=10, fade=4),
            part('flame', '~ ~0.3 ~', ('$(r_45)', 0.1, '$(r_45)'), 0.02, 8), part('lava', '~ ~0.2 ~', ('$(r_40)', 0, '$(r_40)'), 0, 2),
            dust(rgb('#EB8029'), 1.4, '~ ~0.5 ~', ('$(r_45)', 0.3, '$(r_45)'), 6)]


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


HEADER = '# Generated by tools/build_mboss_az_fx.py (야타용왕 fx kit) - edit the generator, not this file.\n'
E = FN + 'e/'
SEL = f'@e[type=minecraft:item_display,tag={TAG}'
DEF_A = 'tg:"rlk_ak_c",t2:"rlk_ak_c",tpd:0'          # storage a defaults: two extra tags, teleport_duration


def mac(line):
    """prefix a line holding a macro placeholder with '$'"""
    return '$' + line if '$(' in line and not line.startswith('$') else line


def engine(W):
    W.w('card', [
        '# Spawn one painted card at pos, rotated rot, seen from the executing context.',
        '# {kind, pos:"^x ^y ^z", rot:"~ ~", bb:fixed|center|vertical|horizontal, roll:<deg, about local z>,',
        '#  spin:<deg over the main interpolation, -170..170, about the card normal (y for flat / cross / band / box)>,',
        '#  s0:<start size>, s1:<end size>, move:"dx,dy,dz" (end offset, display frame: +x left, +y up, +z forward),',
        '#  life:<ticks>, fade:<shrink-out ticks>, col:<RGB int tint, 16777215 = the painted colours>}. az_fx_api.md §2.',
        f'# Skipped (no error) while {CAP} fx cards are alive.',
        f'execute if score #akN mb matches {CAP}.. run return 0',
        f'$data modify storage {STO} a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)f,$(s0)f,$(s0)f",s1:"$(s1)f,$(s1)f,$(s1)f",off:"0f,0f,0f",move:"$(move)",col:$(col),col2:-1,'
        f'ax:"0f,0f,1f",{DEF_A}}}',
        f'execute unless data storage {STO} ax.glow run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #akRoll mb $(roll)',
        '$scoreboard players set #akSpin mb $(spin)',
        '$scoreboard players set #akLife mb $(life)',
        '$scoreboard players set #akFade mb $(fade)',
        'scoreboard players set #akDly mb 0',
        'scoreboard players set #akDur mb 0',
        'scoreboard players set #akHit mb -1',
        'scoreboard players set #akTel mb 0',
        f'function {E}make',
    ])
    W.w('cardx', [
        '# card with every option: s0 / s1 as "xf,yf,zf" vectors, off:"xf,yf,zf" (static start translation), move',
        '# (the END translation), dly:<ticks hidden before it shows>, dur:<ticks of the main interpolation, 0 = up to',
        '# the fade>, hit:<ticks after the call when the tint becomes col2, -1 = never>, col2:<RGB int>. Same cap.',
        f'execute if score #akN mb matches {CAP}.. run return 0',
        f'$data modify storage {STO} a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)",s1:"$(s1)",off:"$(off)",move:"$(move)",col:$(col),col2:$(col2),ax:"0f,0f,1f",' + DEF_A + '}',
        f'execute unless data storage {STO} ax.glow run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #akRoll mb $(roll)',
        '$scoreboard players set #akSpin mb $(spin)',
        '$scoreboard players set #akLife mb $(life)',
        '$scoreboard players set #akFade mb $(fade)',
        '$scoreboard players set #akDly mb $(dly)',
        '$scoreboard players set #akDur mb $(dur)',
        '$scoreboard players set #akHit mb $(hit)',
        'scoreboard players set #akTel mb 0',
        f'function {E}make',
    ])
    W.w('e/make', [
        f'# Internal: storage {STO} a (kind pos rot bb s0 s1 off move col col2 ax tg t2 tpd) + #akRoll #akSpin #akLife',
        '# #akFade #akDly #akDur #akHit #akTel (0 fx, 1 attack telegraph, 2 field pool) -> one card. The stage clock is',
        '# gametime + 1: the ager (fx/e/world, a 1t schedule) runs at the END of this server tick with gametime already',
        '# + 1, so counting from it starts the main interpolation in the next server tick and the client animates it',
        '# (the fg kit\'s first-tick fix). Stages: shows at clock + dly, interpolates from clock + dly + 1 over dur ticks,',
        '# recolours at clock + hit, shrinks over the last fade ticks, removed at clock + dly + life.',
        f'execute unless score #akInit mb matches 1 run function {E}init',
        'execute if score #akTel mb matches 0 run scoreboard players add #akN mb 1',
        'execute if score #akTel mb matches 1 run scoreboard players add #akTN mb 1',
        'execute if score #akTel mb matches 2 run scoreboard players add #akFN mb 1',
        'execute if score #akLife mb matches ..1 run scoreboard players set #akLife mb 2',
        'execute if score #akFade mb matches ..-1 run scoreboard players set #akFade mb 0',
        'execute if score #akDly mb matches ..-1 run scoreboard players set #akDly mb 0',
        'scoreboard players operation #akWd mb = #akLife mb',
        'scoreboard players remove #akWd mb 2',
        'scoreboard players operation #akFade mb < #akWd mb',
        'scoreboard players operation #akWd mb = #akLife mb',
        'scoreboard players operation #akWd mb -= #akFade mb',
        'scoreboard players remove #akWd mb 1',
        'execute if score #akDur mb matches 1.. run scoreboard players operation #akWd mb = #akDur mb',
        'execute if score #akWd mb matches ..0 run scoreboard players set #akWd mb 1',
        'execute if score #akSpin mb matches 171.. run scoreboard players set #akSpin mb 170',
        'execute if score #akSpin mb matches ..-171 run scoreboard players set #akSpin mb -170',
        f'execute store result storage {STO} a.rr float 0.017453292 run scoreboard players get #akRoll mb',
        f'execute store result storage {STO} a.sr float 0.017453292 run scoreboard players get #akSpin mb',
        f'execute store result storage {STO} a.d int 1 run scoreboard players get #akWd mb',
        f'execute store result storage {STO} a.f int 1 run scoreboard players get #akFade mb',
        f'execute store result score #akC2 mb run data get storage {STO} a.col2',
        f'data modify storage {STO} a.z set from storage {STO} a.s0',
        f'execute if score #akDly mb matches 1.. run data modify storage {STO} a.z set value "0f,0f,0f"',
        f'function {E}spawn with storage {STO} a',
        f'execute if score #akTel mb matches 1 run tag {SEL}_new] add {TAG}_t',
        f'execute if score #akTel mb matches 2 run tag {SEL}_new] add {TAG}_fp',
        'execute store result score #akNow mb run time query gametime',
        'scoreboard players add #akNow mb 1',
        f'execute as {SEL}_new,limit=1] run function {E}born',
        f'tag {SEL}_new] remove {TAG}_new',
        f'schedule function {E}world 1t replace',
    ])
    W.w('e/cardf', [
        '# Internal (FIX STATE-2): the fast fx card of K.card when every stage number is a constant: the generator did',
        '# e/make\'s clamps and stage arithmetic ({kind pos rot bb s0 s1 z off move col col2 ax rr sr d f life dly h1',
        '# tsh tfd thit}); the same entity, stages and cap as fx/card + e/make.',
        f'execute if score #akN mb matches {CAP}.. run return 0',
        f'execute unless score #akInit mb matches 1 run function {E}init',
        'scoreboard players add #akN mb 1',
        f'$function {E}spawn {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",s0:"$(s0)",s1:"$(s1)",z:"$(z)",off:"$(off)",'
        'move:"$(move)",col:$(col),col2:$(col2),ax:"$(ax)",rr:"$(rr)",sr:"$(sr)",d:$(d),f:$(f),' + DEF_A + '}',
        'execute store result score #akNow mb run time query gametime',
        'scoreboard players add #akNow mb 1',
        f'$execute as {SEL}_new,limit=1] run function {E}bornf {{dly:$(dly),life:$(life),fade:$(f),h1:$(h1),tsh:"$(tsh)",'
        'tfd:"$(tfd)",thit:"$(thit)"}',
        f'tag {SEL}_new] remove {TAG}_new',
        f'schedule function {E}world 1t replace',
    ])
    W.w('e/bornf', [
        '# Internal (macro, as the new fast card): e/born with the constant stage numbers.',
        'scoreboard players operation @s akS = #akNow mb',
        '$scoreboard players add @s akS $(dly)',
        'scoreboard players operation @s akG = @s akS',
        'scoreboard players add @s akG 1',
        'scoreboard players operation @s akD = @s akS',
        '$scoreboard players add @s akD $(life)',
        'scoreboard players operation @s akK = @s akD',
        '$scoreboard players remove @s akK $(fade)',
        'scoreboard players operation @s akH = #akNow mb',
        '# akH = clock + hit: h1 = hit + 1 >= 0 (scoreboard add takes no negative; with hit -1 the hit tag is never set)',
        '$scoreboard players add @s akH $(h1)',
        'scoreboard players remove @s akH 1',
        f'tag @s add {TAG}_go',
        '$tag @s add $(tsh)',
        '$tag @s add $(tfd)',
        '$tag @s add $(thit)',
    ])
    end_tr = ('translation:[$(move)],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(s1)],'
              'right_rotation:{angle:$(sr)f,axis:[$(ax)]}')
    W.w('e/spawn', [
        f'# Internal (macro, storage {STO} a): the item_display; the stage snapshots ride on its item.',
        f'$summon minecraft:item_display $(pos) {{Tags:["{TAG}","{TAG}_new","rlk_room","rlk_mb_aux","$(tg)","$(t2)"],'
        'billboard:"$(bb)",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
        'teleport_duration:$(tpd),interpolation_duration:0,transformation:{translation:[$(off)],'
        'left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(z)],right_rotation:[0f,0f,0f,1f]},'
        f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{NS_TEX}$(kind)",'
        '"minecraft:custom_model_data":{colors:[$(col)]},"minecraft:custom_data":{'
        'akS:{start_interpolation:0,interpolation_duration:0,transformation:{scale:[$(s0)]}},'
        'akG:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'akF:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}},'
        'akC:$(col2)}}}}',
        f'$execute positioned $(pos) rotated $(rot) run tp {SEL}_new,limit=1] ~ ~ ~ ~ ~',
    ])
    W.w('e/born', [
        '# Internal, as the new card: stage clock values (gametime + 1 based) in akS akG akH akK akD.',
        'scoreboard players operation @s akS = #akNow mb',
        'scoreboard players operation @s akS += #akDly mb',
        'scoreboard players operation @s akG = @s akS',
        'scoreboard players add @s akG 1',
        'scoreboard players operation @s akD = @s akS',
        'scoreboard players operation @s akD += #akLife mb',
        'scoreboard players operation @s akK = @s akD',
        'scoreboard players operation @s akK -= #akFade mb',
        'scoreboard players operation @s akH = #akNow mb',
        'scoreboard players operation @s akH += #akHit mb',
        f'tag @s add {TAG}_go',
        f'execute if score #akDly mb matches 1.. run tag @s add {TAG}_sh',
        f'execute if score #akFade mb matches 1.. run tag @s add {TAG}_fd',
        f'execute if score #akHit mb matches 0.. if score #akC2 mb matches 0.. run tag @s add {TAG}_hit',
    ])
    W.w('e/world', [
        '# Ages the kit\'s cards once per tick while any is alive (scheduled from e/make and from itself, so it runs at',
        '# the end of the server tick; no hook in rlk:tick). A dead or reviving player clears them (fields too: the',
        '# module redraws its field table on resume). Safe-circle beams (tele/safe_beam) emit every 2 t.',
        f'execute unless entity {SEL},limit=1] run return run function {E}zero',
        f'execute if entity @a[tag=player,scores={{dead=1}}] run return run function {FN}clear',
        f'execute if entity @a[tag=player,scores={{rnDie=1..}}] run return run function {FN}clear',
        'execute store result score #akNow mb run time query gametime',
        f'execute as {SEL}] run function {E}age',
        f'execute store result score #akN mb if entity {SEL},tag=!{TAG}_t,tag=!{TAG}_fp]',
        f'execute store result score #akTN mb if entity {SEL}_t]',
        f'execute store result score #akFN mb if entity {SEL}_fp]',
        'scoreboard players operation #akPar mb = #akNow mb',
        'scoreboard players operation #akPar mb %= #akK2 mb',
        f'execute if score #akPar mb matches 0 as {SEL}_sb] at @s run function {E}beam',
        f'execute if entity {SEL},limit=1] run schedule function {E}world 1t replace',
    ])
    W.w('e/zero', ['scoreboard players set #akN mb 0', 'scoreboard players set #akTN mb 0', 'scoreboard players set #akFN mb 0'])
    W.w('e/age', [
        '# As one card (the stage clock in #akNow).',
        'execute unless score @s akD = @s akD run return run kill @s',
        'execute if score #akNow mb >= @s akD run return run kill @s',
        f'execute if entity @s[tag={TAG}_sh] if score #akNow mb >= @s akS run function {E}show',
        f'execute if entity @s[tag={TAG}_go] if score #akNow mb >= @s akG run function {E}go',
        f'execute if entity @s[tag={TAG}_hit] if score #akNow mb >= @s akH run function {E}hit',
        f'execute if entity @s[tag={TAG}_fd] if score #akNow mb >= @s akK run function {E}fade',
    ])
    W.w('e/show', ['# a delayed card appears at its start size',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".akS',
                   f'tag @s remove {TAG}_sh'])
    W.w('e/go', ['# start -> end transformation over dur ticks (client interpolation)',
                 'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".akG',
                 f'tag @s remove {TAG}_go'])
    W.w('e/hit', ['# the tint changes (telegraph flash on the hit tick)',
                  'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set from entity @s '
                  'item.components."minecraft:custom_data".akC',
                  f'tag @s remove {TAG}_hit'])
    W.w('e/fade', ['# shrink to nothing over the last fade ticks',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".akF',
                   f'tag @s remove {TAG}_fd'])
    W.w('e/beam', ['# As a safe-circle card with a beam (tele/safe_beam), every 2 t: a green particle column.',
                   dust(rgb('#8CF0A0'), 1.6, '~ ~1.5 ~', (0.12, 1.4, 0.12), 6),
                   part('end_rod', '~ ~1 ~', (0.08, 1.0, 0.08), 0.01, 2),
                   part('happy_villager', '~ ~0.4 ~', (0.6, 0.1, 0.6), 0, 1)])
    W.w('e/init', ['# Objectives of the kit (created on the first card; removed by fx/uninstall).',
                   *[f'scoreboard objectives add {o} dummy' for o in OBJECTIVES],
                   'scoreboard players set #akInit mb 1', 'scoreboard players set #akK2 mb 2',
                   'scoreboard players set #akMinus1 mb -1', 'scoreboard players set #akK10 mb 10',
                   'scoreboard players set #akK15 mb 15', 'scoreboard players set #akK150 mb 150',
                   'scoreboard players set #akK300 mb 300', 'scoreboard players set #akK1000 mb 1000',
                   'scoreboard players set #akN mb 0', 'scoreboard players set #akTN mb 0', 'scoreboard players set #akFN mb 0'])
    W.w('clear', ['# Remove every card of the kit (fx, attack telegraphs, lanes, waves, rims, the field pool). Safe to call',
                  '# any time.',
                  f'kill {SEL}]', f'function {E}zero'])
    W.w('uninstall', ['# Remove the kit\'s cards, the demo anchor, objectives, fake players, storage and schedules (call',
                      '# from the module\'s uninstall hook).',
                      f'kill {SEL}]', 'kill @e[type=minecraft:marker,tag=rlk_ak_demo]',
                      *[f'scoreboard objectives remove {o}' for o in OBJECTIVES],
                      *[f'scoreboard players reset {s} mb' for s in FAKE],
                      *[f'data remove storage {STO} {k}' for k in STORAGE_KEYS],
                      f'schedule clear {E}world', f'schedule clear {FN}hud/e/unflash', f'schedule clear {FN}test/e/tick',
                      f'schedule clear {FN}test/e/mturn'])
    spin_y = ','.join(f'{k}:"0f,1f,0f"' for k, v in KINDS.items() if v[0] in SPIN_Y)
    W.w('e/axes', ['# Spin axis (= the card normal / long axis) of the flat, cross, band, box and prism kinds; face kinds',
                   '# keep z.',
                   f'data modify storage {STO} ax set value {{{spin_y}}}',
                   f'data modify storage {STO} ax.glow set value "0f,0f,1f"',
                   *[f'data modify storage {STO} ax.{k} set value "0f,0f,1f"' for k, v in KINDS.items()
                     if v[0] not in SPIN_Y and k != 'glow']])
    W.w('look', [
        '# Dress @s (an item_display the module owns, e.g. a projectile) as a kit sprite: {kind, col:<RGB int>}. Full',
        '# bright; the caller keeps its own transformation / billboard (az_fx_api.md §6 for the prop recipes).',
        '$data merge entity @s {item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        f'"{NS_TEX}$(kind)","minecraft:custom_model_data":{{colors:[$(col)]}}}}}},brightness:{{sky:15,block:15}}}}',
    ])


FAKE = ('#akInit', '#akN', '#akTN', '#akFN', '#akNow', '#akWd', '#akC2', '#akRoll', '#akSpin', '#akLife', '#akFade',
        '#akDly', '#akDur', '#akHit', '#akTel', '#akPar', '#akK2', '#akMinus1', '#akK10', '#akK15', '#akK150', '#akK300',
        '#akK1000', '#akTr', '#akTr0', '#akTa', '#akTa0', '#akTa1', '#akTl', '#akTw', '#akTb', '#akTd', '#akTell',
        '#akTEl', '#akTnd', '#akThold', '#akTn', '#akTj', '#akTm', '#akTx', '#akTy', '#akTq', '#akTg', '#akTc', '#akTk',
        '#akTs', '#akT30', '#akTlast', '#akTodd', '#akA', '#akB', '#akPe', '#akWl', '#akHudV', '#akDemo', '#akDT',
        '#akMT', '#akWid', *[f'#akWw{k}' for k in range(8)], *[f'#akWh{k}' for k in range(8)],
        *[f'#akA_{k}' for k in ('r', 'r0', 'r1', 'w', 'len', 'h', 't', 'dur')])
STORAGE_KEYS = ('a', 't', 'w', 'pr', 'hud', 'ax', 'dm', 'fd')


def telegraphs(W):
    T = FN + 'tele/e/'
    cols = []
    for el in sorted(TELE_COL):
        c1, c2, c3 = TELE_COL[el]
        cols.append(f'execute if score #akTEl mb matches {el} run data modify storage {STO} t merge value '
                    f'{{c1:{c1},c2:{c2},c3:{c3}}}')
    d1, d2, d3 = TELE_COL[TELE_DEFAULT]
    W.w('tele/e/prep', [
        '# Internal: common telegraph setup from #akTell #akTEl #akTnd #akThold. Colours by el (#elem numbering):',
        '# 0 physical, 1 Pyro, 2 Hydro, 3 Electro, 4 Cryo, 5 Geo; 6-8 and anything else draw Geo. nd >= 1 turns the rim',
        '# the shared undodgeable red-amber and picks the 回 card (nd 2: + the jump chevron). Life = tell + hold + 1, the',
        '# fill grows over tell - 1 ticks from the tick after the call, so its edge reaches the rim on call + tell (the',
        '# framework hz strike tick when both are made in the same tick with the same tell); every card flashes (col2)',
        '# on that tick.',
        'execute if score #akTell mb matches ..1 run scoreboard players set #akTell mb 2',
        'execute if score #akThold mb matches ..-1 run scoreboard players set #akThold mb 0',
        f'data modify storage {STO} t merge value {{c1:{d1},c2:{d2},c3:{d3},tg:"rlk_ak_c",t2:"rlk_ak_c",tpd:0,'
        f'gk:"t_nd",cg:{ND_RIM}}}',
        *cols,
        f'execute if score #akTnd mb matches 1.. run data modify storage {STO} t.c1 set value {ND_RIM}',
        f'execute if score #akTnd mb matches 2.. run data modify storage {STO} t.gk set value "t_ndj"',
        'scoreboard players operation #akLife mb = #akTell mb',
        'scoreboard players operation #akLife mb += #akThold mb',
        'scoreboard players add #akLife mb 1',
        'scoreboard players operation #akDur mb = #akTell mb',
        'scoreboard players remove #akDur mb 1',
        'scoreboard players operation #akHit mb = #akTell mb',
        'scoreboard players set #akFade mb 0',
        'scoreboard players set #akDly mb 0',
        'scoreboard players set #akRoll mb 0',
        'scoreboard players set #akSpin mb 0',
        'scoreboard players set #akTel mb 1',
    ])

    def head(extra, el=True, nd=True):
        return [f'execute if score #akTN mb matches {TCAP - TSKIP}.. run return 0',
                f'execute unless score #akInit mb matches 1 run function {E}init',
                '$scoreboard players set #akTell mb $(tell)',
                '$scoreboard players set #akTEl mb $(el)' if el is True else f'scoreboard players set #akTEl mb {el}',
                '$scoreboard players set #akTnd mb $(nd)' if nd is True else f'scoreboard players set #akTnd mb {nd}',
                '$scoreboard players set #akThold mb $(hold)',
                *extra,
                f'function {T}prep']

    def mk(kind, pos, s0, s1, col, rot='~ 0', off='0f,0f,0f', move=None, flash='$(c3)', tg='$(tg)', t2='$(t2)'):
        """one telegraph card inside a macro reading storage t (static cards have s0 = s1)"""
        mv = move if move is not None else off
        return [f'$data modify storage {STO} a set value {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"fixed",'
                f's0:"{s0}",s1:"{s1}",off:"{off}",move:"{mv}",col:{col},col2:{flash},ax:"0f,1f,0f",'
                f'tg:"{tg}",t2:"{t2}",tpd:$(tpd)}}',
                f'function {E}make']

    def store(key, score, scale):
        return f'execute store result storage {STO} t.{key} float {scale} run scoreboard players get {score} mb'

    def glyph_size(score, pct):
        """t.gs = clamp(score (tenths) * pct %, 1.0 .. 2.2) blocks"""
        return [f'scoreboard players operation #akTg mb = {score} mb',
                f'scoreboard players set #akTc mb {pct}', 'scoreboard players operation #akTg mb *= #akTc mb',
                'scoreboard players set #akTc mb 100', 'scoreboard players operation #akTg mb /= #akTc mb',
                'execute if score #akTg mb matches ..9 run scoreboard players set #akTg mb 10',
                'execute if score #akTg mb matches 23.. run scoreboard players set #akTg mb 22',
                store('gs', '#akTg', 0.1)]
    # the undodgeable 回 card (gk t_nd / t_ndj) at ^ ^0.05 ^$(gz), static, tinted red-amber, flashing on the hit
    W.w('tele/e/glyph', ['# Internal (macro, storage t): the undodgeable card at t.gz along the aim, size t.gs.',
                         *mk('$(gk)', '^ ^0.05 ^$(gz)', '$(gs)f,1f,$(gs)f', '$(gs)f,1f,$(gs)f', '$(cg)',
                             t2='rlk_ak_g')])

    # ---- disc
    W.w('tele/disc', [
        '# Disc telegraph decal: {r:<radius, tenths of a block>, tell:<ticks to the hit>, el:<#elem palette>, nd:<0 / 1',
        '# undodgeable / 2 + jump chevron>, hold:<ticks it stays after the hit>}. Positioned on the floor point. Visual',
        f'# only: pair it with hz/disc (same tell, #hzQuiet 1). 2 cards (+1 with nd); skipped while {TCAP - TSKIP}+',
        '# attack-telegraph cards live.',
        *head(['$scoreboard players set #akTr mb $(r)']),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1),
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #akTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc with storage {STO} t',
        f'data modify storage {STO} t.gz set value 0f', *glyph_size('#akTr', 45),
        f'execute if score #akTnd mb matches 1.. run function {T}glyph with storage {STO} t',
    ])
    W.w('tele/e/disc', [
        '# Internal (macro, storage t): the progress fill (0 -> r) under the static rim.',
        *mk('t_fill', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', '$(c2)'),
        *mk('$(rim)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', '$(c1)'),
    ])
    # outline-only disc (Change note 1 "keep (trim)", requests Rpa-2 / Rpb-1 / Rpl-3): the static rim alone
    W.w('tele/disc_o', [
        '# Outline-only disc telegraph (plan Change note 1 "keep (trim)": no progress fill): the same arguments as',
        '# tele/disc {r, tell, el, nd, hold}; the static rim (+ the undodgeable card with nd) flashes on call + tell.',
        '# 1 card (+1 with nd).',
        *head(['$scoreboard players set #akTr mb $(r)']),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1),
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #akTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc_o with storage {STO} t',
        f'data modify storage {STO} t.gz set value 0f', *glyph_size('#akTr', 45),
        f'execute if score #akTnd mb matches 1.. run function {T}glyph with storage {STO} t',
    ])
    W.w('tele/e/disc_o', [
        '# Internal (macro, storage t): the static rim alone.',
        *mk('$(rim)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', '$(c1)'),
    ])
    # the shaped keep outlines (plan Change note 1 per-hazard rows; FIX FID-4): disc_o with the footage's outline shape
    for style, sprite, what in (('crack', 't_crack', 'P4 spike landings: the gold zig-zag crack ring'),
                                ('chev', 't_chev', 'P9 rock rings: the gold chevron ring'),
                                ('swirl', 't_swirl', 'the P1 Hydro geyser: the water-swirl field outline')):
        W.w(f'tele/{style}_o', [
            f'# Shaped outline-only disc telegraph ({what}; plan Change note 1 keep): tele/disc_o\'s arguments',
            '# {r, tell, el, nd, hold}; the static outline (+ the undodgeable card with nd) flashes on call + tell. 1 card.',
            *head(['$scoreboard players set #akTr mb $(r)']),
            'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
            store('r', '#akTr', 0.1),
            f'data modify storage {STO} t.rim set value "{sprite}"',
            f'function {T}disc_o with storage {STO} t',
            f'data modify storage {STO} t.gz set value 0f', *glyph_size('#akTr', 45),
            f'execute if score #akTnd mb matches 1.. run function {T}glyph with storage {STO} t',
        ])
    # ---- ring
    W.w('tele/ring', [
        '# Ring telegraph decal (safe hole inside r0): {r0, r (tenths), tell, el, nd, hold}. Positioned on the floor',
        '# point. Outer and inner rims and a progress ring travelling from r0 to r. 3 cards (+1 with nd, on the band',
        '# straight ahead).',
        *head(['$scoreboard players set #akTr mb $(r)', '$scoreboard players set #akTr0 mb $(r0)']),
        'execute if score #akTr0 mb matches ..1 run scoreboard players set #akTr0 mb 2',
        'execute if score #akTr mb <= #akTr0 mb run scoreboard players operation #akTr mb = #akTr0 mb',
        'execute if score #akTr mb = #akTr0 mb run scoreboard players add #akTr mb 5',
        store('r', '#akTr', 0.1), store('r0', '#akTr0', 0.1),
        f'function {T}ring with storage {STO} t',
        'scoreboard players operation #akTg mb = #akTr mb', 'scoreboard players operation #akTg mb += #akTr0 mb',
        store('gz', '#akTg', 0.05),
        'scoreboard players operation #akTg mb = #akTr mb', 'scoreboard players operation #akTg mb -= #akTr0 mb',
        *glyph_size('#akTg', 60),
        f'execute if score #akTnd mb matches 1.. run function {T}glyph with storage {STO} t',
    ])
    W.w('tele/e/ring', [
        *mk('t_rim', '~ ~0.035 ~', '$(r0)f,1f,$(r0)f', '$(r)f,1f,$(r)f', '$(c2)'),
        *mk('t_rim', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', '$(c1)'),
        *mk('t_rim', '~ ~0.046 ~', '$(r0)f,1f,$(r0)f', '$(r0)f,1f,$(r0)f', '$(c1)'),
    ])
    # ---- sector: a fan of 15-degree slices (30-degree slices beyond 13 slices), rim variants carry the edges
    W.w('tele/sector', [
        '# Sector (arc) telegraph decal: {r (tenths), a:<half-angle deg>, tell, el, nd, hold}. Positioned on the apex,',
        '# rotated = aim (yaw). The half-angle snaps to 7.5-degree steps and is drawn as a fan of 15-degree slices',
        '# (fill + rim each, the outer slices\' rims carry the radial edges); beyond 97.5 degrees the fan uses 30-degree',
        '# slices and two edge bars. a >= 175 draws a disc. <= 26 cards (+1 with nd).',
        *head(['$scoreboard players set #akTr mb $(r)', '$scoreboard players set #akTa mb $(a)']),
        f'execute if score #akTa mb matches 175.. run return run function {T}sector_disc',
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1),
        '# n15 = round(a / 7.5) slices of 15 degrees (at least 1)',
        'scoreboard players operation #akTn mb = #akTa mb', 'scoreboard players operation #akTn mb *= #akK2 mb',
        'scoreboard players add #akTn mb 7', 'scoreboard players operation #akTn mb /= #akK15 mb',
        'execute if score #akTn mb matches ..0 run scoreboard players set #akTn mb 1',
        '# the left edge of the fan, tenths of a degree: -75 x n15',
        'scoreboard players set #akTx mb -75', 'scoreboard players operation #akTx mb *= #akTn mb',
        'scoreboard players set #akT30 mb 0', 'scoreboard players set #akTodd mb 0',
        'execute if score #akTn mb matches 14.. run scoreboard players set #akT30 mb 1',
        'execute if score #akT30 mb matches 1 run scoreboard players operation #akTodd mb = #akTn mb',
        'execute if score #akT30 mb matches 1 run scoreboard players operation #akTodd mb %= #akK2 mb',
        '# slice count: n15, or n15 / 2 + odd with 30-degree slices',
        'scoreboard players operation #akTc mb = #akTn mb',
        'execute if score #akT30 mb matches 1 run scoreboard players operation #akTc mb /= #akK2 mb',
        'execute if score #akT30 mb matches 1 run scoreboard players operation #akTc mb += #akTodd mb',
        'scoreboard players operation #akTlast mb = #akTc mb', 'scoreboard players remove #akTlast mb 1',
        'scoreboard players set #akTj mb 0',
        f'function {T}sec_loop',
        f'execute if score #akT30 mb matches 1 run function {T}sec_edges_at',
        f'data modify storage {STO} t.gz set from storage {STO} t.rh',
        store('rh', '#akTr', 0.05), f'data modify storage {STO} t.gz set from storage {STO} t.rh',
        *glyph_size('#akTr', 30),
        f'execute if score #akTnd mb matches 1.. run function {T}glyph with storage {STO} t',
    ])
    W.w('tele/e/sector_disc', [
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #akTr mb',
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1),
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #akTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc with storage {STO} t',
        f'data modify storage {STO} t.gz set value 0f', *glyph_size('#akTr', 45),
        f'execute if score #akTnd mb matches 1.. run function {T}glyph with storage {STO} t',
    ])
    W.w('tele/e/sec_loop', [
        '# Internal: one slice of the sector fan (#akTj index, #akTx its left edge in tenths of a degree), then recurse.',
        'scoreboard players set #akTs mb 150',
        'execute if score #akT30 mb matches 1 run scoreboard players set #akTs mb 300',
        'execute if score #akT30 mb matches 1 if score #akTodd mb matches 1 if score #akTj mb matches 0 run '
        'scoreboard players set #akTs mb 150',
        'scoreboard players operation #akTy mb = #akTs mb', 'scoreboard players operation #akTy mb /= #akK2 mb',
        'scoreboard players operation #akTy mb += #akTx mb',
        store('ya', '#akTy', 0.1),
        f'data modify storage {STO} t merge value {{fk:"t_sf15",rk:"t_sa15"}}',
        f'execute if score #akT30 mb matches 0 if score #akTj mb matches 0 run data modify storage {STO} t.rk set value "t_sa15l"',
        f'execute if score #akT30 mb matches 0 if score #akTj mb = #akTlast mb run data modify storage {STO} t.rk set value '
        '"t_sa15r"',
        f'execute if score #akT30 mb matches 0 if score #akTj mb matches 0 if score #akTlast mb matches 0 run data modify '
        f'storage {STO} t.rk set value "t_sa15b"',
        f'execute if score #akTs mb matches 300 run data modify storage {STO} t merge value {{fk:"t_sf30",rk:"t_sa30"}}',
        f'function {T}sec_slice with storage {STO} t',
        'scoreboard players operation #akTx mb += #akTs mb',
        'scoreboard players add #akTj mb 1',
        f'execute if score #akTj mb < #akTc mb run function {T}sec_loop',
    ])
    W.w('tele/e/sec_slice', [
        '# Internal (macro, storage t): one slice: the fill (0 -> r) and its rim, turned ya degrees from the aim.',
        *mk('$(fk)', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', '$(c2)', rot='~$(ya) 0'),
        *mk('$(rk)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', '$(c1)', rot='~$(ya) 0'),
    ])
    W.w('tele/e/sec_edges_at', [
        '# Internal: the two radial edge bars of a fan drawn with 30-degree slices (+-7.5 x n15 degrees).',
        'scoreboard players set #akTy mb 75', 'scoreboard players operation #akTy mb *= #akTn mb',
        store('ea', '#akTy', 0.1), store('eb', '#akTy', -0.1),
        f'function {T}sec_edges with storage {STO} t',
    ])
    W.w('tele/e/sec_edges', [
        *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(r)f', '0.24f,1f,$(r)f', '$(c1)', rot='~$(ea) 0'),
        *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(r)f', '0.24f,1f,$(r)f', '$(c1)', rot='~$(eb) 0'),
    ])
    # ---- wedge
    W.w('tele/wedge', [
        '# Annular-sector telegraph decal (the P7 swept wedges): {r0, r1 (tenths), a0, a1 (degrees relative to the aim,',
        '# + = clockwise from above, a0 < a1, a1 - a0 <= 180), tell, el, nd, hold}. Positioned on the apex (the tail',
        '# root), rotated = the reference yaw. Drawn as m slices of equal span (15-degree slices squeezed to the span,',
        '# 30-degree ones beyond 105 degrees): a fill and an outer-arc rim each, no radial edges (stacked wedges of a',
        '# union join without seams). r0 > 0: two annular band fills per slice (r0 / r1 in 0.0625 .. 0.84, span <= 105).',
        '# The 回 card (nd >= 1) sits at the mid angle and mid radius unless another 回 card is within 3.9 b (so a union',
        '# of wedges carries one every ~4 b). <= 14 cards for r0 = 0 (+1).',
        *head(['$scoreboard players set #akTr mb $(r1)', '$scoreboard players set #akTr0 mb $(r0)',
               '$scoreboard players set #akTa0 mb $(a0)', '$scoreboard players set #akTa1 mb $(a1)']),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        'execute if score #akTr0 mb matches ..-1 run scoreboard players set #akTr0 mb 0',
        'execute if score #akTr0 mb >= #akTr mb run scoreboard players set #akTr0 mb 0',
        '# span (degrees) 1..180',
        'scoreboard players operation #akTa mb = #akTa1 mb', 'scoreboard players operation #akTa mb -= #akTa0 mb',
        'execute if score #akTa mb matches ..0 run scoreboard players set #akTa mb 1',
        'execute if score #akTa mb matches 181.. run scoreboard players set #akTa mb 180',
        '# inner ratio q x 1000 and its band (0 = from the apex)',
        'scoreboard players set #akTq mb 0',
        'execute if score #akTr0 mb matches 1.. run scoreboard players operation #akTq mb = #akTr0 mb',
        'execute if score #akTr0 mb matches 1.. run scoreboard players operation #akTq mb *= #akK1000 mb',
        'execute if score #akTr0 mb matches 1.. run scoreboard players operation #akTq mb /= #akTr mb',
        'execute if score #akTq mb matches ..62 run scoreboard players set #akTq mb 0',
        'execute if score #akTq mb matches 1.. if score #akTa mb matches 106.. run scoreboard players set #akTa mb 105',
        '# slices: m = ceil(span / 15) of 15-degree texture (k = span / 15m), or ceil(span / 30) of 30 beyond 105',
        'scoreboard players set #akT30 mb 0',
        'execute if score #akTa mb matches 106.. run scoreboard players set #akT30 mb 1',
        'scoreboard players operation #akTc mb = #akTa mb',
        'execute if score #akT30 mb matches 0 run scoreboard players add #akTc mb 14',
        'execute if score #akT30 mb matches 0 run scoreboard players operation #akTc mb /= #akK15 mb',
        'execute if score #akT30 mb matches 1 run scoreboard players add #akTc mb 29',
        'execute if score #akT30 mb matches 1 run scoreboard players set #akTs mb 30',
        'execute if score #akT30 mb matches 1 run scoreboard players operation #akTc mb /= #akTs mb',
        '# span in tenths, the slice span (the last slice takes the remainder), the left edge in tenths',
        'scoreboard players operation #akTd mb = #akTa mb', 'scoreboard players operation #akTd mb *= #akK10 mb',
        'scoreboard players operation #akTs mb = #akTd mb', 'scoreboard players operation #akTs mb /= #akTc mb',
        'scoreboard players operation #akTx mb = #akTa0 mb', 'scoreboard players operation #akTx mb *= #akK10 mb',
        'scoreboard players operation #akTlast mb = #akTc mb', 'scoreboard players remove #akTlast mb 1',
        store('r1', '#akTr', 0.1),
        f'data modify storage {STO} t merge value {{fk:"t_sf15",rk:"t_sa15",bo:"t_bo50",bi:"t_bi50"}}',
        f'execute if score #akT30 mb matches 1 run data modify storage {STO} t merge value {{fk:"t_sf30",rk:"t_sa30"}}',
        f'execute if score #akTq mb matches 1..249 run data modify storage {STO} t merge value {{bo:"t_bo25",bi:"t_bi25"}}',
        f'execute if score #akTq mb matches 500..706 run data modify storage {STO} t merge value {{bo:"t_bo71",bi:"t_bi71"}}',
        f'execute if score #akTq mb matches 707.. run data modify storage {STO} t merge value {{bo:"t_bo84",bi:"t_bi84"}}',
        '# the inner band\'s outer radius r0 / rho (tenths x 1000 / rho x 1000)',
        'scoreboard players set #akTg mb 500',
        'execute if score #akTq mb matches 1..249 run scoreboard players set #akTg mb 250',
        'execute if score #akTq mb matches 500..706 run scoreboard players set #akTg mb 707',
        'execute if score #akTq mb matches 707.. run scoreboard players set #akTg mb 841',
        '# r0 / rho in thousandths of a block: r0 (tenths) x 100 x 1000 / rho (thousandths)',
        'scoreboard players operation #akTm mb = #akTr0 mb', 'scoreboard players operation #akTm mb *= #akK1000 mb',
        'scoreboard players set #akTk mb 100', 'scoreboard players operation #akTm mb *= #akTk mb',
        'scoreboard players operation #akTm mb /= #akTg mb',
        'scoreboard players set #akTj mb 0',
        f'function {T}wdg_loop',
        '# the 回 card: mid angle, mid radius, one per ~4 b',
        'scoreboard players operation #akTy mb = #akTa0 mb', 'scoreboard players operation #akTy mb += #akTa1 mb',
        store('gy', '#akTy', 0.5),
        'scoreboard players operation #akTg mb = #akTr mb', 'scoreboard players operation #akTg mb += #akTr0 mb',
        store('gm', '#akTg', 0.05),
        f'data modify storage {STO} t.gz set value 0f',
        'scoreboard players operation #akTg mb = #akTr mb', 'scoreboard players operation #akTg mb -= #akTr0 mb',
        *glyph_size('#akTg', 30),
        f'execute if score #akTnd mb matches 1.. run function {T}wdg_glyph with storage {STO} t',
    ])
    W.w('tele/e/wdg_glyph', [
        '# Internal (macro, storage t): the 回 card of a wedge unless one is within 3.9 b.',
        f'$execute rotated ~$(gy) 0 positioned ^ ^ ^$(gm) unless entity {SEL}_g,distance=..3.9] run function {T}glyph '
        f'with storage {STO} t',
    ])
    W.w('tele/e/wdg_loop', [
        '# Internal: one wedge slice (#akTj index, #akTx left edge and #akTs span in tenths of a degree), then recurse.',
        'scoreboard players operation #akTw mb = #akTs mb',
        'execute if score #akTj mb = #akTlast mb run scoreboard players operation #akTw mb = #akTd mb',
        'execute if score #akTj mb = #akTlast mb run scoreboard players operation #akTb mb = #akTs mb',
        'execute if score #akTj mb = #akTlast mb run scoreboard players operation #akTb mb *= #akTlast mb',
        'execute if score #akTj mb = #akTlast mb run scoreboard players operation #akTw mb -= #akTb mb',
        'scoreboard players operation #akTy mb = #akTw mb', 'scoreboard players operation #akTy mb /= #akK2 mb',
        'scoreboard players operation #akTy mb += #akTx mb',
        store('ya', '#akTy', 0.1),
        '# lateral scale k x r1 in hundredths of a block = span x r1 x 10 / 150 (or / 300), rounded',
        'scoreboard players operation #akTb mb = #akTw mb', 'scoreboard players operation #akTb mb *= #akTr mb',
        'scoreboard players operation #akTb mb *= #akK10 mb',
        'execute if score #akT30 mb matches 0 run scoreboard players add #akTb mb 75',
        'execute if score #akT30 mb matches 0 run scoreboard players operation #akTb mb /= #akK150 mb',
        'execute if score #akT30 mb matches 1 run scoreboard players add #akTb mb 150',
        'execute if score #akT30 mb matches 1 run scoreboard players operation #akTb mb /= #akK300 mb',
        'execute if score #akTb mb matches ..0 run scoreboard players set #akTb mb 1',
        store('xr', '#akTb', 0.01),
        '# the inner band: lateral k x r0 / rho (#akTm = r0 / rho in thousandths of a block)',
        'scoreboard players operation #akTb mb = #akTw mb', 'scoreboard players operation #akTb mb *= #akTm mb',
        'scoreboard players add #akTb mb 75', 'scoreboard players operation #akTb mb /= #akK150 mb',
        'execute if score #akTb mb matches ..0 run scoreboard players set #akTb mb 1',
        store('xi', '#akTb', 0.001), store('ri', '#akTm', 0.001),
        f'execute if score #akTq mb matches 0 run function {T}wdg_slice with storage {STO} t',
        f'execute if score #akTq mb matches 1.. run function {T}wdg_band with storage {STO} t',
        'scoreboard players operation #akTx mb += #akTs mb',
        'scoreboard players add #akTj mb 1',
        f'execute if score #akTj mb < #akTc mb run function {T}wdg_loop',
    ])
    W.w('tele/e/wdg_slice', [
        '# Internal (macro, storage t): a wedge slice from the apex (fill + outer arc), squeezed to the span.',
        *mk('$(fk)', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(xr)f,1f,$(r1)f', '$(c2)', rot='~$(ya) 0'),
        *mk('$(rk)', '~ ~0.045 ~', '$(xr)f,1f,$(r1)f', '$(xr)f,1f,$(r1)f', '$(c1)', rot='~$(ya) 0'),
    ])
    W.w('tele/e/wdg_band', [
        '# Internal (macro, storage t): an annular wedge slice: the outer band (rho r1 .. r1, with the leading edge), the',
        '# inner band (r0 .. r0 / rho) and the outer arc; both bands grow from the apex, so their union is r0 .. r1.',
        *mk('$(bo)', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(xr)f,1f,$(r1)f', '$(c2)', rot='~$(ya) 0'),
        *mk('$(bi)', '~ ~0.034 ~', '0.02f,1f,0.02f', '$(xi)f,1f,$(ri)f', '$(c2)', rot='~$(ya) 0'),
        *mk('$(rk)', '~ ~0.045 ~', '$(xr)f,1f,$(r1)f', '$(xr)f,1f,$(r1)f', '$(c1)', rot='~$(ya) 0'),
    ])

    # ---- line / lane_side / mline (shared arithmetic)
    def line_math():
        return [
            'execute if score #akTl mb matches ..1 run scoreboard players set #akTl mb 2',
            'execute if score #akTw mb matches ..1 run scoreboard players set #akTw mb 2',
            '# a negative back starts the lane beyond the pivot (hz/line with a negative #hzBack); keep 0.2 b of length',
            'scoreboard players operation #akTd mb = #akTl mb',
            'scoreboard players remove #akTd mb 2',
            'scoreboard players operation #akTd mb *= #akMinus1 mb',
            'scoreboard players operation #akTb mb > #akTd mb',
            store('len', '#akTl', 0.1), store('w', '#akTw', 0.1), store('hw', '#akTw', 0.05), store('nhw', '#akTw', -0.05),
            store('nb', '#akTb', -0.1),
            'scoreboard players operation #akTl mb += #akTb mb',
            store('lb', '#akTl', 0.1),
        ]
    lhead = ['$scoreboard players set #akTl mb $(len)', '$scoreboard players set #akTw mb $(w)',
             '$scoreboard players set #akTb mb $(back)']

    def nd_cards(fn):
        """the 回 cards every ~4 b along a lane: n = round(L / 4) (1..8) at -back + (k + 0.5) L / n"""
        return ['# the undodgeable cards every ~4 b along the lane (#akTl = the drawn length now)',
                *glyph_size('#akTw', 60),
                'scoreboard players operation #akTn mb = #akTl mb', 'scoreboard players add #akTn mb 20',
                'scoreboard players set #akTc mb 40', 'scoreboard players operation #akTn mb /= #akTc mb',
                'execute if score #akTn mb matches ..0 run scoreboard players set #akTn mb 1',
                'execute if score #akTn mb matches 9.. run scoreboard players set #akTn mb 8',
                'scoreboard players set #akTj mb 0',
                f'execute if score #akTnd mb matches 1.. run function {T}{fn}']

    def nd_loop(name, call):
        W.w(f'tele/e/{name}', [
            '# Internal: the k-th undodgeable card along the lane, at -back + (2k + 1) L / 2n (tenths), then recurse.',
            'scoreboard players operation #akTx mb = #akTj mb', 'scoreboard players operation #akTx mb *= #akK2 mb',
            'scoreboard players add #akTx mb 1', 'scoreboard players operation #akTx mb *= #akTl mb',
            'scoreboard players operation #akTy mb = #akTn mb', 'scoreboard players operation #akTy mb *= #akK2 mb',
            'scoreboard players operation #akTx mb /= #akTy mb', 'scoreboard players operation #akTx mb -= #akTb mb',
            store('gz', '#akTx', 0.1),
            f'function {T}{call} with storage {STO} t',
            'scoreboard players add #akTj mb 1',
            f'execute if score #akTj mb < #akTn mb run function {T}{name}'])
    W.w('tele/line', [
        '# Line / lane telegraph decal: {len, w, back (tenths), tell, el, nd, hold}. Positioned on the start point',
        '# (floor), rotated = aim (yaw); covers -back..len along the aim, w wide (as hz/line + #hzBack; a negative back',
        '# starts it beyond the point). Two rails, two caps and the fill growing toward the far end (its bright edge',
        '# reaches it on the hit). 5 cards (+ one 回 card every ~4 b with nd).',
        *head(lhead), *line_math(),
        f'function {T}line with storage {STO} t',
        *nd_cards('ndl_loop'),
    ])
    nd_loop('ndl_loop', 'glyph')
    W.w('tele/e/line', [
        *mk('t_lane', '^ ^0.035 ^$(nb)', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', '$(c2)'),
        *mk('t_bar', '^$(hw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', '$(c1)'),
        *mk('t_bar', '^$(nhw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', '$(c1)'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(nb)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', '$(c1)', rot='~90 0'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(len)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', '$(c1)', rot='~90 0'),
    ])
    W.w('tele/lane_side', [
        '# Flank strip (성동격서 P6): {len, w, back (tenths), tell, el, hold}: a line decal with the undodgeable look',
        '# (always nd 1) and a standing dust wall on the OUTER rail = the executor\'s left (+x): run the left flank\'s',
        '# strip rotated as the body axis, the right flank\'s rotated 180 degrees from its front end. 5 cards + the',
        '# 回 cards (one every ~4 b).',
        *head(lhead, nd=1), *line_math(),
        f'function {T}lane_side with storage {STO} t',
        *nd_cards('ndl_loop'),
    ])
    W.w('tele/e/lane_side', [
        *mk('t_lane', '^ ^0.035 ^$(nb)', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', '$(c2)'),
        *mk('t_bar', '^$(nhw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', '$(c1)'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(nb)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', '$(c1)', rot='~90 0'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(len)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', '$(c1)', rot='~90 0'),
        '# the dust wall standing on the outer rail (a face card turned 90 degrees, its width along the lane)',
        *mk('t_wall', '^$(hw) ^0.02 ^$(nb)', '0.02f,0.6f,1f', '$(lb)f,0.9f,1f', '$(c3)', rot='~90 0',
            off='0f,0f,0f', move='0f,0f,0f'),
    ])
    W.w('tele/mline', [
        '# Moving line (P3 charge lane following the player until the lock): {id:<0-7>, len, w, back (tenths), tell,',
        '# el, nd, hold}. Like tele/line, but every card sits on the pivot (the executing point) with its offset in its',
        '# own transformation, and carries teleport_duration 1 and the tag rlk_ak_ml<id>: tele/mline_aim (run rotated',
        '# as the new aim) or tele/mline_turn {id, d} turns the whole lane about the pivot, smoothly. The fill reaches',
        '# the far end on call + tell; the lane then stays `hold` ticks in the flash colour, or until tele/mline_end.',
        '# 5 cards (+ the 回 cards with nd, riding with the lane).',
        *head(lhead), *line_math(),
        f'$data modify storage {STO} t merge value {{tg:"rlk_ak_ml$(id)",tpd:1}}',
        f'function {T}mline with storage {STO} t',
        *nd_cards('ndm_loop'),
        f'data modify storage {STO} t merge value {{tg:"rlk_ak_c",tpd:0}}',
    ])
    nd_loop('ndm_loop', 'mglyph')
    W.w('tele/e/mglyph', ['# Internal (macro, storage t): a 回 card riding a moving lane (on the pivot, offset gz).',
                          *mk('$(gk)', '~ ~0.05 ~', '$(gs)f,1f,$(gs)f', '$(gs)f,1f,$(gs)f', '$(cg)',
                              off='0f,0f,$(gz)f', t2='rlk_ak_g')])
    W.w('tele/e/mline', [
        *mk('t_lane', '~ ~0.035 ~', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', '$(c2)', off='0f,0f,$(nb)f'),
        *mk('t_bar', '~ ~0.045 ~', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', '$(c1)', off='$(hw)f,0f,$(nb)f'),
        *mk('t_bar', '~ ~0.045 ~', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', '$(c1)', off='$(nhw)f,0f,$(nb)f'),
        '# the caps are turned 90 degrees right (in their frame +x = the lane forward, +z = the lane right) and tagged',
        '# rlk_ak_ml<id>c, so mline_aim keeps that turn',
        *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', '$(c1)', rot='~90 0', off='$(nb)f,0f,$(nhw)f',
            tg='$(tg)c'),
        *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', '$(c1)', rot='~90 0', off='$(len)f,0f,$(nhw)f',
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
        '# Remove moving line {id} now (the lane locks or the pattern is cancelled).',
        f'$kill {SEL}_ml$(id)]',
        f'$kill {SEL}_ml$(id)c]',
        f'execute store result score #akTN mb if entity {SEL}_t]',
    ])

    # ---- the expanding front with ids
    W.w('tele/wave', [
        '# Expanding front (N10): {id:<0-7>, r0, r1, w (tenths), tell, dur (ticks), el, nd, hold}. At the floor centre.',
        '# Over the tell a disc decal fills to r0 (the front\'s start radius) and flashes on the strike tick; from the',
        '# strike the front ring travels r0 -> r1 in dur ticks with the band edge w behind it, then stays `hold` ticks',
        '# (tele/wave_to retargets it: eased fronts as linear segments; tele/wave_end removes it; calling an id again',
        '# replaces it). The rings start interpolating at the end of the strike tick, so the drawn front equals the',
        '# hazard front r0 + spd x (T - strike) each tick. nd >= 1: red-amber rings and four 回 cards riding the front',
        '# (nd 2: chevrons pointing outward = jump it). 4 cards (8 with nd).',
        *head(['$scoreboard players set #akTr0 mb $(r0)', '$scoreboard players set #akTr mb $(r1)',
               '$scoreboard players set #akTw mb $(w)', '$scoreboard players set #akTd mb $(dur)',
               '$scoreboard players set #akWid mb $(id)', f'$kill {SEL}_wv$(id)]']),
        'execute if score #akTr0 mb matches ..4 run scoreboard players set #akTr0 mb 5',
        'execute if score #akTr mb <= #akTr0 mb run scoreboard players operation #akTr mb = #akTr0 mb',
        'execute if score #akTr mb = #akTr0 mb run scoreboard players add #akTr mb 5',
        'execute if score #akTw mb matches ..1 run scoreboard players set #akTw mb 2',
        'execute if score #akTd mb matches ..0 run scoreboard players set #akTd mb 1',
        '$scoreboard players operation #akWw$(id) mb = #akTw mb',
        '$scoreboard players operation #akWh$(id) mb = #akThold mb',
        store('r0', '#akTr0', 0.1), store('r1', '#akTr', 0.1),
        'scoreboard players operation #akTb mb = #akTr mb', 'scoreboard players operation #akTb mb -= #akTw mb',
        store('ri1', '#akTb', 0.1),
        'scoreboard players operation #akTb mb = #akTr0 mb', 'scoreboard players operation #akTb mb -= #akTw mb',
        'execute if score #akTb mb matches ..0 run scoreboard players set #akTb mb 1',
        store('ri0', '#akTb', 0.1),
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #akTr0 mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'$data modify storage {STO} t.tg set value "rlk_ak_wv$(id)"',
        f'function {T}wave with storage {STO} t',
        *glyph_size('#akTw', 60),
        f'execute if score #akTnd mb matches 1.. run function {T}wave_g with storage {STO} t',
        f'data modify storage {STO} t.tg set value "rlk_ak_c"',
    ])
    W.w('tele/e/wave', [
        '# Internal (macro, storage t). 1-2: the start disc (fill reaches r0 on the strike, stays 1 tick).',
        'scoreboard players operation #akLife mb = #akTell mb',
        'scoreboard players add #akLife mb 2',
        *mk('t_fill', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(r0)f,1f,$(r0)f', '$(c2)'),
        *mk('$(rim)', '~ ~0.045 ~', '$(r0)f,1f,$(r0)f', '$(r0)f,1f,$(r0)f', '$(c1)'),
        '# 3-4: the travelling rings: shown on the tick before the strike, moving from its end over dur ticks.',
        'scoreboard players operation #akDly mb = #akTell mb',
        'scoreboard players remove #akDly mb 1',
        'scoreboard players operation #akDur mb = #akTd mb',
        'scoreboard players operation #akLife mb = #akTd mb',
        'scoreboard players operation #akLife mb += #akThold mb',
        'scoreboard players add #akLife mb 1',
        'scoreboard players set #akHit mb -1',
        *mk('t_ring', '~ ~0.05 ~', '$(r0)f,1f,$(r0)f', '$(r1)f,1f,$(r1)f', '$(c1)', flash='-1', t2='rlk_ak_wf'),
        *mk('t_ring', '~ ~0.048 ~', '$(ri0)f,1f,$(ri0)f', '$(ri1)f,1f,$(ri1)f', '$(c2)', flash='-1', t2='rlk_ak_wi'),
    ])
    W.w('tele/e/wave_g', [
        '# Internal (macro, storage t): four 回 cards riding the front (same timing as the rings).',
        *[ln for yaw in (45, 135, 225, 315) for ln in
          mk('$(gk)', '~ ~0.052 ~', '$(gs)f,1f,$(gs)f', '$(gs)f,1f,$(gs)f', '$(cg)', rot=f'~{yaw} 0',
             off='0f,0f,$(r0)f', move='0f,0f,$(r1)f', flash='-1', t2='rlk_ak_wg')],
    ])
    W.w('tele/wave_to', [
        '# Retarget live front {id} to radius {r} (tenths) over {dur} ticks from now (the next linear segment of an eased',
        '# front, N10): the front ring, the band edge (r - w) and the riding 回 cards; the front then stays its hold.',
        '# Call it after the strike (the segment boundaries of the hazard\'s per-tick resize).',
        f'execute unless score #akInit mb matches 1 run function {E}init',
        '$scoreboard players set #akTr mb $(r)', '$scoreboard players set #akTd mb $(dur)',
        'execute if score #akTr mb matches ..4 run scoreboard players set #akTr mb 5',
        'execute if score #akTd mb matches ..0 run scoreboard players set #akTd mb 1',
        '$scoreboard players operation #akTb mb = #akWw$(id) mb',
        'scoreboard players operation #akTb mb *= #akMinus1 mb', 'scoreboard players operation #akTb mb += #akTr mb',
        'execute if score #akTb mb matches ..0 run scoreboard players set #akTb mb 1',
        f'execute store result storage {STO} w.r float 0.1 run scoreboard players get #akTr mb',
        f'execute store result storage {STO} w.ri float 0.1 run scoreboard players get #akTb mb',
        f'execute store result storage {STO} w.d int 1 run scoreboard players get #akTd mb',
        '$data modify storage ' + STO + ' w.id set value $(id)',
        '# the new end of life: now + dur + hold + 1',
        'execute store result score #akWl mb run time query gametime',
        'scoreboard players add #akWl mb 2', 'scoreboard players operation #akWl mb += #akTd mb',
        '$scoreboard players operation #akWl mb += #akWh$(id) mb',
        f'function {T}wave_to with storage {STO} w',
    ])
    W.w('tele/e/wave_to', [
        '# Internal (macro, storage w): merge the new targets (the client interpolates from where the ring is now).',
        f'$execute as {SEL}_wv$(id),tag=rlk_ak_wf] run data merge entity @s {{start_interpolation:0,'
        'interpolation_duration:$(d),transformation:{scale:[$(r)f,1f,$(r)f]}}',
        f'$execute as {SEL}_wv$(id),tag=rlk_ak_wi] run data merge entity @s {{start_interpolation:0,'
        'interpolation_duration:$(d),transformation:{scale:[$(ri)f,1f,$(ri)f]}}',
        f'$execute as {SEL}_wv$(id),tag=rlk_ak_wg] run data merge entity @s {{start_interpolation:0,'
        'interpolation_duration:$(d),transformation:{translation:[0f,0f,$(r)f]}}',
        f'$execute as {SEL}_wv$(id),tag=!rlk_ak_c] run function {T}wave_life',
    ])
    W.w('tele/e/wave_life', ['# Internal, as a front card: the pending main interpolation is superseded; life to #akWl.',
                             f'tag @s remove {TAG}_go', 'scoreboard players operation @s akD = #akWl mb'])
    W.w('tele/wave_end', [
        '# Remove front {id} now (a cancelled pattern; the front reached its end).',
        f'$kill {SEL}_wv$(id)]',
        f'execute store result score #akTN mb if entity {SEL}_t]',
    ])

    # ---- seals and stars: fill + rim + the seal art
    for name, kind, doc in (('heptagram', 't_hept', '서리 습격 (41): the {7/2} heptagram with meander tips and the 大巛 rune'),
                            ('hexagram', 't_hex', '번개 가시 (46): the hexagram with the 번개 rune'),
                            ('starseal', 't_star', '얼음 가시 (45): the white star seal with the ❄ rune'),
                            ('seal8', 't_seal8', '운석 (32): two overlapping squares with the 火 runes')):
        W.w(f'tele/{name}', [
            f'# {doc}: {{r (tenths; the circumradius = the disc radius of its hazard), tell, el, hold}}. At the floor',
            '# centre. The seal art pops in at r, the progress fill grows 0 -> r over the tell, a rim marks the hit radius;',
            '# all flash on the hit. 3 cards.',
            *head(['$scoreboard players set #akTr mb $(r)'], nd=0),
            'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
            store('r', '#akTr', 0.1), store('r9', '#akTr', 0.085),
            f'data modify storage {STO} t.art set value "{kind}"',
            f'function {T}seal with storage {STO} t',
        ])
        W.w(f'tele/{name}_o', [
            f'# {doc}, outline only (plan Change note 1 "keep (trim)": the seal lines + rune, no progress fill): the',
            f'# same arguments as tele/{name} {{r, tell, el, hold}}. The art pops in at r, the rim marks the hit radius;',
            '# both flash on the hit. 2 cards.',
            *head(['$scoreboard players set #akTr mb $(r)'], nd=0),
            'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
            store('r', '#akTr', 0.1), store('r9', '#akTr', 0.085),
            f'data modify storage {STO} t.art set value "{kind}"',
            f'function {T}seal_o with storage {STO} t',
        ])
    W.w('tele/e/seal', [
        '# Internal (macro, storage t): the seal art (pops 0.85 r -> r over 4 t), the fill and the rim.',
        'scoreboard players set #akDur mb 4',
        *mk('$(art)', '~ ~0.04 ~', '$(r9)f,1f,$(r9)f', '$(r)f,1f,$(r)f', '$(c3)', flash='16777215'),
        'scoreboard players operation #akDur mb = #akTell mb', 'scoreboard players remove #akDur mb 1',
        *mk('t_fill', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', '$(c2)'),
        *mk('t_rim', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', '$(c1)'),
    ])
    W.w('tele/e/seal_o', [
        '# Internal (macro, storage t): the seal art (pops 0.85 r -> r over 4 t) and the rim, no fill.',
        'scoreboard players set #akDur mb 4',
        *mk('$(art)', '~ ~0.04 ~', '$(r9)f,1f,$(r9)f', '$(r)f,1f,$(r)f', '$(c3)', flash='16777215'),
        'scoreboard players operation #akDur mb = #akTell mb', 'scoreboard players remove #akDur mb 1',
        *mk('t_rim', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', '$(c1)'),
    ])
    # ---- 42: mask wash and safe circles
    W.w('tele/mask_wash', [
        '# 벼락 습격 (42) strike area: {r (tenths), tell, hold}: ONE floor-wide violet card at the arena centre growing',
        '# 0.3 r -> r over the tell (the "purple light"; the strike is everywhere outside the safe circles) and',
        '# flashing on the strike. 1 card.',
        *head(['$scoreboard players set #akTr mb $(r)'], el=3, nd=0),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1), store('r3', '#akTr', 0.03),
        f'function {T}mask with storage {STO} t',
    ])
    W.w('tele/e/mask', [*mk('t_mask', '~ ~0.03 ~', '$(r3)f,1f,$(r3)f', '$(r)f,1f,$(r)f', '$(c2)')])
    W.w('tele/safe_rim', [
        '# 벼락 습격 safe circle {id:<0-5>, r (tenths; the safe radius R0), tell, hold}: one green ring with the safe',
        '# glyph at its centre (calling an id again replaces it). Tagged rlk_ak_sr<id>; tele/safe_beam {id} adds its',
        '# particle column, tele/safe_end {id} removes it. 1 card (a round of 5 circles + the wash = 6 cards).',
        *head(['$scoreboard players set #akTr mb $(r)', f'$kill {SEL}_sr$(id)]'], el=5, nd=0),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1),
        f'$data modify storage {STO} t.tg set value "rlk_ak_sr$(id)"',
        f'function {T}safe with storage {STO} t',
        f'data modify storage {STO} t.tg set value "rlk_ak_c"',
    ])
    W.w('tele/e/safe', [*mk('t_safe', '~ ~0.05 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', str(SAFE_RIM), flash=str(SAFE_FLASH))])
    W.w('tele/safe_beam', ['# The particle column on safe circle {id} (lives with the circle; emitted by the ager every 2 t).',
                           f'$tag {SEL}_sr$(id)] add {TAG}_sb'])
    W.w('tele/safe_end', ['# Remove safe circle {id} now.', f'$kill {SEL}_sr$(id)]',
                          f'execute store result score #akTN mb if entity {SEL}_t]'])
    # ---- crater, halo
    W.w('tele/crater', [
        '# B3 crater at the floor cut: {r (tenths), tell, hold}: the rubble crater grows 0.4 r -> r over the tell, a',
        '# dark Geo rim at r. At the arena centre. 2 cards.',
        *head(['$scoreboard players set #akTr mb $(r)'], el=5, nd=0),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1), store('r4', '#akTr', 0.04),
        f'function {T}crater with storage {STO} t',
    ])
    W.w('tele/e/crater', [*mk('t_crater', '~ ~0.03 ~', '$(r4)f,1f,$(r4)f', '$(r)f,1f,$(r)f', '16777215', flash='-1'),
                          *mk('t_rim', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', str(rgb('#6B4A20')), flash='-1')])
    W.w('tele/halo', [
        '# Air ring over a landing spot (32 small meteors): {r (tenths), h (tenths above the floor point), tell, el,',
        '# hold}: a thin ring h up shrinking 2 r -> r over the tell and flashing on the impact. 1 card.',
        *head(['$scoreboard players set #akTr mb $(r)', '$scoreboard players set #akTy mb $(h)'], nd=0),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1), store('r2', '#akTr', 0.2), store('h', '#akTy', 0.1),
        f'function {T}halo with storage {STO} t',
    ])
    W.w('tele/e/halo', [*mk('t_ring', '~ ~$(h) ~', '$(r2)f,1f,$(r2)f', '$(r)f,1f,$(r)f', '$(c1)')])
    W.w('tele/glyph_circle', [
        '# The intro seal\'s gold floor glyph circle (decor, never paired with a hazard; plan §2.2, §5 E): {r (tenths),',
        '# tell (ticks to draw in), hold}. At the floor centre (the spawn): the glyph circle grows 0.6 r -> r over the',
        '# tell with a gold rim and an inner ring, then stays `hold` ticks (tele/clear removes it). 3 cards.',
        *head(['$scoreboard players set #akTr mb $(r)'], el=5, nd=0),
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        store('r', '#akTr', 0.1), store('r6', '#akTr', 0.06), store('r5', '#akTr', 0.055),
        f'function {T}gcircle with storage {STO} t',
    ])
    W.w('tele/e/gcircle', [*mk('t_gcircle', '~ ~0.04 ~', '$(r6)f,1f,$(r6)f', '$(r)f,1f,$(r)f', '16777215', flash='-1'),
                           *mk('t_rim', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', str(GOLD), flash='-1'),
                           *mk('t_ring', '~ ~0.046 ~', '$(r5)f,1f,$(r5)f', '$(r5)f,1f,$(r5)f', str(GOLD_PALE), flash='-1')])
    W.w('tele/clear', ['# Remove every attack telegraph of the kit (decals, lanes, fronts, safe circles, the wash, the crater,',
                       '# halos); fx cards and the field pool stay (a cancelled pattern, a pause).',
                       f'kill {SEL}_t]', f'execute store result score #akTN mb if entity {SEL}_t]'])

    # ---- the field pool (N6)
    fcols = []
    for el in sorted(TELE_COL):
        fk = f'fld{el}' if 1 <= el <= 5 else 'fld5'
        sk = f'fst{el}' if el in (3, 4) else 't_lane'
        fcols.append(f'execute if score #akTEl mb matches {el} run data modify storage {STO} fd merge value '
                     f'{{c1:{TELE_COL[el][0]},c2:{TELE_COL[el][1] if sk == "t_lane" else WHITE},fk:"{fk}",sk:"{sk}"}}')
    W.w('tele/e/fprep', [
        '# Internal: field-pool setup from #akTEl, #akTell (= life): the element look, life, fade 8, #akTel 2.',
        f'data modify storage {STO} fd merge value {{c1:{TELE_COL[5][0]},c2:{WHITE},fk:"fld5",sk:"t_lane",tpd:0}}',
        *fcols,
        'execute if score #akTell mb matches ..9 run scoreboard players set #akTell mb 10',
        'scoreboard players operation #akLife mb = #akTell mb',
        'scoreboard players set #akFade mb 8', 'scoreboard players set #akDur mb 4', 'scoreboard players set #akDly mb 0',
        'scoreboard players set #akHit mb -1', 'scoreboard players set #akRoll mb 0', 'scoreboard players set #akSpin mb 0',
        'scoreboard players set #akTel mb 2',
    ])

    def fmk(kind, pos, s0, s1, col, rot='~ 0'):
        return [f'$data modify storage {STO} a set value {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"fixed",'
                f's0:"{s0}",s1:"{s1}",off:"0f,0f,0f",move:"0f,0f,0f",col:{col},col2:-1,ax:"0f,1f,0f",'
                f'tg:"$(tg)",t2:"rlk_ak_c",tpd:0}}',
                f'function {E}make']
    W.w('tele/field', [
        '# Lingering field disc (N6 field pool): {id:<0-7>, r (tenths), el, life (ticks)} at the floor point: the',
        '# element fill (Pyro fire ring, Hydro pool, Electro crackle, Cryo frost seal, Geo cracks) and a rim. Calling an',
        '# id again redraws it (refresh, resume). Never counted against the fx / attack-telegraph caps; at most',
        f'# {FCAP} cards (skipped beyond). 2 cards.',
        f'$kill {SEL}_f$(id)]',
        f'execute store result score #akFN mb if entity {SEL}_fp]',
        f'execute if score #akFN mb matches {FCAP - 1}.. run return 0',
        '$scoreboard players set #akTEl mb $(el)', '$scoreboard players set #akTell mb $(life)',
        '$scoreboard players set #akTr mb $(r)',
        'execute if score #akTr mb matches ..1 run scoreboard players set #akTr mb 2',
        f'function {T}fprep',
        f'execute store result storage {STO} fd.r float 0.1 run scoreboard players get #akTr mb',
        f'execute store result storage {STO} fd.r8 float 0.085 run scoreboard players get #akTr mb',
        f'$data modify storage {STO} fd.tg set value "rlk_ak_f$(id)"',
        f'function {T}field with storage {STO} fd',
    ])
    W.w('tele/e/field', [*fmk('$(fk)', '~ ~0.03 ~', '$(r8)f,1f,$(r8)f', '$(r)f,1f,$(r)f', '$(c2)'),
                         *fmk('t_rim', '~ ~0.033 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', '$(c1)')])
    W.w('tele/strip', [
        '# Lingering element strip (N6 field pool): {id:<0-7>, len, w (tenths), yaw:<absolute world yaw, int degrees>,',
        '# el, life} from the executing point along the absolute yaw (Electro crackle / Cryo frost; other elements a',
        '# tinted lane), with an outline. Calling an id again redraws it. 2 cards.',
        f'$kill {SEL}_f$(id)]',
        f'execute store result score #akFN mb if entity {SEL}_fp]',
        f'execute if score #akFN mb matches {FCAP - 1}.. run return 0',
        '$scoreboard players set #akTEl mb $(el)', '$scoreboard players set #akTell mb $(life)',
        '$scoreboard players set #akTl mb $(len)', '$scoreboard players set #akTw mb $(w)',
        'execute if score #akTl mb matches ..1 run scoreboard players set #akTl mb 2',
        'execute if score #akTw mb matches ..1 run scoreboard players set #akTw mb 2',
        f'function {T}fprep',
        f'execute store result storage {STO} fd.len float 0.1 run scoreboard players get #akTl mb',
        f'execute store result storage {STO} fd.w float 0.1 run scoreboard players get #akTw mb',
        f'$data modify storage {STO} fd.tg set value "rlk_ak_f$(id)"',
        f'$execute rotated $(yaw) 0 run function {T}strip with storage {STO} fd',
    ])
    W.w('tele/e/strip', [*fmk('$(sk)', '^ ^0.03 ^', '$(w)f,1f,$(len)f', '$(w)f,1f,$(len)f', '$(c2)'),
                         *fmk('t_frame', '^ ^0.033 ^', '$(w)f,1f,$(len)f', '$(w)f,1f,$(len)f', '$(c1)')])
    W.w('tele/field_end', ['# Remove field / strip {id} now (cancelled, expired early).', f'$kill {SEL}_f$(id)]',
                           f'execute store result score #akFN mb if entity {SEL}_fp]'])
    W.w('tele/field_clear', ['# Remove every field-pool card (pause, death; the module redraws its field table on resume).',
                             f'kill {SEL}_fp]', 'scoreboard players set #akFN mb 0'])


# ----------------------------------------------------------------------------- props (as @s = a module item_display)
ICICLE_TR = ('{translation:[0f,0f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[1.6f,1.6f,1.6f],'
             'right_rotation:[0f,0f,0f,1f]}')
# name -> (comment, item kind, tint, billboard, scale SNBT or None = keep the module's transformation)
PROPS = {
    'seal_stele': ('Intro seal stele (6 at r 8 around the spawn): a dark red-brown carved tablet with glowing gold cracks, '
                   '1.1 x 3.2 x 0.4 b standing on the prop (box kind, pivot at its centre: spawn it 1.6 b up).', 'stele',
                   WHITE, 'fixed', '[1.6f,1.6f,1.6f]'),
    'seal_chunk': ('Seal stele chunk (shatter pieces): a 0.6 b block of the stele stone.', 'stele', WHITE, 'fixed',
                   '[0.9f,0.3f,1.4f]'),
    'seal_prism': ('Intro seal prism (UUID 0x80): an eight-walled translucent gold glyph prism, radius 6 b, 9 b tall, '
                   'standing on the prop.', 'prism', WHITE, 'fixed', '[6f,6f,6f]'),
    'gate_icon': ('The gate label icon (registry icon.model; also the item model rlk:mboss/az_kit/gate_icon), 1 b, '
                  'turning to the viewer.', 'gate_icon', WHITE, 'vertical', '[1f,1f,1f]'),
    'orb': ('격류 범람 Hydro orb (31): a water sphere 2.6 b across (hz r 1.3), camera-facing; pair with p/orb_ribbon every '
            '2 t.', 'orb', WHITE, 'center', '[2.6f,2.6f,2.6f]'),
    'meteor_big': ('운석 낙하 big meteor (32): molten head with a flame trail up, 3.6 b, upright.', 'meteor', WHITE,
                   'vertical', '[3.6f,3.6f,3.6f]'),
    'meteor_small': ('운석 낙하 small meteor (32), 1.7 b, upright.', 'meteor', WHITE, 'vertical', '[1.7f,1.7f,1.7f]'),
    'lump': ('Pyro molten lump (P1 / P2 / P5 extras), 1 b, camera-facing; pair with p/lump_trail.', 'lava', WHITE, 'center',
             '[1f,1f,1f]'),
    'elump': ('Electro crystal lump (46), a violet crystal cluster 1.4 b.', 'crystal', ELECTRO, 'fixed', '[1.4f,1.4f,1.4f]'),
    'shell': ('번개의 가루 shell (44): a violet sphere with the square glyph, 1.2 b, camera-facing.', 'shell', WHITE, 'center',
              '[1.2f,1.2f,1.2f]'),
    'icicle': ('Ice lance / icicle (41, 43): tip along the prop\'s facing (local +z; aim it with tp ... facing), 1.6 b '
               'long.', 'icicle', WHITE, 'fixed', None),
    'ice_sphere': ('쏟아지는 천화 spiky ice sphere (43), 2.2 b, camera-facing; pair with p/ice_sphere.', 'ice_sphere', WHITE,
                   'center', '[2.2f,2.2f,2.2f]'),
    'cone': ('Planted stone cone (P8), 2 b tall, foot at the prop, upright.', 'cone', WHITE, 'vertical', '[2f,2f,2f]'),
    'crater': ('B3 crater at the floor cut (UUID 0x81): the rubble crater, radius 7.5 b, flat at the prop (spawn it '
               '0.03 b over the floor).', 't_crater', WHITE, 'fixed', '[7.5f,1f,7.5f]'),
}
CRYSTAL_COL = {1: rgb('#FF7A3A'), 2: rgb('#5EC4FF'), 3: rgb('#B07CFF'), 4: rgb('#A8F2FF'), 5: rgb('#F2C25A')}
WATER_COL = {1: rgb('#FF8A5A'), 2: rgb('#5AB8F0'), 3: rgb('#A884F0'), 4: rgb('#B4F0FF'), 5: rgb('#C8B080')}
# family -> (comment, (lo, hi), {el: (kind, tint)}, billboard, scale SNBT or None)
PFAM = {
    'arena_crystal': ('Arena crystal cluster in the element look (plan §2.6; theme.md §6.3): pale crystals tinted geo gold / '
                      'Pyro / Hydro / Electro / Cryo. Keeps the module\'s transformation (the theme record\'s scale).',
                      (1, 5), {el: ('crystal', CRYSTAL_COL[el]) for el in range(1, 6)}, None, None),
    'water_sheet': ('The 14-b shallow-water tile at y 201.005 in the element look (about 40 % alpha). Keeps the module\'s '
                    'transformation (the theme record\'s scale 14).', (1, 5),
                    {el: ('water', WATER_COL[el]) for el in range(1, 6)}, None, None),
    'glyph': ('Entrance stele / arrival glyph: flame, water curl, bolt, snowflake, Geo emblem (the item models '
              'rlk:mboss/az_kit/glyph_<pyro|hydro|electro|cryo|geo>). Keeps the module\'s transformation.', (1, 5),
              {el: (f'glyph_{EL_KEYS[el]}', WHITE) for el in range(1, 6)}, None, None),
    'spike': ('천동만상 spike (P4 Geo / 45 Cryo / 46 Electro): 2.5 b, tip up at scale 1 (pitch the prop to plant it point '
              'first).', (3, 5), {3: ('spike_electro', WHITE), 4: ('spike_cryo', WHITE), 5: ('spike_geo', WHITE)},
              'fixed', '[2.5f,2.5f,2.5f]'),
    'shard': ('응결 결정 (the brand shield pickup, plan §4.10-4): a gold-amber crystal with the brand element inside, 1 b, '
              'camera-facing.', (1, 4), {el: (f'shard_{EL_KEYS[el]}', WHITE) for el in range(1, 5)}, 'center', '[1f,1f,1f]'),
}


def prop_tr(scale):
    return '{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:' + scale + ',right_rotation:[0f,0f,0f,1f]}'


def prop_line(kind, col, bb, scale, name):
    item = (f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{NS_TEX}{kind}",'
            f'"minecraft:custom_model_data":{{colors:[{col}]}}}}}}')
    if bb is None:
        return f'data merge entity @s {{{item},brightness:{{sky:15,block:15}}}}'
    tr = ICICLE_TR if name == 'icicle' else prop_tr(scale)
    return (f'data merge entity @s {{{item},billboard:"{bb}",brightness:{{sky:15,block:15}},view_range:2f,'
            f'shadow_radius:0f,transformation:{tr}}}')


def static_dispatch(base, lo, hi, call=''):
    """One static line per family member, chosen by #akPe (already clamped by the caller): no macro-built function
    names, so check_refs / lint / check_macro see every target (az_fx_api.md section 0.7)."""
    return [('$' if '$(' in call else '') + f'execute if score #akPe mb matches {k} run return run function {base}/{k}' +
            (' ' + call if call else '') for k in range(lo, hi + 1)]


def props(W):
    for name, (doc, kind, col, bb, sc) in PROPS.items():
        W.w(f'prop/{name}', [f'# {doc}', '# As @s = an item_display the module owns: item, tint, billboard, full bright,',
                             '# transformation. Keep teleport_duration 1 on moving props.',
                             prop_line(kind, col, bb, sc, name)])
    for name, (doc, (lo, hi), mem, bb, sc) in PFAM.items():
        for el, (kind, col) in mem.items():
            W.w(f'prop/{name}/{el}', [f'# {doc}', f'# Element {el} ({EL_KEYS[el]}). As @s.', prop_line(kind, col, bb, sc, name)])
        oor = (f'execute unless score #akPe mb matches {lo}..{hi} run scoreboard players set #akPe mb 5' if hi == 5 else
               f'execute unless score #akPe mb matches {lo}..{hi} run return 0')
        W.w(f'prop/{name}', [f'# {doc}', f'# Dispatcher {{el}} (as @s): el {lo}..{hi}; anything else ' +
                             ('draws Geo (5).' if hi == 5 else 'does nothing.'),
                             '$scoreboard players set #akPe mb $(el)', oor] + static_dispatch(f'{FN}prop/{name}', lo, hi))


# ----------------------------------------------------------------------------- sounds


def sounds(W):
    for name, (doc, layers) in SOUNDS.items():
        W.w(f'snd/{name}', [f'# {doc}', '# Layers: event volume pitch minVolume (per-layer minimum, mboss_lib.sound rule).'] +
            [sound_line(*l) for l in layers])
    for name, ((lo, hi), mem) in SFAM.items():
        for el, (doc, layers) in mem.items():
            W.w(f'snd/{name}/{el}', [f'# {doc}', '# Layers: event volume pitch minVolume.'] + [sound_line(*l) for l in layers])
        oor = (f'execute unless score #akPe mb matches {lo}..{hi} run scoreboard players set #akPe mb 5' if hi == 5 else
               f'execute unless score #akPe mb matches {lo}..{hi} run return 0')
        W.w(f'snd/{name}', [f'# Dispatcher {{el}}: snd/{name}/<el> for el {lo}..{hi}; anything else ' +
                            ('plays Geo (5).' if hi == 5 else 'plays nothing.'),
                            '$scoreboard players set #akPe mb $(el)', oor] + static_dispatch(f'{FN}snd/{name}', lo, hi))


# ----------------------------------------------------------------------------- HUD
HUD_FUNCS = ('banner_end', 'cue_jump', 'cue_end', 'flash_white', 'flash_gold', 'flash_amber', 'flash_violet', 'flash_end',
             'clear')
HFAM = ('banner_tr', 'banner_ab', 'banner_ab2', 'banner_brand')
TXT = '#F4E8CD'
SUBTXT = '#C9BFA8'


def gls(text, extra=''):
    return '{text:"' + text + '",font:"' + FONT + '",color:"white"' + extra + '}'


def banner_component(kind, el):
    name, col = EL_NAMES[el], EL_HEX[el]
    orn_l, orn_r = gl('orn_l', f',color:"{col}"'), gl('orn_r', f',color:"{col}"')
    nm = f'{{text:"{name}",color:"{col}",bold:true}}'
    if kind == 'banner_tr':
        return (f'[{orn_l},{{text:" 야타용왕이 곧 ",color:"{TXT}"}},{nm},{{text:" 원소의 힘을 흡수합니다… ",color:"{TXT}"}},'
                f'{orn_r}]'), 60
    if kind == 'banner_ab':
        return f'[{orn_l},{{text:" "}},{nm},{{text:" 원소 흡수 ",color:"{col}",bold:true}},{orn_r}]', 60
    if kind == 'banner_ab2':
        return (f'[{orn_l},{{text:" "}},{nm},{{text:" 원소 흡수",color:"{col}",bold:true}},'
                f'{{text:"  ·  원소를 추가로 하나 더 흡수합니다 ",color:"{SUBTXT}"}},{orn_r}]'), 80
    brand = gl('brand', ',color:"' + col + '"')
    return (f'[{brand},{{text:" 야타용왕의 ",color:"{TXT}"}},{nm},'
            f'{{text:" 원소 공격에 맞고 보호막이 없으면 계속 ",color:"{TXT}"}},{nm},{{text:" 원소 피해를 받습니다",color:"{TXT}"}}]'), 100


def hud_funcs(W):
    H = FN + 'hud/'
    docs = {'banner_tr': 'the transition message "야타용왕이 곧 {물} 원소의 힘을 흡수합니다…" (60 t)',
            'banner_ab': 'the absorb banner "{물} 원소 흡수" (absorb 1, 60 t)',
            'banner_ab2': 'the absorb-2 banner "{번개} 원소 흡수 · 원소를 추가로 하나 더 흡수합니다" (80 t)',
            'banner_brand': 'the phase-2 brand tutorial "야타용왕의 {물} 원소 공격에 맞고 보호막이 없으면 계속 {물} 원소 피해를 받습니다" (100 t)'}
    for kind in HFAM:
        for el in range(1, 5):
            comp, hold = banner_component(kind, el)
            W.w(f'hud/{kind}/{el}', [f'# {docs[kind]}, element {el} ({EL_NAMES[el]}): the actionbar for {hold} t, holding',
                                     '# the regular actionbar HUD (hudHold). No sound (the caller plays snd/msg_chime / the',
                                     '# absorb recipes).',
                                     f'title @a[tag=player] actionbar {comp}',
                                     f'scoreboard players set @a[tag=player] hudHold {hold}'])
        W.w(f'hud/{kind}', [f'# Dispatcher {{el}} of hud/{kind}/<el> (el 1..4; anything else shows nothing).',
                            '$scoreboard players set #akPe mb $(el)',
                            'execute unless score #akPe mb matches 1..4 run return 0'] + static_dispatch(f'{H}{kind}', 1, 4))
    W.w('hud/banner_end', ['# Drop a banner early (cancel, cut-scene end).', 'title @a[tag=player] actionbar ""',
                           'scoreboard players set @a[tag=player] hudHold 0'])
    W.w('hud/cue_jump', ['# The "점프!" cue on the title line for 12 t (landslide waves - 8; the kit\'s big glyph); vBig rests',
                         '# the F5 crosshair title. Pair with snd/jump_cue.',
                         'scoreboard players set @a[tag=player] vBig 14',
                         'title @a[tag=player] times 0 9 3',
                         'title @a[tag=player] title [' + gl('jump', ',shadow_color:0') + ']'])
    W.w('hud/cue_end', ['# Drop the jump cue at once.', 'scoreboard players set @a[tag=player] vBig 0',
                        'title @a[tag=player] times 0 1 2', 'title @a[tag=player] title ""'])
    for name, g, t in (('flash_white', 'fl_white', '0 2 5'), ('flash_gold', 'fl_gold', '1 3 8'),
                       ('flash_amber', 'fl_amber', '0 3 8'), ('flash_violet', 'fl_violet', '1 4 9')):
        W.w(f'hud/{name}', ['# Full-screen flat flash on the title line (any view mode); vBig rests the F5 crosshair.',
                            'scoreboard players set @a[tag=player] vBig 16',
                            f'title @a[tag=player] times {t}',
                            'title @a[tag=player] title [' + gl(g, ',shadow_color:0') + ',' + gls(SP_NEG1) + ']'])
    W.w('hud/flash_end', ['# Drop a title overlay (flash, jump cue) at once (pause, cancel).',
                          'scoreboard players set @a[tag=player] vBig 0',
                          'title @a[tag=player] times 0 1 2', 'title @a[tag=player] title ""'])
    W.w('hud/clear', ['# Every banner, cue and flash off (fight end, death, abort, uninstall).',
                      'title @a[tag=player] actionbar ""', 'scoreboard players set @a[tag=player] hudHold 0',
                      'scoreboard players set @a[tag=player] vBig 0', 'title @a[tag=player] times 0 1 2',
                      'title @a[tag=player] title ""'])


# ----------------------------------------------------------------------------- presets (macro plumbing)
PH = __import__('re').compile(r'\$\((\w+)\)')


def _derived(args, lines):
    """the storage conversions a preset needs: base args (tenths / ticks) and derived placeholders <arg>_<pct>,
    <arg>_m<pct> (sizes: blocks x pct %), <arg>_<pct> / <arg>_p<k> (ticks: pct % / + k ticks)"""
    names = sorted({m for l in lines for m in PH.findall(l)})
    conv = []
    for a in args:
        conv.append(f'$scoreboard players set #akA_{a} mb $({a})')
    for nm in names:
        base, _, suf = nm.partition('_')
        if nm in args:
            base, suf = nm, ''
        assert base in args, (nm, args)
        if base in ARG_SIZE:
            if not suf:
                scale = 0.1
            else:
                neg = suf.startswith('m')
                scale = (-1 if neg else 1) * int(suf.lstrip('m')) / 1000
            conv.append(f'execute store result storage {STO} pr.{nm} float {num(scale, 5)} run scoreboard players get '
                        f'#akA_{base} mb')
        else:
            if not suf:
                conv.append(f'execute store result storage {STO} pr.{nm} int 1 run scoreboard players get #akA_{base} mb')
            elif suf.startswith('p'):
                conv += [f'scoreboard players operation #akB mb = #akA_{base} mb',
                         f'scoreboard players add #akB mb {int(suf[1:])}',
                         f'execute store result storage {STO} pr.{nm} int 1 run scoreboard players get #akB mb']
            else:
                conv.append(f'execute store result storage {STO} pr.{nm} int {num(int(suf) / 100, 3)} run scoreboard '
                            f'players get #akA_{base} mb')
    return conv


def emit_preset(W, rel, worker, doc, args, lines, ambient, extra_doc=(), trail=False):
    head = [f'# {doc}', *extra_doc]
    if ambient:
        head += [f'# Ambient: skipped while {SOFT}+ fx cards live (room for the fx of the hits).',
                 f'execute if score #akN mb matches {SOFT}.. run return 0']
    elif trail:
        head += [f'# Trail: skipped while {TSOFT}+ fx cards live (room for the hit-tick visuals).',
                 f'execute if score #akN mb matches {TSOFT}.. run return 0']
    if not args:
        assert not any('$(' in l for l in lines), rel
        W.w(rel, head + lines)
        return
    head.insert(1, '# {' + ', '.join(args) + '} (macro; sizes in tenths of a block, ticks as ints)')
    W.w(rel, head + _derived(args, lines) + [f'function {FN}{worker} with storage {STO} pr'])
    W.w(worker, [f'# Internal (macro, storage {STO} pr): the cards of {rel}.'] + [mac(l) for l in lines])


def presets_dp(W):
    assert set(AMBIENT) <= set(PRESETS) | set(EPRESETS), set(AMBIENT) - set(PRESETS)
    assert set(TRAIL) <= set(PRESETS) and not set(TRAIL) & set(AMBIENT), set(TRAIL) - set(PRESETS)
    for name, (doc, args, f) in PRESETS.items():
        emit_preset(W, f'p/{name}', f'p/e/{name}', doc, args, f(), name in AMBIENT, trail=name in TRAIL)
    for name, (doc, args, mem) in EPRESETS.items():
        for el, f in mem.items():
            emit_preset(W, f'p/{name}/{el}', f'p/e/{name}_{el}', doc, args, f(), name in AMBIENT,
                        (f'# Element {el} ({EL_KEYS[el]}).',))
        call = ('{' + ','.join(f'{a}:$({a})' for a in args) + '}') if args else ''
        W.w(f'p/{name}', [f'# {doc}', '# Dispatcher {el' + ''.join(', ' + a for a in args) + '} (macro): fx/p/' + name +
                          '/<el>, el 1..5 (0 and 6-8 draw Geo).',
                          '$scoreboard players set #akPe mb $(el)',
                          'execute unless score #akPe mb matches 1..5 run scoreboard players set #akPe mb 5']
            + static_dispatch(f'{FN}p/{name}', 1, 5, call))


def preset_cards(name, el=None):
    """fx cards a preset (or a family member) spawns"""
    if name in EPRESETS:
        lines = EPRESETS[name][2][el or 5]()
    else:
        lines = PRESETS[name][2]()
    return sum(1 for l in lines if f'{FN}card' in l or f'{FN}e/cardf' in l)


# ----------------------------------------------------------------------------- tests and demos
TEST_ARGS = {'r': 4.0, 'r0': 2.0, 'r1': 9.0, 'w': 2.0, 'dur': 12, 't': 30, 'len': 8.0, 'h': 8.0}


def _test_call(name, el=None):
    if name in EPRESETS:
        args = EPRESETS[name][1]
        return fxe(name, el or 5, **{a: TEST_ARGS[a] for a in args})
    args = PRESETS[name][1]
    return fx(name, **{a: TEST_ARGS[a] for a in args})


# Demo timelines (in-game previews on a vanilla stand-in anchor; F:fx/test/demo/<name>): (tick, where, line). The
# anchor is a marker 12 b in front of the player facing them ("forward" = toward the player). where: 'a' (the anchor's
# floor point), (x, z) / (x, z, y) local offsets from it (x left, z forward), 'p' (the player's feet, rotated as the
# anchor), ('p', x, z). Lines may hold $(g) (the ground element: Geo in phase 1, the leg element after), $(l) (leg)
# and $(t) (tail) from storage rlk:azkit dm (fx/test/pair {leg, tail, ph}).
G, L, TL = '$(g)', '$(l)', '$(t)'


def _wedges(n, a0, a1, r0, r1, tell0, nd=1, el=5):
    out = []
    for k in range(n):
        lo = a0 + (a1 - a0) * k / n
        hi = a0 + (a1 - a0) * (k + 1) / n
        out.append(tele_wedge(r0, r1, int(round(lo)), int(round(hi)), tell0 + k, el, nd, 3))
    return out


def _demo_p1():
    ev = [(0, 'a', snd('chin_rear')), (10, (0, 6.5), tele_disc(5.0, 25, G)), (10, (0, 6.5), tele_sector(5.6, 30, 25, G)),
          (35, (0, 6.5), fxe('crown', G)), (35, (0, 6.5), fxe('cracks', G, r=5.6)), (35, (0, 6.5), fxe('dust_ring', G, r=5.0)),
          (35, (0, 6.5), fxe('impact', G)), (35, (0, 6.5), snd('chin_impact')), (35, 'p', hud('flash_amber'))]
    return 65, ev


def _demo_p2():
    ev = [(1, (0, 8), tele_disc(4.5, 20, G)), (1, (0, 8), tele_wave(0, 3.0, 10.5, 2.5, 20, 5, G)),
          (12, (0, 8), tele_wave(1, 3.0, 10.5, 2.5, 20, 5, G)), (6, 'a', snd('jump_takeoff')),
          (20, (0, 8), fxe('front', G, r0=3.0, r1=10.5, w=2.5, dur=5)), (21, (0, 8), fxe('impact', G)),
          (21, (0, 8), fxe('dust_ring', G, r=4.5)), (21, (0, 8), snd('jump_land')),
          (31, (0, 8), fxe('front', G, r0=3.0, r1=10.5, w=2.5, dur=5)), (32, (0, 8), snd('jump_wave2')),
          (32, (0, 8), fx('dust'))]
    return 53, ev


def _demo_p3():
    ev = [(0, 'a', snd('charge_growl')), (4, 'a', tele_mline(0, 26.0, 8.0, 20, 5, hold=24)), (14, 'a', tele_mline_end(0)),
          (14, 'a', tele_line(26.0, 8.0, 10, 5, 0, 24))]
    for t in range(24, 48, 4):
        ev += [(t, (0, (t - 24) * 1.0), fx('dust_trail')), (t, (0, (t - 24) * 1.0), snd('charge_gallop'))]
    ev += [(48, (0, 24), fx('skid')), (48, (0, 24), snd('charge_skid'))]
    return 70, ev


def _demo_p4():
    pts = [(0, 4), (1, 8), (2, 12), (3, 16)]
    land = [46, 51, 54, 59]
    expl = [76, 79, 82, 85]
    ev = [(0, (0, 0, 6), fx('gold_plume')), (0, 'a', snd('spikes_bristle')), (14, 'a', snd('spikes_launch'))]
    for (x, z), tl, te in zip(pts, land, expl):
        ev += [(tl - 14, (x, z), tele_disc(1.6, 14, G)), (tl - 4, (x, z), fx('shard_fall', h=8.0)),
               (tl, (x, z), fxe('impact', G)), (tl, (x, z), snd('spikes_land')),
               (te - 14, (x, z), tele_disc(2.5, 14, G)), (te, (x, z), fxe('crown', G)), (te, (x, z), snd('spikes_explode'))]
    return 90, ev


def _demo_p5():
    ev = [(3, (2, 3), tele_disc(2.8, 14, G)), (3, (2, 3), tele_ring(2.8, 9.7, 14, G))]
    for k, s in enumerate((17, 32, 47)):
        ev += [(s - 14, (2, 3), tele_wave(k, 1.5, 9.7, 2.0, 14, 15, G)), (s - 1, (2, 3), fxe('front', G, r0=1.5, r1=9.7, w=2.0, dur=15)),
               (s, (2, 3), snd('stomp_wave'))]
    ev += [(17, (2, 3), fxe('impact', G)), (17, (2, 3), snd('stomp_slam')), (17, (2, 3), fxe('cracks', G, r=2.8))]
    return 63, ev


def _demo_p5b():
    ev = []
    for k, (s, x) in enumerate(((17, 2), (40, -2), (63, 2))):
        ev += [(s - 14, (x, 3), tele_disc(2.8, 14, G)), (s - 14, (x, 3), tele_wave(k, 1.5, 9.7, 2.0, 14, 15, G)),
               (s - 1, (x, 3), fxe('front', G, r0=1.5, r1=9.7, w=2.0, dur=15)), (s, (x, 3), fxe('impact', G)),
               (s, (x, 3), snd('stomp_slam')), (s + 5, (x, 3), fx('splash_wall', r=6.5))]
    return 85, ev


def _demo_p6():
    left, right = (5.3, -6.0), (-5.3, 5.0)
    ev = [(0, left, tele_lane_side(11.0, 6.6, 22, G)), (0, right + (0, 180), tele_lane_side(11.0, 6.6, 22, G)),
          (0, (0, 6.5), tele_disc(2.5, 22, G)), (0, (0, -5.5), tele_disc(2.5, 22, G)), (0, 'a', snd('feint_sway')),
          (8, 'a', snd('feint_sway')), (22, left, fxe('flank_blades', G, len=11.0)), (22, left, fx('dust_wall', len=11.0)),
          (22, right + (0, 180), fxe('flank_blades', G, len=11.0)), (22, right + (0, 180), fx('dust_wall', len=11.0)),
          (22, (0, 6.5), fxe('impact', G)), (22, (0, -5.5), fxe('impact', G)), (22, 'a', snd('feint_burst'))]
    return 50, ev


def _demo_p7():
    ev = [(0, (0, -5), w) for w in _wedges(9, 65, 180, 0, 12.0, 23, 1, 5)]
    ev += [(0, 'a', snd('whip_raise')), (23, 'a', snd('whip_sweep')), (25, (-5, -2, 0, 120), fx('tail_lane')),
           (28, (-6, -6, 0, 150), fx('boulders'))]
    for k in range(4):
        ev.append((19, (-1.5 - 2.5 * k, -5 + 0.5 * k), tele_disc(1.6, 14, G)))
        ev.append((33, (-1.5 - 2.5 * k, -5 + 0.5 * k), fxe('crown', G)))
    ev.append((33, 'a', snd('whip_erupt')))
    return 64, ev


def _demo_p7_ice():
    ev = [(0, (0, -5), w) for w in _wedges(4, 65, 180, 5.0, 12.0, 25, 0, 4)]
    for k in range(4):
        ev.append((25 + 2 * k, (-3.5 - 1.5 * k, -5 - 3.5 * (k > 1), 0, 100 + 25 * k), fx('ice_wall')))
    return 50, ev


def _demo_p8():
    ev = [(0, 'a', snd('tslam_raise')), (9, (0, -5, 0, 180), tele_line(13.0, 3.5, 30, G)),
          (39, (0, -5, 0, 180), fxe('spike_line', G, len=13.0)), (39, (0, -5, 0, 180), fx('leaf_burst')),
          (39, 'a', snd('tslam_impact')), (41, (0, -5, 0, 180), fx('cones'))]
    return 100, ev


def _demo_p9():
    ev = [(0, 'a', fxe('dig', 5)), (0, 'a', snd('burrow_dive')), (20, 'a', fx('mound'))]
    for t, pos in ((50, ('p', 0, 0)), (75, ('p', 2, 1))):
        ev += [(t - 19, pos, tele_disc(3.4, 19, 5)), (t - 19, pos, fx('light_shaft')), (t - 19, pos, snd('burrow_ring')),
               (t - 6, pos, fx('rock_rain', r=3.4)), (t, pos, fxe('impact', 5)), (t, pos, snd('burrow_rock')), (t, pos, fx('dust'))]
    ev += [(80, (0, 2), tele_line(10.0, 6.0, 20, 5)), (100, (0, 4), fx('mound')), (100, (0, 4), snd('burrow_rush')),
           (100, (0, 4), fx('dust')), (105, (0, 8), fx('dust')), (110, (0, 12), fx('dust')),
           (120, 'a', tele_disc(3.7, 19, 5)), (139, 'a', fx('emerge_spikes', r=3.7)), (139, 'a', snd('b3_emerge'))]
    for t in (40, 70, 100):
        ev.append((t, 'a', snd('burrow_loop')))
    return 160, ev


def _demo_t1():
    ev = [(0, 'p', hude('banner_tr', L)), (0, 'p', snd('msg_chime')), (10, 'a', snd('slide_lift')), (30, 'a', snd('slide_lift'))]
    waves = [(57, 18.0, 3.5, 5, 0.8), (77, 18.0, 3.5, 5, 0.8), (98, 18.0, 3.5, 5, 0.8), (118, 18.0, 3.5, 5, 0.8),
             (139, 18.0, 3.5, 5, 0.8), (179, 30.0, 4.5, 7, 1.0)]
    for k, (s, r1, w, dur, _c) in enumerate(waves):
        ev += [(s - 20, 'a', tele_wave(k, 4.0, r1, w, 20, dur, G, 2, 2)),
               (s - 1, 'a', fxe('front', G, r0=4.0, r1=r1, w=w, dur=dur)),
               (s - 8, 'p', hud('cue_jump')), (s - 8, 'p', snd('jump_cue')),
               (s, 'a', snd('slide_wave6' if k == 5 else 'slide_wave'))]
    return 203, ev


def _demo_t2():
    ev = [(0, 'a', fxe('vortex', L, t=47)), (0, 'a', fxe('sigils', L)), (0, 'a', snde('absorb_vortex', L)),
          (47, 'a', fxe('recolour', L, r=28.0, t=20)), (47, 'a', snde('absorb_burst', L)), (47, 'p', hude('banner_ab', L)),
          (47, (0, 0, 3), fxe('impact', L)), (47, 'p', hud('flash_white')), (60, 'a', fx('shock_dome', r=8.0)),
          (94, 'a', snd('absorb_roar')), (100, 'a', fx('shock_dome', r=10.0)), (100, 'a', snd('roar_ring')),
          (108, 'a', fx('shock_dome', r=10.0)), (108, 'a', snd('roar_ring')), (110, 'p', hude('banner_brand', L))]
    return 140, ev


def _demo_t3():
    ev = [(0, 'a', fxe('vortex', TL, t=42)), (0, 'a', fxe('sigils', TL)), (0, 'a', snde('absorb_vortex', TL)),
          (42, 'a', fxe('recolour', TL, r=28.0, t=20)), (42, 'a', snde('absorb_burst', TL)),
          (42, 'p', hude('banner_ab2', TL)), (42, 'a', fxe('shard_rain', TL, r=20.0, t=48)), (42, 'p', hud('flash_violet')),
          (52, 'a', snd('absorb_roar')), (72, 'a', fx('shock_dome', r=10.0)), (72, 'a', snd('roar_ring'))]
    return 110, ev


def _demo_b3():
    ev = [(0, 'a', fxe('dig', G)), (0, 'a', snd('b3_sink')), (0, 'a', tele_crater(7.5, 40, 120)), (40, 'a', fx('mound')),
          (58, 'a', snd('b3_rise')), (120, 'a', fx('mound')), (140, 'a', tele_disc(5.2, 28, G)),
          (168, 'a', fx('emerge_spikes', r=5.2)), (168, 'a', fxe('impact', G)), (168, 'a', snd('b3_emerge'))]
    return 190, ev


def _demo_m31():
    ev = [(0, 'a', snd('orb_spawn')), (20, 'a', snd('orb_loop'))]
    for t in range(0, 60, 2):
        for k, (r, w) in enumerate(((6.5, -3.5), (6.5, -3.5), (10.5, 2.4), (10.5, 2.4))):
            a = math.radians((90 if k % 2 else -90) + (0 if k < 2 else 90) + w * t)
            ev.append((t, (r * math.sin(a), r * math.cos(a), 1.2), fx('orb_ribbon')))
    return 62, ev


def _demo_m32():
    ev = [(7, 'p', tele_seal8(5.2, 28)), (7, 'p', snd('meteor_glyph')), (29, 'p', fx('meteor_big', h=12.0)),
          (29, 'p', snd('meteor_fall')), (35, 'p', fx('fire_dome', r=5.2)), (35, 'p', snd('meteor_impact')),
          (36, 'p', tele_field(0, 4.5, 1, 200))]
    for k, t in enumerate((44, 50, 56, 62, 68, 74)):
        pos = ('p', 4 * math.sin(k * 2.1), 4 * math.cos(k * 2.1))
        ev += [(t - 12, pos, tele_halo(2.8, 3.0, 12, 1)), (t - 12, pos, tele_disc(2.8, 12, 1)),
               (t - 4, pos, fx('meteor_small', h=6.0)), (t, pos, fxe('impact', 1)), (t, pos, snd('meteor_small'))]
        if k < 3:
            ev.append((t + 1, pos, tele_field(k + 1, 2.8, 1, 160)))
    return 100, ev


def _demo_m33():
    ev = [(0, 'p', tele_field(4, 4.5, 1, 160))]
    for t in range(0, 160, 20):
        ev += [(t, 'p', fx('fire_field', r=4.5)), (t, 'p', snd('fire_loop'))]
    return 165, ev


def _demo_m41():
    ev = []
    for k, t0 in enumerate((0, 34)):
        pos = ('p', 2 * k, 2)
        ev += [(t0, pos, tele_heptagram(7.5, 22)), (t0, pos, snd('frost_draw')),
               (t0 + 14, pos, card('icicle', '~ ~6 ~', '~ 0', roll=180, s0=2.2, s1=2.2, move=(0, -6, 0), life=5, dur=4)),
               (t0 + 18, pos, snd('frost_icicle')), (t0 + 22, pos, fx('frost_burst', r=7.5)),
               (t0 + 22, pos, snd('frost_burst'))]
    return 70, ev


def _demo_m42():
    spots = [(0, 0), (12, 4), (-11, 6), (5, 14), (-6, -12)]
    ev = [(0, 'a', tele_mask_wash(30.0, 48)), (0, 'a', snd('bolt_marker'))]
    for k, (x, z) in enumerate(spots):
        ev += [(0, (x, z), tele_safe_rim(k, 3.2, 48)), (0, (x, z), tele_safe_beam(k)), (50, (x, z), tele_safe_end(k))]
    ev += [(48, 'a', fx('bolt_round', r=25.0)), (48, 'a', snd('bolt_strike')), (56, 'a', snd('bolt_strike')),
           (66, 'p', tele_disc(1.6, 12, 3)), (78, 'p', fx('bolt')), (78, 'p', snd('hex_bolt'))]
    return 90, ev


def _demo_m43():
    ev = [(0, (0, -2, 9), snd('sphere_form')), (20, (0, -2, 9), snd('sphere_loop'))]
    for t in range(0, 110, 6):
        ev.append((t, (0, -2, 9), fx('ice_sphere')))
    for t in (30, 66, 102):
        ev += [(t, 'p', tele_disc(1.6, 12, 4)), (t, (0, -2, 9), snd('lance')),
               (t + 12, 'p', fx('frost_burst', r=1.6)), (t + 12, 'p', fxe('impact', 4))]
    return 120, ev


def _demo_m44():
    ev = [(0, (0, -9), fx('spark_column', h=9.0)), (0, 'a', snd('shell_spawn'))]
    for k in range(8):
        ev.append((10 + 5 * k, (0, -9, 9), card('shell', '~ ~ ~', bb='center', s0=0.4, s1=1.2,
                                                move=((k - 3.5) * 1.2, 0, 4 + (k % 3)), life=60, fade=4, dur=12)))
    ev.append((60, 'a', snd('shell_hover')))
    for k in range(8):
        t = 70 + 6 * k
        ev += [(t, 'p', tele_disc(2.4, 12, 3)), (t + 4, 'p', snd('shell_dive')), (t + 12, 'p', fx('shell_dive')),
               (t + 12, 'p', snd('shell_impact'))]
    return 130, ev


def _demo_m45():
    ev = [(0, (0, 0, 6), fx('gold_plume')), (14, 'a', snd('ice_launch'))]
    pts = [('p', 0, 0), ('p', 5, 0), ('p', -4, 5)]
    for k, (pos, tb) in enumerate(zip(pts, (68, 74, 80))):
        ev += [(26, pos, tele_starseal(4.0, tb - 26)), (tb - 4, pos, fx('shard_fall', h=8.0)), (tb - 1, pos, snd('ice_land')),
               (tb, pos, fx('frost_burst', r=4.0)), (tb, pos, snd('ice_erupt'))]
        if k < 2:
            ev.append((tb + 1, pos, tele_field(5 + k, 4.0, 4, 100)))
            for t in range(tb + 5, tb + 100, 10):
                ev.append((t, pos, fx('hail', r=4.0)))
    return 180, ev


def _demo_m46():
    ev = [(0, (0, 0, 6), fx('gold_plume')), (14, 'a', snd('ice_launch')), (26, 'p', tele_hexagram(4.8, 18)),
          (26, 'p', snd('hex_draw'))]
    for t in (44, 54, 64, 74, 98, 122):
        ev += [(t - 13, 'p', tele_disc(3.0, 13, 3)), (t - 3, 'p', fx('bolt')), (t - 3, 'p', snd('hex_bolt')),
               (t, 'p', fxe('impact', 3)), (t, 'p', snd('hex_impact'))]
    return 140, ev


def _demo_e():
    steles = [(8 * math.sin(math.radians(30 + 60 * k)), 8 * math.cos(math.radians(30 + 60 * k))) for k in range(6)]
    ev = [(0, 'a', tele_glyph_circle(9.0, 20, 92)), (0, 'a', snd('intro_drone')), (40, 'a', snd('intro_drone')),
          (80, 'a', snd('intro_drone'))]
    for t in (10, 30, 50, 70, 90):
        ev.append((t, 'a', snd('intro_thump')))
    for t, k in ((50, 0), (70, 3)):
        ev += [(t, steles[k], fx('stele_shatter')), (t, steles[k], snd('stele_break'))]
    ev += [(112, 'a', fx('prism_shatter')), (112, 'a', snd('seal_shatter')), (112, 'p', hud('flash_white')),
           (120, 'a', snd('intro_roar')), (120, (0, 2, 0), fx('gold_leaves')), (120, 'a', fx('shock_dome', r=12.0)),
           (130, 'a', fx('shock_dome', r=8.0))]
    for k in (1, 2, 4, 5):
        ev.append((131 + k, steles[k], fx('stele_shatter')))
    return 150, ev


def _demo_d():
    ev = [(0, 'a', snd('death_sting')), (34, (0, 5), fx('dust')), (34, 'a', snd('death_fall')), (66, (0, -9), fx('dust')),
          (92, (0, 5), fx('dust')), (92, 'a', snd('death_fall')), (96, 'a', fx('seal_reform')), (96, 'a', snd('death_seal')),
          (100, 'a', fx('petrify_pulse')), (120, 'a', fx('gold_motes'))]
    return 140, ev


DEMOS = {'p1': ('P1 갈라지는 봉인의 땅 (chin slam)', _demo_p1), 'p2': ('P2 바위 분쇄 충돌 (jump slam)', _demo_p2),
         'p3': ('P3 바위 용왕의 돌진 (charge)', _demo_p3), 'p4': ('P4 천동만상 (back spikes)', _demo_p4),
         'p5': ('P5 산명곡응 (foot stomp)', _demo_p5), 'p5b': ('P5b 산명곡응 – 연속 발구르기', _demo_p5b),
         'p6': ('P6 성동격서 (side feint)', _demo_p6), 'p7': ('P7 교활한 통수 (tail whip, the wedge union)', _demo_p7),
         'p7ice': ('P7 Cryo ice wall (annular wedges)', _demo_p7_ice), 'p8': ('P8 꼬리찍기 (rear tail slam)', _demo_p8),
         'p9': ('P9 잠복 돌진 (burrow charge, shortened)', _demo_p9), 't1': ('T1 파멸의 산사태 (landslide)', _demo_t1),
         't2': ('T2 absorb 1 + roar', _demo_t2), 't3': ('T3 absorb 2 + roar', _demo_t3),
         'b3': ('B3 phase-3 burrow (shortened)', _demo_b3), 'm31': ('31 격류 범람 (orb ribbons)', _demo_m31),
         'm32': ('32 운석 낙하 (meteors)', _demo_m32), 'm33': ('33 화염 잠식 (fire field)', _demo_m33),
         'm41': ('41 서리 습격 (frost circles)', _demo_m41), 'm42': ('42 벼락 습격 (lightning round)', _demo_m42),
         'm43': ('43 쏟아지는 천화 (ice sphere)', _demo_m43), 'm44': ('44 번개의 가루 (shells)', _demo_m44),
         'm45': ('45 천동만상 – 얼음 가시', _demo_m45), 'm46': ('46 천동만상 – 번개 가시', _demo_m46),
         'e': ('E intro', _demo_e), 'd': ('D death', _demo_d)}


def demo_events(name):
    length, ev = DEMOS[name][1]()
    return length, sorted(ev, key=lambda e: e[0])


def demo_where(where):
    """execute sub-commands of a demo event (run as the demo anchor marker)"""
    if where == 'a':
        return 'at @s rotated as @s rotated ~ 0'
    if where == 'p':
        return 'at @p[tag=player] rotated as @s rotated ~ 0'
    if where[0] == 'p':
        _p, x, z = where
        return f'at @p[tag=player] rotated as @s rotated ~ 0 positioned ^{num(float(x), 2)} ^ ^{num(float(z), 2)}'
    x, z = where[0], where[1]
    y = where[2] if len(where) > 2 else 0
    yaw = where[3] if len(where) > 3 else 0
    rot = f' rotated ~{ang(yaw)} 0' if yaw else ''
    return (f'at @s rotated as @s rotated ~ 0 positioned ^{num(float(x), 2)} ^{num(float(y), 2)} ^{num(float(z), 2)}'
            f'{rot}')


def tests(W):
    t = ['# Every fx kind in rows in front of the executor (3 s each):',
         '# /execute as @p at @s rotated ~ 0 run function rlk:mboss/azhdaha/fx/test/kinds']
    for i, kind in enumerate(FX_KINDS):
        row, colm = divmod(i, 8)
        x = 5.25 - 1.5 * colm
        z = 4 + 2.4 * row
        plane = KINDS[kind][0]
        if plane in ('flat', 'band'):
            t.append(card(kind, f'^{num(x)} ^0.05 ^{num(z)}', '~ 0', s0=0.3, s1=1.4, life=60, fade=10))
        else:
            t.append(card(kind, f'^{num(x)} ^1.2 ^{num(z)}', '~180 0', s0=0.3, s1=1.2, life=60, fade=10))
    W.w('test/kinds', t)
    tl = ['# One telegraph of each shape (tell 40 t) around the executor: discs in every el palette, the nd looks,',
          '# a ring, sectors, a wedge union, lines, a flank strip, a front, a moving line turning for 84 t, the seals:',
          '# /execute as @p at @s rotated ~ 0 run function rlk:mboss/azhdaha/fx/test/tele']
    for el in range(0, 6):
        tl.append(f'execute positioned ^{num(7.5 - 3 * el)} ^ ^5 run ' + tele_disc(1.3, 40, el))
    tl += ['execute positioned ^6 ^ ^10 run ' + tele_disc(2.0, 40, 5, 1),
           'execute positioned ^2 ^ ^10 run ' + tele_disc(2.0, 40, 5, 2),
           'execute positioned ^-3 ^ ^10 run ' + tele_ring(1.5, 3.5, 40, 2),
           'execute positioned ^-9 ^ ^9 run ' + tele_sector(4.5, 30, 40, 1),
           'execute positioned ^9 ^ ^14 run ' + tele_sector(4.0, 90, 40, 3),
           'execute positioned ^ ^ ^14 run ' + tele_line(6.0, 2.0, 40, 4, 1),
           'execute positioned ^-6 ^ ^14 rotated ~90 0 run ' + tele_lane_side(6.0, 3.0, 40, 5),
           'execute positioned ^ ^ ^24 run ' + tele_wave(0, 2.5, 9.0, 2.0, 40, 17, 5, 2),
           'execute positioned ^-8 ^ ^20 run ' + tele_mline(0, 5.8, 0.8, 24, 3, hold=60, back=-2.8),
           'execute positioned ^8 ^ ^22 run ' + tele_heptagram(3.5, 40),
           'execute positioned ^14 ^ ^14 run ' + tele_hexagram(3.0, 40),
           'execute positioned ^-14 ^ ^14 run ' + tele_seal8(3.0, 40),
           'execute positioned ^-14 ^ ^22 run ' + tele_starseal(3.0, 40)]
    tl += ['execute positioned ^12 ^ ^28 run ' + w for w in _wedges(9, -60, 55, 0, 6.0, 40, 1, 5)]
    tl += ['scoreboard players set #akMT mb 0', f'schedule function {FN}test/e/mturn 1t replace']
    W.w('test/tele', tl)
    W.w('test/e/mturn', ['# Turn the test moving line 5 degrees a tick for 84 t.',
                         'scoreboard players add #akMT mb 1', tele_mline_turn(0, 5),
                         f'execute if score #akMT mb matches ..83 run schedule function {FN}test/e/mturn 1t replace'])
    W.w('test/sounds', ['# Click through the sound recipes (tellraw list).',
                        'tellraw @s [{"text":"야타용왕 sounds: ","color":"#F2B53A"}' +
                        ''.join(f',{{"text":"[{n}] ","color":"#F5E0A0","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}"}}}}' for n in SOUNDS) +
                        ''.join(f',{{"text":"[{n}/{e}] ","color":"#C8D8F0","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}/{e}"}}}}'
                                for n, (_r, mem) in SFAM.items() for e in mem) + ']'])
    W.w('test/hud', ['# The banners, the jump cue and a flash in sequence (run during a fight to see them over the HUD).',
                     hude('banner_tr', 2), hud('cue_jump')])
    W.w('test/presets', ['# Click through the presets (tellraw list; family presets in Geo, macro presets with test values).',
                         'tellraw @s [{"text":"야타용왕 fx: ","color":"#F2B53A"}' +
                         ''.join(f',{{"text":"[{n}] ","color":"#F5E0A0","click_event":{{"action":"run_command",'
                                 f'"command":"/execute at @s rotated ~ 0 positioned ^ ^ ^6 run {_test_call(n)}"}}}}'
                                 for n in list(PRESETS) + list(EPRESETS)) + ']'])
    pr = ['# Every prop look on a row of temporary item_displays in front of the executor (removed after 10 s by the',
          '# kit ager: they carry the card tags):',
          '# /execute as @p at @s rotated ~ 0 run function rlk:mboss/azhdaha/fx/test/props']
    names = list(PROPS) + [f'{n}/{e}' for n, (_d, _r, mem, _b, _s) in PFAM.items() for e in mem]
    for i, n in enumerate(names):
        row, colm = divmod(i, 8)
        at = f'positioned ^{num(7.0 - 2.0 * colm)} ^ ^{num(5 + 3.0 * row)}'
        pr += [f'execute {at} run ' + card('glow', '~ ~ ~', bb='fixed', s0=1.0, s1=1.0, life=200, fade=0, col=WHITE),
               f'execute {at} as @e[type=minecraft:item_display,tag={TAG},sort=nearest,limit=1] run function {FN}prop/{n}']
    W.w('test/props', pr)
    # demos
    W.w('test/pair', ['# Set the demo elements: {leg:<1 Pyro | 2 Hydro>, tail:<3 Electro | 4 Cryo>, ph:<1..3>} (ground = Geo',
                      '# in phase 1, the leg element after).',
                      f'$data modify storage {STO} dm set value {{l:$(leg),t:$(tail),g:$(leg)}}',
                      '$scoreboard players set #akA mb $(ph)',
                      f'execute if score #akA mb matches ..1 run data modify storage {STO} dm.g set value 5'])
    W.w('test/stage', ['# Spawn the demo stand-in anchor (a vanilla marker tagged rlk_ak_demo) 12 b in front of the executor,',
                       '# facing it. /execute as @p at @s rotated ~ 0 run function rlk:mboss/azhdaha/fx/test/stage, then',
                       '# test/demo/<name>. test/stop removes it.',
                       f'function {FN}test/stop',
                       'execute positioned ^ ^ ^12 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_ak_demo","rlk_room","rlk_mb_aux"]}',
                       'execute as @e[type=minecraft:marker,tag=rlk_ak_demo,limit=1] at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0',
                       f'execute unless data storage {STO} dm.g run data modify storage {STO} dm set value {{l:2,t:3,g:5}}',
                       'scoreboard players set #akDemo mb 0', 'scoreboard players set #akDT mb 0',
                       f'schedule function {FN}test/e/tick 1t replace'])
    W.w('test/stop', ['# Remove the demo anchor and stop the demo ticker.',
                      'kill @e[type=minecraft:marker,tag=rlk_ak_demo]', f'schedule clear {FN}test/e/tick',
                      'scoreboard players set #akDemo mb 0'])
    tick = ['# Demo ticker (scheduled): the running demo\'s events as the anchor.',
            'execute unless entity @e[type=minecraft:marker,tag=rlk_ak_demo,limit=1] run return 0',
            'execute if score #akDemo mb matches 1.. run scoreboard players add #akDT mb 1']
    for k, name in enumerate(DEMOS, 1):
        length, ev = demo_events(name)
        macro = any('$(' in l for _t, _w, l in ev)
        tick.append(f'execute if score #akDemo mb matches {k} as @e[type=minecraft:marker,tag=rlk_ak_demo,limit=1] '
                    f'run function {FN}test/demo/e/{name}' + (f' with storage {STO} dm' if macro else ''))
        tick.append(f'execute if score #akDemo mb matches {k} if score #akDT mb matches {length}.. run '
                    'scoreboard players set #akDemo mb 0')
    tick.append(f'schedule function {FN}test/e/tick 1t replace')
    W.w('test/e/tick', tick)
    for k, name in enumerate(DEMOS, 1):
        desc = DEMOS[name][0]
        length, ev = demo_events(name)
        W.w(f'test/demo/{name}', [f'# Demo "{name}": {desc} ({length} t) on the stand-in anchor; needs test/stage first',
                                  '# (made here if missing). Elements from test/pair.',
                                  'execute unless entity @e[type=minecraft:marker,tag=rlk_ak_demo,limit=1] run '
                                  f'function {FN}test/stage',
                                  f'scoreboard players set #akDemo mb {k}', 'scoreboard players set #akDT mb -1'])
        lines = [f'# Demo "{name}" events (as the anchor; #akDT = the demo tick).']
        for tk, where, line in ev:
            lines.append(mac(f'execute if score #akDT mb matches {tk} {demo_where(where)} run {line}'))
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
    removed = W.flush()
    return len(W.files), removed


def manifest():
    fam_cards = {n: {str(el): preset_cards(n, el) for el in range(1, 6)} for n in EPRESETS}
    return {
        'generator': 'tools/build_mboss_az_fx.py',
        'api': 'scratchpad az/az_fx_api.md (tools-side copy: tools/az_fx_api.md)',
        'functions': FN, 'item_models': NS_TEX, 'font': FONT, 'storage': STO,
        'owned': {'dirs': [f'{FDIR}/{d}' for d in OWNED_DIRS], 'files': [f'{FDIR}/{f}.mcfunction' for f in OWNED_FILES],
                  'rp': [f'assets/rlk/textures/{TEXDIR}', f'assets/rlk/models/item/{TEXDIR}', f'assets/rlk/items/{TEXDIR}',
                         f'assets/rlk/font/{FONT_NAME}.json', f'assets/rlk/textures/font/{FONT_NAME}']},
        'caps': {'fx': CAP, 'telegraph': TCAP, 'telegraph_skip_from': TCAP - TSKIP, 'field': FCAP, 'ambient_skip_from': SOFT,
                 'trail_skip_from': TSOFT},
        'objectives': list(OBJECTIVES),
        'fake_players': '#ak* (objective mb)',
        'tags': [TAG, f'{TAG}_t', f'{TAG}_fp', f'{TAG}_f<k>', f'{TAG}_ml<k>', f'{TAG}_ml<k>c', f'{TAG}_wv<k>',
                 f'{TAG}_sr<k>', f'{TAG}_sb', f'{TAG}_g', 'rlk_ak_demo'],
        'kinds': {k: {'plane': v[0], 'px': list(v[1]), 'extent': list(v[2]), 'tint': 'neutral' if v[6] else 'painted',
                      'desc': v[7]} for k, v in KINDS.items()},
        'atlas_px': atlas_px(),
        'telegraphs': {k: list(v) for k, v in TELE_ARGS.items()},
        'telegraph_colours': {str(k): [f'#{c:06X}' for c in v] for k, v in TELE_COL.items()},
        'undodgeable_rim': f'#{ND_RIM:06X}', 'safe_rim': f'#{SAFE_RIM:06X}',
        'presets': {k: {'args': v[1], 'doc': v[0], 'cards': preset_cards(k), 'ambient': k in AMBIENT}
                    for k, v in PRESETS.items()},
        'epresets': {k: {'args': v[1], 'doc': v[0], 'els': [1, 5], 'cards': fam_cards[k], 'ambient': k in AMBIENT}
                     for k, v in EPRESETS.items()},
        'props': {**{k: v[0] for k, v in PROPS.items()}, **{k: v[0] for k, v in PFAM.items()},
                  **{f'{k}/{e}': f'{v[0]} (element {e})' for k, v in PFAM.items() for e in v[2]}},
        'prop_families': {k: list(v[1]) for k, v in PFAM.items()},
        'item_models_public': {'gate_icon': NS_TEX + 'gate_icon', **{f'glyph_{EL_KEYS[e]}': NS_TEX + f'glyph_{EL_KEYS[e]}'
                                                                  for e in range(1, 6)}},
        'sounds': {**{k: v[0] for k, v in SOUNDS.items()},
                   **{f'{k}/{e}': d for k, (_r, mem) in SFAM.items() for e, (d, _l) in mem.items()}},
        'sound_families': {k: list(v[0]) for k, v in SFAM.items()},
        'hud': {'functions': list(HUD_FUNCS), 'families': {k: [1, 4] for k in HFAM}},
        'glyphs': {k: f'U+{v[0]:04X}' for k, v in GLYPHS.items()},
        'spaces': {f'U+{k:04X}': v for k, v in SPACES.items()},
        'demos': {k: {'desc': v[0], 'len': demo_events(k)[0]} for k, v in DEMOS.items()},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--resourcepack', help='unpacked resource pack root (assets/...)')
    ap.add_argument('--datapack', default=str(HERE.parent), help='datapack root (data/...)')
    ap.add_argument('--skip-rp', action='store_true', help='only write the datapack functions')
    a = ap.parse_args()
    check_sprites()
    n, removed = build_datapack(a.datapack)
    (HERE / 'mboss_az_fx_manifest.json').write_text(json.dumps(manifest(), ensure_ascii=False, indent=1) + '\n',
                                                     encoding='utf-8')
    n_sounds = len(SOUNDS) + sum(len(m) for _r, m in SFAM.values())
    msg = (f'야타용왕 fx kit: {n} functions ({removed} stale removed), {len(PRESETS)} presets + {len(EPRESETS)} element '
           f'families, {n_sounds} sounds')
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error('--resourcepack is required unless --skip-rp')
        k, px, g = build_resourcepack(a.resourcepack)
        msg += f', {k} sprites ({px / 1e6:.2f} M px of atlas), {g} glyphs in {FONT}'
    print(msg)


if __name__ == '__main__':
    main()
