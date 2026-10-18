"""STUB rig for the field generator's fx kit (removable; used only while the real rig manifest
tools/mboss_fieldgen_rig_manifest.json does not exist).

tools/build_mboss_fg_fx.py imports this module only in stub mode. It writes F:mboss/fieldgen/fx/rig_stub/** with the
rig API the kit calls (the real one is rlk:mboss/fieldgen/rig/..., built on wip/fg-rig): init, spawn, tick, kill,
uninstall, play/<clip>, form/<dormant|cruise|field|coreup|tower|laser|deployed>, look/<idle|charge|field|groggy|off>,
crack/<0..4>, face/player, face/track, flash and prop/clear. Clips only keep time (id, tick, loop / next, as the real
manifest's clip names); the figure is a crude vanilla stand-in (a sandstone ring slab, a gold core, an amethyst halo,
two gold spikes, a lightning-rod pendulum) plus the kit's own bubble overlay (bubble0..3) and violet column, so the
kit's demos (fx/test/demo/*) and the meter's crack calls are visible in game. Parts carry rlk_fk_rs (never the real
rig's tags) and follow the anchor at the form's rest-pose heights (model.md §8).

Delete this file once the real rig is merged: with the real manifest present the kit never imports it, calls
rlk:mboss/fieldgen/rig/... and removes F:mboss/fieldgen/fx/rig_stub/ on its next run.
"""
NS = 'rlk:mboss/fieldgen/fx/rig_stub/'
DIR = 'rig_stub'
OBJ = ('fkRsC', 'fkRsT', 'fkRsF', 'fkRsL', 'fkRsY', 'fkRsK')       # clip id, clip tick, form, look, flash, crack
C, T, F, LK, Y, K = OBJ
TAG = 'rlk_fk_rs'
SEL = f'@e[type=minecraft:item_display,tag={TAG}'

# clip -> (len, loop, next, form at start, form at the end or None)
CLIPS = {
    'entrance': (130, False, 'idle_cruise', 'dormant', 'cruise'),
    'idle_cruise': (40, True, None, 'cruise', None),
    'glide': (20, True, None, 'cruise', None),
    'bomb_run': (97, False, 'idle_cruise', 'cruise', None),
    'slam': (45, False, 'idle_cruise', 'cruise', None),
    'laser': (174, False, 'idle_cruise', 'laser', 'cruise'),
    'missiles': (73, False, 'idle_cruise', 'cruise', None),
    'coreup': (110, False, 'idle_cruise', 'coreup', 'cruise'),
    'tower_throw': (157, False, 'idle_cruise', 'tower', 'cruise'),
    'warp_out': (34, False, 'warp_in_field', 'cruise', None),
    'warp_in_field': (23, False, 'field_idle', 'field', None),
    'wave': (60, False, 'field_idle', 'field', None),
    'field_idle': (40, True, None, 'field', None),
    'field_erupt': (30, False, 'field_idle', 'field', None),
    'field_end': (102, False, 'idle_cruise', 'deployed', 'cruise'),
    'break': (34, False, 'groggy', 'field', 'cruise'),
    'groggy': (200, True, None, 'cruise', None),
    'recover': (15, False, 'idle_cruise', 'cruise', None),
    'death': (110, False, None, 'cruise', None),
}
CLIP_ID = {n: k for k, n in enumerate(CLIPS)}
# form -> (ring centre height H, core offset from the ring centre, halo shown, bubble shown, violet column shown)
FORMS = {
    'dormant': (2.15, 0.0, False, False, False),
    'cruise': (4.5, 0.1, True, False, False),
    'field': (5.8, -1.96, True, True, True),
    'coreup': (5.0, 2.8, True, False, False),
    'tower': (4.5, -0.4, True, False, False),
    'laser': (4.5, 0.1, True, False, False),
    'deployed': (5.6, -1.96, True, False, True),
}
FORM_ID = {n: k for k, n in enumerate(FORMS, 1)}
LOOKS = {'idle': 'minecraft:gold_block', 'charge': 'minecraft:shroomlight', 'field': 'minecraft:amethyst_block',
         'groggy': 'minecraft:copper_block', 'off': 'minecraft:smooth_stone'}
