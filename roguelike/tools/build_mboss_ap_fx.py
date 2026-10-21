#!/usr/bin/env python3
"""FX / audio / HUD kit of the chapter-3 boss 아펩의 오아시스 파수꾼 (Guardian of Apep's Oasis).

The field generator kit (tools/build_mboss_fg_fx.py, scratchpad mb3/fg_fx_api.md) copied and renamed, with the
Azhdaha kit's day-0 conventions (scratchpad az/contract/fx.md) and the call list of scratchpad ap/ap_fx_api.md §0
(frozen names and arguments). Pattern, organism and revival authors call it through api.K; nothing here decides
gameplay (hits, hazards, projectiles, the Heart progress and every timing stay in the module core). Parts, all
regenerated on every run:

  1. The tinted card engine (fg kit, with its first-tick fix): painted sprites on short-lived item_display cards;
     planes face, flat, cross, band, box. Four counted pools: fx cards (cap CAP), attack telegraphs (TCAP, calls
     skipped from TCAP - TSKIP on or when the shape would overflow), the phase-2 dressing pool (DCAP, long-lived,
     never aged) and the 종말의 여파 flood pool (FLCAP). Ambient presets are skipped from SOFT live fx cards on.
  2. Ground telegraphs: disc, sector (any integer half-angle, drawn within 1 degree), wedge (stacked swept wedges),
     line, crack (the 생명의 손 strips), wave (ids), mask_wash, safe_rim, mring (the moving target ring), wall_spot;
     palettes el 7 Dendro / 20 gold / 22 target / 23 olive / 24 field and the nd undodgeable looks.
  3. The dressing pool (fx/dress/*: the Heart's gold swirl, the pulsing ley-line strips, redraw after /reload).
  4. Vanilla sound recipes fx/snd/<name> with the per-layer minimum volume rule of mboss_lib.
  5. The HUD: font rlk:mboss_ap (U+E900-E9FF): badges, the title glyphs, the dome glyph, full-screen flats, the Heart
     bar cells (the FN-24 fallback); title / banner / white-out / flash functions (the kit owns no boss-bar line).
  6. Presets fx/p/<name>, prop looks fx/prop/<name>, the in-game test functions and one demo per plan §8 item on a
     vanilla stand-in anchor (no rig calls).

Generic textures are not painted again (plan §5.4: <= 0.35 M new px): the telegraph rims / fills / rings / lane bars
and the neutral glow / glint / mote / streak / ripple / spark / smoke kinds are the field generator kit's sprites,
referenced from the Apep item models (rlk:mboss/ap_kit/<kind> -> texture rlk:mboss/fg_kit/<name>); the build fails
when a referenced texture is missing from the resource pack or its size changed.

Outputs (owned; stale files in these places are removed):
  resource pack  assets/rlk/textures/mboss/ap_kit/<kind>.png      painted sprites (stdlib painter)
                 assets/rlk/models/item/mboss/ap_kit/<kind>.json    card models (tintindex 0)
                 assets/rlk/items/mboss/ap_kit/<kind>.json          item definitions, custom_model_data tint
                 assets/minecraft/atlases/items.json                adds rlk:mboss/ap_kit/* (merges)
                 assets/rlk/font/mboss_ap.json + textures/font/mboss_ap/*.png
  datapack       data/rlk/function/boss/apep/fx/{card,cardx,look,clear,uninstall}
                 data/rlk/function/boss/apep/fx/{e,p,tele,dress,snd,hud,prop,test}/**
                 (every other file under boss/apep/fx/ belongs to the module core and is left alone)
  manifest       tools/mboss_ap_fx_manifest.json

No hook in a shared file: the engine ages its cards from a self-rescheduling function (schedule ... 1t replace).
Cards carry rlk_room + rlk_mb_aux. The module wires uninstall / clear / pause / death_start (ap_fx_api.md §0.12).

Run: python3 tools/build_mboss_ap_fx.py --resourcepack <unpacked RP> [--datapack <dp root>]   (or --skip-rp)
API: scratchpad ap/ap_fx_api.md. Other generators `import build_mboss_ap_fx as K` (no files are written on import).
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
import mboss_ap_fx_paint as P  # noqa: E402
import mboss_lib as L  # noqa: E402

ROOT = L.fn_root_of('apep')            # the module's function root (registry fn: boss/apep, user 10-22)
FN = f'rlk:{ROOT}/fx/'
FDIR = f'data/rlk/function/{ROOT}/fx'
NS_TEX = 'rlk:mboss/ap_kit/'           # textures, models (rlk:item/mboss/ap_kit/*) and item ids
TEXDIR = 'mboss/ap_kit'
FG_TEX = 'rlk:mboss/fg_kit/'           # the field generator kit's sprites (referenced, never written)
FG_TEXDIR = 'mboss/fg_kit'
FONT = 'rlk:mboss_ap'
FONT_NAME = 'mboss_ap'
STO = 'rlk:apkit'
CAP = 64            # live fx cards; further fx spawns are skipped until some expire
TCAP = 40           # live attack-telegraph cards (counted apart, so busy fx never hide a telegraph)
TSKIP = 6           # telegraph calls are skipped from TCAP - TSKIP on, or when the shape would pass TCAP
SOFT = 40           # ambient presets are skipped from SOFT live fx cards on (room for the hits' fx)
DCAP = 16           # the dressing pool (fx/dress/*), never counted against the others
FLCAP = 48          # the flood pool (p/flood), never counted against the others
ATLAS_BUDGET = 350_000          # new px of the items atlas (plan §5.4)
OWNED_DIRS = ('e', 'p', 'tele', 'dress', 'snd', 'hud', 'prop', 'test')
OWNED_FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')
OBJECTIVES = ('wkS', 'wkG', 'wkH', 'wkK', 'wkD')
TAG = 'rlk_wk'
WALL_H = 0.5                     # band kind: wall height at scale 1
BOX = (0.5, 0.135, 0.2)          # box kind half extents
DOME_TAG = 'rlk_mb_ap_dome'      # the module's dome markers (the flood skips their cells)
DOME_SKIP = 7.5                  # a flood tile is skipped when a dome marker is within this distance of its centre


def rgb(h):
    return int(h[1:], 16)


# ----------------------------------------------------------------------------- colours (RGB ints for tints)
WHITE = 0xFFFFFF
DENDRO = rgb('#A6D45A')
DENDRO_DEEP = rgb('#4E8A1E')
DENDRO_PALE = rgb('#F1FFD2')
LIME = rgb('#B6E35A')
LIME_PALE = rgb('#E0F996')
LIME_RIM = rgb('#A2CA6C')
LEAF_PALE = rgb('#D8F2B0')
GHOST = rgb('#E6EED8')
BLACK_LEAF = rgb('#2A2A10')
OLIVE = rgb('#3F3C15')
GOLD = rgb('#EBC55A')
GOLD_DEEP = rgb('#B07A1E')
GOLD_PALE = rgb('#FFF4C8')
GOLD_WHITE = rgb('#F0F2BB')          # the P1 burst flash (v1 #F0F2BB / #FAFCDF)
ORANGE_GOLD = rgb('#E8A53A')
YELLOW_BEAM = rgb('#FDFBBD')         # Q3 / Q5 light columns
SHELL = rgb('#E7F99F')
FLOOD = rgb('#FBFAA4')
TEAL_FOAM = rgb('#CDEFE4')
RED_EMBER = rgb('#D2442A')
BANNER_RED = '#C36E5A'
ND_RIM = rgb(BANNER_RED)              # the undodgeable rim (nd 1 / 2)
CRESC = (rgb('#A4D6AC'), rgb('#BFE682'), rgb('#EBF898'))     # Q4 crescents
HELIX = (rgb('#E7F99F'), rgb('#8BCAAA'))
TETHER = rgb('#D4E784')

# telegraph tints per el (rim, fill, flash); anything else draws Dendro (ap_fx_api.md §0.2)
TELE_COL = {7: (rgb('#4E8A1E'), rgb('#A6D45A'), rgb('#F1FFD2')),
            20: (rgb('#B07A1E'), rgb('#EBC55A'), rgb('#FFF4C8')),
            22: (rgb('#6FA85A'), rgb('#C1E6A8'), rgb('#F5FFF0')),
            23: (rgb('#FCF9ED'), rgb('#B9B46A'), rgb('#FFFFF4')),
            24: (rgb('#9DBA2E'), rgb('#DCEB72'), rgb('#FFFFD8'))}
TELE_DEFAULT = 7
SAFE_DIM = rgb('#B9C9A8')             # the safe rim before its dome forms (white = formed)
WALL_DIM = rgb('#C6CDB0')

# ----------------------------------------------------------------------------- kinds
# name -> (plane, (w, h) px, card extent in blocks at scale 1 (a0, a1, b0, b1), painter box, painter, supersampling,
#          neutral?, description). Planes as the fg kit: face, flat, cross, band, box.
SQ = (-0.5, 0.5, -0.5, 0.5)
UNIT = (-1, 1, -1, 1)
BX = (-1, 1, -1, 1)
FOOT = (-0.5, 0.5, 0.0, 1.0)
LANE = (-0.5, 0.5, 0.0, 1.0)
NARROW = (-0.25, 0.25, -0.5, 0.5)
KINDS = {
    # leaves, blades, pools
    'leaf':         ('face', (32, 32), SQ, SQ, P.paint_leaf, 3, True, 'neutral leaf (tint pale green, black #2A2A10, gold)'),
    'leaf_blade':   ('face', (32, 64), NARROW, NARROW, P.paint_leaf_blade, 2, True, 'neutral glowing leaf blade (rosette petals, sweep / skim blades, spikes)'),
    'blade':        ('face', (32, 64), NARROW, NARROW, P.paint_blade, 2, True, 'neutral faceted crystal blade (white-gold burst blades)'),
    'pool':         ('flat', (64, 64), SQ, SQ, P.paint_pool, 2, False, 'dark olive leaf pool decal (the burrow pool)'),
    'pad':          ('flat', (64, 64), SQ, SQ, P.paint_pad, 2, False, 'translucent green leaf pad (the underground trail)'),
    'mound':        ('face', (64, 32), (-0.5, 0.5, 0.0, 0.5), (-0.5, 0.5, 0.0, 0.5), P.paint_mound, 2, False, 'lime leaf mound with white spray, foot at b 0'),
    'root_chunk':   ('face', (32, 32), SQ, SQ, P.paint_root_chunk, 3, False, 'brown root chunk with gold glints'),
    # props / projectiles
    'thorn_wheel':  ('face', (96, 96), SQ, BX, P.paint_thorn_wheel, 2, False, 'pale-green carpet thorn wheel'),
    'thorn_wheel_homing': ('face', (96, 96), SQ, BX, P.paint_thorn_wheel_hm, 2, False, 'gold-orange homing thorn wheel with a red 4-point flare'),
    'seed_bolt':    ('face', (32, 32), SQ, BX, P.paint_seed_bolt, 3, False, 'lime seed bolt (O2)'),
    'seed_orb':     ('face', (64, 64), SQ, BX, P.paint_seed_orb, 2, False, 'yellow-green seed orb with a spiral glyph (Q5)'),
    'charge_ball':  ('face', (64, 64), SQ, BX, P.paint_charge_ball, 2, False, 'Q3 light ball (#FDFBBD core, white-green halo)'),
    # light
    'beam':         ('cross', (32, 128), FOOT, FOOT, P.paint_beam, 2, True, 'neutral light column, foot at b 0, 1 b tall at scale 1'),
    'dome_flare':   ('face', (64, 32), (-0.5, 0.5, 0.0, 0.5), (-0.5, 0.5, 0.0, 0.5), P.paint_dome_flare, 2, True, 'neutral half-dome flare, pivot at the base'),
    'crescent':     ('face', (128, 32), (-0.5, 0.5, -0.125, 0.125), (-0.5, 0.5, -0.125, 0.125), P.paint_crescent, 2, True, 'neutral crescent trail segment (bows toward +b)'),
    'rib':          ('face', (64, 64), SQ, SQ, P.paint_rib, 2, False, 'pale rib afterimage (P1 sweep)'),
    'spiral':       ('face', (64, 64), SQ, SQ, P.paint_spiral, 2, True, 'neutral spiral wisp'),
    'splash':       ('face', (64, 64), FOOT, FOOT, P.paint_splash, 2, True, 'near-white water splash crown, foot at b 0'),
    'shard':        ('face', (32, 64), NARROW, NARROW, P.paint_shard, 2, True, 'neutral glass shard (dome pop)'),
    'wisp':         ('face', (32, 64), NARROW, NARROW, P.paint_wisp, 2, False, 'black twisted wisp (수호 death)'),
    'lightning':    ('face', (32, 128), (-0.25, 0.25, 0.0, 1.0), (-0.25, 0.25, 0.0, 1.0), P.paint_lightning, 2, True, 'neutral lightning ribbon, root at b 0'),
    # arena props (theme records, the entrance)
    'water_sheet':  ('flat', (128, 128), SQ, SQ, P.paint_water_tile, 1, False, 'the lake water sheet tile (1 b at scale 1; records use 14)'),
    'lily_pad':     ('flat', (64, 64), SQ, SQ, P.paint_lily_pad, 2, False, 'lily pad (1 b at scale 1)'),
    'bell_flower':  ('cross', (32, 64), (-0.25, 0.25, 0.0, 1.0), (-0.25, 0.25, 0.0, 1.0), P.paint_bell_flower, 2, False, 'yellow bell flowers, foot at b 0'),
    'bulb_flower':  ('cross', (32, 64), (-0.25, 0.25, 0.0, 1.0), (-0.25, 0.25, 0.0, 1.0), P.paint_bulb_flower, 2, False, 'glowing bulb flower, foot at b 0'),
    'bank_crystal': ('cross', (64, 128), FOOT, FOOT, P.paint_bank_crystal, 2, False, 'gold crystal spikes, foot at b 0'),
    'gate_crystal': ('cross', (64, 128), (-0.75, 0.75, 0.0, 1.5), (-0.5, 0.5, 0.0, 1.0), P.paint_gate_crystal, 2, False, 'gold-green gate crystal, 1.5 b tall at scale 1'),
    # telegraph decals (unit radius / unit length: the scale is the size in blocks)
    't_jump':       ('flat', (32, 32), SQ, (-1, 1, -1, 1), P.paint_t_jump, 3, True, 'jump chevron (nd 2)'),
    't_crack':      ('flat', (32, 128), LANE, LANE, P.paint_t_crack, 2, False, 'P2 white-gold crack line (unit length)'),
    't_wash':       ('flat', (96, 96), UNIT, BX, P.paint_t_wash, 2, True, '종말의 여파 field wash (unit radius)'),
    't_safe':       ('flat', (128, 128), UNIT, BX, P.paint_t_safe, 2, False, 'dome footprint rim (unit radius)'),
    't_dome':       ('flat', (48, 48), UNIT, BX, P.paint_t_dome, 2, False, 'dome glyph decal'),
    't_target':     ('flat', (64, 64), UNIT, BX, P.paint_t_target, 2, True, 'Q3 target ring disc (unit radius)'),
    't_wall':       ('flat', (64, 32), (-0.7, 0.7, -0.25, 0.25), (-0.7, 0.7, -0.25, 0.25), P.paint_t_wall, 2, False, '둥지 blade footprint 1.4 x 0.5 b'),
    # dressing and flood pools
    'd_swirl':      ('flat', (128, 128), UNIT, BX, P.paint_d_swirl, 2, False, 'the Heart\'s gold swirl ring (unit radius)'),
    'd_ley':        ('flat', (32, 128), LANE, LANE, P.paint_d_ley, 2, False, '지맥 이상 ley-line crack strip (unit length)'),
    'fl_tile':      ('flat', (32, 32), SQ, SQ, P.paint_fl_tile, 2, False, '종말의 여파 flood tile (seamless)'),
}
for _w in P.PIECES:
    _hw = P.piece_half_width(_w)
    _fx = max(16, math.ceil(2 * _hw * 64 / 16) * 16)
    _ax = _fx / 128
    KINDS[f't_pf{_w}'] = ('flat', (_fx, 64), (-_ax, _ax, 0.0, 1.0), (-_ax, _ax, 0.0, 1.0), P.make_t_pf(_w), 2, True,
                          f'sector / wedge fill piece, {_w} deg')
    if _w in P.PIECES_NARROW:
        _rx = max(16, math.ceil(2 * _hw * 128 / 16) * 16)
        _bx = _rx / 256
        KINDS[f't_pa{_w}'] = ('flat', (_rx, 32), (-_bx, _bx, 0.75, 1.0), (-_bx, _bx, 0.75, 1.0), P.make_t_pa(_w), 2, True,
                              f'sector / wedge rim piece, {_w} deg')
    _sx = max(16, math.ceil(2 * _hw * 64 / 16) * 16)
    _cx = _sx / 128
    _y0 = 0.5 if _w <= 32 else 0.375
    _sy = 32 if _w <= 32 else 48
    KINDS[f't_pas{_w}'] = ('flat', (_sx, _sy), (-_cx, _cx, _y0, 1.0), (-_cx, _cx, _y0, 1.0), P.make_t_pa(_w, True), 2,
                           True, f'thick sector / wedge rim piece (r <= 3.5), {_w} deg')
    KINDS[f't_pe{_w}'] = ('flat', (_sx, 64), (-_cx, _cx, 0.0, 1.0), (-_cx, _cx, 0.0, 1.0), P.make_t_pa(_w, True, True), 2,
                          True, f'thick one-piece sector rim with both radial edges (r <= 3.5), {_w} deg')

# Generic kinds referenced from the fg kit (the Apep item model points at the fg texture; no px of our own).
REF = {
    'glow': 'glow', 'glint': 'glint', 'mote': 'mote', 'streak': 'streak', 'ripple': 'ripple', 'spark': 'spark',
    'smoke': 'smoke', 't_rim': 't_rim', 't_rim_s': 't_rim_s', 't_ring': 't_ring', 't_fill': 't_fill', 't_bar': 't_bar',
    't_lane': 't_lane',
}
REF_NEUTRAL = ('glow', 'glint', 'mote', 'streak', 'ripple', 't_rim', 't_rim_s', 't_ring', 't_fill', 't_bar', 't_lane')
# Own sprites drawn with another plane (same texture, no extra px): the carpet wheels as crossed quads.
ALIAS = {'thorn_wheel_x': ('thorn_wheel', 'cross', 'the carpet thorn wheel as two crossed quads (reads from every side)')}
ALL_KINDS = list(KINDS) + list(REF) + list(ALIAS)
TELE_KINDS = [k for k in ALL_KINDS if k.startswith('t_')]
POOL_KINDS = ['d_swirl', 'd_ley', 'fl_tile']
FX_KINDS = [k for k in ALL_KINDS if k not in TELE_KINDS and k not in POOL_KINDS]
SPIN_Y = ('flat', 'cross', 'band', 'box')       # planes that spin about local y


def _fg():
    """the field generator kit's generator (its KINDS table: planes, extents and sizes of the referenced sprites)"""
    import build_mboss_fg_fx as FG
    return FG


def kind_info(kind):
    """(plane, (w, h), extent, neutral, texture id, description) of an own or referenced kind"""
    if kind in KINDS:
        v = KINDS[kind]
        return v[0], v[1], v[2], v[6], NS_TEX + kind, v[7]
    if kind in ALIAS:
        src, plane, desc = ALIAS[kind]
        v = KINDS[src]
        return plane, v[1], v[2], v[6], NS_TEX + src, desc
    fgk = _fg().KINDS[REF[kind]]
    return fgk[0], fgk[1], fgk[2], kind in REF_NEUTRAL, FG_TEX + REF[kind], f'{fgk[7]} (fg kit sprite)'


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


def png_size(path):
    data = Path(path).read_bytes()[:24]
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    return struct.unpack('>II', data[16:24])


def r4(v):
    return round(v, 4)


def model_json(kind):
    """Zero-thickness double-sided quads (or a cuboid) with tintindex 0 (fg kit convention: display-local p is
    written at model m = (8 - 16 px, 8 + 16 py, 8 - 16 pz); card +a = local -x = model +x)."""
    plane, _s, (a0, a1, b0, b1), _n, tex, _d = kind_info(kind)
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1

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
    """new px this kit adds to the items atlas (its own painted kinds; the fg references add nothing)"""
    return sum(v[1][0] * v[1][1] for v in KINDS.values())


def check_refs(rp):
    """every referenced fg sprite exists in the resource pack with the size the fg kit declares"""
    rp = Path(rp)
    FG = _fg()
    bad = []
    for kind, name in REF.items():
        assert name in FG.KINDS, f'{kind}: the fg kit has no kind {name}'
        p = rp / f'assets/rlk/textures/{FG_TEXDIR}/{name}.png'
        if not p.exists():
            bad.append(f'{kind} -> {p} is missing (build the field generator kit first)')
        elif png_size(p) != tuple(FG.KINDS[name][1]):
            bad.append(f'{kind} -> {p} is {png_size(p)}, the fg kit declares {FG.KINDS[name][1]}')
    atlas = rp / 'assets/minecraft/atlases/items.json'
    srcs = json.loads(atlas.read_text(encoding='utf-8'))['sources'] if atlas.exists() else []
    have = {s.get('resource') for s in srcs}
    for kind, name in REF.items():
        if FG_TEX + name not in have:
            bad.append(f'{kind} -> {FG_TEX}{name} is not in the items atlas')
    if bad:
        raise SystemExit('fg kit sprite references broken:\n  ' + '\n  '.join(bad))
    return len(REF)


# ----------------------------------------------------------------------------- HUD font
CP_LO, CP_HI = 0xE900, 0xE9FF
# name -> (codepoint, painter: analytic fn (x right, y up, -1..1) | ('pix', fn, arg) | flat (hex, alpha),
#          texture px (w, h), height, ascent)
GLYPHS = {
    'apep':      (0xE900, P.glyph_apep, (36, 36), 9, 8),
    'guard':     (0xE901, P.make_glyph_diamond('#FFFFFF'), (24, 24), 7, 7),
    'nest':      (0xE902, P.make_glyph_diamond('#FFFFFF'), (24, 24), 7, 7),
    'nurt':      (0xE903, P.make_glyph_diamond('#FFFFFF'), (24, 24), 7, 7),
    'pred':      (0xE904, P.make_glyph_diamond('#FFFFFF'), (24, 24), 7, 7),
    'destr':     (0xE905, P.make_glyph_diamond('#FFFFFF'), (24, 24), 7, 7),
    'warn':      (0xE906, P.glyph_warn, (36, 36), 9, 8),
    'fail_s':    (0xE907, P.glyph_fail_small, (36, 36), 9, 8),
    't_heart':   (0xE910, P.glyph_t_heart, (48, 48), 12, 10),
    't_warn':    (0xE911, P.glyph_t_warn, (48, 48), 12, 10),
    't_fail':    (0xE912, P.glyph_t_fail, (48, 48), 12, 10),
    't_success': (0xE913, P.glyph_t_success, (48, 48), 12, 10),
    'dome':      (0xE914, P.glyph_dome, (36, 36), 9, 8),
    'fl_white':  (0xE920, ('#FFFFFF', 1.0), (16, 9), 144, 69),
    'fl_white9': (0xE921, ('#FFFFFF', 0.9), (16, 9), 144, 69),
    'fl_green':  (0xE922, ('#B6E35A', 0.5), (16, 9), 144, 69),
    'fl_edge':   (0xE923, P.glyph_vignette, (64, 36), 144, 69),
    'bar0':      (0xE930, ('pix', P.pixel_cell, 0), (4, 8), 8, 7),
    'bar1':      (0xE931, ('pix', P.pixel_cell, 1), (4, 8), 8, 7),
    'bar_l':     (0xE932, ('pix', P.pixel_cell, 2), (4, 8), 8, 7),
    'bar_r':     (0xE933, ('pix', P.pixel_cell, 3), (4, 8), 8, 7),
}
SPACES = {0xE9F0: -1, 0xE9F1: 2, 0xE9F2: 1}
SP_NEG1, SP_TWO, SP_ONE = chr(0xE9F0), chr(0xE9F1), chr(0xE9F2)
FONTS_CHECKED = ('hud', 'minimap', 'bossbar', 'mboss_gd', 'mboss_bf', 'mboss_fg', 'mboss_az')
BADGES = {'guard': ('수호', '#F2D45C'), 'nest': ('둥지', '#C9E07A'), 'nurt': ('양육', '#D4E784'),
          'pred': ('포식성', '#E07A5A'), 'destr': ('파괴', '#F0A040'), 'fail': ('', BANNER_RED)}
DIM_HEX = '#707070'
TITLE_G = {'heart': 't_heart', 'warn': 't_warn', 'fail': 't_fail', 'success': 't_success'}
BAR_CELLS = 20


def glyph(name):
    """the literal glyph string (use it with font rlk:mboss_ap)"""
    if name in ('sp_neg1', 'sp_two', 'sp_one'):
        return {'sp_neg1': SP_NEG1, 'sp_two': SP_TWO, 'sp_one': SP_ONE}[name]
    return chr(GLYPHS[name][0])


