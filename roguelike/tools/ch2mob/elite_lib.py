"""Local shim + shared helpers for the chapter-2 elites (part B: kr, nj, cc, ci).

Owned by part B. elite.py imports only this module (never A's common.py / swarm.py), so the two halves merge
file-disjoint. Everything here is generic over the mob id `m` and writes only under cm/<m>/:

* rig(...)        display-entity rig: create / select / rebuild / tick sync / pose/<id> / hurt flash / death sequence.
                  Pose transforms come from tools/ch2_elite_poses.json (written by tools/build_ch2_elite_rigs.mjs).
* lib(...)        per-mob preamble (haste: fixed-id movement modifier rlk:cm_haste +30 %, timers x1.3 as one extra
                  step on 3 of 10 game ticks), objectives, first-tick stats, and the safe-ground walker used by every
                  dash / reappearance / blink (never into blocks, never through walls or doors, never off a ledge).
* HOOKS           the lines the shared framework files need (cm/tick, cm/vis, cm/flash, cm/clean); install_hooks()
                  applies them idempotently. B never commits those shared files: the lead / A's entry applies them.
"""
import json
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
POSES = TOOLS / 'ch2_elite_poses.json'
IDS = ('kr', 'nj', 'cc', 'ci')


def fl(v):
    v = 0.0 if abs(v) < 5e-7 else round(v, 5)
    s = repr(float(v))
    if s.endswith('.0'):
        s = s[:-2]
    return s + 'f'


def arr(a):
    return '[' + ','.join(fl(x) for x in a) + ']'


def poses():
    return json.loads(POSES.read_text(encoding='utf-8'))['mobs']


def ps(sound, vol=1.0, pitch=1.0, where='~ ~ ~'):
    """playsound line (vanilla ids only; build/psnd.py wraps them later like every other pack sound)."""
    return f'playsound minecraft:{sound} master @a {where} {vol:g} {pitch:g}'


# ---------------------------------------------------------------------------------------------- per-mob library
def lib(w, m, *, hp, speed_note=''):
    f = lambda rel, text: w(f'cm/{m}/{rel}', text)  # noqa: E731
    f('lib/obj', '\n'.join([
        '# chapter-2 elite objectives (created on spawn; adding an existing objective is a harmless no-op)',
        'scoreboard objectives add c2eOw dummy',
        'scoreboard objectives add c2eA dummy',
        'scoreboard objectives add c2eF dummy',
        'scoreboard objectives add c2eQ dummy']))
    f('lib/pre', '\n'.join([
        '# every tick, first: haste (tag rlk_cm_haste set by a drumming 북잡이) -> #eStep 1 or 2',
        f'execute if entity @s[tag=rlk_cm_haste,tag=!rlk_c2_hs] run function rlk:cm/{m}/lib/haste_on',
        f'execute if entity @s[tag=!rlk_cm_haste,tag=rlk_c2_hs] run function rlk:cm/{m}/lib/haste_off',
        'scoreboard players set #eStep tmp 1',
        f'execute if entity @s[tag=rlk_c2_hs] run function rlk:cm/{m}/lib/haste_step',
        f'execute unless score @s c2eQ matches 1 run function rlk:cm/{m}/lib/first']))
    f('lib/haste_on', '\n'.join([
        'attribute @s minecraft:movement_speed modifier add rlk:cm_haste 0.3 add_multiplied_base',
        'tag @s add rlk_c2_hs']))
    f('lib/haste_off', '\n'.join([
        'attribute @s minecraft:movement_speed modifier remove rlk:cm_haste',
        'tag @s remove rlk_c2_hs']))
    f('lib/haste_step', '\n'.join([
        '# x1.3 timers: one extra step on game ticks 0, 3 and 6 of every 10 (integer, deterministic)',
        'execute store result score #eHz tmp run time query gametime',
        'scoreboard players operation #eHz tmp %= #10 tmp',
        'execute if score #eHz tmp matches 0 run scoreboard players set #eStep tmp 2',
        'execute if score #eHz tmp matches 3 run scoreboard players set #eStep tmp 2',
        'execute if score #eHz tmp matches 6 run scoreboard players set #eStep tmp 2',
        'execute if score #eStep tmp matches 2 if score @s cmCd matches 1.. run scoreboard players remove @s cmCd 1',
        'execute if score #eStep tmp matches 2 if score @s cmCd2 matches 1.. run scoreboard players remove @s cmCd2 1']))
    f('lib/first', '\n'.join([
        f'# first brain tick: the 1-level HP ({hp}) and no vanilla attack, whatever the room init left in #mhp / #mad',
        'scoreboard players set @s c2eQ 1',
        f'scoreboard players set @s mhp0 {hp}',
        'execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1',
        'function rlk:mob/level_apply',
        'attribute @s minecraft:attack_damage base set 0']))
    walker(f, m)


