"""STUB rig for the butterfly module (removable; used only while api.STUB, i.e. the real rig manifest
tools/mboss_butterfly_rig_manifest.json does not exist yet).

It writes F:mboss/butterfly/rig_stub/** with the same API as the real rig (rlk:mboss/butterfly/rig/...): init,
spawn, tick, kill, uninstall, play/<clip>, look/<dendro|pyro|flat>, form/<human|butterfly>, face/player,
face/track, flash, prop/clear and prop/<name> for the manifest props. Clips only keep time (id, tick, loop /
next, the form switches of stub_rig_manifest.json "forms"); the figure is a crude vanilla stand-in (a lime glass
body, a froglight head and two glass-pane wings that show in butterfly form) so a test fight in game is readable.
Named parts (rlk_mb_bf_<name>) follow the anchor at rest-pose offsets, so fx anchors resolve.

Delete this file and stub_rig_manifest.json once the real rig is merged: with the real manifest present the module
build never imports it and removes F:mboss/butterfly/rig_stub/.
"""
from . import api as A
from .api import L

DIR = 'rig_stub'
NSR = f'{A.NS}{DIR}/'
C, T, F, LK, Y = A.RIG_OBJECTIVES[:5]          # clip id, clip tick, form (1 human 2 butterfly), look, flash
TAG = 'rlk_mb_bfs'                             # every stub part
# part -> (offset ^x ^y ^z from the anchor at its yaw, item or None (invisible anchor), scale)
PARTS = {
    'body': ((0.0, 1.3, 0.0), 'minecraft:lime_stained_glass', (0.7, 2.6, 0.45)),
    'head': ((0.0, 2.65, 0.0), 'minecraft:verdant_froglight', (0.42, 0.42, 0.42)),
    'foot_r': ((-0.26, 0.15, 0.1), None, None), 'foot_l': ((0.26, 0.15, 0.1), None, None),
    'hand_r': ((-0.95, 2.05, -0.15), None, None), 'hand_l': ((0.9, 1.75, -0.1), None, None),
    'core': ((0.0, 2.1, 0.25), None, None),
    'fwing_l': ((1.6, 3.2, -0.3), 'minecraft:lime_stained_glass_pane', (3.0, 3.0, 0.3)),
    'fwing_r': ((-1.6, 3.2, -0.3), 'minecraft:lime_stained_glass_pane', (3.0, 3.0, 0.3)),
    'hwing_l': ((1.2, 1.8, -0.3), 'minecraft:lime_stained_glass_pane', (2.2, 2.2, 0.3)),
    'hwing_r': ((-1.2, 1.8, -0.3), 'minecraft:lime_stained_glass_pane', (2.2, 2.2, 0.3)),
}
WINGS = [p for p in PARTS if 'wing' in p]
LOOK_ITEM = {'dendro': 'minecraft:lime_stained_glass_pane', 'pyro': 'minecraft:orange_stained_glass_pane',
             'flat': 'minecraft:green_stained_glass_pane'}
LOOK_ID = {'dendro': 0, 'pyro': 1, 'flat': 2}


def tf(scale, ty=0.0):
    sx, sy, sz = scale
    return (f'{{translation:[0f,{L.num(ty)}f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
            f'scale:[{L.num(sx)}f,{L.num(sy)}f,{L.num(sz)}f]}}')


