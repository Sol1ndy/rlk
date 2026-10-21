"""The stand-in rig runtime AP:rig_stub/** (AP-CORE; ap_contract 0.4.9 API names): three item displays (body, head,
tail) that follow the anchor in the stance's rest offsets, show the visibility state, the form, the brightness and a hit
flash, and run the stub clips' clocks (apRigC / apRigT; loop / next / hold) with their state, stance, look and hand
events, so the core's px-set driver, yaw driver and stance reads work before the real rig (wip/ap-rig) lands. Written
while api.stub_rig_needed(); the real rig replaces it function by function (AP-I1 / AP-I2).

The stand-in never moves or turns the anchor (0.4.9): face/* only record the request (apRigY).
"""
from . import api as A
from .api import L

TAG = 'rlk_mb_aps'
NSR = f'{A.NS}rig_stub/'
HEAD = '# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.'
# part -> (item p1, item p3, {stance: (scale (x, y, z), offset (s, y, f))}, flash groups it answers)
FIG = {
    'sbody': ('minecraft:moss_block', 'minecraft:flowering_azalea_leaves',
              {0: ((4.2, 2.4, 6.0), (0.0, 2.6, -0.4)), 1: ((2.8, 4.6, 2.6), (0.0, 3.6, -0.1))},
              ('body', 'front', 'rear', 'arms')),
    'shead': ('minecraft:pitcher_plant', 'minecraft:spore_blossom',
              {0: ((2.4, 2.4, 2.4), (0.0, 3.4, 2.4)), 1: ((2.2, 2.2, 2.2), (0.0, 6.4, 0.3))},
              ('head',)),
    'stail': ('minecraft:stripped_mangrove_log', 'minecraft:mangrove_roots',
              {0: ((1.2, 1.0, 9.0), (0.6, 1.4, -7.4)), 1: ((1.0, 1.0, 4.0), (1.2, 0.8, -2.4))},
              ('tail',)),
}
ID_ROT = '[0f,0f,0f,1f]'


def _n(v):
    s = f'{float(v):.4f}'.rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def _tf(scale):
    sx, sy, sz = scale
    return (f'{{translation:[0f,0f,0f],left_rotation:{ID_ROT},right_rotation:[0f,0f,0f,1f],'
            f'scale:[{_n(sx)}f,{_n(sy)}f,{_n(sz)}f]}}')


def _sel(name):
    return f'@e[type=minecraft:item_display,tag=rlk_mb_ap_{name},tag={TAG},limit=1]'