# part -> (x offset (left), y relative to 'ring' | 'core' plus dy, item or kit kind, scale, billboard)
PARTS = {
    'ring': (0.0, 'ring', 0.0, 'minecraft:smooth_sandstone', (6.4, 0.7, 6.4), 'fixed'),
    'core': (0.0, 'core', 0.0, 'minecraft:gold_block', (1.3, 1.3, 1.3), 'fixed'),
    'glow': (0.0, 'core', 0.0, 'kit:bubble0', (2.4, 2.4, 2.4), 'center'),
    'halo': (0.0, 'ring', 1.6, 'minecraft:amethyst_block', (3.2, 0.12, 3.2), 'fixed'),
    'spike_l': (3.5, 'ring', 0.0, 'minecraft:gold_block', (1.4, 0.35, 0.35), 'fixed'),
    'spike_r': (-3.5, 'ring', 0.0, 'minecraft:gold_block', (1.4, 0.35, 0.35), 'fixed'),
    'pendulum': (0.0, 'ring', -2.6, 'minecraft:lightning_rod', (1.0, 1.6, 1.0), 'fixed'),
    'column': (0.0, 'core', -0.5, 'kit:ousia_col', (1.0, 3.2, 1.0), 'fixed'),
}


def num(v):
    s = f'{v:.3f}'.rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def tf(scale):
    sx, sy, sz = scale
    return (f'{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
            f'scale:[{num(sx)}f,{num(sy)}f,{num(sz)}f]}}')


def item(spec):
    if spec.startswith('kit:'):
        return (f'{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"rlk:mboss/fg_kit/{spec[4:]}"}}}}')
    return f'{{id:"{spec}",count:1}}'


def shown(part, form):
    _h, _c, halo, bub, col = FORMS[form]
    return {'halo': halo, 'glow': bub, 'column': col}.get(part, True)


