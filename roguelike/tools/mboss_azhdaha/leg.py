"""S2-L: 31 격류 범람 (Hydro orbs, cast slot -> bg slot L), 32 운석 낙하 (Pyro meteors, cast slot), 33 화염 잠식 (the Pyro
fire rule, p/firefield/on_brand) and the leg-element addon bodies AZ:xl/** (Hydro geyser / blades, Pyro lumps) at the
host patterns' ADDON_POINTS (plan.md 4.5-4.7, 5 rows 31-33, Change note 1; s2.md 6, 9, 10, 17, 18).

Telegraphs (Change note 1, the 10-20 rule): *keep* only 32's big seal (seal8 r 5.2, tell 28) and the P1 Hydro geyser
swirl (tele/disc r 3.0, tell 22); every other hazard draws no ground decal: 31 = the orb props, 32's small meteors = the
air halo + the falling prop, the Pyro lumps = the lump props in flight (26 t), the Hydro blades = the blade props inside
the host's strike group. Every hit plays its impact preset at the hit tick.

Numbers: tools/mboss_azhdaha/h_pl.py (shared with S:az/tests_pl/pat_leg.py). Scratch: fake players #aq31* #aq32* #aq33*
(patterns) and #axl* (addon bodies) in mb; entity tags rlk_mb_az_p31* / p32* (patterns), rlk_mb_az_xl* (addon bodies),
all with rlk_room rlk_mb_aux rlk_mb_az_pat.
"""
import math

import mboss_lib as L

from . import api as A
from . import h_pl as H

K = A.K
NS = A.NS
BODY = A.BODY
PLAYER = A.PLAYER
CY = A.CY
O = H.ORB
M = H.MET

EVERY2 = {z: 2 for z in A.ZONES}
EVERY1 = {z: 1 for z in A.ZONES}
PATTERNS = [
    A.Pattern(31, 'orbs', '격류 범람', 'cast', None, phases=(2, 3), elem=('leg', 2), phase_weight={2: EVERY2, 3: EVERY1},
              cooldown=600, recover=30, max_len=90, length=82, gates=('no_live', 'no_bg'),
              hooks=('cast', 'ctick', 'refresh', 'bgtick', 'cancel_bg', 'reload')),
    A.Pattern(32, 'meteor', '운석 낙하', 'cast', None, phases=(2, 3), elem=('leg', 1), phase_weight={2: EVERY2, 3: EVERY1},
              cooldown=600, recover=30, max_len=110, length=M['end'], gates=('no_live', 'field_area'),
              hooks=('cast', 'ctick', 'resume')),
]
PAT_TAGS = ['rlk_room', 'rlk_mb_aux', 'rlk_mb_az_pat']


def F(rel):
    return f'function {NS}{rel}'


def tags(*extra):
    return '[' + ','.join(f'"{t}"' for t in PAT_TAGS + list(extra)) + ']'


def n(v):
    return L.num(float(v), 3)


def body_near(r):
    return BODY.replace('limit=1', f'distance=..{n(r)},limit=1')


def mk(tag, etype='marker'):
    return f'@e[type=minecraft:{etype},tag={tag},limit=1]'


def mks(tag, etype='marker'):
    return f'@e[type=minecraft:{etype},tag={tag}]'


