"""Display-only lightning for Narukami eyes, stakes and object break bursts.

Generate independently of the encounter controller. Object IDs may be reused
by later patterns, so persistent effects follow a separate unique owner serial.
The illusion cue / swing / sword-wave cards of the release's 찰나의 포영 are retired (S3): the
rework's clones are rig props and their volleys are kit slabs.

Every model is a handful of flat painted cards (raiden_obj_cards.py) using the
gradient sprites of build_raiden_fx_textures.py (rlk:raiden/fxg/*):
  eye     crackling orbit rings (chakra_*) tilted like a gyroscope, an electric rim
          with inner glow (orb_rim) on four crossed planes around the orb, an arc
          leaping off every fin and spark dots; the two frames swap tilt and sprites.
  stake   spiralling current (pillar_*) on four crossed planes through the stake,
          arcs jumping over its cap and two lightning forks; frames alternate.
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
    for flower in (False, True):
        base = 'flower_break' if flower else 'object_break'
        put(base, burst(flower, False))
        put(base + '_fade', burst(flower, True))
    ensure_textures(RP, used)
    return stats


STATS = build_models()


def spawn(name, kind, owned=True, life=0, roll=0):
    # roll: degrees about the display's forward (+Z) axis through chest height (the swing
    # arc's height), e.g. the two diagonal strokes of the real illusion's X slash.
    r, h = math.radians(roll), 1.2
    q = f'[0f,0f,{math.sin(r/2):.6f}f,{math.cos(r/2):.6f}f]' if roll else '[0f,0f,0f,1f]'
    t = f'[{h*math.sin(r):.6f}f,{h-h*math.cos(r):.6f}f,0f]' if roll else '[0f,0f,0f]'
    lines = [
        'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_object_fx","rlk_rd_ofnew"],'
        'NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:0,'
        'brightness:{sky:15,block:15},view_range:3f,width:6f,height:6f,shadow_radius:0f,'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_object/' + name + '"}},'
        'transformation:{translation:' + t + ',scale:[4f,4f,4f],left_rotation:' + q + ',right_rotation:[0f,1f,0f,0f]}}',
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


# Retired outputs (the release illusion's X cue, then the S3 removal of the illusion cue / swing / wave cards).
for retired in ('cross', 'illusion_cue', 'slash', 'slash_xa', 'slash_xb', 'cue_tick'):
    (OUT / (retired + '.mcfunction')).unlink(missing_ok=True)
for retired in ('warn_slash', 'strike_slash', 'swing', 'swing_fade', 'wave', 'wave_fade'):
    for kind in ('models/item', 'items'):
        (RP / 'assets/rlk' / kind / 'raiden' / FOLDER / (retired + '.json')).unlink(missing_ok=True)
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
write('tick', [
    'execute if score @s rdOvKind matches 1..2 run function rlk:boss/raiden/object_vfx/owner',
    'execute if score @s rdOvKind matches 1..2 if score #rdOvExists rd matches 0 run return run kill @s',
    'scoreboard players add @s rdOvAge 1',
    'execute if score @s rdOvLife matches 1.. if score @s rdOvAge >= @s rdOvLife run return run kill @s',
    'scoreboard players operation #rdOvFrame rd = @s rdOvAge',
    'scoreboard players set #rdOvEight rd 8',
    'scoreboard players operation #rdOvFrame rd %= #rdOvEight rd',
    'execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 0 run ' + setmodel('eye_0'),
    'execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 4 run ' + setmodel('eye_1'),
    'execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 0 run ' + setmodel('stake_0'),
    'execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 4 run ' + setmodel('stake_1'),
    'execute if score @s rdOvKind matches 3 if score @s rdOvAge matches 3 run ' + setmodel('object_break_fade'),
    'execute if score @s rdOvKind matches 4 if score @s rdOvAge matches 3 run ' + setmodel('flower_break_fade'),
])
print(f'Generated {len(STATS)} painted-card object lightning models (eyes, stakes, '
      f'break bursts; {min(n for _, n in STATS)}-{max(n for _, n in STATS)} cards each).')
