"""Display-only lightning for Narukami eyes, stakes and the illusion challenge.

Generate independently of the encounter controller. Object IDs may be reused
by later patterns, so persistent effects follow a separate unique owner serial.
Illusion cues are identical for the real and the fake illusions (only the number
of slashes tells them apart); each slash adds a swing arc and a flying sword wave.

Every model is a handful of flat painted cards (raiden_obj_cards.py) using the
gradient sprites of build_raiden_fx_textures.py (rlk:raiden/fxg/*):
  eye     crackling orbit rings (chakra_*) tilted like a gyroscope, an electric rim
          with inner glow (orb_rim) on four crossed planes around the orb, an arc
          leaping off every fin and spark dots; the two frames swap tilt and sprites.
  stake   spiralling current (pillar_*) on four crossed planes through the stake,
          arcs jumping over its cap and two lightning forks; frames alternate.
  cue     warn_slash: one thin crackling glint (blade_a, cool tint) on two crossed
          planes along the cut; strike_slash: hot forked bolt over a soft beam glow.
  swing   a curved ribbon of chord cards (obj_swing_band: bright newest end, gradient
          tail back to the swing start, the cut dropping slightly) over a flat
          blade-light crescent, with a flare where the blade leaves the arc;
          swing_fade: purple afterglow trail (blade_trail_*).
  wave    layered crescent: flat crescent_b sheet, a lens-shaped front band of chord
          cards (obj_wave_band) with a dimmer wider band behind it, two lightning
          tails and spark dots; wave_fade dissolves (obj_wave_fade, bolt_fade_*).
  break   radial flash on crossed planes, impact sparks, a burst ring, flying shards
          (obj_shard) and a strike from above; *_fade keeps a wider dim residue.
          flower_break is the cyan-tinted petal variant; hit reuses object_break small.
"""
from pathlib import Path
import argparse
import math

from raiden_obj_cards import Model, save, ensure_textures, fx_names, polar, FULL, MIRROR_U

DP = Path(__file__).resolve().parents[1]
args = argparse.ArgumentParser()
args.add_argument('--resourcepack', required=True)
RP = Path(args.parse_args().resourcepack)
OUT = DP / 'data/rlk/function/boss/raiden/object_vfx'
SCALE = 4
FX = fx_names()
FOLDER = 'fx_object'
# Constant item tints (RGB multiply): cool warning glint, cyan flower burst, dim residues.
TINT_WARN = 0xA8C4FF
TINT_FLOWER = 0x9CE8FF
TINT_FLOWER_FADE = 0x6C9FD6
TINT_RESIDUE = 0x9A86CC
TINT_SHEET_FADE = 0x7C68AE


def write(name, lines):
    p = OUT / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def new():
    return Model(SCALE, FX)


def spark(m, p, size=0.24, tint=False):
    """Small cyan-white spark dot on two crossed vertical planes."""
    m.crossed(p, size, 'spark', planes=2, tint=tint)


def mirror(uv, on):
    return (uv[2], uv[1], uv[0], uv[3]) if on else uv


# --------------------------------------------------------------------------- eyes
ORB_Y = 0.77          # electro_orb centre: display y 0.3 + model 12..19 px


def eye(variant):
    m = new()
    v = variant
    c = (0.0, ORB_Y, 0.0)
    ring = ('chakra_a', 'chakra_b')
    # Crackling rim hugging the orb (ring radius 0.40 of the card, transparent centre) on four
    # crossed planes, so one of them is always nearly face-on, plus a faint inner glow.
    m.crossed(c, 0.92, ring[v], planes=4, flip=bool(v))
    m.crossed(c, 0.95, 'glow_soft', planes=2)
    # Two tilted orbits around it like a gyroscope; the frames swap their tilt.
    m.card(c, 'y', '+x', '+z', 1.5, 1.5, ring[1 - v], FULL, ('x', 45.0 if v == 0 else -45.0))
    m.card(c, 'y', '+z', '+x', 1.38, 1.38, ring[v], MIRROR_U, ('z', -45.0 if v == 0 else 45.0))
    # One arc leaping off each fin (fin tips at 0.55 from the centre), alternating sides.
    arcs = ('arc_a', 'arc_b')
    for k, theta in enumerate((90.0, -90.0, 0.0, 180.0)):
        tip = polar(0.53, theta, ORB_Y)
        tex = arcs[(k + v) % 2]
        tilt = 22.5 if (k + v) % 2 == 0 else 0.0
        if theta in (90.0, -90.0):
            side = 1 if theta > 0 else -1
            m.anchored((0.06 if side > 0 else 0.94, 0.86), tip, 'z', '+x', '-y', 1.05, 0.52, tex,
                       mirror(FULL, side < 0), ('z', side * tilt))
        else:
            side = 1 if theta == 0.0 else -1
            m.anchored((0.06 if side > 0 else 0.94, 0.86), tip, 'x', '+z', '-y', 1.05, 0.52, tex,
                       mirror(FULL, side < 0), ('x', -side * tilt))
    for k in range(4):
        a = 45 + 90 * k + (22.5 if v else 0)
        spark(m, polar(0.66 + 0.1 * ((k + v) % 2), a, ORB_Y + (0.32 if (k + v) % 2 else -0.22)))
    return m


