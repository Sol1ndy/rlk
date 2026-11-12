#!/usr/bin/env python3
"""Renders of the 아를레키노 fx kit: s1k_sprites.jpg (the painted sprites, tinted as used) and s1k_presets.jpg (one strip
per preset / prop / decal: three moments of the kit's own functions run in the test harness, next to the matching
footage frame). See render_kn_core.py (the card ray caster of the Tachy / Apep kit renders).

    python3 render_kn.py <worktree roguelike dir> <resource pack> <out dir>
"""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_kn_core as R  # noqa: E402

G, api, np = R.G, R.api, R.np
Image, ImageDraw = R.Image, R.ImageDraw
SRC = R.S / 'ar/src'
P0 = R.P0
FW, FH = 134, 90
LW = 96


# ----------------------------------------------------------------------------- sprite sheet
NEUTRAL_TINT = {'flame': [G.PYRO, G.CRIM], 'ember': [G.EMBER, G.CRIM], 'streak': [G.PYRO, G.CRIM], 'burst': [G.PYRO, G.CRIM],
                'wisp_0': [G.WHITE, G.SPIRIT[2]], 'wisp_1': [G.WHITE], 'wisp_2': [G.WHITE]}


def tinted(kind, col, scale):
    T = R.tex(G.NS_TEX + kind)
    c = np.array([(col >> 16) & 255, (col >> 8) & 255, col & 255]) / 255
    im = Image.fromarray((np.concatenate([T[..., :3] * c, T[..., 3:4]], -1) * 255).astype(np.uint8), 'RGBA')
    return im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.NEAREST)


def sprites():
    items = []
    for k, v in G.KINDS.items():
        w, h = v[1]
        sc = 2 if max(w, h) <= 32 else 1 if max(w, h) <= 64 else 0.75 if max(w, h) <= 128 else 0.5
        for col in NEUTRAL_TINT.get(k, [G.WHITE]):
            items.append((k if col == G.WHITE or len(NEUTRAL_TINT.get(k, [])) < 2 else f'{k} c{1 + NEUTRAL_TINT[k].index(col)}',
                          tinted(k, col, sc)))
    W, pad = 640, 5
    f = R.font(10)
    x = y = rowh = 0
    pos = []
    for name, im in items:
        w, h = max(im.width, 6 * len(name)) + pad * 2, im.height + 14 + pad
        if x + w > W:
            x, y, rowh = 0, y + rowh, 0
        pos.append((x, y))
        x += w
        rowh = max(rowh, h)
    H = y + rowh + 26
    sheet = Image.new('RGBA', (W, H), (58, 62, 60, 255))
    d = ImageDraw.Draw(sheet)
    d.text((6, H - 22), f'kn_kit: {len(G.KINDS)} own sprites, {G.atlas_px()} px (budget 700 000); fg references '
           f'{", ".join(G.REF)}; neutral ones in their tints', fill=(235, 235, 235, 255), font=f)
    for (name, im), (x, y) in zip(items, pos):
        sheet.alpha_composite(im, (x + pad, y + 13))
        d.text((x + pad, y + 1), name, fill=(255, 220, 220, 255), font=f)
    sheet.convert('RGB').save(R.OUT / 's1k_sprites.jpg', quality=86)
    print('s1k_sprites.jpg', sheet.size)


# ----------------------------------------------------------------------------- stand-in body (2.8 b, x 1.25 of Tachy's)
BODY = [((0.0, 0.7, 0.0), (0.3, 0.7, 0.25), (0.14, 0.12, 0.12)), ((0.0, 1.8, 0.0), (0.4, 0.55, 0.27), (0.85, 0.85, 0.82)),
        ((0.0, 2.55, 0.0), (0.21, 0.24, 0.21), (0.9, 0.88, 0.86)), ((0.0, 1.75, -0.4), (0.7, 1.0, 0.12), (0.12, 0.1, 0.1)),
        ((-0.7, 1.5, 0.7), (0.05, 0.05, 1.4), (0.55, 0.06, 0.1))]


def standin(at):
    def draw(img, cam, depth):
        O, D = cam.rays()
        for off, rad, col in BODY:
            c = np.array(at) + np.array(off)
            lo = (O - c) / np.array(rad)
            ld = D / np.array(rad)
            A = (ld * ld).sum(-1)
            B = 2 * (lo * ld).sum(-1)
            C = (lo * lo).sum(-1) - 1
            disc = B * B - 4 * A * C
            t = np.full(A.shape, np.inf)
            ok = disc >= 0
            t1 = (-B - np.sqrt(np.where(ok, disc, 0))) / (2 * A)
            good = ok & (t1 > 1e-4)
            t[good] = t1[good]
            m = t < depth
            if m.any():
                img[m] = np.array(col)
                depth[m] = t[m]
    return draw