# =============================================================================================== shared utilities (xl/u)
def utils(g):
    """xl/u/**: random marker, clear-melee-point push, the lump and blade pieces (also used by 32)."""
    g.xw('u/rnd', ['# Macro {a, d, t}: a marker tagged t (+ rlk_mb_az_xnt) at world yaw a, d blocks from here, on the floor.',
                   f'$execute rotated $(a) 0 positioned ^ ^ ^$(d) run summon minecraft:marker ~ {CY} ~ '
                   + '{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xnt","$(t)"]}'])
    hf, tl_ = H.clear_points()
    for name, r in (('lump', H.LUMP['field'][0]), ('met', M['small_field'][0])):
        d = r + A.CLEAR_PAD
        g.xw(f'u/clear_{name}', [
            f'# @s = a target marker of a pattern field r {n(r)}: pushed radially to >= {n(d)} b from the head-front point and',
            '# the tail-lane point (plan 4.7 clear melee points), then pulled inside the walk disc.',
            'tag @s add rlk_mb_az_xcp',
            f'execute at {BODY} rotated as {BODY} rotated ~ 0 positioned ^{n(hf[0])} ^ ^{n(hf[1])} run {F(f"xl/u/cp_{name}")}',
            f'execute at {BODY} rotated as {BODY} rotated ~ 0 positioned ^{n(tl_[0])} ^ ^{n(tl_[1])} run {F(f"xl/u/cp_{name}")}',
            'tag @s remove rlk_mb_az_xcp',
            g.clamp_walk()])
        g.xw(f'u/cp_{name}', [f'# At a clear point: the tagged target within {n(d)} b goes out to {n(d)} b on its bearing.',
                              f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcp,distance=..{n(d)},limit=1] facing entity @s feet '
                              f'rotated ~ 0 positioned ^ ^ ^{n(d)} run tp @s ~ ~ ~'])
    # Pyro lumps
    lr, lf = H.LUMP['r'], H.LUMP['field']
    g.xw('u/lump_dress', ['# @s = a lump prop (kit prop/lump), hidden (scale 0) until its launch.', K.prop('lump'),
                          'data merge entity @s {transformation:{scale:[0f,0f,0f]}}'])
    g.xw('u/lump_hz', [f'# Positioned at a lump target: disc r {n(lr)}, tell {H.LUMP["flight"]} (the flight), Pyro, the current volley group.']
         + g.hz_opts(el=1, grp=True) + [L.hz_disc(lr, H.LUMP['flight'], A.DMG['x_lump'])])
    half = H.LUMP['flight'] // 2
    g.xw('u/lump_fly', [f'# @s = a lump prop, at its target: glides there over {H.LUMP["flight"]} t (teleport_duration) on a',
                        f'# two-segment arc (translation up {n(H.LUMP["apex"])} b over {half} t, down at the apex call).',
                        f'data merge entity @s {{teleport_duration:{min(59, H.LUMP["flight"])},start_interpolation:0,'
                        f'interpolation_duration:{half},transformation:{{translation:[0f,{n(H.LUMP["apex"])}f,0f],scale:[1f,1f,1f]}}}}',
                        'tp @s ~ ~0.5 ~'])
    g.xw('u/lump_down', ['# @s = a lump prop past its apex.',
                         f'data merge entity @s {{start_interpolation:0,interpolation_duration:{H.LUMP["flight"] - half},'
                         'transformation:{translation:[0f,0f,0f]}}'])
    g.xw('u/lump_land', ['# Positioned at a lump target on landing: the fireball and its fire field (plan 4.6).',
                         K.fxe('impact', 1), g.sound('entity.generic.explode', 0.5, 1.3), g.sound('block.lava.pop', 1.0, 0.8),
                         g.field('fire', lf[0], lf[1], A.DMG['fire'], el=1), F('p/firefield/amb_on')])
    # Hydro blades
    b = H.BLADE
    g.xw('u/blade', ['# Positioned / rotated at a blade launch point: one water blade prop, flown by pj/launch.',
                     f'summon minecraft:item_display ~ ~ ~ {{Tags:{tags("rlk_mb_az_x", "rlk_mb_az_xlb", "rlk_mb_az_xnb")},'
                     'billboard:"fixed",teleport_duration:1}',
                     f'execute as {mk("rlk_mb_az_xnb", "item_display")} run {F("xl/u/blade_go")}'])
    g.xw('u/blade_go', ['# @s = a new blade prop (positioned / rotated = its flight): look, then pj/launch',
                        f'# ({n(b["spd"])} b/t, life {b["life"]} t, hit radius {n(b["hr"])}, Hydro, the host strike group #axlBG).',
                        'tag @s remove rlk_mb_az_xnb', 'tp @s ~ ~ ~ ~ 0', K.look('blade', 0x4FB8FF),
                        'data merge entity @s {view_range:2f,shadow_radius:0f,transformation:{translation:[0f,0f,0f],'
                        'left_rotation:[0f,0f,0f,1f],scale:[3.2f,1.6f,1f],right_rotation:[0f,0f,0f,1f]}}']
         + g.pj_opts(el=2) + ['scoreboard players operation #pjGrp mb = #axlBG mb',
                              L.pj_launch(b['spd'], b['life'], A.DMG['x_blade'], b['hr'])])


# =============================================================================================== addon bodies
def geyser(g):
    """chin/impact Hydro: the geyser disc r 3.0 on a random side 5-7 b off the impact, perpendicular to the crack line;
    *keep* decal (the water swirl, tele/disc rim) and hazard from the call (E - 12), hit E + 10 (tell 22)."""
    gy = H.GEYSER
    lines = ['# chin/impact Hydro (plan 4.6; Change note 1: keep, the swirl from the call). As the body at the impact point,',
             '# rotated = the crack line: a random side and distance 5-7 b (local x = perpendicular).',
             'kill @e[type=minecraft:marker,tag=rlk_mb_az_xlg]',
             'execute store result score #axlR mb run random value 0..9']
    for j in range(10):
        side = 1 if j < 5 else -1
        d = gy['side'][0] + (gy['side'][1] - gy['side'][0]) * (j % 5) / 4
        lines.append(f'execute if score #axlR mb matches {j} positioned ^{n(side * d)} ^ ^ run summon minecraft:marker ~ {CY} ~ '
                     f'{{Tags:{tags("rlk_mb_az_x", "rlk_mb_az_xlg")}}}')
    lines += [f'execute as {mk("rlk_mb_az_xlg")} run {g.clamp_walk()}',
              f'execute at {mk("rlk_mb_az_xlg")} run {F("xl/chin_impact/hydro_at")}',
              'kill @e[type=minecraft:marker,tag=rlk_mb_az_xlg]']
    g.xw('chin_impact/hydro', lines)
    g.xw('chin_impact/hydro_at', ['# At the geyser spot: own volley group, Hydro, the swirl decal = the hazard (r, tell).',
                                  g.GRP_NEW] + g.hz_opts(el=2, grp=True) + [
        L.hz_disc(gy['r'], gy['tell'], A.DMG['x_geyser']),
        K.tele_disc(gy['r'], gy['tell'], el=2, nd=0, hold=3),
        g.sound('block.bubble_column.whirlpool_inside', 0.9, 1.1)] + g.after(gy['tell'], 'xl/chin_impact/hydro_hit'))
    g.xw('chin_impact/hydro_hit', ['# The geyser erupts (the hit tick): column, stream ring, sounds.',
                                   K.fx('geyser'), K.fxe('dust_ring', 2, r=gy['r']),
                                   g.sound('entity.player.splash.high_speed', 1.0, 0.8),
                                   g.sound('block.bubble_column.upwards_inside', 1.0, 1.0)])