# --------------------------------------------------------------------------- stakes
STAKE_TOP = 1.29      # cap of the lightning_stake model (spike up to 1.4)


def stake(variant):
    m = new()
    v = variant
    pil = ('pillar_a', 'pillar_b')
    # Spiralling current: three winding bolts per plane, four planes through the axis, so
    # the strands weave in and out from behind the 0.3-wide stake.
    for k, theta in enumerate((90.0, 0.0, 45.0, 135.0)):
        tex = pil[(k + v) % 2]
        m.vcard((0.0, 0.98, 0.0), theta, 1.25 - 0.1 * (k % 2), 1.96, tex, mirror(FULL, (k + v) % 2 == 1))
    # Arcs jumping over the cap.
    m.anchored((0.5, 0.86), (0.0, STAKE_TOP - 0.02, 0.0), 'z', '+x', '-y', 0.86, 0.46, 'arc_a' if v == 0 else 'arc_b')
    m.anchored((0.5, 0.86), (0.0, STAKE_TOP + 0.04, 0.0), 'x', '+z', '-y', 0.74, 0.40, 'arc_b' if v == 0 else 'arc_a',
               MIRROR_U)
    # Two forks leaping off the stake (left/right on one frame, front/back on the other).
    bolts = ('bolt_b', 'bolt_d')
    for side in (-1, 1):
        y = 1.02 + 0.12 * side * (1 if v else -1)
        if v == 0:
            start = (side * 0.12, y, 0.0)
            m.anchored((0.02 if side > 0 else 0.98, 0.5), start, 'z', '+x', '-y', 1.05, 0.30, bolts[0],
                       mirror(FULL, side < 0), ('z', -side * 22.5))
        else:
            start = (0.0, y, side * 0.12)
            m.anchored((0.02 if side > 0 else 0.98, 0.5), start, 'x', '+z', '-y', 1.05, 0.30, bolts[1],
                       mirror(FULL, side < 0), ('x', side * 22.5))
    for k in range(3):
        a = 120 * k + (60 if v else 0)
        spark(m, polar(0.34, a, 0.45 + 0.42 * k))
    return m


# --------------------------------------------------------------------------- illusion cue
CUE_C = (0.0, 1.38, 0.38)     # the glint runs from (-1.13, 0.83) to (1.13, 1.93) at z 0.38


def cue(contact):
    m = new()
    if not contact:
        m.tint = TINT_WARN
        m.card(CUE_C, 'z', '+x', '-y', 2.6, 0.30, 'blade_a', FULL, ('z', 22.5), True)
        m.card(CUE_C, 'y', '+x', '+z', 2.6, 0.30, 'blade_b', FULL, ('z', 22.5), True)
        return m
    back = (CUE_C[0], CUE_C[1], CUE_C[2] - 0.03)
    m.card(back, 'z', '+x', '-y', 2.75, 0.36, 'glow_strip', FULL, ('z', 22.5))
    m.card(CUE_C, 'z', '+x', '-y', 2.6, 0.62, 'bolt_a', FULL, ('z', 22.5))
    m.card(CUE_C, 'y', '+x', '+z', 2.6, 0.42, 'blade_c', FULL, ('z', 22.5))
    for s in (-1, 1):
        spark(m, (s * 1.18, CUE_C[1] + s * 0.50, CUE_C[2] + 0.02), 0.34)
    return m