# ----------------------------------------------------------------------------- strips
HEIGHT = {'slash_arc': 1.4, 'spin_ring': 1.0, 'twirl_ring': 1.5, 'scythe_form': 1.4, 'embers_puff': 1.4, 'dash_trail': 1.0,
          'leap_flare': 0.3, 'dive_streak': 6.0, 'impact_burst': 0.2, 'claw': 1.0, 'wing_burst': 1.4, 'zig_streak': 1.2,
          'brand_x': 1.0, 'threads': 0.2, 'web': 4.0, 'clone_trail': 0.0, 'blade_burst': 1.0, 'shock_gain': 1.0,
          'shock_aura': 1.3, 'shock_hit': 1.4, 'break_burst': 1.4, 'stun_motes': 2.9, 'legs_burst': 1.8, 'moon_flare': 8.0,
          'aim_line': 1.8, 'reticle': 1.8, 'beam': 1.8, 'rapid_slash': 1.2, 'wisp_turn': 1.0}
AHEAD = ('impact_burst', 'claw', 'brand_ring', 'brand_x', 'shock_gain', 'blade_rise', 'blade_burst', 'feather_hit',
         'orb_burst', 'gate_flames')
WIDE = ('threads', 'thorns', 'blast', 'wheel_trail', 'dash_trail', 'beam', 'aim_line', 'final_burst', 'pillar',
        'ambient_petals', 'moon_flare', 'orb_gather')
TICKS = {'brand_ring': (2, 9, 16), 'pillar': (3, 12, 40), 'x_mark': (6, 20, 60), 'web': (2, 6, 30), 'reticle': (3, 12, 22),
         'wheel_trail': (3, 7, 12), 'death_flames': (6, 14, 24), 'threads': (1, 3, 8), 'aim_line': (1, 2, 3),
         'stun_motes': (1, 5, 9), 'shock_aura': (2, 8, 16), 'moon_flare': (2, 8, 16), 'gate_flames': (2, 6, 10)}
