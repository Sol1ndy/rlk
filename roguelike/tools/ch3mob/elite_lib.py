"""Shared helpers for the chapter-3 elites (part B: cs 성수 전갈, rv 성수 붉은 독수리, pc 원시 정령 기계·재구성자).

Owned by part B. elite.py imports only this module, which reuses the chapter-2 elite helpers (ch2mob.elite_lib:
objectives, haste, first-tick stats and the safe-ground walker, all generic over the mob id) without changing them.
Everything here writes only under cm/<m>/:

* lib(...)        = ch2mob.elite_lib.lib: lib/obj, lib/pre (haste -> #eStep), lib/first (1-level HP, no vanilla attack),
                    lib/walk + lib/walk_step + lib/drop (the safe-ground walker: 0.5 b steps over checked columns).
* rig(...)        display-entity rig: create / select / rebuild / tick sync / pose/<id> / hurt flash / death sequence,
                    poses from tools/ch3_elite_poses.json (written by tools/build_ch3_elite_rigs.mjs).
* HOOKS           the lines the shared files need (cm/tick, cm/vis, cm/flash, cm/clean, combat/apply); install_hooks()
                    applies them idempotently. B never commits those shared files: the lead / A's entry applies them.
"""
import json
from pathlib import Path

try:
    from ch2mob import elite_lib as L2
except ImportError:  # tools/ch2mob on sys.path as a plain directory
    import importlib.util
    _p = Path(__file__).resolve().parent.parent / 'ch2mob' / 'elite_lib.py'
    _s = importlib.util.spec_from_file_location('ch2_elite_lib', _p)
    L2 = importlib.util.module_from_spec(_s)
    _s.loader.exec_module(L2)

TOOLS = Path(__file__).resolve().parent.parent
POSES = TOOLS / 'ch3_elite_poses.json'
IDS = ('cs', 'rv', 'pc')
fl, arr, ps = L2.fl, L2.arr, L2.ps


def poses():
    return json.loads(POSES.read_text(encoding='utf-8'))['mobs']


def lib(w, m, *, hp):
    L2.lib(w, m, hp=hp)


# ---------------------------------------------------------------------------------------------- display rig
def rig(w, m, *, tp_dur=1, glow=(), death=None, death_fx='', die_fx='', frozen_extra=(), cull=3.0, fall=False):
    """death = list of (tick, pose id); the corpse is killed at the last tick. glow = parts drawn at full brightness
    (never tinted by the hurt flash). fall = the corpse drops 0.4 b per tick while the block under it is open."""
    f = lambda rel, text: w(f'cm/{m}/{rel}', text)  # noqa: E731
    P = poses()[m]
    parts, plist, models = P['parts'], P['poses'], P['models']
    tint = [p for p in parts if p not in glow]
    n = len(parts) + 1
    this = f'rlk_{m}_this'

    f('rig/select', '\n'.join([
        '# @s = brain or corpse anchor; cmId is the sole ownership key',
        f'tag @e[tag={this}] remove {this}',
        'scoreboard players operation #c2r tmp = @s cmId',
        f'execute as @e[tag=rlk_{m}_rig] if score @s cmId = #c2r tmp run tag @s add {this}']))
    lines = [f'# {len(parts)} item displays + a feet-origin anchor marker; model joint [8,8,8]',
             f'summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_{m}_rig","rlk_{m}_anchor","rlk_cmlink","rlk_cmsync","rlk_{m}_new"]}}']
    for p in parts:
        bright = p in glow
        comp = f'"minecraft:item_model":"{models[p]}"' + ('' if bright else ',"minecraft:custom_model_data":{colors:[16777215]}')
        extra = ',brightness:{sky:15,block:15}' if bright else ''
        tags = f'"rlk_room","rlk_pet","rlk_{m}_rig","rlk_{m}_part","rlk_{m}_{p}","rlk_cmlink","rlk_cmsync","rlk_{m}_new"' + (f',"rlk_{m}_tint"' if p in tint else '')
        lines.append(f'summon minecraft:item_display ~ ~ ~ {{Tags:[{tags}],NoGravity:1b,Invulnerable:1b,billboard:"fixed",'
                     f'item_display:"none",interpolation_duration:1,teleport_duration:{tp_dur},view_range:1.5f,width:{cull:g}f,height:{cull:g}f,'
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
            if part in p.get('model', {}) or (part in glow and any(part in q.get('model', {}) for q in plist)):
                mdl = p.get('model', {}).get(part, models[part])      # frame swap on a bright part (pc core -> red-hot core)
                item = f',item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{mdl}"}}}}'
            body.append(f'execute as @e[tag={this},tag=rlk_{m}_{part}] run data merge entity @s {{start_interpolation:0,'
                        f'interpolation_duration:{p["dur"]},transformation:{{translation:{arr(r["t"])},left_rotation:{arr(r["q"])},'
                        f'scale:{arr(r["s"])},right_rotation:[0f,0f,0f,1f]}}{item}}}')
        f(f'rig/pose/{p["id"]}', '\n'.join(body))
    f('rig/apply', '\n'.join([
        'execute store result storage rlk:c2e p.p int 1 run scoreboard players get #c2p tmp',
        f'function rlk:cm/{m}/rig/apply_m with storage rlk:c2e p']))
    f('rig/apply_m', f'$function rlk:cm/{m}/rig/pose/$(p)')
    flash_off = f'execute if score @s cmAH matches 1 as @e[tag={this},tag=rlk_{m}_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {{colors:[16777215]}}'
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
        flash_off,
        'execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1',
        f'tag @e[tag={this}] remove {this}']))
    f('rig/frozen', '\n'.join([
        '# frozen: hold the current pose, still clear the hurt flash', *frozen_extra, flash_off,
        'execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1',
        f'tag @e[tag={this}] remove {this}']))
    f('rig/hurt', '\n'.join([
        '# confirmed damage (cm/flash hook): red tint for 6 ticks; glowing parts stay bright',
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
    if fall:
        dt.append(f'execute if block ~ ~-0.4 ~ #rlk:cm_pass as @e[tag={this}] at @s run tp @s ~ ~-0.4 ~')
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
APPLY_ANCHOR = 'execute unless score #trueDmg tmp matches 1 run function rlk:combat/apply_mods'


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
    # 원시 정령 기계 core exposed (tag rlk_c3_core): every hit x1.5, any source / element, after the damage modifiers
    out.append(('combat/apply', 'after', APPLY_ANCHOR, 'execute if entity @s[tag=rlk_c3_core] run function rlk:cm/pc/core_hit'))
    return out


HOOKS = hook_lines()


def install_hooks(fn_root):
    """Idempotent: insert every HOOKS line into the shared files under <fn_root> (= data/rlk/function)."""
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
            if anchor not in s.split('\n'):
                raise SystemExit(f'hook anchor missing in {rel}: {anchor}')
            s = s.replace(anchor + '\n', anchor + '\n' + line + '\n', 1)
        p.write_text(s, encoding='utf-8')
        changed += 1
    return changed
