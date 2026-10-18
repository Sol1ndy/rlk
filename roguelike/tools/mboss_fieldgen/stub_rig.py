"""STUB rig for the field generator module (removable; used only while api.STUB, i.e. the real rig manifest
tools/mboss_fieldgen_rig_manifest.json does not exist yet).

It writes F:mboss/fieldgen/rig_stub/** with the same API as the real rig (rlk:mboss/fieldgen/rig/...): init, spawn,
tick, kill, uninstall, play/<clip>, form/<dormant|cruise|field|coreup|tower|laser|deployed>,
look/<idle|charge|field|groggy|off>, crack/<0..4>, face/player, face/track, flash, prop/clear. Clips only keep time
(id, tick, loop / next, the form switches and the warp's hidden span of stub_rig_manifest.json); the figure is a crude
vanilla stand-in: a clock face lying flat as the 7 b ring, a gold block as the core, a glass pane halo and a lightning
rod pendulum, posed per form at the plan's hover heights (ring centre 2.15 dormant, 4.5 cruise, 5.8 field ...), so a
test fight in game is readable. Named parts (rlk_mb_fg_<name>) follow the anchor, so fx anchors resolve.

Delete this file and stub_rig_manifest.json once the real rig is merged: with the real manifest present the module
build never imports it and removes F:mboss/fieldgen/rig_stub/.
"""
from . import api as A
from .api import L

DIR = 'rig_stub'
NSR = f'{A.NS}{DIR}/'
OBJ = {k: k for k in A.RIG_OBJECTIVES}
C, T, F, LK, K, Y, V = 'fgRigC', 'fgRigT', 'fgRigF', 'fgRigL', 'fgRigK', 'fgRigY', 'fgRigV'
assert all(o in A.RIG_OBJECTIVES for o in (C, T, F, LK, K, Y, V)), A.RIG_OBJECTIVES
TAG = 'rlk_mb_fgs'                         # every stub part
FORM_ID = {f: i for i, f in enumerate(A.RIG_FORMS)}
LOOK_ID = {lk: i for i, lk in enumerate(A.LOOKS)}
# ring-centre height per form (model.md §8) and the part offsets (y from the ring centre)
H = {'dormant': 2.15, 'cruise': 4.5, 'field': 5.8, 'coreup': 5.0, 'tower': 4.5, 'laser': 4.5, 'deployed': 5.6}
CORE_Y = {'dormant': 0.0, 'cruise': 0.1, 'field': -1.96, 'coreup': 2.8, 'tower': -0.4, 'laser': 0.1, 'deployed': -1.96}
HALO_Y = {'dormant': 0.0, 'cruise': 1.6, 'field': 1.55, 'coreup': 1.6, 'tower': 3.2, 'laser': 1.6, 'deployed': 1.55}
PEND_Y = {'dormant': 0.12, 'cruise': -1.85, 'field': -3.4, 'coreup': -2.6, 'tower': -2.2, 'laser': -1.85, 'deployed': -3.2}
MEDAL = {'dormant': (3.3, -0.35), 'cruise': (3.3, -0.35), 'field': (3.85, -1.96), 'coreup': (3.6, 0.3),
         'tower': (0.5, 3.6), 'laser': (2.8, -2.0), 'deployed': (5.6, -0.6)}
FLAT = '[0.7071f,0f,0f,0.7071f]'           # item model turned to lie flat (about x)
PARTS = {   # name -> (item or None, scale (x, y, z), left_rotation)
    'ring': ('minecraft:clock', (7.0, 7.0, 7.0), FLAT),
    'core': ('minecraft:gold_block', (1.6, 1.6, 1.6), '[0f,0f,0f,1f]'),
    'halo': ('minecraft:yellow_stained_glass_pane', (3.0, 3.0, 3.0), FLAT),
    'pend': ('minecraft:lightning_rod', (1.4, 2.2, 1.4), '[0f,0f,0f,1f]'),
    'medal_e': (None, None, None), 'medal_g': (None, None, None),
}
assert set(PARTS) == set(A.PARTS), (sorted(PARTS), A.PARTS)
LOOK_GLOW = {'idle': None, 'charge': 0xFADEA8, 'field': 0x9C86E8, 'groggy': None, 'off': None}


