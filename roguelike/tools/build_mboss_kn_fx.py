#!/usr/bin/env python3
"""FX / audio / HUD kit of the chapter-4 boss 아를레키노 (Arlecchino, Genshin Impact).

The Tachy kit's card engine (tools/build_mboss_tk_fx.py: the fg kit engine with its first-tick fix, counted pools, the
self-rescheduling ager, no shared-file hooks) copied and renamed, with the call list frozen in
tools/mboss_arlecchino/api.py §8 (KIT_PRESETS, KIT_PROPS, KIT_DECALS, KIT_SOUNDS, KIT_HUD, KIT_FIXED; scratchpad
ar/contract.md §3.3). The module (S2 sequences, S3 core / phase 1, S4 phase 2) calls it only through api.K; nothing here
decides gameplay (hits, hazards, projectiles, timings stay in the module). Parts, all regenerated on every run:

  1. The tinted card engine: painted sprites on short-lived item_display cards (planes face, flat, cross, lance). Pools:
     fx cards (cap CAP; ambient presets skipped from SOFT live cards) and floor decals (rlk_kn_fx_d: never capped, never
     skipped; the flood keeps one card that a second call re-times).
  2. Presets fx/p/<name> (macro args in tenths of a block / degrees / ticks / c 1 Pyro orange-gold, 2 crimson Bond of
     Life), props fx/prop/<name> (@s = the projectile / prop item_display, dressed in place: exactly one card each, facing
     its flight; any other entity, e.g. a sequence marker, gets one follower display that the kit keeps on it), the
     seven floor decals fx/decal/<name> (PLAN §1.5 only, at floor y + 0.02, each flashing DECAL_FLASH ticks before its
     hit tick t), sound recipes fx/snd/<name> (vanilla events only, the mboss_lib.sound min-volume rule).
  3. The HUD: font rlk:mboss_kn (U+EB00-EBFF): the badge glyph; fx/hud/badge {on} (◆선혈의 충격 appended to the boss-bar
     third line rlk:mboss sub, idempotent, re-appended while on after any rewrite of sub), fx/hud/banner {on} (the real
     game's Banquet banner, api.BANNER, as a text line under the boss bars: the footage shows it there), fx/hud/line
     {id} (the dialog subtitle of api.LINES[id], Raiden's letter reveal), fx/hud/clear. The glyph root text is always
     empty and unstyled; the font ends with a reference to minecraft:default.
  4. In-game demos fx/test/<preset>, fx/test/prop/<name>, fx/test/decal/<name> on a vanilla stand-in (an armour stand
     with a netherite hoe), fx/test/{stage,stop,sounds,hud,kinds}.

Generic glows are the field generator kit's sprites, referenced from our item models (no repaint): glow, mote, spark.

Outputs (owned; stale files in these places are removed):
  resource pack  assets/rlk/textures/mboss/kn_kit/<kind>.png      painted sprites (stdlib painter)
                 assets/rlk/models/item/mboss/kn_kit/<kind>.json    card models (tintindex 0)
                 assets/rlk/items/mboss/kn_kit/<kind>.json          item definitions, custom_model_data tint
                 assets/minecraft/atlases/items.json                adds rlk:mboss/kn_kit/* (merges)
                 assets/rlk/font/mboss_kn.json + textures/font/mboss_kn/*.png
  datapack       data/rlk/function/boss/arlecchino/fx/{card,cardx,look,clear,uninstall}
                 data/rlk/function/boss/arlecchino/fx/{e,p,prop,decal,snd,hud,test}/**
  manifest       tools/mboss_kn_fx_manifest.json   (its presence switches api.K on)

Cards carry rlk_kn_fx + rlk_room + rlk_mb_aux. Objectives knFx (fake players) and knFxS knFxG knFxH knFxK knFxD (the
card stage clock), knFxL (prop follower links); storage rlk:kn fx.*; bossbar rlk:kn_banner. The module wires cleanup ->
fx/clear + fx/hud/clear, pause / death_start -> fx/clear, uninstall -> fx/uninstall (contract §3.3).

Run: python3 tools/build_mboss_kn_fx.py --resourcepack <unpacked RP>   (or --skip-rp: the datapack + manifest only)
"""
from pathlib import Path
# VP beat (round V, lane VP): the kit clock is the game time minus the ticks the perfect parry / dodge beat held the world
# (#btLag cb, player/def/beat/clock): while the fight is frozen the effects stand still, and a timed effect stays in step
# with the hit it announces.
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
import mboss_kn_fx_paint as P  # noqa: E402
import mboss_lib as L  # noqa: E402
from mboss_arlecchino import api  # noqa: E402

ROOT = api.ROOT                        # boss/arlecchino
FN = f'rlk:{ROOT}/fx/'
FDIR = f'data/rlk/function/{ROOT}/fx'
NS_TEX = 'rlk:mboss/kn_kit/'
TEXDIR = 'mboss/kn_kit'
FG_TEX = 'rlk:mboss/fg_kit/'
FG_TEXDIR = 'mboss/fg_kit'
FONT = 'rlk:mboss_kn'
FONT_NAME = 'mboss_kn'
STO = api.STORAGE                      # rlk:kn; kit keys fx.* (contract §2)
CAP = 96            # live fx cards; further fx cards are skipped until some expire (decals never)
SOFT = 64           # ambient presets are skipped from SOFT live fx cards on
ATLAS_BUDGET = 700_000                 # new px of the items atlas (contract §5: S1K <= 0.70 M)
OWNED_DIRS = ('e', 'p', 'prop', 'decal', 'snd', 'hud', 'test')
OWNED_FILES = tuple(api.KIT_FIXED)     # card cardx look clear uninstall
OBJ = 'knFx'                           # the kit's fake players
OBJECTIVES = ('knFxS', 'knFxG', 'knFxH', 'knFxK', 'knFxD', 'knFxL')
TAG = api.TAGS['fx']                   # rlk_kn_fx
DEMO = f'{TAG}_demo'
ANIM = f'{TAG}a'                       # props the anim chain turns (rlk_kn_fxa + _w wheel / _s spirit)
FOLLOW = f'{TAG}f'                     # follower displays (a prop called on a non-display entity)
LEAD = f'{TAG}l'                       # the entities followers stay on
BANNER_BAR = 'rlk:kn_banner'
FLOOR = api.CY                         # the arena floor (fl_ruins: y 201); demos store their own in fx.fl
DECAL_Y = 0.02                         # every decal at floor y + 0.02 (layers up to + 0.028 against z-fighting)
MANIFEST = HERE / 'mboss_kn_fx_manifest.json'
assert MANIFEST == api.KIT_MANIFEST
C_PY, C_BOL = api.C_PYRO, api.C_BOL    # 1, 2


def rgb(h):
    return int(h[1:], 16)


# ----------------------------------------------------------------------------- colours (RGB ints for tints)
WHITE = 0xFFFFFF
PYRO = rgb('#FF9A3A')          # warm-white sprites x this = the orange-gold flame (#FF8A2A -> #FFD27A)
PYRO_GOLD = rgb('#FFD27A')
PYRO_DEEP = rgb('#FF8A2A')
CRIM = rgb('#FF3A4A')          # warm-white sprites x this = the bright crimson
CRIM_DEEP = rgb('#7A0A1A')
ROSE = rgb('#FFB0B8')
EMBER = rgb('#FF6A2A')
DIM = rgb('#A8A8A8')           # decals at rest (the painted colours x 0.66); the flash = WHITE (full)
DIM2 = rgb('#888888')
FADE_P = rgb('#C08870')        # the last slash-arc frame darkens as it fades
FADE_C = rgb('#905058')
SPIRIT = {1: WHITE, 2: rgb('#FF4A54')}      # wisp c 1 white (the intro spirits), c 2 red (P2)
TINT = {C_PY: PYRO, C_BOL: CRIM}
DEEP = {C_PY: PYRO_DEEP, C_BOL: CRIM_DEEP}
ARCK = {C_PY: 'arc_p', C_BOL: 'arc_c'}
RINGK = {C_PY: 'ring_p', C_BOL: 'ring_c'}
DUSTC = {C_PY: (1.0, 0.55, 0.16), C_BOL: (0.72, 0.04, 0.12)}

# ----------------------------------------------------------------------------- kinds
# name -> (plane, (w, h) px, card extent in blocks at scale 1 (a0, a1, b0, b1), painter box, painter, supersampling,
#          neutral?, description). Planes: face (x-y quad), flat (x-z quad, +b forward), cross (two vertical quads), lance
#          (a flat and a vertical quad along local +z: beams and streaks seen from any side).
SQ = (-0.5, 0.5, -0.5, 0.5)
BX = (-1, 1, -1, 1)
UNIT = (-1, 1, -1, 1)
ARC = (-1, 1, 0, 1)
FOOT_N = (-0.25, 0.25, 0.0, 1.0)
FOOT_8 = (-0.125, 0.125, 0.0, 1.0)
FOOT_16 = (-0.0625, 0.0625, 0.0, 1.0)
STROKE = (-0.125, 0.125, -0.5, 0.5)
NARROW = (-0.25, 0.25, -0.5, 0.5)
WIDE = (-0.5, 0.5, -0.25, 0.25)
WIDE_P = (-1, 1, -0.5, 0.5)
LANCE = (-0.5, 0.5, 0.0, 1.0)
STRIP = (-0.5, 0.5, -0.5, 0.5)
KINDS = {
    # slash arcs: four sweep frames per colour (flat, unit radius = the reach at scale r)
    **{f'arc_p{k}': ('flat', (128, 64), ARC, ARC, P.make_arc(k, 'p'), 2, False,
                     f'Pyro slash-arc sweep frame {k} (orange-gold flame band on r 0.8)') for k in range(4)},
    **{f'arc_c{k}': ('flat', (128, 64), ARC, ARC, P.make_arc(k, 'c'), 2, False,
                     f'crimson slash-arc sweep frame {k} (Bond of Life: crimson band, black smoke)') for k in range(4)},
    'ring_p':     ('flat', (128, 128), UNIT, UNIT, P.make_ring('p'), 2, False, 'Pyro spin ring of fire (unit radius)'),
    'ring_c':     ('flat', (128, 128), UNIT, UNIT, P.make_ring('c'), 2, False, 'crimson ring with black smoke (unit radius)'),
    # props
    **{f'wheel_{k}': ('face', (64, 64), SQ, BX, P.make_wheel(k), 2, False,
                      f'flaming scythe wheel, spin frame {k} (the scythe turned {90 * k} deg)') for k in range(4)},
    'crescent':   ('face', (128, 64), WIDE, WIDE_P, P.paint_crescent, 2, False, 'P2 thrown flame crescent (one quad facing its flight)'),
    'feather':    ('face', (32, 64), NARROW, NARROW, P.paint_feather, 2, False, 'crimson feather bolt, tip down'),
    'orb':        ('face', (32, 32), SQ, BX, P.paint_orb, 3, False, 'crimson orb'),
    'blade':      ('face', (32, 128), FOOT_8, (-0.125, 0.125, 0.0, 1.0), P.paint_blade, 2, False,
                   'giant crimson blade, base at b 0'),
    'clone':      ('face', (64, 128), FOOT_N, FOOT_N, P.paint_clone, 2, False, 'crimson shadow clone, feet at b 0'),
    **{f'wisp_{k}': ('face', (32, 32), SQ, BX, P.make_wisp(k), 3, True, f'white flame spirit, frame {k} (tinted)')
       for k in range(3)},
    'halo':       ('face', (128, 128), SQ, BX, P.paint_halo, 2, False, 'red-moon halo ring'),
    # effect sprites
    'claw':       ('face', (64, 64), SQ, BX, P.paint_claw, 2, False, 'crimson claw closing'),
    'thread':     ('face', (16, 128), FOOT_16, (-0.0625, 0.0625, 0.0, 1.0), P.paint_thread, 2, False,
                   'crimson thread from the sky, base at b 0'),
    'thorn':      ('face', (32, 64), FOOT_N, FOOT_N, P.paint_thorn, 2, False, 'crimson thorn spike, base at b 0'),
    'web':        ('flat', (128, 128), UNIT, UNIT, P.paint_web, 2, False, 'crimson web (H perch)'),
    'stroke':     ('face', (32, 128), STROKE, STROKE, P.paint_stroke, 2, False, 'one carved crimson slash stroke (X halves)'),
    'brand':      ('flat', (128, 128), UNIT, UNIT, P.paint_brand, 2, False, 'crimson sigil ring of the forced bond'),
    'reticle':    ('face', (128, 128), SQ, BX, P.paint_reticle, 2, False, 'Q4 aim reticle'),
    'beam':       ('lance', (32, 128), LANCE, LANCE, P.paint_beam, 2, False, 'Q4 crimson beam body (along +z)'),
    'aim':        ('lance', (16, 128), LANCE, LANCE, P.paint_aim, 2, False, 'Q4 thin red aim line (along +z)'),
    'streak':     ('lance', (32, 128), LANCE, LANCE, P.paint_streak, 2, True, 'soft streak along +z (tinted)'),
    'flame':      ('face', (32, 64), FOOT_N, FOOT_N, P.paint_flame, 2, True, 'flame tongue, root at b 0 (tinted)'),
    'ember':      ('face', (16, 16), SQ, BX, P.paint_ember, 3, True, 'glowing ember fleck (tinted)'),
    'smoke':      ('face', (32, 32), SQ, BX, P.paint_smoke, 3, False, 'black-crimson smoke puff'),
    'burst':      ('face', (64, 64), SQ, BX, P.paint_burst, 2, True, 'starburst flash (tinted)'),
    'pillar':     ('cross', (32, 128), FOOT_8, FOOT_8, P.paint_pillar, 2, False, 'crimson flame column, root at b 0'),
    'veil':       ('face', (64, 64), SQ, BX, P.paint_veil, 2, True, 'T form-swap shroud: dense flame veil, opaque core (tinted)'),
    # floor decals (flat; unit radius / unit length; at floor + 0.02)
    'flood':      ('flat', (128, 128), UNIT, UNIT, P.paint_flood, 2, False, 'F red flood / E70 pool decal'),
    'cracks':     ('flat', (256, 256), UNIT, UNIT, P.paint_cracks, 1, False, 'F glowing crimson cracks decal'),
    'strip':      ('flat', (32, 128), STRIP, STRIP, P.paint_strip, 2, False, 'G translucent red strip decal (unit w x len)'),
    'band':       ('flat', (128, 128), UNIT, UNIT, P.paint_band, 2, False, 'G rim-tint annulus 0.7-1.0 decal'),
    'ring':       ('flat', (256, 256), UNIT, UNIT, P.paint_ring, 1, False, 'Q5A red ring outline decal'),
    # the gate icon
    'gate_icon':  ('face', (64, 64), SQ, BX, P.paint_gate_icon, 2, False, 'gate label icon: a crimson scythe across a red moon'),
}
DECAL_KINDS = ('flood', 'cracks', 'strip', 'band', 'ring')
# Generic kinds referenced from the fg kit (our item model points at the fg texture; no px of our own).
REF = {'glow': 'glow', 'mote': 'mote', 'spark': 'spark'}
REF_NEUTRAL = ('glow', 'mote')
ALL_KINDS = list(KINDS) + list(REF)
SPIN_Y = ('flat', 'cross')             # planes that spin about local y; face / lance spin about z


def _fg():
    import build_mboss_fg_fx as FG
    return FG


def kind_info(kind):
    """(plane, (w, h), extent, neutral, texture id, description) of an own or referenced kind"""
    if kind in KINDS:
        v = KINDS[kind]
        return v[0], v[1], v[2], v[6], NS_TEX + kind, v[7]
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
    """Zero-thickness double-sided quads with tintindex 0 (fg kit convention: display-local p is written at model
    m = (8 - 16 px, 8 + 16 py, 8 - 16 pz); card +a = local -x = model +x). The lance's vertical quad maps the texture
    rows along z (face rotation), so a beam texture runs along the beam on both quads."""
    plane, _s, (a0, a1, b0, b1), _n, tex, _d = kind_info(kind)
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
CP_LO, CP_HI = 0xEB00, 0xEBFF
# name -> (codepoint, painter (x right, y up, -1..1), texture px (w, h), height, ascent)
GLYPHS = {
    'badge': (0xEB00, P.glyph_badge, (32, 32), 8, 7),
}
LINE_COL = '#FF9AA8'                  # the dialog subtitles (S3's stand-in colour)
LINE_GAP, LINE_HOLD = 2, 44           # ticks per typing step, ticks the full line stays
BADGE_COL, BADGE_TXT = '#FF3A4A', '#FF5A64'
BANNER_HOT, BANNER_REST = '#F07858', '#FFFFFF'   # ref/hud_bars_banner.jpg: the first phrase salmon-red, the rest white
BANNER_SPLIT = api.BANNER.index('으로 ')
assert api.BADGE.startswith('◆')


def glyph(name):
    return chr(GLYPHS[name][0])


def badge_component():
    """The 선혈의 충격 badge for the boss-bar third line (rlk:mboss sub[]): the root text is empty and unstyled; the
    glyph sibling carries the kit font (the ◆), the name is a plain sibling (no font inheritance)."""
    return (f'{{text:"",extra:[{{text:"  "}},{{text:"{glyph("badge")}",font:"{FONT}",color:"{BADGE_COL}"}},'
            f'{{text:"{api.BADGE[1:]}",color:"{BADGE_TXT}",bold:true}}]}}')


BADGE_MATCH = f'rlk:mboss sub[{{extra:[{{font:"{FONT}"}}]}}]'


def banner_component():
    """api.BANNER as the real game shows it: '생명의 계약을 제거하고 일반 공격' salmon-red, the rest white."""
    a, b = api.BANNER[:BANNER_SPLIT], api.BANNER[BANNER_SPLIT:]
    return f'{{text:"",extra:[{{text:"{a}",color:"{BANNER_HOT}"}},{{text:"{b}",color:"{BANNER_REST}"}}]}}'


def paint_glyph(fn, w, h, ss=4):
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
            if al < 0.1 or aa <= 0:
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


def build_font(rp):
    rp = Path(rp)
    tex = rp / f'assets/rlk/textures/font/{FONT_NAME}'
    font_path = rp / f'assets/rlk/font/{FONT_NAME}.json'
    ours = [g[0] for g in GLYPHS.values()]
    assert all(CP_LO <= c <= CP_HI for c in ours) and len(set(ours)) == len(ours)
    clash = font_used_elsewhere(rp, font_path)
    hit = [c for c in ours if c in clash]
    if hit:
        raise SystemExit(f'{FONT} glyphs collide with ' + ', '.join(f'U+{c:04X} ({clash[c]})' for c in hit))
    tex.mkdir(parents=True, exist_ok=True)
    for old in tex.glob('*'):
        if old.stem not in GLYPHS or old.suffix != '.png':
            old.unlink()
    providers = []
    for name, (cp, painter, (w, h), height, ascent) in GLYPHS.items():
        raw = paint_glyph(painter, w, h)
        rows = b''.join(b'\x00' + bytes(raw[y * w * 4:(y + 1) * w * 4]) for y in range(h))
        data = png_bytes(w, h, rows)
        p = tex / f'{name}.png'
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
        providers.append({'type': 'bitmap', 'file': f'rlk:font/{FONT_NAME}/{name}.png', 'ascent': ascent,
                          'height': height, 'chars': [chr(cp)]})
    # every char the kit does not draw falls back to the default font (a component that inherits this font by mistake
    # still shows its text)
    providers.append({'type': 'reference', 'id': 'minecraft:default'})
    text = json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n'
    font_path.parent.mkdir(parents=True, exist_ok=True)
    if not font_path.exists() or font_path.read_text(encoding='utf-8') != text:
        font_path.write_text(text, encoding='utf-8')
    return len(GLYPHS)