def walker(f, m):
    """Safe-ground walker. @s = a cursor marker (rlk_c2cur), rotated toward the travel direction, pitch 0.
    Steps 0.5 b at a time while the column ahead has free feet/body/head space (#rlk:dash_pass: no water, lava,
    barrier, iron bars, glass, doors or walls) and solid ground (not #rlk:cm_pass) under it; climbs or drops at most
    one block per step and never across a drop deeper than one block. #wN = steps allowed, #wK = steps taken.
    Ends snapped to the centre of the last good column (that column was fully checked)."""
    f('lib/walk', '\n'.join([
        'scoreboard players set #wK tmp 0',
        f'execute if score #wN tmp matches 1.. at @s run function rlk:cm/{m}/lib/walk_step',
        'execute at @s align xz positioned ~0.5 ~ ~0.5 run tp @s ~ ~ ~']))
    f('lib/walk_step', '\n'.join([
        'scoreboard players set #wOk tmp 0',
        '# flat / one down / one up; the body also needs 0.3 b of room on both sides (no corner squeezing)',
        'execute if block ^ ^0.3 ^0.5 #rlk:dash_pass if block ^ ^1.2 ^0.5 #rlk:dash_pass if block ^ ^1.85 ^0.5 #rlk:dash_pass unless block ^ ^-0.5 ^0.5 #rlk:cm_pass if block ^0.3 ^1 ^0.5 #rlk:dash_pass if block ^-0.3 ^1 ^0.5 #rlk:dash_pass run scoreboard players set #wOk tmp 1',
        'execute if score #wOk tmp matches 0 if block ^ ^0.3 ^0.5 #rlk:dash_pass if block ^ ^1.2 ^0.5 #rlk:dash_pass if block ^ ^1.85 ^0.5 #rlk:dash_pass if block ^ ^-0.5 ^0.5 #rlk:cm_pass unless block ^ ^-1.5 ^0.5 #rlk:cm_pass if block ^0.3 ^0.2 ^0.5 #rlk:dash_pass if block ^-0.3 ^0.2 ^0.5 #rlk:dash_pass run scoreboard players set #wOk tmp 2',
        'execute if score #wOk tmp matches 0 unless block ^ ^0.3 ^0.5 #rlk:cm_pass if block ^ ^1.3 ^0.5 #rlk:dash_pass if block ^ ^2.2 ^0.5 #rlk:dash_pass if block ^ ^2.85 ^0.5 #rlk:dash_pass if block ~ ~2.85 ~ #rlk:dash_pass if block ^0.3 ^2 ^0.5 #rlk:dash_pass if block ^-0.3 ^2 ^0.5 #rlk:dash_pass run scoreboard players set #wOk tmp 3',
        'execute if score #wOk tmp matches 0 run return 0',
        'execute if score #wOk tmp matches 1 run tp @s ^ ^ ^0.5',
        'execute if score #wOk tmp matches 2 run tp @s ^ ^-1 ^0.5',
        'execute if score #wOk tmp matches 3 run tp @s ^ ^1 ^0.5',
        'scoreboard players add #wK tmp 1',
        'scoreboard players remove #wN tmp 1',
        f'execute if score #wN tmp matches 1.. at @s run function rlk:cm/{m}/lib/walk_step']))
    f('lib/drop', '\n'.join([
        '# cursor straight down onto the ground below it (at most 2 b: under a jumping player, never into a pit)',
        'scoreboard players set #wD tmp 8',
        f'function rlk:cm/{m}/lib/drop_step']))
    f('lib/drop_step', '\n'.join([
        'execute at @s unless block ~ ~-0.25 ~ #rlk:cm_pass run return 0',
        'execute at @s run tp @s ~ ~-0.25 ~',
        'scoreboard players remove #wD tmp 1',
        f'execute if score #wD tmp matches 1.. run function rlk:cm/{m}/lib/drop_step']))