# --------------------------------------------------------------------------- swing arc
SWING_R = 1.85
SWING_TOP = 1.863     # ribbon card top; obj_swing_band's line runs v 0.27 -> 0.73 (y 1.62 -> 1.20)
SWING_H = 0.9
CHORDS = 9            # vertices at -101.25 + 22.5 k: every chord lies at a multiple of 22.5 deg


def swing(fade):
    m = new()
    half = 2 * SWING_R * math.sin(math.radians(11.25))
    for k in range(CHORDS):
        phi = -90.0 + 22.5 * k                       # chord midpoint direction
        mid = polar(SWING_R * math.cos(math.radians(11.25)), phi)
        u0, u1 = 16 * k / CHORDS, 16 * (k + 1) / CHORDS
        if not fade:
            m.vcard((mid[0], SWING_TOP - SWING_H / 2, mid[2]), phi + 90, half + 0.01, SWING_H, 'obj_swing_band',
                    (u0, 0, u1, 16))
        else:
            # level afterglow trail, stepped down with the cut (u=0 of blade_trail = newest)
            y = 1.62 - 0.42 * (k + 0.5) / CHORDS
            m.vcard((mid[0], y, mid[2]), phi + 90, half + 0.01, 0.42, 'blade_trail_a', (16 - u0, 0, 16 - u1, 16))
    H = SWING_R / 0.94
    if not fade:
        m.hcard((0.0, 1.41, H / 2), 90.0, 2 * H, H, 'crescent_a')
        tip = polar(SWING_R, 103.0, 1.2)
        m.crossed(tip, 0.75, 'flash', planes=2)
        m.anchored((0.06, 0.86), tip, 'z', '+x', '-y', 0.7, 0.35, 'arc_b', FULL, ('z', 22.5))
    else:
        m.tint = TINT_SHEET_FADE
        m.hcard((0.0, 1.40, H / 2 - 0.1), 90.0, 2 * H * 1.04, H * 1.04, 'crescent_a', FULL, True)
    return m


# --------------------------------------------------------------------------- flying sword wave
WAVE_Y = 1.18
WAVE_W, WAVE_D = 3.47, 1.38            # crescent card: tips at x = +-1.55, sagitta 0.9
WAVE_APEX = 0.62
WAVE_PIVOT = WAVE_APEX - 0.94 * WAVE_D


def wave_edge(phi):
    """Plan-view point of the crescent's cutting edge at texture angle phi (deg)."""
    p = math.radians(phi)
    return (0.94 * math.sin(p) * WAVE_W / 2, WAVE_PIVOT + 0.94 * math.cos(p) * WAVE_D)