SHOTS = {
    'slash_arc': [('r42 roll0 c1 t3', dict(r=42, yaw=0, pitch=0, roll=0, c=1), 3), ('r36 p-50 roll90 t3', dict(r=36, yaw=0, pitch=-50, roll=90, c=1), 3),
                  ('r56 roll10 c2 t4', dict(r=56, yaw=0, pitch=0, roll=10, c=2), 4)],
    'spin_ring': [('r46 c1 t2', dict(r=46, c=1), 2), ('r46 c1 t6', dict(r=46, c=1), 6), ('r42 c2 t4', dict(r=42, c=2), 4)],
    'dash_trail': [('c1 t2', dict(len=120, c=1), 2), ('c1 t5', dict(len=120, c=1), 5), ('c2 t3', dict(len=120, c=2), 3)],
    'impact_burst': [('r36 c1 t2', dict(r=36, c=1), 2), ('r36 c1 t5', dict(r=36, c=1), 5), ('r22 c2 t3', dict(r=22, c=2), 3)],
    'threads': [('r260 t1', dict(r=260), 1), ('r260 t4', dict(r=260), 4), ('r260 t10', dict(r=260), 10)],
    'thorns': [('r260 t1', dict(r=260), 1), ('r260 t3', dict(r=260), 3), ('r260 t8', dict(r=260), 8)],
    'blast': [('r260 t2', dict(r=260), 2), ('r260 t5', dict(r=260), 5), ('r260 t9', dict(r=260), 9)],
    'wisp_turn': [('c2 t2', dict(c=2), 2), ('c2 t5', dict(c=2), 5), ('c1 t2', dict(c=1), 2)],
    'beam': [('len200 t1', dict(len=200), 1), ('t3', dict(len=200), 3), ('t7', dict(len=200), 7)],
    'aim_line': [('len60 t1', dict(len=60), 1), ('t2', dict(len=60), 2), ('t3', dict(len=60), 3)],
    'final_burst': [('r40 t1', dict(r=40), 1), ('t3', dict(r=40), 3), ('t7', dict(r=40), 7)],
}
REF = {   # (clip, seconds): the matching footage frame
    'slash_arc': ('v2', 19.8), 'spin_ring': ('v2', 21.0), 'twirl_ring': ('v1', 2.7), 'scythe_form': ('v1', 1.45),
    'embers_puff': ('v1', 0.9), 'wheel_trail': ('v1', 17.2), 'dash_trail': ('v2', 8.0), 'leap_flare': ('v1', 27.2),
    'dive_streak': ('v1', 33.6), 'impact_burst': ('v1', 34.3), 'claw': ('v1', 24.0), 'wing_burst': ('v1', 37.0),
    'zig_streak': ('v2', 38.5), 'brand_ring': ('v3', 9.75), 'brand_x': ('v3', 10.25), 'threads': ('v3', 17.9),
    'thorns': ('v3', 18.25), 'blast': ('v3', 19.75), 'web': ('v4', 4.5), 'clone_trail': ('v4', 5.6),
    'blade_rise': ('v3', 34.5), 'blade_burst': ('v3', 36.25), 'shock_gain': ('v3', 24.6), 'shock_aura': ('v1', 22.8),
    'shock_hit': ('v3', 27.05), 'break_burst': ('v3', 27.25), 'stun_motes': ('v3', 28.5), 'pillar': ('v4', 14.0),
    'legs_burst': ('v4', 21.0), 'moon_flare': ('v7', 30.5), 'aim_line': ('v6', 16.75), 'reticle': ('v6', 17.25),
    'beam': ('v6', 17.75), 'x_mark': ('v7', 16.45), 'rapid_slash': ('v7', 18.2), 'final_burst': ('v7', 19.25),
    'feather_hit': ('v7', 32.0), 'orb_gather': ('v7', 34.0), 'orb_burst': ('v7', 38.0), 'death_flames': None,
    'wisp_turn': ('v5', 35.0), 'gate_flames': None, 'ambient_petals': ('v5', 20.0),
    'prop/wheel': ('v1', 16.3), 'prop/crescent': ('v4', 31.9), 'prop/feather': ('v7', 31.0), 'prop/orb': ('v7', 35.0),
    'prop/blade': ('v3', 35.0), 'prop/clone': ('v4', 5.75), 'prop/wisp': ('v5', 36.0), 'prop/moon_halo': ('v4', 16.5),
    'decal/flood': ('v3', 16.5), 'decal/cracks': ('v3', 21.0), 'decal/strip': ('v3', 35.25), 'decal/rim_tint': ('v3', 39.25),
    'decal/pool': ('v2', 34.0), 'decal/ring_o': ('v7', 5.25), 'decal/donut_o': ('v7', 9.8),
}


def ref_frame(key):
    ref = REF.get(key)
    if not ref:
        im = Image.new('RGB', (FW, FH), (40, 36, 38))
        ImageDraw.Draw(im).text((6, FH // 2 - 6), 'no footage (designed)', fill=(200, 200, 200), font=R.font(10))
        return im
    clip, t = ref
    with tempfile.TemporaryDirectory(dir=str(R.S / 'ar/tmp')) as d:
        out = Path(d) / 'f.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(SRC / f'{clip}.mp4'), '-frames:v', '1',
                        '-vf', f'scale={FW}:{FH}', '-y', str(out)], check=True)
        im = Image.open(out).convert('RGB')
        im.load()
    ImageDraw.Draw(im).text((2, FH - 12), f'{clip} {t:.2f}', fill=(255, 255, 0), font=R.font(9))
    return im


CLOSE = ('scythe_form', 'embers_puff', 'twirl_ring', 'shock_aura', 'stun_motes', 'legs_burst', 'shock_gain', 'brand_x',
         'blade_rise', 'blade_burst', 'wisp_turn', 'gate_flames', 'claw', 'clone_trail', 'reticle', 'feather_hit',
         'leap_flare', 'wing_burst', 'shock_hit', 'prop/wisp', 'prop/feather', 'prop/orb', 'prop/wheel', 'prop/crescent')
SIDE = {'beam': 20, 'aim_line': 6, 'dash_trail': 12, 'wheel_trail': 16, 'dive_streak': 7, 'zig_streak': 0}
NOBODY = CLOSE[:13] + ('ambient_petals', 'moon_flare')