# ---------------------------------------------------------------------------------------------- display rig
def rig(w, m, *, tp_dur=1, glow=(), bright_all=False, death=None, death_fx='', die_fx='', frozen_extra=()):
    """death = list of (tick, pose id); the corpse is killed at the last tick. glow = parts drawn at full brightness."""
    f = lambda rel, text: w(f'cm/{m}/{rel}', text)  # noqa: E731
    P = poses()[m]
    parts, plist = P['parts'], P['poses']
    tint = [p for p in parts if p not in glow and not bright_all]
    n = len(parts) + 1
    this = f'rlk_{m}_this'

    f('rig/select', '\n'.join([
        f'# @s = brain or corpse anchor; cmId is the sole ownership key',
        f'tag @e[tag={this}] remove {this}',
        'scoreboard players operation #c2r tmp = @s cmId',
        f'execute as @e[tag=rlk_{m}_rig] if score @s cmId = #c2r tmp run tag @s add {this}']))
    lines = [f'# {len(parts)} item displays + a feet-origin anchor marker; model pivot [8,8,8]',
             f'summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_{m}_rig","rlk_{m}_anchor","rlk_cmlink","rlk_cmsync","rlk_{m}_new"]}}']
    for p in parts:
        bright = p in glow or bright_all
        model = plist[0].get('model', {}).get(p, f'rlk:cm/{m}/{p}')
        comp = f'"minecraft:item_model":"{model}"' + ('' if bright else ',"minecraft:custom_model_data":{colors:[16777215]}')
        extra = ',brightness:{sky:15,block:15}' if bright else ''
        tags = f'"rlk_room","rlk_pet","rlk_{m}_rig","rlk_{m}_part","rlk_{m}_{p}","rlk_cmlink","rlk_cmsync","rlk_{m}_new"' + (',"rlk_%s_tint"' % m if p in tint else '')
        lines.append(f'summon minecraft:item_display ~ ~ ~ {{Tags:[{tags}],NoGravity:1b,Invulnerable:1b,billboard:"fixed",'
                     f'item_display:"none",interpolation_duration:1,teleport_duration:{tp_dur},view_range:1.5f,width:3f,height:3f,'
                     f'shadow_radius:0f{extra},item:{{id:"minecraft:paper",count:1,components:{{{comp}}}}}}}')
    lines += [f'scoreboard players operation @e[tag=rlk_{m}_new] cmId = #c2r tmp',
              f'tag @e[tag=rlk_{m}_new] add {this}',
              f'tag @e[tag=rlk_{m}_new] remove rlk_{m}_new',
              f'function rlk:cm/{m}/rig/pose/{plist[0]["id"]}',
              'scoreboard players set @s cmAP -1',
              'scoreboard players set @s cmAH 0',
              'scoreboard players set @s cmAF 0']
    f('rig/create', '\n'.join(['# @s = brain, at @s', 'scoreboard players operation #c2r tmp = @s cmId'] + lines))
    f('rig/rebuild', '\n'.join([
        '# missing or extra displays (reload, chunk unload): replace only this mob\'s rig',
        f'function rlk:cm/{m}/rig/select',
        f'kill @e[tag={this}]',
        f'function rlk:cm/{m}/rig/create',
        f'function rlk:cm/{m}/rig/select']))
    for p in plist:
        body = [f'# {p["name"]} ({p["dur"]} t)']
        for part in parts:
            r = p['rig'][part]
            item = ''
            if part in p.get('model', {}):        # frame swap (the cicin's wing beat): bright, untinted parts only
                item = f',item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{p["model"][part]}"}}}}'
            body.append(f'execute as @e[tag={this},tag=rlk_{m}_{part}] run data merge entity @s {{start_interpolation:0,'
                        f'interpolation_duration:{p["dur"]},transformation:{{translation:{arr(r["t"])},left_rotation:{arr(r["q"])},'
                        f'scale:{arr(r["s"])},right_rotation:[0f,0f,0f,1f]}}{item}}}')
        f(f'rig/pose/{p["id"]}', '\n'.join(body))
    f('rig/apply', '\n'.join([
        'execute store result storage rlk:c2e p.p int 1 run scoreboard players get #c2p tmp',
        f'function rlk:cm/{m}/rig/apply_m with storage rlk:c2e p']))
    f('rig/apply_m', f'$function rlk:cm/{m}/rig/pose/$(p)')
    f('rig/tick', '\n'.join([
        f'# @s = brain, at @s (from cm/vis). Keeps the displays synced, faced and posed; AI lives in cm/{m}/tick',
        f'function rlk:cm/{m}/rig/select',
        f'execute store result score #c2n tmp if entity @e[tag={this}]',
        f'execute unless score #c2n tmp matches {n} run function rlk:cm/{m}/rig/rebuild',
        f'tag @e[tag={this}] add rlk_cmsync',
        f'function rlk:cm/{m}/rig/face',
        f'execute if score @s frzT matches 1.. run return run function rlk:cm/{m}/rig/frozen',
        f'function rlk:cm/{m}/rig/choose',
        f'execute unless score @s cmAP = #c2p tmp run function rlk:cm/{m}/rig/apply',
        'scoreboard players operation @s cmAP = #c2p tmp',
        f'execute if score @s cmAH matches 1 as @e[tag={this},tag=rlk_{m}_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {{colors:[16777215]}}',
        'execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1',
        f'tag @e[tag={this}] remove {this}']))
    f('rig/frozen', '\n'.join([
        '# frozen: hold the current pose, still clear the hurt flash', *frozen_extra,
        f'execute if score @s cmAH matches 1 as @e[tag={this},tag=rlk_{m}_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {{colors:[16777215]}}',
        'execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1',
        f'tag @e[tag={this}] remove {this}']))
    f('rig/hurt', '\n'.join([
        '# confirmed damage (cm/flash hook): red tint for 6 ticks; glow parts stay bright',
        'scoreboard players set @s cmAH 6',
        f'function rlk:cm/{m}/rig/select',
        f'execute as @e[tag={this},tag=rlk_{m}_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {{colors:[16737903]}}',
        f'tag @e[tag={this}] remove {this}']))
    death = death or [(0, plist[-1]['id']), (6, None)]
    last = death[-1][0]
    f('rig/die', '\n'.join([
        '# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId',
        f'function rlk:cm/{m}/rig/select',
        f'tag @e[tag={this}] add rlk_{m}_dying',
        f'tag @e[tag={this}] add rlk_cmsync',
        'scoreboard players set @s cmAD 0',
        f'execute as @e[tag={this},tag=rlk_{m}_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {{colors:[16777215]}}',
        f'function rlk:cm/{m}/rig/pose/{death[0][1]}'] + ([die_fx] if die_fx else []) + [f'tag @e[tag={this}] remove {this}']))
    dt = [f'function rlk:cm/{m}/rig/select', 'scoreboard players add @s cmAD 1']
    for t, pid in death[1:]:
        if pid is not None:
            dt.append(f'execute if score @s cmAD matches {t} run function rlk:cm/{m}/rig/pose/{pid}')
    if death_fx:
        dt.append(death_fx)
    dt += [f'execute if score @s cmAD matches {last}.. run kill @e[tag={this}]',
           f'tag @e[tag={this}] add rlk_cmsync',
           f'tag @e[tag={this}] remove {this}']
    f('rig/death_tick', '\n'.join(dt))
    return parts, plist