def offsets(form):
    h = H[form]
    mx, my = MEDAL[form]
    return {'ring': (0.0, h, 0.0), 'core': (0.0, h + CORE_Y[form], 0.0), 'halo': (0.0, h + HALO_Y[form], 0.0),
            'pend': (0.0, h + PEND_Y[form], 0.0), 'medal_e': (mx, h + my, 0.0), 'medal_g': (-mx, h + my, 0.0)}


def tf(scale, rot='[0f,0f,0f,1f]'):
    sx, sy, sz = scale
    return (f'{{translation:[0f,0f,0f],left_rotation:{rot},right_rotation:[0f,0f,0f,1f],'
            f'scale:[{L.num(sx)}f,{L.num(sy)}f,{L.num(sz)}f]}}')


def sel(name):
    return f'@e[type=minecraft:item_display,tag=rlk_mb_fg_{name},tag={TAG},limit=1]'


def emit(g):
    w = lambda rel, lines: g.w(f'{DIR}/{rel}', lines)
    head = '# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.'
    w('init', [head, '# Objectives; safe on every load.'] + [f'scoreboard objectives add {o} dummy' for o in A.RIG_OBJECTIVES])
    spawn = [head, '# @s = anchor (the body), at it, rotated as it: kills old parts, summons the stand-in in the cruise pose.',
             f'function {NSR}init', f'function {NSR}kill']
    for name, (item, sc, rot) in PARTS.items():
        tags = f'["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","{TAG}","rlk_mb_fg_{name}"]'
        it = f',item:{{id:"{item}",count:1}}' if item else ''
        x, y, z = offsets('cruise')[name]
        spawn.append(f'summon minecraft:item_display ^{L.num(x)} ^{L.num(y)} ^{L.num(z)} {{Tags:{tags},billboard:"fixed",'
                     f'item_display:"none",teleport_duration:1,interpolation_duration:3,brightness:{{block:14,sky:15}},'
                     f'transformation:{tf(sc or (0, 0, 0), rot or "[0f,0f,0f,1f]")}{it}}}')
    spawn += [f'scoreboard players set @s {C} {A.CLIPS["idle_cruise"]["id"]}', f'scoreboard players set @s {T} -1',
              f'scoreboard players set @s {F} {FORM_ID["cruise"]}', f'scoreboard players set @s {LK} 0',
              f'scoreboard players set @s {K} 0', f'scoreboard players set @s {Y} 0', f'scoreboard players set @s {V} 0']
    w('spawn', spawn)
    for form in A.RIG_FORMS:
        follow = [head, f'# @s = anchor, at it, rotated ~ 0 as it: every part to its {form} rest offset.']
        for name, (x, y, z) in offsets(form).items():
            follow.append(f'execute positioned ^{L.num(x)} ^{L.num(y)} ^{L.num(z)} run tp {sel(name)} ~ ~ ~ ~ 0')
        w(f'follow/{form}', follow)
    w('tick', [head, '# @s = anchor, at it; every game tick (after the AI). Missing parts respawn.',
               f'execute unless entity {sel("ring")} run function {NSR}spawn'] +
      [f'execute if score @s {F} matches {i} rotated as @s rotated ~ 0 run function {NSR}follow/{f}' for f, i in FORM_ID.items()] +
      [f'scoreboard players add @s {T} 1',
       f'function {NSR}run',
       f'execute if score @s {Y} matches 1.. run function {NSR}flash_tick'])
    run = [head, '# Clip end: loop, next clip or hold; the clips\' form switches and hidden spans (manifest "forms", "hidden").']
    for name, c in A.CLIPS.items():
        if c['loop']:
            run.append(f'execute if score @s {C} matches {c["id"]} if score @s {T} matches {c["len"]}.. run scoreboard players set @s {T} 0')
        elif c['next']:
            run.append(f'execute if score @s {C} matches {c["id"]} if score @s {T} matches {c["len"]}.. run return run function {NSR}play/{c["next"]}')
    for name, switches in A._MAN.get('forms', {}).items():
        if name in A.CLIPS:
            for tick, form in switches:
                run.append(f'execute if score @s {C} matches {A.CLIPS[name]["id"]} if score @s {T} matches {tick} run function {NSR}form/{form}')
    for name, (t_hide, t_show) in A._MAN.get('hidden', {}).items():
        if name in A.CLIPS:
            if t_hide >= 0:
                run.append(f'execute if score @s {C} matches {A.CLIPS[name]["id"]} if score @s {T} matches {t_hide} run function {NSR}hide')
            if t_show >= 0:
                run.append(f'execute if score @s {C} matches {A.CLIPS[name]["id"]} if score @s {T} matches {t_show} run function {NSR}show')
    w('run', run)
    hides = {n for n, (th, ts) in A._MAN.get('hidden', {}).items() if th >= 0}
    for name, c in A.CLIPS.items():
        lines = [head, f'# Starts {name} ({c["len"]} t) at the next rig tick.',
                 f'scoreboard players set @s {C} {c["id"]}', f'scoreboard players set @s {T} -1']
        if name not in hides:
            lines.append(f'execute if score @s {V} matches 1 run function {NSR}show')
        w(f'play/{name}', lines)
    vis = [p for p, v in PARTS.items() if v[0]]
    w('hide', [head, '# Every visible part at scale 0 (the warp).', f'scoreboard players set @s {V} 1']
      + [f'data merge entity {sel(p)} {{start_interpolation:0,interpolation_duration:1,transformation:{tf((0, 0, 0), PARTS[p][2])}}}' for p in vis])
    w('show', [head, '# Every part back.', f'scoreboard players set @s {V} 0']
      + [f'data merge entity {sel(p)} {{start_interpolation:0,interpolation_duration:2,transformation:{tf(PARTS[p][1], PARTS[p][2])}}}' for p in vis])
    for form, i in FORM_ID.items():
        w(f'form/{form}', [head, f'# Instant form {form}: the parts take its rest offsets on the next tick.',
                           f'scoreboard players set @s {F} {i}'])
    for look, i in LOOK_ID.items():
        glow = LOOK_GLOW[look]
        lines = [head, f'# Look {look}.', f'scoreboard players set @s {LK} {i}']
        if glow is None:
            lines.append(f'data merge entity {sel("core")} {{Glowing:0b}}')
        else:
            lines.append(f'data merge entity {sel("core")} {{Glowing:1b,glow_color_override:{glow}}}')
        lines.append(f'data modify entity {sel("core")} item set value {{id:"{"minecraft:copper_block" if look in ("groggy", "off") else "minecraft:gold_block"}",count:1}}')
        w(f'look/{look}', lines)
    for n in A.CRACKS:
        item = {0: 'minecraft:gold_block', 1: 'minecraft:gold_block', 2: 'minecraft:raw_gold_block', 3: 'minecraft:raw_gold_block',
                4: 'minecraft:copper_block'}[n]
        w(f'crack/{n}', [head, f'# Core bubble crack stage {n} (0-3 = meter hits 0-4 / 5-9 / 10-14 / 15-19, 4 = burst).',
                         f'scoreboard players set @s {K} {n}',
                         f'data modify entity {sel("core")} item set value {{id:"{item}",count:1}}'])
    w('face/player', [head, '# Instant yaw toward the player\'s body.',
                      'execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'])
    w('face/track', [head, '# At most 4 degrees per call toward the player\'s body (the device turns slowly).',
                     'function rlk:mboss/mv/turn {max:4}'])
    w('flash', [head, '# Hit flash: outline for 3 t.', f'scoreboard players set @s {Y} 3',
                f'execute as @e[type=minecraft:item_display,tag={TAG}] run data merge entity @s {{Glowing:1b,glow_color_override:16777215}}'])
    w('flash_tick', [f'scoreboard players remove @s {Y} 1',
                     f'execute if score @s {Y} matches ..0 as @e[type=minecraft:item_display,tag={TAG}] run data merge entity @s {{Glowing:0b}}'])
    w('kill', [head, f'kill @e[type=minecraft:item_display,tag={TAG}]'])
    w('prop/clear', [head, 'kill @e[type=minecraft:item_display,tag=rlk_mb_fg_prop]'])
    w('uninstall', [head, f'function {NSR}kill', f'function {NSR}prop/clear']
      + [f'scoreboard objectives remove {o}' for o in A.RIG_OBJECTIVES])