def emit(g, man):
    w = lambda rel, lines: g.w(f'rig_stub/{rel}', lines)       # noqa: E731
    rt = man['runtime']
    objs = list(man['objectives'])
    ids = {c['name']: c['id'] for c in man['clips']}
    stub_clips = [c for c in man['clips'] if c['id'] >= 1000 and not c['name'].startswith('dbg_')]
    looks = man['looks']
    stance_id = man['stances']['ids']
    hand_sets = man['hands']['ids']

    w('init', [HEAD, '# The rig objectives (shared with the real rig); safe on every load.']
      + [f'scoreboard objectives add {o} dummy' for o in objs])
    spawn = [HEAD, '# @s = anchor, at it: kills old parts, summons the stand-in, keeps the stored channels (form, stance, state,',
             '# park, brightness), queues the idle of the form.',
             f'function {NSR}init', f'function {NSR}kill']
    for name, (item, _, st, _) in FIG.items():
        tags = f'["rlk_room","rlk_mb_aux","{TAG}","rlk_mb_ap_{name}"]'
        (sx, sy, sz), (x, y, z) = st[0]
        spawn.append(f'execute rotated as @s rotated ~ 0 run summon minecraft:item_display ^{_n(x)} ^{_n(y)} ^{_n(z)} '
                     f'{{Tags:{tags},billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:2,'
                     f'brightness:{{block:13,sky:15}},view_range:3f,width:24f,height:12f,transformation:{_tf((sx, sy, sz))},'
                     f'item:{{id:"{item}",count:1}}}}')
    for o, dflt in (('apRigForm', 0), ('apRigStance', 0), ('apRigState', 0), ('apRigPark', 0), ('apRigBright', 0),
                    ('apRigFace', 0), ('apRigCore', 0), ('apRigGlow', 0), ('apRigTint', 0), ('apRigHands', 0)):
        spawn.append(f'execute unless score @s {o} matches 0.. run scoreboard players set @s {o} {dflt}')
    spawn += [f'scoreboard players set @s {rt["clip_obj"]} {ids["idle_p1"]}',
              f'execute if score @s apRigForm matches 1 run scoreboard players set @s {rt["clip_obj"]} {ids["idle_p3"]}',
              f'scoreboard players set @s {rt["tick_obj"]} -1', 'scoreboard players set @s apRigF 0',
              f'function {NSR}look_apply']
    w('spawn', spawn)

    follow = [HEAD, '# @s = anchor, at it, rotated ~ 0 as it: the parts to the rest offsets of the stance (apRigStance).']
    for name, (_, _, st, _) in FIG.items():
        for k, (_, (x, y, z)) in sorted(st.items()):
            follow.append(f'execute if score @s apRigStance matches {k} positioned ^{_n(x)} ^{_n(y)} ^{_n(z)} run tp {_sel(name)} ~ ~ ~ ~ 0')
    w('follow', follow)
    w('tick', [HEAD, '# @s = anchor, at it; once per game tick after the module (the pose of this tick). Missing parts respawn;',
               '# parked: skipped (manifest park.tick "skip").',
               f'execute unless entity {_sel("sbody")} run function {NSR}spawn',
               'execute if score @s apRigPark matches 1 run return 0',
               f'execute rotated as @s rotated ~ 0 run function {NSR}follow',
               f'scoreboard players add @s {rt["tick_obj"]} 1',
               f'function {NSR}chain',
               f'execute if score @s apRigF matches 1.. run function {NSR}flash_tick'])

    # the clip clocks: a dispatch tree on the clip id -> cl/c<id> (events of this tick, then loop / next / hold)
    def ev_lines(c):
        rows = []
        for t, st in c.get('state') or []:
            rows.append((t, f'function {NSR}state/{st}'))
        for t, st in c.get('stance_events') or []:
            rows.append((t, f'function {NSR}stance/{st.lower()}'))
        for e in c.get('hand_events') or []:
            if len(e) == 3:
                rows.append((e[0], f'function {NSR}hand/{e[1]}/{e[2]}'))
            else:
                rows.append((e[0], f'function {NSR}hands/{e[1]}'))
        for t, ch, lk in c.get('look_events') or []:
            rows.append((t, f'function {NSR}bright/{lk}' if ch == 'bright' else f'function {NSR}look/{ch}/{lk}'))
        return sorted(rows, key=lambda r: r[0])
    cids = sorted(c['id'] for c in stub_clips)
    byid = {c['id']: c for c in stub_clips}

    def node(lo):
        if len(lo) <= 4:
            return [f'execute if score @s apRigC matches {c} run return run function {NSR}cl/c{c}' for c in lo]
        mid = len(lo) // 2
        out = []
        for part in (lo[:mid], lo[mid:]):
            nm = f'cl/d{part[0]}_{part[-1]}'
            w(nm, node(part))
            out.append(f'execute if score @s apRigC matches {part[0]}..{part[-1]} run return run function {NSR}{nm}')
        return out
    w('chain', [HEAD, '# The stub clips\' clocks (ids >= 1000): this tick\'s events, then loop / next / hold. Also called after a',
                '# real rig tick while clips fall back (api.rig_tick_lines).',
                'execute unless score @s apRigC matches 1000.. run return 0'] + node(cids))
    for cid in cids:
        c = byid[cid]
        lines = [f'# {c["name"]} ({c["len"]} t)']
        for t, ln in ev_lines(c):
            lines.append(f'execute if score @s apRigT matches {t} run {ln}')
        n = c['len']
        if c.get('loop'):
            lines.append(f'execute if score @s apRigT matches {n}.. run scoreboard players set @s apRigT 0')
        elif c.get('next'):
            lines.append(f'execute if score @s apRigT matches {n}.. run function {NSR}chain_to {{c:{ids[c["next"]]}}}')
        else:
            lines.append(f'execute if score @s apRigT matches {n}.. run scoreboard players set @s apRigT {n - 1}')
        w(f'cl/c{cid}', lines)
    w('chain_to', ['# The next clip starts at its tick 0 this same tick (its tick-0 events included).',
                   '$scoreboard players set @s apRigC $(c)', 'scoreboard players set @s apRigT 0',
                   f'function {NSR}chain'])
    for c in stub_clips:
        st0 = (c.get('stance') or {}).get('start', 'CROUCH')
        w(f'play/{c["name"]}', [HEAD, f'# Play {c["name"]} ({c["len"]} t, stub id {c["id"]}) from its tick 0 at the next rig tick (the',
                                '# stance of its first pose at once).',
                                f'scoreboard players set @s apRigC {c["id"]}', 'scoreboard players set @s apRigT -1',
                                f'function {NSR}stance/{st0.lower()}'])

    # visibility, stance, park
    for i, st in enumerate(('normal', 'burrowed')):
        w(f'state/{st}', [HEAD, f'# Visibility {st} (apRigState {i}).', f'scoreboard players set @s apRigState {i}',
                          f'function {NSR}shape'])
    shape = [HEAD, '# The parts\' scales from the visibility, the park flag and the stance.']
    for name, (_, _, st, _) in FIG.items():
        shape.append(f'execute if score @s apRigPark matches 1 run data merge entity {_sel(name)} {{transformation:{_tf((0, 0, 0))}}}')
        shape.append(f'execute unless score @s apRigPark matches 1 if score @s apRigState matches 1 run data merge entity {_sel(name)} '
                     f'{{start_interpolation:0,interpolation_duration:3,transformation:{_tf((0, 0, 0))}}}')
        for k, (sc, _) in sorted(st.items()):
            shape.append(f'execute unless score @s apRigPark matches 1 if score @s apRigState matches 0 if score @s apRigStance matches {k} '
                         f'run data merge entity {_sel(name)} {{start_interpolation:0,interpolation_duration:3,transformation:{_tf(sc)}}}')
    w('shape', shape)
    for st, k in stance_id.items():
        w(f'stance/{st.lower()}', [HEAD, f'# Snap to the {st} rest (apRigStance {k}).', f'scoreboard players set @s apRigStance {k}',
                                   f'function {NSR}shape'])
    w('park', [HEAD, '# Parked (R10): every part at scale 0, the tick skipped until unpark.', 'scoreboard players set @s apRigPark 1',
               f'function {NSR}shape'])
    w('unpark', [HEAD, '# Unparked: the stored channels again, the parts follow.', 'scoreboard players set @s apRigPark 0',
                 f'function {NSR}look_apply', f'execute rotated as @s rotated ~ 0 run function {NSR}follow'])

    # looks
    for ch, rec in looks.items():
        obj = rec['objective']
        for lk, i in rec['ids'].items():
            if ch == 'bright':
                rel = f'bright/{lk}'
                lines = [HEAD, f'# Body brightness {lk} ({obj} {i}).', f'scoreboard players set @s {obj} {i}']
                lines += [f'data merge entity {_sel(nm)} {{brightness:{{block:{lk},sky:15}}}}' for nm in FIG]
            else:
                rel = f'look/{ch}/{lk}'
                lines = [HEAD, f'# Look channel {ch} = {lk} ({obj} {i}).', f'scoreboard players set @s {obj} {i}']
                if ch == 'form':
                    for nm, (i1, i3, _, _) in FIG.items():
                        lines.append(f'data modify entity {_sel(nm)} item set value {{id:"{i1 if lk == "p1" else i3}",count:1}}')
                elif ch == 'core_glow':
                    lines.append(f'data merge entity {_sel("sbody")} {{Glowing:{"1b" if lk == "lit" else "0b"},glow_color_override:15065431}}')
            w(rel, lines)
    la = [HEAD, '# Every stored channel again (spawn, unpark, reload).']
    for ch, rec in looks.items():
        for lk, i in rec['ids'].items():
            fn = f'bright/{lk}' if ch == 'bright' else f'look/{ch}/{lk}'
            la.append(f'execute if score @s {rec["objective"]} matches {i} run function {NSR}{fn}')
    la.append(f'function {NSR}shape')
    w('look_apply', la)
    for hs, i in hand_sets.items():
        w(f'hands/{hs}', [HEAD, f'# Hand set {hs} (apRigHands {i}); the stand-in has no hand parts.', f'scoreboard players set @s apRigHands {i}'])
    for part, vs in man['hands']['variants'].items():
        for v in vs:
            w(f'hand/{part}/{v}', [HEAD, f'# {part} -> {v}; the stand-in has no hand parts.'])
    for grp in man['flash_groups']:
        parts = [nm for nm, rec in FIG.items() if grp in rec[3]] or ['sbody']
        w(f'flash/{grp}', [HEAD, f'# Hit flash of the {grp} group: a white outline for 3 t.', 'scoreboard players set @s apRigF 3']
          + [f'data merge entity {_sel(nm)} {{Glowing:1b,glow_color_override:16777215}}' for nm in parts])
    w('flash_tick', ['scoreboard players remove @s apRigF 1',
                     f'execute if score @s apRigF matches ..0 as @e[type=minecraft:item_display,tag={TAG}] run data merge entity @s {{Glowing:0b}}',
                     f'execute if score @s apRigF matches ..0 if score @s apRigGlow matches 1 run function {NSR}look/core_glow/lit'])
    w('face/player', [HEAD, '# The head toward the player (the stand-in has no head yaw; the anchor is never turned).',
                      'scoreboard players set @s apRigY 1'])
    w('face/track', [HEAD, '# The head tracks the player <= 2 deg per call (no head yaw in the stand-in).', 'scoreboard players set @s apRigY 2'])
    w('face/set', [HEAD, '# Macro {yaw}: the head yaw (no head yaw in the stand-in).', '$data modify storage rlk:mboss ap.rig_yaw set value $(yaw)'])
    w('kill', [HEAD, f'kill @e[type=minecraft:item_display,tag={TAG}]'])
    w('uninstall', [HEAD, f'function {NSR}kill'] + [f'scoreboard objectives remove {o}' for o in objs])
    assert L is not None