def wave_chords(grow=1.0, back=0.0):
    """Edge polyline whose chords point exactly at 45/67.5/90/112.5/135 deg: the tangent
    lines of the edge at those directions, cut at their intersections and at the tips
    (phi = +-70). Scaled by `grow` about the apex, then moved `back`.
    Returns [(center (x, z), theta, length, x0, x1)]."""
    A, B = 0.94 * WAVE_W / 2, 0.94 * WAVE_D
    lines = []
    for theta in (45.0, 67.5, 90.0, 112.5, 135.0):
        phi = math.atan(-A / (B * math.tan(math.radians(theta)))) if theta != 90.0 else 0.0
        p = wave_edge(math.degrees(phi))
        lines.append((p, (math.sin(math.radians(theta)), math.cos(math.radians(theta))), theta))

    def meet(l1, l2):
        (p, d), (q, e) = (l1[0], l1[1]), (l2[0], l2[1])
        det = d[0] * -e[1] - d[1] * -e[0]
        t = ((q[0] - p[0]) * -e[1] - (q[1] - p[1]) * -e[0]) / det
        return (p[0] + d[0] * t, p[1] + d[1] * t)

    def foot(l, pt):
        (p, d) = l[0], l[1]
        t = (pt[0] - p[0]) * d[0] + (pt[1] - p[1]) * d[1]
        return (p[0] + d[0] * t, p[1] + d[1] * t)
    verts = [foot(lines[0], wave_edge(-70.0))]
    verts += [meet(a, b) for a, b in zip(lines, lines[1:])]
    verts.append(foot(lines[-1], wave_edge(70.0)))
    verts = [(x * grow, WAVE_APEX + (z - WAVE_APEX) * grow - back) for x, z in verts]
    out = []
    for (a, b), line in zip(zip(verts, verts[1:]), lines):
        L = math.dist(a, b) + 0.02
        out.append((((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), line[2], L, a[0], b[0]))
    return out


def wave(fade):
    m = new()
    if not fade:
        m.hcard((0.0, WAVE_Y - 0.02, WAVE_PIVOT + WAVE_D / 2), 90.0, WAVE_W, WAVE_D, 'crescent_b')
    else:
        m.tint = TINT_RESIDUE
        m.hcard((0.0, WAVE_Y - 0.02, WAVE_PIVOT + WAVE_D / 2 - 0.15), 90.0, WAVE_W * 1.06, WAVE_D * 1.1, 'crescent_a',
                FULL, True)
    layers = [(1.0, 0.0, 0.70, 'obj_wave_fade' if fade else 'obj_wave_band')]
    if not fade:
        layers.insert(0, (1.12, 0.16, 0.95, 'obj_wave_fade'))     # wider, dimmer purple layer behind
    for grow, back, height, tex in layers:
        chords = wave_chords(grow, back)
        span = chords[-1][4]
        for (cx, cz), q, L, x0, x1 in chords:
            u0 = 16 * (x0 / span + 1) / 2
            u1 = 16 * (x1 / span + 1) / 2
            m.vcard((cx, WAVE_Y, cz), q, L, height, tex, (u0, 0, u1, 16))
    tails = ('bolt_fade_a', 'bolt_fade_c') if fade else ('blade_b', 'bolt_c')
    for side in (-1, 1):
        x = side * 0.55
        for normal, k in (('x', 0), ('y', 1)):
            tex = tails[(k + (side > 0)) % 2]
            vax = '-y' if normal == 'x' else '+x'
            m.card((x, WAVE_Y + 0.08, -0.45), normal, '-z', vax, 1.75, 0.34 if k == 0 else 0.28, tex,
                   mirror(FULL, side > 0), ('z' if normal == 'x' else 'x', 0.0), fade)
    if not fade:
        for k, (phi, dy) in enumerate(((-52, 0.22), (-18, -0.2), (14, 0.26), (48, -0.16))):
            x, z = wave_edge(phi)
            spark(m, (x * 1.04, WAVE_Y + dy, z + 0.08), 0.26 if k % 2 else 0.3)
    return m


# --------------------------------------------------------------------------- break / hit bursts
BURST_Y = 0.9


def burst(flower, fade):
    m = new()
    c = (0.0, BURST_Y, 0.0)
    t = True
    if flower:
        m.tint = TINT_FLOWER_FADE if fade else TINT_FLOWER
    elif fade:
        m.tint = TINT_RESIDUE
    else:
        t = False
    grow = 1.55 if fade else 1.0
    if not fade:
        m.crossed(c, 2.3, 'flash', planes=4, tint=t)
        m.vcard(c, 22.5, 2.5, 2.5, 'impact_sparks', FULL, t)
        m.vcard(c, 112.5, 2.5, 2.5, 'impact_sparks', MIRROR_U, t)
        # a strike from above landing on the object (vbolt impact bloom at v 0.965)
        for theta in (67.5, -22.5):
            m.vcard((0.0, BURST_Y - 0.035 * 1.65 + 1.65 / 2, 0.0), theta, 0.95, 1.65, 'vbolt_b', FULL, t)
    else:
        m.crossed(c, 1.5, 'glow_soft', planes=2, tint=t)
        for theta in (67.5, -22.5):
            m.vcard((0.0, BURST_Y + 0.75, 0.0), theta, 0.95, 1.65, 'vbolt_after_c', FULL, t)
    ring = 'chakra_a' if flower and not fade else 'shockwave'
    size = (2.6 if ring == 'shockwave' else 2.9) * grow
    m.card((0.0, BURST_Y - 0.12, 0.0), 'y', '+x', '+z', size, size, ring, FULL, None, t)
    # Flying shards: four axis-aligned ones tilted up/down, four diagonal level ones.
    count = 10 if flower else 8
    for k in range(count):
        theta = 45.0 * k + (22.5 if k >= 8 else 0.0)
        r = (0.78 + 0.22 * (k % 3)) * grow
        y = BURST_Y + (0.25, -0.18, 0.4, -0.05, 0.12, -0.25, 0.32, 0.0, 0.2, -0.1)[k] * grow
        size = (0.52 if k % 2 == 0 else 0.42) * (0.8 if fade else 1.0)
        p = polar(r, theta, y)
        if theta % 90 == 0:
            # vertical card along the radial direction, tilted about its normal (up/down)
            normal = 'x' if theta % 180 == 0 else 'z'
            s = math.cos(math.radians(theta)) + math.sin(math.radians(theta))
            uax = ('+z' if s > 0 else '-z') if normal == 'x' else ('+x' if s > 0 else '-x')
            tilt = (22.5 if k % 4 == 0 else -22.5)
            # positive tilt raises the outward end for every heading
            sign = {('x', '+z'): -1, ('x', '-z'): 1, ('z', '+x'): 1, ('z', '-x'): -1}[(normal, uax)]
            m.card(p, normal, uax, '-y', size, size, 'obj_shard', FULL, (normal, sign * tilt), t)
        else:
            m.vcard(p, theta, size, size, 'obj_shard', FULL, t)
    return m


def build_models():
    used = set()
    stats = []

    def put(name, model):
        used.update(v.split('/')[-1] for v in model.textures.values())
        stats.append((name, save(RP, FOLDER, name, model)))
    for v in (0, 1):
        put(f'eye_{v}', eye(v))
        put(f'stake_{v}', stake(v))
    put('warn_slash', cue(False))
    put('strike_slash', cue(True))
    put('swing', swing(False))
    put('swing_fade', swing(True))
    put('wave', wave(False))
    put('wave_fade', wave(True))
    for flower in (False, True):
        base = 'flower_break' if flower else 'object_break'
        put(base, burst(flower, False))
        put(base + '_fade', burst(flower, True))
    ensure_textures(RP, used)
    return stats


STATS = build_models()


def spawn(name, kind, owned=True, life=0):
    lines = [
        'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_object_fx","rlk_rd_ofnew"],'
        'NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:0,'
        'brightness:{sky:15,block:15},view_range:3f,width:6f,height:6f,shadow_radius:0f,'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_object/' + name + '"}},'
        'transformation:{translation:[0f,0f,0f],scale:[4f,4f,4f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}',
        'data modify entity @e[tag=rlk_rd_ofnew,limit=1] Rotation set from entity @s Rotation',
        'data modify entity @e[tag=rlk_rd_ofnew,limit=1] Rotation[1] set value 0f',
        f'scoreboard players set @e[tag=rlk_rd_ofnew] rdOvKind {kind}',
        'scoreboard players set @e[tag=rlk_rd_ofnew] rdOvAge -1',
        f'scoreboard players set @e[tag=rlk_rd_ofnew] rdOvLife {life}',
    ]
    if owned:
        lines += ['scoreboard players operation @e[tag=rlk_rd_ofnew,limit=1] rdOvId = @s rdOvId',
                  'scoreboard players operation @e[tag=rlk_rd_ofnew,limit=1] rdObjId = @s rdObjId']
    lines += ['tag @e[tag=rlk_rd_ofnew] remove rlk_rd_ofnew']
    return lines


(OUT / 'cross.mcfunction').unlink(missing_ok=True)  # retired real-illusion X cue
write('init', [f'scoreboard objectives add {name} dummy' for name in
               ['rdOvId', 'rdOvKind', 'rdOvAge', 'rdOvLife']])
write('create', [
    '# Call once as every newly created gameplay object, including flower/illusion.',
    'scoreboard players add #rdObjectSerial rd 1',
    'scoreboard players operation @s rdOvId = #rdObjectSerial rd',
    'execute if score @s rdObjKind matches 1 run function rlk:boss/raiden/object_vfx/eye',
    'execute if score @s rdObjKind matches 4 run function rlk:boss/raiden/object_vfx/stake',
])
write('eye', spawn('eye_0', 1))
write('stake', spawn('stake_0', 2))
cue_lines = ['$scoreboard players set @e[tag=rlk_rd_ofnew] rdOvLife $(life)' if line.endswith(' rdOvLife 0') else line
             for line in spawn('warn_slash', 5)]
assert any(line.startswith('$') for line in cue_lines)
write('illusion_cue', [
    '# As an illusion facing the arena centre, {life:<ticks until its slash>}. Identical',
    '# for the real and the fake illusions; it disappears with its owner.',
] + cue_lines)
swing_lines = spawn('swing', 6, owned=False, life=4)
wave_lines = spawn('wave', 7, owned=False, life=5)
wave_lines.insert(-1, 'data merge entity @e[tag=rlk_rd_ofnew,limit=1] {teleport_duration:1}')
write('slash', [
    '# As the slashing illusion at its feet, facing the centre: swing arc + flying wave.',
] + swing_lines + wave_lines)
write('break', [
    '# Detached burst survives its destroyed owner for nine ticks, then disappears.',
    'execute if score @s rdObjKind matches 3 run function rlk:boss/raiden/object_vfx/flower_break',
    'execute unless score @s rdObjKind matches 3 run function rlk:boss/raiden/object_vfx/object_break',
])
write('flower_break', spawn('flower_break', 4, owned=False, life=9))
write('object_break', spawn('object_break', 3, owned=False, life=9))
hit = spawn('object_break', 3, owned=False, life=5)
hit.insert(-1, 'data merge entity @e[tag=rlk_rd_ofnew,limit=1] {transformation:{translation:[0f,.5f,0f],scale:[1.8f,1.8f,1.8f]}}')
write('hit', hit)
write('clear', ['kill @e[tag=rlk_rd_object_fx]'])
write('world', ['execute as @e[tag=rlk_rd_object_fx] at @s run function rlk:boss/raiden/object_vfx/tick'])
write('owner', [
    'scoreboard players operation #rdOvOwner rd = @s rdOvId',
    'scoreboard players set #rdOvExists rd 0',
    'execute as @e[tag=rlk_rd_object] if score @s rdOvId = #rdOvOwner rd run scoreboard players set #rdOvExists rd 1',
])
setmodel = lambda name: 'data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/' + name + '"'
write('cue_tick', [
    'scoreboard players operation #rdOvLeft rd = @s rdOvLife',
    'scoreboard players operation #rdOvLeft rd -= @s rdOvAge',
    'execute if score #rdOvLeft rd matches 3 run ' + setmodel('strike_slash'),
])
write('tick', [
    'execute if score @s rdOvKind matches 1..2 run function rlk:boss/raiden/object_vfx/owner',
    'execute if score @s rdOvKind matches 5 run function rlk:boss/raiden/object_vfx/owner',
    'execute if score @s rdOvKind matches 1..2 if score #rdOvExists rd matches 0 run return run kill @s',
    'execute if score @s rdOvKind matches 5 if score #rdOvExists rd matches 0 run return run kill @s',
    'scoreboard players add @s rdOvAge 1',
    'execute if score @s rdOvLife matches 1.. if score @s rdOvAge >= @s rdOvLife run return run kill @s',
    'scoreboard players operation #rdOvFrame rd = @s rdOvAge',
    'scoreboard players set #rdOvEight rd 8',
    'scoreboard players operation #rdOvFrame rd %= #rdOvEight rd',
    'execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 0 run ' + setmodel('eye_0'),
    'execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 4 run ' + setmodel('eye_1'),
    'execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 0 run ' + setmodel('stake_0'),
    'execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 4 run ' + setmodel('stake_1'),
    # Illusion cue (5) charges for its last three ticks; it dies on the slash tick.
    'execute if score @s rdOvKind matches 5 run function rlk:boss/raiden/object_vfx/cue_tick',
    # Swing arc (6) fades; the sword wave (7) flies 5.5 blocks a tick to the line's end.
    'execute if score @s rdOvKind matches 6 if score @s rdOvAge matches 2 run ' + setmodel('swing_fade'),
    'execute if score @s rdOvKind matches 7 if score @s rdOvAge matches 1.. run tp @s ^ ^ ^5.5',
    'execute if score @s rdOvKind matches 7 if score @s rdOvAge matches 3 run ' + setmodel('wave_fade'),
    'execute if score @s rdOvKind matches 3 if score @s rdOvAge matches 3 run ' + setmodel('object_break_fade'),
    'execute if score @s rdOvKind matches 4 if score @s rdOvAge matches 3 run ' + setmodel('flower_break_fade'),
])
print(f'Generated {len(STATS)} painted-card object lightning models (eyes, stakes, illusion cue/swing/wave, '
      f'break bursts; {min(n for _, n in STATS)}-{max(n for _, n in STATS)} cards each).')