def cam_for(key, at):
    x, y, z = at
    if key in SIDE:
        L = SIDE[key]
        return R.view_cam((x + 7 + L * 0.35, R.FY + 3.5, z + L / 2 + 2), (x, R.FY + 1.0, z + L / 2), FW, FH, fov=70)
    if key in CLOSE:
        return R.view_cam((x + 2.6, y + 1.2, z + 3.6), (x, y, z + 0.4), FW, FH, fov=70)
    if key in WIDE or key in ('decal/flood', 'decal/cracks', 'decal/rim_tint', 'decal/pool', 'decal/ring_o', 'decal/donut_o'):
        return R.view_cam((x + 14, R.FY + 13, z + 22), (x, R.FY + 0.8, z), FW, FH, fov=70)
    if key == 'decal/strip':
        return R.view_cam((x + 10, R.FY + 10, z + 16), (x, R.FY + 0.5, z), FW, FH, fov=70)
    if key == 'web':
        return R.view_cam((x + 5, R.FY + 1.6, z + 6), (x, y, z), FW, FH, fov=70)
    if key in ('moon_flare', 'prop/moon_halo', 'prop/blade', 'x_mark'):
        return R.view_cam((x + 7, R.FY + 3.0, z + 9), (x, R.FY + (y - R.FY) * 0.6 + 1.0, z), FW, FH, fov=70)
    return R.view_cam((x + 3.8, R.FY + 2.8, z + 5.4), (x, R.FY + 1.3, z + 1.0), FW, FH, fov=70)


def shot_preset(name, args, tick):
    s = R.fresh()
    h = HEIGHT.get(name, 0.0)
    at = (P0[0], R.FY + h, P0[2] + (2.5 if name in AHEAD else 0.0))
    if name == 'wisp_turn':
        s.run('summon minecraft:marker 760.5 202 8.5 {Tags:["rlk_kn_wisp"]}')
        mk = [e for e in s.ents if e.etype == 'marker'][0]
        s.run(api.K.prop('wisp', c=1), ex=mk, pos=tuple(mk.pos))
        at = tuple(mk.pos)
        s.run(G.fx(name, **args), pos=at, ex=mk)
    else:
        s.run(G.fx(name, **args), pos=at, rot=(0.0, 0.0))
    s.tick(tick)
    body = None if name in NOBODY else standin((P0[0], R.FY, P0[2]))
    return R.render(cam_for(name, at), R.sim_cards(s), s.gt, bg=(0.42, 0.5, 0.56), dts=R.dots(s), extra=body)


PROP_TICKS = (2, 6, 10)


def shot_prop(name, tick):
    s = R.fresh()
    if name in ('wisp', 'moon_halo'):
        y = R.FY + (1.0 if name == 'wisp' else 7.0)
        s.run(f'summon minecraft:marker 760.5 {y} 10.5 {{Tags:["rlk_kn_wisp"]}}')
        mk = [e for e in s.ents if e.etype == 'marker'][0]
        s.run(api.K.prop(name, **({'c': 1 if tick < 8 else 2} if name == 'wisp' else {})), ex=mk, pos=tuple(mk.pos))
        at = tuple(mk.pos)
        for k in range(tick):
            mk.pos[1] = y + 0.15 * np.sin(k / 3)
            s.tick(1)
    else:
        y = R.FY + (0.0 if name in ('blade',) else 1.2)
        s.run(f'summon minecraft:item_display 760.5 {y} 10.5 {{Tags:["rlk_kn_p"],teleport_duration:1}}')
        d = [e for e in s.ents if e.etype == 'item_display'][0]
        d.rot = [200.0 if name != 'clone' else 160.0, 0.0]          # flying toward the camera side
        s.run(api.K.prop(name), ex=d)
        for _ in range(tick):
            if name in ('wheel', 'crescent', 'feather'):
                d.pos = list(R.mcsim.Sim.local(s, R.mcsim.Ctx(d, tuple(d.pos), tuple(d.rot)), 0, 0, 0.4))
            s.tick(1)
        at = tuple(d.pos)
    cam = cam_for(f'prop/{name}', (760.5, at[1], at[2] if name in ('wheel', 'crescent', 'feather') else 10.5))
    return R.render(cam, R.sim_cards(s), s.gt, bg=(0.42, 0.5, 0.56), dts=R.dots(s), extra=standin((P0[0], R.FY, P0[2] - 1.5)))