def emit(g):
    w = lambda rel, lines: g.w(f'{DIR}/{rel}', lines)
    head = '# STUB rig (tools/mboss_butterfly/stub_rig.py): replaced by the real rig at merge time.'
    w('init', [head, '# Objectives; safe on every load.'] + [f'scoreboard objectives add {o} dummy' for o in A.RIG_OBJECTIVES])
    spawn = [head, '# @s = anchor (the body), at it, rotated as it: kills old parts, summons the stand-in in the idle pose.',
             f'function {NSR}init', f'function {NSR}kill']
    for name, (off, item, sc) in PARTS.items():
        tags = f'["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_butterfly_part","{TAG}","rlk_mb_bf_{name}"]'
        it = f',item:{{id:"{item}",count:1}}' if item else ''
        hidden = name in WINGS
        scale = sc if (sc and not hidden) else (0, 0, 0)
        spawn.append(f'summon minecraft:item_display ^{off[0]} ^{off[1]} ^{off[2]} {{Tags:{tags},billboard:"fixed",'
                     f'item_display:"none",teleport_duration:1,interpolation_duration:2,brightness:{{block:14,sky:15}},'
                     f'transformation:{tf(scale)}{it}}}')
    spawn += [f'scoreboard players set @s {C} {A.CLIPS["idle_h"]["id"]}', f'scoreboard players set @s {T} -1',
              f'scoreboard players set @s {F} 1', f'scoreboard players set @s {LK} 0', f'scoreboard players set @s {Y} 0']
    w('spawn', spawn)
    follow = [head, '# @s = anchor, at it, rotated ~ 0 as it: every part to its rest offset at the anchor yaw.']
    for name, (off, _, _) in PARTS.items():
        follow.append(f'execute positioned ^{off[0]} ^{off[1]} ^{off[2]} run tp @e[type=minecraft:item_display,tag=rlk_mb_bf_{name},tag={TAG},limit=1] ~ ~ ~ ~ 0')
    w('follow', follow)
    w('tick', [head, '# @s = anchor, at it; every game tick. Missing parts respawn.',
               f'execute unless entity @e[type=minecraft:item_display,tag={TAG},tag=rlk_mb_bf_body,limit=1] run function {NSR}spawn',
               f'execute rotated as @s rotated ~ 0 run function {NSR}follow',
               f'scoreboard players add @s {T} 1',
               f'function {NSR}run',
               f'execute if score @s {Y} matches 1.. run function {NSR}flash_tick'])
    run = [head, '# Clip end: loop, next clip or hold; the clips\' form switches (manifest "forms").']
    for name, c in A.CLIPS.items():
        if c['loop']:
            run.append(f'execute if score @s {C} matches {c["id"]} if score @s {T} matches {c["len"]}.. run scoreboard players set @s {T} 0')
        elif c['next']:
            run.append(f'execute if score @s {C} matches {c["id"]} if score @s {T} matches {c["len"]}.. run return run function {NSR}play/{c["next"]}')
    forms = A._MAN.get('forms', {})
    for name, (tick, form) in forms.items():
        if name in A.CLIPS:
            run.append(f'execute if score @s {C} matches {A.CLIPS[name]["id"]} if score @s {T} matches {tick} run function {NSR}form/{form}')
    if 'entrance' in A.CLIPS:
        burst = A.CLIPS['entrance']['events'].get('burst', 79)
        run.append(f'execute if score @s {C} matches {A.CLIPS["entrance"]["id"]} if score @s {T} matches {burst} run function {NSR}show')
    w('run', run)
    for name, c in A.CLIPS.items():
        lines = [head, f'# Starts {name} ({c["len"]} t) at the next rig tick.',
                 f'scoreboard players set @s {C} {c["id"]}', f'scoreboard players set @s {T} -1']
        if name == 'entrance':
            lines.append(f'function {NSR}hide')
        w(f'play/{name}', lines)
    sel = lambda names: ','.join(names)
    body_parts = [p for p, v in PARTS.items() if v[1] and p not in WINGS]
    w('hide', [head, '# Every visible part at scale 0 (entrance: inside the cocoon).']
      + [f'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_bf_{p},tag={TAG},limit=1] {{transformation:{tf((0, 0, 0))}}}'
         for p in body_parts + WINGS])
    w('show', [head, '# Body parts back (wings per the form).']
      + [f'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_bf_{p},tag={TAG},limit=1] {{start_interpolation:0,transformation:{tf(PARTS[p][2])}}}'
         for p in body_parts]
      + [f'execute if score @s {F} matches 2 run function {NSR}form/butterfly'])
    w('form/human', [head, '# Instant: wings and tendrils hidden.', f'scoreboard players set @s {F} 1']
      + [f'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_bf_{p},tag={TAG},limit=1] {{start_interpolation:0,transformation:{tf((0, 0, 0))}}}'
         for p in WINGS])
    w('form/butterfly', [head, '# Instant: wings shown.', f'scoreboard players set @s {F} 2']
      + [f'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_bf_{p},tag={TAG},limit=1] {{start_interpolation:0,transformation:{tf(PARTS[p][2])}}}'
         for p in WINGS])
    for look in A.LOOKS:
        item = LOOK_ITEM.get(look, LOOK_ITEM['dendro'])
        w(f'look/{look}', [head, f'# Wing element look: {look}.', f'scoreboard players set @s {LK} {LOOK_ID.get(look, 0)}']
          + [f'data modify entity @e[type=minecraft:item_display,tag=rlk_mb_bf_{p},tag={TAG},limit=1] item set value {{id:"{item}",count:1}}'
             for p in WINGS])
    w('face/player', [head, '# Instant yaw toward the player\'s body.',
                      'execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'])
    w('face/track', [head, '# At most 12 degrees per call toward the player\'s body.', 'function rlk:mboss/mv/turn {max:12}'])
    w('flash', [head, '# Hit flash: outline for 3 t.', f'scoreboard players set @s {Y} 3',
                f'execute as @e[type=minecraft:item_display,tag={TAG}] run data merge entity @s {{Glowing:1b,glow_color_override:16777215}}'])
    w('flash_tick', [f'scoreboard players remove @s {Y} 1',
                     f'execute if score @s {Y} matches ..0 as @e[type=minecraft:item_display,tag={TAG}] run data merge entity @s {{Glowing:0b}}'])
    w('kill', [head, f'kill @e[type=minecraft:item_display,tag={TAG}]'])
    w('prop/clear', [head, 'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop]'])
    for prop in A.PROPS:
        if prop == 'cocoon':
            w('prop/cocoon', [head, '# The entrance cocoon (white glass lozenge) at the execution position; free prop (rlk_mb_bf_prop).',
                              'summon minecraft:item_display ~ ~2.1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_prop","rlk_mb_bf_cocoon"],'
                              'billboard:"fixed",brightness:{block:15,sky:15},item:{id:"minecraft:white_stained_glass",count:1},'
                              f'transformation:{tf((1.3, 3.6, 1.3))}}}'])
        else:
            w(f'prop/{prop}', [head, f'# Prop {prop}: nothing in the stub.'])
    w('uninstall', [head, f'function {NSR}kill', f'function {NSR}prop/clear']
      + [f'scoreboard objectives remove {o}' for o in A.RIG_OBJECTIVES])