def lumps(g, point):
    """Pyro lumps (chin/impact, jump/wave2, stomp/w3, stomp3/s3): 3 lumps, one volley group, x_lump; targets 1 x lockv
    (lead 8) + 2 random 7-14 b from the context point, moved out of the clear melee points; launch / land per h_pl;
    each leaves a fire field r 4.0 / 160 t. No ground decal (Change note 1): the props in flight are the tell."""
    pk = A.ADDON_POINTS[point]['key']
    c = H.POINT_CODE[point]
    call, launch, land = H.lump_ticks(point)
    pre = f'rlk_mb_az_xl{c}'
    g.xw(f'{pk}/pyro', [f'# {point} Pyro (plan 4.6; call t{call}, launch t{launch}, land t{land} on the host clock). As the body at',
                        '# the context point: three hidden lump props wait here; the launch runs as an after() timer.',
                        f'kill @e[tag={pre}]']
         + [f'summon minecraft:item_display ~ ~1 ~ {{Tags:{tags("rlk_mb_az_x", pre, pre + "p", f"{pre}p{i}")},teleport_duration:0}}'
            for i in range(3)]
         + [f'execute as {mks(pre + "p", "item_display")} run {F("xl/u/lump_dress")}']
         + g.after(launch - call, f'xl/{pk}/pyro_go'))
    go = [f'# Launch (t{launch}): one new volley group; target 0 = lockv (lead {H.LUMP["lead"]}), 1 / 2 = random {H.LUMP["rnd"][0]}-'
          f'{H.LUMP["rnd"][1]} b from here;',
          '# every target out of the clear melee points; the hazards (tell = the flight); the props fly.',
          g.GRP_NEW,
          L.lockv(H.LUMP['lead'])]
    go += [f'tag @e[type=minecraft:marker,tag=rlk_mb_lock] add {t}' for t in ('rlk_mb_az_pat', 'rlk_mb_az_x', pre, pre + 't', pre + 't0')]
    go += ['tag @e[type=minecraft:marker,tag=rlk_mb_lock] remove rlk_mb_lock']
    for i in (1, 2):
        go += ['execute store result storage rlk:mboss az.xl.r.a int 1 run random value 0..359',
               f'execute store result storage rlk:mboss az.xl.r.d int 1 run random value {H.LUMP["rnd"][0]}..{H.LUMP["rnd"][1]}',
               f'data modify storage rlk:mboss az.xl.r.t set value "{pre}t{i}"',
               f'function {NS}xl/u/rnd with storage rlk:mboss az.xl.r',
               f'tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add {pre}',
               f'tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add {pre}t',
               'tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] remove rlk_mb_az_xnt']
    go += [f'execute as {mks(pre + "t")} run {F("xl/u/clear_lump")}',
           f'execute as {mks(pre + "t")} at @s run {F("xl/u/lump_hz")}']
    go += [f'execute as {mk(f"{pre}p{i}", "item_display")} at {mk(f"{pre}t{i}")} run {F("xl/u/lump_fly")}' for i in range(3)]
    go += [g.sound('item.firecharge.use', 1.0, 0.7), g.sound('entity.blaze.shoot', 0.7, 0.6)]
    go += g.after(H.LUMP['flight'] // 2, f'xl/{pk}/pyro_apex') + g.after(H.LUMP['flight'], f'xl/{pk}/pyro_land')
    g.xw(f'{pk}/pyro_go', go)
    g.xw(f'{pk}/pyro_apex', ['# The lumps pass their apex.', f'execute as {mks(pre + "p", "item_display")} run {F("xl/u/lump_down")}'])
    g.xw(f'{pk}/pyro_land', [f'# Landing (t{land}): fireball + fire field at every target, then the props and targets go.',
                             f'execute as {mks(pre + "t")} at @s run {F("xl/u/lump_land")}', f'kill @e[tag={pre}]'])


def blades(g, point):
    """Hydro blades (jump/land, stomp/w1, stomp3/s1): 8 water blades from r 2 at 2.0 b/t, launched E + 4, life 6 t,
    hit radius 1.6, 0.9 b up, in the host's strike group (#azCtxGrp saved at the call), x_blade. No ground decal."""
    pk = A.ADDON_POINTS[point]['key']
    call, launch, end = H.blade_ticks(point)
    b = H.BLADE
    g.xw(f'{pk}/hydro', [f'# {point} Hydro (plan 4.6; call t{call}, launch t{launch}, in flight to t{end}). As the body at the context',
                         '# point rotated to the player: the host group is kept for the launch (the next addon call may move it).',
                         'scoreboard players operation #axlBG mb = #azCtxGrp mb'] + g.after(launch - call, f'xl/{pk}/hydro_go'))
    go = [f'# Launch: {b["n"]} blades radially (blade 0 toward the player) from r {n(b["r0"])}, {n(b["up"])} b up.']
    for k in range(b['n']):
        go.append(f'execute rotated ~{n(360.0 * k / b["n"])} 0 positioned ^ ^{n(b["up"])} ^{n(b["r0"])} run {F("xl/u/blade")}')
    go += [K.fxe('dust_ring', 2, r=b['r0'] + 1.0), g.sound('entity.player.splash.high_speed', 0.9, 1.2),
           g.sound('item.trident.riptide_1', 0.6, 1.5)]
    g.xw(f'{pk}/hydro_go', go)


# =============================================================================================== 31 격류 범람
def orbs(g):
    key = 'orbs'
    tag_o, tag_d, tag_y = 'rlk_mb_az_p31o', 'rlk_mb_az_p31d', 'rlk_mb_az_p31y'
    rings = O['rings']
    spawn_rel = f'p/{key}/spawn'
    # one orb: ring (k even inner, k odd outer), angle #aq31A + 90 k + omega x #aq31C (the reload's elapsed steps)
    for k in range(4):
        ring = 1 if k % 2 == 0 else 2
        r, w = rings[ring]
        sp = g.orbit_spawn(f'{tag_o}{k}', ring, k, r, w, O['a0'], O['hr'], O['band'], A.DMG['o31'], grp=True)
        g.pw(key, f'mk{k}', [f'# Orb {k}: ring {ring} (r {n(r)}, {n(w)} deg/t), angle = base + {90 * k} + omega x #aq31C; Hydro hz r {n(O["hr"])}',
                             '# (N5 orb/spawn: band, #hzRearm 10, the current volley group); its prop; ring and pattern tags.',
                             f'scoreboard players set #aq31O mb {int(round(w * 100))}',
                             'scoreboard players operation #aq31Q mb = #aq31C mb',
                             'scoreboard players operation #aq31Q mb *= #aq31O mb',
                             'scoreboard players operation #aq31Q mb += #aq31A mb',
                             f'scoreboard players add #aq31Q mb {9000 * k}']
             + g.hz_opts(el=2) + [sp[0], 'execute store result storage rlk:mboss az.orb.a int 1 run scoreboard players get #aq31Q mb', sp[1],
                                  f'tag @e[type=minecraft:marker,tag={tag_o}{k}] add {tag_o}',
                                  f'tag @e[type=minecraft:marker,tag={tag_o}{k}] add rlk_mb_az_p31r{ring}',
                                  f'execute at {mk(f"{tag_o}{k}")} run summon minecraft:item_display ~ ~ ~ '
                                  f'{{Tags:{tags("rlk_mb_az_p31", tag_d, f"{tag_d}{k}")},teleport_duration:1}}',
                                  f'execute as {mk(f"{tag_d}{k}", "item_display")} run {F(f"p/{key}/dress")}'])
    g.pw(key, 'dress', ['# @s = an orb prop: the kit orb, small (it grows), its centre 1.1 b up (normal band).', K.prop('orb'),
                        f'data merge entity @s {{transformation:{{translation:[0f,{n(O["y_lo"])}f,0f],scale:[0.4f,0.4f,0.4f]}}}}',
                        'scoreboard players set @s azS 0'])
    g.pw(key, 'spawn', ['# The orbs appear (cast clock = roar_rear drop - 2): base angle = the facing + 45 (two orbs per side),',
                        '# one volley group for all four, the yaw scratch marker, the cue.',
                        F(f'p/{key}/kill'),
                        f'scoreboard players set #aq31E mb {O["life"]}', 'scoreboard players set #aq31K mb 36000',
                        'scoreboard players set #aq31W mb 0', 'scoreboard players set #aq31C mb 0',
                        'execute store result score #aq31A mb run data get entity @s Rotation[0] 100',
                        f'scoreboard players add #aq31A mb {int(round(O["a0"] * 100))}',
                        g.GRP_NEW] + [F(f'p/{key}/mk{k}') for k in range(4)] + [
                        f'summon minecraft:marker ~ ~ ~ {{Tags:{tags("rlk_mb_az_p31", tag_y)}}}',
                        K.snd('orb_spawn'), K.fx('splash')])
    g.pw(key, 'kill', ['# Every orb now (selectors only): the hazards, the markers (and the orbit centre), the props.',
                       f'execute as {mks("rlk_mb_az_orbhz")} at @s run function rlk:mboss/hz/expire']
         + g.orbit_end(tag_o) + ['kill @e[tag=rlk_mb_az_p31]'])
    # cast slot (#azCT = the roar_rear tick)
    g.pw(key, 'cast', ['# 31 cast (s2.md 6): roar_rear t0 (the host plays it). The orbs spawn at drop - 2 in ctick.'])
    g.pw(key, 'ctick', [f'# Cast clock #azCT: t{O["spawn"]} the orbs spawn, then bg slot L takes them and the cast slot ends.',
                        f'execute if score #azCT mb matches {O["spawn"]} run {F(spawn_rel)}',
                        f'execute if score #azCT mb matches {O["spawn"]} run {g.bg_start("L")}',
                        f'execute if score #azCT mb matches {O["spawn"]}.. run {g.cast_end()}'])
    g.pw(key, 'cancel', ['# The cast was cut before the hand-over: nothing of it may stay (orbs in bg slot L live on).',
                         f'execute unless score #azBgL mb matches 31 run {F(f"p/{key}/kill")}'])
    # bg slot L (#azBgLT 0 = the spawn tick)
    grow = ['# Growing out from the sides (bg clock 0..9): the orbit radius ramps to its ring (azT = r x 1000).']
    for c in range(O['grow']):
        f = 0.35 + 0.65 * (c + 1) / O['grow']
        for ring, (r, _) in rings.items():
            grow.append(f'execute if score #azBgLT mb matches {c} run scoreboard players set @e[type=minecraft:marker,'
                        f'tag=rlk_mb_az_p31r{ring}] azT {int(round(r * f * 1000))}')
    g.pw(key, 'grow', grow)
    bt = [f'# bg slot L clock #azBgLT: grow 0-{O["grow"] - 1} (harmless), orbit until #aq31E ({O["life"]}; refresh moves it), fade '
          f'{O["fade"]} t, end.',
          'scoreboard players set #aq31K mb 36000',
          f'execute if score #azBgLT mb matches ..{O["grow"] - 1} run {F(f"p/{key}/grow")}',
          f'execute if score #azBgLT mb matches 1 as {mks(tag_d, "item_display")} run data merge entity @s '
          f'{{start_interpolation:0,interpolation_duration:{O["grow"] - 1},transformation:{{scale:[2.6f,2.6f,2.6f]}}}}',
          g.orbit_tick(tag_o),
          'execute store result score #aq31Y mb run data get entity @s Rotation[0] 100']
    for k in range(4):
        bt.append(f'execute as {mk(f"{tag_o}{k}")} at @s run {F(f"p/{key}/band")}')
        bt.append(f'execute as {mk(f"{tag_d}{k}", "item_display")} at {mk(f"{tag_o}{k}")} run {F(f"p/{key}/prop")}')
    bt += ['# the hit cue (the group was marked this tick)', 'scoreboard players set #aq31N mb 0',
           f'execute as {mks("rlk_mb_az_orbhz")} if score @s mbHzHit matches 1 run scoreboard players set #aq31N mb 1',
           f'execute if score #aq31N mb matches 1 unless score #aq31W mb matches 1 at {PLAYER} run {K.snd("orb_hit")}',
           'scoreboard players operation #aq31W mb = #aq31N mb']
    bt += [f'execute if score #azBgLT mb matches {O["grow"]}.. if score #azBgLT mb < #aq31E mb run {F(f"p/{key}/amb")}',
           f'execute if score #azBgLT mb = #aq31E mb run {F(f"p/{key}/fade")}',
           'scoreboard players operation #aq31X mb = #aq31E mb', f'scoreboard players add #aq31X mb {O["fade"]}',
           f'execute if score #azBgLT mb >= #aq31X mb run {F(f"p/{key}/end")}']
    g.pw(key, 'bgtick', bt)
    g.pw(key, 'amb', ['# Ribbons every 2 t at each orb, the loop at the orb nearest the player every 20 t.']
         + g.every(O['rib'], f'execute as {mks(tag_d, "item_display")} at @s run {F(f"p/{key}/rib")}', clock='#azBgLT')
         + g.every(O['loop'], f'execute at {PLAYER} at @e[type=minecraft:item_display,tag={tag_d},sort=nearest,limit=1] run {K.snd("orb_loop")}',
                   start=5, clock='#azBgLT'))
    g.pw(key, 'rib', ['# @s = an orb prop: the ribbon at its centre height.',
                      f'execute if score @s azS matches 1 positioned ~ ~{n(O["y_hi"])} ~ run {K.fx("orb_ribbon")}',
                      f'execute unless score @s azS matches 1 positioned ~ ~{n(O["y_lo"])} ~ run {K.fx("orb_ribbon")}'])
    g.pw(key, 'band', [
        '# @s = an orb marker, at it: #aq31H 0 normal band, 1 rides high (transitions / cine, the head-lane eye: front +-30 deg',
        f'# about the facing and < {n(O["eye_r"])} b from the anchor, over a 42 safe circle), 2 harmless (growing / fading).',
        'scoreboard players set #aq31H mb 0',
        'execute if score #azOrbHigh mb matches 1 run scoreboard players set #aq31H mb 1',
        f'execute if score #aq31H mb matches 0 if entity {body_near(O["eye_r"])} run {F(f"p/{key}/eye")}',
        f'execute if score #aq31H mb matches 0 if entity @e[type=minecraft:marker,tag=rlk_mb_hzsafe,distance=..{n(O["safe_pad"])}] '
        'run scoreboard players set #aq31H mb 1',
        f'execute unless score #azBgLT mb matches {O["grow"]}.. run scoreboard players set #aq31H mb 2',
        'execute if score #azBgLT mb >= #aq31E mb run scoreboard players set #aq31H mb 2',
        'scoreboard players operation #aq31X mb = @s azF',
        f'execute as {mks("rlk_mb_az_orbhz")} if score @s mbHzI = #aq31X mb run {F(f"p/{key}/hzb")}'])
    half = int(round(O['eye_half'] * 100))
    g.pw(key, 'eye', ['# @s = an orb marker near the anchor: the yaw anchor -> orb against the facing (#aq31Y), x 100, mod 360.',
                      f'execute at {BODY} facing entity @s feet as {mk(tag_y)} run tp @s ~ ~ ~ ~ 0',
                      f'execute store result score #aq31Q mb run data get entity {mk(tag_y)} Rotation[0] 100',
                      'scoreboard players operation #aq31Q mb -= #aq31Y mb',
                      'scoreboard players operation #aq31Q mb %= #aq31K mb',
                      f'execute if score #aq31Q mb matches ..{half} run scoreboard players set #aq31H mb 1',
                      f'execute if score #aq31Q mb matches {36000 - half}.. run scoreboard players set #aq31H mb 1'])
    lo, hi = O['band'], O['high']
    g.pw(key, 'hzb', ['# @s = the orb\'s hazard: its height band (milliblocks) by #aq31H.']
         + [f'execute if score #aq31H mb matches {s} run scoreboard players set @s mbHzY{j} {v}'
            for s, (y0, y1) in ((0, lo), (1, hi), (2, (99, 99))) for j, v in ((0, int(round(y0 * 1000))), (1, int(round(y1 * 1000))))])
    g.pw(key, 'prop', ['# @s = an orb prop, at its marker: follow it; rise / sink over 6 t when the band changes.', 'tp @s ~ ~ ~',
                       f'execute if score #aq31H mb matches 1 unless score @s azS matches 1 run {F(f"p/{key}/up")}',
                       f'execute unless score #aq31H mb matches 1 if score @s azS matches 1 run {F(f"p/{key}/down")}'])
    for nm, y, st in (('up', O['y_hi'], 1), ('down', O['y_lo'], 0)):
        g.pw(key, nm, [f'scoreboard players set @s azS {st}',
                       f'data merge entity @s {{start_interpolation:0,interpolation_duration:6,transformation:{{translation:[0f,{n(y)}f,0f]}}}}'])
    g.pw(key, 'fade', ['# The orbit is over: the props shrink away (harmless from now).',
                       f'execute as {mks(tag_d, "item_display")} run data merge entity @s {{start_interpolation:0,'
                       f'interpolation_duration:{O["fade"]},transformation:{{scale:[0f,0f,0f]}}}}',
                       f'execute at {mk(tag_d, "item_display")} run {K.fx("splash")}'])
    g.pw(key, 'end', ['# The orbs are gone: bg slot L frees (the 600-t cooldown starts there).', F(f'p/{key}/kill'), g.bg_end('L')])
    g.pw(key, 'cancel_bg', ['# Death, cleanup, test stop: the orbs go at once (selectors only).', F(f'p/{key}/kill')])
    g.pw(key, 'refresh', [
        '# Transition 2 with live orbs (core cast host, roar_low): full life again, no new orbs; a fading orb grows back.',
        'scoreboard players operation #aq31E mb = #azBgLT mb', f'scoreboard players add #aq31E mb {O["refresh"]}',
        f'execute as {mks(tag_d, "item_display")} run data merge entity @s {{start_interpolation:0,interpolation_duration:6,'
        'transformation:{scale:[2.6f,2.6f,2.6f]}}',
        K.snd('orb_spawn'), f'execute as {mks(tag_d, "item_display")} at @s run {K.fx("splash")}'])
    g.pw(key, 'reload', ['# /reload with the orbs in bg slot L: every aux entity is gone; re-make them at their angles (elapsed',
                         '# steps = the bg clock + 1) in a new volley group; a fading orbit just ends.',
                         f'execute if score #azBgLT mb >= #aq31E mb run return run {F(f"p/{key}/end")}',
                         f'execute at @s run {F(f"p/{key}/remake")}'])
    g.pw(key, 'remake', ['scoreboard players set #aq31K mb 36000', 'scoreboard players set #aq31W mb 0',
                         'scoreboard players operation #aq31C mb = #azBgLT mb', 'scoreboard players add #aq31C mb 1',
                         g.GRP_NEW] + [F(f'p/{key}/mk{k}') for k in range(4)] + [
                         f'summon minecraft:marker ~ ~ ~ {{Tags:{tags("rlk_mb_az_p31", tag_y)}}}',
                         f'execute if score #azBgLT mb matches {O["grow"]}.. as {mks(tag_d, "item_display")} run data merge entity @s '
                         '{transformation:{scale:[2.6f,2.6f,2.6f]}}'])


# =============================================================================================== 32 운석 낙하
def meteor(g):
    key = 'meteor'
    tl = A.TL(g, key, clock='#azCT', sub='ck')
    big = 'rlk_mb_az_p32b'
    tl.at(0, 'kill @e[tag=rlk_mb_az_p32]', 'scoreboard players set #aq32G mb 0')
    # the big meteor: seal + hazard under the player (locked) at R + 7, impact R + 35
    tl.at(M['seal'], f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:{tags("rlk_mb_az_p32", big)}}}',
          f'execute as {mk(big)} run {g.clamp_walk()}', f'execute at {mk(big)} run {F(f"p/{key}/big_hz")}')
    g.pw(key, 'big_hz', [f'# At the lock: own group, Pyro, KB {A.KB["o32_big"]}; the seal8 decal = the hazard (keep, r {n(M["big_r"])}, '
                         f'tell {M["big"] - M["seal"]}).', g.GRP_NEW]
         + g.hz_opts(el=1, kb=A.KB['o32_big'], grp=True)
         + [L.hz_disc(M['big_r'], M['big'] - M['seal'], A.DMG['o32_big']), g.tag_last_hz('rlk_mb_az_p32h'),
            K.tele_seal8(M['big_r'], M['big'] - M['seal'], el=1, hold=3), K.snd('meteor_glyph')])
    tl.at(M['big'] - M['big_fall'], f'execute at {mk(big)} run {K.fx("meteor_big", h=M["big_h"])}',
          f'execute at {mk(big)} run {K.snd("meteor_fall")}')
    tl.at(M['big'], f'execute at {mk(big)} run {F(f"p/{key}/big_hit")}', f'kill {mk(big)}')
    bf = M['big_field']
    g.pw(key, 'big_hit', ['# The big impact: the dome, the boom, a fire field r 4.5 / 200 t.', K.fx('fire_dome', r=M['big_r']),
                          K.snd('meteor_impact')]
         + g.field('fire', bf[0], bf[1], A.DMG['fire'], el=1) + [F('p/firefield/amb_on')])
    # the six small meteors: halo 12 t before each hit; even k = lockv (lead 10), odd k = random 6-14 b from the anchor
    sf = M['small_field']
    for k, t in enumerate(M['small']):
        mt, pt = f'rlk_mb_az_p32m{k}', f'rlk_mb_az_p32p{k}'
        made = t - M['small_tell']
        if k % 2 == 0:
            tgt = [L.lockv(M['small_lead'])] + [f'tag @e[type=minecraft:marker,tag=rlk_mb_lock] add {x}'
                                                  for x in ('rlk_mb_az_pat', 'rlk_mb_az_p32', mt)] + [
                'tag @e[type=minecraft:marker,tag=rlk_mb_lock] remove rlk_mb_lock']
        else:
            tgt = ['execute store result storage rlk:mboss az.p32.r.a int 1 run random value 0..359',
                   f'execute store result storage rlk:mboss az.p32.r.d int 1 run random value {M["small_rnd"][0]}..{M["small_rnd"][1]}',
                   f'data modify storage rlk:mboss az.p32.r.t set value "{mt}"',
                   f'function {NS}xl/u/rnd with storage rlk:mboss az.p32.r',
                   'tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_p32',
                   'tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] remove rlk_mb_az_xnt',
                   f'execute as {mk(mt)} run {F("xl/u/clear_met")}']
        g.pw(key, f's{k}', [f'# Small meteor {k} (hit t{t}): its target, then the hazard + the air halo + the prop high above it.']
             + tgt + [f'execute at {mk(mt)} run {F(f"p/{key}/s{k}_hz")}'])
        grp = ([g.GRP_NEW, 'scoreboard players operation #aq32G mb = #mbGrp mb'] if k == 0 else [])
        g.pw(key, f's{k}_hz', [f'# At target {k}: disc r {n(M["small_r"])}, tell {M["small_tell"]}, Pyro, the group of the six; no ground decal',
                               '# (Change note 1): the halo in the air and the falling meteor are the tell.'] + grp
             + g.hz_opts(el=1) + ['scoreboard players operation #hzGrp mb = #aq32G mb',
                                  L.hz_disc(M['small_r'], M['small_tell'], A.DMG['o32_small']), g.tag_last_hz('rlk_mb_az_p32h'),
                                  K.tele_halo(M['small_r'], M['halo_h'], M['small_tell'], el=1, hold=2),
                                  f'summon minecraft:item_display ~ ~{n(M["prop_h"])} ~ {{Tags:{tags("rlk_mb_az_p32", pt)},teleport_duration:0}}',
                                  f'execute as {mk(pt, "item_display")} run {K.prop("meteor_small")}'])
        tl.at(made, F(f'p/{key}/s{k}'))
        drop = M['prop_h'] - M['prop_mid']
        steps = M['small_tell'] - M['prop_fall'] - 1
        tl.at(made + 1, f'execute as {mk(pt, "item_display")} at @s run {F(f"p/{key}/fall")}')
        tl.at(t - M['prop_fall'], f'kill {mk(pt, "item_display")}',
              f'execute at {mk(mt)} run {K.fx("meteor_small", h=M["prop_mid"])}', f'execute at {mk(mt)} run {K.snd("meteor_fall")}')
        tl.at(t, f'execute at {mk(mt)} run {F(f"p/{key}/small_hit")}', f'kill {mk(mt)}')
    g.pw(key, 'fall', [f'# @s = a small meteor prop: glides {n(drop)} b down over {steps} t (to the preset fall).',
                       f'data merge entity @s {{teleport_duration:{steps}}}', f'tp @s ~ ~-{n(drop)} ~'])
    g.pw(key, 'small_hit', ['# A small meteor lands: the blast and a fire field r 2.8 / 160 t.', K.fxe('impact', 1), K.snd('meteor_small')]
         + g.field('fire', sf[0], sf[1], A.DMG['fire'], el=1) + [F('p/firefield/amb_on')])
    tl.at(M['end'], g.cast_end())
    tl.write(['# 32 cast (s2.md 6): the cast clock #azCT = the roar_rear tick; R = roar (t20). Seal t27, big t55, small t64-94.'],
             [f'# 32 ctick (#azCT): the timeline; the cast slot ends after the last small meteor (t{M["end"]}).'],
             t0=0, start='cast', tick='ctick')
    # resume (s2.md 12): the kit dropped every attack telegraph at the pause; the keep seal and the air halos come back
    # with their remaining tell (the hazards were frozen with the clocks)
    res = ['# Resume: the seal8 (keep) and the live small-meteor halos again, each with its remaining tell (cast clock).',
           f'execute if score #azCT mb matches {M["seal"]}..{M["big"] - 1} at {mk(big)} run {F(f"p/{key}/re_seal")}']
    for k, t in enumerate(M['small']):
        res.append(f'execute if score #azCT mb matches {t - M["small_tell"]}..{t - 1} at {mk(f"rlk_mb_az_p32m{k}")} run '
                   f'{F(f"p/{key}/re_halo{k}")}')
        g.pw(key, f're_halo{k}', [f'scoreboard players set #aq32X mb {t}', 'scoreboard players operation #aq32X mb -= #azCT mb',
                                  f'data modify storage rlk:mboss az.tl set value {{r:{int(round(M["small_r"] * 10))},'
                                  f'h:{int(round(M["halo_h"] * 10))},tell:1,el:1,hold:2}}',
                                  'execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq32X mb',
                                  f'function {K.FN}tele/halo with storage rlk:mboss az.tl'])
    g.pw(key, 'resume', res)
    g.pw(key, 're_seal', [f'scoreboard players set #aq32X mb {M["big"]}', 'scoreboard players operation #aq32X mb -= #azCT mb',
                          f'data modify storage rlk:mboss az.tl set value {{r:{int(round(M["big_r"] * 10))},tell:1,el:1,hold:3}}',
                          'execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq32X mb',
                          f'function {K.FN}tele/seal8 with storage rlk:mboss az.tl'])
    g.pw(key, 'cancel', ['# The cast was cut (test, reload, a new cast): its markers, props and live hazards go (selectors only).',
                         'kill @e[tag=rlk_mb_az_p32]',
                         f'execute as {mks("rlk_mb_az_p32h")} at @s run function rlk:mboss/hz/expire'])