DECAL_SHOTS = {
    'flood': [('t50: t4', dict(r=260, t=50), 4), ('t30', dict(r=260, t=50), 30), ('flash t45', dict(r=260, t=50), 45)],
    'cracks': [('t2', dict(r=260), 2), ('t12', dict(r=260), 12), ('t30', dict(r=260), 30)],
    'strip': [('t2', dict(len=280, w=30, yaw=0, t=28), 2), ('t10', dict(len=280, w=30, yaw=0, t=28), 10),
              ('flash t24', dict(len=280, w=30, yaw=0, t=28), 24)],
    'rim_tint': [('t6', dict(r0=0, r=240, t=34), 6), ('t18', dict(r0=0, r=240, t=34), 18), ('flash t30', dict(r0=0, r=240, t=34), 30)],
    'pool': [('t6', dict(r=120, t=30), 6), ('t18', dict(r=120, t=30), 18), ('flash t26', dict(r=120, t=30), 26)],
    'ring_o': [('r60 t4', dict(r=60, t=35), 4), ('r60 t20', dict(r=60, t=35), 20), ('flash t31', dict(r=60, t=35), 31)],
    'donut_o': [('r60-150 t4', dict(r0=60, r=150, t=21), 4), ('t12', dict(r0=60, r=150, t=21), 12), ('flash t17', dict(r0=60, r=150, t=21), 17)],
}


def shot_decal(name, args, tick):
    s = R.fresh()
    at = (760.5, R.FY, 8.5)
    if name == 'strip':
        s.run(G.decal('strip', **args), pos=at)
        s.run(G.decal('strip', **dict(args, yaw=90)), pos=at)
    else:
        s.run(G.decal(name, **args), pos=at)
    s.tick(tick)
    return R.render(cam_for(f'decal/{name}', at), R.sim_cards(s), s.gt, bg=(0.42, 0.5, 0.56), dts=R.dots(s),
                    extra=standin((760.5, R.FY, 8.5)))


def strips():
    f = R.font(10)
    rows = []
    for name in api.KIT_PRESETS:
        if name in SHOTS:
            shots = SHOTS[name]
        else:
            a = {k: G.TEST_ARGS[k] for k in api.KIT_PRESETS[name]}
            if name == 'final_burst':
                a = {'r': 40}
            shots = [(f't{t}', a, t) for t in TICKS.get(name, (1, 3, 7))]
        ims = [shot_preset(name, a, t) for _lab, a, t in shots]
        rows.append((name, '{' + ','.join(api.KIT_PRESETS[name]) + '}' if api.KIT_PRESETS[name] else '',
                     [lab for lab, _a, _t in shots], ims, ref_frame(name)))
        print(' ', name)
    for name in G.PROPS:
        ims = [shot_prop(name, t) for t in PROP_TICKS]
        rows.append((f'prop/{name}', '{c}' if name == 'wisp' else '', [f't{t}' for t in PROP_TICKS], ims, ref_frame(f'prop/{name}')))
        print('  prop', name)
    for name, shots in DECAL_SHOTS.items():
        ims = [shot_decal(name, a, t) for _lab, a, t in shots]
        rows.append((f'decal/{name}', '{' + ','.join(api.KIT_DECALS[name]) + '}', [lab for lab, _a, _t in shots], ims,
                     ref_frame(f'decal/{name}')))
        print('  decal', name)
    W = LW + 4 * (FW + 2)
    H = len(rows) * (FH + 2) + 24
    out = Image.new('RGB', (W, H), (22, 20, 22))
    d = ImageDraw.Draw(out)
    d.text((4, 5), 'kn_kit: three moments of each preset / prop / decal (kit functions in the test harness, plaza floor, '
           '2.8 b stand-in) | footage', fill=(255, 255, 255), font=f)
    for i, (name, args, labs, ims, ref) in enumerate(rows):
        y = 24 + i * (FH + 2)
        d.text((4, y + 3), name, fill=(255, 200, 200), font=R.font(10))
        if args:
            d.text((4, y + 18), args, fill=(200, 200, 200), font=R.font(9))
        for j, (im, lab) in enumerate(zip(ims, labs)):
            ImageDraw.Draw(im).text((3, FH - 12), lab, fill=(255, 255, 255), font=R.font(9))
            out.paste(im, (LW + j * (FW + 2), y))
        out.paste(ref, (LW + 3 * (FW + 2), y))
    out.save(R.OUT / 's1k_presets.jpg', quality=80)
    print('s1k_presets.jpg', out.size)


sprites()
strips()
