#!/usr/bin/env python3
"""FX / audio / HUD kit of the special boss 타키 (Tachy, Stellar Blade).

The Apep kit's card engine (tools/build_mboss_ap_fx.py: the fg kit engine with its first-tick fix, counted pools, the
self-rescheduling ager, no shared-file hooks) copied and renamed, with the call list frozen in
tools/mboss_tachy/api.py §8 (KIT_PRESETS, KIT_PROPS, KIT_SOUNDS, KIT_HUD, KIT_FIXED; scratchpad tk/contract.md §3.3).
The module (S2 sequences, S3 core / melee, S4 aerial / mantle) calls it only through api.K; nothing here decides
gameplay (hits, hazards, projectiles, timings stay in the module). Tachy has no ground telegraphs (api.NO_DECALS), so
the kit has no fx/tele/** functions. Parts, all regenerated on every run:

  1. The tinted card engine: painted sprites on short-lived item_display cards (planes face, flat, cross, wave). Pools:
     fx cards (cap CAP; ambient presets skipped from SOFT live cards) and the mantle cocoon (rlk_tk_fx_coc: long-lived,
     never counted against the cap, replaced by every fx/p/cocoon call).
  2. Presets fx/p/<name> (macro args in tenths of a block / degrees / ticks / el 1 Pyro 3 Electro / c 1 amber 2 red
     3 gold / pct 0-100), prop looks fx/prop/<name> (@s = the projectile display), sound recipes fx/snd/<name>
     (vanilla events only, the mboss_lib.sound min-volume rule).
  3. The HUD: font rlk:mboss_tk (U+EA00-EAFF): the badge glyph and the mantle gauge cells; fx/hud/badge {el} (◈불 /
     ◈번개 / ◈외피 in the element colours on the boss-bar name line: storage rlk:mboss extra), fx/hud/gauge {pct}
     (20 gold cells after the badge), fx/hud/clear. The glyph root text is always empty and unstyled; the font ends
     with a reference to minecraft:default.
  4. In-game demos fx/test/<preset> (one per preset) on a vanilla stand-in (an armour stand with a netherite sword),
     fx/test/{sounds,props,hud,kinds,stage,stop}.

Generic glows are the field generator kit's sprites, referenced from our item models (no repaint): glow, mote, streak,
spark, dust, chunk. arrive_rift uses the dungeon rift's item models rlk:item/rift/{void,rim,arc_0..3} (stage S1) when
the resource pack has them, else this kit's own fallback card (tear + glow + sky arcs); the build never fails on it.

Outputs (owned; stale files in these places are removed):
  resource pack  assets/rlk/textures/mboss/tk_kit/<kind>.png      painted sprites (stdlib painter)
                 assets/rlk/models/item/mboss/tk_kit/<kind>.json    card models (tintindex 0)
                 assets/rlk/items/mboss/tk_kit/<kind>.json          item definitions, custom_model_data tint
                 assets/minecraft/atlases/items.json                adds rlk:mboss/tk_kit/* (merges)
                 assets/rlk/font/mboss_tk.json + textures/font/mboss_tk/*.png
  datapack       data/rlk/function/boss/tachy/fx/{card,cardx,look,clear,uninstall}
                 data/rlk/function/boss/tachy/fx/{e,p,tele,snd,hud,prop,test}/**
  manifest       tools/mboss_tk_fx_manifest.json   (its presence switches api.K on)

Cards carry rlk_tk_fx + rlk_room + rlk_mb_aux. Objectives tkFx (fake players) and tkFxS tkFxG tkFxH tkFxK tkFxD (the
card stage clock); storage rlk:tk fx.*; the module wires cleanup -> fx/clear + fx/hud/clear, pause / death_start ->
fx/clear, uninstall -> fx/uninstall (contract §3.3).

Run: python3 tools/build_mboss_tk_fx.py --resourcepack <unpacked RP>   (or --skip-rp: the datapack + manifest only)
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
import mboss_tk_fx_paint as P  # noqa: E402
import mboss_lib as L  # noqa: E402
from mboss_tachy import api  # noqa: E402

ROOT = api.ROOT                        # boss/tachy
FN = f'rlk:{ROOT}/fx/'
FDIR = f'data/rlk/function/{ROOT}/fx'
NS_TEX = 'rlk:mboss/tk_kit/'
TEXDIR = 'mboss/tk_kit'
FG_TEX = 'rlk:mboss/fg_kit/'
FG_TEXDIR = 'mboss/fg_kit'
RIFT_MODEL = 'rlk:item/rift/'          # S1's dungeon rift models (used by arrive_rift when present)
FONT = 'rlk:mboss_tk'
FONT_NAME = 'mboss_tk'
STO = 'rlk:tk'                         # kit keys: fx.* (contract §2)
CAP = 64            # live fx cards; further cards are skipped until some expire
SOFT = 40           # ambient presets are skipped from SOFT live fx cards on
ATLAS_BUDGET = 180_000                 # new px of the items atlas (contract §5: S1K <= 0.18 M)
OWNED_DIRS = ('e', 'p', 'tele', 'snd', 'hud', 'prop', 'test')
OWNED_FILES = tuple(api.KIT_FIXED)     # card cardx look clear uninstall
OBJ = 'tkFx'                           # the kit's fake players
OBJECTIVES = ('tkFxS', 'tkFxG', 'tkFxH', 'tkFxK', 'tkFxD')
TAG = api.TAGS['fx']                   # rlk_tk_fx
COC = f'{TAG}_coc'                     # the cocoon pool
DEMO = f'{TAG}_demo'
MANIFEST = HERE / 'mboss_tk_fx_manifest.json'
assert MANIFEST == api.KIT_MANIFEST


def rgb(h):
    return int(h[1:], 16)


# ----------------------------------------------------------------------------- colours (RGB ints for tints)
WHITE = 0xFFFFFF
PYRO = rgb('#FFA45A')          # warm-white flame sprites x this = the orange blade flame
PYRO_DEEP = rgb('#FF7A30')
ELECTRO = rgb('#FFF0B0')       # = the white-gold crackle
ELECTRO_DEEP = rgb('#F2C84A')
GOLD = rgb('#F5C842')
GOLD_PALE = rgb('#FFF2C0')
GOLD_WHITE = rgb('#FFF8DC')
AMBER = rgb('#FFAE3A')
RED_CORE = rgb('#FF3A24')
EMBER = rgb('#FF8A3D')
SAND = rgb('#D9B07A')
SAND_DARK = rgb('#A87E50')
ASH = rgb('#8C8580')
RIFT_RIM = rgb('#C9C0FF')
EL_TINT = {1: PYRO, 3: ELECTRO}
EL_DEEP = {1: PYRO_DEEP, 3: ELECTRO_DEEP}
CORE_C = {1: AMBER, 2: RED_CORE, 3: GOLD}

# ----------------------------------------------------------------------------- kinds
# name -> (plane, (w, h) px, card extent in blocks at scale 1 (a0, a1, b0, b1), painter box, painter, supersampling,
#          neutral?, description). Planes: face (x-y quad), flat (x-z quad, +b forward), cross (two vertical quads),
#          wave (a face quad and a flat quad with the same texture: the W1 crescent from the front and from above).
SQ = (-0.5, 0.5, -0.5, 0.5)
BX = (-1, 1, -1, 1)
UNIT = (-1, 1, -1, 1)
ARC = (-1, 1, 0, 1)
NARROW = (-0.25, 0.25, -0.5, 0.5)
HANG = (-0.25, 0.25, -1.0, 0.0)
FOOT_N = (-0.25, 0.25, 0.0, 1.0)
COCOON = (-0.5, 0.5, -1.0, 1.0)
TEAR = (-1 / 3, 1 / 3, -0.5, 0.5)
KINDS = {
    # slash arcs: four sweep frames + the Electro crackle (flat, unit radius = the reach at scale r, +b = the aim)
    **{f'arc_{k}': ('flat', (128, 64), ARC, ARC, P.make_arc(k), 2, True,
                    f'slash-arc sweep frame {k} (flame band on r 0.8, head at {int(P.ARC_F[k] * 100)} % of the sweep)')
       for k in range(4)},
    'arc_e':        ('flat', (128, 64), ARC, ARC, P.paint_arc_e, 2, True, 'Electro crackle filaments along the slash arc'),
    # projectiles
    'crescent_h':   ('wave', (128, 32), SQ, SQ, P.paint_crescent_h, 2, True, 'W1 ground crescent (front + top quads)'),
    'crescent_v':   ('cross', (32, 128), SQ, SQ, P.paint_crescent_v, 2, True, 'W2 upright air crescent (crossed quads)'),
    # rings
    'spin_ring':    ('flat', (128, 128), UNIT, UNIT, P.paint_spin_ring, 2, True, 'C1 spin fire ring (unit radius)'),
    'shock_ring':   ('flat', (128, 128), UNIT, UNIT, P.paint_shock_ring, 2, True, 'L / nova golden shock ring (unit radius)'),
    # lightning
    'bolt_0':       ('cross', (32, 128), FOOT_N, FOOT_N, P.make_bolt(41), 2, True, 'golden lightning bolt, strike at b 0, 1 b tall'),
    'bolt_1':       ('cross', (32, 128), FOOT_N, FOOT_N, P.make_bolt(57), 2, True, 'golden lightning bolt (variant)'),
    **{f'sky_arc_{k}': ('face', (32, 64), HANG, HANG, P.make_sky_arc(70 + k), 2, True,
                        f'thin golden arc hanging from b 0 down to b -1 (variant {k})') for k in range(4)},
    # glints, flares
    'glint_star':   ('face', (64, 64), SQ, BX, P.paint_glint_star, 2, True, 'the blade glint: gold 4-point star with a ring'),
    'core_flare':   ('face', (64, 64), SQ, BX, P.paint_core_flare, 2, True, 'chest core / visor flare burst (tinted)'),
    # mantle
    'cocoon':       ('face', (64, 128), COCOON, COCOON, P.paint_cocoon, 2, False, 'the overload mantle: wings wrapped into a cocoon'),
    'cocoon_crack': ('face', (64, 128), COCOON, COCOON, P.paint_cocoon_crack, 2, True, 'cracks of light over the cocoon'),
    # flecks
    'feather':      ('face', (32, 64), NARROW, NARROW, P.paint_feather, 2, False, 'black metallic blade-feather, gold edge'),
    'feather_glow': ('face', (32, 64), NARROW, NARROW, P.paint_feather_glow, 2, False, 'glowing gold-white feather (mantle feathers)'),
    'ember':        ('face', (32, 32), SQ, BX, P.paint_ember, 3, True, 'glowing ember fleck (tinted)'),
    'ash':          ('face', (32, 32), SQ, BX, P.paint_ash, 3, False, 'grey-black ash flake with a dim ember edge'),
    'flame':        ('face', (32, 64), FOOT_N, FOOT_N, P.paint_flame, 2, True, 'flame tongue, root at b 0 (tinted)'),
    # the arrival tear fallback, the gate icon
    'tear':         ('face', (64, 96), TEAR, TEAR, P.paint_tear, 2, False, 'arrival tear fallback (void lens, pale rim)'),
    'gate_icon':    ('face', (64, 64), SQ, BX, P.paint_gate_icon, 2, False, 'gate label icon: the long sword behind the visor skull'),
}
# Generic kinds referenced from the fg kit (our item model points at the fg texture; no px of our own).
REF = {'glow': 'glow', 'mote': 'mote', 'streak': 'streak', 'spark': 'spark', 'dust': 'dust', 'chunk': 'chunk'}
REF_NEUTRAL = ('glow', 'mote', 'streak')
# The arrival tear: S1's rift models when the pack has them, else (fallback) our own textures with these planes.
RIFT = {'rift_void': ('void', 'tear', 'face'), 'rift_rim': ('rim', 'glow', 'face'),
        **{f'rift_arc{k}': (f'arc_{k}', f'sky_arc_{k}', 'face') for k in range(4)}}
ALL_KINDS = list(KINDS) + list(REF) + list(RIFT)
SPIN_Y = ('flat', 'cross', 'wave')     # planes that spin about local y


def _fg():
    import build_mboss_fg_fx as FG
    return FG


def kind_info(kind):
    """(plane, (w, h), extent, neutral, texture id, description) of an own, referenced or rift kind (rift: the
    fallback look)"""
    if kind in KINDS:
        v = KINDS[kind]
        return v[0], v[1], v[2], v[6], NS_TEX + kind, v[7]
    if kind in RIFT:
        s1name, fb, plane = RIFT[kind]
        if fb in KINDS:
            v = KINDS[fb]
            ext = TEAR if fb == 'tear' else v[2]
            return plane, v[1], ext, v[6], NS_TEX + fb, f'arrival tear part (S1 rift/{s1name}, fallback {fb})'
        fgk = _fg().KINDS[REF[fb]]
        return plane, fgk[1], (-0.5, 0.5, -0.5, 0.5), True, FG_TEX + REF[fb], f'arrival tear part (S1 rift/{s1name}, fallback {fb})'
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
    m = (8 - 16 px, 8 + 16 py, 8 - 16 pz); card +a = local -x = model +x)."""
    plane, _s, (a0, a1, b0, b1), _n, tex, _d = kind_info(kind)
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1

    def q(frm, to, faces):
        return {'from': [r4(v) for v in frm], 'to': [r4(v) for v in to], 'shade': False, 'faces': faces}

    def f(uv):
        return {'uv': uv, 'texture': '#0', 'tintindex': 0}
    face = q([x0, 8 + 16 * b0, 8], [x1, 8 + 16 * b1, 8], {'south': f([0, 0, 16, 16]), 'north': f([16, 0, 0, 16])})
    flat = q([x0, 8, 8 - 16 * b1], [x1, 8, 8 - 16 * b0], {'up': f([0, 0, 16, 16]), 'down': f([0, 16, 16, 0])})
    if plane == 'face':
        els = [face]
    elif plane == 'flat':
        els = [flat]
    elif plane == 'wave':
        els = [face, flat]
    elif plane == 'cross':
        els = [face, q([8, 8 + 16 * b0, 8 - 16 * a1], [8, 8 + 16 * b1, 8 - 16 * a0],
                       {'east': f([0, 0, 16, 16]), 'west': f([16, 0, 0, 16])})]
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
    """new px this kit adds to the items atlas (its own painted kinds; the fg and rift references add nothing)"""
    return sum(v[1][0] * v[1][1] for v in KINDS.values())