def _js(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def glyph_c(name, color='white'):
    """SNBT text component of one glyph in the kit's font"""
    return '{text:"' + glyph(name) + '",font:"' + FONT + '",color:"' + color + '"}'


def badge(kind, on):
    """SNBT text component of a phase-2 name-line badge: ◆ + the kind's name (dim #707070 when off, the kind's colour
    when on); kinds guard, nest, nurt, pred, destr, fail (the withered-Heart mark of a failure strike)."""
    assert kind in BADGES, kind
    name, col = BADGES[kind]
    c = col if on else DIM_HEX
    g = glyph('fail_s' if kind == 'fail' else kind)
    extra = '{text:"' + g + '",font:"' + FONT + '"}' + (',{text:"' + name + '"}' if name else '')
    return '{text:"",color:"' + c + '",extra:[' + extra + ']}'


def heart_bar(v, vmax=10000, cells=BAR_CELLS):
    """the FN-24 fallback Heart progress bar as one glyph string: caps + `cells` gold / dim cells for v of vmax"""
    n = max(0, min(cells, (int(v) * cells) // vmax))
    return glyph('bar_l') + glyph('bar1') * n + glyph('bar0') * (cells - n) + glyph('bar_r')


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
            if al < 0.1 and fn is not P.glyph_vignette:
                px += b'\x00\x00\x00\x00'
            elif aa <= 0:
                px += b'\x00\x00\x00\x00'
            else:
                px += bytes((round(255 * P.clamp01(ar / aa)), round(255 * P.clamp01(ag / aa)),
                             round(255 * P.clamp01(ab / aa)), round(255 * P.clamp01(al))))
    return px


def glyph_raw(name):
    cp, painter, (w, h), _height, _ascent = GLYPHS[name]
    if callable(painter):
        if painter is P.glyph_vignette:
            # the vignette is drawn in screen proportion (x and y both -1..1 over the 16:9 card)
            raw = bytearray()
            for j in range(h):
                for i in range(w):
                    x, y = -1 + 2 * (i + 0.5) / w, 1 - 2 * (j + 0.5) / h
                    r, g, b, a = painter(x, y)
                    raw += bytes((round(r * 255), round(g * 255), round(b * 255), round(a * 255)))
            return w, h, bytes(raw)
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
    assert px <= ATLAS_BUDGET, f'atlas budget: {px} new px > {ATLAS_BUDGET}'
    for k, v in KINDS.items():
        w, h = v[1]
        assert w <= 256 and h <= 256 and w % 16 == 0 and h % 16 == 0, (k, w, h)
    n_ref = check_refs(rp)
    n_glyphs = build_font(rp)
    root = rp / 'assets/rlk'
    tex_dir = root / f'textures/{TEXDIR}'
    dirs = {tex_dir: KINDS, root / f'models/item/{TEXDIR}': ALL_KINDS, root / f'items/{TEXDIR}': ALL_KINDS}
    for d, keep in dirs.items():
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob('*'):
            if old.stem not in keep:
                old.unlink()
    for kind in KINDS:
        w, h, raw = render(kind)
        data = png_bytes(w, h, raw)
        p = tex_dir / f'{kind}.png'
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
    for kind in ALL_KINDS:
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
    return len(KINDS), n_ref, px, n_glyphs


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
    """The function line that spawns one card (fx/card, or fx/cardx when an extended option is used); fg kit
    semantics (fg_fx_api.md §2): pos / rot of the card, billboard, roll (left_rotation about local z), spin over the
    main interpolation, s0 -> s1 (float or (x, y, z)), off (static start translation) + move, life / fade ticks, col
    tint, dly hidden ticks, dur main-interpolation ticks (0 = to the fade), hit / col2 the second tint. Any value may
    be a macro placeholder string such as '$(r)'."""
    assert kind in ALL_KINDS, kind
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


def tele_disc(r, tell, el=7, nd=0, hold=3):
    """Disc decal of radius r blocks; the fill reaches the rim `tell` ticks after the call (the hz/* strike tick when
    both are made in the same tick with the same tell)."""
    return f'function {FN}tele/disc {{r:{_tenths(r)},tell:{int(tell)},el:{int(el)},nd:{int(nd)},hold:{int(hold)}}}'


def tele_sector(r, a, tell, el=7, nd=0, hold=3):
    """Sector decal from the apex along the aim: radius r blocks, half-angle a degrees (any integer 1..180, drawn
    within 1 degree; a >= 175 draws a disc)."""
    return (f'function {FN}tele/sector {{r:{_tenths(r)},a:{int(round(a))},tell:{int(tell)},el:{int(el)},nd:{int(nd)},'
            f'hold:{int(hold)}}}')


def tele_wedge(r0, r1, a0, a1, tell, el=7, nd=0, hold=3):
    """One swept wedge: the annular sector r0..r1 blocks between a0 < a1 degrees relative to the executor's yaw
    (+ = clockwise from above, a1 - a0 <= 180). Call one per swept tick at that tick's tail root (ap_fx_api.md §0.4)."""
    assert a1 > a0 and a1 - a0 <= 180, (a0, a1)
    return (f'function {FN}tele/wedge {{r0:{_tenths(r0)},r1:{_tenths(r1)},a0:{int(round(a0))},a1:{int(round(a1))},'
            f'tell:{int(tell)},el:{int(el)},nd:{int(nd)},hold:{int(hold)}}}')


def tele_line(length, w, tell, el=7, nd=0, hold=3, back=0.0):
    return (f'function {FN}tele/line {{len:{_tenths(length)},w:{_tenths(w)},back:{_tenths(back)},tell:{int(tell)},'
            f'el:{int(el)},nd:{int(nd)},hold:{int(hold)}}}')


def tele_crack(length, w, tell, nd=0, hold=3, back=0.0):
    return (f'function {FN}tele/crack {{len:{_tenths(length)},w:{_tenths(w)},back:{_tenths(back)},tell:{int(tell)},'
            f'nd:{int(nd)},hold:{int(hold)}}}')


def tele_wave(wid, r0, r1, w, tell, dur, el=7, nd=0, hold=2):
    """Expanding wave ring id 0-7: the start disc fills to r0 over the tell, then the front travels r0 -> r1 in dur
    ticks with the band edge w behind (pair with hz/ring + hz/resize_s at (r1 - r0) / dur blocks per tick)."""
    assert 0 <= wid <= 7, wid
    return (f'function {FN}tele/wave {{id:{int(wid)},r0:{_tenths(r0)},r1:{_tenths(r1)},w:{_tenths(w)},tell:{int(tell)},'
            f'dur:{int(dur)},el:{int(el)},nd:{int(nd)},hold:{int(hold)}}}')


def tele_wave_end(wid):
    return f'function {FN}tele/wave_end {{id:{int(wid)}}}'


def tele_mask_wash(r, tell, hold):
    return f'function {FN}tele/mask_wash {{r:{_tenths(r)},tell:{int(tell)},hold:{int(hold)}}}'


def tele_safe_rim(sid, r, tell, hold):
    assert 0 <= sid <= 5, sid
    return f'function {FN}tele/safe_rim {{id:{int(sid)},r:{_tenths(r)},tell:{int(tell)},hold:{int(hold)}}}'


def tele_safe_end(sid):
    return f'function {FN}tele/safe_end {{id:{int(sid)}}}'


def tele_mring(mid, r, el=22):
    assert 0 <= mid <= 3, mid
    return f'function {FN}tele/mring {{id:{int(mid)},r:{_tenths(r)},el:{int(el)}}}'


def tele_mring_move(mid, t=2):
    return f'function {FN}tele/mring_move {{id:{int(mid)},t:{int(t)}}}'


def tele_mring_end(mid):
    return f'function {FN}tele/mring_end {{id:{int(mid)}}}'


def tele_wall_spot(tell, hold):
    return f'function {FN}tele/wall_spot {{tell:{int(tell)},hold:{int(hold)}}}'


DRESS = {'swirl': ('r',), 'ley': ('n',), 'redraw': (), 'clear': ()}


def dress(name, **args):
    """the dressing pool: dress('swirl', r=3.5) (blocks), dress('ley', n=7), dress('redraw'), dress('clear')"""
    assert name in DRESS, name
    assert set(args) == set(DRESS[name]), (name, args)
    if name == 'swirl':
        return f'function {FN}dress/swirl {{r:{_tenths(args["r"])}}}'
    if name == 'ley':
        return f'function {FN}dress/ley {{n:{int(args["n"])}}}'
    return f'function {FN}dress/{name}'


def snd(name):
    assert name in SOUNDS, name
    return f'function {FN}snd/{name}'


TENTHS_ARGS = ('r', 'r0', 'r1', 'len', 'w', 'h')        # preset size arguments are tenths of a block


def fx(name, **args):
    """A preset (fx/p/<name>); size arguments (r, r0, r1, len, w, h) in blocks are written in tenths, ticks and the
    other integers as given."""
    assert name in PRESETS, name
    need = PRESETS[name][1]
    assert set(args) == set(need), (name, sorted(args), need)
    if not need:
        return f'function {FN}p/{name}'
    vals = []
    for k in need:
        v = args[k]
        if isinstance(v, str):
            vals.append(f'{k}:{v}')
        elif k in TENTHS_ARGS:
            vals.append(f'{k}:{_tenths(v)}')
        else:
            vals.append(f'{k}:{int(v)}')
    return f'function {FN}p/{name} {{' + ','.join(vals) + '}'


def look(kind, col=WHITE):
    assert kind in ALL_KINDS, kind
    return f'function {FN}look {{kind:"{kind}",col:{int(col)}}}'


def prop(name):
    """As @s = an item_display prop: dress it as a kit look (fx/prop/<name>)."""
    assert name in PROPS, name
    return f'function {FN}prop/{name}'


def hud(name, **args):
    assert name in HUD_FUNCS, name
    need = HUD_FUNCS[name]
    assert set(args) == set(need), (name, sorted(args), need)
    if not args:
        return f'function {FN}hud/{name}'
    parts = []
    for k in need:
        v = args[k]
        parts.append(f'{k}:"{_js(v)}"' if isinstance(v, str) and k in ('g', 't', 'c', 's') else f'{k}:{int(v)}')
    return f'function {FN}hud/{name} {{' + ','.join(parts) + '}'


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


def itemp(item, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    return part(f'item{{item:"minecraft:{item}"}}', pos, delta, speed, n)


# ----------------------------------------------------------------------------- sound recipes (ap_fx_api.md §0.8)
# name -> (use, [(event, volume, pitch), ...]); one tick each, vanilla events only. Volume 0.8 / pitch 1.0 where the
# call list gives none; "(xN)" layers repeat with a small pitch spread so they read as several hits, not one louder.
V = 0.8


def L(event, vol=V, pitch=1.0, times=1):
    if times == 1:
        return [(event, vol, pitch)]
    spread = (0.0, 0.07, -0.06, 0.12, -0.11)
    return [(event, vol, round(min(2.0, max(0.5, pitch + spread[k])), 2)) for k in range(times)]


def S(use, *layers):
    out = []
    for l in layers:
        out += l
    return (use, out)


SOUNDS = {
    # entrance
    'e_emerge': S('E t0-31: the warden rises from the dark leaf pool.', L('entity.warden.emerge', V, 0.8),
                  L('block.rooted_dirt.break', times=3), L('block.azalea_leaves.break')),
    'e_flash': S('E t60: the flash at the bulb.', L('block.amethyst_block.chime'), L('block.beacon.power_select', V, 1.5)),
    'e_heart_up': S('E t70: the vine draws the Heart up.', L('block.vine.step'),
                    L('block.amethyst_block.resonate', V, 1.2)),
    'e_roar': S('E t100: crouch and roar.', L('entity.ravager.roar', 0.6, 1.3)),
    # P1 / R
    'p1_dive': S('P1 t4, P3 t5, T1 t20: dive and sink.', L('entity.warden.dig', V, 0.9), L('block.rooted_dirt.break'),
                 L('block.mud.break')),
    'p1_travel': S('P1 every 7 t underground (quiet).', L('entity.warden.dig', 0.4, 1.2), L('block.gravel.step', V, 0.5)),
    'p1_ring': S('P1 t32: the gold ring locks.', L('block.beacon.activate', 0.4, 1.5)),
    'p1_burst': S('P1 t44: the burst.', L('entity.warden.emerge', V, 1.4), L('block.amethyst_cluster.break'),
                  L('entity.generic.explode', 0.4, 1.3)),
    'p1_sweep': S('P1 t64: the lunge sweep.', L('entity.player.attack.sweep', V, 0.5),
                  L('entity.breeze.wind_burst', V, 0.6)),
    'p1_land': S('P1 t77: the landing.', L('entity.ravager.step'), L('block.moss.fall')),
    'r_sink': S('R t4: the relocate sink.', L('block.rooted_dirt.break', V, 0.6, 3), L('entity.warden.dig', V, 1.1)),
    'r_emerge': S('R t18: the relocate emergence.', L('entity.warden.emerge', 0.6, 1.3), L('block.azalea.place')),
    # P2
    'p2_swirl': S('P2 t5: the swirl starts.', L('entity.breeze.whirl', V, 0.7), L('block.beacon.ambient', V, 1.6)),
    'p2_swirl_tick': S('P2 every 3 t, t5-27 (leaf rustle).', L('block.azalea_leaves.break', V, 0.8)),
    'p2_plunge': S('P2 t30: the hands plunge.', L('entity.warden.dig', V, 0.7), L('entity.evoker_fangs.attack'),
                   L('block.rooted_dirt.break')),
    'p2_stalks': S('P2 t36: the stalks rise.', L('block.hanging_roots.break'), L('entity.warden.emerge', 0.5, 1.5)),
    'p2_lines': S('P2 t40: the crack lines.', L('block.sculk_sensor.clicking', V, 1.6)),
    'p2_slam': S('P2 slams.', L('entity.iron_golem.attack', V, 0.6), L('entity.generic.explode', 0.3, 1.5),
                 L('block.big_dripleaf.break')),
    'p2_flower': S('P2 t118: the flower rear.', L('entity.ravager.roar', 0.6, 1.2), L('block.azalea_leaves.break')),
    'p2_fold': S('P2 t128: fold down.', L('entity.ravager.step')),
    # P3
    'p3_emerge': S('P3 t44: the crown emerges.', L('entity.warden.emerge', V, 1.1)),
    'p3_glow': S('P3 t39: the gold ground glow.', L('block.beacon.activate', 0.4, 1.5), L('block.sculk_catalyst.bloom')),
    'p3_windup': S('P3 t94: the coil wind-up.', L('block.bamboo.break', V, 0.6), L('entity.breeze.idle_air')),
    'p3_slam': S('P3 slams.', L('entity.warden.attack_impact'), L('entity.generic.explode', 0.5, 0.7),
                 L('block.big_dripleaf.break')),
    'p3_wheels': S('P3 each slam: the wheels spawn.', L('block.amethyst_cluster.place', times=3)),
    'p3_wheel_roll': S('P3 every 4 t while a carpet runs.', L('block.azalea_leaves.step', V, 0.6)),
    'p3_wheel_hit': S('P3 thorn hit (#mbHitEv).', L('entity.player.hurt_sweet_berry_bush'),
                      L('block.amethyst_cluster.break')),
    'p3_homing_loop': S('P3 every 10 t per homing wheel.', L('block.amethyst_block.resonate', V, 1.6),
                        L('entity.blaze.burn', 0.3, 1.8)),
    # P4
    'p4_rear': S('P4 t0: arms and rear.', L('entity.breeze.wind_burst', 0.5, 0.6), L('block.azalea_leaves.break')),
    'p4_hum': S('P4 t16: the disc hum.', L('block.beacon.ambient', 0.4, 1.4), L('block.sculk_sensor.clicking')),
    'p4_spin': S('P4 t40: crash and spin.', L('entity.ravager.attack', V, 0.6), L('entity.player.attack.sweep', V, 0.5, 3),
                 L('entity.generic.splash')),
    # P5
    'p5_raise': S('P5 t8: the tail raise.', L('entity.breeze.idle_air', V, 0.7)),
    'p5_cock': S('P5 t23: the cock cue ("dash now").', L('entity.creaking.activate', V, 1.4),
                 L('item.trident.riptide_1', V, 0.6)),
    'p5_swing': S('P5 t28 / t52: a tail swing.', L('entity.player.attack.sweep', V, 0.6), L('item.trident.throw', V, 0.5)),
    'p5_hit': S('P5 / Q4 hit (#mbHitEv).', L('entity.player.attack.knockback')),
    # P6
    'p6_sweep': S('P6 hit 1: the arm sweep.', L('entity.player.attack.sweep', V, 0.7), L('block.grass.break')),
    'p6_slam': S('P6 hits 2 / 4: the slams.', L('entity.warden.sonic_boom', 0.5, 1.6), L('entity.generic.explode', V, 0.7),
                 L('block.mud.break', times=4)),
    'p6_spin': S('P6 hit 3: the low spin.', L('entity.player.attack.sweep', V, 0.6), L('entity.player.attack.sweep', V, 0.8)),
    # locomotion
    'm_crawl': S('crawl_p1 / walk_p3 steps.', L('entity.camel.step', V, 0.6), L('block.moss_carpet.step'),
                 L('block.azalea_leaves.step')),
    'm_walk': S('walk_p1 steps.', L('entity.warden.step', V, 0.8)),
    # phase 2: organisms and the Heart
    'o1_attack': S('O1 strike.', L('entity.slime.attack', V, 1.2), L('block.big_dripleaf.tilt_down')),
    'heart_hit': S('every Heart loss.', L('block.amethyst_block.hit', 0.4, 0.6)),
    'heart_gain': S('every Heart gain (the chime rises with the progress: 11 steps of #apHt).',
                    L('block.amethyst_block.chime', V, 1.0)),
    'o2_pivot': S('O2 t0.', L('block.big_dripleaf.tilt_up', V, 1.4)),
    'o2_charge': S('O2 t3.', L('entity.breeze.charge', 0.4, 1.6)),
    'o2_shoot': S('O2 t12.', L('entity.breeze.shoot', V, 1.3)),
    'o2_hit': S('O2 bolt end.', L('block.moss.break', V, 1.3)),
    'o3_collapse': S('O3 t0 / t16.', L('block.bamboo.break', 0.5, 0.8), L('block.mangrove_roots.place', V, 0.7)),
    'o3_cast': S('O3 t30.', L('block.beacon.activate', 0.5, 1.6)),
    'o3_pop': S('O3 shields up / a shield pool breaks.', L('block.amethyst_block.resonate', V, 1.4),
                L('item.shield.block', 0.4, 1.6)),
    'o3_death': S('O3 death.', L('block.chorus_flower.death'), L('entity.slime.death', V, 0.7)),
    'shield_hit': S('a hit absorbed by apShd.', L('item.shield.block', 0.4, 1.6)),
    'o4_rise': S('O4 t12: the walls rise.', L('block.big_dripleaf.place', V, 0.7, 3), L('block.azalea.place'),
                 L('block.amethyst_cluster.place', V, 1.2)),
    'o4_fade': S('O4 dissolve.', L('block.azalea_leaves.break'), L('block.beacon.deactivate', 0.3, 2.0)),
    'o4_flap': S('O4 flying (every 14 t).', L('entity.phantom.flap', 0.3, 1.5)),
    'o5_hum': S('O5 every 40 t while linked.', L('block.beacon.ambient', 0.2, 1.8)),
    'o5_destruct': S('O5 self-destruct.', L('block.azalea_leaves.break'), L('entity.allay.death', V, 1.3),
                     L('block.amethyst_cluster.break')),
    'o6_gulp': S('O6a t12.', L('entity.generic.eat', V, 0.6), L('entity.slime.squish')),
    'o6_bud': S('O6a t12.', L('block.beacon.power_select', 0.4, 1.5)),
    'o6_inflate': S('O6a t32.', L('entity.puffer_fish.blow_up', V, 0.8)),
    'o6_burst': S('O6a t42.', L('entity.puffer_fish.blow_out'), L('block.amethyst_cluster.break', V, 1.4),
                  L('entity.firework_rocket.blast', 0.5, 0.8)),
    'o6_bite': S('O6b each bite.', L('entity.evoker_fangs.attack', V, 1.3), L('entity.ravager.attack', 0.4, 1.6)),
    'o6_bite_first': S('O6b the first bite of a chain.', L('entity.evoker_fangs.attack', V, 1.3),
                       L('entity.ravager.attack', 0.4, 1.6), L('entity.player.attack.crit')),
    'o6_swim': S('O6 swimming (every 16 t).', L('entity.dolphin.swim', V, 1.2)),
    'o7_roll': S('O7 every 8 t.', L('entity.armadillo.roll', V, 0.8)),
    'o7_primed': S('O7 contact.', L('entity.creeper.primed', V, 1.4)),
    'o7_suck': S('O7 suck-in.', L('entity.breeze.inhale', V, 0.8)),
    'o7_blast': S('O7 blast.', L('entity.generic.explode', V, 0.8), L('entity.warden.sonic_boom', 0.3, 1.6)),
    'org_kill': S('basic kill.', L('block.azalea_leaves.break'), L('entity.slime.squish_small')),
    'timeout_warn': S('the time-out warning.', L('event.raid.horn', 0.3, 1.0)),
    'fail_strike': S('「소생 실패」 (proposal: plan §3.4 names no sound).', L('block.respawn_anchor.deplete', V, 0.6),
                     L('block.big_dripleaf.break', V, 0.5), L('block.sculk_shrieker.shriek', 0.4, 0.8)),
    # T1
    't1_cradle': S('T1 t45: the cradle rises.', L('block.rooted_dirt.break'), L('block.mangrove_roots.place', V, 0.7)),
    't1_lower': S('T1 t50: the Heart lowers.', L('block.amethyst_block.resonate', V, 1.2), L('block.spore_blossom.break')),
    't1_land': S('T1 t100: the egg lands.', L('block.honey_block.fall', V, 0.6), L('block.beacon.power_select', V, 1.4),
                 L('block.amethyst_block.chime')),
    't1_hud': S('T1 t106: the title.', L('ui.toast.in', V, 1.2)),
    'spawn_marker': S('every spawn marker.', L('block.chorus_flower.grow'), L('block.sculk_shrieker.place', V, 1.5)),
    # CS
    'cs_complete': S('CS t0: the revival completes.', L('block.respawn_anchor.set_spawn', V, 1.3),
                     L('block.amethyst_block.chime')),
    'cs_ember': S('CS t64: the 「불씨」 ember.', L('block.fire.ambient', 0.3, 1.6)),
    'cs_flash': S('CS t80: the green flash.', L('block.beacon.activate'), L('entity.lightning_bolt.thunder', 0.3, 2.0)),
    'cs_heal': S('CS t80: the heal.', L('block.amethyst_block.resonate', V, 1.4)),
    'cs_emerge': S('CS t92: the warden bursts out of the water.', L('entity.warden.emerge', V, 0.8),
                   L('block.azalea_leaves.break', times=4)),
    'cs_reveal': S('CS t132: the reveal.', L('block.beacon.activate', V, 0.7)),
    # Q1 / Q3s sink and trail
    'q1_sink': S('Q1 t8, Q3s t8: the sink.', L('entity.warden.dig', V, 1.2), L('block.mud.break'),
                 L('entity.player.splash.high_speed', V, 0.6)),
    'q1_trail': S('Q1 / Q3s every 4 t underground.', L('block.big_dripleaf.tilt_down', V, 0.8), L('block.lily_pad.place')),
    'q1_rosette': S('Q1 t32: the rosette.', L('block.flowering_azalea.place'), L('block.spore_blossom.place', V, 0.6)),
    'q1_burst': S('Q1 t44: the burst.', L('entity.warden.emerge', 0.6, 1.3), L('entity.generic.splash'),
                  L('block.big_dripleaf.break')),
    'q1_slam': S('Q1 t61 / t69: the slam and the whip.', L('entity.generic.explode', 0.4, 1.4),
                 L('entity.player.attack.sweep', V, 0.6), L('entity.generic.splash')),
    'q1_rise': S('Q1 t71: the rise.', L('block.big_dripleaf.tilt_up'), L('block.vine.step')),
    # Q2
    'q2_banner': S('Q2 B0: the banner.', L('block.respawn_anchor.set_spawn', V, 0.7), L('entity.elder_guardian.curse', 0.4, 1.4)),
    'q2_charge': S('Q2 t0: the charge.', L('block.conduit.activate', V, 0.8), L('block.beacon.power_select', V, 0.6)),
    'q2_whirl': S('Q2 t18: the whirl.', L('entity.breeze.whirl')),
    'q2_release': S('Q2 t40: the field release.', L('entity.warden.sonic_charge', V, 1.4), L('entity.breeze.wind_burst', V, 0.6)),
    'q2_field_loop': S('Q2 every 20 t, t40-156.', L('block.bubble_column.upwards_ambient'), L('block.sculk.spread', V, 1.4)),
    'q2_tick': S('Q2 each landed field tick.', L('entity.player.hurt_sweet_berry_bush')),
    'q2_dome': S('Q2 t54 / 58 / 62: a dome forms.', L('block.beacon.activate', V, 1.8), L('block.amethyst_block.chime', times=3),
                 L('block.respawn_anchor.charge', V, 1.6)),
    'q2_rain': S('Q2 t134: the light rain.', L('block.beacon.power_select', 0.5, 1.8)),
    'q2_blast': S('Q2 t156: the blast.', L('entity.warden.sonic_boom', V, 0.8), L('entity.dragon_fireball.explode', V, 0.7),
                  L('entity.lightning_bolt.thunder', 0.4, 1.5)),
    'q2_pop': S('Q2 t189: the domes pop.', L('block.glass.break', 0.5, 1.5), L('block.amethyst_cluster.break'),
                L('block.bubble_column.bubble_pop')),
    # Q3 / Q3s
    'q3_charge': S('Q3 t14: the charge.', L('block.respawn_anchor.charge', V, 1.5), L('block.beacon.ambient')),
    'q3_launch': S('Q3 t35: the launch.', L('entity.breeze.shoot', V, 0.8), L('item.crossbow.shoot', V, 0.5)),
    'q3_impact1': S('Q3 t45: shell 1.', L('entity.generic.explode', V, 1.2), L('block.beacon.deactivate', V, 1.5),
                    L('block.big_dripleaf.break')),
    'q3_impact2': S('Q3 t93 / 96: shells 2 / 3.', L('entity.dragon_fireball.explode', 0.5, 1.4)),
    'q3s_surface': S('Q3s t36: the surfacing.', L('block.mud.break'), L('entity.player.splash', V, 0.6),
                     L('block.azalea_leaves.break')),
    'q3s_charge': S('Q3s t36: the charge.', L('block.respawn_anchor.charge', 0.6, 1.5), L('block.amethyst_block.resonate', V, 1.6)),
    'q3s_launch': S('Q3s t46: the flat shot.', L('entity.breeze.shoot', V, 0.8), L('item.trident.riptide_1', 0.5, 1.4)),
    'q3s_impact': S('Q3s t48: the impact.', L('entity.generic.explode', 0.5, 1.3), L('block.beacon.activate', V, 1.8),
                    L('block.cherry_leaves.break')),
    # Q4
    'q4_swing': S('Q4 t14: swing 1.', L('entity.player.attack.sweep', V, 0.6), L('item.trident.throw', V, 0.5),
                  L('block.azalea_leaves.fall', times=3)),
    'q4_rear': S('Q4 t3, t36: rear / lunge.', L('entity.creaking.activate', V, 0.6), L('entity.ravager.step', V, 0.6)),
    'q4_swing2': S('Q4 t46: swing 2.', L('entity.player.attack.sweep', V, 0.6), L('item.trident.throw', V, 0.5),
                   L('block.azalea_leaves.fall', times=3), L('block.amethyst_cluster.step', times=4),
                   L('item.bone_meal.use')),
    # Q5
    'q5_unfold': S('Q5 t10: the unfold.', L('entity.breeze.charge', V, 1.2), L('block.big_dripleaf.tilt_up', V, 0.6),
                   L('block.amethyst_block.chime', times=3)),
    'q5_orb': S('Q5 each orb (t19-32).', L('block.amethyst_cluster.place'), L('block.beacon.ambient', 0.3, 1.8)),
    'q5_flare': S('Q5 t37 / 43: the glint.', L('block.beacon.power_select', 0.5, 1.8)),
    'q5_launch': S('Q5 t42 / 48: a volley flies.', L('entity.arrow.shoot', V, 0.6, 5) + L('entity.arrow.shoot', V, 0.66),
                   L('item.trident.throw', 0.4, 1.4)),
    'q5_impact': S('Q5 t49 / 55: the landings.', L('entity.generic.explode', 0.3, 1.6), L('block.amethyst_cluster.break', V, 0.8),
                   L('block.pointed_dripstone.land')),
    'q5_blades': S('Q5 t64: the skimming blades.', L('entity.breeze.wind_burst', V, 1.2), L('block.cherry_leaves.fall')),
    # death (no creature vocals)
    'd_droop': S('D t30: the droop.', L('block.big_dripleaf.break', V, 0.5)),
    'd_face_fade': S('D t30: the face fades.', L('block.beacon.deactivate', V, 0.6)),
    'd_leaves': S('D t85, 100, 110: leaf bursts.', L('block.azalea_leaves.break', times=3)),
    'd_splash': S('D t82: the topple onto the water.', L('entity.generic.splash')),
    'd_sink': S('D t100: the sink.', L('block.respawn_anchor.deplete', V, 0.8)),
    'd_seed': S('D t120: the golden seed.', L('block.amethyst_block.chime')),
}
HEART_PITCH = [round(2 ** ((k - 10) / 12), 3) for k in range(11)]        # k = floor(#apHt / 1000), 0..10
VOICE_EVENTS = ('entity.warden.', 'entity.ravager.roar', 'entity.slime.', 'entity.creaking.', 'entity.allay.',
                'entity.puffer_fish.', 'entity.dolphin.', 'entity.phantom.', 'entity.armadillo.', 'entity.creeper.',
                'entity.breeze.', 'entity.elder_guardian.', 'entity.evoker_fangs.', 'entity.iron_golem.',
                'entity.camel.')
DEATH_SOUNDS = [k for k in SOUNDS if k.startswith('d_')]


def min_volume(vol):
    """mboss_lib.min_volume (the Guardian's L.sound): quiet layers (<= 0.25) fade out completely past their range,
    louder ones keep a third of their volume there, at most 0.4."""
    if vol <= 0.25:
        return 0.0
    return round(min(0.4, vol / 3), 2)


def sound_line(event, vol, pitch):
    return (f'playsound minecraft:{event} hostile @a[tag=player] ~ ~ ~ {num(float(vol))} {num(float(pitch))} '
            f'{num(float(min_volume(vol)), 2)}')


# ----------------------------------------------------------------------------- presets (ap_fx_api.md §0.6)
# name -> (doc, args, fn, conv). A preset with size arguments is a macro whose public function converts the tenths /
# ticks into storage rlk:apkit pa (conv: [(key, arg, scale)]: pa.<key> = arg x scale as a float, or an int when scale
# is None) and runs the internal p/e/<name> with that storage; fn() returns the internal lines then.
PRESETS = {}
AMBIENT = ('gold_embers', 'shadow_glide', 'gold_motes', 'gold_drip', 'leaf_pad', 'floor_glitter', 'haze_withered',
           'haze_lush', 'spores')
PTCL = ('shadow_glide', 'homing_trail', 'comet_trail', 'tether', 'helix_trail', 'haze_withered', 'haze_lush')


def preset(name, doc, args=(), conv=()):
    def deco(f):
        PRESETS[name] = (doc, list(args), f, list(conv))
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


def fly(kind, yaw, el, dist, h=0.3, s0=0.5, s1=1.0, life=8, fade=3, col=WHITE, dly=0, roll=0, dur=0):
    """the fg radial trick: a fixed face card whose local +y points out along (yaw, elevation) flies dist outward"""
    return card(kind, f'~ ~{num(h, 2)} ~', f'~{ang(yaw)} {ang(90 - el)}', roll=roll, s0=s0, s1=s1,
                move=(0, dist if isinstance(dist, str) else round(dist, 2), 0), life=life, fade=fade, col=col, dly=dly,
                dur=dur)


def mac(line):
    return '$' + line


RND = random.Random


# --- generic
@preset('spark', 'A small lime-gold spark burst (tells, clicks). Billboard.')
def _p_spark():
    return [card('spark', bb='center', spin=60, s0=0.2, s1=1.0, life=5, fade=2, col=rgb('#F2FAB8')),
            part('happy_villager', '~ ~ ~', (0.25, 0.25, 0.25), 0, 3), part('wax_on', '~ ~ ~', (0.2, 0.2, 0.2), 0, 2)]


@preset('flash', 'A white-green glow flash (bright moments). Billboard.')
def _p_flash():
    return [card('glow', bb='center', s0=1.0, s1=3.6, life=5, fade=3, col=DENDRO_PALE)]


@preset('leaf_splash', 'Leaf + mote splash on the withered field (P1 land, P4 crash, Q3 shell 1): olive-green leaves '
        'flung up, airborne spray. At the floor point.')
def _p_leaf_splash():
    rnd = RND(11)
    out = [fly('leaf', yaw, rnd.uniform(35, 65), rnd.uniform(1.6, 2.6), h=0.3, s0=0.3, s1=0.6, life=12, fade=5,
               col=[rgb('#C9D88A'), rgb('#9AB65A'), GHOST, rgb('#7E9A3E')][k], roll=rnd.randint(-40, 40))
           for k, yaw in enumerate(radial(4, 20))]
    return out + [dust(rgb('#8A8A3A'), 1.6, '~ ~0.3 ~', (0.8, 0.2, 0.8), 10), blockp('moss_block', '~ ~0.3 ~', (0.6, 0.2, 0.6), 0.2, 12)]


@preset('water_splash', 'Water + leaf splash on the lush sheet (Q1, Q3s, CS t92, D t82). At the floor point.')
def _p_water_splash():
    return [card('splash', '~ ~0.02 ~', bb='vertical', s0=0.8, s1=2.6, life=9, fade=4, col=TEAL_FOAM, dur=4),
            card('ripple', '~ ~0.06 ~', '~ 90', s0=0.8, s1=4.0, life=12, fade=5, col=TEAL_FOAM),
            fly('leaf', 40, 55, 2.0, s0=0.3, s1=0.55, life=12, fade=5, col=LEAF_PALE),
            part('splash', '~ ~0.3 ~', (0.8, 0.3, 0.8), 0.3, 30), part('bubble_pop', '~ ~0.2 ~', (0.8, 0.1, 0.8), 0.05, 8)]


@preset('burrow_pool', 'The dark olive leaf pool the boss sinks into (E t0, P1 t4, P3 t5): spreads to radius {r} (35 = '
        '7 b across) in 10 t and lasts 40 t. At the floor point.', ('r',), (('d', 'r', 0.2),))
def _p_burrow_pool():
    return [mac(card('pool', '~ ~0.02 ~', '~ 0', s0=(0.6, 1, 0.6), s1=('$(d)', 1, '$(d)'), life=40, fade=10, dur=10)),
            dust(rgb('#2D2A04'), 2.2, '~ ~0.15 ~', (1.4, 0.05, 1.4), 14), dust(rgb('#3F3C15'), 1.4, '~ ~0.3 ~', (1.0, 0.2, 1.0), 8),
            blockp('rooted_dirt', '~ ~0.2 ~', (1.2, 0.1, 1.2), 0.1, 10)]


@preset('leaf_flakes', 'Black leaf flakes rising (E, P1 sink). At the floor point.')
def _p_leaf_flakes():
    rnd = RND(12)
    out = []
    for k in range(5):
        x, z = rnd.uniform(-1.6, 1.6), rnd.uniform(-1.6, 1.6)
        out.append(card('leaf', p3(x, 0.4, z, '~'), bb='center', spin=rnd.choice((-120, 120)), s0=0.25, s1=0.45,
                        move=(0, rnd.uniform(2.0, 3.2), 0), life=rnd.randint(20, 26), fade=8, col=BLACK_LEAF,
                        dly=rnd.randint(0, 6)))
    return out + [dust(rgb('#1E1C08'), 1.0, '~ ~0.8 ~', (1.2, 0.6, 1.2), 8)]


@preset('bulb_flash', 'The flash at the Heart bulb (E t60). At the bulb.')
def _p_bulb_flash():
    return [card('glow', bb='center', s0=1.0, s1=5.0, life=6, fade=3, col=rgb('#FFF8C0')),
            card('glint', bb='center', spin=45, s0=0.5, s1=3.6, life=6, fade=3, col=WHITE),
            flash(rgb('#FFF8C0'), '~ ~ ~', 0.9), part('end_rod', '~ ~ ~', (0.4, 0.4, 0.4), 0.1, 8)]


@preset('gold_embers', 'Golden leaf embers drifting around the raised hand (E t63-80, every 4 t). At the bulb.')
def _p_gold_embers():
    return [card('leaf', '~0.8 ~-0.4 ~0.3', bb='center', spin=110, s0=0.18, s1=0.32, move=(0, 0.9, 0), life=14, fade=6,
                 col=GOLD),
            card('mote', '~-0.6 ~-0.2 ~-0.5', bb='center', s0=0.2, s1=0.35, move=(0, 1.1, 0), life=12, fade=6, col=GOLD_PALE),
            dust(GOLD, 0.7, '~ ~ ~', (0.8, 0.6, 0.8), 4), part('wax_on', '~ ~ ~', (0.6, 0.5, 0.6), 0, 2)]


@preset('shadow_glide', 'Underground travel (P1 t23-44, P3 t23-39, every 2 t): a dark leaf ripple and dust over the '
        'hidden body. Particles only. At the hidden anchor (floor).')
def _p_shadow_glide():
    return [dust(rgb('#1E1C08'), 2.4, '~ ~0.1 ~', (1.3, 0.02, 1.3), 10), dust(rgb('#3F3C15'), 1.6, '~ ~0.15 ~', (1.0, 0.05, 1.0), 6),
            blockp('rooted_dirt', '~ ~0.1 ~', (0.9, 0.05, 0.9), 0.05, 4), part('smoke', '~ ~0.2 ~', (0.8, 0.05, 0.8), 0.01, 2)]


@preset('gold_burst', 'The burst (P1 t44, P3 slams): a white-gold flash and radial crystal blades, airborne (the ground '
        'decal is the hazard\'s). At the floor point.')
def _p_gold_burst():
    rnd = RND(13)
    out = [card('glow', '~ ~1 ~', bb='center', s0=1.2, s1=6.0, life=5, fade=3, col=GOLD_WHITE),
           card('glint', '~ ~1.2 ~', bb='center', spin=40, s0=0.6, s1=4.5, life=5, fade=2, col=rgb('#FAFCDF'))]
    for k, yaw in enumerate(radial(8, rnd.uniform(0, 20))):
        out.append(fly('blade', yaw, rnd.uniform(12, 38), rnd.uniform(3.2, 4.6), h=0.6, s0=0.6, s1=rnd.uniform(1.4, 1.9),
                       life=8, fade=3, col=GOLD_WHITE if k % 2 else GOLD, roll=rnd.randint(-10, 10)))
    return out + [flash(rgb('#FAFCDF'), '~ ~1 ~', 1.0), part('end_rod', '~ ~1 ~', (0.6, 0.5, 0.6), 0.25, 14),
                  part('firework', '~ ~1 ~', (0.3, 0.3, 0.3), 0.15, 6)]


@preset('leaf_debris', 'Black leaf debris and a pale ghost-leaf spray (P1 burst). At the floor point.')
def _p_leaf_debris():
    rnd = RND(14)
    out = []
    for k, yaw in enumerate(radial(6, 10)):
        black = k % 2 == 0
        out.append(fly('leaf', yaw + rnd.uniform(-15, 15), rnd.uniform(20, 45) if black else rnd.uniform(50, 75),
                       rnd.uniform(2.5, 3.8), h=0.4, s0=0.3, s1=0.5, life=14, fade=6,
                       col=BLACK_LEAF if black else GHOST, roll=rnd.randint(-60, 60)))
    return out + [blockp('dark_oak_leaves', '~ ~0.6 ~', (1.0, 0.4, 1.0), 0.2, 12), dust(GHOST, 1.2, '~ ~1 ~', (1.2, 0.8, 1.2), 8)]


@preset('slash_band', 'The lunge sweep (P1 t64): a white-gold streak band 1-2.5 b high along the lane of length {len}. '
        'At the lane start, rotated = the aim.', ('len',), (('h', 'len', 0.05), ('L', 'len', 0.1)))
def _p_slash_band():
    return [mac(card('streak', '^ ^1.25 ^$(h)', '~90 0', s0=(0.4, 9, 1), s1=('$(L)', 12, 1), life=7, fade=3, dur=2,
                     col=GOLD_WHITE)),
            mac(card('streak', '^ ^2.1 ^$(h)', '~90 0', s0=(0.4, 5, 1), s1=('$(L)', 7, 1), life=6, fade=3, dur=2,
                     col=rgb('#FAFCDF'), dly=1)),
            mac(card('glow', '^ ^1.6 ^$(h)', '~90 0', s0=(1, 1.5, 1), s1=('$(L)', 2.6, 1), life=5, fade=3, dur=2,
                     col=GOLD)),
            mac(part('end_rod', '^ ^1.6 ^$(h)', (0.4, 0.5, 0.4), 0.15, 10)), part('sweep_attack', '^ ^1.4 ^2', (0, 0, 0), 0, 1)]


@preset('spine_afterimage', 'Pale rib afterimages along the sweep path of length {len}, 10 t (P1 sweep). At the lane '
        'start, rotated = the aim.', ('len',), (('a', 'len', 0.1 / 6), ('b', 'len', 0.05), ('c', 'len', 0.5 / 6),
                                                ('s', 'len', 0.1 / 3 * 1.1)))
def _p_spine_afterimage():
    return [mac(card('rib', f'^ ^1.3 ^$({k})', '~90 0', s0=(0.8, 1.2, 1), s1=('$(s)', 1.7, 1), life=10, fade=6, dur=3,
                     dly=d, col=rgb('#EEF2E0'))) for d, k in enumerate(('a', 'b', 'c'))]


@preset('root_chunks', 'Brown root chunks with gold glints sinking (R t4, T1 t20 / t30). At the floor point.')
def _p_root_chunks():
    rnd = RND(15)
    out = [card('root_chunk', p3(rnd.uniform(-1.2, 1.2), 0.6, rnd.uniform(-1.2, 1.2), '~'), bb='center',
                spin=rnd.choice((-60, 60)), s0=0.45, s1=0.6, move=(0, -0.7, 0), life=16, fade=6, dly=rnd.randint(0, 4))
           for _ in range(5)]
    return out + [blockp('rooted_dirt', '~ ~0.3 ~', (1.0, 0.2, 1.0), 0.15, 14), dust(rgb('#F2C95A'), 0.8, '~ ~0.4 ~', (0.8, 0.3, 0.8), 5)]


@preset('emerge_motes', 'White-green motes of the 4 t scale-in (R t18). At the body.')
def _p_emerge_motes():
    rnd = RND(16)
    out = []
    for yaw in radial(6, 15):
        x, z = ring_xz(rnd.uniform(1.2, 2.2), yaw)
        out.append(card('mote', p3(x, rnd.uniform(0.6, 3.2), z), bb='center', s0=0.4, s1=0.7, move=(0, 1.2, 0), life=12,
                        fade=6, col=rgb('#E8FFD0'), dly=rnd.randint(0, 3)))
    return out + [part('happy_villager', '~ ~1.5 ~', (1.2, 1.2, 1.2), 0, 8)]


@preset('swirl_wisps', 'Pale-green spirals and whirling leaves around the body (P2 t5-27, every 4 t). At the body.')
def _p_swirl_wisps():
    return [card('spiral', '^1.6 ^2.4 ^0.5', bb='center', spin=170, s0=1.2, s1=2.0, life=8, fade=3, col=LEAF_PALE),
            card('spiral', '^-1.4 ^3.8 ^-0.4', bb='center', spin=-170, s0=1.0, s1=1.8, life=8, fade=3, col=LEAF_PALE, dly=2),
            card('leaf', '^2.0 ^1.6 ^-0.8', bb='center', spin=150, s0=0.3, s1=0.5, move=(0, 0.8, 0), life=8, fade=3,
                 col=LEAF_PALE),
            card('leaf', '^-2.1 ^2.8 ^0.9', bb='center', spin=-150, s0=0.3, s1=0.5, move=(0, 0.8, 0), life=8, fade=3,
                 col=rgb('#B8D888'), dly=1),
            dust(rgb('#D8F2B0'), 1.0, '~ ~2.5 ~', (1.6, 1.2, 1.6), 6)]


@preset('plunge_flash', 'The white-gold flash where the hands plunge (P2 t30). At the floor point.')
def _p_plunge_flash():
    return [card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=5.5, life=6, fade=3, col=GOLD_WHITE),
            card('glint', '~ ~0.8 ~', bb='center', spin=45, s0=0.6, s1=3.4, life=5, fade=2, col=rgb('#FAFCDF')),
            flash(GOLD_WHITE, '~ ~0.6 ~', 0.9)]


@preset('splinter_splash', 'The pale-green splinter splash around the hands (P2 t30, r 3-4). At the floor point.')
def _p_splinter_splash():
    rnd = RND(17)
    out = [fly('blade', yaw, rnd.uniform(15, 40), rnd.uniform(2.6, 3.8), h=0.3, s0=0.3, s1=0.7, life=8, fade=3,
               col=rgb('#B8E07A'), roll=rnd.randint(-15, 15)) for yaw in radial(8, 5)]
    return out + [blockp('bamboo', '~ ~0.3 ~', (1.2, 0.2, 1.2), 0.2, 10), dust(rgb('#B8E07A'), 1.2, '~ ~0.4 ~', (1.4, 0.2, 1.4), 10)]


@preset('slam_arc', 'A stalk slam (P2 slams): the arc trail over the strip, the impact flash and green splinters. At the '
        'stalk root, rotated along the strip.')
def _p_slam_arc():
    rnd = RND(18)
    out = [card('crescent', '^ ^3.2 ^3.4', '~90 0', s0=(4, 6, 1), s1=(7.2, 9, 1), life=5, fade=3, dur=2, col=GOLD_WHITE),
           card('glow', '^ ^0.3 ^5.2', bb='center', s0=1.0, s1=3.2, life=5, fade=3, col=GOLD_WHITE, dly=2)]
    for k in range(4):
        out.append(card('blade', '^ ^0.3 ^5.2', f'~{ang(rnd.uniform(-70, 70))} {ang(90 - rnd.uniform(25, 55))}',
                        s0=0.3, s1=0.6, move=(0, rnd.uniform(1.6, 2.6), 0), life=7, fade=3, dly=2, col=rgb('#B8E07A')))
    return out + [blockp('rooted_dirt', '^ ^0.3 ^5', (0.8, 0.2, 0.8), 0.15, 10), dust(rgb('#B8E07A'), 1.2, '^ ^0.3 ^5', (0.8, 0.2, 0.8), 8)]


@preset('gold_glow', 'A soft gold ground glow of radius {r}, no rim (P3 t39-44: it must not read as a telegraph). At the '
        'floor point.', ('r',), (('d', 'r', 0.24),))
def _p_gold_glow():
    return [mac(card('glow', '~ ~0.03 ~', '~ 90', s0=1.0, s1='$(d)', life=12, fade=5, col=rgb('#C8B44A'))),
            dust(rgb('#AB9839'), 1.4, '~ ~0.2 ~', (1.2, 0.05, 1.2), 10), part('wax_on', '~ ~0.4 ~', (1.0, 0.3, 1.0), 0, 4)]


@preset('crown_debris', 'The crown and hood emergence debris (P3 t44): dark leaves and grey dust thrown up. At the body.')
def _p_crown_debris():
    rnd = RND(19)
    out = [fly('leaf', yaw, rnd.uniform(45, 75), rnd.uniform(2.2, 3.4), h=1.2, s0=0.3, s1=0.55, life=14, fade=6,
               col=BLACK_LEAF if k % 3 else OLIVE, roll=rnd.randint(-50, 50)) for k, yaw in enumerate(radial(6, 30))]
    out += [card('smoke', '~1 ~0.8 ~0.4', bb='center', s0=0.8, s1=2.2, move=(0, 0.8, 0), life=16, fade=8, col=rgb('#9A9A88')),
            card('smoke', '~-0.9 ~0.6 ~-0.5', bb='center', s0=0.8, s1=2.0, move=(0, 0.7, 0), life=15, fade=8,
                 col=rgb('#8A8A78'), dly=2)]
    return out + [blockp('moss_block', '~ ~0.8 ~', (1.2, 0.5, 1.2), 0.2, 14)]


@preset('spiral_wisps', 'Wind-up spirals around the coiled column (P3 t94-130, every 4 t). At the body.')
def _p_spiral_wisps():
    return [card('spiral', '^1.2 ^2.0 ^0.6', bb='center', spin=170, s0=1.4, s1=2.2, life=8, fade=3, col=LEAF_PALE),
            card('spiral', '^-1.0 ^4.2 ^-0.5', bb='center', spin=-170, s0=1.2, s1=2.0, life=8, fade=3, col=rgb('#E8F8C8'), dly=1),
            card('spiral', '^0.4 ^6.0 ^0.2', bb='center', spin=170, s0=1.0, s1=1.6, life=8, fade=3, col=LEAF_PALE, dly=2),
            dust(GOLD, 0.8, '~ ~4 ~', (0.8, 2.0, 0.8), 6)]


@preset('blade_burst', 'Gold blade rays to radius {r}, airborne (P3 slams, r 72). At the floor point.', ('r',),
        (('m', 'r', 0.085),))
def _p_blade_burst():
    rnd = RND(20)
    return [mac(fly('blade', yaw, rnd.uniform(4, 14), '$(m)', h=0.4, s0=0.5, s1=rnd.uniform(1.5, 2.0), life=7, fade=3,
                    col=GOLD if k % 2 else GOLD_WHITE, roll=rnd.randint(-6, 6)))
            for k, yaw in enumerate(radial(12, rnd.uniform(0, 15)))]


@preset('wheel_carpet', 'The thorn-wheel carpet (P3 slams): 18 pale-green thorn wheels ride the carpet front from radius '
        '{r0} to {r1} in {dur} ticks (tenths / ticks, like the hazard). Call it on the tick BEFORE the slam (the fg '
        'wave_band rule): the wheels then move from the slam tick with the tele/wave front. At the floor centre.',
        ('r0', 'r1', 'dur'), (('r0', 'r0', 0.1), ('r1', 'r1', 0.1), ('d', 'dur', None, 0), ('l', 'dur', None, 5)))
def _p_wheel_carpet():
    rnd = RND(22)
    return [mac(card('thorn_wheel_x', '~ ~ ~', f'~{ang(yaw)} 0', s0=1.55, s1=1.65, off=(0, 0.82, '$(r0)'),
                     move=(0, 0.82, '$(r1)'), life='$(l)', fade=4, dur='$(d)'))
            for yaw in [y + rnd.uniform(-6, 6) for y in radial(18, 5)]]


@preset('homing_trail', 'The homing wheel\'s gold-orange spark trail (P3, every 2 t; particles only). At the wheel; run '
        'it as the wheel (execute as <wheel> at @s) and it also turns the prop 90 degrees (the camera-facing spin).')
def _p_homing_trail():
    return [dust_fade(rgb('#FFD27A'), rgb('#E8902A'), 1.3, '~ ~ ~', (0.25, 0.25, 0.25), 4),
            part('crit', '~ ~ ~', (0.2, 0.2, 0.2), 0.05, 2), part('small_flame', '~ ~ ~', (0.15, 0.15, 0.15), 0.01, 1),
            f'execute if entity @s[type=minecraft:item_display] run function {FN}prop/e/spin']


@preset('wheel_pop', 'A thorn wheel pops (P3, end of life or hit): a gold-orange flash and sparks (r 1.5). At the prop.')
def _p_wheel_pop():
    out = [card('glow', bb='center', s0=0.8, s1=3.0, life=5, fade=3, col=rgb('#F7C25E'))]
    for k, yaw in enumerate(radial(4, 45)):
        out.append(card('spark', '~ ~ ~', f'~{ang(yaw)} {ang(90 - 25 * (k % 2) - 10)}', s0=0.3, s1=0.6,
                        move=(0, 1.3, 0), life=5, fade=2, col=rgb('#FFD27A')))
    return out + [part('crit', '~ ~ ~', (0.4, 0.4, 0.4), 0.3, 8), dust(rgb('#E8902A'), 1.2, '~ ~ ~', (0.5, 0.5, 0.5), 6)]


@preset('spin_trails', 'Spin trails white-gold -> pale green around the body (P4 t47-71, every 3 t). At the body.')
def _p_spin_trails():
    return [card('crescent', '^ ^1.4 ^3.0', '~ 90', s0=(5, 3, 1), s1=(6, 4, 1), life=6, fade=3, dur=2, col=GOLD_WHITE,
                 hit=3, col2=LEAF_PALE),
            card('crescent', '^ ^2.6 ^-2.6', '~180 90', s0=(4, 3, 1), s1=(5, 4, 1), life=6, fade=3, dur=2, col=GOLD_WHITE,
                 hit=3, col2=LEAF_PALE, dly=1),
            dust_fade(GOLD_WHITE, LEAF_PALE, 1.2, '~ ~1.5 ~', (2.5, 0.6, 2.5), 8)]


@preset('spin_flash', 'The mid-spin flash (P4 t57). At the body.')
def _p_spin_flash():
    return [card('glow', '~ ~2 ~', bb='center', s0=1.2, s1=5.0, life=5, fade=3, col=GOLD_WHITE),
            card('glint', '~ ~2 ~', bb='center', spin=60, s0=0.6, s1=3.6, life=5, fade=2, col=DENDRO_PALE),
            flash(GOLD_WHITE, '~ ~2 ~', 0.8)]


@preset('tail_tip_flash', 'The white tail-tip flash: the "dash now" cue (P5 t23, Q4 t11). At the tail tip anchor.')
def _p_tail_tip_flash():
    return [card('glint', bb='center', spin=45, s0=0.4, s1=3.6, life=6, fade=3, col=WHITE),
            card('glow', bb='center', s0=0.6, s1=2.6, life=6, fade=3, col=rgb('#FFFFF0')),
            flash(rgb('#FFFFF0'), '~ ~ ~', 1.0), part('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.12, 6)]


ARC_N = 7


def _arc(name, n, cols, h, frac, s_y, life, fade, rev):
    """the internal arc of n crescent cards on a circle of radius pa.R about the executor, from -a to +a degrees
    (pa.b<k> = the bearings), each tangent and lying flat, revealed one tick apart in the sweep direction"""
    out = []
    for k in range(n):
        d = (n - 1 - k) if rev else k
        out.append(mac(f'execute rotated ~$(b{k}) 0 run ' +
                       card('crescent', f'^ ^{num(h, 2)} ^$(R)', '~ 90', s0=('$(L)', s_y * 0.6, 1), s1=('$(L)', s_y, 1),
                            life=life, fade=fade, dur=2, dly=d, col=cols[k % len(cols)])))
    return out


@preset('arc_trail', 'The white-gold arc trail over a tail swing (P5): 7 crescents on the circle of radius 0.8 {r} about '
        'the tail root from -{a} to +{a} degrees, revealed in the sweep direction {dir} (+1 clockwise from above). At the '
        'tail root, rotated = the arc\'s mid-bearing.', ('r', 'a', 'dir'))
def _p_arc_trail():
    return _arc_head('arc_trail', 0.8)


@preset('crescent_trail', 'The green crescent trails of a phase-3 tail swing (Q4; #A4D6AC / #BFE682 / #EBF898): 7 '
        'crescents on the circle of radius 0.8 {r} from -{a} to +{a} degrees, revealed in the sweep direction {dir}. At the '
        'tail root, rotated = the arc\'s mid-bearing.', ('r', 'a', 'dir'))
def _p_crescent_trail():
    return _arc_head('crescent_trail', 0.8)


@preset('arm_sweep', 'The arm-sweep arc and ground furrow (P6 hit 1): 5 crescents on the circle of radius 0.75 {r} over '
        '+-{a} degrees, left to right. At the body, rotated = the aim.', ('r', 'a'))
def _p_arm_sweep():
    return _arc_head('arm_sweep', 0.75, n=5, has_dir=False)


def _arc_head(name, frac, n=ARC_N, has_dir=True):
    """the public part of an arc preset: tenths / degrees -> storage pa (R, L, b0..b<n-1>), then the internal arc"""
    out = ['$scoreboard players set #wkAr mb $(r)', '$scoreboard players set #wkAa mb $(a)']
    if has_dir:
        out.append('$scoreboard players set #wkAd mb $(dir)')
    out += ['execute if score #wkAa mb matches ..0 run scoreboard players set #wkAa mb 1',
            'execute if score #wkAa mb matches 181.. run scoreboard players set #wkAa mb 180',
            f'execute store result storage {STO} pa.R float {num(0.1 * frac, 5)} run scoreboard players get #wkAr mb',
            'scoreboard players operation #wkAx mb = #wkAr mb', 'scoreboard players operation #wkAx mb *= #wkAa mb',
            # chord of one card: 2 pi R (2a / 360) / n x 1.18 overlap; R = frac r / 10
            f'execute store result storage {STO} pa.L float {num(2 * math.pi * 0.1 * frac * 2 / 360 / n * 1.18, 7)} run '
            'scoreboard players get #wkAx mb']
    for k in range(n):
        c = (2 * k + 1 - n) / n            # bearing of card k = a x c
        out.append(f'execute store result storage {STO} pa.b{k} float {num(c, 5)} run scoreboard players get #wkAa mb')
    if has_dir:
        out.append(f'execute if score #wkAd mb matches 0.. run function {FN}p/e/{name}_p with storage {STO} pa')
        out.append(f'execute if score #wkAd mb matches ..-1 run function {FN}p/e/{name}_n with storage {STO} pa')
    else:
        out.append(f'function {FN}p/e/{name}_p with storage {STO} pa')
    return out


ARC_BODIES = {
    'arc_trail': dict(n=ARC_N, cols=(GOLD_WHITE, rgb('#FAFCDF'), GOLD_WHITE), h=1.2, s_y=3.2, life=10, fade=5),
    'crescent_trail': dict(n=ARC_N, cols=CRESC, h=0.9, s_y=3.6, life=12, fade=6),
    'arm_sweep': dict(n=5, cols=(GOLD_WHITE, rgb('#FAFCDF')), h=1.0, s_y=3.0, life=8, fade=4),
}


@preset('slam_burst', 'The double-slam radial burst (P6 hit 2): a white-gold floor flash, a shock ring, crystal blades '
        'and dark debris. At the floor point.')
def _p_slam_burst():
    rnd = RND(23)
    out = [card('glow', '~ ~0.05 ~', '~ 90', s0=1.2, s1=7.0, life=6, fade=3, col=GOLD_WHITE),
           card('ripple', '~ ~0.07 ~', '~ 90', spin=30, s0=1.0, s1=6.6, life=9, fade=4, dur=5, col=GOLD)]
    out += [fly('blade', yaw, rnd.uniform(10, 30), rnd.uniform(2.4, 3.4), h=0.3, s0=0.4, s1=1.2, life=7, fade=3,
                col=GOLD_WHITE) for yaw in radial(6, 15)]
    out += [fly('leaf', yaw, rnd.uniform(35, 60), rnd.uniform(1.8, 2.6), h=0.3, s0=0.3, s1=0.5, life=12, fade=5,
                col=BLACK_LEAF, roll=rnd.randint(-40, 40)) for yaw in radial(4, 40)]
    return out + [blockp('rooted_dirt', '~ ~0.3 ~', (1.6, 0.2, 1.6), 0.2, 16), part('explosion', '~ ~0.5 ~', (0.2, 0.1, 0.2), 0, 1)]


@preset('spin_ring', 'The ring of gold sparks of the low spin (P6 hit 3), radius {r}. At the body.', ('r',),
        (('R', 'r', 0.1), ('d', 'r', 0.2)))
def _p_spin_ring():
    out = [mac(card('ripple', '~ ~0.6 ~', '~ 90', spin=60, s0=1.0, s1='$(d)', life=8, fade=4, dur=4, col=GOLD))]
    for k, yaw in enumerate(radial(8, 10)):
        out.append(mac(f'execute rotated ~{ang(yaw)} 0 run ' +
                       card('spark', '^ ^0.7 ^$(R)', bb='center', spin=60, s0=0.3, s1=0.9, life=6, fade=3, dly=k % 2,
                            col=GOLD_WHITE)))
    return out + [dust(GOLD, 1.2, '~ ~0.7 ~', (2.4, 0.2, 2.4), 12)]


@preset('leap_slam', 'The leap slam (P6 hit 4): the biggest flash, black and gold debris. At the floor point.')
def _p_leap_slam():
    rnd = RND(24)
    out = [card('glow', '~ ~1.5 ~', bb='center', s0=2.0, s1=8.0, life=5, fade=3, col=GOLD_WHITE),
           card('glow', '~ ~0.05 ~', '~ 90', s0=1.5, s1=9.0, life=7, fade=4, col=GOLD),
           card('ripple', '~ ~0.07 ~', '~ 90', spin=40, s0=1.0, s1=8.5, life=10, fade=4, dur=5, col=GOLD_WHITE)]
    out += [fly('blade', yaw, rnd.uniform(10, 40), rnd.uniform(3.0, 4.4), h=0.4, s0=0.5, s1=1.5, life=8, fade=3,
                col=GOLD_WHITE if k % 2 else GOLD) for k, yaw in enumerate(radial(8, 5))]
    out += [fly('leaf', yaw, rnd.uniform(40, 70), rnd.uniform(2.4, 3.6), h=0.4, s0=0.3, s1=0.55, life=14, fade=6,
                col=BLACK_LEAF if k < 4 else GOLD, roll=rnd.randint(-60, 60)) for k, yaw in enumerate(radial(6, 25))]
    return out + [flash(GOLD_WHITE, '~ ~1 ~', 1.0), part('explosion', '~ ~0.5 ~', (0.4, 0.1, 0.4), 0, 2),
                  blockp('rooted_dirt', '~ ~0.3 ~', (2.0, 0.2, 2.0), 0.25, 20)]


@preset('spawn_marker', 'An organism spawn marker: a pale wireframe dome for 20 t (T1 t116, every spawn). At the spawn point.')
def _p_spawn_marker():
    return [card('dome_flare', '~ ~0.02 ~', '~ 0', s0=0.4, s1=2.0, life=20, fade=6, dur=6, col=rgb('#E8F4E0')),
            card('dome_flare', '~ ~0.02 ~', '~90 0', s0=0.4, s1=2.0, life=20, fade=6, dur=6, col=rgb('#E8F4E0')),
            card('ripple', '~ ~0.05 ~', '~ 90', s0=0.5, s1=2.4, life=18, fade=6, dur=8, col=rgb('#F1FFD2')),
            part('end_rod', '~ ~0.8 ~', (0.5, 0.5, 0.5), 0.02, 6)]


@preset('org_burst', 'A pale-green organism burst (basic kill, failure, CS wilt). At the organism.')
def _p_org_burst():
    rnd = RND(25)
    out = [card('glow', '~ ~0.7 ~', bb='center', s0=0.6, s1=2.6, life=5, fade=3, col=LEAF_PALE)]
    out += [fly('leaf', yaw, rnd.uniform(30, 70), rnd.uniform(1.0, 1.8), h=0.7, s0=0.2, s1=0.4, life=10, fade=4,
                col=LEAF_PALE if k % 2 else rgb('#B8D888'), roll=rnd.randint(-40, 40)) for k, yaw in enumerate(radial(4, 30))]
    return out + [part('happy_villager', '~ ~0.7 ~', (0.5, 0.5, 0.5), 0, 6), part('composter', '~ ~0.6 ~', (0.4, 0.3, 0.4), 0, 6)]


@preset('heart_gain', 'The Heart\'s gain sparkle (heart/add). At the bulb.')
def _p_heart_gain():
    return [card('glint', bb='center', spin=60, s0=0.4, s1=2.2, life=6, fade=3, col=rgb('#FFF8C0')),
            card('mote', '~0.6 ~ ~0.3', bb='center', s0=0.3, s1=0.5, move=(0, 1.0, 0), life=10, fade=5, col=GOLD),
            card('mote', '~-0.5 ~0.2 ~-0.4', bb='center', s0=0.3, s1=0.5, move=(0, 1.2, 0), life=10, fade=5, col=GOLD_PALE, dly=2),
            part('wax_on', '~ ~ ~', (0.6, 0.6, 0.6), 0, 4)]


@preset('heart_hit', 'The Heart\'s loss: red-gold motes (heart/sub). At the bulb.')
def _p_heart_hit():
    return [card('mote', '~0.5 ~0.3 ~0.2', bb='center', s0=0.35, s1=0.5, move=(0, -0.6, 0), life=10, fade=5, col=rgb('#E06A3A')),
            card('mote', '~-0.6 ~0.1 ~-0.3', bb='center', s0=0.35, s1=0.5, move=(0, -0.5, 0), life=10, fade=5, col=rgb('#F2C24A')),
            card('mote', '~0.1 ~0.5 ~-0.6', bb='center', s0=0.3, s1=0.45, move=(0, -0.7, 0), life=9, fade=5, col=RED_EMBER, dly=1),
            dust(RED_EMBER, 1.0, '~ ~ ~', (0.6, 0.5, 0.6), 6)]


@preset('crown_flare', 'The basic organism\'s crown flare (O2 t3-12). At the crown.')
def _p_crown_flare():
    return [card('glint', bb='center', spin=45, s0=0.3, s1=1.4, life=8, fade=3, col=SHELL),
            card('glow', bb='center', s0=0.4, s1=1.3, life=8, fade=3, col=LIME),
            part('happy_villager', '~ ~ ~', (0.2, 0.2, 0.2), 0, 2)]


@preset('comet_trail', 'The bolt\'s green comet trail, bowing <= 0.5 b (O2, every 2 t; particles only). At the bolt prop.')
def _p_comet_trail():
    return [dust(rgb('#ABDE85'), 1.1, '~ ~ ~', (0.08, 0.08, 0.08), 3),
            dust_fade(SHELL, rgb('#6E9E48'), 0.9, '~ ~ ~', (0.12, 0.12, 0.12), 2),
            part('happy_villager', '~ ~ ~', (0.1, 0.1, 0.1), 0, 1)]


@preset('shield_pop', 'The yellow 3-leaf crown flash of a shield (O3 shields up, a pool breaking). At the basic.')
def _p_shield_pop():
    out = [card('glow', '~ ~1.6 ~', bb='center', s0=0.5, s1=1.8, life=6, fade=3, col=rgb('#F2E05A'))]
    for k, yaw in enumerate(radial(3, 0)):
        out.append(card('leaf', '~ ~1.7 ~', f'~{ang(yaw)} {ang(90 - 55)}', s0=0.3, s1=0.7, move=(0, 0.35, 0), life=10,
                        fade=4, col=rgb('#F2E05A')))
    return out + [part('wax_on', '~ ~1.6 ~', (0.3, 0.3, 0.3), 0, 4)]


@preset('guard_death', 'The 수호 death: red embers and a black twisted wisp. At the 수호.')
def _p_guard_death():
    rnd = RND(26)
    out = [card('wisp', '~0.2 ~1.2 ~', bb='vertical', s0=(2, 2.5, 2), s1=(2.4, 4.0, 2.4), move=(0, 1.4, 0), life=20, fade=8),
           card('wisp', '~-0.3 ~0.8 ~0.2', bb='vertical', roll=8, s0=(1.6, 2, 1.6), s1=(2, 3.4, 2), move=(0, 1.2, 0), life=18,
                fade=8, dly=3)]
    for k in range(4):
        out.append(card('mote', p3(rnd.uniform(-0.8, 0.8), rnd.uniform(0.6, 2.4), rnd.uniform(-0.8, 0.8), '~'), bb='center',
                        s0=0.25, s1=0.35, move=(0, rnd.uniform(1.0, 1.8), 0), life=16, fade=6, col=RED_EMBER, dly=k))
    return out + [part('smoke', '~ ~1.2 ~', (0.4, 0.8, 0.4), 0.02, 8), dust(RED_EMBER, 0.8, '~ ~1.5 ~', (0.5, 1.0, 0.5), 8)]


@preset('wall_motes', 'A wall blade dissolves into motes (O4). At the blade.')
def _p_wall_motes():
    rnd = RND(27)
    return [card('mote', p3(rnd.uniform(-0.6, 0.6), rnd.uniform(0.4, 2.4), rnd.uniform(-0.2, 0.2), '~'), bb='center',
                 s0=0.3, s1=0.45, move=(0, 0.9, 0), life=12, fade=6, col=rgb('#E6F08A'), dly=k) for k in range(4)] + \
        [part('composter', '~ ~1.2 ~', (0.4, 0.8, 0.2), 0, 8)]


@preset('blink_flash', 'The 둥지 blink flash (O4 blink out 0 / in 3). At the 둥지.')
def _p_blink_flash():
    return [card('glow', '~ ~1 ~', bb='center', s0=0.6, s1=2.4, life=5, fade=3, col=DENDRO_PALE),
            card('glint', '~ ~1 ~', bb='center', spin=60, s0=0.3, s1=2.0, life=5, fade=2, col=WHITE),
            part('end_rod', '~ ~1 ~', (0.3, 0.3, 0.3), 0.08, 5)]


TETHER_N = 10


@preset('tether', 'One wavy 양육 tether beam of length {len} toward the basic (O5, refresh every 2 t; particles only, '
        'dust #D4E784, the wave flips phase every 2 t). At the 양육 orb, rotated facing the basic (pitch counts).',
        ('len',), tuple((f'z{k}', 'len', 0.1 * k / TETHER_N) for k in range(1, TETHER_N + 1)))
def _p_tether():
    out = ['execute store result score #wkNow mb run time query gametime', 'scoreboard players set #wk4 mb 4',
           'scoreboard players operation #wkPh mb = #wkNow mb', 'scoreboard players operation #wkPh mb %= #wk4 mb']
    for ph in (0, 1):
        sel = '..1' if ph == 0 else '2..'
        for k in range(1, TETHER_N + 1):
            x = 0.22 * math.sin(math.pi * k / 2.5 + math.pi * ph) * math.sin(math.pi * k / TETHER_N)
            out.append(mac(f'execute if score #wkPh mb matches {sel} run particle minecraft:dust{{color:{colour_list(TETHER)},'
                           f'scale:0.9}} ^{num(x, 3)} ^ ^$(z{k}) 0.02 0.02 0.02 0 1 force @a[tag=player]'))
    return out


@preset('nurt_burst', 'The 양육 self-destruct: green-yellow sparks. At the 양육.')
def _p_nurt_burst():
    out = [card('glow', '~ ~1.2 ~', bb='center', s0=0.8, s1=3.2, life=6, fade=3, col=TETHER)]
    out += [fly('spark', yaw, 25 + 20 * (k % 2), 1.8, h=1.2, s0=0.3, s1=0.7, life=6, fade=3, col=rgb('#E6F08A'))
            for k, yaw in enumerate(radial(6, 15))]
    return out + [part('happy_villager', '~ ~1.2 ~', (0.6, 0.6, 0.6), 0, 8), part('composter', '~ ~1 ~', (0.5, 0.5, 0.5), 0, 8)]


@preset('bite_flash', 'A white-yellow bite flash (O6b). At the bite point.')
def _p_bite_flash():
    return [card('glint', '~ ~0.8 ~', bb='center', spin=45, s0=0.4, s1=2.2, life=5, fade=2, col=rgb('#FFFBD0')),
            card('glow', '~ ~0.8 ~', bb='center', s0=0.5, s1=1.8, life=5, fade=3, col=rgb('#F6F0A0')),
            part('crit', '~ ~0.8 ~', (0.3, 0.3, 0.3), 0.2, 6)]


@preset('pred_burst', 'The 포식성 burst r 3.6 (O6a t42). At the 포식성.')
def _p_pred_burst():
    rnd = RND(28)
    out = [card('glow', '~ ~1 ~', bb='center', s0=1.0, s1=5.0, life=5, fade=3, col=DENDRO_PALE),
           card('ripple', '~ ~0.06 ~', '~ 90', spin=30, s0=1.0, s1=7.0, life=8, fade=3, dur=4, col=DENDRO)]
    out += [fly('leaf_blade', yaw, rnd.uniform(10, 35), rnd.uniform(2.4, 3.2), h=0.6, s0=0.4, s1=1.0, life=7, fade=3,
                col=LIME_PALE) for yaw in radial(6, 0)]
    out += [fly('shard', yaw, rnd.uniform(30, 60), rnd.uniform(1.8, 2.6), h=0.8, s0=0.3, s1=0.6, life=8, fade=3,
                col=rgb('#C8EE8A')) for yaw in radial(4, 30)]
    return out + [part('firework', '~ ~1 ~', (0.4, 0.4, 0.4), 0.15, 8), part('happy_villager', '~ ~1 ~', (1.2, 0.6, 1.2), 0, 10)]


@preset('fuse_pulse', 'One 파괴 fuse glow pulse (O7; every 9 t, every 4 t in the last 20 t). At the 파괴 face.')
def _p_fuse_pulse():
    return [card('glow', bb='center', s0=0.8, s1=2.2, life=5, fade=3, col=rgb('#F0A040')),
            card('ripple', '~ ~-0.5 ~', '~ 90', s0=0.6, s1=2.4, life=6, fade=3, col=rgb('#F0C060')),
            part('small_flame', '~ ~ ~', (0.2, 0.2, 0.2), 0.01, 2)]


@preset('blast_dome', 'The 파괴 blast: a green translucent dome r 3 for 12 t. At the 파괴.')
def _p_blast_dome():
    return [card('dome_flare', '~ ~ ~', '~ 0', s0=0.6, s1=6.2, life=12, fade=6, dur=3, col=rgb('#9CF04A')),
            card('dome_flare', '~ ~ ~', '~90 0', s0=0.6, s1=6.2, life=12, fade=6, dur=3, col=rgb('#9CF04A')),
            card('glow', '~ ~1 ~', bb='center', s0=1.0, s1=5.0, life=5, fade=3, col=DENDRO_PALE),
            part('explosion', '~ ~0.8 ~', (0.3, 0.2, 0.3), 0, 2), part('happy_villager', '~ ~1 ~', (1.8, 1.0, 1.8), 0, 12)]


@preset('cradle_dust', 'Root-chunk dust of the cradle rise (T1 t45-65). At the cradle.')
def _p_cradle_dust():
    rnd = RND(29)
    out = [card('smoke', p3(x, 0.5, z, '~'), bb='center', s0=0.8, s1=2.0, move=(0, 0.6, 0), life=16, fade=8,
                col=rgb('#9A8A68'), dly=k) for k, (x, z) in enumerate(((1.2, 0.4), (-1.0, 0.8), (0.3, -1.3), (-0.6, -0.7)))]
    out += [card('root_chunk', p3(rnd.uniform(-1, 1), 0.3, rnd.uniform(-1, 1), '~'), bb='center', s0=0.4, s1=0.55,
                 move=(0, 0.9, 0), life=12, fade=5, dly=k) for k in range(3)]
    return out + [blockp('rooted_dirt', '~ ~0.4 ~', (1.2, 0.3, 1.2), 0.15, 12)]


@preset('heart_beam', 'The green-gold light beam as the egg lands, 10 t (T1 t100). At the cradle.')
def _p_heart_beam():
    return [card('beam', '~ ~ ~', '~ 0', s0=(0.8, 14, 0.8), s1=(1.8, 14, 1.8), life=10, fade=4, dur=3, col=rgb('#D8EE8A')),
            card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=4.0, life=10, fade=4, col=rgb('#E8E07A')),
            part('end_rod', '~ ~3 ~', (0.3, 3.0, 0.3), 0.02, 12)]


@preset('gold_motes', 'Drifting gold motes over the phase-2 field (every 20 t). At the floor centre.')
def _p_gold_motes():
    out = ['execute store result score #wkNow mb run time query gametime', 'scoreboard players set #wk3 mb 3',
           'scoreboard players operation #wkPh mb = #wkNow mb', 'scoreboard players operation #wkPh mb %= #wk3 mb']
    rnd = RND(30)
    for v in range(3):
        for k in range(3):
            x, z = ring_xz(rnd.uniform(4, 14), rnd.uniform(0, 360))
            out.append(f'execute if score #wkPh mb matches {v} run ' +
                       card('mote', p3(x, rnd.uniform(0.6, 2.6), z, '~'), bb='center', s0=0.3, s1=0.45,
                            move=(0, 1.4, 0), life=30, fade=10, col=GOLD))
    return out + [dust(GOLD, 0.8, '~ ~1.2 ~', (10, 1.0, 10), 6)]


@preset('shock_ring', 'The 「소생 실패」 Dendro shock ring r 0 -> 26. At the floor centre.')
def _p_shock_ring():
    return [card('ripple', '~ ~0.08 ~', '~ 90', spin=40, s0=1.0, s1=52.0, life=14, fade=4, dur=12, col=DENDRO),
            card('ripple', '~ ~0.07 ~', '~ 90', spin=-30, s0=1.0, s1=48.0, life=16, fade=5, dur=12, col=DENDRO_PALE, dly=2),
            card('glow', '~ ~1 ~', bb='center', s0=2.0, s1=8.0, life=6, fade=3, col=DENDRO_PALE),
            flash(DENDRO_PALE, '~ ~1 ~', 1.0)]


@preset('wilt_ring', 'The green pulse ring r 0 -> 26 over 20 t as every organism wilts (CS t0). At the floor centre.')
def _p_wilt_ring():
    return [card('ripple', '~ ~0.08 ~', '~ 90', spin=50, s0=1.0, s1=52.0, life=24, fade=4, dur=20, col=rgb('#9CF04A')),
            card('glow', '~ ~0.05 ~', '~ 90', s0=2.0, s1=12.0, life=12, fade=6, col=rgb('#C8F07A'))]


@preset('gold_drip', 'Gold dripping from the lifted egg (CS t0-24, every 3 t). At the egg.')
def _p_gold_drip():
    return [card('mote', '~0.3 ~-1.0 ~0.2', bb='center', s0=0.25, s1=0.3, move=(0, -2.2, 0), life=8, fade=2, col=GOLD),
            card('mote', '~-0.4 ~-0.9 ~-0.1', bb='center', s0=0.2, s1=0.28, move=(0, -2.0, 0), life=8, fade=2, col=GOLD_PALE, dly=1),
            part('falling_honey', '~ ~-0.8 ~', (0.5, 0.2, 0.5), 0, 3), part('dripping_honey', '~ ~-0.6 ~', (0.4, 0.2, 0.4), 0, 2)]


EMBER_N = 12


@preset('ember_arc', 'The 「불씨」 ember: a spark arcs {h} high over the {len} from a bank twig into the egg (CS t64-76; '
        '12 sparks shown one after another). At the twig, rotated facing the egg (pitch counts).', ('len', 'h'),
        tuple((f'z{k}', 'len', 0.1 * k / (EMBER_N - 1)) for k in range(EMBER_N)) +
        tuple((f'y{k}', 'h', 0.1 * 4 * (k / (EMBER_N - 1)) * (1 - k / (EMBER_N - 1))) for k in range(EMBER_N)))
def _p_ember_arc():
    out = [mac(card('glint', f'^ ^$(y{k}) ^$(z{k})', bb='center', spin=60, s0=0.35, s1=0.6, life=3, fade=1, dly=k,
                    col=rgb('#FFC870'))) for k in range(EMBER_N)]
    return out + [part('flame', '^ ^ ^', (0.05, 0.05, 0.05), 0.01, 3), part('lava', '^ ^ ^', (0, 0, 0), 0, 1)]


@preset('green_lightning', 'Green lightning ribbons around the egg (CS t76-84). At the egg.')
def _p_green_lightning():
    return [card('lightning', '~0.6 ~-1.2 ~0.2', bb='vertical', roll=14, s0=(1.6, 2.4, 1), s1=(2.0, 3.2, 1), life=4, fade=1,
                 col=rgb('#9CF04A')),
            card('lightning', '~-0.7 ~-1.0 ~-0.3', bb='vertical', roll=-18, s0=(1.4, 2.0, 1), s1=(1.8, 2.8, 1), life=4,
                 fade=1, col=rgb('#C8FF7A'), dly=2),
            card('lightning', '~0.1 ~-1.4 ~0.6', bb='vertical', roll=4, s0=(1.6, 2.6, 1), s1=(2.0, 3.4, 1), life=4, fade=1,
                 col=rgb('#9CF04A'), dly=4),
            part('electric_spark', '~ ~ ~', (1.0, 1.0, 1.0), 0.2, 12), flash(rgb('#9CF04A'), '~ ~ ~', 0.6)]


@preset('revival_burst', 'The leaf splash of the warden bursting out of the water (CS t92). At the floor centre.')
def _p_revival_burst():
    rnd = RND(31)
    out = [card('splash', '~ ~0.02 ~', bb='vertical', s0=2.0, s1=6.0, life=12, fade=5, dur=5, col=TEAL_FOAM),
           card('splash', '~ ~0.02 ~', bb='vertical', roll=8, s0=1.6, s1=4.6, life=10, fade=5, dur=4, col=WHITE, dly=2),
           card('glow', '~ ~2 ~', bb='center', s0=2.0, s1=8.0, life=6, fade=3, col=DENDRO_PALE)]
    out += [fly('leaf', yaw, rnd.uniform(45, 75), rnd.uniform(3.0, 4.6), h=1.0, s0=0.4, s1=0.75, life=16, fade=6,
                col=LEAF_PALE if k % 2 else LIME, roll=rnd.randint(-60, 60)) for k, yaw in enumerate(radial(8, 10))]
    return out + [part('splash', '~ ~0.5 ~', (2.5, 0.5, 2.5), 0.4, 40), part('happy_villager', '~ ~2 ~', (2.0, 1.5, 2.0), 0, 16)]


@preset('leaf_mound', 'The leaf mound and spray where the boss sinks (Q1 t8, Q3s t8). At the floor point.')
def _p_leaf_mound():
    return [card('mound', '~ ~ ~', bb='vertical', s0=1.6, s1=3.4, life=14, fade=6, dur=4),
            fly('leaf', 30, 60, 1.8, h=0.5, s0=0.3, s1=0.5, life=12, fade=5, col=rgb('#B1CE71')),
            fly('leaf', 160, 55, 2.0, h=0.5, s0=0.3, s1=0.5, life=12, fade=5, col=LEAF_PALE),
            fly('leaf', 270, 65, 1.6, h=0.5, s0=0.3, s1=0.5, life=12, fade=5, col=rgb('#B1CE71')),
            part('splash', '~ ~0.4 ~', (1.2, 0.3, 1.2), 0.2, 20), blockp('azalea_leaves', '~ ~0.5 ~', (1.0, 0.3, 1.0), 0.15, 10)]


@preset('leaf_pad', 'One translucent 2-3 b leaf pad of the underground trail, life 30 t (Q1 t16-42, Q3s t20-36, every '
        '4 t). At the hidden anchor (floor), rotated as the trail.')
def _p_leaf_pad():
    return [card('pad', '~ ~0.025 ~', '~ 0', s0=0.6, s1=2.4, life=30, fade=8, dur=4),
            part('splash', '~ ~0.1 ~', (0.6, 0.05, 0.6), 0.05, 4)]


@preset('rosette', 'The rosette: 10 glowing leaves rising around the burst point, airborne (Q1 t32; the ground ring is '
        'tele/disc r 4.2). At the burst point.')
def _p_rosette():
    out = []
    for k, yaw in enumerate(radial(10, 9)):
        x, z = ring_xz(3.4, yaw)
        out.append(card('leaf_blade', p3(x, 0.2, z, '^'), f'~{ang(yaw)} {ang(90 - 70)}', s0=0.3, s1=1.6,
                        move=(0, 1.6, 0), life=12, fade=3, dur=10, col=LIME_PALE if k % 2 else rgb('#D8F2A0')))
    return out + [part('happy_villager', '~ ~0.5 ~', (3.0, 0.3, 3.0), 0, 10)]


@preset('surface_burst', 'The white-lime surfacing flash and leaf spray (Q1 t44). At the burst point.')
def _p_surface_burst():
    rnd = RND(32)
    out = [card('glow', '~ ~1.2 ~', bb='center', s0=1.2, s1=6.0, life=5, fade=3, col=rgb('#F4FFD0')),
           card('glint', '~ ~1.4 ~', bb='center', spin=45, s0=0.6, s1=4.0, life=5, fade=2, col=WHITE)]
    out += [fly('leaf', yaw, rnd.uniform(40, 70), rnd.uniform(2.6, 3.6), h=0.6, s0=0.3, s1=0.6, life=12, fade=5,
                col=LIME_PALE if k % 2 else LEAF_PALE, roll=rnd.randint(-50, 50)) for k, yaw in enumerate(radial(6, 15))]
    return out + [part('splash', '~ ~0.5 ~', (1.5, 0.4, 1.5), 0.3, 24), flash(rgb('#F4FFD0'), '~ ~1 ~', 0.9)]


@preset('hoop_trail', 'The hoop arc trail as the body vaults (Q1 t44-49). At the body.')
def _p_hoop_trail():
    return [card('crescent', '^ ^4.2 ^1.2', '~90 0', roll=-20, s0=(4, 4, 1), s1=(5, 5, 1), life=8, fade=4, dur=2,
                 col=LIME_PALE),
            card('crescent', '^ ^5.4 ^3.2', '~90 0', s0=(4, 4, 1), s1=(5, 5, 1), life=8, fade=4, dur=2, col=rgb('#F4FFD0'), dly=1),
            card('crescent', '^ ^4.2 ^5.2', '~90 0', roll=20, s0=(4, 4, 1), s1=(5, 5, 1), life=8, fade=4, dur=2,
                 col=LIME_PALE, dly=2)]


@preset('belly_splash', 'The belly-flop splash (Q1 t61). At the floor point.')
def _p_belly_splash():
    return [card('splash', '~ ~0.02 ~', bb='vertical', s0=1.6, s1=4.2, life=10, fade=4, dur=4, col=TEAL_FOAM),
            card('splash', '~ ~0.02 ~', bb='vertical', roll=10, s0=1.2, s1=3.2, life=9, fade=4, dur=3, col=WHITE, dly=1),
            card('ripple', '~ ~0.06 ~', '~ 90', s0=1.0, s1=6.0, life=12, fade=5, dur=6, col=TEAL_FOAM),
            part('splash', '~ ~0.4 ~', (1.8, 0.3, 1.8), 0.4, 30)]


@preset('sweep_ring', 'The leaf-blade ring of the 360-degree tail whip, radius {r} (Q1 t69; core #E0F996, rim #A2CA6C). '
        'At the body.', ('r',), (('R', 'r', 0.085), ('d', 'r', 0.2)))
def _p_sweep_ring():
    out = [mac(card('ripple', '~ ~0.35 ~', '~ 90', spin=80, s0=2.0, s1='$(d)', life=8, fade=3, dur=4, col=LIME_RIM))]
    for k, yaw in enumerate(radial(12, 0)):
        out.append(mac(f'execute rotated ~{ang(yaw)} 0 run ' +
                       card('leaf_blade', '^ ^0.5 ^$(R)', '~90 90', s0=(0.6, 1.2, 1), s1=(1.0, 2.6, 1), life=6, fade=3,
                            dly=k // 3, col=LIME_PALE if k % 2 else LIME_RIM)))
    return out


@preset('light_sprouts', 'Light sprouts at the rise (Q1 t71). At the body.')
def _p_light_sprouts():
    return [card('leaf_blade', p3(x, 0.0, z, '^'), bb='vertical', s0=0.2, s1=1.3, life=12, fade=5, dur=6,
                 col=LIME_PALE if k % 2 else rgb('#F4FFD0'), dly=k % 3)
            for k, (x, z) in enumerate((ring_xz(1.8, y) for y in radial(6, 20)))] + \
        [part('happy_villager', '~ ~0.6 ~', (1.6, 0.4, 1.6), 0, 8)]


@preset('crouch_splash', 'The splash as the boss crouches to charge (Q2 t0). At the body.')
def _p_crouch_splash():
    return [card('splash', '^1.2 ^0.02 ^0.6', bb='vertical', s0=1.2, s1=3.0, life=10, fade=4, dur=4, col=TEAL_FOAM),
            card('splash', '^-1.4 ^0.02 ^-0.4', bb='vertical', roll=8, s0=1.0, s1=2.6, life=10, fade=4, dur=4, col=WHITE, dly=1),
            card('ripple', '~ ~0.06 ~', '~ 90', s0=2.0, s1=8.0, life=12, fade=5, dur=6, col=TEAL_FOAM),
            part('splash', '~ ~0.4 ~', (2.0, 0.3, 2.0), 0.3, 24)]


@preset('whirl_leaves', 'Whirling leaves around the body (Q2 t18-36, every 3 t; the three positions rotate each call). '
        'At the body.')
def _p_whirl_leaves():
    out = ['execute store result score #wkNow mb run time query gametime', 'scoreboard players set #wk3 mb 3',
           'scoreboard players operation #wkPh mb = #wkNow mb', 'scoreboard players operation #wkPh mb %= #wk3 mb']
    for v in range(3):
        for k in range(3):
            yaw = 120 * k + 40 * v
            x, z = ring_xz(3.0, yaw)
            out.append(f'execute if score #wkPh mb matches {v} run ' +
                       card('leaf', p3(x, 1.0 + 0.9 * k, z), bb='center', spin=160, s0=0.35, s1=0.55, move=(0, 0.6, 0),
                            life=8, fade=3, col=LEAF_PALE if k % 2 else rgb('#B8D888')))
    return out + [dust(LEAF_PALE, 1.0, '~ ~2 ~', (2.5, 1.0, 2.5), 6)]


@preset('field_ring', 'The visible front of the 종말의 여파 field release: a flat translucent yellow-green wave from '
        'radius {r0} to {r1} in {dur} ticks (Q2 t40). At the floor centre.', ('r0', 'r1', 'dur'),
        (('d0', 'r0', 0.2), ('d1', 'r1', 0.2), ('t', 'dur', None, 0), ('l', 'dur', None, 4)))
def _p_field_ring():
    return [mac(card('ripple', '~ ~0.09 ~', '~ 90', spin=40, s0='$(d0)', s1='$(d1)', life='$(l)', fade=4, dur='$(t)',
                     col=rgb('#C5E892'))),
            mac(card('ripple', '~ ~0.085 ~', '~ 90', spin=-30, s0='$(d0)', s1='$(d1)', life='$(l)', fade=5, dur='$(t)',
                     col=rgb('#9BBE61'), dly=2)),
            mac(card('glow', '~ ~0.08 ~', '~ 90', s0='$(d0)', s1='$(d1)', life='$(l)', fade=6, dur='$(t)',
                     col=rgb('#ACD075'))),
            part('happy_villager', '~ ~0.4 ~', (3.0, 0.2, 3.0), 0, 10)]


@preset('floor_glitter', 'Glitter on the tinted 종말의 여파 floor (Q2 t80-155, every 10 t). At the floor centre.')
def _p_floor_glitter():
    return [card('glint', '~6.5 ~0.3 ~-4.0', bb='center', spin=60, s0=0.3, s1=0.9, life=8, fade=4, col=rgb('#E9C20E')),
            card('glint', '~-8.0 ~0.3 ~9.5', bb='center', spin=-60, s0=0.3, s1=0.8, life=8, fade=4, col=rgb('#EAF9E9'), dly=3),
            part('wax_on', '~ ~0.3 ~', (14, 0.1, 14), 0, 24), part('end_rod', '~ ~0.4 ~', (12, 0.2, 12), 0.01, 4)]


@preset('light_pillar', 'A 10 t light-pillar tell where a dome will form (Q2 t44 / 48 / 52). At the dome centre.')
def _p_light_pillar():
    return [card('beam', '~ ~ ~', '~ 0', s0=(0.6, 14, 0.6), s1=(1.6, 16, 1.6), life=12, fade=4, dur=4, col=rgb('#F5FFE0')),
            card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=3.6, life=12, fade=4, col=rgb('#E4F69D')),
            part('end_rod', '~ ~3 ~', (0.3, 3.0, 0.3), 0.02, 10)]


@preset('dome_rise', 'The base-rim sparkle as a dome forms (Q2 t54 / 58 / 62; dome r 4.5). At the dome centre.')
def _p_dome_rise():
    out = [card('ripple', '~ ~0.07 ~', '~ 90', spin=40, s0=2.0, s1=9.2, life=10, fade=4, dur=5, col=rgb('#E4F69D'))]
    for k, yaw in enumerate(radial(8, 22.5)):
        x, z = ring_xz(4.4, yaw)
        out.append(card('spark', p3(x, 0.3, z, '~'), bb='center', spin=60, s0=0.3, s1=0.8, move=(0, 0.8, 0), life=8,
                        fade=4, col=rgb('#F5FFD4'), dly=k % 3))
    return out + [part('end_rod', '~ ~1.5 ~', (3.0, 1.5, 3.0), 0.02, 12)]


@preset('beam_rain', 'Falling light columns over the disc (Q2 t134-156, every 4 t; the three positions rotate each '
        'call). At the floor centre.')
def _p_beam_rain():
    out = ['execute store result score #wkNow mb run time query gametime', 'scoreboard players set #wk3 mb 3',
           'scoreboard players operation #wkPh mb = #wkNow mb', 'scoreboard players operation #wkPh mb %= #wk3 mb']
    rnd = RND(33)
    for v in range(3):
        for k in range(3):
            x, z = ring_xz(rnd.uniform(5, 21), rnd.uniform(0, 360))
            out.append(f'execute if score #wkPh mb matches {v} run ' +
                       card('beam', p3(x, 9, z, '~'), '~ 0', s0=(0.5, 8, 0.5), s1=(0.9, 8, 0.9), move=(0, -9, 0),
                            life=6, fade=2, dur=5, col=YELLOW_BEAM))
    return out + [part('end_rod', '~ ~6 ~', (14, 3, 14), 0, 6)]


FLOOD_CELL = 7.5


def flood_cells():
    """the flood grid: 7.5 b cells whose centre is within 26.6 b of the arena centre (44 cells)"""
    cells = []
    for i in range(-4, 4):
        for j in range(-4, 4):
            x, z = (i + 0.5) * FLOOD_CELL, (j + 0.5) * FLOOD_CELL
            if math.hypot(x, z) <= 26.6:
                cells.append((x, z))
    return cells


@preset('flood', 'The 종말의 여파 flood: yellow tiles over the walk disc for {life} ticks, skipping every cell within '
        f'{DOME_SKIP} b of a live {DOME_TAG} marker (the flood pool, <= {FLCAP} cards). At the floor centre.', ('life',))
def _p_flood():
    out = ['$scoreboard players set #wkFl mb $(life)', 'execute if score #wkFl mb matches ..5 run scoreboard players set #wkFl mb 6',
           f'execute store result storage {STO} pf.l int 1 run scoreboard players get #wkFl mb']
    for x, z in flood_cells():
        out.append(f'execute positioned ~{num(x, 2)} ~ ~{num(z, 2)} unless entity @e[tag={DOME_TAG},distance=..{DOME_SKIP}] '
                   f'run function {FN}p/e/flood_tile with storage {STO} pf')
    return out + [flash(FLOOD, '~ ~1 ~', 1.0)]


@preset('dome_pop', 'A dome pops: a flash and lime shards (Q2 t189). At the dome centre.')
def _p_dome_pop():
    rnd = RND(34)
    out = [card('glow', '~ ~2 ~', bb='center', s0=2.0, s1=7.0, life=5, fade=3, col=rgb('#F5FFD4'))]
    for k, yaw in enumerate(radial(8, 10)):
        el = rnd.uniform(15, 60)
        x, z = ring_xz(3.6 * math.cos(math.radians(el)), yaw)
        out.append(card('shard', p3(x, 0.3 + 3.6 * math.sin(math.radians(el)), z, '~'), f'~{ang(yaw)} {ang(90 - el)}',
                        roll=rnd.randint(-30, 30), s0=0.5, s1=0.9, move=(0, rnd.uniform(1.4, 2.4), 0), life=9, fade=4,
                        col=rgb('#E3FBA7')))
    return out + [part('end_rod', '~ ~2 ~', (2.5, 1.5, 2.5), 0.08, 14), part('bubble_pop', '~ ~0.4 ~', (3.0, 0.3, 3.0), 0, 12)]


@preset('green_burst', 'A green burst at the boss (Q2 t190). At the body.')
def _p_green_burst():
    rnd = RND(35)
    out = [card('glow', '~ ~3 ~', bb='center', s0=1.5, s1=6.0, life=6, fade=3, col=rgb('#9CF04A')),
           card('glint', '~ ~3 ~', bb='center', spin=45, s0=0.8, s1=4.0, life=5, fade=2, col=DENDRO_PALE)]
    out += [fly('leaf', yaw, rnd.uniform(20, 60), rnd.uniform(2.0, 3.0), h=3.0, s0=0.3, s1=0.55, life=10, fade=4,
                col=LIME_PALE) for yaw in radial(4, 45)]
    return out + [part('happy_villager', '~ ~3 ~', (1.5, 1.5, 1.5), 0, 10)]


@preset('launch_flash', 'The launch flash at the crown / muzzle (Q3 t35, Q3s t46). At the anchor.')
def _p_launch_flash():
    return [card('glow', bb='center', s0=1.0, s1=3.8, life=5, fade=3, col=YELLOW_BEAM),
            card('glint', bb='center', spin=45, s0=0.5, s1=3.2, life=5, fade=2, col=WHITE),
            flash(YELLOW_BEAM, '~ ~ ~', 0.9)]


@preset('beam_column', 'A vertical light beam column {w} wide (#FDFBBD; Q3 t45, Q3s t48, Q5 t14). At the floor point.',
        ('w',), (('w', 'w', 0.1), ('c', 'w', 0.045), ('g', 'w', 0.22)))
def _p_beam_column():
    return [mac(card('beam', '~ ~ ~', '~ 0', s0=('$(c)', 22, '$(c)'), s1=('$(w)', 24, '$(w)'), life=9, fade=4, dur=2,
                     col=YELLOW_BEAM)),
            mac(card('beam', '~ ~ ~', '~45 0', s0=('$(c)', 22, '$(c)'), s1=('$(c)', 24, '$(c)'), life=7, fade=3, col=WHITE)),
            mac(card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1='$(g)', life=9, fade=4, col=YELLOW_BEAM)),
            part('end_rod', '~ ~4 ~', (0.4, 4.0, 0.4), 0.02, 14), flash(YELLOW_BEAM, '~ ~1 ~', 0.8)]


@preset('spores', 'Spore puffs on the water after a shell (Q3 t45). At the floor point.')
def _p_spores():
    return [card('mote', '~0.8 ~0.4 ~0.3', bb='center', s0=0.3, s1=0.5, move=(0, 1.0, 0), life=20, fade=8, col=SHELL),
            card('mote', '~-0.7 ~0.3 ~-0.6', bb='center', s0=0.3, s1=0.45, move=(0, 0.9, 0), life=20, fade=8, col=SHELL, dly=3),
            part('spore_blossom_air', '~ ~0.4 ~', (2.0, 0.3, 2.0), 0, 12), part('happy_villager', '~ ~0.4 ~', (2.0, 0.3, 2.0), 0, 4)]


@preset('shell_streak', 'A yellow streak falling from {h} above onto the point in 6 t (Q3 t87 / 90; call it 6 t before the '
        'impact). At the floor point.', ('h',), (('h', 'h', 0.1), ('m', 'h', -0.1)))
def _p_shell_streak():
    return [mac(card('streak', '~ ~$(h) ~', bb='vertical', roll=90, s0=(0.5, 8, 1), s1=(1.6, 8, 1), move=(0, '$(m)', 0),
                     life=7, dur=6, col=YELLOW_BEAM)),
            mac(card('glow', '~ ~$(h) ~', bb='center', s0=0.8, s1=1.2, move=(0, '$(m)', 0), life=7, dur=6, col=SHELL))]


@preset('shell_burst', 'A shell burst r 3 (Q3 t93 / 96, Q3s t48). At the floor point.')
def _p_shell_burst():
    rnd = RND(36)
    out = [card('glow', '~ ~0.05 ~', '~ 90', s0=1.0, s1=6.0, life=6, fade=3, col=rgb('#D1E98D')),
           card('glow', '~ ~1 ~', bb='center', s0=1.0, s1=3.4, life=5, fade=3, col=YELLOW_BEAM),
           card('ripple', '~ ~0.07 ~', '~ 90', spin=30, s0=1.0, s1=6.0, life=8, fade=3, dur=4, col=SHELL)]
    out += [fly('leaf_blade', yaw, rnd.uniform(15, 45), rnd.uniform(2.0, 2.8), h=0.3, s0=0.3, s1=0.9, life=7, fade=3,
                col=SHELL) for yaw in radial(6, 10)]
    return out + [part('happy_villager', '~ ~0.6 ~', (1.5, 0.4, 1.5), 0, 8), flash(YELLOW_BEAM, '~ ~0.6 ~', 0.8)]


@preset('leaf_ring', 'Leaf cards circling the surfacing decal (Q3s t26-36): 8 leaves on r 3.6 shown around the ring one '
        'after another. At the floor point.')
def _p_leaf_ring():
    out = []
    for k, yaw in enumerate(radial(8, 0)):
        x, z = ring_xz(3.4, yaw)
        out.append(card('leaf', p3(x, 0.35, z, '~'), bb='center', spin=150, s0=0.3, s1=0.55, move=(0, 0.3, 0), life=10,
                        fade=4, dly=k, col=LIME_PALE if k % 2 else LEAF_PALE))
    return out


@preset('surface_splash', 'The surfacing splash (Q3s t36). At the floor point.')
def _p_surface_splash():
    rnd = RND(37)
    out = [card('splash', '~ ~0.02 ~', bb='vertical', s0=1.4, s1=3.8, life=10, fade=4, dur=4, col=TEAL_FOAM),
           card('splash', '~ ~0.02 ~', bb='vertical', roll=-8, s0=1.0, s1=2.8, life=9, fade=4, dur=3, col=WHITE, dly=1),
           card('ripple', '~ ~0.06 ~', '~ 90', s0=1.0, s1=5.0, life=12, fade=5, dur=6, col=TEAL_FOAM)]
    out += [fly('leaf', yaw, rnd.uniform(45, 70), rnd.uniform(1.6, 2.4), h=0.5, s0=0.3, s1=0.5, life=12, fade=5,
                col=LIME_PALE) for yaw in radial(4, 20)]
    return out + [part('splash', '~ ~0.4 ~', (1.2, 0.3, 1.2), 0.3, 20)]


@preset('light_band', 'The horizontal light band of the flat surfacing shot over {len} (Q3s t46). At the muzzle anchor, '
        'rotated = the shot.', ('len',), (('h', 'len', 0.05), ('L', 'len', 0.1)))
def _p_light_band():
    return [mac(card('streak', '^ ^ ^$(h)', '~90 0', s0=(0.5, 10, 1), s1=('$(L)', 14, 1), life=6, fade=3, dur=2, col=YELLOW_BEAM)),
            mac(card('streak', '^ ^ ^$(h)', '~90 90', s0=(0.5, 10, 1), s1=('$(L)', 14, 1), life=6, fade=3, dur=2, col=SHELL)),
            card('glow', bb='center', s0=0.6, s1=2.4, life=5, fade=3, col=YELLOW_BEAM)]


@preset('glitter_shower', 'A glitter shower over the body (Q4 t53). At the body.')
def _p_glitter_shower():
    return [card('glint', p3(x, y, z, '~'), bb='center', spin=60, s0=0.3, s1=0.8, move=(0, -2.0, 0), life=12, fade=5,
                 col=rgb('#EBF898'), dly=k)
            for k, (x, y, z) in enumerate(((1.2, 5.0, 0.4), (-1.0, 5.6, -0.6), (0.4, 6.0, 1.1), (-0.5, 4.6, 0.9)))] + \
        [part('wax_on', '~ ~4 ~', (2.0, 1.5, 2.0), 0, 16), part('end_rod', '~ ~4 ~', (1.5, 1.5, 1.5), 0.02, 6)]


@preset('charge_streaks', 'Charge streaks converging on the body (Q5 t10-19). At the body.')
def _p_charge_streaks():
    rnd = RND(38)
    out = []
    for k, yaw in enumerate(radial(6, 15)):
        el = rnd.uniform(-20, 40)
        out.append(card('streak', '~ ~3.2 ~', f'~{ang(yaw)} {ang(90 - el)}', roll=90, s0=(2.0, 6, 1), s1=(1.0, 6, 1),
                        off=(0, 4.0, 0), move=(0, -3.4, 0), life=8, fade=2, dur=6,
                        col=[rgb('#A9D57C'), rgb('#CDE78A'), rgb('#D1EAC2')][k % 3], dly=k % 2))
    return out + [dust(rgb('#CDE78A'), 1.0, '~ ~3.2 ~', (2.0, 1.5, 2.0), 8)]


@preset('star_flare', 'A 4-point star flare at the glint (Q5 t37 / t43). At the glint point.')
def _p_star_flare():
    return [card('glint', bb='center', spin=45, s0=0.5, s1=4.0, life=6, fade=3, col=rgb('#E6F8A5')),
            card('glow', bb='center', s0=0.6, s1=2.6, life=6, fade=3, col=rgb('#F6FBDE')),
            part('end_rod', '~ ~ ~', (0.3, 0.3, 0.3), 0.1, 6)]


HELIX_STEPS = 8


@preset('helix_trail', 'The double-helix ribbon behind a seed orb (Q5 t42-55, every tick; particles only): two sine '
        'strands, dust #E7F99F -> #8BCAAA, the phase turning 45 degrees a tick. At the orb, rotated as its flight.')
def _p_helix_trail():
    out = ['execute store result score #wkNow mb run time query gametime', f'scoreboard players set #wk8 mb {HELIX_STEPS}',
           'scoreboard players operation #wkPh mb = #wkNow mb', 'scoreboard players operation #wkPh mb %= #wk8 mb']
    for k in range(HELIX_STEPS):
        t = 2 * math.pi * k / HELIX_STEPS
        for s in (0, math.pi):
            x, y = 0.3 * math.cos(t + s), 0.3 * math.sin(t + s)
            out.append(f'execute if score #wkPh mb matches {k} run particle minecraft:dust_color_transition'
                       f'{{from_color:{colour_list(HELIX[0])},to_color:{colour_list(HELIX[1])},scale:0.8}} '
                       f'^{num(x, 3)} ^{num(y, 3)} ^ 0 0 0 0 1 force @a[tag=player]')
    return out


@preset('orb_impact', 'A seed-orb landing: a star burst and two upthrust crystal / leaf spikes (Q5 t49 / t55). At the '
        'floor point.')
def _p_orb_impact():
    return [card('glint', '~ ~0.6 ~', bb='center', spin=45, s0=0.5, s1=3.0, life=5, fade=2, col=rgb('#EDF597')),
            card('leaf_blade', '~0.3 ~ ~0.1', bb='vertical', roll=-12, s0=0.3, s1=1.6, life=5, fade=2, dur=2, col=rgb('#D9E674')),
            card('leaf_blade', '~-0.3 ~ ~-0.1', bb='vertical', roll=14, s0=0.3, s1=1.3, life=5, fade=2, dur=2, col=rgb('#C4D353')),
            part('happy_villager', '~ ~0.5 ~', (0.8, 0.3, 0.8), 0, 4), dust(rgb('#F6FBC2'), 1.0, '~ ~0.4 ~', (0.6, 0.3, 0.6), 4)]


@preset('leaf_skim', 'Two skimming pale-yellow leaf blades along the lane of length {len} (Q5 t64). At the lane start, '
        'rotated = the aim.', ('len',), (('L', 'len', 0.1), ('h', 'len', 0.05)))
def _p_leaf_skim():
    return [mac(card('leaf_blade', '^0.55 ^0.35 ^', '~ 90', s0=(1.0, 2.0, 1), s1=(1.0, 2.2, 1), off=(0, 0.6, 0),
                     move=(0, '$(L)', 0), life=10, fade=2, dur=8, col=rgb('#F4F6B0'))),
            mac(card('leaf_blade', '^-0.55 ^0.35 ^', '~ 90', s0=(1.0, 2.0, 1), s1=(1.0, 2.2, 1), off=(0, 0.6, 0),
                     move=(0, '$(L)', 0), life=10, fade=2, dur=8, col=rgb('#E8F09A'), dly=1)),
            mac(card('streak', '^ ^0.4 ^$(h)', '~90 0', s0=(1, 4, 1), s1=('$(L)', 5, 1), life=8, fade=4, dur=6, col=rgb('#F4F6B0')))]


@preset('leaf_dissolve', 'A white leaflet burst as the body dissolves (D t100-118, every 6 t). At the body.')
def _p_leaf_dissolve():
    rnd = RND(39)
    return [card('leaf', p3(rnd.uniform(-1.4, 1.4), rnd.uniform(0.6, 3.2), rnd.uniform(-1.4, 1.4)), bb='center',
                 spin=rnd.choice((-140, 140)), s0=0.3, s1=0.5, move=(0, rnd.uniform(1.0, 1.8), 0), life=14, fade=6,
                 col=rgb('#F4F8E8'), dly=k) for k in range(5)] + [part('white_ash', '~ ~2 ~', (1.5, 1.5, 1.5), 0, 12)]


@preset('haze_withered', 'The withered olive haze drift (phase 1, T1, phase 2; every 10 t; particles only). At the floor centre.')
def _p_haze_withered():
    return [dust(rgb('#8A8A3A'), 2.4, '~ ~2 ~', (13, 2.0, 13), 8), dust(rgb('#C9C452'), 1.0, '~ ~1.5 ~', (12, 1.5, 12), 5)]


@preset('haze_lush', 'The lush spore and glint haze (from CS t64; every 10 t; particles only). At the floor centre.')
def _p_haze_lush():
    return [part('spore_blossom_air', '~ ~3 ~', (13, 3, 13), 0, 6), part('happy_villager', '~ ~1.5 ~', (12, 1.5, 12), 0, 3)]


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


HEADER = '# Generated by tools/build_mboss_ap_fx.py (아펩의 오아시스 파수꾼 fx kit) - edit the generator, not this file.\n'
E = FN + 'e/'
SEL = f'@e[type=minecraft:item_display,tag={TAG}'
DEF_A = 'tg:"rlk_wk_c",tpd:0'          # storage a defaults: an extra tag, teleport_duration
# card pools (#wkTel): 0 fx, 1 attack telegraph, 3 flood; the dressing pool is spawned apart (dress/e/*)
POOL_FX, POOL_TELE, POOL_FLOOD = 0, 1, 3
FAKE = ('#wkInit', '#wkN', '#wkTN', '#wkDN', '#wkFN', '#wkNow', '#wkWd', '#wkC2', '#wkRoll', '#wkSpin', '#wkLife', '#wkFade',
        '#wkDly', '#wkDur', '#wkHit', '#wkTel', '#wkTr', '#wkTr0', '#wkTa', '#wkTl', '#wkTw', '#wkTb', '#wkTd', '#wkTell',
        '#wkTEl', '#wkTnd', '#wkThold', '#wkTn', '#wkTe', '#wkTi', '#wkTq', '#wkTP', '#wkTW', '#wkTk', '#wkTx', '#wkTs', '#wkTA0',
        '#wkMinus1', '#wkPh', '#wk3', '#wk4', '#wk8', '#wk20', '#wkAr', '#wkAa', '#wkAd', '#wkAx', '#wkAl', '#wkFl',
        '#wkDemo', '#wkDT', '#wkHv', '#wkHk', '#wkBan', '#wkSp')


def engine(W):
    W.w('card', [
        '# Spawn one painted card at pos, rotated rot (fixed cards), seen from the executing context.',
        '# {kind, pos:"^x ^y ^z", rot:"~ ~", bb:fixed|center|vertical|horizontal, roll:<deg, about local z>,',
        '#  spin:<deg over the main interpolation, -170..170, about the card normal (y for flat / cross / band / box)>,',
        '#  s0:<start size>, s1:<end size>, move:"dx,dy,dz" (end offset, display frame: +x left, +y up, +z forward),',
        '#  life:<ticks>, fade:<shrink-out ticks>, col:<RGB int tint, 16777215 = the painted colours>}. ap_fx_api.md §2.',
        f'# Skipped (no error) while {CAP} fx cards are alive.',
        f'execute if score #wkN mb matches {CAP}.. run return 0',
        f'$data modify storage {STO} a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)f,$(s0)f,$(s0)f",s1:"$(s1)f,$(s1)f,$(s1)f",off:"0f,0f,0f",move:"$(move)",col:$(col),col2:-1,'
        f'ax:"0f,0f,1f",{DEF_A}}}',
        f'execute unless data storage {STO} ax.leaf run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #wkRoll mb $(roll)',
        '$scoreboard players set #wkSpin mb $(spin)',
        '$scoreboard players set #wkLife mb $(life)',
        '$scoreboard players set #wkFade mb $(fade)',
        'scoreboard players set #wkDly mb 0',
        'scoreboard players set #wkDur mb 0',
        'scoreboard players set #wkHit mb -1',
        f'scoreboard players set #wkTel mb {POOL_FX}',
        f'function {E}make',
    ])
    W.w('cardx', [
        '# card with every option: s0 / s1 as "xf,yf,zf" vectors, off:"xf,yf,zf" (static start translation), move',
        '# (the END translation), dly:<ticks hidden before it shows>, dur:<ticks of the main interpolation, 0 = up to',
        '# the fade>, hit:<ticks after the call when the tint becomes col2, -1 = never>, col2:<RGB int>. Same cap.',
        f'execute if score #wkN mb matches {CAP}.. run return 0',
        f'$data modify storage {STO} a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)",s1:"$(s1)",off:"$(off)",move:"$(move)",col:$(col),col2:$(col2),ax:"0f,0f,1f",' + DEF_A + '}',
        f'execute unless data storage {STO} ax.leaf run function {E}axes',
        f'$data modify storage {STO} a.ax set from storage {STO} ax.$(kind)',
        '$scoreboard players set #wkRoll mb $(roll)',
        '$scoreboard players set #wkSpin mb $(spin)',
        '$scoreboard players set #wkLife mb $(life)',
        '$scoreboard players set #wkFade mb $(fade)',
        '$scoreboard players set #wkDly mb $(dly)',
        '$scoreboard players set #wkDur mb $(dur)',
        '$scoreboard players set #wkHit mb $(hit)',
        f'scoreboard players set #wkTel mb {POOL_FX}',
        f'function {E}make',
    ])
    W.w('e/make', [
        f'# Internal: storage {STO} a (kind pos rot bb s0 s1 off move col col2 ax tg tpd) + #wkRoll #wkSpin #wkLife',
        '# #wkFade #wkDly #wkDur #wkHit #wkTel (the pool: 0 fx, 1 attack telegraph, 3 flood) -> one card. The stage',
        '# clock is gametime + 1 (the fg kit\'s first-tick fix): the ager (fx/e/world, a 1t schedule) runs at the END of',
        '# this server tick with gametime already + 1, so the main interpolation starts in the next server tick and the',
        '# client animates it. Stages: shows at clock + dly, interpolates from clock + dly + 1 over dur ticks, recolours',
        '# at clock + hit, shrinks over the last fade ticks, removed at clock + dly + life.',
        f'execute unless score #wkInit mb matches 1 run function {E}init',
        f'execute if score #wkTel mb matches {POOL_TELE} run scoreboard players add #wkTN mb 1',
        f'execute if score #wkTel mb matches {POOL_FX} run scoreboard players add #wkN mb 1',
        f'execute if score #wkTel mb matches {POOL_FLOOD} run scoreboard players add #wkFN mb 1',
        'execute if score #wkLife mb matches ..1 run scoreboard players set #wkLife mb 2',
        'execute if score #wkFade mb matches ..-1 run scoreboard players set #wkFade mb 0',
        'execute if score #wkDly mb matches ..-1 run scoreboard players set #wkDly mb 0',
        'scoreboard players operation #wkWd mb = #wkLife mb',
        'scoreboard players remove #wkWd mb 2',
        'scoreboard players operation #wkFade mb < #wkWd mb',
        'scoreboard players operation #wkWd mb = #wkLife mb',
        'scoreboard players operation #wkWd mb -= #wkFade mb',
        'scoreboard players remove #wkWd mb 1',
        'execute if score #wkDur mb matches 1.. run scoreboard players operation #wkWd mb = #wkDur mb',
        'execute if score #wkWd mb matches ..0 run scoreboard players set #wkWd mb 1',
        'execute if score #wkSpin mb matches 171.. run scoreboard players set #wkSpin mb 170',
        'execute if score #wkSpin mb matches ..-171 run scoreboard players set #wkSpin mb -170',
        f'execute store result storage {STO} a.rr float 0.017453292 run scoreboard players get #wkRoll mb',
        f'execute store result storage {STO} a.sr float 0.017453292 run scoreboard players get #wkSpin mb',
        f'execute store result storage {STO} a.d int 1 run scoreboard players get #wkWd mb',
        f'execute store result storage {STO} a.f int 1 run scoreboard players get #wkFade mb',
        f'execute store result score #wkC2 mb run data get storage {STO} a.col2',
        f'data modify storage {STO} a.z set from storage {STO} a.s0',
        f'execute if score #wkDly mb matches 1.. run data modify storage {STO} a.z set value "0f,0f,0f"',
        f'function {E}spawn with storage {STO} a',
        f'execute if score #wkTel mb matches {POOL_TELE} run tag {SEL}_new] add {TAG}_t',
        f'execute if score #wkTel mb matches {POOL_FLOOD} run tag {SEL}_new] add {TAG}_fl',
        'execute store result score #wkNow mb run time query gametime',
        'scoreboard players add #wkNow mb 1',
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
        'wkS:{start_interpolation:0,interpolation_duration:0,transformation:{scale:[$(s0)]}},'
        'wkG:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'wkF:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}},'
        'wkC:$(col2)}}}}',
        f'$execute positioned $(pos) rotated $(rot) run tp {SEL}_new,limit=1] ~ ~ ~ ~ ~',
    ])
    W.w('e/born', [
        '# Internal, as the new card: stage clock values (gametime + 1 based) in wkS wkG wkH wkK wkD.',
        'scoreboard players operation @s wkS = #wkNow mb',
        'scoreboard players operation @s wkS += #wkDly mb',
        'scoreboard players operation @s wkG = @s wkS',
        'scoreboard players add @s wkG 1',
        'scoreboard players operation @s wkD = @s wkS',
        'scoreboard players operation @s wkD += #wkLife mb',
        'scoreboard players operation @s wkK = @s wkD',
        'scoreboard players operation @s wkK -= #wkFade mb',
        'scoreboard players operation @s wkH = #wkNow mb',
        'scoreboard players operation @s wkH += #wkHit mb',
        f'tag @s add {TAG}_go',
        f'execute if score #wkDly mb matches 1.. run tag @s add {TAG}_sh',
        f'execute if score #wkFade mb matches 1.. run tag @s add {TAG}_fd',
        f'execute if score #wkHit mb matches 0.. if score #wkC2 mb matches 0.. run tag @s add {TAG}_hit',
    ])
    W.w('e/world', [
        '# Ages the kit\'s cards once per tick while any is alive (scheduled from e/make, the dressing pool and itself,',
        '# so it runs at the end of the server tick; no hook in rlk:tick). A dead or reviving player clears the fx,',
        '# telegraph and flood cards (fx/clear; the phase-2 dressing pool stays). The dressing pool is never aged: its',
        '# ley strips pulse (their width breathes over 20 t).',
        f'execute unless entity {SEL},limit=1] run return run function {E}zero',
        f'execute if entity @a[tag=player,scores={{dead=1}}] if entity {SEL},tag=!{TAG}_d,limit=1] run function {FN}clear',
        f'execute if entity @a[tag=player,scores={{rnDie=1..}}] if entity {SEL},tag=!{TAG}_d,limit=1] run function {FN}clear',
        'execute store result score #wkNow mb run time query gametime',
        f'execute as {SEL},tag=!{TAG}_d] run function {E}age',
        f'execute if score #wkDN mb matches 1.. run function {FN}dress/e/pulse',
        f'execute store result score #wkN mb if entity {SEL},tag=!{TAG}_t,tag=!{TAG}_d,tag=!{TAG}_fl]',
        f'execute store result score #wkTN mb if entity {SEL}_t]',
        f'execute store result score #wkFN mb if entity {SEL}_fl]',
        f'execute store result score #wkDN mb if entity {SEL}_d]',
        f'execute if entity {SEL},limit=1] run schedule function {E}world 1t replace',
    ])
    W.w('e/zero', ['scoreboard players set #wkN mb 0', 'scoreboard players set #wkTN mb 0',
                   'scoreboard players set #wkFN mb 0', 'scoreboard players set #wkDN mb 0'])
    W.w('e/age', [
        '# As one card (the stage clock in #wkNow).',
        'execute unless score @s wkD = @s wkD run return run kill @s',
        'execute if score #wkNow mb >= @s wkD run return run kill @s',
        f'execute if entity @s[tag={TAG}_sh] if score #wkNow mb >= @s wkS run function {E}show',
        f'execute if entity @s[tag={TAG}_go] if score #wkNow mb >= @s wkG run function {E}go',
        f'execute if entity @s[tag={TAG}_hit] if score #wkNow mb >= @s wkH run function {E}hit',
        f'execute if entity @s[tag={TAG}_fd] if score #wkNow mb >= @s wkK run function {E}fade',
    ])
    W.w('e/show', ['# a delayed card appears at its start size',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".wkS',
                   f'tag @s remove {TAG}_sh'])
    W.w('e/go', ['# start -> end transformation over dur ticks (client interpolation)',
                 'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".wkG',
                 f'tag @s remove {TAG}_go'])
    W.w('e/hit', ['# the tint changes (telegraph flash on the hit tick)',
                  'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set from entity @s '
                  'item.components."minecraft:custom_data".wkC',
                  f'tag @s remove {TAG}_hit'])
    W.w('e/fade', ['# shrink to nothing over the last fade ticks',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".wkF',
                   f'tag @s remove {TAG}_fd'])
    W.w('e/init', ['# Objectives and constants of the kit (made on the first card; removed by fx/uninstall).',
                   *[f'scoreboard objectives add {o} dummy' for o in OBJECTIVES],
                   'scoreboard players set #wkInit mb 1', 'scoreboard players set #wkMinus1 mb -1',
                   'scoreboard players set #wk3 mb 3', 'scoreboard players set #wk4 mb 4', 'scoreboard players set #wk8 mb 8',
                   'scoreboard players set #wk20 mb 20',
                   'scoreboard players set #wkN mb 0', 'scoreboard players set #wkTN mb 0',
                   'scoreboard players set #wkFN mb 0', 'scoreboard players set #wkDN mb 0'])
    W.w('clear', ['# Remove every kit card (fx, attack telegraphs, waves, rims, rings, the flood pool; NOT the dressing',
                  '# pool: fx/dress/clear). Safe to call any time.',
                  f'kill {SEL},tag=!{TAG}_d]', 'scoreboard players set #wkN mb 0', 'scoreboard players set #wkTN mb 0',
                  'scoreboard players set #wkFN mb 0'])
    W.w('uninstall', ['# Remove the kit\'s cards (both pools too), the demo anchor, objectives, fake players, storage and',
                      '# schedules (call from the module\'s uninstall hook).',
                      f'kill {SEL}]', 'kill @e[tag=rlk_wk_demo]',
                      *[f'scoreboard objectives remove {o}' for o in OBJECTIVES],
                      *[f'scoreboard players reset {s} mb' for s in FAKE],
                      f'data remove storage {STO} a', f'data remove storage {STO} t', f'data remove storage {STO} pa',
                      f'data remove storage {STO} pf', f'data remove storage {STO} hud', f'data remove storage {STO} ax',
                      f'data remove storage {STO} dress',
                      f'schedule clear {E}world', f'schedule clear {FN}hud/e/banner_tick', f'schedule clear {FN}test/e/tick'])
    spin_y = ','.join(f'{k}:"0f,1f,0f"' for k in ALL_KINDS if kind_info(k)[0] in SPIN_Y)
    W.w('e/axes', ['# Spin axis (= the card normal / long axis) of the flat, cross, band and box kinds; face kinds keep z',
                   '# (the default of storage a; ax.leaf marks the table as made).',
                   f'data modify storage {STO} ax set value {{{spin_y}}}',
                   f'data modify storage {STO} ax.leaf set value "0f,0f,1f"'])
    W.w('look', [
        '# Dress @s (an item_display the module owns) as a kit sprite: {kind, col:<RGB int>}. Full bright; the caller',
        '# keeps its own transformation / billboard.',
        '$data merge entity @s {item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        f'"{NS_TEX}$(kind)","minecraft:custom_model_data":{{colors:[$(col)]}}}}}},brightness:{{sky:15,block:15}}}}',
    ])