def build_resourcepack(rp):
    rp = Path(rp)
    px = atlas_px()
    assert px <= ATLAS_BUDGET, f'atlas budget: {px} new px > {ATLAS_BUDGET}'
    for k, v in KINDS.items():
        w, h = v[1]
        assert w <= 256 and h <= 256 and w % 16 == 0 and h % 16 == 0, (k, w, h)
        assert k == k.lower() and re.fullmatch(r'[a-z0-9_]+', k), k
    n_ref = check_refs(rp)
    n_glyphs = build_font(rp)
    root = rp / 'assets/rlk'
    tex_dir = root / f'textures/{TEXDIR}'
    dirs = {tex_dir: (KINDS, '.png'), root / f'models/item/{TEXDIR}': (ALL_KINDS, '.json'),
            root / f'items/{TEXDIR}': (ALL_KINDS, '.json')}
    for d, (keep, suf) in dirs.items():
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob('*'):
            if old.stem not in keep or old.suffix != suf:
                old.unlink()
    for kind in KINDS:
        w, h, raw = render(kind)
        data = png_bytes(w, h, raw)
        p = tex_dir / f'{kind}.png'
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)

    def put(p, obj):
        text = json.dumps(obj, separators=(',', ':')) + '\n'
        if not p.exists() or p.read_text(encoding='utf-8') != text:
            p.write_text(text, encoding='utf-8')
    for kind in ALL_KINDS:
        put(root / f'models/item/{TEXDIR}' / f'{kind}.json', model_json(kind))
        put(root / f'items/{TEXDIR}' / f'{kind}.json', item_json(kind))
    atlaspath = rp / 'assets/minecraft/atlases/items.json'
    atlas = json.loads(atlaspath.read_text(encoding='utf-8')) if atlaspath.exists() else {'sources': []}
    atlas['sources'] = [s for s in atlas['sources'] if not str(s.get('resource', '')).startswith(NS_TEX)
                        or s['resource'][len(NS_TEX):] in KINDS]
    have = {s.get('sprite', s.get('resource')) for s in atlas['sources']}
    for kind in KINDS:
        if NS_TEX + kind not in have:
            atlas['sources'].append({'type': 'minecraft:single', 'resource': NS_TEX + kind})
    text = json.dumps(atlas, indent=2) + '\n'
    if not atlaspath.exists() or atlaspath.read_text(encoding='utf-8') != text:
        atlaspath.parent.mkdir(parents=True, exist_ok=True)
        atlaspath.write_text(text, encoding='utf-8')
    return len(KINDS), n_ref, px, n_glyphs


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


POOLS = {'fx': (0, f'{TAG}_c'), 'dc': (1, f'{TAG}_d'), 'fl': (1, f'{TAG}_fl')}


def card(kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8, fade=0,
         col=WHITE, dly=0, dur=0, hit=-1, col2=-1, off=None, pool='fx'):
    """The function line that spawns one card (fx/card, or fx/cardx when an extended option is used): pos / rot of the
    card (relative to the executor; rot may be absolute), billboard, roll (left_rotation about local z), spin over the
    main interpolation, s0 -> s1 (float or (x, y, z)), off (static start translation) + move, life / fade ticks, col
    tint, dly hidden ticks, dur main-interpolation ticks (0 = to the fade), hit / col2 the second tint, pool 'fx' (capped)
    / 'dc' decal / 'fl' the flood decal. Any value may be a macro placeholder string such as '$(r)'."""
    assert kind in ALL_KINDS, kind
    assert bb in ('fixed', 'center', 'vertical', 'horizontal'), bb
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


# ----------------------------------------------------------------------------- particles (vanilla)


def colour_list(c):
    if isinstance(c, int):
        c = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
    return '[' + ','.join(num(float(x), 3) + 'f' for x in c) + ']'


def _d(v):
    return v if isinstance(v, str) else num(float(v), 3)