def rift_models_present(rp):
    """True when the resource pack holds all of S1's rift item models that arrive_rift uses"""
    rp = Path(rp)
    return all((rp / f'assets/rlk/models/item/rift/{RIFT[k][0]}.json').exists() for k in RIFT)


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
CP_LO, CP_HI = 0xEA00, 0xEAFF
# name -> (codepoint, painter: analytic fn (x right, y up, -1..1) | ('pix', fn, arg), texture px (w, h), height, ascent)
GLYPHS = {
    'badge': (0xEA00, P.glyph_badge, (36, 36), 8, 7),
    'g0':    (0xEA30, ('pix', P.pixel_cell, 0), (4, 8), 8, 7),
    'g1':    (0xEA31, ('pix', P.pixel_cell, 1), (4, 8), 8, 7),
    'g_l':   (0xEA32, ('pix', P.pixel_cell, 2), (4, 8), 8, 7),
    'g_r':   (0xEA33, ('pix', P.pixel_cell, 3), (4, 8), 8, 7),
}
SPACES = {0xEAF0: -1, 0xEAF1: 2, 0xEAF2: 1}
SP_NEG1 = chr(0xEAF0)
GAUGE_CELLS = 20
BADGES = {api.PYRO: ('불', api.EL_HEX[api.PYRO]), api.ELECTRO: ('번개', api.EL_HEX[api.ELECTRO]), 9: ('외피', '#FFD86B')}


def glyph(name):
    return chr(GLYPHS[name][0])


def badge(el):
    """The boss-bar name-line badge "◈불" / "◈번개" / "◈외피" as an SNBT text component: the root text is empty and
    unstyled; the glyph sibling carries the kit font, the name is a plain sibling (no font inheritance)."""
    name, col = BADGES[el]
    return (f'{{text:"",extra:[{{text:"  "}},{{text:"{glyph("badge")}",font:"{FONT}",color:"{col}"}},'
            f'{{text:"{name}",color:"{col}",bold:true}}]}}')


def gauge_text(n, cells=GAUGE_CELLS):
    return glyph('g_l') + glyph('g1') * n + glyph('g0') * (cells - n) + glyph('g_r')