# =============================================================================================== 33 화염 잠식
def firefield(g):
    key = 'firefield'
    fr = H.FIRE
    on = ['# Rule 33 (plan 4.7; s2.md 9): a Pyro brand by a strike hit, as the body at the player\'s floor point (#azBrNew 1 new /',
          f'# 0 refresh): a fire field r {n(fr["rule_r"])} / {fr["rule_life"]} t here, or the first fire field within {n(fr["extend_r"])} b',
          '# is extended instead (fld/refresh: at most 2x its base life). Fire-rule fields ignore the clear melee points.',
          'scoreboard players set #aq33X mb 0']
    for i in range(A.FIELD_SLOTS):
        on.append(f'execute if score #aq33X mb matches 0 if score #azF{i} mb matches {A.FIELD_FAM["fire"]} as '
                  f'@e[type=minecraft:marker,tag=rlk_mb_az_fld{i},distance=..{n(fr["extend_r"])},limit=1] run {F(f"p/{key}/ext")}')
    on += [f'execute if score #aq33X mb matches 0 run {F(f"p/{key}/new")}', F(f'p/{key}/amb_on')]
    g.pw(key, 'on_brand', on)
    g.pw(key, 'ext', ['# @s = a fire field hazard near the branded player: extended by its base life.',
                      g.field_refresh('@s', fr['rule_life']), 'scoreboard players set #aq33X mb 1',
                      f'execute at @s run {K.fx("fire_field", r=fr["rule_r"])}'])
    g.pw(key, 'new', ['# A new fire-rule field under the player.']
         + g.field('fire', fr['rule_r'], fr['rule_life'], A.DMG['fire'], el=1, rule=True)
         + [K.fx('fire_field', r=fr['rule_r']), g.sound('item.firecharge.use', 0.8, 0.9)])
    # the fire-field ambience (every live fire field, ours or not): an after() chain while any fire field lives
    g.pw(key, 'amb_on', ['# Start the fire-field ambience chain unless it runs (#aq33A = the tick of its next step).',
                         f'execute unless score #aq33A mb >= #azClk mb run {F(f"p/{key}/amb_arm")}'])
    g.pw(key, 'amb_arm', ['scoreboard players operation #aq33A mb = #azClk mb', f'scoreboard players add #aq33A mb {fr["amb"]}']
         + g.after(fr['amb'], f'p/{key}/amb'))
    amb = [f'# Every {fr["amb"]} t: flames over each live fire field (kit p/fire_field, its radius), the loop sound every {fr["snd"]} t;',
           '# re-armed while any fire field lives.', 'scoreboard players set #aq33N mb 0']
    for i in range(A.FIELD_SLOTS):
        amb.append(f'execute if score #azF{i} mb matches {A.FIELD_FAM["fire"]} run scoreboard players add #aq33N mb 1')
        amb.append(f'execute if score #azF{i} mb matches {A.FIELD_FAM["fire"]} at {mk(f"rlk_mb_az_fld{i}")} run '
                   f'function {K.FN}p/fire_field with storage rlk:mboss az.f{i}')
    amb += ['scoreboard players add #aq33S mb 1',
            f'execute if score #aq33S mb matches 2.. at {PLAYER} at @e[type=minecraft:marker,tag=rlk_mb_az_fld,sort=nearest,limit=1] run '
            f'{K.snd("fire_loop")}',
            'execute if score #aq33S mb matches 2.. run scoreboard players set #aq33S mb 0',
            'scoreboard players set #aq33A mb 0',
            f'execute if score #aq33N mb matches 1.. run {F(f"p/{key}/amb_arm")}']
    g.pw(key, 'amb', amb)


# =============================================================================================== emit
def emit(g):
    utils(g)
    geyser(g)
    for point in H.LUMP['launch']:
        lumps(g, point)
    for point in H.BLADE['points']:
        blades(g, point)
    orbs(g)
    meteor(g)
    firefield(g)
    # every leg body of ADDON_POINTS is written (the dispatchers get a line for each)
    for point, d in A.ADDON_POINTS.items():
        for el in d['bodies']:
            if el in ('hydro', 'pyro'):
                assert g.has(f'xl/{d["key"]}/{el}'), (point, el)
    assert math.isclose(H.GEYSER['tell'], A.ADDON_POINTS['chin/impact']['E'] + H.GEYSER['hit'] - A.ADDON_POINTS['chin/impact']['call'])