def emit(W):
    w = lambda rel, lines: W.w(f'{DIR}/{rel}', lines)      # noqa: E731
    head = '# STUB rig (tools/mboss_fg_fx_stub_rig.py): replaced by rlk:mboss/fieldgen/rig/ once its manifest exists.'
    w('init', [head, '# Objectives; safe on every load.'] + [f'scoreboard objectives add {o} dummy' for o in OBJ])
    spawn = [head, '# @s = anchor (the body on the floor under the axis), at it, rotated as it: kills old parts, summons the',
             '# stand-in in the cruise rest pose.', f'function {NS}init', f'function {NS}kill']
    for name, (_x, _ref, _dy, it, sc, bb) in PARTS.items():
        tags = f'["rlk_room","rlk_mb_aux","{TAG}","{TAG}_{name}"]'
        hid = not shown(name, 'cruise')
        spawn.append(f'summon minecraft:item_display ~ ~4.5 ~ {{Tags:{tags},billboard:"{bb}",item_display:"none",'
                     f'teleport_duration:1,interpolation_duration:2,brightness:{{block:14,sky:15}},view_range:3f,'
                     f'transformation:{tf((0, 0, 0) if hid else sc)},item:{item(it)}}}')
    spawn += [f'scoreboard players set @s {C} {CLIP_ID["idle_cruise"]}', f'scoreboard players set @s {T} -1',
              f'scoreboard players set @s {F} {FORM_ID["cruise"]}', f'scoreboard players set @s {LK} 0',
              f'scoreboard players set @s {Y} 0', f'scoreboard players set @s {K} 0']
    w('spawn', spawn)
    for form, (h, cdy, _ha, _bu, _co) in FORMS.items():
        lines = [head, f'# Parts to their {form} rest offsets (ring centre {h} b, core {num(cdy)} b from it) at the anchor yaw.']
        for name, (x, ref, dy, _it, _sc, _bb) in PARTS.items():
            y = (h if ref == 'ring' else h + cdy) + dy
            lines.append(f'execute positioned ^{num(x)} ^{num(y)} ^ run tp {SEL}_{name},limit=1] ~ ~ ~ ~ 0')
        w(f'follow/{form}', lines)
    follow = [head, '# @s = anchor, at it, rotated ~ 0 as it.']
    for form, k in FORM_ID.items():
        follow.append(f'execute if score @s {F} matches {k} run function {NS}follow/{form}')
    w('follow', follow)
    w('tick', [head, '# @s = anchor, at it; every game tick. Missing parts respawn.',
               f'execute unless entity {SEL}_ring,limit=1] run function {NS}spawn',
               f'execute rotated as @s rotated ~ 0 run function {NS}follow',
               f'scoreboard players add @s {T} 1',
               f'function {NS}run',
               f'execute if score @s {Y} matches 1.. run function {NS}flash_tick'])
    run = [head, '# Clip end: loop, next clip or hold, with the form at the end.']
    for name, (ln, loop, nxt, _f0, f1) in CLIPS.items():
        cid = CLIP_ID[name]
        if f1:
            run.append(f'execute if score @s {C} matches {cid} if score @s {T} matches {ln} run function {NS}form/{f1}')
        if loop:
            run.append(f'execute if score @s {C} matches {cid} if score @s {T} matches {ln}.. run scoreboard players set @s {T} 0')
        elif nxt:
            run.append(f'execute if score @s {C} matches {cid} if score @s {T} matches {ln}.. run return run function {NS}play/{nxt}')
    w('run', run)
    for name, (ln, _l, _n, f0, _f1) in CLIPS.items():
        w(f'play/{name}', [head, f'# Starts {name} ({ln} t) at the next rig tick, in form {f0}.',
                           f'scoreboard players set @s {C} {CLIP_ID[name]}', f'scoreboard players set @s {T} -1',
                           f'function {NS}form/{f0}'])
    for form, k in FORM_ID.items():
        lines = [head, f'# Instant form switch: {form}.', f'scoreboard players set @s {F} {k}']
        for name, (_x, _ref, _dy, _it, sc, _bb) in PARTS.items():
            if name in ('halo', 'glow', 'column'):
                s = sc if shown(name, form) else (0, 0, 0)
                lines.append(f'data merge entity {SEL}_{name},limit=1] {{start_interpolation:0,transformation:{tf(s)}}}')
        w(f'form/{form}', lines)
    for k, (look, it) in enumerate(LOOKS.items()):
        w(f'look/{look}', [head, f'# Core look: {look}.', f'scoreboard players set @s {LK} {k}',
                           f'data modify entity {SEL}_core,limit=1] item set value {item(it)}'])
    for k in range(5):
        lines = [head, f'# Core bubble crack stage {k} (0-3 the kit\'s bubble overlays, 4 = burst: hidden).',
                 f'scoreboard players set @s {K} {k}']
        if k < 4:
            lines.append(f'data modify entity {SEL}_glow,limit=1] item set value {item(f"kit:bubble{k}")}')
            lines.append(f'data merge entity {SEL}_glow,limit=1] {{start_interpolation:0,transformation:{tf(PARTS["glow"][4])}}}')
        else:
            lines.append(f'data merge entity {SEL}_glow,limit=1] {{start_interpolation:0,transformation:{tf((0, 0, 0))}}}')
        w(f'crack/{k}', lines)
    w('face/player', [head, '# Instant yaw toward the player\'s body.',
                      'execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'])
    w('face/track', [head, '# At most 12 degrees per call toward the player\'s body.', 'function rlk:mboss/mv/turn {max:12}'])
    w('flash', [head, '# Hit flash: outline for 3 t.', f'scoreboard players set @s {Y} 3',
                f'execute as {SEL}] run data merge entity @s {{Glowing:1b,glow_color_override:16777215}}'])
    w('flash_tick', [f'scoreboard players remove @s {Y} 1',
                     f'execute if score @s {Y} matches ..0 as {SEL}] run data merge entity @s {{Glowing:0b}}'])
    w('kill', [head, f'kill {SEL}]'])
    w('prop/clear', [head, f'kill {SEL}_prop]'])
    w('uninstall', [head, f'function {NS}kill'] + [f'scoreboard objectives remove {o}' for o in OBJ])