def gauge(pct):
    """The mantle gauge component for pct (0..100): 20 cells, n = pct // 5 gold (root empty and unstyled)."""
    n = max(0, min(GAUGE_CELLS, int(pct) * GAUGE_CELLS // 100))
    return f'{{text:"",extra:[{{text:" "}},{{text:"{gauge_text(n)}",font:"{FONT}",color:"white"}}]}}'


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


def glyph_raw(name):
    cp, painter, (w, h), _height, _ascent = GLYPHS[name]
    if callable(painter):
        return w, h, bytes(paint_glyph(painter, w, h))
    pw, ph, rows = painter[1](painter[2])
    assert (pw, ph) == (w, h), name
    raw = bytearray()
    for row in rows:
        for r, g, b, a in row:
            raw += bytes((round(r * 255), round(g * 255), round(b * 255), round(a * 255))) if a > 0 else b'\0\0\0\0'
    return w, h, bytes(raw)


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
    ours = [g[0] for g in GLYPHS.values()] + list(SPACES)
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
    for name, (cp, _painter, (w, h), height, ascent) in GLYPHS.items():
        gw, gh, raw = glyph_raw(name)
        rows = b''.join(b'\x00' + raw[y * gw * 4:(y + 1) * gw * 4] for y in range(gh))
        data = png_bytes(gw, gh, rows)
        p = tex / f'{name}.png'
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
        providers.append({'type': 'bitmap', 'file': f'rlk:font/{FONT_NAME}/{name}.png', 'ascent': ascent,
                          'height': height, 'chars': [chr(cp)]})
    providers.append({'type': 'space', 'advances': {chr(k): v for k, v in SPACES.items()}})
    # every char the kit does not draw falls back to the default font (a component that inherits this font by mistake
    # still shows its text)
    providers.append({'type': 'reference', 'id': 'minecraft:default'})
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
    s1 = rift_models_present(rp)
    root = rp / 'assets/rlk'
    tex_dir = root / f'textures/{TEXDIR}'
    model_kinds = [k for k in ALL_KINDS if not (s1 and k in RIFT)]
    dirs = {tex_dir: (KINDS, '.png'), root / f'models/item/{TEXDIR}': (model_kinds, '.json'),
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
    for kind in model_kinds:
        put(root / f'models/item/{TEXDIR}' / f'{kind}.json', model_json(kind))
    for kind in ALL_KINDS:
        model = RIFT_MODEL + RIFT[kind][0] if (s1 and kind in RIFT) else None
        put(root / f'items/{TEXDIR}' / f'{kind}.json', item_json(kind, model))
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
    return len(KINDS), n_ref, px, n_glyphs, s1


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


def card(kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8, fade=0,
         col=WHITE, dly=0, dur=0, hit=-1, col2=-1, off=None, pool=None):
    """The function line that spawns one card (fx/card, or fx/cardx when an extended option is used): pos / rot of the
    card (relative to the executor), billboard, roll (left_rotation about local z), spin over the main interpolation,
    s0 -> s1 (float or (x, y, z)), off (static start translation) + move, life / fade ticks, col tint, dly hidden ticks,
    dur main-interpolation ticks (0 = to the fade), hit / col2 the second tint, pool 'coc' = the cocoon pool. Any value
    may be a macro placeholder string such as '$(r)'."""
    assert kind in ALL_KINDS, kind
    assert bb in ('fixed', 'center', 'vertical', 'horizontal'), bb
    if all(isinstance(v, int) for v in (life, fade, dur)) and dur > life - fade - 1:
        life = dur + fade + 1              # the main interpolation always completes before the fade starts
    uni = (int, float, str)
    simple = (isinstance(s0, uni) and isinstance(s1, uni) and not dly and not dur and hit == -1 and off is None
              and pool is None)
    if off is not None and all(isinstance(x, (int, float)) for x in tuple(off) + tuple(move)):
        end = tuple(a + b for a, b in zip(off, move))
    else:
        end = tuple(move)
    mv = vec(end)
    if simple:
        return (f'function {FN}card {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
                f'spin:{_i(spin)},s0:{_f(s0)},s1:{_f(s1)},move:"{mv}",life:{_i(life)},'
                f'fade:{_i(fade)},col:{_i(col)}}}')
    tg = COC if pool == 'coc' else f'{TAG}_c'
    return (f'function {FN}cardx {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",roll:{_i(roll)},'
            f'spin:{_i(spin)},s0:"{vec(s0)}",s1:"{vec(s1)}",off:"{vec(off if off is not None else (0, 0, 0))}",'
            f'move:"{mv}",life:{_i(life)},fade:{_i(fade)},col:{_i(col)},dly:{_i(dly)},dur:{_i(dur)},hit:{_i(hit)},'
            f'col2:{_i(col2)},tg:"{tg}"}}')


def fx(name, **args):
    """A preset call line (fx/p/<name>), args as api.KIT_PRESETS (ints: tenths / degrees / ticks / el / c / pct)."""
    assert name in PRESETS, name
    need = PRESETS[name][1]
    assert sorted(args) == sorted(need), (name, sorted(args), need)
    if not need:
        return f'function {FN}p/{name}'
    return f'function {FN}p/{name} {{' + ','.join(f'{k}:{args[k] if isinstance(args[k], str) else int(args[k])}'
                                                  for k in need) + '}'


def snd(name):
    assert name in SOUNDS, name        # api.KIT_SOUNDS + EXTRA_SOUNDS
    return f'function {FN}snd/{name}'


def prop(name):
    assert name in PROPS, name
    return f'function {FN}prop/{name}'


def hud(name, **args):
    assert name in api.KIT_HUD and sorted(args) == sorted(api.KIT_HUD[name]), name
    if not args:
        return f'function {FN}hud/{name}'
    return f'function {FN}hud/{name} {{' + ','.join(f'{k}:{int(v)}' for k, v in args.items()) + '}'


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


def fdust(block, pos='~ ~ ~', delta=(0, 0, 0), n=1):
    return part(f'falling_dust{{block_state:"minecraft:{block}"}}', pos, delta, 0.0, n)


def el_parts(el, pos='~ ~ ~', delta=(0.3, 0.3, 0.3), n=8):
    """the element's particle signature: Pyro flame + small flame, Electro electric sparks + gold dust"""
    if el == api.PYRO:
        return [part('flame', pos, delta, 0.03, n), part('small_flame', pos, delta, 0.02, max(1, n // 2))]
    return [part('electric_spark', pos, delta, 0.15, n), dust(GOLD, 0.9, pos, delta, max(1, n // 2))]


# ----------------------------------------------------------------------------- sound recipes (PLAN §3-§5)
# name -> (use, [(event, volume, pitch), ...]); one tick each, vanilla events only (checked against the game's sound
# list when scratchpad rd/tests/sound_ids.txt is present).
SOUNDS = {
    # intro / sequences (PLAN §3)
    'hang_amb':     ('E0 t0: the hanging cocoon nest.', [('ambient.basalt_deltas.mood', 0.5, 1.0)]),
    'chain_step':   ('E0 t10 / t22: the cables creak.', [('block.chain.step', 0.4, 1.0)]),
    'cable_snap':   ('E1 t30 / 33 / 36: a cable snaps (the caller varies nothing; three calls).',
                     [('block.chain.break', 0.9, 0.7), ('item.lead.break', 0.6, 0.8)]),
    'body_land':    ('E1 t42: she lands prone.', [('entity.iron_golem.damage', 0.6, 1.0), ('block.anvil.land', 0.5, 0.6)]),
    'heartbeat':    ('E2 t48 / t56: the ring lights pulse.', [('entity.warden.heartbeat', 0.7, 1.0)]),
    'servo':        ('E3 t62: the push up.', [('block.piston.extend', 0.5, 0.6)]),
    'armor':        ('E3 t74: armour plates settle.', [('item.armor.equip_netherite', 0.6, 1.0)]),
    'bulb':         ('E4 t96: the armour lights.', [('block.copper_bulb.turn_on', 0.4, 0.6)]),
    'cape_gust':    ('E5 t108: the cape flares (the caller may stop it at 116: stopsound @a hostile item.elytra.flying).',
                     [('item.elytra.flying', 0.5, 1.2)]),
    'hair':         ('E6 t116: the hair sweep.', [('item.armor.equip_leather', 0.5, 1.0)]),
    'visor_close':  ('E7 t126: the helmet slides down over the face.',
                     [('block.iron_trapdoor.close', 0.7, 0.7), ('block.respawn_anchor.charge', 0.5, 1.0)]),
    'skull_ignite': ('E8 t136: the visor skull lights.', [('block.beacon.activate', 0.6, 1.4), ('entity.blaze.ambient', 0.4, 1.0)]),
    'sword_draw':   ('E9 t142: the sword is drawn.', [('item.trident.return', 0.6, 0.8), ('entity.player.attack.sweep', 0.5, 1.0)]),
    'blade_ignite': ('E10 t156: the edge ignites.', [('item.firecharge.use', 0.8, 1.0), ('block.fire.ambient', 0.6, 1.0),
                                                     ('entity.blaze.shoot', 0.5, 1.0)]),
    'stance':       ('E11 t170: the combat stance.', [('entity.wither.ambient', 0.3, 1.6)]),
    't1_split':     ('T1 t10: the cape panels split.', [('item.armor.equip_elytra', 0.8, 0.8),
                                                         ('block.amethyst_cluster.break', 0.5, 0.8)]),
    't1_flare':     ('T1 t50: the wings flare gold.', [('block.beacon.power_select', 0.7, 1.2), ('item.firecharge.use', 0.6, 0.8)]),
    't2_flare':     ('T2 t20: the visor flares red.', [('entity.warden.sonic_charge', 0.6, 1.4),
                                                        ('block.respawn_anchor.set_spawn', 0.6, 0.7)]),
    't2_dark':      ('T2 t50: the dark falls (blindness, the abyss look).', [('block.beacon.deactivate', 0.8, 0.5),
                                                                              ('block.respawn_anchor.deplete', 0.7, 0.6)]),
    'death_knee':   ('Death t20: the knees buckle.', [('entity.iron_golem.damage', 0.6, 0.6), ('item.armor.equip_netherite', 0.5, 0.7)]),
    'death_ash':    ('Death t116: she dissolves into ash.', [('block.sand.break', 0.7, 0.7), ('block.fire.extinguish', 0.5, 0.6),
                                                             ('block.soul_sand.break', 0.6, 0.8)]),
    'arrive_rift':  ('Arrival: the tear closes behind the player.', [('block.end_portal_frame.fill', 0.6, 0.7),
                                                                     ('block.respawn_anchor.deplete', 0.6, 1.0)]),
    # fight (PLAN §4-§5)
    'flare_tell':   ('A1 / C3 t0: the chest + visor flare.', [('entity.ravager.roar', 0.4, 1.8), ('item.firecharge.use', 0.5, 1.0)]),
    'dash':         ('A1 / B3 / C thrust dashes.', [('entity.player.attack.sweep', 0.6, 0.6), ('item.trident.riptide_1', 0.6, 1.2)]),
    'slash_light':  ('T1 slashes.', [('entity.player.attack.sweep', 0.7, 1.2), ('entity.blaze.shoot', 0.3, 1.6)]),
    'slash_heavy':  ('T2 / T3 slashes.', [('entity.player.attack.sweep', 0.9, 0.8), ('item.firecharge.use', 0.5, 0.8),
                                          ('entity.generic.explode', 0.4, 1.6)]),
    'spin':         ('C1 h2: the spin.', [('entity.player.attack.sweep', 0.8, 0.7), ('item.trident.riptide_2', 0.6, 1.0),
                                          ('block.fire.ambient', 0.6, 1.4)]),
    'chop':         ('B3 bangs ("펑").', [('entity.generic.explode', 0.7, 1.2), ('block.anvil.land', 0.4, 1.2),
                                          ('entity.player.attack.crit', 0.8, 0.8)]),
    'glint':        ('C / K glint.', [('block.amethyst_block.resonate', 0.8, 1.6), ('item.trident.return', 0.6, 1.2)]),
    'thrust':       ('C / K thrust.', [('item.trident.throw', 0.9, 0.7), ('entity.player.attack.knockback', 0.8, 0.8)]),
    'blink_out':    ('K vanish.', [('entity.enderman.teleport', 0.6, 0.6)]),
    'blink_in':     ('K reappear.', [('entity.enderman.teleport', 0.6, 0.9), ('block.amethyst_block.chime', 0.6, 1.4)]),
    'leap':         ('K / W2 / L leaps.', [('entity.breeze.jump', 0.7, 0.8), ('entity.phantom.flap', 0.6, 0.8)]),
    'sky_arcs':     ('K: the sky arcs crawl down.', [('block.respawn_anchor.charge', 0.6, 1.6), ('item.trident.thunder', 0.5, 1.6)]),
    'plunge':       ('K plunge hit.', [('entity.lightning_bolt.impact', 1.0, 1.0), ('entity.generic.explode', 0.7, 0.9),
                                       ('block.anvil.land', 0.5, 0.6)]),
    'charge_core':  ('B3 t0: the core charge.', [('entity.warden.sonic_charge', 0.5, 1.3)]),
    'wave_release': ('W1 waves.', [('entity.player.attack.sweep', 0.9, 0.6), ('item.firecharge.use', 0.7, 0.7),
                                   ('entity.blaze.shoot', 0.6, 0.8)]),
    'wave_hit':     ('W1 / W2 crescent impact.', [('entity.generic.explode', 0.5, 1.4)]),
    'air_swoop':    ('W2 pull back.', [('entity.phantom.swoop', 0.7, 1.0)]),
    'dive':         ('W2 / L dive.', [('entity.phantom.swoop', 0.8, 0.7), ('item.trident.riptide_3', 0.6, 0.9)]),
    'shock':        ('L shock.', [('entity.lightning_bolt.impact', 1.0, 1.0), ('entity.generic.explode', 0.6, 1.0)]),
    'high_glint':   ('L high hover glints (every 30 t).', [('entity.phantom.flap', 0.4, 1.0), ('block.amethyst_block.chime', 0.4, 1.6)]),
    'swap_pyro':    ('G1 swap to Pyro.', [('item.firecharge.use', 0.7, 1.0), ('block.fire.extinguish', 0.5, 1.2)]),
    'swap_electro': ('G1 swap to Electro.', [('entity.lightning_bolt.impact', 0.4, 1.8), ('block.respawn_anchor.charge', 0.6, 1.2)]),
    'mantle_wrap':  ('G2 mantle_in.', [('item.elytra.flying', 0.5, 1.4), ('block.beacon.ambient', 0.6, 1.6),
                                       ('item.armor.equip_elytra', 0.6, 0.8)]),
    'mantle_break': ('G2 break.', [('block.glass.break', 1.0, 0.7), ('entity.zombie_villager.cure', 0.5, 0.6)]),
    'nova_swell':   ('G2 nova swell.', [('block.beacon.power_select', 0.7, 1.0), ('entity.warden.sonic_charge', 0.7, 1.0)]),
    'nova_blast':   ('G2 nova hit.', [('entity.generic.explode', 1.0, 0.8), ('entity.lightning_bolt.impact', 0.8, 1.2),
                                      ('block.beacon.deactivate', 0.6, 0.6)]),
    'feather_fall': ('Mantle feathers (each).', [('entity.phantom.flap', 0.4, 1.6), ('block.amethyst_block.chime', 0.4, 1.8)]),
    'core_backfire': ('G3 backfire.', [('entity.generic.explode', 0.9, 0.9), ('entity.blaze.hurt', 0.7, 0.6)]),
    'stagger':      ('Stagger.', [('entity.iron_golem.damage', 0.6, 0.8), ('item.armor.equip_netherite', 0.4, 0.6)]),
    'step':         ('Armoured footstep (walk events).', [('block.chain.step', 0.4, 0.8), ('entity.iron_golem.step', 0.3, 1.4)]),
    # S4's R3 (request S:tk/requests/s1k.md K1; in api.KIT_SOUNDS since I1)
    'wave_charge':  ('W1 t0-40: the gold glow grows along the edge (S4 R3).', [('block.beacon.ambient', 0.6, 1.8),
                                                                              ('block.respawn_anchor.charge', 0.6, 1.0)]),
}
EXTRA_SOUNDS = ()                                  # names beyond api.KIT_SOUNDS (none since I1)
assert set(SOUNDS) == set(api.KIT_SOUNDS) | set(EXTRA_SOUNDS), set(SOUNDS) ^ set(api.KIT_SOUNDS)
DEATH_SOUNDS = ('death_knee', 'death_ash')
VOICE_EVENTS = ('entity.warden.', 'entity.ravager.', 'entity.blaze.ambient', 'entity.blaze.hurt', 'entity.wither.',
                'entity.zombie_villager.')
SOUND_IDS = HERE.parents[1] / 'sound_ids.txt'     # never present in the tree; tests use scratchpad rd/tests


def sound_line(event, vol, pitch):
    return L.sound(event, vol, pitch)


# ----------------------------------------------------------------------------- presets (api.KIT_PRESETS)
# name -> (doc, args, fn, conv, ambient, particles_only). A preset with arguments is a public macro p/<name> that turns
# its arguments into storage rlk:tk fx.pa (conv: [(key, arg, scale or None (int x 1), add)]) and runs p/e/<name>[_<el>]
# with that storage.
PRESETS = {}
AMBIENT = ('ambient_dust',)
PTCL = ('ambient_dust',)
PA = f'{STO} fx.pa'


def preset(name, doc, conv=(), split_el=False):
    args = api.KIT_PRESETS[name]

    def deco(f):
        PRESETS[name] = (doc, list(args), f, list(conv), split_el)
        return f
    return deco


def ang(deg):
    return num(float(deg), 2)


def radial(n, start=0.0):
    return [start + 360.0 * k / n for k in range(n)]


def xz(r, yaw):
    """^x ^z offsets of the point at radius r, yaw degrees to the executor's right"""
    return -r * math.sin(math.radians(yaw)), r * math.cos(math.radians(yaw))


def fly(kind, yaw, el, dist, h=0.0, s0=0.5, s1=1.0, life=8, fade=3, col=WHITE, dly=0, roll=0, dur=0):
    """the fg radial trick: a fixed face card whose local +y points out along (yaw, elevation) flies dist outward"""
    return card(kind, f'~ ~{num(h, 2)} ~', f'~{ang(yaw)} {ang(90 - el)}', roll=roll, s0=s0, s1=s1,
                move=(0, dist if isinstance(dist, str) else round(dist, 2), 0), life=life, fade=fade, col=col, dly=dly,
                dur=dur)


def mac(line):
    return '$' + line


RND = random.Random


# --- blade arcs and trails -------------------------------------------------------------------------------------------
ARC_LIFE = (2, 2, 2, 8)


@preset('slash_arc', 'A slash arc of reach {r} (tenths) about the executor (the chest pivot, S3: at the body + 1.2, '
        'rotated as the body): {yaw} / {pitch} offsets of the aim from the executor rotation, {roll} the blade plane '
        'about the aim (0 horizontal, +-35 diagonal, 90 vertical, 175 backhand: the sweep reversed). Four sweep frames '
        '(1 tick apart, the last one fading over 8 t), el 1 orange flame / el 3 white-gold with a crackle overlay; flame '
        'or spark particles at the arc\'s front.', conv=(('s', 'r', 0.1), ('s9', 'r', 0.09), ('f', 'r', 0.08),
                                                         ('pd', 'r', 0.025)), split_el=True)
def _p_slash_arc(el):
    out = []
    for k in range(4):
        out.append(mac(card(f'arc_{k}', '^ ^ ^', '~$(yaw) ~$(pitch)', roll='$(roll)', s0=('$(s9)', 1, '$(s9)'),
                            s1=('$(s)', 1, '$(s)'), life=ARC_LIFE[k], fade=4 if k == 3 else 0, dly=k, dur=2,
                            col=EL_TINT[el], hit=k + 3 if k == 3 else -1, col2=EL_DEEP[el] if k == 3 else -1)))
    if el == api.ELECTRO:
        out.append(mac(card('arc_e', '^ ^ ^', '~$(yaw) ~$(pitch)', roll='$(roll)', s0=('$(s)', 1, '$(s)'),
                            s1=('$(s)', 1, '$(s)'), life=6, fade=3, dly=2, dur=1, col=GOLD_WHITE)))
    front = 'rotated ~$(yaw) ~$(pitch) positioned ^ ^ ^$(f)'
    if el == api.PYRO:
        out += [mac(f'execute {front} run ' + part('flame', '~ ~ ~', ('$(pd)', 0.25, '$(pd)'), 0.04, 14)),
                mac(f'execute {front} run ' + part('small_flame', '~ ~ ~', ('$(pd)', 0.3, '$(pd)'), 0.03, 8)),
                mac(f'execute {front} run ' + part('lava', '~ ~ ~', (0.3, 0.2, 0.3), 0, 1))]
    else:
        out += [mac(f'execute {front} run ' + part('electric_spark', '~ ~ ~', ('$(pd)', 0.25, '$(pd)'), 0.2, 14)),
                mac(f'execute {front} run ' + dust(GOLD_PALE, 1.0, '~ ~ ~', ('$(pd)', 0.25, '$(pd)'), 8))]
    return out


def _trail(el, ground):
    """the shared body of dash_trail / thrust_trail: crossed ribbons along +z over len, element particles at 1/4..4/4"""
    y = -0.85 if ground else 0.0
    w = 18 if ground else 12
    out = [mac(card('streak', f'^ ^{num(y + 0.1, 2)} ^$(h)', '~90 0', s0=('$(l)', w * 2.4, 1), s1=('$(l)', w * 3.0, 1),
                    life=7, fade=4, dur=2, col=EL_DEEP[el])),
           mac(card('streak', f'^ ^{num(y, 2)} ^$(h)', '~90 0', s0=('$(l)', w * 0.6, 1), s1=('$(l)', w, 1), life=8,
                    fade=5, dur=3, col=EL_TINT[el])),
           mac(card('streak', f'^ ^{num(y + 0.05, 2)} ^$(h)', '~90 90', s0=('$(l)', w * 0.6, 1), s1=('$(l)', w, 1),
                    life=8, fade=5, dur=3, col=EL_TINT[el])),
           mac(card('glow', f'^ ^{num(y + 0.6, 2)} ^$(l)', bb='center', s0=0.6, s1=2.2, life=6, fade=3, col=EL_TINT[el]))]
    for k in range(1, 5):
        p = f'^ ^{num(y + 0.3, 2)} ^$(p{k})'
        if ground:
            out.append(mac(card('flame', f'^ ^{num(y, 2)} ^$(p{k})', bb='vertical', s0=(0.6, 0.3, 0.6),
                                s1=(1.1, 1.6, 1.1), life=10, fade=5, dly=k - 1, dur=4, col=EL_TINT[el])))
        out += [mac(l) for l in el_parts(el, p, (0.25, 0.2, 0.25), 6)]
    if ground:
        out.append(mac(blockp('sand', f'^ ^{num(y + 0.1, 2)} ^$(h)', (0.4, 0.1, '$(q)'), 0.1, 12)))
    return out


TRAIL_CONV = (('l', 'len', 0.1), ('h', 'len', 0.05), ('q', 'len', 0.03), ('p1', 'len', 0.025), ('p2', 'len', 0.05),
              ('p3', 'len', 0.075), ('p4', 'len', 0.1))


@preset('thrust_trail', 'The thrust streak along the aim over {len} (tenths) from the executor (S3: the body + 1.0, '
        'rotated as the body): two crossed ribbons, a glow at the end, element particles along it.', conv=TRAIL_CONV,
        split_el=True)
def _p_thrust_trail(el):
    return _trail(el, False)


@preset('dash_trail', 'The fire trail of a dash along the aim over {len} (tenths) from the executor (S3: the body + 1.0): '
        'wide crossed ribbons at the feet, four flame tongues revealed in turn, sand kicked up, element particles.',
        conv=TRAIL_CONV, split_el=True)
def _p_dash_trail(el):
    return _trail(el, True)


@preset('spin_ring', 'The C1 spin: a full ring of fire of radius {r} (tenths) about the executor (S3: the body + 1.0), '
        'two counter-turning rings, embers thrown out; el 3 gold with sparks.',
        conv=(('s', 'r', 0.1), ('s5', 'r', 0.05), ('s9', 'r', 0.09), ('pd', 'r', 0.06)), split_el=True)
def _p_spin_ring(el):
    out = [mac(card('spin_ring', '^ ^ ^', '~ 0', spin=170, s0=('$(s5)', 1, '$(s5)'), s1=('$(s)', 1, '$(s)'), life=9,
                    fade=4, dur=5, col=EL_TINT[el])),
           mac(card('spin_ring', '^ ^0.25 ^', '~60 0', spin=-150, s0=('$(s5)', 1, '$(s5)'), s1=('$(s9)', 1, '$(s9)'),
                    life=8, fade=4, dly=1, dur=4, col=EL_DEEP[el]))]
    for k, yaw in enumerate(radial(6, 20)):
        out.append(fly('ember', yaw, 15, 2.6, h=0.1, s0=0.25, s1=0.4, life=9, fade=4, col=EL_TINT[el], dly=1))
    out += [mac(l) for l in el_parts(el, '~ ~ ~', ('$(pd)', 0.15, '$(pd)'), 24)]
    return out


@preset('glint', 'The gold glint on the blade before the thrust (C / K): a spinning 4-point star with a ring and a '
        'glow, 0.4 b right / 1.4 b ahead of the executor (S3: the body + 1.6, rotated as the body).')
def _p_glint():
    return [card('glint_star', '^-0.4 ^ ^1.4', bb='center', spin=90, s0=0.3, s1=2.4, life=10, fade=5, dur=4, col=GOLD),
            card('glow', '^-0.4 ^ ^1.4', bb='center', s0=0.4, s1=1.8, life=9, fade=5, col=GOLD),
            dust(GOLD_PALE, 1.2, '^-0.4 ^ ^1.4', (0.15, 0.15, 0.15), 6), part('wax_on', '^-0.4 ^ ^1.4', (0.2, 0.2, 0.2), 0, 3)]


@preset('high_glint', 'The L high hover glint (every 30 t): a big gold star at the executor (the hovering body, '
        '13 b up) readable from the floor.')
def _p_high_glint():
    return [card('glint_star', bb='center', spin=120, s0=0.8, s1=4.6, life=10, fade=4, dur=4, col=GOLD),
            card('glow', bb='center', s0=1.4, s1=4.2, life=9, fade=4, col=GOLD),
            dust(GOLD, 1.4, '~ ~ ~', (0.3, 0.3, 0.3), 6)]


@preset('core_flare', 'The chest core + visor flare tell (A1 / B3 / C3; G3 windows): c 1 amber, 2 red, 3 gold. At the '
        'chest (S3: the body + 1.5, rotated as the body): a pulsing burst on the chest plate and a smaller one on the '
        'visor, ~20 t.', conv=(('c', 'c', None),))
def _p_core_flare():
    return ['# (the public part stores the tint in pa.col from {c})',
            mac(card('core_flare', '^ ^ ^0.3', bb='center', spin=40, s0=0.5, s1=2.1, life=20, fade=6, dur=10, col='$(col)')),
            mac(card('glow', '^ ^ ^0.3', bb='center', s0=0.8, s1=2.4, life=22, fade=8, col='$(col)')),
            mac(card('core_flare', '^ ^0.55 ^0.25', bb='center', spin=-60, s0=0.2, s1=0.8, life=16, fade=5, dly=2,
                     dur=8, col='$(col)')),
            mac(card('glow', '^ ^ ^0.3', bb='center', s0=1.4, s1=0.8, life=10, fade=4, dly=10, col='$(col)'))]


@preset('core_burst', 'G3 backfire: an orange-gold explosion at the chest (the executor): a big flare, a shock ring, '
        'embers and feathers thrown out, explosion particles.')
def _p_core_burst():
    rnd = RND(3)
    out = [card('core_flare', bb='center', spin=90, s0=0.8, s1=4.2, life=8, fade=4, dur=4, col=AMBER),
           card('glow', bb='center', s0=1.2, s1=5.0, life=7, fade=4, col=GOLD_WHITE),
           card('shock_ring', '^ ^ ^', '~ 0', spin=60, s0=(0.6, 1, 0.6), s1=(4.0, 1, 4.0), life=9, fade=4, dur=5, col=EMBER)]
    out += [fly('ember', yaw, rnd.uniform(-10, 50), rnd.uniform(2.2, 3.4), s0=0.3, s1=0.5, life=10, fade=4, col=EMBER)
            for yaw in radial(8, 10)]
    out += [fly('feather', yaw, rnd.uniform(20, 60), rnd.uniform(1.6, 2.4), s0=0.6, s1=0.9, life=14, fade=6,
                roll=rnd.randint(-60, 60)) for yaw in radial(3, 50)]
    return out + [part('explosion', '~ ~ ~', (0.3, 0.3, 0.3), 0, 2), part('flame', '~ ~ ~', (0.6, 0.5, 0.6), 0.12, 24),
                  part('lava', '~ ~ ~', (0.4, 0.3, 0.4), 0, 4), flash(AMBER, '~ ~ ~', 1.0)]


# --- lightning -----------------------------------------------------------------------------------------------------
SKY_N = 6
SKY_PTS = [(0.15 + 0.85 * ((k * 5) % SKY_N) / (SKY_N - 1), 37.0 + 360.0 * k / SKY_N * 1.0) for k in range(SKY_N)]
SKY_DLY = [0.0, 0.12, 0.27, 0.42, 0.58, 0.74]


def _sky_conv():
    out = []
    for k, (rf, yaw) in enumerate(SKY_PTS):
        x, z = xz(rf, yaw)
        out += [(f'x{k}', 'r', 0.1 * x), (f'z{k}', 'r', 0.1 * z), (f'd{k}', 't', None, 0, SKY_DLY[k])]
    return tuple(out)


@preset('sky_arcs', 'K: thin golden lightning arcs crawl down from 8 b above the executor (the locked floor point) '
        'within radius {r} (tenths) for {t} ticks: 6 arcs revealed over the time, each growing down from the top over '
        '6 t; not a floor marking (nothing below 1 b).', conv=_sky_conv())
def _p_sky_arcs():
    out = []
    for k in range(SKY_N):
        out.append(mac(card(f'sky_arc_{k % 4}', f'^$(x{k}) ^8 ^$(z{k})', bb='vertical', s0=(5, 1.0, 5), s1=(5, 7.2, 5),
                            life=9, fade=3, dly=f'$(d{k})', dur=6, col=GOLD_WHITE if k % 2 else GOLD)))
    out += [card('glow', '^ ^8 ^', bb='center', s0=1.0, s1=4.0, life=12, fade=6, col=GOLD),
            dust(GOLD, 1.3, '~ ~8 ~', (1.2, 0.3, 1.2), 10), part('electric_spark', '~ ~7.5 ~', (1.0, 0.6, 1.0), 0.2, 12)]
    return out


@preset('bolt', 'A golden lightning bolt from 12 b down onto the executor (the floor point: K plunge, L shock): two '
        'crossed bolts, a white-gold flash and a burst of sparks.')
def _p_bolt():
    return [card('bolt_0', '^ ^ ^', '~ 0', s0=(4, 12, 4), s1=(5, 12, 5), life=6, fade=3, col=GOLD_WHITE),
            card('bolt_1', '^ ^ ^', '~45 0', s0=(4, 11, 4), s1=(5, 11, 5), life=5, fade=3, dly=1, col=GOLD),
            card('glow', '^ ^1 ^', bb='center', s0=1.5, s1=6.0, life=6, fade=3, col=GOLD_WHITE),
            card('glow', '^ ^6 ^', bb='center', s0=1.0, s1=3.0, life=4, fade=2, col=GOLD),
            flash(GOLD_WHITE, '~ ~1 ~', 1.0), part('electric_spark', '~ ~0.5 ~', (0.8, 0.6, 0.8), 0.6, 40),
            part('firework', '~ ~0.5 ~', (0.2, 0.2, 0.2), 0.25, 10)]


@preset('shock_ring', 'L shock / K plunge: a golden electric shockwave of radius {r} (tenths) at 0.35 b above the '
        'executor (the floor point), a second ring 1 tick later, small bolts flashing up on the ring, sparks.',
        conv=(('s', 'r', 0.1), ('s8', 'r', 0.08), ('q', 'r', 0.05)) + tuple(
            (f'{c}{k}', 'r', 0.1 * v) for k in range(6) for c, v in zip('xz', xz(0.75, 30 + 60 * k))))
def _p_shock_ring():
    out = [mac(card('shock_ring', '^ ^0.35 ^', '~ 0', spin=40, s0=(0.6, 1, 0.6), s1=('$(s)', 1, '$(s)'), life=10,
                    fade=4, dur=5, col=GOLD)),
           mac(card('shock_ring', '^ ^0.6 ^', '~30 0', spin=-40, s0=(0.4, 1, 0.4), s1=('$(s8)', 1, '$(s8)'), life=9,
                    fade=4, dly=1, dur=5, col=GOLD_WHITE)),
           card('glow', '^ ^0.8 ^', bb='center', s0=1.5, s1=5.0, life=6, fade=3, col=GOLD_WHITE)]
    for k in range(6):
        out.append(mac(card(f'bolt_{k % 2}', f'^$(x{k}) ^ ^$(z{k})', f'~{30 + 60 * k} 0', s0=(1.2, 1.0, 1.2),
                            s1=(1.6, 3.2, 1.6), life=5, fade=2, dly=2, dur=2, col=GOLD)))
    out += [mac(part('electric_spark', '~ ~0.5 ~', ('$(q)', 0.3, '$(q)'), 0.3, 40)),
            mac(blockp('sand', '~ ~0.3 ~', ('$(q)', 0.2, '$(q)'), 0.2, 24)), part('explosion', '~ ~0.6 ~', (0.3, 0.1, 0.3), 0, 1)]
    return out


# --- bursts, blinks, wings -----------------------------------------------------------------------------------------
@preset('ember_burst', 'An ember burst at the executor (T1 cape split, intro stance, death): 12 embers flung out and '
        'up, a warm glow, flame particles.')
def _p_ember_burst():
    rnd = RND(11)
    out = [card('glow', bb='center', s0=0.8, s1=3.0, life=7, fade=4, col=EMBER),
           card('core_flare', bb='center', spin=60, s0=0.5, s1=2.2, life=6, fade=3, dur=2, col=EMBER)]
    out += [fly('ember', yaw, rnd.uniform(10, 70), rnd.uniform(1.6, 3.0), s0=0.45, s1=0.75, life=14, fade=6,
                col=EMBER if k % 3 else GOLD_PALE, dly=k % 2) for k, yaw in enumerate(radial(12, rnd.uniform(0, 30)))]
    return out + [part('flame', '~ ~ ~', (0.6, 0.6, 0.6), 0.05, 16), part('lava', '~ ~ ~', (0.4, 0.3, 0.4), 0, 2)]


@preset('blink_out', 'K vanish at the executor (the body + 1.2): a gold spark burst, a short flash, black feathers '
        'scattering (no blue: the player\'s blink is blue-white).')
def _p_blink_out():
    rnd = RND(13)
    out = [card('core_flare', bb='center', spin=120, s0=2.6, s1=0.3, life=6, fade=2, dur=4, col=GOLD),
           card('glint_star', bb='center', spin=120, s0=2.2, s1=0.2, life=6, fade=2, dur=4, col=GOLD_PALE)]
    out += [fly('spark', yaw, rnd.uniform(-20, 50), rnd.uniform(1.6, 2.6), s0=0.6, s1=1.0, life=7, fade=3)
            for yaw in radial(8, 15)]
    out += [fly('feather', yaw, rnd.uniform(-10, 40), rnd.uniform(1.0, 1.8), s0=0.8, s1=1.0, life=12, fade=6,
                roll=rnd.randint(-70, 70)) for yaw in radial(4, 40)]
    return out + [dust(GOLD, 1.2, '~ ~ ~', (0.4, 0.8, 0.4), 16), part('smoke', '~ ~ ~', (0.3, 0.6, 0.3), 0.02, 8)]


@preset('blink_in', 'K reappear at the executor (the body + 1.2): gold sparks converge, a pop of light, feathers '
        'settle.')
def _p_blink_in():
    rnd = RND(14)
    out = []
    for k, yaw in enumerate(radial(6, 10)):
        x, z = xz(2.2, yaw)
        out.append(card('spark', '~ ~ ~', bb='center', s0=1.1, s1=0.4, off=(x, rnd.uniform(-0.6, 0.8), z),
                        move=(-x, 0, -z), life=5, fade=1, dur=4))
    out += [card('core_flare', bb='center', spin=90, s0=0.4, s1=3.0, life=7, fade=3, dly=3, dur=2, col=GOLD),
            card('glint_star', bb='center', spin=90, s0=0.3, s1=2.4, life=7, fade=3, dly=3, dur=2, col=GOLD_PALE)]
    out += [card('feather', f'~{num(x, 2)} ~0.6 ~{num(z, 2)}', f'~{yaw} 0', roll=rnd.randint(-50, 50), s0=0.9, s1=0.9,
                 move=(0, -1.0, 0), life=14, fade=6, dly=3) for x, z, yaw in ((0.8, 0.3, 30), (-0.7, -0.4, 200))]
    return out + [dust(GOLD, 1.0, '~ ~ ~', (0.5, 0.8, 0.5), 12)]


WING_PTS = [(s * (0.9 + 0.6 * k), 0.15 + 0.32 * k, -0.45 - 0.1 * k) for k in range(4) for s in (1, -1)]


@preset('wing_flare', 'The wings flare gold (B1 open, T1 flare): glints running out along both wing spans behind '
        'the executor (the body + 1.4, rotated as the body), a broad gold glow behind her, gold dust.')
def _p_wing_flare():
    out = [card('glow', '^ ^0.3 ^-0.6', bb='center', s0=1.5, s1=4.6, life=10, fade=5, col=GOLD)]
    for i, (x, y, z) in enumerate(WING_PTS):
        out.append(card('glint_star', f'^{num(x, 2)} ^{num(y, 2)} ^{num(z, 2)}', bb='center', spin=80, s0=0.2,
                        s1=1.5 + 0.2 * (i // 2), life=9, fade=4, dly=i // 2, dur=3, col=GOLD_PALE))
    return out + [dust(GOLD, 1.1, '^ ^0.5 ^-0.5', (1.6, 0.6, 0.3), 14)]


# --- mantle --------------------------------------------------------------------------------------------------------
COC_LIFE = 420           # longer than any mantle (M1 360 t); replaced by every cocoon call, removed by crack / clear
COC_POS = '^ ^1.1 ^'     # the cocoon centre over the executor (S3: the body + 1.2; she hovers 1.2 b in the mantle)
COC_S = (2.2, 1.6, 1.0)
CRACK_TINT = {75: rgb('#7A5A38'), 50: rgb('#C09058'), 25: WHITE}


@preset('cocoon', 'The overload mantle cocoon over the hovering body (the executor = the body + 1.2; centre 1.1 b '
        'above it): the wrapped-wing shell (vertical billboard, 2.2 x 3.2 b), a warm glow, and cracks of light by '
        '{pct} (> 75 none, 51-75 dim, 26-50 bright, <= 25 white-hot). Long-lived (the cocoon pool, never counted '
        'against the fx cap); every call replaces the previous cocoon; cocoon_crack / fx/clear remove it.',
        conv=(('p', 'pct', None),))
def _p_cocoon():
    out = [f'kill @e[type=minecraft:item_display,tag={COC}]',
           card('cocoon', COC_POS, bb='vertical', s0=COC_S, s1=COC_S, life=COC_LIFE, pool='coc'),
           card('glow', COC_POS, bb='center', s0=3.6, s1=3.6, life=COC_LIFE, col=rgb('#C8781E'), pool='coc')]
    for lo, hi, pc in ((51, 75, 75), (26, 50, 50), (None, 25, 25)):
        rng = f'{lo}..{hi}' if lo is not None else f'..{hi}'
        out.append(f'execute if score #p {OBJ} matches {rng} run ' +
                   card('cocoon_crack', COC_POS, bb='vertical', s0=(2.21, 1.61, 1.0), s1=(2.21, 1.61, 1.0),
                        life=COC_LIFE, col=CRACK_TINT[pc], pool='coc'))
    out += [dust(EMBER, 1.0, '^ ^1.1 ^', (0.7, 1.2, 0.7), 10), dust(GOLD, 1.0, '^ ^1.1 ^', (0.7, 1.2, 0.7), 10)]
    return out


@preset('cocoon_crack', 'The mantle breaks: the cocoon pool is removed, the shell shatters into black feathers and '
        'light (a flash, a crack card bursting out, embers). At the executor (the body + 1.2).')
def _p_cocoon_crack():
    rnd = RND(21)
    out = [f'kill @e[type=minecraft:item_display,tag={COC}]',
           card('cocoon_crack', COC_POS, bb='vertical', s0=(2.2, 1.6, 1), s1=(3.4, 2.4, 1), life=5, fade=3, dur=3),
           card('glow', COC_POS, bb='center', s0=2.0, s1=6.0, life=6, fade=3, col=GOLD_WHITE)]
    out += [fly('feather', yaw, rnd.uniform(-10, 60), rnd.uniform(2.0, 3.4), h=1.1, s0=0.7, s1=1.0, life=16, fade=6,
                roll=rnd.randint(-80, 80)) for yaw in radial(10, rnd.uniform(0, 20))]
    out += [fly('ember', yaw, rnd.uniform(0, 60), rnd.uniform(1.8, 2.8), h=1.1, s0=0.3, s1=0.5, life=10, fade=4,
                col=GOLD if k % 2 else EMBER) for k, yaw in enumerate(radial(6, 35))]
    return out + [flash(GOLD_WHITE, '~ ~1.1 ~', 1.0), part('end_rod', '~ ~1.1 ~', (0.6, 1.0, 0.6), 0.12, 24),
                  blockp('gold_block', '~ ~1.1 ~', (0.6, 1.0, 0.6), 0.2, 16)]


@preset('nova_swell', 'The nova tell (mantle_nova swell, 40 t): a white-gold glow and flare swelling over {t} ticks at '
        'the executor (the body + 1.2), gold motes drawn in from 4 b, rising sparks.',
        conv=(('t', 't', None), ('l', 't', None, 6),) + tuple((f'd{k}', 't', None, 0, k / 8) for k in range(8)))
def _p_nova_swell():
    out = [mac(card('glow', COC_POS, bb='center', s0=1.0, s1=6.0, life='$(l)', fade=4, dur='$(t)', col=GOLD_WHITE)),
           mac(card('core_flare', COC_POS, bb='center', spin=170, s0=0.6, s1=4.0, life='$(l)', fade=4, dur='$(t)',
                    col=GOLD))]
    for k, yaw in enumerate(radial(8, 22.5)):
        x, z = xz(4.0, yaw)
        out.append(mac(card('mote', '~ ~1.1 ~', bb='center', s0=0.8, s1=0.3, off=(x, 0.8 * ((k % 3) - 1), z),
                            move=(-x, 0, -z), life=6, fade=1, dly=f'$(d{k})', dur=5, col=GOLD)))
    return out + [dust(GOLD_PALE, 1.2, '~ ~1.1 ~', (1.5, 1.5, 1.5), 16), part('end_rod', '~ ~1.1 ~', (1.2, 1.2, 1.2), 0.02, 6)]


@preset('nova_flash', 'The nova hit: an arena-wide white-gold flash at the executor (the body + 1.2): a huge glow, '
        'two shock rings racing out to 24 b at the floor, a flash, sparks.')
def _p_nova_flash():
    return [card('glow', bb='center', s0=2.0, s1=26.0, life=6, fade=3, col=GOLD_WHITE),
            card('core_flare', bb='center', spin=60, s0=1.0, s1=9.0, life=6, fade=3, col=GOLD),
            card('shock_ring', '^ ^-0.8 ^', '~ 0', spin=30, s0=(1, 1, 1), s1=(26, 1, 26), life=10, fade=3, dur=8, col=GOLD),
            card('shock_ring', '^ ^-0.4 ^', '~45 0', spin=-30, s0=(1, 1, 1), s1=(20, 1, 20), life=10, fade=3, dly=2,
                 dur=7, col=GOLD_WHITE),
            flash(GOLD_WHITE, '~ ~ ~', 1.0), part('electric_spark', '~ ~ ~', (3.0, 1.0, 3.0), 0.5, 60),
            part('explosion_emitter', '~ ~ ~', (0, 0, 0), 0, 1)]


# --- sequences / ambient -------------------------------------------------------------------------------------------
@preset('ignite_blade', 'Intro E10: the edge ignites. Executor = the sword guard, the blade straight up along +y for '
        '2.2 b: five flame tongues climbing it in turn (vertical billboards, 14 t), embers and flame particles.')
def _p_ignite_blade():
    out = []
    for k in range(5):
        y = 0.2 + 0.45 * k
        out.append(card('flame', f'^ ^{num(y, 2)} ^', bb='vertical', s0=(0.5, 0.3, 0.5), s1=(0.9, 1.1, 0.9), life=14,
                        fade=5, dly=k, dur=4, col=PYRO))
    out += [card('glow', '^ ^1.1 ^', bb='center', s0=0.6, s1=2.4, life=16, fade=6, dly=2, col=EMBER),
            fly('ember', 0, 75, 2.0, h=1.6, s0=0.25, s1=0.35, life=12, fade=5, col=EMBER, dly=3),
            fly('ember', 120, 70, 1.8, h=1.2, s0=0.25, s1=0.35, life=12, fade=5, col=GOLD_PALE, dly=4),
            fly('ember', 240, 72, 1.9, h=2.0, s0=0.25, s1=0.35, life=12, fade=5, col=EMBER, dly=5)]
    return out + [part('flame', '~ ~1.1 ~', (0.05, 0.9, 0.05), 0.02, 18), part('small_flame', '~ ~1.1 ~', (0.08, 1.0, 0.08), 0.02, 10),
                  part('lava', '~ ~1.6 ~', (0.1, 0.4, 0.1), 0, 2)]


@preset('dust_ring', 'Sand thrown up in a ring of radius {r} (tenths) about the executor (the floor point: landings, '
        'the intro drop, B3 bangs): eight dust puffs riding out to the radius, sand particles. Airborne (no floor card).',
        conv=tuple((f'{c}{k}', 'r', 0.1 * v * f) for k in range(8) for c, v, f in
                   zip(('a', 'b', 'x', 'z'), xz(1.0, 22.5 + 45 * k) * 2, (0.35, 0.35, 1.0, 1.0)))
        + (('q', 'r', 0.05),))
def _p_dust_ring():
    out = []
    for k in range(8):
        out.append(mac(card('dust', '~ ~0.4 ~', bb='center', s0=0.7, s1=2.0, off=(f'$(a{k})', 0.4, f'$(b{k})'),
                            move=(f'$(x{k})', 0.9, f'$(z{k})'), life=14, fade=7, dur=8, col=SAND if k % 2 else SAND_DARK)))
    return out + [mac(blockp('sand', '~ ~0.2 ~', ('$(q)', 0.1, '$(q)'), 0.15, 30)),
                  mac(fdust('sand', '~ ~1.2 ~', ('$(q)', 0.4, '$(q)'), 10))]


@preset('swap_fx', 'G1 element swap at the executor (the body + 1.2, rotated as the body): to Pyro (el 1) flame '
        'tongues swirling up and embers, to Electro (el 3) gold arcs crackling around her and sparks; a glow in the new '
        'colour.', split_el=True)
def _p_swap_fx(el):
    out = [card('glow', bb='center', s0=0.8, s1=3.0, life=10, fade=5, col=EL_TINT[el])]
    if el == api.PYRO:
        for k, yaw in enumerate(radial(6, 0)):
            x, z = xz(0.7, yaw)
            out.append(card('flame', f'^{num(x, 2)} ^-0.9 ^{num(z, 2)}', bb='vertical', s0=(0.5, 0.4, 0.5),
                            s1=(0.8, 1.6, 0.8), move=(0, 0.6, 0), life=12, fade=5, dly=k % 3, dur=5, col=PYRO))
        out += [fly('ember', yaw, 60, 1.8, s0=0.25, s1=0.4, life=10, fade=4, col=EMBER, dly=2) for yaw in radial(4, 45)]
    else:
        for k, yaw in enumerate(radial(5, 10)):
            x, z = xz(0.9, yaw)
            out.append(card(f'sky_arc_{k % 4}', f'^{num(x, 2)} ^1.2 ^{num(z, 2)}', bb='vertical', s0=(1.0, 0.4, 1.0),
                            s1=(1.2, 2.2, 1.2), life=5, fade=2, dly=k % 3, dur=3, col=GOLD_WHITE))
        out.append(card('glint_star', '^-0.4 ^0.3 ^0.8', bb='center', spin=90, s0=0.3, s1=1.4, life=7, fade=3, dly=2,
                        col=GOLD))
    return out + el_parts(el, '~ ~ ~', (0.4, 0.7, 0.4), 20)


RIFT_POS = '^ ^1.45 ^'      # the void centre above the tear point (S1's rift: CENTRE 1.45, VOID_H 2.6)
RIFT_ARCS = [(0.75, 1.9), (-0.8, 1.6), (0.55, 0.8), (-0.6, 2.4)]


@preset('arrive_rift', 'The arrival tear behind the player (PLAN §6.4): at the executor (the floor point 1.5 b behind '
        'the start, facing the arena) the dungeon rift\'s void, rim and four lightning arcs (S1\'s rlk:rift models when '
        'the pack has them, else the kit\'s fallback tear) shrink shut over 30 t, sparks and portal motes.')
def _p_arrive_rift():
    out = [card('rift_rim', RIFT_POS, bb='vertical', s0=3.0, s1=0.1, life=30, fade=4, dur=26, col=RIFT_RIM),
           card('rift_void', RIFT_POS, bb='vertical', s0=2.6, s1=0.1, life=30, fade=4, dur=26)]
    for k, (x, y) in enumerate(RIFT_ARCS):
        out.append(card(f'rift_arc{k}', f'^{num(x, 2)} ^{num(y, 2)} ^0.05', bb='center', s0=1.1, s1=0.4,
                        life=8 + 4 * (k % 2), fade=3, dly=4 * k, dur=6))
    return out + [part('reverse_portal', '~ ~1.4 ~', (0.5, 1.0, 0.5), 0.05, 30), part('end_rod', '~ ~1.4 ~', (0.4, 0.9, 0.4), 0.05, 8)]


@preset('ambient_dust', 'Arena ambience (the module, every ~10 t): sand motes falling through the warm haze and '
        'white ash around the executor (the arena centre), particles only; skipped while the fx cards are busy.')
def _p_ambient_dust():
    return [fdust('sand', '~ ~7 ~', (10.0, 3.0, 10.0), 6), part('white_ash', '~ ~4 ~', (11.0, 3.0, 11.0), 0.0, 10),
            fdust('red_sand', '~ ~8 ~', (9.0, 2.0, 9.0), 2)]


@preset('impact', 'A blade hit landing (S3: on the floor ahead of the body, + 0.2): a burst of light, a flare, sparks '
        'and floor chunks flung out; el 1 flame and embers, el 3 small golden bolts and sparks.', split_el=True)
def _p_impact(el):
    rnd = RND(30 + el)
    out = [card('glow', '^ ^0.5 ^', bb='center', s0=2.2, s1=3.6, life=6, fade=3, col=EL_TINT[el]),
           card('core_flare', '^ ^0.6 ^', bb='center', spin=70, s0=2.2, s1=3.4, life=6, fade=3, dur=2, col=EL_TINT[el]),
           card('glint_star', '^ ^0.6 ^', bb='center', spin=-50, s0=1.6, s1=2.6, life=5, fade=2, dur=2, col=EL_DEEP[el])]
    out += [fly('spark', yaw, rnd.uniform(15, 55), rnd.uniform(1.6, 2.6), h=0.3, s0=0.6, s1=1.0, life=7, fade=3)
            for yaw in radial(6, 10)]
    out += [fly('chunk', yaw, rnd.uniform(40, 70), rnd.uniform(0.9, 1.4), h=0.2, s0=0.35, s1=0.45, life=9, fade=4,
                roll=rnd.randint(-60, 60)) for yaw in radial(3, 60)]
    if el == api.ELECTRO:
        out += [card(f'bolt_{k}', '^ ^ ^', f'~{60 * k} 0', s0=(0.8, 0.8, 0.8), s1=(1.2, 2.4, 1.2), life=4, fade=2, dur=2,
                     col=GOLD) for k in range(2)]
    else:
        out.append(card('flame', '^ ^ ^', bb='vertical', s0=(0.8, 0.4, 0.8), s1=(1.4, 1.6, 1.4), life=7, fade=4, dur=3,
                        col=PYRO))
    return out + el_parts(el, '~ ~0.4 ~', (0.5, 0.3, 0.5), 18) + [blockp('sand', '~ ~0.2 ~', (0.5, 0.1, 0.5), 0.15, 12)]


assert set(PRESETS) == set(api.KIT_PRESETS), set(PRESETS) ^ set(api.KIT_PRESETS)


# ----------------------------------------------------------------------------- props (api.KIT_PROPS)
PROPS = {
    # name -> (doc, kind, tint, billboard, scale (x, y, z), brightness)
    'crescent_h_1': ('W1 ground crescent, Pyro: a 7 b wide golden-orange flame bow, 1.65 b high (front quad) and 3 b deep '
                     '(top quad), centred on the display.', 'crescent_h', PYRO, 'fixed', (7.0, 1.65, 3.0), 15),
    'crescent_h_3': ('W1 ground crescent, Electro: white-gold.', 'crescent_h', ELECTRO, 'fixed', (7.0, 1.65, 3.0), 15),
    'crescent_v_1': ('W2 air crescent, Pyro: an upright flame crescent 2.6 b (crossed quads).', 'crescent_v', PYRO,
                     'fixed', (2.6, 2.6, 2.6), 15),
    'crescent_v_3': ('W2 air crescent, Electro: white-gold.', 'crescent_v', ELECTRO, 'fixed', (2.6, 2.6, 2.6), 15),
    'feather': ('Mantle feather: a glowing gold-white blade-feather 1.6 b, vertical billboard.', 'feather_glow', WHITE,
                'vertical', (1.6, 1.6, 1.6), 15),
}
assert tuple(PROPS) == tuple(api.KIT_PROPS), (tuple(PROPS), api.KIT_PROPS)

# ----------------------------------------------------------------------------- writer
HEADER = '# Generated by tools/build_mboss_tk_fx.py (타키 fx kit) - edit the generator, not this file.\n'
E = FN + 'e/'
SEL = f'@e[type=minecraft:item_display,tag={TAG}'
DEF_A = f'tg:"{TAG}_c",tpd:0'
POOL_FX, POOL_COC = 0, 2
FAKE = ('#n', '#cn', '#now', '#wd', '#c2', '#roll', '#spin', '#life', '#fade', '#dly', '#dur', '#hit', '#pool', '#a',
        '#el', '#p', '#c', '#demo', '#dt')
INIT = f'execute unless data storage {STO} fx{{init:1b}} run function {E}init'


NEG_LIT = __import__('re').compile(r'scoreboard players (add|remove) \S+ \S+ -')


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
    head = [INIT, f'execute if score #n {OBJ} matches {CAP}.. run return 0']
    W.w('card', [
        '# Spawn one painted card at pos, rotated rot (relative to the executing context; fixed cards).',
        '# {kind, pos:"^x ^y ^z", rot:"~ ~", bb:fixed|center|vertical|horizontal, roll:<deg, about local z>,',
        '#  spin:<deg over the main interpolation, -170..170, about the card normal (y for flat / cross / wave)>,',
        '#  s0:<start size>, s1:<end size>, move:"dx,dy,dz" (end offset, display frame: +x left, +y up, +z forward),',
        '#  life:<ticks>, fade:<shrink-out ticks>, col:<RGB int tint, 16777215 = the painted colours>}.',
        f'# Skipped (no error) while {CAP} fx cards are alive.', *head,
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
        '# the fade>, hit:<ticks after the call when the tint becomes col2, -1 = never>, col2:<RGB int>, tg:<the pool tag:',
        f'# {TAG}_c fx, {COC} the cocoon pool (never capped)>. Same cap for fx cards.',
        INIT, f'$execute unless data storage {STO} fx{{tgc:"$(tg)"}} if score #n {OBJ} matches {CAP}.. run return 0',
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
        f'scoreboard players set #pool {OBJ} {POOL_FX}',
        f'$execute if data storage {STO} fx{{tgc:"$(tg)"}} run scoreboard players set #pool {OBJ} {POOL_COC}',
        f'function {E}make',
    ])
    W.w('e/make', [
        f'# Internal: storage {STO} fx.a (kind pos rot bb s0 s1 off move col col2 ax tg tpd) + #roll #spin #life #fade',
        '# #dly #dur #hit #pool (0 fx, 2 cocoon) -> one card. The stage clock is gametime + 1 (the fg kit\'s first-tick',
        '# fix): the ager (fx/e/world, a 1t schedule) runs at the END of this server tick with gametime already + 1, so',
        '# the main interpolation starts in the next server tick and the client animates it. Stages: shows at clock +',
        '# dly, interpolates from clock + dly + 1 over dur ticks, recolours at clock + hit, shrinks over the last fade',
        '# ticks, removed at clock + dly + life.',
        f'execute if score #pool {OBJ} matches {POOL_FX} run scoreboard players add #n {OBJ} 1',
        f'execute if score #pool {OBJ} matches {POOL_COC} run scoreboard players add #cn {OBJ} 1',
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
        'tkS:{start_interpolation:0,interpolation_duration:0,transformation:{scale:[$(s0)]}},'
        'tkG:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'tkF:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}},'
        'tkC:$(col2)}}}}',
        f'$execute positioned $(pos) rotated $(rot) run tp {SEL}_new,limit=1] ~ ~ ~ ~ ~',
    ])
    W.w('e/born', [
        '# Internal, as the new card: stage clock values (gametime + 1 based) in tkFxS tkFxG tkFxH tkFxK tkFxD.',
        f'scoreboard players operation @s tkFxS = #now {OBJ}',
        f'scoreboard players operation @s tkFxS += #dly {OBJ}',
        'scoreboard players operation @s tkFxG = @s tkFxS',
        'scoreboard players add @s tkFxG 1',
        'scoreboard players operation @s tkFxD = @s tkFxS',
        f'scoreboard players operation @s tkFxD += #life {OBJ}',
        'scoreboard players operation @s tkFxK = @s tkFxD',
        f'scoreboard players operation @s tkFxK -= #fade {OBJ}',
        f'scoreboard players operation @s tkFxH = #now {OBJ}',
        f'scoreboard players operation @s tkFxH += #hit {OBJ}',
        f'tag @s add {TAG}_go',
        f'execute if score #dly {OBJ} matches 1.. run tag @s add {TAG}_sh',
        f'execute if score #fade {OBJ} matches 1.. run tag @s add {TAG}_fd',
        f'execute if score #hit {OBJ} matches 0.. if score #c2 {OBJ} matches 0.. run tag @s add {TAG}_hit',
    ])
    W.w('e/world', [
        '# Ages the kit\'s cards once per tick while any is alive (scheduled from e/make and itself, so it runs at the',
        '# end of the server tick; no hook in rlk:tick). A dead or reviving player clears every card (fx/clear).',
        f'execute unless entity {SEL},limit=1] run return run function {E}zero',
        f'execute if entity @a[tag=player,scores={{dead=1}}] run function {FN}clear',
        f'execute if entity @a[tag=player,scores={{rnDie=1..}}] run function {FN}clear',
        f'execute store result score #now {OBJ} run time query gametime',
        f'execute as {SEL}] run function {E}age',
        f'execute store result score #n {OBJ} if entity {SEL},tag=!{COC}]',
        f'execute store result score #cn {OBJ} if entity {SEL},tag={COC}]',
        f'execute if entity {SEL},limit=1] run schedule function {E}world 1t replace',
    ])
    W.w('e/zero', [f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #cn {OBJ} 0'])
    W.w('e/age', [
        '# As one card (the stage clock in #now).',
        'execute unless score @s tkFxD = @s tkFxD run return run kill @s',
        f'execute if score #now {OBJ} >= @s tkFxD run return run kill @s',
        f'execute if entity @s[tag={TAG}_sh] if score #now {OBJ} >= @s tkFxS run function {E}show',
        f'execute if entity @s[tag={TAG}_go] if score #now {OBJ} >= @s tkFxG run function {E}go',
        f'execute if entity @s[tag={TAG}_hit] if score #now {OBJ} >= @s tkFxH run function {E}hit',
        f'execute if entity @s[tag={TAG}_fd] if score #now {OBJ} >= @s tkFxK run function {E}fade',
    ])
    W.w('e/show', ['# a delayed card appears at its start size',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".tkS',
                   f'tag @s remove {TAG}_sh'])
    W.w('e/go', ['# start -> end transformation over dur ticks (client interpolation)',
                 'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".tkG',
                 f'tag @s remove {TAG}_go'])
    W.w('e/hit', ['# the tint changes (the second colour)',
                  'data modify entity @s item.components."minecraft:custom_model_data".colors[0] set from entity @s '
                  'item.components."minecraft:custom_data".tkC',
                  f'tag @s remove {TAG}_hit'])
    W.w('e/fade', ['# shrink to nothing over the last fade ticks',
                   'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".tkF',
                   f'tag @s remove {TAG}_fd'])
    spin_y = ','.join(f'{k}:"0f,1f,0f"' for k in ALL_KINDS if kind_info(k)[0] in SPIN_Y)
    W.w('e/init', ['# Objectives, constants and tables of the kit (made by the first call; removed by fx/uninstall).',
                   f'scoreboard objectives add {OBJ} dummy', *[f'scoreboard objectives add {o} dummy' for o in OBJECTIVES],
                   f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #cn {OBJ} 0',
                   '# spin axes (= the card normal) of the flat, cross and wave kinds; face kinds keep z (storage a default)',
                   f'data modify storage {STO} fx.ax set value {{{spin_y}}}',
                   f'data modify storage {STO} fx.tgc set value "{COC}"',
                   f'data modify storage {STO} fx.hud set value {{badge:[],gauge:[]}}',
                   f'data modify storage {STO} fx.init set value 1b'])
    W.w('clear', ['# Remove every kit card (fx and the cocoon). Safe to call any time (pause, death_start, cleanup).',
                  f'kill {SEL}]', INIT, f'scoreboard players set #n {OBJ} 0', f'scoreboard players set #cn {OBJ} 0'])
    W.w('uninstall', ['# Remove the kit\'s cards, the demo stand-ins, objectives, storage rlk:tk fx and schedules (the',
                      '# module\'s uninstall hook).',
                      f'kill {SEL}]', f'kill @e[tag={DEMO}]',
                      f'scoreboard objectives remove {OBJ}', *[f'scoreboard objectives remove {o}' for o in OBJECTIVES],
                      f'data remove storage {STO} fx',
                      f'schedule clear {E}world', f'schedule clear {FN}test/e/tick'])
    W.w('look', [
        '# Dress @s (an item_display the module owns) as a kit sprite: {kind, col:<RGB int>}. Full bright; the caller',
        '# keeps its own transformation / billboard.',
        '$data merge entity @s {item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        f'"{NS_TEX}$(kind)","minecraft:custom_model_data":{{colors:[$(col)]}}}}}},brightness:{{sky:15,block:15}}}}',
    ])


def props(W):
    for name, (doc, kind, col, bb, sc, br) in PROPS.items():
        tr = (f'transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[{num(sc[0])}f,{num(sc[1])}f,'
              f'{num(sc[2])}f],right_rotation:[0f,0f,0f,1f]}}')
        W.w(f'prop/{name}', [f'# {doc}', '# As @s = the projectile item_display (rotated = its flight): item, tint, billboard,',
                             '# brightness, transformation.',
                             f'data merge entity @s {{item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":'
                             f'"{NS_TEX}{kind}","minecraft:custom_model_data":{{colors:[{col}]}}}}}},billboard:"{bb}",'
                             f'brightness:{{sky:15,block:{br}}},view_range:2f,shadow_radius:0f,{tr}}}'])


def sounds(W):
    for name, (doc, layers) in SOUNDS.items():
        W.w(f'snd/{name}', [f'# {doc}', '# Layers: event volume pitch minVolume (mboss_lib.sound rule).'] +
            [sound_line(*l) for l in layers])


def hud_funcs(W):
    H = FN + 'hud/'
    compose = [f'data modify storage rlk:mboss extra set value []',
               f'data modify storage rlk:mboss extra append from storage {STO} fx.hud.badge[]',
               f'data modify storage rlk:mboss extra append from storage {STO} fx.hud.gauge[]']
    W.w('hud/e/put', ['# Internal: the boss-bar name-line extras = the badge, then the gauge (rlk:mboss extra[]).'] + compose)
    b = ['# {el}: the badge on the boss-bar name line: 1 ◈불 (Pyro #FF8A3D), 3 ◈번개 (Electro #E8C84A), 9 ◈외피 (the',
         '# mantle, gold), anything else none. The root text is empty and unstyled (no glyph-font inheritance).',
         INIT, f'$scoreboard players set #el {OBJ} $(el)', f'data modify storage {STO} fx.hud.badge set value []']
    for el in BADGES:
        b.append(f'execute if score #el {OBJ} matches {el} run data modify storage {STO} fx.hud.badge set value [{badge(el)}]')
    W.w('hud/badge', b + [f'function {H}e/put'])
    g = ['# {pct}: the mantle gauge (0..100) as 20 gold cells after the badge on the name line (n = pct / 5 lit).',
         INIT, f'$scoreboard players set #p {OBJ} $(pct)']
    for n in range(GAUGE_CELLS + 1):
        lo, hi = n * 5, n * 5 + 4
        rng = f'..{hi}' if n == 0 else (f'{lo}..' if n == GAUGE_CELLS else f'{lo}..{hi}')
        g.append(f'execute if score #p {OBJ} matches {rng} run data modify storage {STO} fx.hud.gauge set value [{gauge(lo)}]')
    W.w('hud/gauge', g + [f'function {H}e/put'])
    W.w('hud/clear', ['# Badge and gauge off (cleanup, the mantle end before the element badge comes back).',
                      f'data modify storage {STO} fx.hud.badge set value []',
                      f'data modify storage {STO} fx.hud.gauge set value []', *compose[:1]])


def presets_dp(W):
    for name, (doc, args, f, conv, split) in PRESETS.items():
        head = [f'# {doc}']
        if args:
            head.append('# {' + ', '.join(args) + '} (macro: tenths of a block, degrees, ticks, el 1 / 3, c, pct)')
        if name in AMBIENT:
            head += [f'# Ambient: skipped while {SOFT}+ fx cards live.', INIT,
                     f'execute if score #n {OBJ} matches {SOFT}.. run return 0']
        variants = {el: f(el) for el in (api.PYRO, api.ELECTRO)} if split else {None: f()}
        for body in variants.values():
            if name in PTCL:
                assert not any(f'{FN}card' in l for l in body), name
        if not args:
            W.w(f'p/{name}', head + variants[None])
            assert not any(l.startswith('$') for l in variants[None]), name
            continue
        pub = list(head)
        macro_args = [a for a in args if a != 'el']
        if 'el' in args:
            pub.append(f'$scoreboard players set #el {OBJ} $(el)')
        pub.append(f'data modify storage {STO} fx.pa set value {{}}')
        for a in macro_args:
            if a in ('yaw', 'pitch', 'roll'):
                pub.append(f'$data modify storage {PA}.{a} set value $({a})')
        for c in conv:
            key, a, scale = c[0], c[1], c[2]
            add = c[3] if len(c) > 3 else 0
            frac = c[4] if len(c) > 4 else None
            if frac is not None:
                pub.append(f'$execute store result storage {PA}.{key} int {num(frac, 5)} run scoreboard players set #a {OBJ} $({a})')
            elif scale is None:
                if add:
                    pub.append(f'$scoreboard players set #a {OBJ} $({a})')
                    pub.append(f'execute store result storage {PA}.{key} int 1 run scoreboard players add #a {OBJ} {add}')
                else:
                    pub.append(f'$data modify storage {PA}.{key} set value $({a})')
            else:
                pub.append(f'$execute store result storage {PA}.{key} float {num(scale, 7)} run scoreboard players set #a '
                           f'{OBJ} $({a})')
        if name == 'core_flare':
            pub.append(f'$scoreboard players set #c {OBJ} $(c)')
            pub.append(f'data modify storage {PA}.col set value {CORE_C[2]}')
            for c, col in CORE_C.items():
                if c != 2:
                    pub.append(f'execute if score #c {OBJ} matches {c} run data modify storage {PA}.col set value {col}')
        if name == 'cocoon':
            pub.append(f'$scoreboard players set #p {OBJ} $(pct)')
        if split:
            w3 = f' with storage {PA}' if any(l.startswith('$') for l in variants[api.ELECTRO]) else ''
            w1 = f' with storage {PA}' if any(l.startswith('$') for l in variants[api.PYRO]) else ''
            pub.append(f'execute if score #el {OBJ} matches {api.ELECTRO} run return run function {FN}p/e/{name}_3{w3}')
            pub.append(f'function {FN}p/e/{name}_1{w1}')
            for el, body in variants.items():
                W.w(f'p/e/{name}_{el}', [f'# Internal of p/{name}, el {el}' + (f' (macro, storage {PA}).' if
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
    """fx cards one call spawns (the larger el variant)"""
    _d, _a, f, _c, split = PRESETS[name]
    bodies = [f(1), f(3)] if split else [f()]
    n = max(sum(1 for l in b if f'{FN}card' in l and not l.lstrip('$').startswith('execute if score #p')) for b in bodies)
    if name == 'cocoon':
        n += 1                       # the crack overlay (pct <= 75)
    return n


# ----------------------------------------------------------------------------- tests and demos
TEST_ARGS = {'r': 36, 'yaw': 0, 'pitch': 0, 'roll': 0, 'el': 1, 'len': 70, 't': 16, 'c': 2, 'pct': 50}


def test_call(name, **over):
    a = dict(TEST_ARGS, **over)
    return fx(name, **{k: a[k] for k in PRESETS[name][1]})


def _ev(t, where, *lines):
    return [(t, where, l) for l in lines]


def _demos():
    f = fx
    D = {}
    D['slash_arc'] = sum([_ev(5 + 14 * i, 'chest', f('slash_arc', r=36, yaw=0, pitch=0, roll=roll, el=el), snd(s))
                          for i, (roll, el, s) in enumerate(((0, 1, 'slash_light'), (35, 1, 'slash_light'),
                                                             (90, 1, 'slash_heavy'), (175, 3, 'slash_light'),
                                                             (-35, 3, 'slash_heavy'), (0, 3, 'slash_heavy')))], [])
    D['spin_ring'] = _ev(5, 'waist', f('spin_ring', r=42, el=1), snd('spin')) + _ev(30, 'waist', f('spin_ring', r=42, el=3), snd('spin'))
    D['thrust_trail'] = (_ev(5, 'glintpt', f('glint'), snd('glint')) + _ev(21, 'waist', f('thrust_trail', len=70, el=1), snd('thrust'))
                         + _ev(45, 'waist', f('thrust_trail', len=46, el=3), snd('thrust')))
    D['dash_trail'] = (_ev(0, 'chest', f('core_flare', c=2), snd('flare_tell')) + _ev(14, 'waist', f('dash_trail', len=120, el=1), snd('dash'))
                       + _ev(40, 'waist', f('dash_trail', len=80, el=3), snd('dash')))
    D['glint'] = _ev(5, 'glintpt', f('glint'), snd('glint')) + _ev(25, 'glintpt', f('glint'))
    D['core_flare'] = sum([_ev(5 + 25 * i, 'chest15', f('core_flare', c=c), snd('flare_tell' if c != 3 else 'charge_core'))
                           for i, c in enumerate((1, 2, 3))], [])
    D['core_burst'] = _ev(0, 'chest15', f('core_flare', c=2)) + _ev(12, 'chest15', f('core_burst'), snd('core_backfire'), snd('stagger'))
    D['sky_arcs'] = (_ev(0, 'body', snd('leap')) + _ev(4, 'spot', f('sky_arcs', r=30, t=16), snd('sky_arcs'))
                     + _ev(20, 'spot', f('bolt'), f('shock_ring', r=35), f('impact', el=3), snd('plunge')))
    D['bolt'] = _ev(5, 'spot', f('bolt'), snd('plunge')) + _ev(25, 'spot', f('bolt'), snd('shock'))
    D['shock_ring'] = _ev(5, 'body', f('bolt'), f('shock_ring', r=55), f('dust_ring', r=40), snd('shock'))
    D['ember_burst'] = _ev(5, 'chest', f('ember_burst'), snd('t1_split')) + _ev(25, 'chest', f('ember_burst'))
    D['blink_out'] = _ev(5, 'chest', f('blink_out'), snd('blink_out')) + _ev(35, 'spot2', f('blink_in'), snd('blink_in'))
    D['blink_in'] = _ev(5, 'spot2', f('blink_in'), snd('blink_in'))
    D['wing_flare'] = _ev(5, 'chest14', f('wing_flare'), snd('t1_flare')) + _ev(30, 'chest14', f('wing_flare'))
    D['cocoon'] = (_ev(0, 'chest', f('cocoon', pct=100), snd('mantle_wrap'), hud('badge', el=9), hud('gauge', pct=100))
                   + sum([_ev(30 * i, 'chest', f('cocoon', pct=p), hud('gauge', pct=p)) for i, p in ((1, 75), (2, 50), (3, 25))], [])
                   + _ev(30, 'chest', snd('feather_fall')) + _ev(120, 'chest', f('cocoon_crack'), snd('mantle_break'), hud('clear'),
                                                                  hud('badge', el=1)))
    D['cocoon_crack'] = _ev(0, 'chest', f('cocoon', pct=25)) + _ev(20, 'chest', f('cocoon_crack'), snd('mantle_break'))
    D['nova_swell'] = (_ev(0, 'chest', f('cocoon', pct=60)) + _ev(5, 'chest', f('nova_swell', t=40), snd('nova_swell'))
                       + _ev(45, 'chest', f('nova_flash'), f('cocoon_crack'), snd('nova_blast')))
    D['nova_flash'] = _ev(5, 'chest', f('nova_flash'), snd('nova_blast'))
    D['ignite_blade'] = _ev(5, 'guard', f('ignite_blade'), snd('blade_ignite')) + _ev(19, 'body', f('ember_burst'), snd('stance'))
    D['dust_ring'] = _ev(5, 'body', f('dust_ring', r=30), snd('body_land')) + _ev(25, 'spot', f('dust_ring', r=50))
    D['swap_fx'] = (_ev(5, 'chest', f('swap_fx', el=3), snd('swap_electro'), hud('badge', el=3))
                    + _ev(40, 'chest', f('swap_fx', el=1), snd('swap_pyro'), hud('badge', el=1)))
    D['arrive_rift'] = _ev(5, 'rift', f('arrive_rift'), snd('arrive_rift'))
    D['ambient_dust'] = sum([_ev(t, 'body', f('ambient_dust')) for t in range(0, 80, 10)], [])
    D['impact'] = (_ev(5, 'ahead2', f('impact', el=1), snd('slash_heavy')) + _ev(20, 'ahead2', f('impact', el=3), snd('chop'))
                   + _ev(35, 'ahead2', f('impact', el=1), snd('wave_hit')))
    D['high_glint'] = sum([_ev(t, 'high', f('high_glint'), snd('high_glint')) for t in (5, 35)], [])
    assert set(D) == set(PRESETS), set(D) ^ set(PRESETS)
    return D


DEMOS = _demos()
DEMO_LEN = {k: max(t for t, _w, _l in v) + 40 for k, v in DEMOS.items()}
DEMO_WHERE = {
    'body': 'at @s rotated as @s rotated ~ 0',
    'waist': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~',
    'chest': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~',
    'chest14': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~',
    'chest15': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~',
    'glintpt': 'at @s rotated as @s rotated ~ 0 positioned ~ ~1.6 ~',
    'guard': 'at @s rotated as @s rotated ~ 0 positioned ^-0.5 ^0.9 ^0.5',
    'ahead2': 'at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2',
    'spot': 'at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4.5',
    'spot2': 'at @s rotated as @s rotated ~ 0 positioned ^3 ^1.2 ^2',
    'rift': 'at @s rotated as @s rotated ~ 0 positioned ^-3 ^ ^1',
    'high': 'at @s rotated as @s rotated ~ 0 positioned ~ ~13 ~',
}


def tests(W):
    T = FN + 'test/'
    stand = (f'summon minecraft:armor_stand ~ ~ ~ {{Tags:["{DEMO}","rlk_room","rlk_mb_aux"],NoGravity:1b,Invulnerable:1b,'
             'ShowArms:1b,NoBasePlate:1b,equipment:{mainhand:{id:"minecraft:netherite_sword",count:1},'
             'head:{id:"minecraft:netherite_helmet",count:1},chest:{id:"minecraft:netherite_chestplate",count:1}}}')
    W.w('test/stage', ['# The demo stand-in: an armour stand with a netherite sword 6 b in front of the executor, facing it',
                       '# (a vanilla stand-in for the body; no rig calls).',
                       f'# /execute as @p at @s rotated ~ 0 run function {T}stage, then {T}<preset>.',
                       f'function {T}stop',
                       f'execute positioned ^ ^ ^6 run {stand}',
                       f'execute as @e[type=minecraft:armor_stand,tag={DEMO},limit=1] at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0',
                       INIT, f'scoreboard players set #demo {OBJ} 0', f'scoreboard players set #dt {OBJ} 0',
                       f'schedule function {T}e/tick 1t replace'])
    W.w('test/stop', ['# Remove the demo stand-in and the test props.', f'kill @e[tag={DEMO}]', f'schedule clear {T}e/tick',
                      f'scoreboard players set #demo {OBJ} 0'])
    tick = ['# Demo ticker (scheduled): the running demo\'s events as the stand-in.',
            f'execute unless entity @e[type=minecraft:armor_stand,tag={DEMO},limit=1] run return 0',
            f'execute if score #demo {OBJ} matches 1.. run scoreboard players add #dt {OBJ} 1']
    for k, name in enumerate(DEMOS, 1):
        tick.append(f'execute if score #demo {OBJ} matches {k} as @e[type=minecraft:armor_stand,tag={DEMO},limit=1] '
                    f'run function {T}e/{name}')
        tick.append(f'execute if score #demo {OBJ} matches {k} if score #dt {OBJ} matches {DEMO_LEN[name]}.. run '
                    f'scoreboard players set #demo {OBJ} 0')
    tick.append(f'schedule function {T}e/tick 1t replace')
    W.w('test/e/tick', tick)
    for k, (name, events) in enumerate(DEMOS.items(), 1):
        W.w(f'test/{name}', [f'# Demo of fx/p/{name} on the vanilla stand-in (made by test/stage when missing): the preset at',
                             '# its executor point with test values, next to the calls that go with it in the fight.',
                             f'execute unless entity @e[type=minecraft:armor_stand,tag={DEMO},limit=1] run function {T}stage',
                             INIT, f'scoreboard players set #demo {OBJ} {k}', f'scoreboard players set #dt {OBJ} -1',
                             f'schedule function {T}e/tick 1t replace'])
        lines = [f'# Demo "{name}" events (as the stand-in; #dt = the demo tick).']
        for tk, where, line in sorted(events, key=lambda e: e[0]):
            lines.append(f'execute if score #dt {OBJ} matches {tk} {DEMO_WHERE[where]} run {line}')
        W.w(f'test/e/{name}', lines)
    W.w('test/sounds', ['# Click through the sound recipes (tellraw list).',
                        'tellraw @s [{"text":"타키 sounds: ","color":"#F2C230"}' +
                        ''.join(f',{{"text":"[{n}] ","color":"#FFE7A0","click_event":{{"action":"run_command",'
                                f'"command":"/execute at @s run function {FN}snd/{n}"}}}}' for n in SOUNDS) + ']'])
    W.w('test/hud', ['# The HUD lines: the mantle badge and a half gauge (run in a fight to see the boss bar), then the',
                     '# element badge after 3 s.', hud('badge', el=9), hud('gauge', pct=50),
                     f'schedule function {T}e/hud2 60t replace'])
    W.w('test/e/hud2', [hud('clear'), hud('badge', el=1)])
    W.w('test/props', ['# Every prop look on a display ahead of the executor (removed by test/stop).',
                       f'kill @e[type=minecraft:item_display,tag={DEMO}]'] +
        [f'execute positioned ^{num(6.0 - 4.0 * i)} ^1.2 ^8 run summon minecraft:item_display ~ ~ ~ '
         f'{{Tags:["{DEMO}","{DEMO}_p{i}","rlk_room","rlk_mb_aux"]}}' for i in range(len(PROPS))] +
        [f'execute as @e[type=minecraft:item_display,tag={DEMO}_p{i},limit=1] at @s rotated as @p run tp @s ~ ~ ~ ~180 0'
         for i in range(len(PROPS))] +
        [f'execute as @e[type=minecraft:item_display,tag={DEMO}_p{i},limit=1] run function {FN}prop/{name}'
         for i, name in enumerate(PROPS)])
    kinds = ['# Every fx kind in rows in front of the executor (3 s each):',
             f'# /execute as @p at @s rotated ~ 0 run function {T}kinds']
    for i, kind in enumerate(ALL_KINDS):
        row, colm = divmod(i, 7)
        x = 6.0 - 2.0 * colm
        z = 5 + 2.6 * row
        plane = kind_info(kind)[0]
        if plane == 'flat':
            kinds.append(card(kind, f'^{num(x)} ^0.1 ^{num(z)}', '~ 0', s0=0.3, s1=1.0, life=60, fade=10))
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
        'generator': 'tools/build_mboss_tk_fx.py', 'api': 'tools/mboss_tachy/api.py §8; scratchpad tk/contract.md §3.3',
        'functions': FN, 'item_models': NS_TEX, 'font': FONT, 'font_range': [f'U+{CP_LO:04X}', f'U+{CP_HI:04X}'],
        'storage': f'{STO} fx.*',
        'owned': {'dirs': [f'{FDIR}/{d}' for d in OWNED_DIRS], 'files': [f'{FDIR}/{f}.mcfunction' for f in OWNED_FILES],
                  'rp': [f'assets/rlk/textures/{TEXDIR}', f'assets/rlk/models/item/{TEXDIR}', f'assets/rlk/items/{TEXDIR}',
                         f'assets/rlk/font/{FONT_NAME}.json', f'assets/rlk/textures/font/{FONT_NAME}']},
        'caps': {'fx': CAP, 'ambient_soft': SOFT, 'cocoon': 'replaced per call (3 cards)'},
        'objectives': [OBJ] + list(OBJECTIVES), 'fake_players': f'{", ".join(FAKE)} (objective {OBJ})',
        'tags': [TAG, f'{TAG}_c', COC, f'{TAG}_new', f'{TAG}_go', f'{TAG}_sh', f'{TAG}_fd', f'{TAG}_hit', DEMO],
        'kinds': {k: {'plane': kind_info(k)[0], 'px': list(kind_info(k)[1]), 'extent': [r4(v) for v in kind_info(k)[2]],
                      'tint': 'neutral' if kind_info(k)[3] else 'painted', 'texture': kind_info(k)[4],
                      'source': 'own' if k in KINDS else 'rift (S1 model or fallback)' if k in RIFT else 'fg kit (referenced)',
                      'desc': kind_info(k)[5]} for k in ALL_KINDS},
        'fg_references': {k: FG_TEX + v for k, v in REF.items()},
        'rift_models': {k: RIFT_MODEL + v[0] for k, v in RIFT.items()},
        'atlas_px_new': atlas_px(), 'atlas_budget': ATLAS_BUDGET,
        'presets': {k: {'args': v[1], 'doc': v[0], 'cards': preset_cards(k), 'el_split': v[4],
                        'ambient': k in AMBIENT, 'particles_only': k in PTCL} for k, v in PRESETS.items()},
        'props': {k: v[0] for k, v in PROPS.items()},
        'sounds': {k: {'use': v[0], 'layers': [list(l) for l in v[1]]} for k, v in SOUNDS.items()},
        'sounds_beyond_api': list(EXTRA_SOUNDS),
        'hud': {k: list(v) for k, v in api.KIT_HUD.items()},
        'badges': {str(k): {'name': v[0], 'colour': v[1]} for k, v in BADGES.items()},
        'glyphs': {k: f'U+{v[0]:04X}' for k, v in GLYPHS.items()},
        'gate_icon': api.GATE_ICON_MODEL,
        'demos': {k: DEMO_LEN[k] for k in DEMOS},
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
    msg = (f'tachy fx kit: {n} functions ({removed} stale removed), {len(PRESETS)} presets, {len(SOUNDS)} sounds, '
           f'{len(PROPS)} props')
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error('--resourcepack is required unless --skip-rp')
        k, nref, px, g, s1 = build_resourcepack(a.resourcepack)
        msg += (f', {k} sprites ({px / 1e6:.3f} M new px), {nref} fg references, {g} glyphs in {FONT}, arrival tear: '
                + ('S1 rift models' if s1 else 'fallback card'))
    print(msg)


if __name__ == '__main__':
    main()