def part(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    d = ' '.join(_d(v) for v in delta)
    return f'particle minecraft:{name} {pos} {d} {num(float(speed), 3)} {int(n)} force @a[tag=player]'


def dust(c, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1, speed=0.0):
    return part(f'dust{{color:{colour_list(c)},scale:{num(float(scale), 2)}}}', pos, delta, speed, n)


def flash(c, pos='~ ~ ~', alpha=1.0):
    cl = colour_list(c)[:-1] + f',{num(float(alpha), 2)}f]'
    return part(f'flash{{color:{cl}}}', pos, (0, 0, 0), 0, 1)


def blockp(block, pos='~ ~ ~', delta=(0, 0, 0), speed=0.0, n=1):
    return part(f'block{{block_state:"minecraft:{block}"}}', pos, delta, speed, n)


def c_parts(c, pos='~ ~ ~', delta=(0.3, 0.3, 0.3), n=8):
    """the colour's particle signature: Pyro flame + small flame, Bond of Life crimson dust + black smoke"""
    if c == C_PY:
        return [part('flame', pos, delta, 0.03, n), part('small_flame', pos, delta, 0.02, max(1, n // 2))]
    return [dust(DUSTC[C_BOL], 1.4, pos, delta, n), part('large_smoke', pos, delta, 0.02, max(1, n // 3))]


# ----------------------------------------------------------------------------- sound recipes (PLAN §3, §5, §6)
# name -> (use, [(event, volume, pitch), ...]); one tick each, vanilla events only (checked against the game's sound
# list when scratchpad rd/tests/sound_ids.txt is present).
SOUNDS = {
    # intro (PLAN §3.1)
    'tea_sip':      ('E0 t16: she sips the tea.', [('entity.generic.drink', 0.35, 1.3)]),
    'wisp_chime':   ('E0 t4 / t20: the white flame spirits.', [('block.amethyst_block.chime', 0.3, 1.0)]),
    'cup_embers':   ('E1 t34: cup and saucer burst into embers.', [('block.fire.extinguish', 0.4, 1.6)]),
    'wisps_flee':   ('E1 t35: the spirits flee to the rim posts.', [('entity.allay.item_thrown', 0.4, 1.0)]),
    'ember_reach':  ('E2 t44: crimson embers stream into her palm.', [('block.respawn_anchor.charge', 0.5, 1.4)]),
    'scythe_vortex': ('E3 t52: the crimson flame vortex.', [('item.firecharge.use', 0.6, 0.7), ('block.fire.ambient', 0.6, 1.0)]),
    'scythe_form':  ('E4 t62: the haft grows out of the palm.', [('entity.blaze.shoot', 0.6, 0.8)]),
    'blade_ignite': ('E4 t70: the crescent ignites.', [('item.trident.return', 0.6, 1.0), ('item.firecharge.use', 0.4, 1.2)]),
    'intro_title':  ('E5 t80: the title.', [('entity.wither.ambient', 0.25, 1.8)]),
    'twirl':        ('E6 t94 / t100: the 360 twirl.', [('entity.player.attack.sweep', 0.6, 0.6)]),
    'twirl_ring':   ('E6 t96 / t98: the ring closes, the floor ring.', [('item.trident.riptide_1', 0.5, 1.3)]),
    'flip':         ('E8 t112: the scythe rolls through the hand.', [('item.armor.equip_netherite', 0.6, 1.0)]),
    'stance':       ('E9 t120: the stance.', [('block.respawn_anchor.set_spawn', 0.5, 0.7)]),
    'heartbeat':    ('E9 t126.', [('entity.warden.heartbeat', 0.6, 1.0)]),
    # transition T (PLAN §3.2)
    't_stagger':    ('T 0: she staggers to one knee.', [('entity.wither.hurt', 0.4, 1.6), ('item.armor.equip_netherite', 0.5, 0.7)]),
    't_pillar':     ('T 24: the crimson pillar builds.', [('block.fire.ambient', 0.8, 0.7), ('block.beacon.deactivate', 0.6, 1.0)]),
    't_dark':       ('T 50: the blackout.', [('entity.warden.sonic_charge', 0.4, 1.0)]),
    't_swap':       ('T 90: the form swap inside the pillar.', [('entity.blaze.ambient', 0.6, 0.5)]),
    't_legs':       ('T 110 / 116 / 122: a pair of blade legs unfolds.', [('entity.phantom.flap', 0.5, 0.8), ('item.elytra.flying', 0.3, 1.4)]),
    't_scythes':    ('T 130: the twin scythes form.', [('item.trident.return', 0.6, 0.9), ('item.trident.return', 0.5, 1.1)]),
    't_title':      ('T 140: the title.', [('entity.ender_dragon.growl', 0.4, 1.2)]),
    't_launch':     ('T 150: she launches up and away.', [('entity.phantom.swoop', 0.6, 1.0)]),
    # death (PLAN §3.3)
    'death_lower':  ('Death 0-10: she lowers both scythes.', [('item.armor.equip_netherite', 0.5, 0.7)]),
    'death_flames': ('Death 70: crimson flames climb her.', [('block.fire.ambient', 0.8, 0.6), ('entity.blaze.burn', 0.4, 0.7)]),
    'death_gone':   ('Death 96: she vanishes in a flame burst.', [('block.fire.extinguish', 0.8, 0.6), ('item.firecharge.use', 0.6, 0.5)]),
    # fight (PLAN §4-6)
    'step':         ('Walk events.', [('entity.player.attack.nodamage', 0.4, 0.6)]),
    'swing_light':  ('T1 swings.', [('entity.player.attack.sweep', 0.8, 1.1), ('item.firecharge.use', 0.3, 1.4)]),
    'swing_heavy':  ('T2+ swings.', [('entity.player.attack.sweep', 1.0, 0.7), ('item.firecharge.use', 0.5, 0.9)]),
    'spin':         ('A h3 / h5, Q1 h1 spin rings.', [('entity.player.attack.sweep', 1.0, 0.6), ('item.trident.riptide_1', 0.6, 1.3)]),
    'slam':         ('A h4 overhead slam.', [('entity.generic.explode', 0.7, 1.2), ('block.anvil.land', 0.4, 0.6)]),
    'wheel_spin':   ('B 10: the scythe spins into a wheel.', [('item.trident.riptide_2', 0.6, 1.4), ('block.fire.ambient', 0.6, 1.0)]),
    'wheel_throw':  ('B release.', [('item.trident.throw', 1.0, 0.7), ('entity.blaze.shoot', 0.5, 0.8)]),
    'wheel_catch':  ('B catch.', [('item.trident.return', 0.8, 0.9)]),
    'claw_reach':   ('B2 76: the reach, crimson glow on the palm.', [('block.respawn_anchor.charge', 0.6, 1.5)]),
    'claw_grab':    ('B2 96: the claw closes.', [('entity.evoker_fangs.attack', 1.0, 0.7), ('entity.wither.hurt', 0.4, 1.6)]),
    'leap':         ('C / H / E leaps.', [('entity.ender_dragon.flap', 0.7, 1.4), ('item.firecharge.use', 0.6, 0.8)]),
    'apex':         ('C apex spin.', [('block.fire.ambient', 0.8, 0.7)]),
    'dive':         ('C / E / H dives.', [('entity.phantom.swoop', 0.8, 1.2)]),
    'impact':       ('C impact.', [('entity.generic.explode', 0.9, 1.0), ('item.firecharge.use', 0.6, 0.6)]),
    'wing_burst':   ('Wings burst open.', [('entity.phantom.flap', 0.8, 0.6), ('item.elytra.flying', 0.4, 1.6)]),
    'wing_hit':     ('Wing strikes (Bond of Life).', [('entity.player.attack.sweep', 1.0, 0.5), ('entity.wither.shoot', 0.4, 1.4)]),
    'dash_tell':    ('D / E flare tell.', [('entity.ravager.roar', 0.4, 1.8), ('block.respawn_anchor.charge', 0.5, 1.2)]),
    'dash':         ('D dash.', [('entity.blaze.shoot', 0.7, 1.4), ('entity.phantom.swoop', 0.5, 1.6)]),
    'follow':       ('D2 follow-up burst.', [('entity.player.attack.sweep', 1.0, 0.8), ('entity.generic.explode', 0.5, 1.4)]),
    'zig':          ('E lateral dashes.', [('entity.phantom.swoop', 0.5, 1.8)]),
    'sweep':        ('Sweeps.', [('entity.player.attack.sweep', 1.0, 0.6)]),
    'brand':        ('Forced bond: the sigil closes, the brand.', [('block.respawn_anchor.set_spawn', 0.7, 1.4),
                                                                  ('entity.wither.shoot', 0.4, 0.6)]),
    'bond_gain':    ('A Bond-of-Life hit lands.', [('block.respawn_anchor.charge', 0.6, 0.7)]),
    'bond_tick':    ('The bond DoT.', [('block.fire.extinguish', 0.25, 1.6)]),
    'orb_spawn':    ('Heal orbs appear.', [('block.amethyst_block.chime', 0.6, 1.2)]),
    'flood':        ('F / E70: the red flood / pool spreads.', [('block.respawn_anchor.deplete', 0.8, 0.6)]),
    'threads':      ('F hit 1: threads and thorns.', [('entity.evoker_fangs.attack', 1.0, 0.8), ('entity.wither.shoot', 0.5, 0.6)]),
    'blast':        ('F hit 2 / G field: the blast.', [('entity.generic.explode', 1.0, 0.7), ('entity.wither.break_block', 0.4, 1.2)]),
    'cracks':       ('F the cracks.', [('block.basalt.break', 0.8, 0.6)]),
    'blade_rise':   ('G blades rise.', [('block.pointed_dripstone.place', 1.0, 0.6), ('item.trident.return', 0.5, 0.6)]),
    'blade_fly':    ('G the blades fly in along the cross lines.', [('item.trident.throw', 0.9, 0.6), ('entity.phantom.swoop', 0.6, 0.7)]),
    'cross_hit':    ('G cross strikes.', [('entity.evoker_fangs.attack', 1.0, 1.0), ('entity.player.attack.sweep', 0.8, 0.6)]),
    'rim':          ('G rim blades erupt.', [('block.pointed_dripstone.fall', 1.0, 0.7)]),
    'clone_launch': ('H clones dive.', [('entity.phantom.swoop', 0.8, 0.8), ('entity.illusioner.cast_spell', 0.5, 1.2)]),
    'clone_hit':    ('H clone slashes.', [('entity.player.attack.sweep', 1.0, 0.9), ('entity.wither.shoot', 0.3, 1.6)]),
    'perch':        ('H perch on the web.', [('entity.spider.ambient', 0.5, 0.6)]),
    'shock_gain':   ('선혈의 충격 armed.', [('block.beacon.power_select', 0.8, 1.4), ('entity.wither.ambient', 0.25, 1.8)]),
    'shock_hit':    ('선혈의 충격 outside a window.', [('entity.generic.explode', 0.7, 1.4), ('block.respawn_anchor.deplete', 0.6, 1.4)]),
    'break':        ('The Banquet broken.', [('entity.wither.break_block', 1.0, 0.8), ('block.glass.break', 1.0, 0.6)]),
    'stun':         ('Stun.', [('entity.iron_golem.damage', 0.6, 0.6)]),
    'beam_aim':     ('Q4 aim line + reticle.', [('block.beacon.ambient', 0.7, 1.8), ('block.respawn_anchor.charge', 0.5, 1.6)]),
    'beam_fire':    ('Q4 the beam.', [('entity.warden.sonic_boom', 0.6, 1.4), ('entity.blaze.shoot', 0.6, 0.6)]),
    'x_carve':      ('Q5B the red X carved.', [('entity.player.attack.sweep', 1.0, 0.5), ('block.respawn_anchor.set_spawn', 0.6, 0.8)]),
    'rapid':        ('Q5B rapid slashes (each).', [('entity.player.attack.sweep', 0.7, 1.5)]),
    'final':        ('Q5B final burst.', [('entity.generic.explode', 1.0, 0.6), ('entity.wither.break_block', 0.6, 0.8),
                                          ('block.respawn_anchor.deplete', 0.6, 0.6)]),
    'feather':      ('Q6 a feather volley.', [('entity.phantom.flap', 0.6, 1.4), ('item.trident.throw', 0.5, 1.6)]),
    'orbs_gather':  ('Q6 110: the orbs gather.', [('block.beacon.power_select', 0.6, 0.8), ('block.amethyst_block.resonate', 0.6, 0.6)]),
    'orbs_toss':    ('Q6 125: the orbs fly to the rim.', [('entity.blaze.shoot', 0.6, 1.2), ('entity.phantom.swoop', 0.4, 1.6)]),
    'orb_burst':    ('Q6 the orbs explode.', [('entity.generic.explode', 0.9, 0.9), ('entity.wither.shoot', 0.4, 0.8)]),
    'fall_dive':    ('Q0 the opening fall.', [('entity.phantom.swoop', 0.9, 0.7), ('item.trident.riptide_3', 0.6, 0.9)]),
    'fall_impact':  ('Q0 impact + blade eruption.', [('entity.generic.explode', 1.0, 0.8), ('block.pointed_dripstone.fall', 0.8, 0.6)]),
    'rear_whip':    ('Q3 she whips around.', [('entity.player.attack.sweep', 1.0, 0.7), ('entity.phantom.flap', 0.5, 1.0)]),
    'crescent_throw': ('Q1 / Q3 thrown crescents.', [('item.trident.throw', 0.9, 0.9), ('item.firecharge.use', 0.5, 1.2)]),
    'moon':         ('Q6 30: the red moon flares.', [('block.beacon.power_select', 0.7, 0.6), ('entity.wither.ambient', 0.25, 1.4)]),
}
assert tuple(SOUNDS) == tuple(api.KIT_SOUNDS), set(SOUNDS) ^ set(api.KIT_SOUNDS)
DEATH_SOUNDS = ('death_lower', 'death_flames', 'death_gone')
VOICE_EVENTS = ('entity.warden.ambient', 'entity.ravager.ambient', 'entity.wither.death', 'entity.ender_dragon.death')


def sound_line(event, vol, pitch):
    return L.sound(event, vol, pitch)


# ----------------------------------------------------------------------------- presets (api.KIT_PRESETS)
# name -> (doc, args, fn, conv, ambient, split_c, pre). A preset with arguments is a public macro p/<name> that turns its
# arguments into storage rlk:kn fx.pa (conv: [(key, src, scale or None (int x 1), add, frac)], src = a macro arg or a
# '#score' of knFx) and runs p/e/<name>[_<c>] with that storage; pre = lines run before the conv (floor clamps).
PRESETS = {}
AMBIENT = ('ambient_petals', 'gate_flames')
PTCL = ('ambient_petals',)
PA = f'{STO} fx.pa'


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


def fly(kind, yaw, el, dist, h=0.0, s0=0.5, s1=1.0, life=8, fade=3, col=WHITE, dly=0, roll=0, dur=0, pos=None):
    """the fg radial trick: a fixed face card whose local +y points out along (yaw, elevation) flies dist outward. The
    card's pitch is 90 - el and the game clamps an entity's pitch to [-90, 90] when fx/e/spawn teleports it, so el < 0
    (below the horizon) would fly level in game: el must be 0..90."""
    assert 0 <= el <= 90, (kind, el)
    return card(kind, pos or f'~ ~{num(h, 2)} ~', f'~{ang(yaw)} {ang(90 - el)}', roll=roll, s0=s0, s1=s1,
                move=(0, dist if isinstance(dist, str) else round(dist, 2), 0), life=life, fade=fade, col=col, dly=dly,
                dur=dur)


def inward(kind, yaw, r, h, dist, s0=0.5, s1=0.3, life=10, fade=3, col=WHITE, dly=0, dur=0):
    """a fixed face card at radius r (bearing yaw, height h) flying dist toward the centre"""
    x, z = xz(r, yaw)
    return card(kind, f'^{num(x, 3)} ^{num(h, 2)} ^{num(z, 3)}', f'~{ang(yaw + 180)} 90', s0=s0, s1=s1,
                move=(0, round(dist, 2), 0), life=life, fade=fade, col=col, dly=dly, dur=dur)


def mac(line):
    return '$' + line


RND = random.Random

# --- the floor clamp of vertical / tilted cards ----------------------------------------------------------------------
# fx/e/hgt: #h = the executor's height over the floor (hundredths; storage fx.fl = floor y x 100, the arena's by default).
# Slash arcs: LOW[ip * 36 + ir] = the lowest point of the arc (bearings +-80 deg from the aim, unit radius) below the
# pivot, per mille, for the pitch cell ip (centre -90 + 10 ip) and roll cell ir (centre -180 + 10 ir), the max over the
# cell; the reach is clamped to 100 (h - 10) / LOW (tenths) so no arc reaches below the floor.
ARC_BEAR = 80.0
ARC_LIFT = 100                         # hundredths: a low arc rises up to 1 b before it shrinks


def arc_low(p, ro):
    pr, rr = math.radians(p), math.radians(ro)
    A = math.sin(rr) * math.cos(pr)            # the y component of the card's a axis (rolled about the aim)
    B = -math.sin(pr)                          # the aim's y component (pitch down = positive)
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

ARC_CLAMP = [
    '$scoreboard players set #r knFx $(r)', '$scoreboard players set #p knFx $(pitch)',
    '$scoreboard players set #o knFx $(roll)', f'function {FN}e/clamp_arc']


def _c_conv(*pairs):
    return tuple(pairs)


# --- blade arcs and rings --------------------------------------------------------------------------------------------
ARC_LIFE = (2, 2, 2, 8)


@preset('slash_arc', 'A slash arc of reach {r} (tenths) about the executor (S3: the body + 1.4 / 1.8, rotated as the body; '
        'S2: the blade anchor): {yaw} / {pitch} offsets of the aim from the executor rotation, {roll} the blade plane about '
        'the aim (0 horizontal, 90 vertical, 180 backhand: the sweep reversed). Four sweep frames 1 tick apart (the last '
        'fades over 8 t), c 1 orange-gold flame / c 2 crimson with black smoke; particles at the arc front. An arc that '
        'would reach below the floor rises up to 1 b, then shrinks (fx/e/clamp_arc): no frame goes below the floor.',
        conv=(('s', '#r', 0.1), ('s9', '#r', 0.09), ('f', '#r', 0.08), ('pd', '#r', 0.025), ('ly', '#ly', 0.01)), split_c=True,
        pre=ARC_CLAMP)
def _p_slash_arc(c):
    out = []
    for k in range(4):
        out.append(mac(card(f'{ARCK[c]}{k}', '^ ^$(ly) ^', '~$(yaw) ~$(pitch)', roll='$(roll)', s0=('$(s9)', 1, '$(s9)'),
                            s1=('$(s)', 1, '$(s)'), life=ARC_LIFE[k], fade=4 if k == 3 else 0, dly=k, dur=2,
                            hit=k + 3 if k == 3 else -1, col2=(FADE_P if c == C_PY else FADE_C) if k == 3 else -1)))
    front = 'positioned ^ ^$(ly) ^ rotated ~$(yaw) ~$(pitch) positioned ^ ^ ^$(f)'
    out += [mac(f'execute {front} run ' + l) for l in c_parts(c, '~ ~ ~', ('$(pd)', 0.25, '$(pd)'), 14)]
    if c == C_PY:
        out.append(mac(f'execute {front} run ' + part('lava', '~ ~ ~', (0.3, 0.2, 0.3), 0, 1)))
    else:
        out.append(mac(f'execute {front} run ' + part('crimson_spore', '~ ~ ~', ('$(pd)', 0.3, '$(pd)'), 0, 10)))
    return out


@preset('spin_ring', 'A full ring of flame of radius {r} (tenths) about the executor (S3: the body + 1.0; S2: her feet, '
        'the intro floor ring), lifted 0.3 b: two counter-turning rings, embers thrown out; c 1 orange-gold, c 2 crimson '
        'with smoke.', conv=(('s', 'r', 0.1), ('s5', 'r', 0.05), ('s9', 'r', 0.09), ('pd', 'r', 0.06)), split_c=True)
def _p_spin_ring(c):
    out = [mac(card(RINGK[c], '^ ^0.3 ^', '~ 0', spin=170, s0=('$(s5)', 1, '$(s5)'), s1=('$(s)', 1, '$(s)'), life=9,
                    fade=4, dur=5)),
           mac(card(RINGK[c], '^ ^0.5 ^', '~60 0', spin=-150, s0=('$(s5)', 1, '$(s5)'), s1=('$(s9)', 1, '$(s9)'),
                    life=8, fade=4, dly=1, dur=4, col=rgb('#E0C0B0')))]
    for yaw in radial(6, 20):
        out.append(fly('ember', yaw, 15, 2.6, h=0.4, s0=0.25, s1=0.4, life=9, fade=4, col=TINT[c], dly=1))
    out += [mac(l) for l in c_parts(c, '~ ~0.4 ~', ('$(pd)', 0.15, '$(pd)'), 24)]
    return out


TWIRL_CLAMP = [f'function {FN}e/hgt', 'scoreboard players set #r knFx 13', 'scoreboard players operation #m knFx = #h knFx',
               'scoreboard players remove #m knFx 12', 'scoreboard players operation #m knFx /= #c10 knFx',
               'scoreboard players operation #r knFx < #m knFx',
               'execute if score #r knFx matches ..3 run scoreboard players set #r knFx 4']


@preset('twirl_ring', 'Intro E6 (S2: at the hand anchor, rotated as the body): the crimson crescent trail closing into a '
        'full ring in the frontal plane (radius 1.3 b, less when the hand is low: the ring never reaches the floor), an '
        'orange inner ring, crimson sparks.', conv=(('s', '#r', 0.1), ('s3', '#r', 0.03)), pre=TWIRL_CLAMP)
def _p_twirl_ring():
    return [mac(card('ring_c', '^ ^ ^', '~ 90', spin=170, s0=('$(s3)', 1, '$(s3)'), s1=('$(s)', 1, '$(s)'), life=12,
                     fade=5, dur=6)),
            mac(card('ring_p', '^ ^ ^0.05', '~ 90', spin=-160, s0=('$(s3)', 1, '$(s3)'), s1=('$(s)', 1, '$(s)'), life=9,
                     fade=4, dly=2, dur=5, col=rgb('#FFD0A0'))),
            dust(DUSTC[C_BOL], 1.2, '^ ^ ^', (0.6, 0.6, 0.2), 16), part('crimson_spore', '^ ^ ^', (0.5, 0.5, 0.2), 0, 10)]


# --- the scythe forming, embers --------------------------------------------------------------------------------------
@preset('scythe_form', 'The crimson flame vortex where a scythe forms (S2 intro E3 / T twin scythes, S3 B wheel spin: at the '
        'palm / hand anchor or the body + 1.4): six crimson flame tongues stream in to the point, a glow, crimson '
        'sparks and smoke.')
def _p_scythe_form():
    out = [inward('flame', yaw, 0.9, 0.1 * ((k % 3) - 1), 0.8, s0=0.7, s1=0.3, life=10, fade=3, col=CRIM, dly=k % 2, dur=6)
           for k, yaw in enumerate(radial(6, 15))]
    out += [card('glow', '~ ~ ~', bb='center', s0=0.3, s1=1.2, life=12, fade=5, col=CRIM),
            card('burst', '~ ~ ~', bb='center', spin=90, s0=0.2, s1=0.9, life=8, fade=4, dly=4, col=ROSE),
            dust(DUSTC[C_BOL], 1.2, '~ ~ ~', (0.4, 0.4, 0.4), 14), part('large_smoke', '~ ~ ~', (0.3, 0.3, 0.3), 0.01, 4),
            part('crimson_spore', '~ ~ ~', (0.5, 0.5, 0.5), 0, 12)]
    return out


@preset('embers_puff', 'A small puff of red-orange embers at the executor (anchors, the body + 1.4: the cup to embers, the '
        'reach, the stance, her heal): six embers flung out, a soft glow, ash.')
def _p_embers_puff():
    rnd = RND(11)
    out = [fly('ember', yaw, rnd.uniform(20, 70), rnd.uniform(0.7, 1.3), s0=0.28, s1=0.45, life=10, fade=4,
               col=(EMBER if k % 2 else CRIM)) for k, yaw in enumerate(radial(6, 25))]
    out += [card('glow', '~ ~ ~', bb='center', s0=0.4, s1=1.2, life=6, fade=3, col=EMBER),
            dust((1.0, 0.35, 0.12), 0.8, '~ ~ ~', (0.25, 0.25, 0.25), 8), part('small_flame', '~ ~ ~', (0.2, 0.2, 0.2), 0.02, 4),
            part('ash', '~ ~ ~', (0.3, 0.3, 0.3), 0, 6)]
    return out


# --- trails and streaks ----------------------------------------------------------------------------------------------
WHEEL_SPEED = 1.5                       # b / t of the flown wheel (pj/launch rounds 1.4 up to 1.5)


@preset('wheel_trail', 'The fire trail the thrown wheel leaves on the ground (B release: the body at the floor, rotated as '
        'the body): eight flame tongues along the aim over {len} (tenths), each lit as the wheel passes it (1.5 b / t), '
        'burning out over 18 t (vertical cards standing on the floor, no floor decal).',
        conv=tuple((f'p{k}', 'len', 0.1 * k / 8) for k in range(1, 9)) +
        tuple((f'd{k}', 'len', None, 0, k / (8 * 10 * WHEEL_SPEED)) for k in range(1, 9)))
def _p_wheel_trail():
    out = []
    for k in range(1, 9):
        out.append(mac(card('flame', f'^{num(0.25 * (-1) ** k, 2)} ^ ^$(p{k})', bb='vertical', s0=(0.5, 0.2, 0.5),
                            s1=(0.9, 1.1 + 0.1 * (k % 3), 0.9), life=18, fade=8, dly=f'$(d{k})', dur=4, col=PYRO)))
    out += [part('flame', '^ ^0.3 ^1', (0.3, 0.1, 0.3), 0.02, 8), part('lava', '^ ^0.2 ^1', (0.3, 0.1, 0.3), 0, 2)]
    return out


TRAIL_CONV = (('l', 'len', 0.1), ('h', 'len', 0.05), ('p1', 'len', 0.025), ('p2', 'len', 0.05), ('p3', 'len', 0.075),
              ('p4', 'len', 0.1))


@preset('dash_trail', 'The streak of a dash along the aim over {len} (tenths) from the executor (S3: the body + 1.0, rotated '
        'as the body): a wide outer streak and a white-hot inner one at hip height, four flame tongues revealed in turn '
        'at the feet, colour particles; c 1 orange-gold, c 2 crimson.', conv=TRAIL_CONV, split_c=True)
def _p_dash_trail(c):
    out = [mac(card('streak', '^ ^-0.4 ^', '~ 0', s0=(0.5, 0.5, '$(l)'), s1=(1.4, 1.4, '$(l)'), life=9, fade=5, dur=2,
                    col=DEEP[c] if c == C_BOL else TINT[c])),
           mac(card('streak', '^ ^-0.35 ^', '~ 0', s0=(0.3, 0.3, '$(l)'), s1=(0.6, 0.6, '$(l)'), life=7, fade=4, dur=2,
                    col=PYRO_GOLD if c == C_PY else ROSE))]
    for k in range(1, 5):
        out.append(mac(card('flame', f'^ ^-0.98 ^$(p{k})', bb='vertical', s0=(0.5, 0.3, 0.5), s1=(0.9, 1.3, 0.9), life=10,
                            fade=5, dly=k - 1, dur=4, col=TINT[c])))
        out += [mac(l) for l in c_parts(c, f'^ ^-0.6 ^$(p{k})', (0.25, 0.2, 0.25), 5)]
    return out


@preset('leap_flare', 'The take-off flare (C / E leaps, T launch: the body + 0.3 / + 1.4): a flaming ring bursting out, a '
        'flash, embers rising.')
def _p_leap_flare():
    out = [card('ring_p', '^ ^ ^', '~ 0', spin=120, s0=(0.4, 1, 0.4), s1=(2.4, 1, 2.4), life=8, fade=4, dur=4),
           card('burst', '~ ~0.4 ~', bb='center', spin=60, s0=0.5, s1=2.0, life=5, fade=3, col=PYRO)]
    out += [fly('ember', yaw, 70, 1.8, s0=0.2, s1=0.35, life=10, fade=4, col=EMBER, dly=1) for yaw in radial(5, 10)]
    out += [part('flame', '~ ~ ~', (0.5, 0.1, 0.5), 0.06, 16), part('lava', '~ ~ ~', (0.4, 0.1, 0.4), 0, 2)]
    return out


DIVE_CLAMP = [f'function {FN}e/hgt', '$scoreboard players set #r knFx $(len)', 'scoreboard players operation #m knFx = #h knFx',
              'scoreboard players remove #m knFx 45', 'scoreboard players operation #m knFx *= #c10 knFx',
              'scoreboard players operation #m knFx /= #c77 knFx', 'scoreboard players operation #r knFx < #m knFx',
              'execute if score #r knFx matches ..4 run scoreboard players set #r knFx 5']


@preset('dive_streak', 'The dive streak (C / E dives, Q0 fall: the body + 1, rotated as the body): a streak from the '
        'executor down-forward (50 deg) over {len} (tenths), clamped to end above the floor: a crimson outer streak and '
        'an orange-gold core, sparks at the executor.', conv=(('l', '#r', 0.1),), pre=DIVE_CLAMP)
def _p_dive_streak():
    return [mac(card('streak', '^ ^ ^', '~ 50', s0=(0.6, 0.6, '$(l)'), s1=(1.3, 1.3, '$(l)'), life=8, fade=4, dur=2,
                     col=CRIM)),
            mac(card('streak', '^ ^ ^', '~ 50', s0=(0.3, 0.3, '$(l)'), s1=(0.55, 0.55, '$(l)'), life=6, fade=3, dur=2,
                     col=PYRO_GOLD)),
            part('flame', '~ ~ ~', (0.3, 0.3, 0.3), 0.05, 10), dust(DUSTC[C_BOL], 1.2, '~ ~ ~', (0.4, 0.4, 0.4), 10)]


@preset('impact_burst', 'A blade landing (S3: the floor point + 0.2, the lock marker): a shock ring of radius {r} (tenths) at '
        '0.3 b, a flash, embers low; c 2 adds crimson thorn shards and smoke.',
        conv=(('s', 'r', 0.1), ('s3', 'r', 0.03), ('sb', 'r', 0.09), ('pd', 'r', 0.035), ('t1', 'r', 0.04)), split_c=True)
def _p_impact_burst(c):
    out = [mac(card(RINGK[c], '^ ^0.3 ^', '~ 0', spin=90, s0=('$(s3)', 1, '$(s3)'), s1=('$(s)', 1, '$(s)'), life=8,
                    fade=4, dur=4)),
           mac(card('burst', '~ ~0.8 ~', bb='center', spin=45, s0=0.5, s1='$(sb)', life=5, fade=3, col=TINT[c]))]
    out += [fly('ember', yaw, 20, 2.0, h=0.4, s0=0.22, s1=0.35, life=8, fade=4, col=TINT[c]) for yaw in radial(6, 0)]
    if c == C_BOL:
        for k, yaw in enumerate(radial(4, 45)):
            x, z = xz(1.0, yaw)
            out.append(mac(card('thorn', f'^{num(x, 2)} ^ ^{num(z, 2)}', bb='vertical', s0=(0.6, 0.05, 0.6),
                                s1=(0.9, '$(t1)', 0.9), life=9, fade=4, dly=k % 2, dur=2)))
    out += [mac(l) for l in c_parts(c, '~ ~0.4 ~', ('$(pd)', 0.2, '$(pd)'), 20)]
    out.append(part('explosion', '~ ~0.4 ~', (0, 0, 0), 0, 1))
    return out


@preset('claw', 'B2 grab (S3: the lock + 1 at pt 92, the hit at 96): the crimson claw closing over 4 t to the reach {r} '
        '(tenths), white-hot at the close, then a crimson burst.', conv=(('s', 'r', 0.2), ('s0', 'r', 0.27), ('sb', 'r', 0.16)))
def _p_claw():
    return [mac(card('claw', '~ ~ ~', bb='center', spin=-40, s0='$(s0)', s1='$(s)', life=9, fade=3, dur=4, hit=4,
                     col=rgb('#E0A0A8'), col2=WHITE)),
            mac(card('burst', '~ ~ ~', bb='center', s0=0.5, s1='$(sb)', life=5, fade=3, dly=4, col=CRIM)),
            dust(DUSTC[C_BOL], 1.4, '~ ~ ~', (1.0, 0.8, 1.0), 24), part('crimson_spore', '~ ~ ~', (1.0, 0.8, 1.0), 0, 12)]


@preset('wing_burst', 'The crimson wings burst open (C2 / H / E70 / F: the body + 1.4, rotated as the body): crimson '
        'feathers flung back and out, black smoke, crimson dust.')
def _p_wing_burst():
    rnd = RND(23)
    out = [fly('feather', 180 + rnd.uniform(-70, 70), rnd.uniform(10, 50), rnd.uniform(1.4, 2.4), h=0.2, s0=0.5,
               s1=0.9, life=14, fade=6, roll=rnd.randint(-60, 60)) for _ in range(8)]
    out += [fly('smoke', 180 + yaw, 25, 1.2, s0=0.6, s1=1.4, life=12, fade=6) for yaw in (-50, 0, 50)]
    out += [dust(DUSTC[C_BOL], 1.5, '^ ^ ^-0.4', (1.2, 0.9, 1.2), 30), part('large_smoke', '^ ^ ^-0.4', (0.8, 0.6, 0.8), 0.02, 10)]
    return out


@preset('zig_streak', 'An E lateral dash (S3: the body + 1.2, rotated as the body, at each dash): a red-orange streak of '
        '{len} (tenths) across her, centred on her (the dash goes either way), sparks at both ends.',
        conv=(('l', 'len', 0.1), ('hm', 'len', -0.05), ('h', 'len', 0.05)))
def _p_zig_streak():
    return [mac(card('streak', '^ ^ ^', '~90 0', s0=(0.4, 0.4, '$(l)'), s1=(1.1, 1.1, '$(l)'), off=(0, 0, '$(hm)'),
                     life=8, fade=4, dur=2, col=CRIM)),
            mac(card('streak', '^ ^ ^', '~90 0', s0=(0.2, 0.2, '$(l)'), s1=(0.45, 0.45, '$(l)'), off=(0, 0, '$(hm)'),
                     life=6, fade=3, dur=2, col=PYRO_GOLD)),
            mac(dust(DUSTC[C_BOL], 1.2, '^$(h) ^ ^', (0.2, 0.3, 0.2), 6)), mac(dust(DUSTC[C_BOL], 1.2, '^$(hm) ^ ^', (0.2, 0.3, 0.2), 6)),
            part('flame', '~ ~ ~', (0.3, 0.3, 0.3), 0.03, 6)]


# --- the forced bond, threads, thorns, blast -------------------------------------------------------------------------
@preset('brand_ring', 'The crimson sigil closing on the player (F / Q5 pt 6 -> brand 22: at the player\'s feet): two sigil '
        'rings at 0.5 b and 1.3 b (on the player, not a floor marking) contract from r 3.2 to 0.5 over 16 t, turning, '
        'white-hot at the close.')
def _p_brand_ring():
    return [card('brand', '~ ~1.3 ~', '0 0', spin=160, s0=(3.2, 1, 3.2), s1=(0.5, 1, 0.5), life=18, fade=2, dur=16, hit=15,
                 col=rgb('#E0A0A8'), col2=WHITE),
            card('brand', '~ ~0.5 ~', '45 0', spin=-160, s0=(3.0, 1, 3.0), s1=(0.6, 1, 0.6), life=18, fade=2, dly=1,
                 dur=15, hit=15, col=rgb('#C08088'), col2=WHITE),
            dust(DUSTC[C_BOL], 1.2, '~ ~0.9 ~', (1.4, 0.4, 1.4), 20)]


@preset('brand_x', 'The forced bond lands (bond/force: the player + 1): a red X branded on the player (two strokes), a red '
        'flash, crimson sparks.')
def _p_brand_x():
    return [card('stroke', '~ ~ ~', bb='center', roll=45, s0=(1.2, 0.4, 1.2), s1=(2.4, 2.2, 2.4), life=16, fade=6, dur=3,
                 col=WHITE),
            card('stroke', '~ ~ ~', bb='center', roll=-45, s0=(1.2, 0.4, 1.2), s1=(2.4, 2.2, 2.4), life=16, fade=6, dly=2,
                 dur=3, col=WHITE),
            card('glow', '~ ~ ~', bb='center', s0=0.8, s1=2.6, life=8, fade=4, col=CRIM),
            flash((1.0, 0.12, 0.18), '~ ~0.6 ~', 1.0), dust(DUSTC[C_BOL], 1.5, '~ ~ ~', (0.5, 0.7, 0.5), 24),
            part('crimson_spore', '~ ~ ~', (0.6, 0.8, 0.6), 0, 16)]


_TH = random.Random(47)
THREAD_PTS = [(_TH.uniform(0, 360), math.sqrt(_TH.uniform(0.02, 1.0))) for _ in range(14)]
THORN_PTS = [(_TH.uniform(0, 360), math.sqrt(_TH.uniform(0.01, 1.0)), _TH.uniform(1.6, 2.6)) for _ in range(16)]
THREAD_H = 12.0


@preset('threads', 'Crimson threads from the sky (F hit 1: the arena centre + 0.2, r = the walk; H leap: the body + 3, r 10): '
        'up to 14 threads (0.6 b wide cards) at fixed points inside radius {r} (tenths; 4 below r 60), drawn down from 12 b to the '
        'executor\'s height in 3 t (vertical cards, never below the executor), fading after 14 t.',
        conv=tuple((f'd{k}', 'r', 0.1 * f) for k, (_y, f) in enumerate(THREAD_PTS)) + (('pd', 'r', 0.04),),
        pre=['$scoreboard players set #r knFx $(r)'])
def _p_threads():
    out = []
    for k, (yaw, _f) in enumerate(THREAD_PTS):
        c = card('thread', f'^ ^ ^$(d{k})', '~ 0', bb='vertical', s0=(5.0, 0.2, 5.0), s1=(5.0, THREAD_H, 5.0),
                 off=(0, THREAD_H, 0), move=(0, -THREAD_H, 0), life=14, fade=5, dly=k % 4, dur=3)
        line = f'execute rotated ~{ang(yaw)} 0 run {c}'
        if k >= 4:
            line = f'execute if score #r knFx matches 60.. rotated ~{ang(yaw)} 0 run {c}'
        out.append(mac(line))
    out += [mac(dust(DUSTC[C_BOL], 1.3, '~ ~1 ~', ('$(pd)', 1.0, '$(pd)'), 40)),
            mac(part('crimson_spore', '~ ~2 ~', ('$(pd)', 1.5, '$(pd)'), 0, 30))]
    return out


@preset('thorns', 'Crimson thorns erupting from the floor (F hit 1, G field: the arena centre on the floor, r = the walk): up '
        'to 16 thorns at fixed points inside radius {r} (tenths; 6 below r 60), rising 2.3-3.8 b in 2 t from the floor '
        '(vertical cards standing on it), crimson chips and smoke.',
        conv=tuple((f'd{k}', 'r', 0.1 * f) for k, (_y, f, _h) in enumerate(THORN_PTS)) + (('pd', 'r', 0.035),),
        pre=['$scoreboard players set #r knFx $(r)'])
def _p_thorns():
    out = []
    for k, (yaw, _f, h) in enumerate(THORN_PTS):
        c = card('thorn', f'^ ^ ^$(d{k})', '~ 0', bb='vertical', s0=(1.2, 0.05, 1.2), s1=(1.8, round(1.45 * h, 2), 1.8),
                 life=12, fade=5, dly=k % 3, dur=2)
        line = f'execute rotated ~{ang(yaw)} 0 run {c}'
        if k >= 6:
            line = f'execute if score #r knFx matches 60.. rotated ~{ang(yaw)} 0 run {c}'
        out.append(mac(line))
    out += [mac(blockp('redstone_block', '~ ~0.3 ~', ('$(pd)', 0.2, '$(pd)'), 0, 60)),
            mac(part('large_smoke', '~ ~0.6 ~', ('$(pd)', 0.3, '$(pd)'), 0.02, 20))]
    return out


@preset('blast', 'F hit 2 / G field (the arena centre on the floor, r = the walk): a crimson blast over radius {r} (tenths): '
        'a huge glow, a shock ring at 0.6 b to the full radius, smoke thrown out, explosions across the floor.',
        conv=(('s', 'r', 0.1), ('s2', 'r', 0.02), ('pd', 'r', 0.04), ('gs', 'r', 0.035)))
def _p_blast():
    out = [mac(card('ring_c', '^ ^0.6 ^', '~ 0', spin=60, s0=('$(s2)', 1, '$(s2)'), s1=('$(s)', 1, '$(s)'), life=10, fade=5,
                    dur=6)),
           mac(card('glow', '~ ~2 ~', bb='center', s0=2.0, s1='$(gs)', life=8, fade=5, col=CRIM)),
           card('burst', '~ ~2 ~', bb='center', spin=60, s0=1.0, s1=6.0, life=6, fade=3, col=ROSE)]
    out += [fly('smoke', yaw, 20, 4.0, h=0.8, s0=1.0, s1=2.4, life=14, fade=6) for yaw in radial(6, 30)]
    out += [mac(part('explosion', '~ ~0.5 ~', ('$(pd)', 0.3, '$(pd)'), 0, 8)),
            mac(dust(DUSTC[C_BOL], 1.8, '~ ~0.8 ~', ('$(pd)', 0.6, '$(pd)'), 80)),
            mac(part('large_smoke', '~ ~1 ~', ('$(pd)', 0.6, '$(pd)'), 0.03, 30)), flash((1.0, 0.2, 0.25), '~ ~2 ~', 1.0)]
    return out


@preset('web', 'H perch (S3: the body + 0.5, perched 7 b up): the crimson web spreads under her (4 b), turning slowly, for '
        '56 t.')
def _p_web():
    return [card('web', '^ ^ ^', '~ 0', spin=25, s0=(0.5, 1, 0.5), s1=(3.8, 1, 3.8), life=62, fade=6, dur=4),
            dust(DUSTC[C_BOL], 1.2, '~ ~ ~', (1.5, 0.1, 1.5), 20)]


@preset('clone_trail', 'A clone\'s afterimage (at / rotated as a clone prop: its facing is its flight): a crimson streak '
        'behind it, smoke, crimson dust.')
def _p_clone_trail():
    return [card('streak', '^ ^1.2 ^', '~180 0', s0=(0.6, 0.6, 2.2), s1=(1.2, 1.2, 2.6), life=7, fade=4, col=CRIM),
            fly('smoke', 180, 10, 0.8, h=1.0, s0=0.6, s1=1.2, life=10, fade=5),
            dust(DUSTC[C_BOL], 1.3, '~ ~1.2 ~', (0.4, 0.6, 0.4), 12)]


@preset('blade_rise', 'G a giant blade rises (at each blade prop, on the floor): a crimson glow at its base, crimson chips '
        'and two small thorns beside it.')
def _p_blade_rise():
    return [card('glow', '~ ~0.4 ~', bb='center', s0=0.5, s1=1.8, life=8, fade=4, col=CRIM),
            card('thorn', '^0.5 ^ ^0.2', bb='vertical', s0=(0.5, 0.05, 0.5), s1=(0.7, 0.9, 0.7), life=10, fade=4, dur=2),
            card('thorn', '^-0.45 ^ ^-0.25', bb='vertical', s0=(0.5, 0.05, 0.5), s1=(0.6, 0.7, 0.6), life=10, fade=4, dly=1,
                 dur=2),
            blockp('redstone_block', '~ ~0.3 ~', (0.4, 0.2, 0.4), 0, 16), dust(DUSTC[C_BOL], 1.3, '~ ~0.5 ~', (0.4, 0.5, 0.4), 12),
            part('large_smoke', '~ ~0.4 ~', (0.3, 0.2, 0.3), 0.01, 4)]


@preset('blade_burst', 'G the blades strike (at each blade prop + 1): crimson shards flung out, a flash, smoke.')
def _p_blade_burst():
    rnd = RND(29)
    out = [fly('stroke', yaw, rnd.uniform(10, 60), rnd.uniform(1.2, 2.2), s0=(0.6, 0.6, 0.6), s1=(0.9, 0.9, 0.9), life=9,
               fade=4) for yaw in radial(5, 20)]
    out += [card('burst', '~ ~ ~', bb='center', spin=60, s0=0.6, s1=2.4, life=5, fade=3, col=CRIM),
            dust(DUSTC[C_BOL], 1.5, '~ ~ ~', (0.5, 1.0, 0.5), 20), part('large_smoke', '~ ~ ~', (0.4, 0.6, 0.4), 0.02, 6)]
    return out



@preset('cross_thorns', 'G a cross line erupts, one thorn per call (at its floor point on the line, the module calls 12 a '
        'tick along the four arms, each only on the walk disc): a crimson thorn rising to {h} (tenths) in 2 t from the tick '
        'after the call, crimson chips and dust.', conv=(('hh', 'h', 0.1),))
def _p_cross_thorns():
    return [mac(card('thorn', '^ ^ ^', '~ 0', bb='vertical', s0=(0.9, 0.05, 0.9), s1=(1.3, '$(hh)', 1.3), life=12, fade=5,
                     dur=2)),
            blockp('redstone_block', '^ ^0.3 ^', (0.35, 0.2, 0.35), 0, 4),
            dust(DUSTC[C_BOL], 1.4, '^ ^0.7 ^', (0.3, 0.5, 0.3), 3)]


# --- 선혈의 충격, the break, the stun ----------------------------------------------------------------------------------
@preset('shock_gain', '선혈의 충격 armed (bond/cleared: the player + 1): crimson and gold embers spiral up around the player, '
        'a crimson glow pulse, sparkles.')
def _p_shock_gain():
    out = [fly('ember', yaw, 78, 1.8, h=-0.6 + 0.2 * k, s0=0.2, s1=0.35, life=14, fade=5,
               col=(CRIM if k % 2 else PYRO_GOLD), dly=k) for k, yaw in enumerate(radial(6, 0))]
    out += [card('glow', '~ ~ ~', bb='center', s0=0.6, s1=2.2, life=10, fade=5, col=CRIM),
            dust(DUSTC[C_BOL], 1.2, '~ ~ ~', (0.5, 0.8, 0.5), 16), part('end_rod', '~ ~ ~', (0.4, 0.7, 0.4), 0.02, 4)]
    return out


@preset('shock_aura', 'The crimson glow on her palm (B2 reach: at the hand anchor): a pulsing crimson glow for 20 t, crimson '
        'dust.')
def _p_shock_aura():
    return [card('glow', '~ ~ ~', bb='center', s0=0.3, s1=0.9, life=20, fade=6, dur=8, col=CRIM),
            card('burst', '~ ~ ~', bb='center', spin=120, s0=0.2, s1=0.6, life=12, fade=4, dly=6, col=ROSE),
            dust(DUSTC[C_BOL], 1.0, '~ ~ ~', (0.2, 0.2, 0.2), 10)]


@preset('shock_hit', '선혈의 충격 outside a break window (bond/burst: the body + 1.4): a crimson burst, a ring, sparks.')
def _p_shock_hit():
    out = [card('burst', '~ ~ ~', bb='center', spin=60, s0=0.5, s1=3.2, life=6, fade=3, col=CRIM),
           card('ring_c', '^ ^ ^', '~ 0', spin=90, s0=(0.3, 1, 0.3), s1=(2.8, 1, 2.8), life=8, fade=4, dur=4)]
    out += [fly('ember', yaw, 15, 2.0, s0=0.2, s1=0.35, life=8, fade=4, col=CRIM) for yaw in radial(6, 15)]
    out += [dust(DUSTC[C_BOL], 1.5, '~ ~ ~', (0.6, 0.6, 0.6), 30), part('crit', '~ ~ ~', (0.5, 0.5, 0.5), 0.4, 10),
            part('explosion', '~ ~ ~', (0, 0, 0), 0, 1)]
    return out


@preset('break_burst', 'The Banquet broken (core/break: the body + 1.4): a big crimson shatter: burst, two rings, crimson '
        'shards flung out like glass, smoke, a flash.')
def _p_break_burst():
    rnd = RND(37)
    out = [card('burst', '~ ~ ~', bb='center', spin=60, s0=0.6, s1=5.0, life=7, fade=3, col=CRIM),
           card('ring_c', '^ ^ ^', '~ 0', spin=90, s0=(0.4, 1, 0.4), s1=(4.2, 1, 4.2), life=9, fade=4, dur=5),
           card('ring_c', '^ ^ ^', '~ 90', spin=-90, s0=(0.4, 1, 0.4), s1=(3.4, 1, 3.4), life=8, fade=4, dly=1, dur=4)]
    out += [fly('stroke', yaw, max(0.0, rnd.uniform(-20, 60)), rnd.uniform(2.0, 3.4), s0=(0.5, 0.5, 0.5), s1=(0.8, 0.8, 0.8), life=14,
                fade=6, roll=rnd.randint(-80, 80)) for yaw in radial(10, 7)]
    out += [fly('smoke', yaw, 30, 1.6, s0=0.8, s1=1.6, life=12, fade=6) for yaw in radial(4, 45)]
    out += [part('explosion', '~ ~ ~', (0.5, 0.5, 0.5), 0, 2), dust(DUSTC[C_BOL], 1.8, '~ ~ ~', (1.2, 1.0, 1.2), 50),
            part('large_smoke', '~ ~ ~', (0.8, 0.6, 0.8), 0.03, 12), flash((1.0, 0.15, 0.2), '~ ~ ~', 1.0),
            blockp('redstone_block', '~ ~ ~', (0.8, 0.8, 0.8), 0, 30)]
    return out


@preset('stun_motes', 'The stun (core/stun_fx every 10 t: the body + 2.9): three small crimson-gold motes circling over her '
        'head for one call (11 t), at a random start angle, little crits.')
def _p_stun_motes():
    return [f'execute store result storage {PA}.y int 1 run random value 0..119']   # body continues in p/e (see writer)


STUN_BODY = [mac(card('mote', f'^{num(xz(0.45, a)[0], 3)} ^ ^{num(xz(0.45, a)[1], 3)}', bb='center', s0=0.25, s1=0.35,
                      life=11, fade=3, col=(PYRO_GOLD if k == 1 else CRIM)).replace('function', 'execute rotated $(y) 0 run function', 1))
             for k, a in enumerate((0, 120, 240))] + [part('crit', '~ ~ ~', (0.35, 0.1, 0.35), 0.05, 3)]


# --- transition, legs, moon, beams -----------------------------------------------------------------------------------
@preset('pillar', 'The crimson flame column of T (S2: her feet; pillar 24 r 12, swap 90 r 16): two crossed column cards of '
        'radius {r} (tenths), 6 b tall, rising from her feet over 10 t, burning 66 t; crimson flame dust, smoke at the top.',
        conv=(('w', 'r', 0.8), ('w6', 'r', 0.6), ('pd', 'r', 0.08)))
def _p_pillar():
    return [mac(card('pillar', '^ ^ ^', '~ 0', s0=('$(w6)', 0.4, '$(w6)'), s1=('$(w)', 6.0, '$(w)'), life=66, fade=8, dur=10)),
            mac(card('pillar', '^ ^ ^', '~45 0', s0=('$(w6)', 0.3, '$(w6)'), s1=('$(w)', 5.4, '$(w)'), life=64, fade=8,
                     dly=2, dur=10, col=rgb('#E0B0B8'))),
            card('glow', '~ ~1.4 ~', bb='center', s0=1.0, s1=3.0, life=30, fade=10, dur=10, col=CRIM),
            mac(dust(DUSTC[C_BOL], 1.6, '~ ~2 ~', ('$(pd)', 2.0, '$(pd)'), 40)),
            part('large_smoke', '~ ~6 ~', (0.6, 0.4, 0.6), 0.02, 10), part('crimson_spore', '~ ~3 ~', (0.8, 2.0, 0.8), 0, 20)]



@preset('shroud', 'T the form swap is hidden (S2: her feet, rotated as the body, 8 t before the swap; she hangs 1.3-3 b up, '
        'her forearms up to 1.2 b out): a cocoon of crimson flame veils closes round her in 3 t (4 rings of 10 at r 1.35, '
        '1.1-4.25 b up, facing the viewer, none below the floor) with flame tongues licking up it; the rings burn away one '
        'by one from the bottom (fading 13-29 t after it starts) while she rises out of the top in her new form.')
def _p_shroud():
    rnd = RND(61)
    out = []
    for k, h in enumerate((1.1, 2.15, 3.2, 4.25)):
        for i, yaw in enumerate(radial(10, 18 * (k % 2))):
            x, z = xz(1.35, yaw)
            out.append(card('veil', f'^{num(x, 2)} ^{num(h, 2)} ^{num(z, 2)}', bb='center', roll=rnd.randint(0, 359),
                            spin=rnd.choice((-20, 20)), s0=0.5, s1=round(rnd.uniform(1.8, 2.1), 2), life=20 + 3 * k,
                            fade=7, col=CRIM if (i + k) % 3 else ROSE, dur=3))
    for yaw in radial(6, 15):
        x, z = xz(1.5, yaw)
        out.append(card('flame', f'^{num(x, 2)} ^0.4 ^{num(z, 2)}', bb='vertical', s0=(0.8, 0.4, 0.8), s1=(1.6, 4.6, 1.6),
                        life=24, fade=8, col=CRIM, dur=5))
    out += [dust(DUSTC[C_BOL], 1.8, '~ ~2.4 ~', (0.7, 1.4, 0.7), 40), part('crimson_spore', '~ ~2.4 ~', (0.9, 1.6, 0.9), 0, 30),
            part('large_smoke', '~ ~4.6 ~', (0.5, 0.3, 0.5), 0.02, 8)]
    return out


@preset('shroud_burst', 'T the swap itself (S2: the chest anchor at the swap tick): a white-hot flash inside the cocoon, a crimson '
        'glow, crimson blade shards flung out all round (as in the footage), a flash.')
def _p_shroud_burst():
    rnd = RND(67)
    out = [card('burst', '~ ~ ~', bb='center', spin=60, s0=2.5, s1=5.0, life=8, fade=4),          # <= 2.5 b down: the
           card('glow', '~ ~ ~', bb='center', s0=3.0, s1=5.5, life=10, fade=6, col=CRIM)]       # chest is ~2.9 b up
    out += [fly('stroke', yaw, rnd.uniform(0, 50), rnd.uniform(3.5, 5.5), s0=(1.0, 1.0, 1.0), s1=(1.6, 1.6, 1.6), life=11,
                fade=4, col=CRIM) for yaw in radial(12, 10)]
    out += [flash((1.0, 0.35, 0.4), '~ ~ ~', 1.0), dust(DUSTC[C_BOL], 2.0, '~ ~ ~', (1.2, 1.2, 1.2), 50),
            part('large_smoke', '~ ~ ~', (0.8, 0.8, 0.8), 0.04, 16)]
    return out

@preset('legs_burst', 'T: a pair of blade legs unfolds (S2: the spine anchor, rotated as the body): crimson feathers and ash '
        'flung out sideways and back, a crimson glow.')
def _p_legs_burst():
    rnd = RND(53)
    out = [fly('feather', side * rnd.uniform(90, 160), rnd.uniform(0, 40), rnd.uniform(1.2, 2.0), s0=0.5, s1=0.8, life=12,
               fade=5, roll=rnd.randint(-40, 40)) for side in (1, -1) for _ in range(3)]
    out += [card('glow', '~ ~ ~', bb='center', s0=0.5, s1=1.6, life=8, fade=4, col=CRIM),
            part('ash', '~ ~ ~', (0.8, 0.5, 0.8), 0, 20), part('white_ash', '~ ~ ~', (0.8, 0.5, 0.8), 0, 10),
            dust(DUSTC[C_BOL], 1.2, '~ ~ ~', (0.6, 0.4, 0.6), 14)]
    return out


@preset('moon_flare', 'The red moon flares (Q6 moon: at the halo / her): the halo swelling and fading over 20 t, a big '
        'crimson glow, crimson dust.')
def _p_moon_flare():
    return [card('halo', '~ ~ ~', bb='center', spin=30, s0=4.0, s1=9.0, life=20, fade=8, dur=12),
            card('glow', '~ ~ ~', bb='center', s0=4.0, s1=10.0, life=14, fade=6, col=CRIM),
            dust(DUSTC[C_BOL], 2.0, '~ ~ ~', (2.5, 2.5, 2.5), 40)]


@preset('aim_line', 'Q4 aim (at the chest anchor, rotated toward the player, pitch counts; call every tick or every 2 t '
        'while it tracks): a thin red line over {len} (tenths), 3 t.', conv=(('l', 'len', 0.1),))
def _p_aim_line():
    return [mac(card('aim', '^ ^ ^', '~ ~', s0=(0.12, 0.12, '$(l)'), s1=(0.12, 0.12, '$(l)'), life=3, fade=0, dur=1))]


@preset('reticle', 'Q4 the reticle growing at her chest (at the chest anchor, rotated toward the player): the red reticle '
        '0.6 b ahead grows over 18 t, turning, white-hot from 20 t (the lock), gone at 26 t.')
def _p_reticle():
    return [card('reticle', '^ ^ ^0.6', bb='center', spin=120, s0=0.3, s1=1.6, life=26, fade=4, dur=18, hit=20,
                 col=rgb('#E0A0A8'), col2=WHITE),
            card('glow', '^ ^ ^0.6', bb='center', s0=0.3, s1=1.0, life=22, fade=6, dur=18, col=CRIM)]


@preset('beam', 'Q4 the beam (at the chest anchor, rotated toward the locked point, pitch counts): a crimson beam over {len} '
        '(tenths) swelling to 2.2 b in 2 t, a white core, a flash at the origin, crimson dust along it; 10 t.',
        conv=(('l', 'len', 0.1), ('h', 'len', 0.05), ('q', 'len', 0.1)))
def _p_beam():
    return [mac(card('beam', '^ ^ ^', '~ ~', s0=(0.6, 0.6, '$(l)'), s1=(2.2, 2.2, '$(l)'), life=10, fade=5, dur=2)),
            mac(card('aim', '^ ^ ^', '~ ~', s0=(0.4, 0.4, '$(l)'), s1=(0.7, 0.7, '$(l)'), life=6, fade=3, dur=2, col=WHITE)),
            card('burst', '^ ^ ^0.4', bb='center', spin=60, s0=0.6, s1=3.0, life=6, fade=3, col=ROSE),
            flash((1.0, 0.25, 0.3), '^ ^ ^0.5', 1.0),
            mac(dust(DUSTC[C_BOL], 1.6, '^ ^ ^$(h)', (0.5, 0.5, 0.5), 20)),
            mac(dust(DUSTC[C_BOL], 1.6, '^ ^ ^$(q)', (0.5, 0.5, 0.5), 12))]


@preset('x_mark', 'Q5B the vertical red X carved in front of her (at her feet, rotated toward the player): two strokes 4.6 b '
        'long crossing 1.6 b ahead, 2.3 b up (never below 0.4 b), the second 12 t after the first, each carved in 10 t; '
        'held 72 t (to the final), white-hot from 64.')
def _p_x_mark():
    out = []
    for k, roll in enumerate((45, -45)):
        out.append(card('stroke', '^ ^2.3 ^1.6', '~ 0', roll=roll, s0=(2.6, 0.2, 2.6), s1=(2.6, 4.6, 2.6), life=72 - 12 * k,
                        fade=6, dly=12 * k, dur=10, hit=64, col=rgb('#E0A8B0'), col2=WHITE))
    out += [card('glow', '^ ^2.3 ^1.6', bb='center', s0=1.0, s1=3.0, life=30, fade=8, dur=20, col=CRIM),
            dust(DUSTC[C_BOL], 1.4, '^ ^2.3 ^1.6', (0.8, 1.2, 0.3), 20)]
    return out


@preset('rapid_slash', 'Q5B one rapid slash (S4: per slash, the body + 1.2): two flat crimson arcs of reach 5.5 b at random '
        'bearings (roll within +-10 deg: they stay above the floor), 3 t each.')
def _p_rapid_slash():
    return [f'execute store result storage {PA}.y int 1 run random value 0..359',
            f'execute store result storage {PA}.y2 int 1 run random value 0..359',
            f'execute store result storage {PA}.ro int 1 run random value -10..10']


RAPID_BODY = [mac(card('arc_c3', '^ ^ ^', '~$(y) 0', roll='$(ro)', s0=(5.0, 1, 5.0), s1=(5.5, 1, 5.5), life=3, fade=2)),
              mac(card('arc_c2', '^ ^0.2 ^', '~$(y2) 0', roll='$(ro)', s0=(4.6, 1, 4.6), s1=(5.2, 1, 5.2), life=3, fade=2)),
              dust(DUSTC[C_BOL], 1.2, '~ ~ ~', (1.5, 0.3, 1.5), 10)]


@preset('final_burst', 'A big crimson flame burst of radius {r} (tenths) at the executor (Q5B final: her feet; death gone: '
        'her feet, r 20): a flash, a shock ring at 0.4 b, crimson flames flung out low, smoke, explosions.',
        conv=(('s', 'r', 0.1), ('s3', 'r', 0.03), ('sb', 'r', 0.12), ('pd', 'r', 0.035)))
def _p_final_burst():
    out = [mac(card('burst', '~ ~1.2 ~', bb='center', spin=60, s0=0.6, s1='$(sb)', life=7, fade=4, col=CRIM)),
           mac(card('ring_c', '^ ^0.4 ^', '~ 0', spin=90, s0=('$(s3)', 1, '$(s3)'), s1=('$(s)', 1, '$(s)'), life=10, fade=5,
                    dur=5))]
    out += [fly('flame', yaw, 15, 1.8, h=0.5, s0=0.6, s1=1.0, life=10, fade=5, col=CRIM) for yaw in radial(8, 10)]
    out += [fly('smoke', yaw, 40, 1.4, h=1.0, s0=0.8, s1=1.6, life=12, fade=6) for yaw in radial(4, 30)]
    out += [part('explosion', '~ ~0.8 ~', (0.4, 0.3, 0.4), 0, 2), mac(dust(DUSTC[C_BOL], 1.8, '~ ~1 ~', ('$(pd)', 0.8, '$(pd)'), 60)),
            part('large_smoke', '~ ~1 ~', (0.6, 0.6, 0.6), 0.03, 20), flash((1.0, 0.2, 0.25), '~ ~1.2 ~', 1.0)]
    return out


@preset('feather_hit', 'Q6 a feather bolt lands (its landing point on the floor): a small crimson ring at 0.3 b, a flash, '
        'three small thorns, crimson chips.')
def _p_feather_hit():
    out = [card('ring_c', '^ ^0.3 ^', '~ 0', spin=90, s0=(0.3, 1, 0.3), s1=(1.6, 1, 1.6), life=7, fade=4, dur=3),
           card('burst', '~ ~0.5 ~', bb='center', s0=0.4, s1=1.4, life=5, fade=3, col=CRIM)]
    for k, yaw in enumerate(radial(3, 20)):
        x, z = xz(0.5, yaw)
        out.append(card('thorn', f'^{num(x, 2)} ^ ^{num(z, 2)}', bb='vertical', s0=(0.4, 0.05, 0.4), s1=(0.5, 0.8, 0.5),
                        life=8, fade=4, dly=k % 2, dur=2))
    out += [blockp('redstone_block', '~ ~0.3 ~', (0.4, 0.1, 0.4), 0, 10), dust(DUSTC[C_BOL], 1.2, '~ ~0.4 ~', (0.5, 0.3, 0.5), 10)]
    return out


@preset('orb_gather', 'Q6 110: eight crimson orbs gather around her (the body): orbs flying in from 4 b to 1.6 b at 1.5 b up, '
        'a crimson glow at her.')
def _p_orb_gather():
    out = [inward('orb', yaw, 4.0, 1.5, 2.4, s0=0.5, s1=0.7, life=16, fade=4, dur=10) for yaw in radial(8, 0)]
    out += [card('glow', '~ ~1.5 ~', bb='center', s0=0.5, s1=2.2, life=16, fade=6, dur=10, col=CRIM),
            dust(DUSTC[C_BOL], 1.3, '~ ~1.5 ~', (1.5, 0.5, 1.5), 24)]
    return out


@preset('orb_burst', 'Q6 an orb explodes (at the orb on the floor): a crimson ring of radius {r} (tenths) at 0.3 b, a glow, '
        'four thorns, smoke.', conv=(('s', 'r', 0.1), ('s3', 'r', 0.03), ('pd', 'r', 0.04), ('t1', 'r', 0.03)))
def _p_orb_burst():
    out = [mac(card('ring_c', '^ ^0.3 ^', '~ 0', spin=90, s0=('$(s3)', 1, '$(s3)'), s1=('$(s)', 1, '$(s)'), life=9, fade=4,
                    dur=4)),
           card('glow', '~ ~0.6 ~', bb='center', s0=0.8, s1=3.0, life=7, fade=4, col=CRIM)]
    for k, yaw in enumerate(radial(4, 0)):
        x, z = xz(1.2, yaw)
        out.append(mac(card('thorn', f'^{num(x, 2)} ^ ^{num(z, 2)}', bb='vertical', s0=(0.6, 0.05, 0.6),
                            s1=(0.9, '$(t1)', 0.9), life=9, fade=4, dly=k % 2, dur=2)))
    out += [part('explosion', '~ ~0.5 ~', (0, 0, 0), 0, 1), mac(dust(DUSTC[C_BOL], 1.5, '~ ~0.5 ~', ('$(pd)', 0.3, '$(pd)'), 30)),
            part('large_smoke', '~ ~0.6 ~', (0.6, 0.3, 0.6), 0.02, 6)]
    return out


DF = random.Random(61)
DEATH_PTS = [(DF.uniform(-0.45, 0.45), 0.2 + 2.3 * k / 9, DF.uniform(-0.3, 0.3)) for k in range(10)]


@preset('death_flames', 'Death 70: crimson flames climb her body (her feet): ten flame tongues from the feet to 2.5 b over '
        '24 t, smoke, crimson dust.')
def _p_death_flames():
    out = [card('flame', f'^{num(x, 2)} ^{num(y, 2)} ^{num(z, 2)}', bb='vertical', s0=(0.5, 0.3, 0.5), s1=(0.9, 1.2, 0.9),
                life=14, fade=6, dly=int(round(24 * k / 9)), dur=4, col=CRIM) for k, (x, y, z) in enumerate(DEATH_PTS)]
    out += [fly('smoke', yaw, 70, 1.6, h=1.6, s0=0.8, s1=1.6, life=16, fade=6, dly=8) for yaw in radial(3, 0)]
    out += [dust(DUSTC[C_BOL], 1.4, '~ ~1.4 ~', (0.4, 1.2, 0.4), 40), part('large_smoke', '~ ~1.6 ~', (0.4, 0.8, 0.4), 0.02, 10)]
    return out


@preset('wisp_turn', 'A wisp turns colour (as / at a wisp: its display, or the marker a wisp prop follows): c 2 red, c 1 white '
        'again; a puff in the new colour.', conv=(('c', 'c', None),))
def _p_wisp_turn():
    return []     # the public part recolours (see the writer); the body is the puff below


WISP_PUFF = {c: [fly('ember', yaw, 40, 0.6, s0=0.15, s1=0.25, life=8, fade=3, col=SPIRIT[c]) for yaw in radial(4, 45)]
             + [card('glow', '~ ~ ~', bb='center', s0=0.3, s1=1.0, life=7, fade=3, col=SPIRIT[c])]
             + ([part('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.02, 6)] if c == 1 else [dust(DUSTC[C_BOL], 1.0, '~ ~ ~', (0.2, 0.3, 0.2), 10)])
             for c in (1, 2)}


@preset('gate_flames', 'Crimson flames on the entrance gravestone (S3 gate/flames every 10 t: at the stone\'s flame point): '
        'two flame tongues, crimson spores. Ambient: skipped from SOFT live fx cards.')
def _p_gate_flames():
    return [card('flame', '^0.15 ^ ^', bb='vertical', s0=(0.4, 0.3, 0.4), s1=(0.6, 0.9, 0.6), life=12, fade=5, col=CRIM),
            card('flame', '^-0.15 ^ ^', bb='vertical', s0=(0.4, 0.3, 0.4), s1=(0.5, 0.7, 0.5), life=12, fade=5, dly=5, col=CRIM),
            part('crimson_spore', '~ ~0.4 ~', (0.25, 0.3, 0.25), 0, 4), dust(DUSTC[C_BOL], 1.0, '~ ~0.4 ~', (0.2, 0.35, 0.2), 3)]


@preset('ambient_petals', 'Arena ambience (the module, every ~10 t; at the arena centre): crimson embers and spores drifting '
        'down through the plaza (particles only). Ambient: skipped from SOFT live fx cards.')
def _p_ambient_petals():
    return [dust(DUSTC[C_BOL], 0.9, '~ ~6 ~', (12, 2, 12), 10), part('crimson_spore', '~ ~4 ~', (12, 3, 12), 0, 8),
            part('ash', '~ ~5 ~', (12, 2, 12), 0, 6)]


assert tuple(PRESETS) == tuple(api.KIT_PRESETS), set(PRESETS) ^ set(api.KIT_PRESETS)

# ----------------------------------------------------------------------------- props (api.KIT_PROPS)
PROPS = {
    # name -> (doc, kind, tint, billboard, scale (x, y, z), anim ('w' wheel frames / 's' spirit frames + bob / None))
    'wheel': ('B / Q2 flaming scythe wheel: one face card 2.3 b across facing its flight (the display\'s rotation), the '
              'four spin frames turned every tick by the kit.', 'wheel_0', WHITE, 'fixed', (2.3, 2.3, 2.3), 'w'),
    'crescent': ('P2 thrown flame crescent: one face card 2.8 b wide facing its flight.', 'crescent', WHITE, 'fixed',
                 (2.8, 2.8, 2.8), None),
    'feather': ('Q6 crimson feather bolt: one face card 0.7 x 1.4 b facing its flight, tip toward the display\'s local -y.',
                'feather', WHITE, 'fixed', (1.4, 1.4, 1.4), None),
    'orb': ('Q6 crimson orb: one card 1.2 b, always facing the viewer (an orb is round).', 'orb', WHITE, 'center',
            (1.2, 1.2, 1.2), None),
    'blade': ('G giant crimson blade: one card 1.4 x 5.6 b standing on the display (its base at the display, never below '
              'it), turning about the vertical to face the viewer.', 'blade', WHITE, 'vertical', (5.6, 5.6, 5.6), None),
    'clone': ('H crimson shadow clone: one face card 1.3 x 2.6 b, feet at the display, facing the display\'s yaw (its '
              'flight).', 'clone', WHITE, 'fixed', (2.6, 2.6, 2.6), None),
    'wisp': ('A flame spirit {c} (1 white, 2 red): one card 0.7 b facing the viewer, three flicker frames and a slow bob '
             'by the kit.', 'wisp_0', None, 'center', (0.7, 0.7, 0.7), 's'),
    'moon_halo': ('The red-moon halo: one card 7 b facing the viewer.', 'halo', WHITE, 'center', (7.0, 7.0, 7.0), None),
}
assert tuple(PROPS) == tuple(api.KIT_PROPS), (tuple(PROPS), api.KIT_PROPS)
WHEEL_FRAMES = [f'wheel_{k}' for k in range(4)]
WISP_FRAMES = [f'wisp_{k}' for k in range(3)]
WISP_BOB = 0.12

# ----------------------------------------------------------------------------- decals (api.KIT_DECALS)
FLOOD_SPREAD, FLOOD_HOLD, FLOOD_FADE = 44, 14, 4
POOL_HOLD, POOL_FADE = 20, 6
DECAL_HOLD = 3
RIM_RATIO = 0.7
RIM_BANDS = 10
DECALS = {
    'flood': 'F the red flood {r, t}: one crimson wash disc of radius r spreading from the centre over min(t - 6, 44) '
             'ticks; DECAL_FLASH ticks before t a bright overlay flashes on until the hit; it stays 14 t after t. A '
             'second call while it is shown re-times it (no second disc): it stays to the new t + 14 and flashes again.',
    'cracks': 'F the cracks {r}: glowing crimson cracks over radius r, 36 t (cosmetic), dimming after 22 t.',
    'strip': 'G a strip {len, w, yaw, t}: a translucent red band len x w centred on the executor along the absolute yaw, '
             'drawn out along its length in 6 t, bright from t - 6, gone at t + 3.',
    'rim_tint': 'G the rim tint {r0, r, t}: nested red annuli appear from radius r inward to r0 by t - 6 (the floor '
                'reddening inside the blade ring), bright from t - 6, gone at t + 3.',
    'pool': 'E70 the red pool {r, t} (cosmetic): a darker crimson disc spreading to r by t - 6, bright from t - 6, '
            'lingering 20 t after t.',
    'ring_o': 'Q5A a ring outline {r, t}: a thin red circle of radius r (outline only), bright from t - 6, gone at t + 3.',
    'donut_o': 'Q5A a donut outline {r0, r, t}: the two circles r0 and r, bright from t - 6, gone at t + 3.',
}
assert tuple(DECALS) == tuple(api.KIT_DECALS)

# ----------------------------------------------------------------------------- writer
HEADER = '# Generated by tools/build_mboss_kn_fx.py (아를레키노 fx kit) - edit the generator, not this file.\n'
E = FN + 'e/'
SEL = f'@e[type=minecraft:item_display,tag={TAG}'
DEF_A = f'tg:"{TAG}_c",tpd:0'
POOL_FX, POOL_DC = 0, 1
FAKE = ('#n', '#dn', '#now', '#wd', '#c2', '#roll', '#spin', '#life', '#fade', '#dly', '#dur', '#hit', '#pool', '#a',
        '#c', '#r', '#r0', '#t', '#p', '#o', '#i', '#j', '#f', '#h', '#fl', '#m', '#b', '#k', '#on', '#l', '#lid', '#at',
        '#af', '#lnW', '#lnA', '#demo', '#dt', '#c4', '#c10', '#c12', '#c20', '#c36', '#c77', '#c100', '#c360', '#c1000')
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
        '# Spawn one painted fx card at pos, rotated rot (relative to the executing context).',
        '# {kind, pos:"^x ^y ^z", rot:"~ ~", bb:fixed|center|vertical|horizontal, roll:<deg, about local z>,',
        '#  spin:<deg over the main interpolation, -170..170, about the card normal (y for flat / cross)>,',
        '#  s0:<start size>, s1:<end size>, move:"dx,dy,dz" (end offset, display frame: +x left, +y up, +z forward),',
        '#  life:<ticks>, fade:<shrink-out ticks>, col:<RGB int tint, 16777215 = the painted colours>}.',
        f'# Skipped (no error) while {CAP} fx cards are alive.', INIT,
        f'execute if score #n {OBJ} matches {CAP}.. run return 0',
        f'$data modify storage {STO} fx.a set value {{kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:"$(s0)f,$(s0)f,$(s0)f",s1:"$(s1)f,$(s1)f,$(s1)f",off:"0f,0f,0f",move:"$(move)",col:$(col),col2:-1,'
        f'ax:"0f,0f,1f",{DEF_A}}}',
        f'$data modify storage {STO} fx.a.ax set from storage {STO} fx.ax.$(kind)',
        f'$scoreboard players set #roll {OBJ} $(roll)',
        f'$scoreboard players set #spin {OBJ} $(spin)',
        f'$scoreboard players set #life {OBJ} $(life)',
        f'$scoreboard players set #fade {OBJ} $(fade)',
        f'scoreboard players set #dly {OBJ} 0',
        f'scoreboard players set #dur {OBJ} 0',
        f'scoreboard players set #hit {OBJ} -1',
        f'scoreboard players set #pool {OBJ} {POOL_FX}',
        f'function {E}make',
    ])
    W.w('cardx', [
        '# card with every option: s0 / s1 as "xf,yf,zf" vectors, off:"xf,yf,zf" (static start translation), move',
        '# (the END translation), dly:<ticks hidden before it shows>, dur:<ticks of the main interpolation, 0 = up to',
        '# the fade>, hit:<ticks after the call when the tint becomes col2, -1 = never>, col2:<RGB int>, pl:<pool: 0 fx',
        f'# (capped at {CAP}), 1 decal (never capped)>, tg:<the pool tag: {TAG}_c fx, {TAG}_d decal, {TAG}_fl the flood>.',
        INIT, f'$scoreboard players set #pool {OBJ} $(pl)',
        f'execute if score #pool {OBJ} matches {POOL_FX} if score #n {OBJ} matches {CAP}.. run return 0',
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
        '# #dly #dur #hit #pool (0 fx, 1 decal) -> one card. The stage clock is gametime + 1 (the fg kit\'s first-tick',
        '# fix): the ager (fx/e/world, a 1t schedule) runs at the END of this server tick with gametime already + 1, so',
        '# the main interpolation starts in the next server tick and the client animates it. Stages: shows at clock +',
        '# dly, interpolates from clock + dly + 1 over dur ticks, recolours at clock + hit, shrinks over the last fade',
        '# ticks, removed at clock + dly + life.',
        f'execute if score #pool {OBJ} matches {POOL_FX} run scoreboard players add #n {OBJ} 1',
        f'execute if score #pool {OBJ} matches {POOL_DC} run scoreboard players add #dn {OBJ} 1',
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
        f'execute store result score #c2 {OBJ} run data get storage {STO} fx.a.col2',
        f'data modify storage {STO} fx.a.z set from storage {STO} fx.a.s0',
        f'execute if score #dly {OBJ} matches 1.. run data modify storage {STO} fx.a.z set value "0f,0f,0f"',
        f'function {E}spawn with storage {STO} fx.a',
        'execute store result score #now ' + OBJ + ' run time query gametime', 'scoreboard players operation #now ' + OBJ + ' -= #btLag cb',
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
        'knS:{start_interpolation:0,interpolation_duration:0,transformation:{scale:[$(s0)]}},'
        'knG:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'knF:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}},'
        'knC:$(col2)}}}}',
        f'$execute positioned $(pos) rotated $(rot) run tp {SEL}_new,limit=1] ~ ~ ~ ~ ~',
    ])
    W.w('e/born', [
        '# Internal, as the new card: stage clock values (gametime + 1 based) in knFxS knFxG knFxH knFxK knFxD.',
        f'scoreboard players operation @s knFxS = #now {OBJ}',
        f'scoreboard players operation @s knFxS += #dly {OBJ}',
        'scoreboard players operation @s knFxG = @s knFxS',
        'scoreboard players add @s knFxG 1',
        'scoreboard players operation @s knFxD = @s knFxS',
        f'scoreboard players operation @s knFxD += #life {OBJ}',
        'scoreboard players operation @s knFxK = @s knFxD',
        f'scoreboard players operation @s knFxK -= #fade {OBJ}',
        f'scoreboard players operation @s knFxH = #now {OBJ}',
        f'scoreboard players operation @s knFxH += #hit {OBJ}',
        f'tag @s add {TAG}_go',
        f'execute if score #dly {OBJ} matches 1.. run tag @s add {TAG}_sh',
        f'execute if score #fade {OBJ} matches 1.. run tag @s add {TAG}_fd',
        f'execute if score #hit {OBJ} matches 0.. if score #c2 {OBJ} matches 0.. run tag @s add {TAG}_hit',
    ])
    W.w('e/world', [
        '# Ages the kit\'s cards once per tick while any is alive (scheduled from e/make and itself, so it runs at the',
        '# end of the server tick; no hook in rlk:tick). A dead or reviving player clears every card (fx/clear).',
        f'execute unless entity {SEL},limit=1] run return run function {E}zero',
        # VP beat: a tick the beat holds - nothing ages (per-run counters too), the loop stays scheduled
        f'execute if score #btHold cb matches 1 run return run schedule function {E}world 1t replace',
        f'execute if entity @a[tag=player,scores={{dead=1}}] run function {FN}clear',
        f'execute if entity @a[tag=player,scores={{rnDie=1..}}] run function {FN}clear',
        f'execute store result score #now {OBJ} run time query gametime', f'scoreboard players operation #now {OBJ} -= #btLag cb',
        f'execute as {SEL}] run function {E}age',
        f'execute store result score #n {OBJ} if entity {SEL},tag={TAG}_c]',
        f'execute store result score #dn {OBJ} if entity {SEL},tag=!{TAG}_c]',
        f'execute if entity {SEL},limit=1] run schedule function {E}world 1t replace',
    ])
    W.w('e/zero', [f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #dn {OBJ} 0'])
    W.w('e/age', [
        '# As one card (the stage clock in #now).',
        'execute unless score @s knFxD = @s knFxD run return run kill @s',
        f'execute if score #now {OBJ} >= @s knFxD run return run kill @s',
        f'execute if entity @s[tag={TAG}_sh] if score #now {OBJ} >= @s knFxS run function {E}show',
        f'execute if entity @s[tag={TAG}_go] if score #now {OBJ} >= @s knFxG run function {E}go',
        f'execute if entity @s[tag={TAG}_hit] if score #now {OBJ} >= @s knFxH run function {E}hit',
        f'execute if entity @s[tag={TAG}_fd] if score #now {OBJ} >= @s knFxK run function {E}fade',
    ])
    W.w('e/show', ['# a delayed card appears at its start size',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".knS',
                   f'tag @s remove {TAG}_sh'])
    W.w('e/go', ['# start -> end transformation over dur ticks (client interpolation)',
                 'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".knG',
                 f'tag @s remove {TAG}_go'])
    W.w('e/hit', ['# the tint changes (the second colour: decal flashes, white-hot closes, fading arcs)',
                  'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set from entity @s '
                  'item.components."minecraft:custom_data".knC',
                  f'tag @s remove {TAG}_hit'])
    W.w('e/fade', ['# shrink to nothing over the last fade ticks',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".knF',
                   f'tag @s remove {TAG}_fd'])
    spin_y = ','.join(f'{k}:"0f,1f,0f"' for k in ALL_KINDS if kind_info(k)[0] in SPIN_Y)
    W.w('e/init', ['# Objectives, constants and tables of the kit (made by the first call; removed by fx/uninstall).',
                   f'scoreboard objectives add {OBJ} dummy', *[f'scoreboard objectives add {o} dummy' for o in OBJECTIVES],
                   f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #dn {OBJ} 0',
                   *[f'scoreboard players set #c{v} {OBJ} {v}' for v in (4, 10, 12, 20, 36, 77, 100, 360, 1000)],
                   '# spin axes (= the card normal) of the flat and cross kinds; face / lance kinds keep z (storage a default)',
                   f'data modify storage {STO} fx.ax set value {{{spin_y}}}',
                   f'# the floor (y x 100) the clamps measure from: the arena\'s ({FLOOR}); test/stage sets the demo floor',
                   f'data modify storage {STO} fx.fl set value {FLOOR * 100}',
                   '# slash-arc floor clamp: the lowest point per mille per (pitch cell, roll cell), fx/e/clamp_arc',
                   f'data modify storage {STO} fx.low set value [I;{",".join(str(v) for v in LOW)}]',
                   f'data modify storage {STO} fx.hud set value {{badge:0b,ban:0b}}',
                   f'data modify storage {STO} fx.init set value 1b'])
    W.w('e/hgt', ['# #h = the executor\'s height over the floor in hundredths (storage fx.fl = the floor y x 100).',
                  f'execute summon minecraft:marker run function {E}hgt_m',
                  f'execute store result score #fl {OBJ} run data get storage {STO} fx.fl',
                  f'scoreboard players operation #h {OBJ} -= #fl {OBJ}'])
    W.w('e/hgt_m', ['# Internal: as a marker summoned at the executor: its y x 100, then gone.',
                    f'execute store result score #h {OBJ} run data get entity @s Pos[1] 100', 'kill @s'])
    W.w('e/clamp_arc', [
        '# Slash-arc floor clamp: #r reach (tenths), #p pitch, #o roll (degrees) -> #ly the lift (hundredths, <= ARC_LIFT)',
        '# and #r = min(#r, 100 (h - 10 + ly) / LOW) so the arc (bearings +-80 deg from the aim, unit radius x reach) stays',
        '# above the floor; LOW per mille from the table.',
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
        '# the lift: the arc rises (up to ARC_LIFT hundredths) by what it would reach below the floor, the rest shrinks it',
        f'scoreboard players operation #ly {OBJ} = #r {OBJ}', f'scoreboard players operation #ly {OBJ} *= #f {OBJ}',
        f'scoreboard players operation #ly {OBJ} /= #c100 {OBJ}', f'scoreboard players operation #ly {OBJ} -= #h {OBJ}',
        f'execute if score #ly {OBJ} matches ..-1 run scoreboard players set #ly {OBJ} 0',
        f'execute if score #ly {OBJ} matches {ARC_LIFT + 1}.. run scoreboard players set #ly {OBJ} {ARC_LIFT}',
        f'scoreboard players operation #h {OBJ} += #ly {OBJ}',
        f'scoreboard players operation #m {OBJ} = #h {OBJ}', f'scoreboard players operation #m {OBJ} *= #c100 {OBJ}',
        f'scoreboard players operation #m {OBJ} /= #f {OBJ}', f'scoreboard players operation #r {OBJ} < #m {OBJ}',
        f'execute if score #r {OBJ} matches ..4 run scoreboard players set #r {OBJ} 5'])
    W.w('e/lowf', ['# Internal (macro {i}): #f = the floor-clamp table entry i.',
                   f'$execute store result score #f {OBJ} run data get storage {STO} fx.low[$(i)]'])
    W.w('clear', ['# Remove every kit card (fx and decals) and close the banner. Safe to call any time (pause, death_start,',
                  '# cleanup). Props (the module\'s displays and the followers on its markers) are not cards: they stay.',
                  f'kill {SEL}]', INIT, f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #dn {OBJ} 0',
                  f'function {FN}hud/e/ban_off'])
    W.w('uninstall', ['# Remove the kit\'s cards, followers, demo stand-ins, the banner bossbar, objectives, storage rlk:kn fx',
                      '# and schedules (the module\'s uninstall hook).',
                      f'kill {SEL}]', f'kill @e[type=minecraft:item_display,tag={FOLLOW}]', f'kill @e[tag={DEMO}]',
                      f'tag @e[tag={LEAD}] remove {LEAD}',
                      f'execute if data storage {STO} fx.hud{{badge:1b}} run data remove storage {BADGE_MATCH}',
                      f'bossbar remove {BANNER_BAR}',
                      f'scoreboard objectives remove {OBJ}', *[f'scoreboard objectives remove {o}' for o in OBJECTIVES],
                      f'data remove storage {STO} fx',
                      f'schedule clear {E}world', f'schedule clear {E}anim', f'schedule clear {FN}hud/e/ln',
                      f'schedule clear {FN}hud/e/badge', f'schedule clear {FN}test/e/tick'])
    W.w('look', [
        '# Dress @s (an item_display the module owns) as a kit sprite: {kind, col:<RGB int>}. Full bright; the caller',
        '# keeps its own transformation / billboard.',
        '$data merge entity @s {item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        f'"{NS_TEX}$(kind)","minecraft:custom_model_data":{{colors:[$(col)]}}}}}},brightness:{{sky:15,block:15}}}}',
    ])
    # --- the prop anim / follow chain
    w_lines = [f'execute if score #af {OBJ} matches {k} as @e[type=minecraft:item_display,tag={ANIM}_w] run data modify entity '
               f'@s item.components."minecraft:item_model" set value "{NS_TEX}{fr}"' for k, fr in enumerate(WHEEL_FRAMES)]
    s_lines = [f'execute if score #af {OBJ} matches {4 * k} as @e[type=minecraft:item_display,tag={ANIM}_s] run data modify '
               f'entity @s item.components."minecraft:item_model" set value "{NS_TEX}{fr}"' for k, fr in enumerate(WISP_FRAMES)]
    bob = [f'execute if score #af {OBJ} matches {t} as @e[type=minecraft:item_display,tag={ANIM}_s] run data merge entity @s '
           f'{{start_interpolation:0,interpolation_duration:10,transformation:{{translation:[0f,{num(y)}f,0f]}}}}'
           for t, y in ((0, WISP_BOB), (10, -WISP_BOB))]
    W.w('e/anim', [
        '# The prop chain (scheduled every tick while a kit-animated prop exists; no hook in rlk:tick): followers stay on',
        '# their entity (and go with it), the wheels turn their four spin frames, the spirits flicker and bob.',
        f'execute unless entity @e[type=minecraft:item_display,tag={ANIM},limit=1] run return 0',
        f'scoreboard players add #at {OBJ} 1',
        f'execute as @e[type=minecraft:item_display,tag={FOLLOW}] run function {E}follow',
        f'scoreboard players operation #af {OBJ} = #at {OBJ}', f'scoreboard players operation #af {OBJ} %= #c4 {OBJ}',
        *w_lines,
        f'scoreboard players operation #af {OBJ} = #at {OBJ}', f'scoreboard players operation #af {OBJ} %= #c12 {OBJ}',
        *s_lines,
        f'scoreboard players operation #af {OBJ} = #at {OBJ}', f'scoreboard players operation #af {OBJ} %= #c20 {OBJ}',
        *bob,
        f'execute if entity @e[type=minecraft:item_display,tag={ANIM},limit=1] run schedule function {E}anim 1t replace'])
    W.w('e/follow', [
        '# As a follower display: on its entity (the same knFxL), or gone with it.',
        f'scoreboard players operation #l {OBJ} = @s knFxL',
        f'execute as @e[tag={LEAD}] if score @s knFxL = #l {OBJ} run tag @s add {TAG}_t',
        f'execute unless entity @e[tag={TAG}_t,limit=1] run return run kill @s',
        f'execute at @e[tag={TAG}_t,limit=1] run tp @s ~ ~ ~',
        f'tag @e[tag={TAG}_t] remove {TAG}_t'])


def props(W):
    P_ = FN + 'prop/'
    for name, (doc, kind, col, bb, sc, anim) in PROPS.items():
        tr = (f'transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[{num(sc[0])}f,{num(sc[1])}f,'
              f'{num(sc[2])}f],right_rotation:[0f,0f,0f,1f]}}')
        tags = [ANIM, f'{ANIM}_{anim}'] if anim else []
        colour = '$(col)' if col is None else str(col)
        dress = [f'{"$" if col is None else ""}data merge entity @s {{item:{{id:"minecraft:paper",count:1,components:{{'
                 f'"minecraft:item_model":"{NS_TEX}{kind}","minecraft:custom_model_data":{{colors:[{colour}]}}}}}},'
                 f'billboard:"{bb}",brightness:{{sky:15,block:15}},view_range:2f,shadow_radius:0f,{tr}}}']
        dress += [f'tag @s add {t}' for t in tags]
        if anim:
            dress.append(f'schedule function {E}anim 1t replace')
        args = api.KIT_PROPS[name]
        W.w(f'prop/e/{name}_d', [f'# Internal: dress @s (an item_display) as {name}' + (' (macro {col})' if col is None else '') + '.']
            + dress)
        withc = f' with storage {STO} fx.pc' if col is None else ''
        pub = [f'# {doc}', '# @s = the projectile / prop item_display (dressed in place, idempotent: resume calls it again; it',
               '# keeps its own position, rotation = its flight); any other entity (a sequence marker) gets one follower',
               '# display the kit keeps on it and removes with it (re-calling replaces it).', INIT]
        if col is None:
            pub += [f'$scoreboard players set #c {OBJ} $(c)',
                    f'data modify storage {STO} fx.pc set value {{col:{SPIRIT[1]}}}',
                    f'execute if score #c {OBJ} matches 2 run data modify storage {STO} fx.pc.col set value {SPIRIT[2]}']
        pub += [f'execute if entity @s[type=minecraft:item_display] run return run function {P_}e/{name}_d{withc}',
                f'function {P_}e/link',
                f'execute at @s run summon minecraft:item_display ~ ~ ~ {{Tags:["{FOLLOW}","{TAG}_nf","rlk_room","rlk_mb_aux"],'
                'teleport_duration:1}',
                f'execute as @e[type=minecraft:item_display,tag={TAG}_nf] run function {P_}e/{name}_f']
        W.w(f'prop/{name}', pub)
        assert sorted(args) == (['c'] if col is None else []), name
        W.w(f'prop/e/{name}_f', ['# Internal: as the new follower display: linked to the leader (#l), dressed, animated.',
                                 f'tag @s remove {TAG}_nf', f'scoreboard players operation @s knFxL = #l {OBJ}',
                                 f'tag @s add {ANIM}', f'function {P_}e/{name}_d{withc}',
                                 f'schedule function {E}anim 1t replace'])
    W.w('prop/e/link', ['# Internal: @s (the leader) gets a link id (once) and the lead tag; its old follower goes (#l = the id).',
                        f'execute unless score @s knFxL matches 1.. run scoreboard players add #lid {OBJ} 1',
                        f'execute unless score @s knFxL matches 1.. run scoreboard players operation @s knFxL = #lid {OBJ}',
                        f'scoreboard players operation #l {OBJ} = @s knFxL', f'tag @s add {LEAD}',
                        f'execute as @e[type=minecraft:item_display,tag={FOLLOW}] if score @s knFxL = #l {OBJ} run kill @s'])
    W.w('prop/e/recolour', ['# Internal (as a dressed wisp display, #c): its tint 1 white / 2 red.',
                            f'execute if score #c {OBJ} matches 2 run return run data modify entity @s item.components.'
                            f'"minecraft:custom_model_data".colors[0] set value {SPIRIT[2]}',
                            f'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set value {SPIRIT[1]}'])


def sounds(W):
    for name, (doc, layers) in SOUNDS.items():
        W.w(f'snd/{name}', [f'# {doc}', '# Layers: event volume pitch minVolume (mboss_lib.sound rule).'] +
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
    """[(text, stay, fade, ttl, gap)] of api.LINES[lid]"""
    steps = typed(api.LINES[lid])
    out = []
    for k, text in enumerate(steps):
        last = k == len(steps) - 1
        stay = LINE_HOLD if last else LINE_GAP + 6
        fade = 12 if last else 0
        out.append((text, stay, fade, stay + fade, LINE_GAP))
    return out


def hud_funcs(W):
    H = FN + 'hud/'
    badge = badge_component()
    W.w('hud/badge', [
        f'# {{on}}: the badge {api.BADGE} (crimson glyph + name) at the end of the boss-bar third line (rlk:mboss sub[]).',
        '# Idempotent (the old badge is removed first); while on, a 10 t chain re-appends it after any rewrite of sub.',
        '# The root text is empty and unstyled (no glyph-font inheritance).',
        INIT, f'data remove storage {BADGE_MATCH}', f'$scoreboard players set #on {OBJ} $(on)',
        f'data modify storage {STO} fx.hud.badge set value 0b',
        f'execute if score #on {OBJ} matches 1 run data modify storage {STO} fx.hud.badge set value 1b',
        f'execute if score #on {OBJ} matches 1 run data modify storage rlk:mboss sub append value {badge}',
        f'execute if score #on {OBJ} matches 1 run schedule function {H}e/badge 10t replace',
        f'execute unless score #on {OBJ} matches 1 run schedule clear {H}e/badge'])
    W.w('hud/e/badge', ['# Internal (10 t chain while the badge is on): put it back if a rewrite of rlk:mboss sub dropped it.',
                        f'execute unless data storage {STO} fx.hud{{badge:1b}} run return 0',
                        'execute unless data storage rlk:mboss sub run return 0',
                        f'execute unless data storage {BADGE_MATCH} run data modify storage rlk:mboss sub append value {badge}',
                        f'schedule function {H}e/badge 10t replace'])
    W.w('hud/banner', [
        f'# {{on}}: the real game\'s Banquet banner (api.BANNER, PLAN §4.6; ref/hud_bars_banner.jpg: under the boss bar,',
        f'# the first phrase salmon-red, the rest white) as a text line under the boss bars (bossbar {BANNER_BAR}, white',
        '# progress = no bar in this pack); 0 = off. S3 opens it at the window start, closes it at the end / break /',
        '# cancel, resume re-opens it.',
        INIT, f'$scoreboard players set #on {OBJ} $(on)',
        f'execute unless score #on {OBJ} matches 1 run return run function {H}e/ban_off',
        f'bossbar add {BANNER_BAR} {{text:""}}', f'bossbar set {BANNER_BAR} name {banner_component()}',
        f'bossbar set {BANNER_BAR} color white', f'bossbar set {BANNER_BAR} style progress', f'bossbar set {BANNER_BAR} max 1',
        f'bossbar set {BANNER_BAR} value 0', f'bossbar set {BANNER_BAR} players @a[tag=player]',
        f'bossbar set {BANNER_BAR} visible true', f'data modify storage {STO} fx.hud.ban set value 1b'])
    W.w('hud/e/ban_off', ['# Internal: the banner off (no error when it was never made).',
                          f'execute unless data storage {STO} fx.hud{{ban:1b}} run return 0',
                          f'bossbar set {BANNER_BAR} visible false', f'bossbar set {BANNER_BAR} players',
                          f'data modify storage {STO} fx.hud.ban set value 0b'])
    W.w('hud/line', [f'# {{id}}: the dialog subtitle of api.LINES[id] (ids {min(api.LINES)}..{max(api.LINES)}) with Raiden\'s letter',
                     '# reveal (two syllables per step, a quiet tick each); a new line replaces the running one.',
                     f'$function {H}l/$(id)'])
    for lid in api.LINES:
        steps = line_steps(lid)
        q = []
        for text, stay, fade, ttl, gap in steps:
            assert '"' not in text and '\\' not in text, text
            q.append(f'{{t:"{text}",s:{stay},f:{fade},n:{ttl},g:{gap}}}')
        W.w(f'hud/l/{lid}', [f'# Line {lid}: 「{api.LINES[lid]}」 ({len(steps)} steps).', INIT,
                             f'data modify storage {STO} fx.ln set value {{q:[{",".join(q)}]}}',
                             f'scoreboard players set #lnW {OBJ} 0', f'scoreboard players set #lnA {OBJ} 1',
                             f'function {H}e/ln'])
    W.w('hud/e/ln', ['# Internal: the running line (a 1 t chain): the next step when its gap is over.',
                     f'execute unless data storage {STO} fx.ln.q[0] run return 0',
                     f'execute if entity @a[tag=player,scores={{dead=1}}] run return run function {H}e/ln_stop',
                     f'scoreboard players remove #lnW {OBJ} 1',
                     f'execute if score #lnW {OBJ} matches ..0 run function {H}e/ln_step',
                     f'execute if data storage {STO} fx.ln.q[0] run schedule function {H}e/ln 1t replace'])
    W.w('hud/e/ln_step', ['# Internal: show the first queued step and drop it.',
                          f'execute store result score #lnW {OBJ} run data get storage {STO} fx.ln.q[0].g',
                          f'function {H}e/ln_show with storage {STO} fx.ln.q[0]',
                          f'data remove storage {STO} fx.ln.q[0]'])
    W.w('hud/e/ln_show', ['# Internal (macro: t text, s stay, f fade, n ttlT): one typing step on the subtitle line (Raiden).',
                          '$title @a[tag=player] times 0 $(s) $(f)',
                          f'$title @a[tag=player] subtitle {{text:"$(t)",color:"{LINE_COL}",bold:true}}',
                          'execute as @a[tag=player] run function rlk:view/ttl_blank',
                          '$scoreboard players set @a[tag=player] ttlT $(n)',
                          'execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0'])
    W.w('hud/e/ln_stop', ['# Internal: stop the running line and blank it.', f'data remove storage {STO} fx.ln',
                          f'schedule clear {H}e/ln', f'execute unless score #lnA {OBJ} matches 1 run return 0',
                          f'scoreboard players set #lnA {OBJ} 0', 'title @a[tag=player] subtitle ""',
                          'scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0'])
    W.w('hud/clear', ['# Badge, banner and the dialog line off (cleanup, uninstall).', INIT,
                      f'data remove storage {BADGE_MATCH}', f'data modify storage {STO} fx.hud.badge set value 0b',
                      f'schedule clear {H}e/badge', f'function {H}e/ban_off', f'function {H}e/ln_stop'])


# ----------------------------------------------------------------------------- decals -> datapack
def decals(W):
    D = FN + 'decal/'
    fl = f'~ ~{num(DECAL_Y, 3)} ~'
    fl2 = f'~ ~{num(DECAL_Y + 0.006, 3)} ~'
    fl1 = f'~ ~{num(DECAL_Y + 0.003, 3)} ~'
    head = lambda doc, args: [f'# {doc}', '# {' + ', '.join(args) + '} (tenths / ticks); at the decal centre on the floor (the call\'s y = the',
                              f'# floor top); cards at floor + {DECAL_Y} .. + 0.028; never capped.', INIT]

    # --- flood
    W.w('decal/flood', head(DECALS['flood'], api.KIT_DECALS['flood']) + [
        '$scoreboard players set #r knFx $(r)', '$scoreboard players set #t knFx $(t)',
        f'data modify storage {PA} set value {{}}',
        f'execute store result storage {PA}.s float 0.1 run scoreboard players get #r {OBJ}',
        f'execute store result storage {PA}.s0 float 0.005 run scoreboard players get #r {OBJ}',
        f'scoreboard players operation #a {OBJ} = #t {OBJ}', f'scoreboard players remove #a {OBJ} {api.DECAL_FLASH}',
        f'execute if score #a {OBJ} matches ..0 run scoreboard players set #a {OBJ} 0',
        f'execute store result storage {PA}.h int 1 run scoreboard players get #a {OBJ}',
        f'execute if score #a {OBJ} matches {FLOOD_SPREAD + 1}.. run scoreboard players set #a {OBJ} {FLOOD_SPREAD}',
        f'execute if score #a {OBJ} matches ..0 run scoreboard players set #a {OBJ} 1',
        f'execute store result storage {PA}.d int 1 run scoreboard players get #a {OBJ}',
        f'scoreboard players operation #a {OBJ} = #t {OBJ}', f'scoreboard players add #a {OBJ} {FLOOD_HOLD}',
        f'execute store result storage {PA}.l int 1 run scoreboard players get #a {OBJ}',
        f'scoreboard players set #a {OBJ} {api.DECAL_FLASH + 1}',
        f'execute store result storage {PA}.fl int 1 run scoreboard players get #a {OBJ}',
        f'execute if entity {SEL.replace(TAG, TAG + "_fl")},limit=1] run return run function {D}e/flood_re with storage {PA}',
        f'function {D}e/flood_new with storage {PA}'])
    W.w('decal/e/flood_new', ['# Internal (macro, storage fx.pa: s s0 d l h fl): the flood disc and its flash overlay.',
                              mac(card('flood', fl, '0 0', s0=('$(s0)', 1, '$(s0)'), s1=('$(s)', 1, '$(s)'), life='$(l)',
                                       fade=FLOOD_FADE, dur='$(d)', col=DIM, pool='fl')),
                              f'function {D}e/flood_flash with storage {PA}'])
    W.w('decal/e/flood_flash', ['# Internal (macro): the bright flood overlay from t - 6 to the hit.',
                                mac(card('flood', fl2, '0 0', s0=('$(s)', 1, '$(s)'), s1=('$(s)', 1, '$(s)'), life='$(fl)',
                                         dly='$(h)', col=WHITE, pool='dc'))])
    W.w('decal/e/flood_re', ['# Internal (macro): re-time the flood shown (it stays to the new t + 14) and flash it again.',
                             'execute store result score #now knFx run time query gametime', 'scoreboard players operation #now knFx -= #btLag cb', 'scoreboard players add #now knFx 1',
                             f'$scoreboard players set #a {OBJ} $(l)',
                             f'execute as {SEL.replace(TAG, TAG + "_fl")}] run function {D}e/retime',
                             f'function {D}e/flood_flash with storage {PA}'])
    W.w('decal/e/retime', ['# Internal (as the flood card): removed at now + #a, shrinking over the last ticks.',
                           f'scoreboard players operation @s knFxD = #now {OBJ}', f'scoreboard players operation @s knFxD += #a {OBJ}',
                           'scoreboard players operation @s knFxK = @s knFxD', f'scoreboard players remove @s knFxK {FLOOD_FADE}',
                           f'tag @s add {TAG}_fd'])
    # --- pool
    W.w('decal/pool', head(DECALS['pool'], api.KIT_DECALS['pool']) + [
        '$scoreboard players set #r knFx $(r)', '$scoreboard players set #t knFx $(t)',
        f'data modify storage {PA} set value {{}}',
        f'execute store result storage {PA}.s float 0.1 run scoreboard players get #r {OBJ}',
        f'execute store result storage {PA}.s0 float 0.01 run scoreboard players get #r {OBJ}',
        f'scoreboard players operation #a {OBJ} = #t {OBJ}', f'scoreboard players remove #a {OBJ} {api.DECAL_FLASH}',
        f'execute if score #a {OBJ} matches ..0 run scoreboard players set #a {OBJ} 0',
        f'execute store result storage {PA}.h int 1 run scoreboard players get #a {OBJ}',
        f'execute if score #a {OBJ} matches ..0 run scoreboard players set #a {OBJ} 1',
        f'execute store result storage {PA}.d int 1 run scoreboard players get #a {OBJ}',
        f'scoreboard players operation #a {OBJ} = #t {OBJ}', f'scoreboard players add #a {OBJ} {POOL_HOLD}',
        f'execute store result storage {PA}.l int 1 run scoreboard players get #a {OBJ}',
        f'function {D}e/pool with storage {PA}'])
    W.w('decal/e/pool', ['# Internal (macro): the pool disc, spreading, bright from t - 6.',
                         mac(card('flood', fl, '0 0', s0=('$(s0)', 1, '$(s0)'), s1=('$(s)', 1, '$(s)'), life='$(l)',
                                  fade=POOL_FADE, dur='$(d)', hit='$(h)', col=DIM2, col2=rgb('#E8C8C8'), pool='dc'))])
    # --- cracks
    W.w('decal/cracks', head(DECALS['cracks'], api.KIT_DECALS['cracks']) + [
        '$scoreboard players set #r knFx $(r)', f'data modify storage {PA} set value {{}}',
        f'execute store result storage {PA}.s float 0.1 run scoreboard players get #r {OBJ}',
        f'execute store result storage {PA}.s9 float 0.09 run scoreboard players get #r {OBJ}',
        f'function {D}e/cracks with storage {PA}'])
    W.w('decal/e/cracks', ['# Internal (macro): the crack decal, dimming after 22 t, gone at 36 t.',
                           mac(card('cracks', fl1, '0 0', s0=('$(s9)', 1, '$(s9)'), s1=('$(s)', 1, '$(s)'), life=36, dur=2,
                                    hit=22, col=WHITE, col2=DIM2, pool='dc'))])
    # --- strip
    W.w('decal/strip', head(DECALS['strip'], api.KIT_DECALS['strip']) + [
        '$scoreboard players set #t knFx $(t)', f'data modify storage {PA} set value {{}}',
        f'$data modify storage {PA}.yaw set value $(yaw)',
        f'$execute store result storage {PA}.w float 0.1 run scoreboard players set #a {OBJ} $(w)',
        f'$execute store result storage {PA}.l float 0.1 run scoreboard players set #a {OBJ} $(len)',
        f'$execute store result storage {PA}.l0 float 0.01 run scoreboard players set #a {OBJ} $(len)',
        *_t_lines(DECAL_HOLD), f'function {D}e/strip with storage {PA}'])
    W.w('decal/e/strip', ['# Internal (macro): one strip card along the absolute yaw.',
                          mac(card('strip', fl, '$(yaw) 0', s0=('$(w)', 1, '$(l0)'), s1=('$(w)', 1, '$(l)'), life='$(lf)',
                                   dur=6, hit='$(h)', col=DIM, col2=WHITE, pool='dc'))])
    # --- ring / donut
    W.w('decal/ring_o', head(DECALS['ring_o'], api.KIT_DECALS['ring_o']) + [
        '$scoreboard players set #t knFx $(t)', f'data modify storage {PA} set value {{}}',
        f'$execute store result storage {PA}.s float 0.1 run scoreboard players set #a {OBJ} $(r)',
        f'$execute store result storage {PA}.s9 float 0.092 run scoreboard players set #a {OBJ} $(r)',
        *_t_lines(DECAL_HOLD), f'function {D}e/ring with storage {PA}'])
    W.w('decal/donut_o', head(DECALS['donut_o'], api.KIT_DECALS['donut_o']) + [
        '$scoreboard players set #t knFx $(t)', f'data modify storage {PA} set value {{}}',
        *_t_lines(DECAL_HOLD),
        f'$execute store result storage {PA}.s float 0.1 run scoreboard players set #a {OBJ} $(r)',
        f'$execute store result storage {PA}.s9 float 0.092 run scoreboard players set #a {OBJ} $(r)',
        f'function {D}e/ring with storage {PA}',
        f'$execute store result storage {PA}.s float 0.1 run scoreboard players set #a {OBJ} $(r0)',
        f'$execute store result storage {PA}.s9 float 0.092 run scoreboard players set #a {OBJ} $(r0)',
        f'function {D}e/ring with storage {PA}'])
    W.w('decal/e/ring', ['# Internal (macro): one ring outline of scale s (drawn in from 0.92 s over 3 t).',
                         mac(card('ring', fl1, '0 0', s0=('$(s9)', 1, '$(s9)'), s1=('$(s)', 1, '$(s)'), life='$(lf)', dur=3,
                                  hit='$(h)', col=DIM, col2=WHITE, pool='dc'))])
    # --- rim tint: nested bands from r inward to r0
    band = ['$scoreboard players set #r knFx $(r)', '$scoreboard players set #r0 knFx $(r0)', '$scoreboard players set #t knFx $(t)',
            f'data modify storage {PA} set value {{}}', *_t_lines(DECAL_HOLD),
            '# the inward front: band k (outer radius r 0.7^k) shows when the front reaches it, dly = (t - 6) (r - r_k) / (r - r0)',
            f'scoreboard players operation #m {OBJ} = #r {OBJ}', f'scoreboard players operation #m {OBJ} -= #r0 {OBJ}',
            f'execute if score #m {OBJ} matches ..0 run scoreboard players set #m {OBJ} 1',
            f'scoreboard players operation #k {OBJ} = #t {OBJ}', f'scoreboard players remove #k {OBJ} {api.DECAL_FLASH}',
            f'execute if score #k {OBJ} matches ..0 run scoreboard players set #k {OBJ} 0']
    for k in range(RIM_BANDS):
        f1000 = int(round(1000 * RIM_RATIO ** k))
        band += [f'scoreboard players operation #b {OBJ} = #r {OBJ}', f'scoreboard players set #a {OBJ} {f1000}',
                 f'scoreboard players operation #b {OBJ} *= #a {OBJ}', f'scoreboard players operation #b {OBJ} /= #c1000 {OBJ}',
                 f'execute if score #b {OBJ} <= #r0 {OBJ} run return 0',
                 f'function {D}e/band_k']
    W.w('decal/rim_tint', head(DECALS['rim_tint'], api.KIT_DECALS['rim_tint']) + band)
    W.w('decal/e/band_k', ['# Internal: one band of outer radius #b (tenths) with its delay; #b <= 10 draws the centre disc.',
                           f'execute store result storage {PA}.s float 0.1 run scoreboard players get #b {OBJ}',
                           f'scoreboard players operation #a {OBJ} = #r {OBJ}', f'scoreboard players operation #a {OBJ} -= #b {OBJ}',
                           f'scoreboard players operation #a {OBJ} *= #k {OBJ}', f'scoreboard players operation #a {OBJ} /= #m {OBJ}',
                           f'execute store result storage {PA}.dl int 1 run scoreboard players get #a {OBJ}',
                           '# its life ends with the others at t + hold (the life counts from its delayed show)',
                           f'scoreboard players operation #b {OBJ} = #t {OBJ}', f'scoreboard players add #b {OBJ} {DECAL_HOLD}',
                           f'scoreboard players operation #b {OBJ} -= #a {OBJ}',
                           f'execute store result storage {PA}.lb int 1 run scoreboard players get #b {OBJ}',
                           f'function {D}e/band with storage {PA}'])
    W.w('decal/e/band', ['# Internal (macro): one annulus card (0.7 .. 1.0 of its scale), bright from t - 6.',
                         mac(card('band', fl, '0 0', s0=('$(s)', 1, '$(s)'), s1=('$(s)', 1, '$(s)'), life='$(lb)',
                                  dly='$(dl)', hit='$(h)', col=DIM, col2=WHITE, pool='dc'))])


def _t_lines(hold):
    """storage fx.pa h = t - 6 (>= 0: the flash), lf = t + hold (the life), lb = lf (the band life is cut by its delay in
    band_k: the bands all go at t + hold)"""
    return [f'scoreboard players operation #a {OBJ} = #t {OBJ}', f'scoreboard players remove #a {OBJ} {api.DECAL_FLASH}',
            f'execute if score #a {OBJ} matches ..0 run scoreboard players set #a {OBJ} 0',
            f'execute store result storage {PA}.h int 1 run scoreboard players get #a {OBJ}',
            f'scoreboard players operation #a {OBJ} = #t {OBJ}', f'scoreboard players add #a {OBJ} {hold}',
            f'execute store result storage {PA}.lf int 1 run scoreboard players get #a {OBJ}',
            f'execute store result storage {PA}.lb int 1 run scoreboard players get #a {OBJ}']


# ----------------------------------------------------------------------------- presets -> datapack
def presets_dp(W):
    for name, (doc, args, f, conv, split, pre) in PRESETS.items():
        head = [f'# {doc}']
        if args:
            head.append('# {' + ', '.join(args) + '} (macro: tenths of a block, degrees, ticks, c 1 Pyro / 2 crimson)')
        if name in AMBIENT:
            head += [f'# Ambient: skipped while {SOFT}+ fx cards live.', INIT,
                     f'execute if score #n {OBJ} matches {SOFT}.. run return 0']
        variants = {c: f(c) for c in (C_PY, C_BOL)} if split else {None: f()}
        if name in PTCL:
            assert not any(f'{FN}card' in l for l in variants[None]), name
        if name == 'stun_motes':
            pub = head + [INIT, f'data modify storage {PA} set value {{}}'] + variants[None] + \
                [f'function {FN}p/e/{name} with storage {PA}']
            W.w(f'p/e/{name}', [f'# Internal (macro, storage {PA}: y the start angle) of p/{name}.'] + STUN_BODY)
            W.w(f'p/{name}', pub)
            continue
        if name == 'rapid_slash':
            pub = head + [INIT, f'data modify storage {PA} set value {{}}'] + variants[None] + \
                [f'function {FN}p/e/{name} with storage {PA}']
            W.w(f'p/e/{name}', [f'# Internal (macro, storage {PA}: y y2 bearings, ro roll) of p/{name}.'] + RAPID_BODY)
            W.w(f'p/{name}', pub)
            continue
        if name == 'wisp_turn':
            pub = head + [INIT, '$scoreboard players set #c knFx $(c)',
                          f'execute if entity @s[type=minecraft:item_display] run function {FN}prop/e/recolour',
                          f'execute if score @s knFxL matches 1.. run scoreboard players operation #l {OBJ} = @s knFxL',
                          f'execute unless entity @s[type=minecraft:item_display] if score @s knFxL matches 1.. as '
                          f'@e[type=minecraft:item_display,tag={FOLLOW}] if score @s knFxL = #l {OBJ} run function '
                          f'{FN}prop/e/recolour',
                          f'execute if score #c {OBJ} matches 2 run return run function {FN}p/e/{name}_2',
                          f'function {FN}p/e/{name}_1']
            for c in (1, 2):
                W.w(f'p/e/{name}_{c}', [f'# Internal of p/{name}: the puff of colour {c}.'] + WISP_PUFF[c])
            W.w(f'p/{name}', pub)
            continue
        if not args and not pre and not conv:
            W.w(f'p/{name}', head + variants[None])
            assert not any(l.startswith('$') for l in variants[None]), name
            continue
        pub = list(head)
        if INIT not in pub:
            pub.append(INIT)
        if 'c' in args:
            pub.append(f'$scoreboard players set #c {OBJ} $(c)')
        pub.append(f'data modify storage {PA} set value {{}}')
        for a in args:
            if a in ('yaw', 'pitch', 'roll'):
                pub.append(f'$data modify storage {PA}.{a} set value $({a})')
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
            for c, body in variants.items():
                w = f' with storage {PA}' if any(l.startswith('$') for l in body) else ''
                if c == C_BOL:
                    pub.append(f'execute if score #c {OBJ} matches {C_BOL} run return run function {FN}p/e/{name}_{c}{w}')
            body1 = variants[C_PY]
            w1 = f' with storage {PA}' if any(l.startswith('$') for l in body1) else ''
            pub.append(f'function {FN}p/e/{name}_{C_PY}{w1}')
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
    _d, _a, f, _c, split, _p = PRESETS[name]
    if name == 'stun_motes':
        bodies = [STUN_BODY]
    elif name == 'rapid_slash':
        bodies = [RAPID_BODY]
    elif name == 'wisp_turn':
        bodies = list(WISP_PUFF.values())
    else:
        bodies = [f(1), f(2)] if split else [f()]
    return max(sum(1 for l in b if f'{FN}card' in l) for b in bodies)


# ----------------------------------------------------------------------------- tests and demos
TEST_ARGS = {'r': 36, 'yaw': 0, 'pitch': 0, 'roll': 0, 'c': 1, 'len': 70, 't': 30, 'r0': 0, 'w': 30, 'on': 1, 'id': 1, 'h': 24}


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
    return f'function {FN}hud/{name} {{' + ','.join(f'{k}:{int(v)}' for k, v in args.items()) + '}'


def decal(name, **args):
    assert name in api.KIT_DECALS and sorted(args) == sorted(api.KIT_DECALS[name]), name
    return f'function {FN}decal/{name} {{' + ','.join(f'{k}:{int(v)}' for k, v in args.items()) + '}'


def _ev(t, where, *lines):
    return [(t, where, l) for l in lines]


def _demos():
    f = fx
    D = {}
    D['slash_arc'] = sum([_ev(5 + 14 * i, 'chest', f('slash_arc', r=r, yaw=0, pitch=p, roll=ro, c=c), snd(s))
                          for i, (r, p, ro, c, s) in enumerate(((42, 0, 0, 1, 'swing_light'), (42, 0, 180, 1, 'swing_light'),
                                                                (36, -50, 90, 1, 'slam'), (56, 0, 10, 2, 'wing_hit'),
                                                                (42, -60, 90, 1, 'swing_heavy'), (40, -30, 100, 2, 'sweep')))], [])
    D['spin_ring'] = _ev(5, 'waist', f('spin_ring', r=46, c=1), snd('spin')) + _ev(30, 'body', f('spin_ring', r=25, c=1)) + \
        _ev(55, 'waist', f('spin_ring', r=42, c=2), snd('spin'))
    D['twirl_ring'] = _ev(5, 'hand', f('twirl_ring'), snd('twirl')) + _ev(10, 'body', f('spin_ring', r=25, c=1), snd('twirl_ring'))
    D['scythe_form'] = _ev(5, 'hand', f('scythe_form'), snd('scythe_vortex')) + _ev(15, 'hand', snd('scythe_form'))
    D['embers_puff'] = _ev(5, 'chest', f('embers_puff'), snd('cup_embers')) + _ev(25, 'hand', f('embers_puff'))
    D['wheel_trail'] = _ev(5, 'body', f('wheel_trail', len=160), snd('wheel_throw'))
    D['dash_trail'] = (_ev(0, 'chest', f('embers_puff'), snd('dash_tell')) + _ev(14, 'waist', f('dash_trail', len=120, c=1), snd('dash'))
                       + _ev(40, 'waist', f('dash_trail', len=80, c=2), snd('dash')))
    D['leap_flare'] = _ev(5, 'low', f('leap_flare'), snd('leap'))
    D['dive_streak'] = _ev(5, 'high', f('dive_streak', len=90), snd('dive')) + _ev(25, 'waist', f('dive_streak', len=60))
    D['impact_burst'] = (_ev(5, 'spot', f('impact_burst', r=36, c=1), snd('impact')) + _ev(25, 'spot', f('impact_burst', r=22, c=2),
                                                                                         snd('claw_grab')))
    D['claw'] = _ev(5, 'spot1', f('claw', r=22), snd('claw_reach')) + _ev(9, 'spot', snd('claw_grab'))
    D['wing_burst'] = _ev(5, 'chest', f('wing_burst'), snd('wing_burst'))
    D['zig_streak'] = sum([_ev(5 + 10 * i, 'chest12', f('zig_streak', len=40), snd('zig')) for i in range(3)], [])
    D['brand_ring'] = _ev(5, 'body', f('brand_ring'), snd('brand')) + _ev(21, 'chest1', f('brand_x'), snd('bond_gain'))
    D['brand_x'] = _ev(5, 'chest1', f('brand_x'), snd('brand'))
    D['threads'] = _ev(5, 'spot', f('threads', r=60), snd('threads')) + _ev(25, 'body3', f('threads', r=10), snd('leap'))
    D['thorns'] = _ev(5, 'spot', f('thorns', r=60), snd('threads'))
    D['blast'] = _ev(5, 'spot', f('blast', r=60), snd('blast'))
    D['web'] = _ev(5, 'webpt', f('web'), snd('perch'))
    D['clone_trail'] = _ev(5, 'chest', f('clone_trail'), snd('clone_launch'))
    D['blade_rise'] = _ev(5, 'spot', f('blade_rise'), snd('blade_rise'))
    D['blade_burst'] = _ev(5, 'spot1', f('blade_burst'), snd('cross_hit'))
    D['cross_thorns'] = sum([_ev(5 + i, w, f('cross_thorns', h=h)) for i, (w, h) in
                             enumerate((('tl0', 26), ('tl1', 19), ('tl2', 29)))], []) + _ev(8, 'spot', snd('cross_hit'))
    D['shock_gain'] = _ev(5, 'chest1', f('shock_gain'), snd('shock_gain'))
    D['shock_aura'] = _ev(5, 'hand', f('shock_aura'), snd('claw_reach'))
    D['shock_hit'] = _ev(5, 'chest', f('shock_hit'), snd('shock_hit'))
    D['break_burst'] = _ev(5, 'chest', f('break_burst'), snd('break'), snd('stun'))
    D['stun_motes'] = sum([_ev(5 + 10 * i, 'head', f('stun_motes')) for i in range(4)], [])
    D['pillar'] = _ev(5, 'body', f('pillar', r=12), snd('t_pillar')) + _ev(40, 'body', f('pillar', r=16), snd('t_swap'))
    D['shroud'] = _ev(5, 'body', f('shroud'), snd('scythe_vortex'))
    D['shroud_burst'] = _ev(13, 'chest', f('shroud_burst'), snd('t_swap'))
    D['legs_burst'] = sum([_ev(5 + 6 * i, 'chest', f('legs_burst'), snd('t_legs')) for i in range(3)], [])
    D['moon_flare'] = _ev(5, 'moon', f('moon_flare'), snd('moon'))
    D['aim_line'] = sum([_ev(t, 'chest', f('aim_line', len=60)) for t in range(5, 25, 2)], []) + _ev(5, 'chest', snd('beam_aim'))
    D['reticle'] = _ev(5, 'chest', f('reticle'), snd('beam_aim')) + _ev(31, 'chest', f('beam', len=200), snd('beam_fire'))
    D['beam'] = _ev(5, 'chest', f('beam', len=200), snd('beam_fire'))
    D['x_mark'] = _ev(5, 'body', f('x_mark'), snd('x_carve')) + _ev(17, 'body', snd('x_carve')) + \
        sum([_ev(30 + 3 * i, 'chest12', f('rapid_slash'), snd('rapid')) for i in range(9)], []) + \
        _ev(75, 'body', f('final_burst', r=75), snd('final'))
    D['rapid_slash'] = sum([_ev(5 + 3 * i, 'chest12', f('rapid_slash'), snd('rapid')) for i in range(6)], [])
    D['final_burst'] = _ev(5, 'body', f('final_burst', r=40), snd('final'))
    D['feather_hit'] = sum([_ev(5 + 8 * i, 'spot', f('feather_hit'), snd('feather')) for i in range(3)], [])
    D['orb_gather'] = _ev(5, 'body', f('orb_gather'), snd('orbs_gather'))
    D['orb_burst'] = _ev(5, 'spot', f('orb_burst', r=50), snd('orb_burst'))
    D['death_flames'] = _ev(5, 'body', f('death_flames'), snd('death_flames')) + _ev(35, 'body', f('final_burst', r=20), snd('death_gone'))
    D['wisp_turn'] = _ev(5, 'chest', f('wisp_turn', c=2)) + _ev(25, 'chest', f('wisp_turn', c=1))
    D['gate_flames'] = sum([_ev(t, 'spot', f('gate_flames')) for t in range(5, 60, 10)], [])
    D['ambient_petals'] = sum([_ev(t, 'body', f('ambient_petals')) for t in range(0, 80, 10)], [])
    assert set(D) == set(PRESETS), set(D) ^ set(PRESETS)
    return D


DEMOS = _demos()
DEMO_LEN = {k: max(t for t, _w, _l in v) + 40 for k, v in DEMOS.items()}
DEMO_WHERE = {
    'body': 'at @s rotated as @s rotated ~ 0',
    'low': 'at @s rotated as @s rotated ~ 0 positioned ~ ~0.3 ~',
    'waist': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~',
    'chest1': 'at @s rotated as @s rotated ~ 0 positioned ^ ^1 ^2',
    'chest': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~',
    'chest12': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~',
    'hand': 'at @s rotated as @s rotated ~ 0 positioned ^-0.5 ^1.2 ^0.4',
    'head': 'at @s rotated as @s rotated ~ 0 positioned ~ ~2.3 ~',
    'body3': 'at @s rotated as @s rotated ~ 0 positioned ~ ~3 ~',
    'webpt': 'at @s rotated as @s rotated ~ 0 positioned ~ ~4 ~',
    'high': 'at @s rotated as @s rotated ~ 0 positioned ~ ~6 ~',
    'spot': 'at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4.5',
    'spot1': 'at @s rotated as @s rotated ~ 0 positioned ^ ^1 ^4.5',
    'tl0': 'at @s rotated as @s rotated ~ 0 positioned ^-0.5 ^ ^3.35',
    'tl1': 'at @s rotated as @s rotated ~ 0 positioned ^0.45 ^ ^4.5',
    'tl2': 'at @s rotated as @s rotated ~ 0 positioned ^-0.05 ^ ^5.65',
    'moon': 'at @s rotated as @s rotated ~ 0 positioned ^ ^9 ^-6',
}
def demo_lens():
    lens = dict(DEMO_LEN, **{f'prop/{p}': 90 for p in PROPS}, **{f'decal/{d}': 60 for d in DECALS})
    lens['decal/flood'] = 130
    return lens


PROP_DEMO_MOVE = {'wheel': 0.6, 'crescent': 0.6, 'feather': 0.3, 'clone': 0.3}


def tests(W):
    T = FN + 'test/'
    stand = (f'summon minecraft:armor_stand ~ ~ ~ {{Tags:["{DEMO}","rlk_room","rlk_mb_aux"],NoGravity:1b,Invulnerable:1b,'
             'ShowArms:1b,NoBasePlate:1b,equipment:{mainhand:{id:"minecraft:netherite_hoe",count:1},'
             'head:{id:"minecraft:red_stained_glass",count:1},chest:{id:"minecraft:netherite_chestplate",count:1}}}')
    STAND = f'@e[type=minecraft:armor_stand,tag={DEMO},limit=1]'
    W.w('test/stage', ['# The demo stand-in: an armour stand with a netherite hoe 6 b in front of the executor, facing it',
                       '# (a vanilla stand-in for the body; no rig calls). Its feet are the demo floor (storage fx.fl).',
                       f'# /execute as @p at @s rotated ~ 0 run function {T}stage, then {T}<preset>.',
                       f'function {T}stop',
                       f'execute positioned ^ ^ ^6 run {stand}',
                       f'execute as {STAND} at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0',
                       INIT, f'execute store result storage {STO} fx.fl int 100 run data get entity {STAND} Pos[1]',
                       f'scoreboard players set #demo {OBJ} 0', f'scoreboard players set #dt {OBJ} 0',
                       f'schedule function {T}e/tick 1t replace'])
    W.w('test/stop', ['# Remove the demo stand-in and the test props; the floor back to the arena\'s.', f'kill @e[tag={DEMO}]',
                      f'schedule clear {T}e/tick', f'scoreboard players set #demo {OBJ} 0',
                      f'execute if data storage {STO} fx{{init:1b}} run data modify storage {STO} fx.fl set value {FLOOR * 100}'])
    tick = ['# Demo ticker (scheduled): the running demo\'s events as the stand-in; demo props fly on.',
            f'execute unless entity {STAND} run return 0',
            f'execute if score #demo {OBJ} matches 1.. run scoreboard players add #dt {OBJ} 1',
            f'execute as @e[type=minecraft:item_display,tag={DEMO}_mv] at @s run tp @s ^ ^ ^0.5']
    allk = list(DEMOS) + [f'prop/{p}' for p in PROPS] + [f'decal/{d}' for d in DECALS]
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
        W.w(f'test/prop/{name}', demo_entry(k, f'prop/{name}', 'one display dressed in front of it' +
                                            (' and one marker it follows' if name in ('wisp', 'moon_halo') else '') + '.'))
        args = '{c:1}' if name == 'wisp' else ''
        mv = name in PROP_DEMO_MOVE
        tags = f'["{DEMO}","rlk_room","rlk_mb_aux"{"," + chr(34) + DEMO + "_mv" + chr(34) if mv else ""}]'
        lines = [f'# Demo prop "{name}" (as the stand-in).',
                 f'execute if score #dt {OBJ} matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^1.2 ^1.5 run summon '
                 f'minecraft:item_display ~ ~ ~ {{Tags:{tags},teleport_duration:1}}',
                 f'execute if score #dt {OBJ} matches 1 as @e[type=minecraft:item_display,tag={DEMO},limit=1,sort=nearest] at @s '
                 f'rotated as {STAND} run tp @s ~ ~ ~ ~ 0',
                 f'execute if score #dt {OBJ} matches 1 as @e[type=minecraft:item_display,tag={DEMO},limit=1,sort=nearest] run '
                 f'function {FN}prop/{name} {args}'.rstrip()]
        if name in ('wisp', 'moon_halo'):
            up = '^2 ^1.6 ^2' if name == 'wisp' else '^ ^6 ^3'
            lines += [f'execute if score #dt {OBJ} matches 1 at @s rotated as @s rotated ~ 0 positioned {up} run summon '
                      f'minecraft:marker ~ ~ ~ {{Tags:["{DEMO}","rlk_room","rlk_mb_aux"]}}',
                      f'execute if score #dt {OBJ} matches 1 as @e[type=minecraft:marker,tag={DEMO},limit=1] at @s run '
                      f'function {FN}prop/{name} {args}'.rstrip(),
                      f'execute if score #dt {OBJ} matches 2..60 as @e[type=minecraft:marker,tag={DEMO},limit=1] at @s run '
                      f'tp @s ^0.08 ^ ^ ~3 ~']
        if name == 'wisp':
            lines.append(f'execute if score #dt {OBJ} matches 40 as @e[type=minecraft:marker,tag={DEMO},limit=1] at @s run '
                         f'{fx("wisp_turn", c=2)}')
        W.w(f'test/e/prop/{name}', lines)
    base += len(PROPS)
    dcalls = {'flood': [(1, decal('flood', r=60, t=50)), (56, decal('flood', r=60, t=30)), (86, decal('cracks', r=60))],
              'cracks': [(1, decal('cracks', r=60))],
              'strip': [(1, decal('strip', len=140, w=30, yaw=0, t=28)),
                        (1, decal('strip', len=140, w=30, yaw=90, t=28))],
              'rim_tint': [(1, decal('rim_tint', r0=0, r=60, t=34))],
              'pool': [(1, decal('pool', r=60, t=30))],
              'ring_o': [(1, decal('ring_o', r=60, t=35))],
              'donut_o': [(1, decal('donut_o', r0=30, r=70, t=21))]}
    for i, name in enumerate(DECALS):
        k = base + i + 1
        W.w(f'test/decal/{name}', demo_entry(k, f'decal/{name}', 'on the floor 7 b in front of it.'))
        lines = [f'# Demo decal "{name}" (as the stand-in; the floor at its feet).']
        for tk, line in dcalls[name]:
            lines.append(f'execute if score #dt {OBJ} matches {tk} at @s rotated as @s rotated ~ 0 positioned ^ ^ ^7 run {line}')
        W.w(f'test/e/decal/{name}', lines)
    W.w('test/sounds', ['# Click through the sound recipes (tellraw list).',
                        'tellraw @s [{"text":"아를레키노 sounds: ","color":"#E0303A"}' +
                        ''.join(f',{{"text":"[{n}] ","color":"#FFB0B8","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}"}}}}' for n in SOUNDS) + ']'])
    W.w('test/hud', ['# The HUD: the badge on the boss-bar third line, the banner and dialog line 1, then all off after 6 s.',
                     hud('badge', on=1), hud('banner', on=1), hud('line', id=1), f'schedule function {T}e/hud2 120t replace'])
    W.w('test/e/hud2', [hud('clear')])
    kinds = ['# Every fx kind in rows in front of the executor (3 s each):',
             f'# /execute as @p at @s rotated ~ 0 run function {T}kinds']
    for i, kind in enumerate(ALL_KINDS):
        row, colm = divmod(i, 8)
        x = 7.0 - 2.0 * colm
        z = 5 + 2.6 * row
        plane = kind_info(kind)[0]
        if plane == 'flat':
            kinds.append(card(kind, f'^{num(x)} ^0.3 ^{num(z)}', '~ 0', s0=0.3, s1=1.0, life=60, fade=10))
        elif plane == 'lance':
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
    decals(W)
    tests(W)
    removed = W.flush()
    return len(W.files), removed, W


def manifest():
    return {
        'generator': 'tools/build_mboss_kn_fx.py', 'api': 'tools/mboss_arlecchino/api.py §8; scratchpad ar/contract.md §3.3',
        'functions': FN, 'item_models': NS_TEX, 'font': FONT, 'font_range': [f'U+{CP_LO:04X}', f'U+{CP_HI:04X}'],
        'storage': f'{STO} fx.*', 'bossbar': BANNER_BAR,
        'owned': {'dirs': [f'{FDIR}/{d}' for d in OWNED_DIRS], 'files': [f'{FDIR}/{f}.mcfunction' for f in OWNED_FILES],
                  'rp': [f'assets/rlk/textures/{TEXDIR}', f'assets/rlk/models/item/{TEXDIR}', f'assets/rlk/items/{TEXDIR}',
                         f'assets/rlk/font/{FONT_NAME}.json', f'assets/rlk/textures/font/{FONT_NAME}']},
        'caps': {'fx': CAP, 'ambient_soft': SOFT, 'decals': 'never capped (flood: one card, re-timed)'},
        'objectives': [OBJ] + list(OBJECTIVES), 'fake_players': f'{", ".join(FAKE)} (objective {OBJ})',
        'tags': [TAG, f'{TAG}_c', f'{TAG}_d', f'{TAG}_fl', f'{TAG}_new', f'{TAG}_go', f'{TAG}_sh', f'{TAG}_fd', f'{TAG}_hit',
                 f'{TAG}_t', f'{TAG}_nf', ANIM, f'{ANIM}_w', f'{ANIM}_s', FOLLOW, LEAD, DEMO, f'{DEMO}_mv'],
        'floor': {'decal_y': DECAL_Y, 'decal_layers': [DECAL_Y, DECAL_Y + 0.003, DECAL_Y + 0.006],
                  'clamp_floor_storage': f'{STO} fx.fl (y x 100, default {FLOOR * 100})', 'arc_bearings': ARC_BEAR},
        'kinds': {k: {'plane': kind_info(k)[0], 'px': list(kind_info(k)[1]), 'extent': [r4(v) for v in kind_info(k)[2]],
                      'tint': 'neutral' if kind_info(k)[3] else 'painted', 'texture': kind_info(k)[4],
                      'source': 'own' if k in KINDS else 'fg kit (referenced)', 'desc': kind_info(k)[5]} for k in ALL_KINDS},
        'fg_references': {k: FG_TEX + v for k, v in REF.items()},
        'atlas_px_new': atlas_px(), 'atlas_budget': ATLAS_BUDGET,
        'presets': {k: {'args': v[1], 'doc': v[0], 'cards': preset_cards(k), 'c_split': v[4],
                        'ambient': k in AMBIENT, 'particles_only': k in PTCL} for k, v in PRESETS.items()},
        'props': {k: {'doc': v[0], 'kind': v[1], 'billboard': v[3], 'scale': list(v[4]), 'anim': v[5]} for k, v in PROPS.items()},
        'decals': {k: {'args': api.KIT_DECALS[k], 'doc': v} for k, v in DECALS.items()},
        'decal_flash': api.DECAL_FLASH,
        'sounds': {k: {'use': v[0], 'layers': [list(l) for l in v[1]]} for k, v in SOUNDS.items()},
        'hud': {k: list(v) for k, v in api.KIT_HUD.items()},
        'badge': {'glyph': f'U+{GLYPHS["badge"][0]:04X}', 'text': api.BADGE, 'component': badge_component()},
        'banner': {'text': api.BANNER, 'component': banner_component(), 'where': f'bossbar {BANNER_BAR}'},
        'lines': {str(k): {'text': v, 'steps': len(typed(v))} for k, v in api.LINES.items()},
        'glyphs': {k: f'U+{v[0]:04X}' for k, v in GLYPHS.items()},
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
    msg = (f'arlecchino fx kit: {n} functions ({removed} stale removed), {len(PRESETS)} presets, {len(PROPS)} props, '
           f'{len(DECALS)} decals, {len(SOUNDS)} sounds, {len(api.KIT_HUD)} hud calls, {len(api.LINES)} lines')
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error('--resourcepack is required unless --skip-rp')
        k, nref, px, g = build_resourcepack(a.resourcepack)
        msg += f', {k} sprites ({px / 1e6:.3f} M new px), {nref} fg references, {g} glyph in {FONT}'
    print(msg)


if __name__ == '__main__':
    main()