# ---------------------------------------------------------------------------------------------- shared hooks
def hook_lines():
    """(shared function, mode, anchor, line). mode 'after' inserts after the anchor line, 'prefix' at the top."""
    out = []
    for m in IDS:
        out.append(('cm/tick', 'after', 'execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_cn] run function rlk:cm/cn/tick',
                    f'execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_{m}] run function rlk:cm/{m}/tick'))
        out.append(('cm/vis', 'prefix', None, f'execute if entity @s[tag=rlk_cm_{m}] run return run function rlk:cm/{m}/rig/tick'))
        out.append(('cm/flash', 'prefix', None, f'execute if entity @s[tag=rlk_cm_{m}] run return run function rlk:cm/{m}/rig/hurt'))
        out.append(('cm/clean', 'prefix', None, f'execute as @e[tag=rlk_{m}_anchor,tag=rlk_{m}_dying] at @s run function rlk:cm/{m}/rig/death_tick'))
        out.append(('cm/clean', 'prefix', None, f'execute as @e[tag=rlk_{m}_anchor,tag=!rlk_cmsync,tag=!rlk_{m}_dying] at @s run function rlk:cm/{m}/rig/die'))
    return out


HOOKS = hook_lines()


def install_hooks(fn_root):
    """Idempotent: insert every HOOKS line into the shared cm files under <fn_root> (= data/rlk/function)."""
    root = Path(fn_root)
    changed = 0
    for rel, mode, anchor, line in HOOKS:
        p = root / (rel + '.mcfunction')
        s = p.read_text(encoding='utf-8').replace('\r\n', '\n')
        if line in s.split('\n'):
            continue
        if mode == 'prefix':
            s = line + '\n' + s
        else:
            if anchor not in s:
                raise SystemExit(f'hook anchor missing in {rel}: {anchor}')
            s = s.replace(anchor, anchor + '\n' + line, 1)
        p.write_text(s, encoding='utf-8')
        changed += 1
    return changed