# ----------------------------------------------------------------------------- telegraphs
T = FN + 'tele/e/'
PIECE_MAX = 32                    # widest piece (degrees) above SMALL_R; a shape of F degrees is ceil(F / 32) pieces
PIECE_MAX_SMALL = 64              # widest piece at radii <= SMALL_R (the dip stays <= 0.14 b there)
SMALL_R = 3.5                     # blocks: thick rims, wide pieces and the one-piece edged sector rim at or below it


def piece_k_coeffs():
    """per family width W: (lo, hi, A, B, W) with the piece width P (tenths of a degree) in (lo, hi] and the card's x
    squeeze k(P) = tan(P / 2) / tan(W / 2) ~= (A + B P) / 1e6 (k(hi) = 1 exactly, k(lo) within 0.01 %; tan is convex so
    the line is within 0.02 % between)"""
    out = []
    lo = 0
    for w in P.PIECES:
        hi = w * 10
        tw = math.tan(math.radians(w / 2))
        k_lo = math.tan(math.radians(lo / 20)) / tw
        b = round((1.0 - k_lo) / (hi - lo) * 1e6)
        a = 1_000_000 - b * hi
        out.append((lo, hi, a, b, w))
        lo = hi
    return out


def piece_geometry(f_deg, r=7.2, a0=0.0):
    """Python mirror of the fan drawing (renderer, tests): [(bearing deg, W, k)] for a shape a0 .. a0 + f_deg of radius
    r blocks"""
    f10 = int(round(f_deg * 10))
    m10 = (PIECE_MAX_SMALL if r <= SMALL_R + 1e-9 else PIECE_MAX) * 10
    n = (f10 + m10 - 1) // m10
    p10 = f10 // n
    for lo, hi, a, b, w in piece_k_coeffs():
        if lo < p10 <= hi or (w == P.PIECES[0] and p10 <= lo):
            k = (a + b * p10) / 1e6
            break
    return [((int(round(a0 * 10)) + (f10 * (2 * i + 1)) // (2 * n)) / 10, w, k) for i in range(n)]


def sector_cards(r, a):
    """attack-telegraph cards of tele/sector (r blocks, half-angle a degrees)"""
    if a >= 175:
        return 2
    n = len(piece_geometry(2 * a, r))
    return 2 if n == 1 and r <= SMALL_R + 1e-9 else 2 * n + 2


def telegraphs(W):
    cols = []
    for el, (c1, c2, c3) in sorted(TELE_COL.items()):
        cols.append(f'execute if score #wkTEl mb matches {el} run data modify storage {STO} t merge value '
                    f'{{c1:{c1},c2:{c2},c3:{c3}}}')
    d1, d2, d3 = TELE_COL[TELE_DEFAULT]
    W.w('tele/e/prep', [
        '# Internal: common telegraph setup from #wkTell #wkTEl #wkTnd #wkThold (palettes by el: 7 Dendro, 20 gold,',
        '# 22 target, 23 olive, 24 field; anything else draws Dendro; nd >= 1 turns the rim the undodgeable red).',
        '# Life = tell + hold + 1; the fill grows over tell - 1 ticks from the tick after the call, so its edge reaches',
        '# the rim on call + tell (the framework hz strike tick when both are made in the same tick with the same',
        '# tell); every card flashes (col2) on that tick.',
        f'execute unless score #wkInit mb matches 1 run function {E}init',
        'execute if score #wkTell mb matches ..1 run scoreboard players set #wkTell mb 2',
        'execute if score #wkThold mb matches ..-1 run scoreboard players set #wkThold mb 0',
        f'data modify storage {STO} t set value {{c1:{d1},c2:{d2},c3:{d3},tg:"rlk_wk_c",tpd:0}}',
        *cols,
        f'execute if score #wkTnd mb matches 1.. run data modify storage {STO} t.c1 set value {ND_RIM}',
        'scoreboard players operation #wkLife mb = #wkTell mb',
        'scoreboard players operation #wkLife mb += #wkThold mb',
        'scoreboard players add #wkLife mb 1',
        'scoreboard players operation #wkDur mb = #wkTell mb',
        'scoreboard players remove #wkDur mb 1',
        'scoreboard players operation #wkHit mb = #wkTell mb',
        'scoreboard players set #wkFade mb 0',
        'scoreboard players set #wkDly mb 0',
        'scoreboard players set #wkRoll mb 0',
        'scoreboard players set #wkSpin mb 0',
        f'scoreboard players set #wkTel mb {POOL_TELE}',
    ])

    def head(extra, el=True, nd=True, need=2):
        """the cap guard (no shape is half drawn) and the common arguments"""
        lines = [f'execute if score #wkTN mb matches {min(TCAP - TSKIP, TCAP - need + 1)}.. run return 0',
                 '$scoreboard players set #wkTell mb $(tell)']
        lines.append('$scoreboard players set #wkTEl mb $(el)' if el else 'scoreboard players set #wkTEl mb 7')
        lines.append('$scoreboard players set #wkTnd mb $(nd)' if nd else 'scoreboard players set #wkTnd mb 0')
        lines += ['$scoreboard players set #wkThold mb $(hold)', *extra, f'function {T}prep']
        return lines

    def mk(kind, pos, s0, s1, colkey, rot='~ 0', off='0f,0f,0f', move=None, flash=True, tg='$(tg)', col2=None):
        """one telegraph card inside a macro reading storage t (static cards have s0 = s1)"""
        mv = move if move is not None else off
        c2 = col2 if col2 is not None else ('$(c3)' if flash else '-1')
        col = f'$({colkey})' if not str(colkey).isdigit() else colkey
        return [f'$data modify storage {STO} a set value {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"fixed",'
                f's0:"{s0}",s1:"{s1}",off:"{off}",move:"{mv}",col:{col},col2:{c2},ax:"0f,1f,0f",'
                f'tg:"{tg}",tpd:$(tpd)}}',
                f'function {E}make']

    def fan_n():
        """#wkTn = ceil(#wkTa / M) with M = 320 tenths, or 640 at r <= SMALL_R"""
        return [f'scoreboard players set #wkTx mb {PIECE_MAX * 10}',
                f'execute if score #wkTr mb matches ..{int(SMALL_R * 10)} run scoreboard players set #wkTx mb {PIECE_MAX_SMALL * 10}',
                'scoreboard players operation #wkTn mb = #wkTa mb', 'scoreboard players operation #wkTn mb += #wkTx mb',
                'scoreboard players remove #wkTn mb 1', 'scoreboard players operation #wkTn mb /= #wkTx mb']

    jump = ['execute if score #wkTnd mb matches 2 run function ' + T + 'jump with storage ' + STO + ' t']
    W.w('tele/e/jump', ['# Internal (macro, storage t): the jump chevron of nd 2 at the decal centre (tinted the rim).',
                        *mk('t_jump', '~ ~0.05 ~', '0.6f,1f,0.6f', '1.3f,1f,1.3f', 'c1')])
    # --- disc
    W.w('tele/disc', [
        '# Disc decal: {r:<radius, tenths>, tell:<ticks to the hit>, el, nd, hold:<ticks after the hit>}. At the floor',
        '# point. Visual only: pair it with hz/disc (same tell, #hzQuiet 1). 2 cards (+1 with nd 2).',
        *head(['$scoreboard players set #wkTr mb $(r)'], need=3),
        'execute if score #wkTr mb matches ..1 run scoreboard players set #wkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #wkTr mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #wkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}disc with storage {STO} t',
        *jump,
    ])
    W.w('tele/e/disc', [
        '# Internal (macro, storage t): the progress fill (0 -> r) under the static rim.',
        *mk('t_fill', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(r)f,1f,$(r)f', 'c2'),
        *mk('$(rim)', '~ ~0.045 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', 'c1'),
    ])
    # --- the fan of pieces (sector, wedge)
    sel = []
    for lo, hi, a, b, w in piece_k_coeffs():
        cond = f'{lo + 1}..{hi}' if lo else f'..{hi}'
        sel.append(f'execute if score #wkTP mb matches {cond} run function {T}kw{w}')
        pa = f't_pa{w}' if w in P.PIECES_NARROW else f't_pas{w}'
        W.w(f'tele/e/kw{w}', [f'# Internal: pieces of family width {w} deg: k(P) = ({a} + {b} P) / 1e6 (P in tenths).',
                              f'scoreboard players set #wkTW mb {w}', f'scoreboard players set #wkTk mb {b}',
                              'scoreboard players operation #wkTk mb *= #wkTP mb',
                              f'scoreboard players {"add" if a >= 0 else "remove"} #wkTk mb {abs(a)}',
                              f'data modify storage {STO} t merge value {{pf:"t_pf{w}",pa:"{pa}",pas:"t_pas{w}",pe:"t_pe{w}"}}'])
    W.w('tele/e/fan', [
        '# Internal: draw the fan from #wkTA0 (start, tenths of a degree relative to the executor yaw) over #wkTa',
        '# (the full angle, tenths) with radius #wkTr (and inner #wkTr0 when >= 10): n = ceil(F / M) equal pieces of',
        f'# width P (M = {PIECE_MAX} deg, {PIECE_MAX_SMALL} at r <= {SMALL_R}), each the family piece W >= P squeezed across by',
        '# k = tan(P / 2) / tan(W / 2), so the drawn edges are exactly P apart and every arc stays at or inside the',
        '# radius (ap_fx_api.md §3.2). #wkTe 0 = a one-piece small sector: its rim piece carries both edges.',
        *fan_n(),
        'scoreboard players operation #wkTP mb = #wkTa mb', 'scoreboard players operation #wkTP mb /= #wkTn mb',
        *sel,
        f'data modify storage {STO} t.pr set from storage {STO} t.pa',
        f'execute if score #wkTr mb matches ..{int(SMALL_R * 10)} run data modify storage {STO} t.pr set from storage {STO} t.pas',
        f'execute if score #wkTe mb matches 0 run data modify storage {STO} t.pr set from storage {STO} t.pe',
        'scoreboard players operation #wkTs mb = #wkTk mb', 'scoreboard players operation #wkTs mb *= #wkTr mb',
        f'execute store result storage {STO} t.sx float 0.0000001 run scoreboard players get #wkTs mb',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #wkTr mb',
        'scoreboard players operation #wkTs mb = #wkTk mb', 'scoreboard players operation #wkTs mb *= #wkTr0 mb',
        f'execute store result storage {STO} t.sx0 float 0.0000001 run scoreboard players get #wkTs mb',
        f'execute store result storage {STO} t.r0 float 0.1 run scoreboard players get #wkTr0 mb',
        f'data modify storage {STO} t.f0 set value "0.01f,1f,0.01f"',
        f'execute if score #wkTr0 mb matches 10.. run function {T}fan_f0 with storage {STO} t',
        'scoreboard players set #wkTi mb 0',
        f'function {T}fan_loop',
    ])
    W.w('tele/e/fan_f0', ['# Internal (macro): an annular wedge\'s fill starts at the inner radius.',
                          f'$data modify storage {STO} t.f0 set value "$(sx0)f,1f,$(r0)f"'])
    W.w('tele/e/fan_loop', [
        '# Internal: piece #wkTi of #wkTn at bearing A0 + F (2 i + 1) / (2 n) (tenths of a degree).',
        'scoreboard players operation #wkTq mb = #wkTi mb', 'scoreboard players operation #wkTq mb += #wkTi mb',
        'scoreboard players add #wkTq mb 1', 'scoreboard players operation #wkTq mb *= #wkTa mb',
        'scoreboard players operation #wkTx mb = #wkTn mb', 'scoreboard players operation #wkTx mb += #wkTn mb',
        'scoreboard players operation #wkTq mb /= #wkTx mb', 'scoreboard players operation #wkTq mb += #wkTA0 mb',
        f'execute store result storage {STO} t.b float 0.1 run scoreboard players get #wkTq mb',
        f'function {T}piece with storage {STO} t',
        f'execute if score #wkTr0 mb matches 10.. run function {T}piece_in with storage {STO} t',
        'scoreboard players add #wkTi mb 1',
        f'execute if score #wkTi mb < #wkTn mb run function {T}fan_loop',
    ])
    W.w('tele/e/piece', ['# Internal (macro, storage t): one fill piece (growing f0 -> full) and its rim-arc piece.',
                         *mk('$(pf)', '~ ~0.035 ~', '$(f0)', '$(sx)f,1f,$(r)f', 'c2', rot='~$(b) 0'),
                         *mk('$(pr)', '~ ~0.045 ~', '$(sx)f,1f,$(r)f', '$(sx)f,1f,$(r)f', 'c1', rot='~$(b) 0')])
    W.w('tele/e/piece_in', ['# Internal (macro, storage t): the inner rim-arc piece of an annular wedge.',
                            *mk('$(pr)', '~ ~0.046 ~', '$(sx0)f,1f,$(r0)f', '$(sx0)f,1f,$(r0)f', 'c1', rot='~$(b) 0')])
    W.w('tele/e/edges', ['# Internal (macro, storage t): the two radial edge bars of a sector, each just inside its edge.',
                         *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(r)f', '0.24f,1f,$(r)f', 'c1', rot='~$(e0) 0',
                             off='-0.12f,0f,0f'),
                         *mk('t_bar', '~ ~0.046 ~', '0.24f,1f,$(r)f', '0.24f,1f,$(r)f', 'c1', rot='~$(e1) 0',
                             off='0.12f,0f,0f')])

    def fan_need():
        """#wkTq = #wkTN + the cards the fan will make (2 per piece, + 1 per piece with an inner rim)"""
        return [*fan_n(), 'scoreboard players operation #wkTq mb = #wkTn mb', 'scoreboard players operation #wkTq mb += #wkTn mb',
                'execute if score #wkTr0 mb matches 10.. run scoreboard players operation #wkTq mb += #wkTn mb',
                'scoreboard players operation #wkTq mb += #wkTN mb']
    W.w('tele/sector', [
        '# Sector decal: {r (tenths), a:<half-angle, any integer 1..180, drawn within 1 degree>, tell, el, nd, hold}.',
        '# At the apex, rotated = the aim (yaw). a >= 175 draws a disc. Fill + rim-arc pieces (2 per 32 degrees, 64 at',
        f'# r <= {SMALL_R}) and two edge bars; a one-piece sector of r <= {SMALL_R} paints its edges into the rim: a 78-degree',
        '# P6 hit 1 (r 7.2) is 12 cards, the 27-degree O1 cone (r 3.1) and the 24-degree O6b bite 2. Skipped when it',
        '# would pass the cap.',
        *head(['$scoreboard players set #wkTr mb $(r)', '$scoreboard players set #wkTa mb $(a)'], need=2),
        'execute if score #wkTa mb matches 175.. run return run function ' + T + 'sector_disc with storage ' + STO + ' t',
        'execute if score #wkTa mb matches ..0 run scoreboard players set #wkTa mb 1',
        'execute if score #wkTr mb matches ..1 run scoreboard players set #wkTr mb 2',
        'scoreboard players set #wkTr0 mb 0',
        # A0 = -10 a, F = 20 a (tenths)
        'scoreboard players operation #wkTA0 mb = #wkTa mb', 'scoreboard players operation #wkTA0 mb *= #wkMinus1 mb',
        'scoreboard players set #wkTx mb 10', 'scoreboard players operation #wkTA0 mb *= #wkTx mb',
        f'execute store result storage {STO} t.e0 float -1 run scoreboard players get #wkTa mb',
        f'execute store result storage {STO} t.e1 float 1 run scoreboard players get #wkTa mb',
        'scoreboard players set #wkTx mb 20', 'scoreboard players operation #wkTa mb *= #wkTx mb',
        *fan_need(),
        'scoreboard players set #wkTe mb 1',
        f'execute if score #wkTn mb matches 1 if score #wkTr mb matches ..{int(SMALL_R * 10)} run scoreboard players set #wkTe mb 0',
        'execute if score #wkTe mb matches 1 run scoreboard players add #wkTq mb 2',
        f'execute if score #wkTq mb matches {TCAP + 1}.. run return 0',
        f'function {T}fan',
        f'execute if score #wkTe mb matches 1 run function {T}edges with storage {STO} t',
    ])
    W.w('tele/e/sector_disc', ['# Internal (macro): a >= 175 draws the disc of radius r.',
                               f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #wkTr mb',
                               f'data modify storage {STO} t.rim set value "t_rim"',
                               f'execute if score #wkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
                               f'function {T}disc with storage {STO} t'])
    W.w('tele/wedge', [
        '# One swept wedge: {r0, r1 (tenths), a0 < a1 (degrees relative to the executor yaw, + = clockwise from above,',
        '# a1 - a0 <= 180), tell, el, nd, hold}. At the swept tick\'s tail root, rotated = the reference yaw. The host',
        '# stacks one per swept tick (api.wedges()), so the drawn union is the hazard union. Fill + rim piece, no radial',
        '# edges (2 cards up to 32 degrees); r0 >= 1 b adds an inner rim arc (the fill keeps its apex: no Apep call',
        '# uses r0 > 0).',
        *head(['$scoreboard players set #wkTr0 mb $(r0)', '$scoreboard players set #wkTr mb $(r1)',
               '$scoreboard players set #wkTA0 mb $(a0)', '$scoreboard players set #wkTa mb $(a1)'], need=2),
        'scoreboard players operation #wkTa mb -= #wkTA0 mb',
        'execute if score #wkTa mb matches ..0 run scoreboard players set #wkTa mb 1',
        'execute if score #wkTa mb matches 181.. run scoreboard players set #wkTa mb 180',
        'execute if score #wkTr mb matches ..1 run scoreboard players set #wkTr mb 2',
        'execute if score #wkTr0 mb >= #wkTr mb run scoreboard players set #wkTr0 mb 0',
        'scoreboard players set #wkTx mb 10', 'scoreboard players operation #wkTA0 mb *= #wkTx mb',
        'scoreboard players operation #wkTa mb *= #wkTx mb',
        *fan_need(),
        'scoreboard players set #wkTe mb 1',
        f'execute if score #wkTq mb matches {TCAP + 1}.. run return 0',
        f'function {T}fan',
    ])

    # --- line, crack (shared arithmetic)
    def line_math():
        return [
            'execute if score #wkTl mb matches ..1 run scoreboard players set #wkTl mb 2',
            'execute if score #wkTw mb matches ..1 run scoreboard players set #wkTw mb 2',
            '# a negative back starts the lane beyond the point (hz/line with a negative #hzBack); keep 0.2 b of length',
            'scoreboard players operation #wkTd mb = #wkTl mb',
            'scoreboard players remove #wkTd mb 2',
            'scoreboard players operation #wkTd mb *= #wkMinus1 mb',
            'scoreboard players operation #wkTb mb > #wkTd mb',
            f'execute store result storage {STO} t.len float 0.1 run scoreboard players get #wkTl mb',
            f'execute store result storage {STO} t.w float 0.1 run scoreboard players get #wkTw mb',
            f'execute store result storage {STO} t.hw float 0.05 run scoreboard players get #wkTw mb',
            f'execute store result storage {STO} t.nhw float -0.05 run scoreboard players get #wkTw mb',
            f'execute store result storage {STO} t.nb float -0.1 run scoreboard players get #wkTb mb',
            'scoreboard players operation #wkTx mb = #wkTl mb', 'scoreboard players operation #wkTx mb -= #wkTb mb',
            f'execute store result storage {STO} t.mid float 0.05 run scoreboard players get #wkTx mb',
            'scoreboard players operation #wkTl mb += #wkTb mb',
            f'execute store result storage {STO} t.lb float 0.1 run scoreboard players get #wkTl mb',
        ]
    lhead = ['$scoreboard players set #wkTl mb $(len)', '$scoreboard players set #wkTw mb $(w)',
             '$scoreboard players set #wkTb mb $(back)']
    lane_cards = [
        *mk('t_lane', '^ ^0.035 ^$(nb)', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', 'c2'),
        *mk('t_bar', '^$(hw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1'),
        *mk('t_bar', '^$(nhw) ^0.045 ^$(nb)', '0.24f,1f,$(lb)f', '0.24f,1f,$(lb)f', 'c1'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(nb)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0'),
        *mk('t_bar', '^$(hw) ^0.046 ^$(len)', '0.24f,1f,$(w)f', '0.24f,1f,$(w)f', 'c1', rot='~90 0'),
    ]
    W.w('tele/line', [
        '# Line / lane decal: {len, w, back (tenths), tell, el, nd, hold}. At the start point (floor), rotated = the aim;',
        '# covers -back..len along the aim, w wide (as hz/line + #hzBack). Two rails, two caps and the fill growing',
        '# toward the far end (its bright edge reaches it on the hit). 5 cards (+1 with nd 2: the chevron mid-lane).',
        *head(lhead, need=6), *line_math(),
        f'function {T}line with storage {STO} t',
        f'execute if score #wkTnd mb matches 2 run function {T}jump_mid with storage {STO} t',
    ])
    W.w('tele/e/line', ['# Internal (macro, storage t).', *lane_cards])
    W.w('tele/e/jump_mid', ['# Internal (macro): the nd 2 chevron in the middle of a lane.',
                            *mk('t_jump', '^ ^0.05 ^$(mid)', '0.6f,1f,0.6f', '1.3f,1f,1.3f', 'c1')])
    g1, g2, g3 = TELE_COL[20]
    W.w('tele/crack', [
        '# 생명의 손 crack strip (P2): {len, w, back (tenths), tell, nd, hold}. At the stalk root, rotated along the',
        '# strip: the tele/line geometry in the gold palette (fixed) with a white-gold glowing crack growing along the',
        '# middle with the fill. 6 cards.',
        *head(lhead, el=False, need=6), *line_math(),
        f'data modify storage {STO} t merge value {{c1:{g1},c2:{g2},c3:{g3}}}',
        f'execute if score #wkTnd mb matches 1.. run data modify storage {STO} t.c1 set value {ND_RIM}',
        f'function {T}crack with storage {STO} t',
    ])
    W.w('tele/e/crack', ['# Internal (macro, storage t).', *lane_cards,
                         *mk('t_crack', '^ ^0.04 ^$(nb)', '$(w)f,1f,0.02f', '$(w)f,1f,$(lb)f', str(WHITE),
                             col2=str(WHITE))])
    # --- the expanding wave ring (ids)
    W.w('tele/wave', [
        '# Expanding wave ring id 0-7: {id, r0, r1, w (tenths), tell, dur (ticks), el, nd, hold}. At the floor centre.',
        '# Over the tell a disc fills to r0 (the start radius of the front) and flashes on the strike tick; from the',
        '# strike the front ring travels r0 -> r1 in dur ticks with the band\'s inner edge w behind it, then stays',
        '# hold ticks. Pair with hz/ring + hz/resize_s at (r1 - r0) / dur b/t. tele/wave_end {id} removes it. 4 cards.',
        *head(['$scoreboard players set #wkTr0 mb $(r0)', '$scoreboard players set #wkTr mb $(r1)',
               '$scoreboard players set #wkTw mb $(w)', '$scoreboard players set #wkTd mb $(dur)'], need=4),
        f'$data modify storage {STO} t.tg set value "rlk_wk_wv$(id)"',
        'execute if score #wkTr0 mb matches ..4 run scoreboard players set #wkTr0 mb 5',
        'execute if score #wkTr mb <= #wkTr0 mb run scoreboard players operation #wkTr mb = #wkTr0 mb',
        'execute if score #wkTr mb = #wkTr0 mb run scoreboard players add #wkTr mb 5',
        'execute if score #wkTw mb matches ..1 run scoreboard players set #wkTw mb 2',
        'execute if score #wkTd mb matches ..0 run scoreboard players set #wkTd mb 1',
        f'execute store result storage {STO} t.r0 float 0.1 run scoreboard players get #wkTr0 mb',
        f'execute store result storage {STO} t.r1 float 0.1 run scoreboard players get #wkTr mb',
        'scoreboard players operation #wkTb mb = #wkTr mb',
        'scoreboard players operation #wkTb mb -= #wkTw mb',
        f'execute store result storage {STO} t.ri1 float 0.1 run scoreboard players get #wkTb mb',
        'scoreboard players operation #wkTb mb = #wkTr0 mb',
        'scoreboard players operation #wkTb mb -= #wkTw mb',
        'execute if score #wkTb mb matches ..0 run scoreboard players set #wkTb mb 1',
        f'execute store result storage {STO} t.ri0 float 0.1 run scoreboard players get #wkTb mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #wkTr0 mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}wave with storage {STO} t',
    ])
    W.w('tele/e/wave', [
        '# Internal (macro, storage t). 1-2: the start disc (fill reaches r0 on the strike, stays 1 tick).',
        'scoreboard players operation #wkLife mb = #wkTell mb',
        'scoreboard players add #wkLife mb 2',
        *mk('t_fill', '~ ~0.035 ~', '0.02f,1f,0.02f', '$(r0)f,1f,$(r0)f', 'c2'),
        *mk('$(rim)', '~ ~0.045 ~', '$(r0)f,1f,$(r0)f', '$(r0)f,1f,$(r0)f', 'c1'),
        '# 3-4: the travelling rings: shown on the tick before the strike, moving from its end over dur ticks.',
        'scoreboard players operation #wkDly mb = #wkTell mb',
        'scoreboard players remove #wkDly mb 1',
        'scoreboard players operation #wkDur mb = #wkTd mb',
        'scoreboard players operation #wkLife mb = #wkTd mb',
        'scoreboard players operation #wkLife mb += #wkThold mb',
        'scoreboard players add #wkLife mb 1',
        'scoreboard players set #wkHit mb -1',
        *mk('t_ring', '~ ~0.05 ~', '$(r0)f,1f,$(r0)f', '$(r1)f,1f,$(r1)f', 'c1', flash=False),
        *mk('t_ring', '~ ~0.048 ~', '$(ri0)f,1f,$(ri0)f', '$(ri1)f,1f,$(ri1)f', 'c2', flash=False),
    ])
    W.w('tele/wave_end', ['# Remove wave ring {id} now (P3 cancel).', f'$kill {SEL}_wv$(id)]',
                          f'execute store result score #wkTN mb if entity {SEL}_t]'])
    # --- 종말의 여파: the mask wash, the dome footprints
    f1, f2, f3 = TELE_COL[24]
    W.w('tele/mask_wash', [
        '# The 종말의 여파 field wash: {r (tenths), tell, hold}. At the arena centre. One floor-wide card in the field look',
        '# (el 24) that fills from the centre to r over the tell (the first field tick), flashes then and stays hold',
        '# ticks; the dome footprints (tele/safe_rim) sit on top of it. 1 card.',
        *head(['$scoreboard players set #wkTr mb $(r)'], el=False, nd=False, need=1),
        f'data modify storage {STO} t merge value {{c1:{f1},c2:{f2},c3:{f3},tg:"rlk_wk_mw"}}',
        'execute if score #wkTr mb matches ..1 run scoreboard players set #wkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #wkTr mb',
        f'function {T}mask_wash with storage {STO} t',
    ])
    W.w('tele/e/mask_wash', ['# Internal (macro, storage t).',
                             *mk('t_wash', '~ ~0.03 ~', '0.05f,1f,0.05f', '$(r)f,1f,$(r)f', 'c2')])
    W.w('tele/safe_rim', [
        '# A dome footprint id 0-5: {id, r (tenths), tell, hold}. At the dome centre. The pale rim ring (dimmed until the',
        '# dome forms) and the dome glyph growing over the tell; on call + tell (the dome forms) both turn full bright,',
        '# then they stay hold ticks (to the pop) or until tele/safe_end {id}. 2 cards.',
        *head(['$scoreboard players set #wkTr mb $(r)'], el=False, nd=False, need=2),
        f'$data modify storage {STO} t.tg set value "rlk_wk_sr$(id)"',
        'execute if score #wkTr mb matches ..1 run scoreboard players set #wkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #wkTr mb',
        f'execute store result storage {STO} t.g0 float 0.012 run scoreboard players get #wkTr mb',
        f'execute store result storage {STO} t.g1 float 0.036 run scoreboard players get #wkTr mb',
        f'function {T}safe_rim with storage {STO} t',
    ])
    W.w('tele/e/safe_rim', ['# Internal (macro, storage t).',
                            *mk('t_safe', '~ ~0.047 ~', '$(r)f,1f,$(r)f', '$(r)f,1f,$(r)f', str(SAFE_DIM), col2=str(WHITE)),
                            *mk('t_dome', '~ ~0.05 ~', '$(g0)f,1f,$(g0)f', '$(g1)f,1f,$(g1)f', str(SAFE_DIM),
                                col2=str(WHITE))])
    W.w('tele/safe_end', ['# Remove dome footprint {id} now (the pop, a cancel).', f'$kill {SEL}_sr$(id)]',
                          f'execute store result score #wkTN mb if entity {SEL}_t]'])
    # --- the moving target ring (not a hazard decal)
    W.w('tele/mring', [
        '# A moving target ring id 0-3: {id, r (tenths), el}. At the floor point. A pale disc and its rim without fill',
        '# timing (증폭의 풀\'s ring lagging the player); move it with tele/mring_move, end it with tele/mring_end',
        '# (it expires by itself after 30 s). The cards keep their height in their own translation, so a move only',
        '# changes their position. 2 cards.',
        f'execute if score #wkTN mb matches {TCAP - TSKIP}.. run return 0',
        '$scoreboard players set #wkTEl mb $(el)', 'scoreboard players set #wkTnd mb 0',
        'scoreboard players set #wkTell mb 2', 'scoreboard players set #wkThold mb 0', f'function {T}prep',
        '$scoreboard players set #wkTr mb $(r)',
        'scoreboard players set #wkLife mb 600', 'scoreboard players set #wkDur mb 3', 'scoreboard players set #wkHit mb -1',
        f'$data modify storage {STO} t merge value {{tg:"rlk_wk_mr$(id)",tpd:2}}',
        'execute if score #wkTr mb matches ..1 run scoreboard players set #wkTr mb 2',
        f'execute store result storage {STO} t.r float 0.1 run scoreboard players get #wkTr mb',
        f'data modify storage {STO} t.rim set value "t_rim"',
        f'execute if score #wkTr mb matches ..25 run data modify storage {STO} t.rim set value "t_rim_s"',
        f'function {T}mring with storage {STO} t',
    ])
    W.w('tele/e/mring', ['# Internal (macro, storage t).',
                         *mk('t_target', '~ ~ ~', '0.3f,1f,0.3f', '$(r)f,1f,$(r)f', 'c2', off='0f,0.035f,0f', flash=False),
                         *mk('$(rim)', '~ ~ ~', '0.3f,1f,0.3f', '$(r)f,1f,$(r)f', 'c1', off='0f,0.045f,0f', flash=False)])
    W.w('tele/mring_move', ['# Move ring {id} to the executing point over {t} ticks (teleport_duration).',
                            f'$execute as {SEL}_mr$(id)] run data modify entity @s teleport_duration set value $(t)',
                            f'$tp {SEL}_mr$(id)] ~ ~ ~'])
    W.w('tele/mring_end', ['# Remove ring {id} now.', f'$kill {SEL}_mr$(id)]',
                           f'execute store result score #wkTN mb if entity {SEL}_t]'])
    W.w('tele/wall_spot', [
        '# One 둥지 blade footprint: {tell, hold}. At the blade spot, rotated = the blade facing. A pale yellow-green',
        '# 1.4 x 0.5 b bar growing over the tell, full bright when the wall rises (call + tell), then hold ticks. No',
        '# damage. 1 card.',
        f'execute if score #wkTN mb matches {TCAP - TSKIP}.. run return 0',
        '$scoreboard players set #wkTell mb $(tell)', 'scoreboard players set #wkTEl mb 7', 'scoreboard players set #wkTnd mb 0',
        '$scoreboard players set #wkThold mb $(hold)', f'function {T}prep',
        f'data modify storage {STO} t.tg set value "rlk_wk_ws"',
        f'function {T}wall_spot with storage {STO} t',
    ])
    W.w('tele/e/wall_spot', ['# Internal (macro, storage t).',
                             *mk('t_wall', '~ ~0.04 ~', '0.3f,1f,0.3f', '1f,1f,1f', str(WALL_DIM), col2=str(WHITE))])
    W.w('tele/clear', ['# Remove every attack telegraph of the kit: decals, waves, safe rims, moving rings, wall spots, the',
                       '# mask wash (a cancelled pattern, a pause, death). fx cards and both pools stay.',
                       f'kill {SEL}_t]', 'scoreboard players set #wkTN mb 0'])


# ----------------------------------------------------------------------------- the dressing pool (fx/dress/*)
LEY_BEARINGS = (12, 58, 104, 152, 197, 243, 290, 333)        # absolute yaws of the ley strips (a fixed table)
LEY_R0, LEY_R1 = 1.8, 14.0


def dress_funcs(W):
    D = FN + 'dress/'
    W.w('dress/swirl', [
        '# The Heart\'s gold swirl ring: {r (tenths)}. At the arena centre (T1 t45 -> CS t24). Replaces an earlier swirl;',
        f'# remembered in storage {STO} dress.swirl for dress/redraw. 2 cards of the dressing pool (never aged).',
        f'$data modify storage {STO} dress.swirl set value {{r:$(r)}}',
        f'execute unless score #wkInit mb matches 1 run function {E}init',
        f'kill {SEL}_dsw]',
        '$scoreboard players set #wkTr mb $(r)',
        f'execute store result storage {STO} dress.s.d float 0.1 run scoreboard players get #wkTr mb',
        f'execute store result storage {STO} dress.s.g float 0.26 run scoreboard players get #wkTr mb',
        f'function {D}e/swirl with storage {STO} dress.s',
    ])
    W.w('dress/e/swirl', ['# Internal (macro): the swirl ring (r) and its soft gold glow (1.3 r).',
                          f'execute if score #wkDN mb matches {DCAP - 1}.. run return 0',
                          f'$summon minecraft:item_display ~ ~0.032 ~ {{Tags:["{TAG}","{TAG}_d","{TAG}_dsw","rlk_room","rlk_mb_aux"],'
                          'billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
                          'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[$(d)f,1f,$(d)f],'
                          'right_rotation:[0f,0f,0f,1f]},Rotation:[0f,0f],item:{id:"minecraft:paper",count:1,components:'
                          f'{{"minecraft:item_model":"{NS_TEX}d_swirl"}}}}}}',
                          f'$summon minecraft:item_display ~ ~0.031 ~ {{Tags:["{TAG}","{TAG}_d","{TAG}_dsw","rlk_room","rlk_mb_aux"],'
                          'billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
                          'transformation:{translation:[0f,0f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],'
                          'scale:[$(g)f,$(g)f,$(g)f],right_rotation:[0f,0f,0f,1f]},Rotation:[0f,0f],item:{id:"minecraft:paper",'
                          f'count:1,components:{{"minecraft:item_model":"{NS_TEX}glow","minecraft:custom_model_data":'
                          f'{{colors:[{rgb("#D8B44A")}]}}}}}}}}',
                          f'function {D}e/count'])
    ley = ['# The 지맥 이상 ley-line strips: {n:<6-8>}. At the arena centre (T1 t106 -> CS t24): n pulsing orange-gold crack',
           f'# strips from r {LEY_R0} to r {LEY_R1} on the absolute bearings {LEY_BEARINGS} (the first n). Replaces',
           f'# earlier strips; remembered in storage {STO} dress.ley for dress/redraw. n cards of the dressing pool.',
           f'$data modify storage {STO} dress.ley set value {{n:$(n)}}',
           f'execute unless score #wkInit mb matches 1 run function {E}init',
           f'kill {SEL}_dly]', '$scoreboard players set #wkTn mb $(n)',
           'execute if score #wkTn mb matches ..5 run scoreboard players set #wkTn mb 6',
           'execute if score #wkTn mb matches 9.. run scoreboard players set #wkTn mb 8']
    for k, yaw in enumerate(LEY_BEARINGS):
        ley.append(f'execute if score #wkTn mb matches {k + 1}.. run function {D}e/ley{k}')
    ley.append(f'function {D}e/count')
    W.w('dress/ley', ley)
    for k, yaw in enumerate(LEY_BEARINGS):
        ln = LEY_R1 - LEY_R0
        wn, ww = 1.0, 1.7
        W.w(f'dress/e/ley{k}', [
            f'# Internal: ley strip {k} at the absolute bearing {yaw}; its width breathes {wn} <-> {ww} b (dress/e/pulse).',
            f'execute if score #wkDN mb matches {DCAP}.. run return 0',
            f'execute rotated {yaw} 0 run summon minecraft:item_display ~ ~0.033 ~ {{Tags:["{TAG}","{TAG}_d","{TAG}_dly",'
            f'"{TAG}_dp","rlk_room","rlk_mb_aux"],billboard:"fixed",brightness:{{sky:15,block:15}},view_range:2f,shadow_radius:0f,'
            f'Rotation:[{yaw}f,0f],transformation:{{translation:[0f,0f,{num(LEY_R0)}f],left_rotation:[0f,0f,0f,1f],'
            f'scale:[{num(wn)}f,1f,{num(ln)}f],right_rotation:[0f,0f,0f,1f]}},item:{{id:"minecraft:paper",count:1,components:'
            f'{{"minecraft:item_model":"{NS_TEX}d_ley","minecraft:custom_data":{{wkP0:{{start_interpolation:0,'
            f'interpolation_duration:10,transformation:{{scale:[{num(wn)}f,1f,{num(ln)}f]}}}},wkP1:{{start_interpolation:0,'
            f'interpolation_duration:10,transformation:{{scale:[{num(ww)}f,1f,{num(ln)}f]}}}}}}}}}}}}'])
    W.w('dress/e/count', ['# Internal: recount the pool and keep the ager running (the strips pulse from it).',
                          f'execute store result score #wkDN mb if entity {SEL}_d]',
                          f'schedule function {E}world 1t replace'])
    W.w('dress/e/pulse', ['# Internal (from the ager): every 10 t the ley strips swap width (client-interpolated over 10 t).',
                          'scoreboard players operation #wkPh mb = #wkNow mb', 'scoreboard players operation #wkPh mb %= #wk20 mb',
                          f'execute if score #wkPh mb matches 0 as {SEL}_dp] run data modify entity @s {{}} merge from entity @s '
                          'item.components."minecraft:custom_data".wkP1',
                          f'execute if score #wkPh mb matches 10 as {SEL}_dp] run data modify entity @s {{}} merge from entity @s '
                          'item.components."minecraft:custom_data".wkP0'])
    W.w('dress/redraw', ['# Re-make the dressing pool from storage (after /reload, which kills the rlk_mb_aux cards). Run it',
                         '# at the arena centre.',
                         f'execute if data storage {STO} dress.swirl run function {D}swirl with storage {STO} dress.swirl',
                         f'execute if data storage {STO} dress.ley run function {D}ley with storage {STO} dress.ley'])
    W.w('dress/clear', ['# Remove the dressing pool and forget it (CS white-out, cleanup, uninstall).',
                        f'kill {SEL}_d]', f'data remove storage {STO} dress', 'scoreboard players set #wkDN mb 0'])


def flood_tile(W):
    W.w('p/e/flood_tile', [
        '# Internal (macro, storage pf: l = life): one 7.5 b flood tile of the flood pool, growing from its centre in 4 t.',
        f'execute if score #wkFN mb matches {FLCAP}.. run return 0',
        f'execute unless score #wkInit mb matches 1 run function {E}init',
        f'data modify storage {STO} a set value {{kind:"fl_tile",pos:"~ ~0.04 ~",rot:"0 0",bb:"fixed",s0:"0.5f,1f,0.5f",'
        f's1:"{num(FLOOD_CELL + 0.02)}f,1f,{num(FLOOD_CELL + 0.02)}f",off:"0f,0f,0f",move:"0f,0f,0f",col:{WHITE},col2:-1,'
        f'ax:"0f,1f,0f",tg:"rlk_wk_c",tpd:0}}',
        'scoreboard players set #wkRoll mb 0', 'scoreboard players set #wkSpin mb 0',
        '$scoreboard players set #wkLife mb $(l)', 'scoreboard players set #wkFade mb 8',
        'scoreboard players set #wkDly mb 0', 'scoreboard players set #wkDur mb 4', 'scoreboard players set #wkHit mb -1',
        f'scoreboard players set #wkTel mb {POOL_FLOOD}',
        f'function {E}make'])


# ----------------------------------------------------------------------------- props (ap_fx_api.md §0.7)
PROPS = {
    # name -> (doc, kind, tint, billboard, uniform scale or None (the record / module sets the transformation), brightness)
    'thorn_wheel_homing': ('P3 homing wheel (pj, #pjNoDodge 1): gold-orange thorn wheel Ø 2 with a red 4-point flare, '
                           'camera-facing; p/homing_trail run as it spins it.', 'thorn_wheel_homing', WHITE, 'center', 2.05, 15),
    'thorn_wheel': ('P3 carpet wheel as a prop (fallback): pale-green thorn wheel Ø 1.6, camera-facing.', 'thorn_wheel',
                    WHITE, 'center', 1.65, 15),
    'seed_bolt': ('O2 ranged bolt: lime seed ball Ø 0.6 with a glow, camera-facing.', 'seed_bolt', WHITE, 'center', 1.0, 15),
    'seed_orb': ('Q5 seed orb Ø 0.7: glowing yellow-green with a spiral glyph, camera-facing (the module moves / bobs it).',
                 'seed_orb', WHITE, 'center', 1.15, 15),
    'charge_ball': ('Q3 light ball over the crown: #FDFBBD core, white-green halo, camera-facing, Ø 1.6.', 'charge_ball',
                    WHITE, 'center', 1.6, 15),
    'water_sheet': ('One water-sheet tile of the lush lake (theme props(\'lush\'), 16 tiles at scale 14, y 201.005): '
                    'flat, about 40 % alpha. The record sets the scale.', 'water_sheet', WHITE, 'fixed', None, 13),
    'lily_pad': ('Lily pad (lush pond dressing beyond r 22), flat; the record sets the scale.', 'lily_pad', WHITE, 'fixed',
                 None, 14),
    'bell_flower': ('Yellow bell flowers (lush pond dressing beyond r 22), crossed quads; the record sets the scale.',
                    'bell_flower', WHITE, 'fixed', None, 14),
    'bulb_flower': ('Glowing bulb flower (lush pond dressing beyond r 22), crossed quads; the record sets the scale.',
                    'bulb_flower', WHITE, 'fixed', None, 15),
    'bank_crystal': ('Gold crystal spikes on the bank r 26-29 (both looks), brightness 15; the record sets the scale.',
                     'bank_crystal', WHITE, 'fixed', None, 15),
    'gate_crystal': ('Gold-green gate crystal of the chapter-3 entrance (≈ 1.5 b at scale 1), brightness 15, static.',
                     'gate_crystal', WHITE, 'fixed', None, 15),
}
SPIN_Q = ('[0f,0f,0f,1f]', '[0f,0f,0.7071068f,0.7071068f]', '[0f,0f,1f,0f]', '[0f,0f,0.7071068f,-0.7071068f]')


def props(W):
    for name, (doc, kind, col, bb, sc, br) in PROPS.items():
        tr = ''
        if sc is not None:
            tr = (f',transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[{num(sc)}f,{num(sc)}f,'
                  f'{num(sc)}f],right_rotation:[0f,0f,0f,1f]}}')
        W.w(f'prop/{name}', [f'# {doc}', '# As @s = an item_display the module owns: item, tint, billboard, brightness' +
                             (', transformation.' if sc is not None else ' (the transformation is the caller\'s).'),
                             f'data merge entity @s {{item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":'
                             f'"{NS_TEX}{kind}","minecraft:custom_model_data":{{colors:[{col}]}}}}}},billboard:"{bb}",'
                             f'brightness:{{sky:15,block:{br}}},view_range:2f,shadow_radius:0f{tr}}}'])
    spin = ['# Internal (as a homing-wheel prop, from p/homing_trail every 2 t): roll it a quarter turn about the view axis',
            '# over 2 t (four phases of gametime), so the camera-facing wheel spins.',
            'execute store result score #wkSp mb run time query gametime', 'scoreboard players set #wk8 mb 8',
            'scoreboard players operation #wkSp mb %= #wk8 mb']
    for k, q in enumerate(SPIN_Q):
        spin.append(f'execute if score #wkSp mb matches {2 * k}..{2 * k + 1} run data merge entity @s {{start_interpolation:0,'
                    f'interpolation_duration:2,transformation:{{left_rotation:{q}}}}}')
    W.w('prop/e/spin', spin)


def sounds(W):
    for name, (doc, layers) in SOUNDS.items():
        lines = [f'# {doc}', '# Layers: event volume pitch minVolume (per-layer minimum, mboss_lib.sound rule).']
        if name == 'heart_gain':
            ev, vol, _p = layers[0]
            for k, pit in enumerate(HEART_PITCH):
                rng = f'{k * 1000}..{k * 1000 + 999}' if k < 10 else '10000..'
                if k == 0:
                    rng = '..999'
                lines.append(f'execute if score #apHt mb matches {rng} run ' + sound_line(ev, vol, pit))
        else:
            lines += [sound_line(*l) for l in layers]
        W.w(f'snd/{name}', lines)


# ----------------------------------------------------------------------------- HUD (ap_fx_api.md §0.9)
HUD_FUNCS = {'title': ('g', 't', 'c', 's', 'hold'), 'banner_aftermath': (), 'banner_end': (), 'whiteout': ('hold',),
             'flash_white': (), 'flash_green': (), 'flash_hit': (), 'flash_end': (), 'clear': (), 'heart_bar': ()}
BANNER = ('[' + glyph_c('dome') + ',{text:" "},{text:"소생의 찬가 보호막",color:"' + BANNER_RED + '",bold:true},'
          '{text:" 안으로 들어가서 종말의 여파를 막아내세요",color:"#FFFFFF"}]')


def hud_funcs(W):
    H = FN + 'hud/'
    title = ['# The title line: {g:<heart|warn|fail|success|none>, t:<text>, c:<"#RRGGBB">, s:<subtitle>, hold:<ticks>}.',
             '# The kit glyph g, then the module\'s text t in colour c (bold); subtitle s; fade-in 6 t, hold, fade-out 12 t.',
             '# T1 「오아시스의 심장」, the time-out "!", 「소생 실패」, "오아시스의 심장이 소생했습니다".',
             f'$data modify storage {STO} hud.g set value "$(g)"',
             f'data modify storage {STO} hud.gc set value {{text:""}}']
    for g, gname in TITLE_G.items():
        title.append(f'execute if data storage {STO} hud{{g:"{g}"}} run data modify storage {STO} hud.gc set value '
                     f'{{text:"",extra:[{glyph_c(gname)},{{text:" "}}]}}')
    title += ['$scoreboard players set @a[tag=player] vBig $(hold)', 'scoreboard players add @a[tag=player] vBig 18',
              '$title @a[tag=player] times 6 $(hold) 12',
              '$title @a[tag=player] subtitle {text:"$(s)",color:"#F2EEDC"}',
              f'$title @a[tag=player] title [{{nbt:"hud.gc",storage:"{STO}",interpret:true}},{{text:"$(t)",color:"$(c)",bold:true}}]']
    W.w('hud/title', title)
    W.w('hud/banner_aftermath', [
        '# The 종말의 여파 banner (Q2 B0 -> t156): the actionbar line "소생의 찬가 보호막 안으로 들어가서 종말의 여파를',
        '# 막아내세요" (the first phrase red #C36E5A, bold; the rest white) with the dome glyph, re-sent every 20 t (holding',
        '# the regular actionbar HUD, hudHold) until hud/banner_end.',
        f'data modify storage {STO} hud.ban set value 1b', f'function {H}e/banner_tick'])
    W.w('hud/e/banner_tick', ['# Internal: re-send the banner while it is on (a 20 t schedule chain).',
                              f'execute unless data storage {STO} hud{{ban:1b}} run return 0',
                              f'title @a[tag=player] actionbar {BANNER}', 'scoreboard players set @a[tag=player] hudHold 30',
                              f'schedule function {H}e/banner_tick 20t replace'])
    W.w('hud/banner_end', ['# Drop the banner (Q2 t156, cancel, pause).', f'data modify storage {STO} hud.ban set value 0b',
                           f'schedule clear {H}e/banner_tick', 'title @a[tag=player] actionbar ""',
                           'scoreboard players set @a[tag=player] hudHold 0'])
    W.w('hud/whiteout', ['# Full-screen white on the title line: fade-in 4 t, {hold} ticks, fade-out 8 t (CS t24, hold 28 ->',
                         '# white to t64). No Blindness, no FOV change; vBig rests the F5 crosshair title meanwhile.',
                         '$scoreboard players set @a[tag=player] vBig $(hold)', 'scoreboard players add @a[tag=player] vBig 12',
                         'title @a[tag=player] subtitle ""', '$title @a[tag=player] times 4 $(hold) 8',
                         'title @a[tag=player] title [' + glyph_c('fl_white') + ',{text:"' + SP_NEG1 + '",font:"' + FONT + '"}]'])
    for name, g, t, v in (('flash_white', 'fl_white9', '0 2 4', 6), ('flash_green', 'fl_green', '1 3 4', 8),
                          ('flash_hit', 'fl_edge', '0 1 2', 3)):
        W.w(f'hud/{name}', [f'# Full-screen flat flash on the title line ({v} t); vBig rests the F5 crosshair title.',
                            f'scoreboard players set @a[tag=player] vBig {v}', 'title @a[tag=player] subtitle ""',
                            f'title @a[tag=player] times {t}',
                            'title @a[tag=player] title [' + glyph_c(g) + ',{text:"' + SP_NEG1 + '",font:"' + FONT + '"}]'])
    W.w('hud/flash_end', ['# Drop a title overlay at once (pause, cancel).', 'scoreboard players set @a[tag=player] vBig 0',
                          'title @a[tag=player] times 0 1 2', 'title @a[tag=player] title ""'])
    W.w('hud/clear', ['# Every banner and overlay off (cleanup, death, abort, uninstall).',
                      f'data modify storage {STO} hud.ban set value 0b', f'schedule clear {H}e/banner_tick',
                      'title @a[tag=player] actionbar ""', 'title @a[tag=player] clear',
                      'scoreboard players set @a[tag=player] vBig 0', 'scoreboard players set @a[tag=player] hudHold 0'])
    hb = ['# FN-24 fallback (only when the framework bossui lacks #buHpCol / #buNoNum): the gold Heart progress bar as',
          f'# one glyph string in storage {STO} hud.hbar (a text component) from #apHt mb (0..10000, {BAR_CELLS} cells):',
          f'# the core appends {{nbt:"hud.hbar",storage:"{STO}",interpret:true}} to its line.']
    for n in range(BAR_CELLS + 1):
        lo = n * 10000 // BAR_CELLS
        hi = (n + 1) * 10000 // BAR_CELLS - 1
        rng = f'{lo}..{hi}' if n < BAR_CELLS else f'{lo}..'
        if n == 0:
            rng = f'..{hi}'
        hb.append(f'execute if score #apHt mb matches {rng} run data modify storage {STO} hud.hbar set value '
                  f'{{text:"{heart_bar(lo)}",font:"{FONT}",color:"white"}}')
    W.w('hud/heart_bar', hb)


# ----------------------------------------------------------------------------- presets -> datapack
def preset_body(name):
    return PRESETS[name][2]()


def presets_dp(W):
    assert set(AMBIENT) <= set(PRESETS), set(AMBIENT) - set(PRESETS)
    assert set(PTCL) <= set(PRESETS), set(PTCL) - set(PRESETS)
    for name, (doc, args, f, conv) in PRESETS.items():
        body = f()
        head = [f'# {doc}']
        if args:
            head.append('# {' + ', '.join(args) + '} (macro; sizes in tenths of a block, ticks, degrees)')
        if name in AMBIENT:
            head += [f'# Ambient: skipped while {SOFT}+ fx cards live (room for the fx of the hits).',
                     f'execute if score #wkN mb matches {SOFT}.. run return 0']
        if name in PTCL:
            assert not any(f'{FN}card' in l for l in body), name
        if conv:
            pub = list(head)
            for a in args:
                pub.append(f'$scoreboard players set #wkA{a} mb $({a})')
            for c in conv:
                key, a, scale = c[0], c[1], c[2]
                add = c[3] if len(c) > 3 else 0
                if scale is None:
                    if add:
                        pub.append(f'scoreboard players add #wkA{a} mb {add}')
                    pub.append(f'execute store result storage {STO} pa.{key} int 1 run scoreboard players get #wkA{a} mb')
                    if add:
                        pub.append(f'scoreboard players remove #wkA{a} mb {add}')
                else:
                    pub.append(f'execute store result storage {STO} pa.{key} float {num(scale, 7)} run scoreboard players '
                               f'get #wkA{a} mb')
            pub.append(f'function {FN}p/e/{name} with storage {STO} pa')
            W.w(f'p/{name}', pub)
            assert any(l.startswith('$') for l in body), name
            W.w(f'p/e/{name}', [f'# Internal (macro, storage {STO} pa) of p/{name}.'] + body)
        else:
            if args:
                assert any(l.startswith('$') for l in body), name
            else:
                assert not any(l.startswith('$') for l in body), name
            W.w(f'p/{name}', head + body)
    for name, spec in ARC_BODIES.items():
        W.w(f'p/e/{name}_p', [f'# Internal (macro, storage {STO} pa) of p/{name}: the arc revealed clockwise.'] +
            _arc(name, spec['n'], spec['cols'], spec['h'], 0, spec['s_y'], spec['life'], spec['fade'], False))
        if name != 'arm_sweep':
            W.w(f'p/e/{name}_n', [f'# Internal (macro, storage {STO} pa) of p/{name}: the arc revealed counter-clockwise.'] +
                _arc(name, spec['n'], spec['cols'], spec['h'], 0, spec['s_y'], spec['life'], spec['fade'], True))


def preset_cards(name):
    """fx cards a preset spawns (card / cardx lines; the flood counts its pool tiles apart: preset_pool_cards)"""
    if name in ARC_BODIES:
        return ARC_BODIES[name]['n']
    if name == 'flood':
        return 0
    lines = preset_body(name)
    n = sum(1 for l in lines if f'{FN}card' in l)
    if name in ('gold_motes', 'whirl_leaves', 'beam_rain'):
        return n // 3                  # one of three position variants runs per call
    return n


def preset_pool_cards(name):
    return len(flood_cells()) if name == 'flood' else 0


# ----------------------------------------------------------------------------- tests and demos
TEST_ARGS = {'r': 4.2, 'len': 8.0, 'r0': 3.0, 'r1': 14.4, 'dur': 14, 'a': 60, 'dir': 1, 'w': 3.0, 'h': 3.0, 'life': 24}


def test_call(name):
    args = PRESETS[name][1]
    return fx(name, **{a: TEST_ARGS[a] for a in args})


def _wedges(r, t0, tell0, k0=0, n=8, dir_=1):
    """the stub swing (200 degrees in 8 ticks, 25 per tick) as stacked wedges: (call tick, line)"""
    out = []
    for k in range(n):
        a0 = -100 + 25 * k if dir_ > 0 else 75 - 25 * k
        out.append((t0, 'tail', tele_wedge(0, r, a0, a0 + 25, tell0 + k, el=20 if r < 11.6 else 7)))
    return out


def _ev(t, where, *lines):
    return [(t, where, l) for l in lines]


F = None   # set below (fx)


def _demos():
    f = fx
    D = {}
    D['entrance'] = sum([
        _ev(0, 'floor', f('burrow_pool', r=3.5), f('leaf_flakes'), snd('e_emerge')),
        _ev(60, 'bulb', f('bulb_flash'), snd('e_flash')),
        *[_ev(t, 'bulb', f('gold_embers')) for t in range(63, 81, 4)],
        _ev(70, 'bulb', snd('e_heart_up')), _ev(100, 'body', snd('e_roar')),
        *[_ev(t, 'floor', f('haze_withered')) for t in range(0, 110, 10)]], [])
    D['burrow'] = sum([
        _ev(4, 'floor', f('burrow_pool', r=3.5), snd('p1_dive')), _ev(8, 'floor', f('leaf_flakes')),
        *[_ev(t, 'glide', f('shadow_glide')) for t in range(23, 45, 2)], *[_ev(t, 'glide', snd('p1_travel')) for t in (23, 30, 37)],
        _ev(32, 'L', tele_disc(4.2, 12, el=20), snd('p1_ring')),
        _ev(44, 'L', f('gold_burst'), f('leaf_debris'), snd('p1_burst')),
        _ev(52, 'lane', tele_line(10.8, 3.6, 12, el=20)),
        _ev(64, 'lane', f('slash_band', len=10.8), f('spine_afterimage', len=10.8), snd('p1_sweep')),
        _ev(77, 'floor', snd('p1_land'), f('leaf_splash'))], [])
    D['relocate'] = sum([_ev(4, 'floor', f('root_chunks'), snd('r_sink')), _ev(18, 'body', f('emerge_motes'), snd('r_emerge'))], [])
    D['hands'] = sum([
        _ev(0, 'floor', tele_disc(4.2, 30, el=20)), *[_ev(t, 'body', f('swirl_wisps')) for t in range(5, 28, 4)],
        _ev(5, 'body', snd('p2_swirl')), *[_ev(t, 'body', snd('p2_swirl_tick')) for t in range(5, 28, 3)],
        _ev(30, 'floor', f('plunge_flash'), f('splinter_splash'), snd('p2_plunge')), _ev(36, 'floor', snd('p2_stalks')),
        *[_ev(40, f'stalk{k}', tele_crack(8.4, 3.0, tl)) for k, tl in enumerate((22, 29, 35, 42))],
        _ev(40, 'floor', snd('p2_lines')),
        *[_ev(t, f'stalk{k}', f('slam_arc'), snd('p2_slam')) for k, t in enumerate((62, 69, 75, 82))],
        _ev(118, 'body', snd('p2_flower')), _ev(128, 'body', snd('p2_fold'))], [])
    slams = ((111, 141, 30), (141, 164, 23), (164, 195, 31))
    ev = [_ev(5, 'floor', f('burrow_pool', r=3.5), snd('p1_dive')), *[_ev(t, 'glide', f('shadow_glide')) for t in range(23, 40, 2)],
          _ev(39, 'floor', f('gold_glow', r=3.0), snd('p3_glow')), _ev(44, 'floor', f('crown_debris'), snd('p3_emerge')),
          *[_ev(t, 'body', f('spiral_wisps')) for t in range(94, 131, 4)], _ev(94, 'body', snd('p3_windup'))]
    for k, (t0, ts, tell) in enumerate(slams):
        ev += [_ev(t0, 'floor', tele_disc(5.4, tell, el=20), tele_wave(k, 3.0, 14.4, 1.0, tell, 14, el=20)),
               _ev(ts - 1, 'floor', f('wheel_carpet', r0=3.0, r1=14.4, dur=14)),
               _ev(ts, 'floor', f('gold_burst'), f('blade_burst', r=7.2), snd('p3_slam'), snd('p3_wheels')),
               *[_ev(ts + d, 'floor', snd('p3_wheel_roll')) for d in range(0, 14, 4)],
               *[_ev(ts + d, 'wheel', f('homing_trail')) for d in range(6, 28, 2)], _ev(ts + 16, 'wheel', snd('p3_homing_loop')),
               _ev(ts + 28, 'wheel', f('wheel_pop'))]
    ev.append(_ev(slams[0][1] + 20, 'player', snd('p3_wheel_hit')))
    D['glow'] = sum(ev, [])
    D['wither'] = sum([
        _ev(0, 'body', snd('p4_rear')), _ev(16, 'floor', tele_disc(9.0, 24, el=23, hold=31), snd('p4_hum')),
        _ev(40, 'body', snd('p4_spin'), f('leaf_splash')), *[_ev(t, 'body', f('spin_trails')) for t in range(47, 72, 3)],
        _ev(57, 'body', f('spin_flash'))], [])
    D['tail'] = sum([
        _ev(8, 'body', snd('p5_raise')), _wedges(11.4, 14, 14),
        _ev(23, 'tip', f('tail_tip_flash'), snd('p5_cock')),
        _ev(28, 'tail', f('arc_trail', r=11.4, a=100, dir=1), snd('p5_swing')),
        _wedges(11.4, 39, 13, dir_=-1),
        _ev(52, 'tail', f('arc_trail', r=11.4, a=100, dir=-1), snd('p5_swing')),
        _ev(30, 'player', snd('p5_hit'), hud('flash_hit'))], [])
    D['combo'] = sum([
        _ev(4, 'body', tele_sector(7.2, 78, 10, el=20)), _ev(14, 'body', f('arm_sweep', r=7.2, a=78), snd('p6_sweep')),
        _ev(32, 'ahead4', tele_disc(6.6, 14, el=20)), _ev(46, 'ahead4', f('slam_burst'), snd('p6_slam')),
        _ev(73, 'body', tele_disc(7.2, 10, el=20, nd=0)), _ev(83, 'body', f('spin_ring', r=7.2), snd('p6_spin')),
        _ev(98, 'ahead7', tele_disc(6.6, 22, el=20)), _ev(120, 'ahead7', f('leap_slam'), snd('p6_slam')),
        *[_ev(t, 'body', snd('m_crawl')) for t in (130, 138)], _ev(146, 'body', snd('m_walk'))], [])
    D['revival_start'] = sum([
        _ev(20, 'floor', f('root_chunks'), snd('p1_dive')), _ev(30, 'floor', f('root_chunks')),
        _ev(45, 'floor', dress('swirl', r=3.5), f('cradle_dust'), snd('t1_cradle')), _ev(50, 'floor', snd('t1_lower')),
        _ev(100, 'floor', f('heart_beam'), snd('t1_land')),
        _ev(106, 'floor', hud('title', g='heart', t='「오아시스의 심장」', c='#EDCF63', s='마물을 처치해서 소생 진행도를 올리세요', hold=60),
            snd('t1_hud'), dress('ley', n=7)),
        *[_ev(116, f'spawn{k}', f('spawn_marker'), snd('spawn_marker')) for k in range(3)],
        *[_ev(t, 'floor', f('gold_motes')) for t in (60, 80, 100, 120)]], [])
    D['organisms'] = sum([
        _ev(0, 'org0', tele_sector(3.1, 27, 10)), _ev(10, 'org0', snd('o1_attack')), _ev(10, 'bulbT1', f('heart_hit'), snd('heart_hit')),
        _ev(20, 'org1', snd('o2_pivot'), tele_line(6.0, 1.4, 12), f('spark')), _ev(23, 'org1', f('crown_flare'), snd('o2_charge')),
        _ev(32, 'org1', snd('o2_shoot')), *[_ev(t, 'bolt', f('comet_trail')) for t in range(32, 42, 2)], _ev(42, 'org1', snd('o2_hit')),
        _ev(40, 'org2', snd('o3_collapse')), _ev(56, 'org2', snd('o3_collapse')), _ev(70, 'org0', snd('o3_cast'), f('shield_pop'), snd('o3_pop')),
        _ev(74, 'org0', snd('shield_hit')), _ev(90, 'org2', f('guard_death'), snd('o3_death')),
        *[_ev(60, f'wall{k}', tele_wall_spot(12, 40)) for k in range(4)], _ev(72, 'org3', snd('o4_rise')),
        *[_ev(112, f'wall{k}', f('wall_motes')) for k in range(4)], _ev(112, 'org3', snd('o4_fade')),
        _ev(80, 'org3', f('blink_flash'), snd('o4_flap')),
        *[_ev(t, 'org4', f('tether', len=5.0)) for t in range(100, 130, 2)], _ev(100, 'org4', snd('o5_hum')),
        _ev(130, 'org4', f('nurt_burst'), snd('o5_destruct')),
        _ev(140, 'org5', snd('o6_gulp'), snd('o6_bud')), _ev(160, 'org5', tele_disc(3.6, 10), snd('o6_inflate')),
        _ev(170, 'org5', f('pred_burst'), snd('o6_burst')),
        _ev(180, 'org5', tele_sector(2.6, 24, 10)), _ev(190, 'org5', f('bite_flash'), snd('o6_bite_first')), _ev(196, 'org5', snd('o6_swim')),
        _ev(198, 'org5', tele_sector(2.6, 24, 10)), _ev(208, 'org5', f('bite_flash'), snd('o6_bite')),
        _ev(200, 'org6', snd('o7_roll')), _ev(208, 'org6', tele_disc(3.6, 61), snd('o7_primed'), f('fuse_pulse')),
        *[_ev(t, 'org6', f('fuse_pulse')) for t in (217, 226, 235, 244, 253, 257, 261, 265)],
        _ev(264, 'org6', snd('o7_suck')), _ev(269, 'org6', f('blast_dome'), snd('o7_blast')),
        _ev(150, 'org0', f('org_burst'), snd('org_kill')), _ev(150, 'bulbT1', f('heart_gain'), f('flash'), snd('heart_gain')),
        _ev(250, 'floor', snd('timeout_warn'), hud('title', g='warn', t='!', c='#C36E5A', s='시간이 얼마 남지 않았습니다', hold=40))], [])
    D['failure'] = sum([_ev(0, 'floor', f('shock_ring'), snd('fail_strike'),
                            hud('title', g='fail', t='「소생 실패」', c='#C36E5A', s='다시 한 번 실패하면 쓰러집니다', hold=60)),
                        *[_ev(0, f'org{k}', f('org_burst')) for k in range(3)]], [])
    D['cutscene'] = sum([
        _ev(0, 'floor', f('wilt_ring'), snd('cs_complete')), *[_ev(0, f'org{k}', f('org_burst')) for k in range(3)],
        *[_ev(t, 'egg', f('gold_drip')) for t in range(0, 25, 3)],
        _ev(24, 'player', hud('whiteout', hold=28), dress('clear')),
        _ev(64, 'twig', f('ember_arc', len=9.0, h=3.0), snd('cs_ember')), *[_ev(t, 'floor', f('haze_lush')) for t in range(64, 190, 10)],
        *[_ev(t, 'egg', f('green_lightning')) for t in (76, 80)], _ev(80, 'player', hud('flash_green'), snd('cs_flash'), snd('cs_heal')),
        _ev(92, 'floor', f('revival_burst'), f('water_splash'), snd('cs_emerge')), _ev(132, 'floor', snd('cs_reveal')),
        _ev(132, 'player', hud('title', g='success', t='오아시스의 심장이 소생했습니다', c='#B6E35A', s='', hold=50))], [])
    D['move_strike'] = sum([
        _ev(8, 'floor', f('leaf_mound'), snd('q1_sink')), *[_ev(t, 'glide', f('leaf_pad'), snd('q1_trail')) for t in range(16, 43, 4)],
        _ev(32, 'L', tele_disc(4.2, 12), f('rosette'), snd('q1_rosette')),
        _ev(44, 'L', f('surface_burst'), f('water_splash'), snd('q1_burst')), _ev(44, 'body', f('hoop_trail')),
        _ev(46, 'ahead4', tele_disc(4.2, 15)), _ev(48, 'body', tele_disc(12.0, 21)),
        _ev(61, 'ahead4', f('belly_splash'), snd('q1_slam')), _ev(69, 'body', f('sweep_ring', r=12.0), snd('q1_slam')),
        _ev(71, 'body', f('light_sprouts'), snd('q1_rise'))], [])
    ev = [_ev(0, 'player', hud('banner_aftermath')), _ev(0, 'floor', snd('q2_banner'))]
    for k in range(3):
        ev.append(_ev(0, f'dome{k}', tele_safe_rim(k, 4.5, 54 + 4 * k, 189 - (54 + 4 * k))))
    ev += [_ev(0, 'body', f('crouch_splash'), snd('q2_charge')), *[_ev(t, 'body', f('whirl_leaves')) for t in range(18, 37, 3)],
           _ev(18, 'body', snd('q2_whirl')),
           _ev(40, 'floor', tele_mask_wash(26.0, 40, 96), f('field_ring', r0=3.0, r1=26.0, dur=18), snd('q2_release')),
           *[_ev(t, 'floor', snd('q2_field_loop')) for t in range(40, 157, 20)],
           *[_ev(44 + 4 * k, f'dome{k}', f('light_pillar')) for k in range(3)],
           *[_ev(54 + 4 * k, f'dome{k}', f('dome_rise'), snd('q2_dome')) for k in range(3)],
           *[_ev(t, 'floor', f('floor_glitter')) for t in range(80, 156, 10)], _ev(95, 'player', snd('q2_tick')),
           *[_ev(t, 'floor', f('beam_rain')) for t in range(134, 157, 4)], _ev(134, 'floor', snd('q2_rain')),
           _ev(156, 'player', hud('flash_white'), hud('banner_end')), _ev(156, 'floor', f('flood', life=24), snd('q2_blast')),
           *[_ev(189, f'dome{k}', f('dome_pop'), snd('q2_pop'), tele_safe_end(k)) for k in range(3)],
           _ev(190, 'body', f('green_burst'))]
    D['aftermath'] = sum(ev, [])
    D['shells'] = sum([
        _ev(10, 'player', tele_mring(0, 3.6, el=22)), *[_ev(t, 'player', tele_mring_move(0, 2)) for t in range(12, 34, 2)],
        _ev(14, 'crown', snd('q3_charge')),
        _ev(33, 'player', tele_mring_end(0), tele_disc(3.6, 12)), _ev(35, 'crown', f('launch_flash'), snd('q3_launch')),
        _ev(45, 'player', f('beam_column', w=3.0), f('leaf_splash'), f('spores'), snd('q3_impact1')),
        _ev(79, 'pk0', tele_disc(3.0, 14)), _ev(82, 'pk1', tele_disc(3.0, 14)),
        _ev(87, 'pk0', f('shell_streak', h=12.0)), _ev(90, 'pk1', f('shell_streak', h=12.0)),
        _ev(93, 'pk0', f('shell_burst'), snd('q3_impact2')), _ev(96, 'pk1', f('shell_burst'), snd('q3_impact2'))], [])
    D['surface_shot'] = sum([
        _ev(8, 'floor', f('leaf_mound'), snd('q1_sink')), *[_ev(t, 'glide', f('leaf_pad'), snd('q1_trail')) for t in range(20, 37, 4)],
        _ev(26, 'L', tele_disc(3.6, 10), f('leaf_ring')),
        _ev(36, 'L', f('surface_splash'), f('water_splash'), snd('q3s_surface'), snd('q3s_charge')),
        _ev(36, 'player', tele_disc(3.0, 12)), _ev(46, 'muzzle', f('light_band', len=8.0), f('launch_flash'), snd('q3s_launch')),
        _ev(48, 'player', f('beam_column', w=2.0), f('shell_burst'), snd('q3s_impact'))], [])
    D['tail_p3'] = sum([
        _wedges(12.0, 2, 12), _ev(3, 'body', snd('q4_rear')), _ev(11, 'tip', f('tail_tip_flash')),
        _ev(14, 'tail', f('crescent_trail', r=12.0, a=100, dir=1), snd('q4_swing')),
        _wedges(12.0, 32, 14, dir_=-1), _ev(36, 'body', snd('q4_rear')),
        _ev(46, 'tail', f('crescent_trail', r=12.0, a=100, dir=-1), snd('q4_swing2')), _ev(53, 'body', f('glitter_shower'))], [])
    ev = [_ev(10, 'body', f('charge_streaks'), snd('q5_unfold')), _ev(14, 'body', f('beam_column', w=1.5))]
    for k in range(12):
        ev.append(_ev(19 + k, f'orb{k}', snd('q5_orb')))
    for v, (tg, tl, tf) in enumerate(((37, 49, 42), (43, 55, 48))):
        ev.append(_ev(tg, 'glint', f('star_flare'), snd('q5_flare')))
        for k in range(6):
            ev.append(_ev(tg, f'land{v}_{k}', tele_disc(2.0, 12)))
            ev.append(_ev(tl, f'land{v}_{k}', f('orb_impact')))
        ev.append(_ev(tf, 'body', snd('q5_launch')))
        ev += [_ev(t, f'orb{k}', f('helix_trail')) for t in range(tf, tl) for k in range(0, 6, 2)]
        ev.append(_ev(tl, f'land{v}_0', snd('q5_impact')))
    ev += [_ev(52, 'lane', tele_line(14.0, 2.2, 12)), _ev(52, 'lane2', tele_line(14.0, 2.2, 12)),
           _ev(64, 'lane', f('leaf_skim', len=14.0), snd('q5_blades')), _ev(64, 'lane2', f('leaf_skim', len=14.0))]
    D['spiral'] = sum(ev, [])
    D['death'] = sum([
        _ev(0, 'floor', f'function {FN}tele/clear', hud('clear')), _ev(30, 'body', snd('d_droop'), snd('d_face_fade')),
        _ev(82, 'floor', f('water_splash'), snd('d_splash')), *[_ev(t, 'body', snd('d_leaves')) for t in (85, 100, 110)],
        *[_ev(t, 'body', f('leaf_dissolve')) for t in range(100, 119, 6)], _ev(100, 'body', snd('d_sink')),
        _ev(120, 'floor', snd('d_seed'))], [])
    return D


DEMOS = _demos()
DEMO_LEN = {k: max(t for t, _w, _l in v) + 30 for k, v in DEMOS.items()}
DEMO_PTS = {
    'L': (0.0, 0.0, 4.0), 'ahead4': (0.0, 0.0, 4.8), 'ahead7': (0.0, 0.0, 7.2), 'tip': (0.0, 3.0, -6.0),
    'bulb': (0.0, 9.0, 0.0), 'bulbT1': (0.0, 2.2, 0.0), 'egg': (0.0, 6.0, 0.0), 'crown': (0.0, 9.5, 0.0),
    'muzzle': (0.0, 1.8, 1.5), 'glint': (0.0, 9.0, 1.0), 'twig': (8.0, 1.5, 3.0), 'glide': (1.0, 0.0, 3.0),
    'wheel': (2.5, 1.0, 5.0), 'bolt': (-1.5, 1.6, 4.0), 'pk0': (1.4, 0.0, 6.0), 'pk1': (-1.6, 0.0, 6.6),
    'lane2': (2.4, 0.0, 0.0),
}
for _k in range(4):
    _x, _z = ring_xz(6.6, (-60, 60, -140, 140)[_k])
    DEMO_PTS[f'stalk{_k}'] = (_x, 0.0, 4.0 + _z)
for _k in range(3):
    DEMO_PTS[f'dome{_k}'] = ((-8.0, 0.0, 8.0) if _k == 1 else (8.0, 0.0, 8.0) if _k == 2 else (0.0, 0.0, 15.0))
    DEMO_PTS[f'spawn{_k}'] = ring_xz(8.0, -45 + 45 * _k)[0], 0.0, ring_xz(8.0, -45 + 45 * _k)[1] + 4
for _k in range(7):
    _x, _z = ring_xz(4.5, -75 + 25 * _k)
    DEMO_PTS[f'org{_k}'] = (_x, 0.0, 4 + _z)
for _k in range(4):
    DEMO_PTS[f'wall{_k}'] = (-2.4 + 1.6 * _k, 0.0, 6.0)
for _k in range(12):
    _x, _z = ring_xz(4.0 + (_k % 3), -70 + 12 * _k)
    DEMO_PTS[f'orb{_k}'] = (_x, 3.0 + (_k % 4) * 1.6, _z)
for _v in range(2):
    for _k in range(6):
        _x, _z = ring_xz(1.6 + (_k % 3) * 0.9, 60 * _k + 30 * _v)
        DEMO_PTS[f'land{_v}_{_k}'] = (_x + (1.5 if _v else -1.0), 0.0, 6.0 + _z)


def demo_where(where):
    """execute sub-commands of a demo event (run as the demo anchor marker, which faces the player)"""
    if where in ('floor', 'body', 'lane'):
        return 'at @s rotated as @s rotated ~ 0'
    if where == 'player':
        return 'at @p[tag=player] rotated as @s rotated ~ 0'
    if where == 'tail':
        return 'at @s rotated as @s rotated ~180 0 positioned ^ ^ ^2'
    if where in DEMO_PTS:
        x, y, z = DEMO_PTS[where]
        rot = ' rotated ~-20 0' if where.startswith('stalk') else ''
        return f'at @s rotated as @s rotated ~ 0 positioned ^{num(x, 2)} ^{num(y, 2)} ^{num(z, 2)}{rot}'
    raise ValueError(where)


def tests(W):
    t = ['# Every fx kind in rows in front of the executor (3 s each):',
         f'# /execute as @p at @s rotated ~ 0 run function {FN}test/kinds']
    for i, kind in enumerate(FX_KINDS):
        row, colm = divmod(i, 7)
        x = 4.5 - 1.5 * colm
        z = 4 + 2.2 * row
        plane = kind_info(kind)[0]
        if plane in ('flat', 'band'):
            t.append(card(kind, f'^{num(x)} ^0.05 ^{num(z)}', '~ 0', s0=0.3, s1=1.4, life=60, fade=10))
        else:
            t.append(card(kind, f'^{num(x)} ^1.2 ^{num(z)}', '~180 0', s0=0.3, s1=1.2, life=60, fade=10))
    W.w('test/kinds', t)
    W.w('test/tele', ['# One telegraph of each shape and palette around the executor (tell 40 t), the wave ring, a wedge',
                      '# stack, the crack strip, the wash with a safe rim, a moving ring and a wall spot:',
                      f'# /execute as @p at @s rotated ~ 0 run function {FN}test/tele',
                      'execute positioned ^4 ^ ^5 run ' + tele_disc(2.8, 40, 7),
                      'execute positioned ^-4 ^ ^5 run ' + tele_disc(1.5, 40, 20, nd=2),
                      'execute positioned ^ ^ ^11 run ' + tele_disc(3.5, 40, 23),
                      'execute positioned ^7 ^ ^12 run ' + tele_sector(4.5, 78, 40, 20),
                      'execute positioned ^-7 ^ ^12 run ' + tele_sector(3.1, 27, 40, 7, nd=1),
                      'execute positioned ^ ^ ^3 run ' + tele_line(6.0, 2.0, 40, 22),
                      'execute positioned ^-10 ^ ^4 rotated ~30 0 run ' + tele_crack(8.4, 3.0, 40),
                      'execute positioned ^ ^ ^20 run ' + tele_wave(0, 2.5, 12.0, 1.0, 40, 17, 20),
                      *['execute positioned ^10 ^ ^20 rotated ~180 0 run ' + tele_wedge(0, 6.0, -100 + 25 * k, -75 + 25 * k, 30 + k, 20)
                        for k in range(8)],
                      'execute positioned ^ ^ ^34 run ' + tele_mask_wash(8.0, 40, 40),
                      'execute positioned ^3 ^ ^34 run ' + tele_safe_rim(0, 3.0, 40, 40),
                      'execute positioned ^-12 ^ ^20 run ' + tele_mring(0, 3.6),
                      'execute positioned ^-4 ^ ^20 run ' + tele_wall_spot(12, 40)])
    W.w('test/sounds', ['# Click through the sound recipes (tellraw list).',
                        'tellraw @s [{"text":"아펩 sounds: ","color":"#A6D45A"}' +
                        ''.join(f',{{"text":"[{n}] ","color":"#D8F2B0","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}"}}}}' for n in SOUNDS) + ']'])
    W.w('test/hud', ['# The HUD: the T1 title, the 종말의 여파 banner and the edge flash (run in a fight to see the lines).',
                     hud('title', g='heart', t='「오아시스의 심장」', c='#EDCF63', s='마물을 처치해서 소생 진행도를 올리세요', hold=60),
                     hud('banner_aftermath'), hud('flash_hit')])
    W.w('test/props', ['# Every prop look on a display 4 b ahead (killed after 10 s by test/stop or the next call).',
                       'kill @e[type=minecraft:item_display,tag=rlk_wk_demo]'] +
        [f'execute positioned ^{num(4.5 - 1.5 * (i % 7))} ^1.2 ^{num(4 + 2.2 * (i // 7))} run summon minecraft:item_display ~ ~ ~ '
         f'{{Tags:["rlk_wk_demo","rlk_room","rlk_mb_aux"]}}' for i in range(len(PROPS))] +
        [f'execute as @e[type=minecraft:item_display,tag=rlk_wk_demo] run function {FN}prop/{name}'
         for name in list(PROPS)[:1]] +
        [f'execute as @e[type=minecraft:item_display,tag=rlk_wk_demo,limit=1,sort=nearest] run function {FN}prop/{name}'
         for name in list(PROPS)[1:]])
    W.w('test/presets', ['# Click through the presets (tellraw list; macro presets use test values).',
                         'tellraw @s [{"text":"아펩 fx: ","color":"#A6D45A"}' +
                         ''.join(f',{{"text":"[{n}] ","color":"#D8F2B0","click_event":{{"action":"run_command",'
                                 f'"command":"/execute at @s rotated ~ 0 positioned ^ ^ ^6 run {test_call(n)}"}}}}'
                                 for n in PRESETS) + ']'])
    W.w('test/stage', ['# Spawn the demo stand-in 9 b in front of the executor, facing it: a marker anchor and a vanilla stand-in',
                       '# (a big dripleaf display) on it, plus three dome markers for the flood demo. No rig calls.',
                       f'# /execute as @p at @s rotated ~ 0 run function {FN}test/stage, then test/demo/<name>.',
                       f'function {FN}test/stop',
                       'execute positioned ^ ^ ^9 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_wk_demo","rlk_room","rlk_mb_aux"]}',
                       'execute as @e[type=minecraft:marker,tag=rlk_wk_demo,limit=1] at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0',
                       'execute at @e[type=minecraft:marker,tag=rlk_wk_demo,limit=1] run summon minecraft:item_display ~ ~2 ~ '
                       '{Tags:["rlk_wk_demo","rlk_room","rlk_mb_aux"],item:{id:"minecraft:big_dripleaf",count:1},'
                       'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f],'
                       'right_rotation:[0f,0f,0f,1f]}}'] +
        [f'execute as @e[type=minecraft:marker,tag=rlk_wk_demo,limit=1] at @s rotated as @s rotated ~ 0 positioned '
         f'^{num(DEMO_PTS[f"dome{k}"][0])} ^ ^{num(DEMO_PTS[f"dome{k}"][2])} run summon minecraft:marker ~ ~ ~ '
         f'{{Tags:["rlk_wk_demo","{DOME_TAG}","rlk_room","rlk_mb_aux"]}}' for k in range(3)] +
        ['scoreboard players set #wkDemo mb 0', 'scoreboard players set #wkDT mb 0',
         f'schedule function {FN}test/e/tick 1t replace'])
    W.w('test/stop', ['# Remove the demo anchor, the stand-in, the dome markers and the test props.',
                      'kill @e[tag=rlk_wk_demo]', f'schedule clear {FN}test/e/tick', 'scoreboard players set #wkDemo mb 0'])
    tick = ['# Demo ticker (scheduled): the running demo\'s events as the anchor.',
            'execute unless entity @e[type=minecraft:marker,tag=rlk_wk_demo,limit=1] run return 0',
            'execute if score #wkDemo mb matches 1.. run scoreboard players add #wkDT mb 1']
    for k, name in enumerate(DEMOS, 1):
        tick.append(f'execute if score #wkDemo mb matches {k} as @e[type=minecraft:marker,tag=rlk_wk_demo,limit=1] '
                    f'run function {FN}test/demo/e/{name}')
        tick.append(f'execute if score #wkDemo mb matches {k} if score #wkDT mb matches {DEMO_LEN[name]}.. run '
                    'scoreboard players set #wkDemo mb 0')
    tick.append(f'schedule function {FN}test/e/tick 1t replace')
    W.w('test/e/tick', tick)
    for k, (name, events) in enumerate(DEMOS.items(), 1):
        W.w(f'test/demo/{name}', [f'# Demo "{name}": the kit calls of ap_fx_api.md §0.11 at their ticks around the stand-in.',
                                  '# Needs test/stage first.',
                                  'execute unless entity @e[type=minecraft:marker,tag=rlk_wk_demo,limit=1] run '
                                  f'function {FN}test/stage',
                                  f'scoreboard players set #wkDemo mb {k}', 'scoreboard players set #wkDT mb -1'])
        lines = [f'# Demo "{name}" events (as the anchor; #wkDT = the demo tick).']
        for tk, where, line in sorted(events, key=lambda e: e[0]):
            lines.append(f'execute if score #wkDT mb matches {tk} {demo_where(where)} run {line}')
        W.w(f'test/demo/e/{name}', lines)


def build_datapack(dp):
    W = Writer(dp)
    engine(W)
    telegraphs(W)
    dress_funcs(W)
    flood_tile(W)
    sounds(W)
    hud_funcs(W)
    presets_dp(W)
    props(W)
    tests(W)
    removed = W.flush()
    return len(W.files), removed


def manifest():
    return {
        'generator': 'tools/build_mboss_ap_fx.py', 'api': 'scratchpad ap/ap_fx_api.md',
        'functions': FN, 'item_models': NS_TEX, 'font': FONT, 'font_range': [f'U+{CP_LO:04X}', f'U+{CP_HI:04X}'],
        'storage': STO,
        'owned': {'dirs': [f'{FDIR}/{d}' for d in OWNED_DIRS], 'files': [f'{FDIR}/{f}.mcfunction' for f in OWNED_FILES],
                  'rp': [f'assets/rlk/textures/{TEXDIR}', f'assets/rlk/models/item/{TEXDIR}', f'assets/rlk/items/{TEXDIR}',
                         f'assets/rlk/font/{FONT_NAME}.json', f'assets/rlk/textures/font/{FONT_NAME}']},
        'caps': {'fx': CAP, 'telegraph': TCAP, 'telegraph_skip_from': TCAP - TSKIP, 'ambient_soft': SOFT,
                 'dressing': DCAP, 'flood': FLCAP},
        'objectives': list(OBJECTIVES),
        'fake_players': '#wk* (objective mb)',
        'tags': [TAG, f'{TAG}_t', f'{TAG}_wv<id>', f'{TAG}_sr<id>', f'{TAG}_mr<id>', f'{TAG}_mw', f'{TAG}_ws', f'{TAG}_d',
                 f'{TAG}_dsw', f'{TAG}_dly', f'{TAG}_dp', f'{TAG}_fl', 'rlk_wk_demo'],
        'kinds': {k: {'plane': kind_info(k)[0], 'px': list(kind_info(k)[1]), 'extent': list(kind_info(k)[2]),
                      'tint': 'neutral' if kind_info(k)[3] else 'painted', 'texture': kind_info(k)[4],
                      'source': 'own' if k in KINDS else 'alias' if k in ALIAS else 'fg kit (referenced)',
                      'desc': kind_info(k)[5]} for k in ALL_KINDS},
        'fg_references': {k: FG_TEX + v for k, v in REF.items()},
        'atlas_px_new': atlas_px(), 'atlas_budget': ATLAS_BUDGET,
        'presets': {k: {'args': v[1], 'doc': v[0], 'cards': preset_cards(k), 'pool_cards': preset_pool_cards(k),
                        'ambient': k in AMBIENT, 'particles_only': k in PTCL} for k, v in PRESETS.items()},
        'telegraphs': ['disc', 'sector', 'wedge', 'line', 'crack', 'wave', 'wave_end', 'mask_wash', 'safe_rim', 'safe_end',
                       'mring', 'mring_move', 'mring_end', 'wall_spot', 'clear'],
        'dress': list(DRESS),
        'props': {k: v[0] for k, v in PROPS.items()},
        'sounds': {k: {'use': v[0], 'layers': [list(l) for l in v[1]]} for k, v in SOUNDS.items()},
        'hud': {k: list(v) for k, v in HUD_FUNCS.items()},
        'glyphs': {k: f'U+{v[0]:04X}' for k, v in GLYPHS.items()},
        'badges': {k: {'name': v[0], 'colour': v[1]} for k, v in BADGES.items()},
        'palettes': {str(k): [f'#{c:06X}' for c in v] for k, v in TELE_COL.items()},
        'nd_rim': f'#{ND_RIM:06X}',
        'pieces': {'family': list(P.PIECES), 'max': PIECE_MAX, 'max_small_r': PIECE_MAX_SMALL, 'small_r': SMALL_R,
                   'k': [{'lo': lo, 'hi': hi, 'A': a, 'B': b, 'W': w} for lo, hi, a, b, w in piece_k_coeffs()]},
        'flood_cells': len(flood_cells()), 'dome_tag': DOME_TAG, 'dome_skip': DOME_SKIP,
        'demos': {k: DEMO_LEN[k] for k in DEMOS},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--resourcepack', help='unpacked resource pack root (assets/...)')
    ap.add_argument('--datapack', default=str(HERE.parent), help='datapack root (data/...)')
    ap.add_argument('--skip-rp', action='store_true', help='only write the datapack functions')
    a = ap.parse_args()
    n, removed = build_datapack(a.datapack)
    (HERE / 'mboss_ap_fx_manifest.json').write_text(json.dumps(manifest(), ensure_ascii=False, indent=1) + '\n',
                                                     encoding='utf-8')
    msg = (f'apep fx kit: {n} functions ({removed} stale removed), {len(PRESETS)} presets, {len(SOUNDS)} sounds, '
           f'{len(PROPS)} props')
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error('--resourcepack is required unless --skip-rp')
        k, nref, px, g = build_resourcepack(a.resourcepack)
        msg += f', {k} sprites ({px / 1e6:.3f} M new px), {nref} fg references, {g} glyphs in {FONT}'
    print(msg)


if __name__ == '__main__':
    main()
