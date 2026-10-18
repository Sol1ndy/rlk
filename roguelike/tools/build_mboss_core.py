#!/usr/bin/env python3
"""Mid-boss (중간보스) framework generator.

    python3 tools/build_mboss_core.py

Reads tools/mboss_registry.json and writes the generic runtime F:mboss/** (F = data/rlk/function):
registry, roll, gate, start / won / abort, teleports, world tick and pause, bars, typed lines,
the generated numeric dispatchers F:mboss/d/<hook>, and the libraries the boss modules use
(hz = ground hazards, pj = projectile props, pull, mv = movement/leash, aux = hit routing for
helper objects, true damage), plus the test commands F:mboss/test/*.

It owns every file under F:mboss/ EXCEPT F:mboss/arena/ (tools/build_mboss_arena.py) and the
per-boss module directories F:mboss/<id>/ (one generator per boss). Stale files inside its own
directories are deleted on every run. Hand-written engine hooks (combat/apply, room/*, lvup/*,
tick, load, uninstall, ...) call into these functions; see README.md "중간보스".

Units at the runtime boundary: distances in tenths of a block (r:50 = 5 blocks), times in ticks,
damage as a percentage of the boss's base hit (dmg:160 = 1.6 x registry atk), elements in #elem
numbering (0 physical 1 pyro 2 hydro 3 electro 4 cryo 5 geo 6 anemo 7 dendro).
"""
import math
import mboss_lib as L

REG = L.load_registry()
A = REG['arena']
BOSSES = L.enabled_bosses(REG)
CX, CY, CZ = A['cx'], A['cy'], A['cz']
SAFE, WALK, RAD = A['safe'], A['walk'], A['r']
# Arena box (also used by the arena generator and room/remove): centre +-24, y 190..240.
BX0, BZ0 = CX - 24, CZ - 24
TOK = {
    '@CX@': str(CX), '@CY@': str(CY), '@CZ@': str(CZ),
    '@SAFE@': str(SAFE), '@SAFE1@': str(SAFE + 1), '@WALK@': str(WALK), '@WALK2@': str(WALK + 2),
    '@OOB@': L.num(WALK + 1.5), '@BOX@': f'{BX0} 190 {BZ0}', '@BOXD@': 'dx=47,dy=50,dz=47',
    '@SAFEP@': L.num(SAFE - 0.5), '@WALKP@': L.num(WALK - 0.7),
    # forceloaded chunk box of the arena (load, room/setup, mboss/start; released by uninstall, room/remove)
    '@FL@': f'{BX0} {BZ0} {BX0 + 47} {BZ0 + 47}',
}
out = L.Out(owned_dirs=['mboss/d', 'mboss/hz', 'mboss/pj', 'mboss/pull', 'mboss/mv', 'mboss/aux',
                        'mboss/line', 'mboss/test', 'mboss/box'],
            owned_files=[])
CORE_TOP = set()


def w(name, text):
    for k, v in TOK.items():
        text = text.replace(k, v)
    if '/' not in name:
        CORE_TOP.add(name)
    out.write('mboss/' + name, text)


T = '[{text:"[중간보스] ",color:"#E0703A",bold:true},'
TT = '[{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},'


def link(cmd, label=None, color='yellow'):
    return f"{{text:\"{label or cmd}\",color:\"{color}\",bold:false,click_event:{{action:\"suggest_command\",command:'{cmd}'}}}}"


def gray(t):
    return f'{{text:"{t}",color:"gray",bold:false}}'


# =============================================================================================
# Objectives
PER_ENTITY = [
    # hazards
    'mbHzK', 'mbHzT', 'mbHzW', 'mbHzA', 'mbHzL', 'mbHzD', 'mbHzE', 'mbHzB', 'mbHzKD', 'mbHzS',
    'mbHzV', 'mbHzI', 'mbHzR', 'mbHzR0', 'mbHzC', 'mbHzAng', 'mbHzRR', 'mbHzRI', 'mbHzLo',
    'mbHzHi', 'mbHzHW', 'mbHzFX', 'mbHzFZ', 'mbHzY0', 'mbHzY1', 'mbHzHit', 'mbHzCol',
    # hazard volley group (one hit per group)
    'mbHzG',
    # hazard options of the field generator: no dash dodge (mbHzND), re-arm period / re-arm clock (mbHzRA / mbHzRT)
    'mbHzND', 'mbHzRA', 'mbHzRT',
    # projectiles (mbPjK hit shape 0 sphere / 1 blade, mbPjG volley group)
    'mbPjV', 'mbPjT', 'mbPjL', 'mbPjD', 'mbPjE', 'mbPjB', 'mbPjR', 'mbPjHit', 'mbPjRet', 'mbPjW', 'mbPjK', 'mbPjG',
    # pull
    'mbPlT', 'mbPlF',
    # movement
    'mbMvK', 'mbMvT', 'mbMvN', 'mbMvH', 'mbMvX0', 'mbMvY0', 'mbMvZ0', 'mbMvX1', 'mbMvY1', 'mbMvZ1',
    # free per-entity scratch for boss modules (timers, ids, states)
    'mbT', 'mbS', 'mbId',
]
OBJECTIVES = ['mb', 'mres', 'pkMb'] + PER_ENTITY

# =============================================================================================
# Registry
def snbt_entry(b):
    start = b.get('start', A['start'])
    picks = int(b.get('picks', 2))
    icon = b.get('icon', {'item': 'minecraft:wither_skeleton_skull', 'model': 'minecraft:wither_skeleton_skull'})
    s = L.snbt_str
    parts = [
        f'id:{s(b["id"])}', f'n:{b["n"]}', f'w:{b["w"]}', f'minCh:{b["minCh"]}', f'maxCh:{b["maxCh"]}',
        f'name:{s(b["name"])}', f'sub:{s(b["sub"])}', f'color:{s(b["color"])}', f'el:{b["el"]}',
        f'hp:{b["hp"]}', f'xp:{b["xp"]}', f'atk:{b["atk"]}', f'lvAdd:{b.get("lvAdd", 0)}',
        f'dmgMul:{b["dmgMul"]}', f'goldMul:{b["goldMul"]}', f'sap:{b["sap"]}', f'picks:{picks}',
        f'scale:{L.num(float(b.get("scale", 1.0)))}d', f'intro:{b["intro"]}', f'death:{b["death"]}',
        # deathSnd false: the module composes its own (non-vocal) death sound, the framework plays none
        f'deathSnd:{1 if b.get("deathSnd", True) else 0}b',
        'hit:{w:%sf,h:%sf}' % (L.num(float(b['hit']['w'])), L.num(float(b['hit']['h']))),
        'start:{x:%sd,y:%sd,z:%sd,yaw:%sf,pitch:%sf}' % tuple(L.num(float(start[k])) for k in ('x', 'y', 'z', 'yaw', 'pitch')),
        f'title:{{text:{s(b["name"])},color:{s(b["color"])},bold:true}}',
        f'gate:{{item:{s(icon["item"])},model:{s(icon["model"])},name:{s(b["name"])},'
        f'desc:{s("좌클릭으로 도전 · 처치 시 아이템 상자 %d개" % picks)},color:{s(b["color"])}}}',
    ]
    return '{' + ','.join(parts) + '}'


reg_lines = ['# GENERATED by tools/build_mboss_core.py from tools/mboss_registry.json (enabled entries only).',
             '# reg[]: roll candidates and their stats. byid.<id>.n: lookup for test commands.',
             'data modify storage rlk:mboss reg set value [' + ','.join(snbt_entry(b) for b in BOSSES) + ']',
             'data modify storage rlk:mboss byid set value {' + ','.join(f'{b["id"]}:{{n:{b["n"]}}}' for b in BOSSES) + '}',
             f'scoreboard players set #mbN mb {len(BOSSES)}',
             '# Bosses the normal node roll can pick (w >= 1). 0 keeps the 중간보스 node out of the offers.',
             f'scoreboard players set #mbRoll mb {sum(1 for b in BOSSES if b["w"] >= 1)}']
w('register', '\n'.join(reg_lines))

cos_table = [round(math.cos(math.radians(a)) * 1000) for a in range(181)]
hzc = [L.colour_list(L.HZ_COLOURS[e]) for e in range(9)] + [L.colour_list(L.STRIKE_COLOUR),
                                                            L.colour_list((0.35, 0.95, 0.45))]
w('init', '\n'.join(
    ['# From rlk:load. Objectives, the three boss bars, registry, tables; a /reload keeps a running fight',
     '# (HP kept, aux entities rebuilt by the module reload hook).']
    + [f'scoreboard objectives add {o} dummy' for o in OBJECTIVES]
    + ['bossbar add rlk:mboss {text:"중간보스"}',
       'bossbar add rlk:mboss_state {text:""}',
       'bossbar add rlk:mboss_sub {text:""}',
       '# Resource-pack boss bar (tools/build_bossbar.py): white bars are transparent; the names carry',
       '# the name line, the drawn HP bar (bossui) and the module sub-line.',
       'bossbar set rlk:mboss color white', 'bossbar set rlk:mboss_state color white', 'bossbar set rlk:mboss_sub color white',
       'bossbar set rlk:mboss style progress', 'bossbar set rlk:mboss_state style progress', 'bossbar set rlk:mboss_sub style progress',
       'function rlk:mboss/register',
       'data modify storage rlk:mboss cos set value [' + ','.join(map(str, cos_table)) + ']',
       '# Telegraph colours by #elem 0..8, then 9 = strike flash, 10 = safe zone.',
       'data modify storage rlk:mboss hzc set value [' + ','.join(f'"{c}"' for c in hzc) + ']',
       'execute unless data storage rlk:mboss met run data modify storage rlk:mboss met set value []',
       'execute unless data storage rlk:mboss sub run data modify storage rlk:mboss sub set value []',
       'execute unless data storage rlk:mboss extra run data modify storage rlk:mboss extra set value []',
       'execute unless data storage rlk:mboss aura run data modify storage rlk:mboss aura set value []',
       'scoreboard players set #c2 mb 2', 'scoreboard players set #c4 mb 4', 'scoreboard players set #c10 mb 10',
       'scoreboard players set #c30 mb 30', 'scoreboard players set #c100 mb 100', 'scoreboard players set #c500 mb 500',
       'scoreboard players set #c1000 mb 1000', 'scoreboard players set #c10000 mb 10000', 'scoreboard players set #cm1 mb -1',
       'scoreboard players set #c36000 mb 36000',
       'execute unless score #mbOn mb matches 0.. run scoreboard players set #mbOn mb 0',
       'execute unless score #mbSt mb matches 0.. run scoreboard players set #mbSt mb 0',
       'execute unless score #mbKilled mb matches 0.. run scoreboard players set #mbKilled mb 0',
       'execute unless score #mbTest mb matches 0.. run scoreboard players set #mbTest mb 0',
       'execute unless score #mbForce mb matches 0.. run scoreboard players set #mbForce mb 0',
       'execute unless score #mbLock mb matches 0.. run scoreboard players set #mbLock mb 0',
       'execute unless score #mbId mb matches 0.. run scoreboard players set #mbId mb 0',
       'execute unless score #mbGoldMul mb matches 1.. run scoreboard players set #mbGoldMul mb 5',
       'execute unless score #mbSap mb matches 0.. run scoreboard players set #mbSap mb 1',
       'execute unless score #mbLive mb matches 0.. run scoreboard players set #mbLive mb 0',
       'execute unless score #mbLd mb matches 0.. run scoreboard players set #mbLd mb 0',
       '# Player-side fight modifiers a module may set (player_heal, items/hook/stat_buffs); a /reload keeps a',
       '# running fight\'s values (the module reload hook re-asserts them), so only unset ones are initialised.',
       'execute unless score #mbHealPct mb matches -1000.. run scoreboard players set #mbHealPct mb 100',
       'execute unless score #mbCritAdd mb matches -1000.. run scoreboard players set #mbCritAdd mb 0',
       'execute unless score #mbHealEv mb matches 0.. run scoreboard players set #mbHealEv mb 0',
       'execute unless score #mbGrpN mb matches 0.. run scoreboard players set #mbGrpN mb 0',
       '# Low gravity requested by the running module (#mbLowG 1; mboss/main clears it every tick, the module tick sets it',
       '# again; rlk:tick syncs the attribute modifiers through mboss/lowg_on|off). Hazard re-arm clock (hz/all).',
       'execute unless score #mbLowG mb matches 0..1 run scoreboard players set #mbLowG mb 0',
       'execute unless score #mbHzClk mb matches 0.. run scoreboard players set #mbHzClk mb 0',
       'scoreboard players set #mbNoDodge mb 0',
       '# Library activity flags (a set flag makes the world tick scan for that library\'s entities once).',
       'scoreboard players set #mbHzOn mb 1', 'scoreboard players set #mbPjOn mb 1',
       'scoreboard players set #mbPlOn mb 1', 'scoreboard players set #mbMvOn mb 1',
       'function rlk:mboss/opts_reset',
       'function rlk:mboss/bars_hide',
       'scoreboard players set #mbLn mb 0',
       '# Every helper entity dies on reload; a surviving body rebuilds its own (module reload hook).',
       'kill @e[tag=rlk_mb_aux]',
       'execute as @e[tag=rlk_mb_body] at @s run function rlk:mboss/reload',
       '# The arena is built once the dungeon area is set up (room/setup) and its chunks are loaded.',
       f'execute if data storage rlk:room {{ready:1b}} in minecraft:overworld if loaded {CX} {CY} {CZ} run function rlk:mboss/arena/ensure']))

w('reload', '''
# @s = surviving body after /reload (objectives and the registry are fresh, aux entities are gone).
scoreboard players set #mbLive mb 1
execute if entity @s[tag=rlk_mb_dying] run return run function rlk:mboss/death_finish
execute in minecraft:overworld run summon minecraft:marker @CX@ @CY@ @CZ@ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_arena"],Rotation:[180.0f,0.0f]}
scoreboard players set #mbPause mb 0
scoreboard players set #mbNoLeash mb 0
execute unless score #mbId mb matches 1.. run return 0
function rlk:mboss/d/reload
''')

w('uninstall', '''
# From rlk:uninstall: remove everything the mid-boss framework created (arena blocks stay); every module's
# uninstall hook first (their own objectives and leftovers).
function rlk:mboss/cleanup
function rlk:mboss/d/uninstall
# low gravity (mboss/lowg_on): the modifiers off every player and every entity still tagged
execute as @a run function rlk:mboss/lowg_rem
execute as @e[tag=rlk_lowg] run function rlk:mboss/lowg_rem
kill @e[tag=rlk_mb_body]
kill @e[tag=rlk_mb_aux]
bossbar remove rlk:mboss
bossbar remove rlk:mboss_state
bossbar remove rlk:mboss_sub
execute in minecraft:overworld run forceload remove @FL@
data remove storage rlk:mboss reg
data remove storage rlk:mboss byid
data remove storage rlk:mboss met
''' + '\n'.join(f'scoreboard objectives remove {o}' for o in OBJECTIVES))

w('opts_reset', '''
# One-shot options of the next hz/pj/pull call, back to their defaults (see README 중간보스).
scoreboard players set #hzAct mb 1
scoreboard players set #hzEl mb -1
scoreboard players set #hzKB mb 3
scoreboard players set #hzKBDir mb -1
scoreboard players set #hzY0 mb -5
scoreboard players set #hzY1 mb 35
scoreboard players set #hzR0 mb 0
scoreboard players set #hzBack mb 0
scoreboard players set #hzSfx mb 1
scoreboard players set #hzVis mb 0
scoreboard players set #hzCol mb -1
scoreboard players set #hzLinger mb 8
scoreboard players set #hzQuiet mb 0
scoreboard players set #hzNoDodge mb 0
scoreboard players set #hzRearm mb 0
scoreboard players set #pjEl mb -1
scoreboard players set #pjKB mb 2
scoreboard players set #pjRet mb 0
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 0
scoreboard players set #pjGrp mb 0
scoreboard players set #hzGrp mb 0
scoreboard players set #pullFace mb 1
scoreboard players set #auxHp mb 100
scoreboard players set #auxHpPct mb 0
scoreboard players set #auxRes mb 0
''')

# =============================================================================================
# Roll
w('roll', '''
# Picks rlk:mboss cur (copy of a reg[] entry) and #mbId. Order: #mbForce (tests) > weighted roll over entries
# with w >= 1 inside their chapter range and not met this run > the same allowing met ones > any w >= 1 entry
# (chapter ignored) > reg[0]. Entries with w 0 (test bosses) are only reachable through #mbForce or that last step.
data remove storage rlk:mboss cur
scoreboard players set #mbId mb 0
execute if score #mbForce mb matches 1.. run function rlk:mboss/roll_force
execute if data storage rlk:mboss cur run return run function rlk:mboss/roll_done
scoreboard players set #mbUseMet mb 1
scoreboard players set #mbUseCh mb 1
function rlk:mboss/roll_pass
execute unless data storage rlk:mboss cand[0] run scoreboard players set #mbUseMet mb 0
execute unless data storage rlk:mboss cand[0] run function rlk:mboss/roll_pass
execute unless data storage rlk:mboss cand[0] run scoreboard players set #mbUseCh mb 0
execute unless data storage rlk:mboss cand[0] run function rlk:mboss/roll_pass
execute if data storage rlk:mboss cand[0] run function rlk:mboss/roll_pick
execute unless data storage rlk:mboss cur run data modify storage rlk:mboss cur set from storage rlk:mboss reg[0]
function rlk:mboss/roll_done
''')
w('roll_done', '''
execute store result score #mbId mb run data get storage rlk:mboss cur.n
data remove storage rlk:mboss cand
data remove storage rlk:mboss wq
''')
w('roll_force', '''
data modify storage rlk:mboss wq set from storage rlk:mboss reg
function rlk:mboss/roll_force_loop
''')
w('roll_force_loop', '''
execute unless data storage rlk:mboss wq[0] run return 0
execute store result score #v mb run data get storage rlk:mboss wq[0].n
execute if score #v mb = #mbForce mb run return run data modify storage rlk:mboss cur set from storage rlk:mboss wq[0]
data remove storage rlk:mboss wq[0]
function rlk:mboss/roll_force_loop
''')
w('roll_pass', '''
data modify storage rlk:mboss cand set value []
scoreboard players set #wsum mb 0
data modify storage rlk:mboss wq set from storage rlk:mboss reg
function rlk:mboss/roll_loop
''')
w('roll_loop', '''
execute unless data storage rlk:mboss wq[0] run return 0
scoreboard players set #ok mb 1
execute store result score #v mb run data get storage rlk:mboss wq[0].w
execute if score #v mb matches ..0 run scoreboard players set #ok mb 0
execute store result score #v mb run data get storage rlk:mboss wq[0].minCh
execute if score #mbUseCh mb matches 1 if score #chapter room < #v mb run scoreboard players set #ok mb 0
execute store result score #v mb run data get storage rlk:mboss wq[0].maxCh
execute if score #mbUseCh mb matches 1 if score #chapter room > #v mb run scoreboard players set #ok mb 0
execute if score #ok mb matches 1 if score #mbUseMet mb matches 1 run function rlk:mboss/roll_met with storage rlk:mboss wq[0]
execute if score #ok mb matches 1 run data modify storage rlk:mboss cand append from storage rlk:mboss wq[0]
execute if score #ok mb matches 1 store result score #v mb run data get storage rlk:mboss wq[0].w
execute if score #ok mb matches 1 run scoreboard players operation #wsum mb += #v mb
data remove storage rlk:mboss wq[0]
function rlk:mboss/roll_loop
''')
w('roll_met', '''
$execute if data storage rlk:mboss {met:["$(id)"]} run scoreboard players set #ok mb 0
''')
w('roll_pick', '''
execute store result score #r mb run random value 0..9999
scoreboard players operation #r mb %= #wsum mb
function rlk:mboss/roll_pick_loop
''')
w('roll_pick_loop', '''
execute unless data storage rlk:mboss cand[0] run return 0
execute store result score #v mb run data get storage rlk:mboss cand[0].w
execute if score #r mb < #v mb run return run data modify storage rlk:mboss cur set from storage rlk:mboss cand[0]
scoreboard players operation #r mb -= #v mb
data remove storage rlk:mboss cand[0]
function rlk:mboss/roll_pick_loop
''')

# =============================================================================================
# Gate (zone kind 15 object, oact 14) and start
w('gate', T.join(['''
# The 중간보스 gate object was clicked (@s = its rlk_obj marker, at @s; room/obj/click already refuses
# clicks during combat). Starts the zone fight; room/mob_wave calls mboss/start 1.5 s later.
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @a[tag=player] ''', gray("난이도가 '평화로움'이면 중간보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 누르세요.") + ''']
execute unless entity @e[tag=rlk_zone,scores={zkind=15,zst=3},limit=1] run return 0
execute if entity @e[tag=rlk_mb_body,limit=1] run return 0
execute unless data storage rlk:mboss cur run function rlk:mboss/roll
execute unless data storage rlk:mboss cur run return 0
function rlk:room/obj/kill_group
execute as @e[tag=rlk_zone,scores={zkind=15,zst=3},sort=nearest,limit=1] at @s run function rlk:room/combat_start
scoreboard players set #spawnT room 30
title @a[tag=player] times 6 46 14
title @a[tag=player] subtitle {nbt:"cur.sub",storage:"rlk:mboss",color:"#E8E2D0"}
title @a[tag=player] title {nbt:"cur.title",storage:"rlk:mboss",interpret:true}
scoreboard players set @a[tag=player] vBig 66
scoreboard players set @a[tag=player] ttlT 66
execute as @a[tag=player] at @s run playsound minecraft:block.bell.resonate hostile @s ~ ~ ~ 0.7 0.6
execute as @a[tag=player] at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.7
''']))

w('start', '''
# @s = the 중간보스 zone marker, at @s (from room/mob_wave, #combat = its zid). Builds the fight in the
# arena and teleports the player. A failed spawn retries 10 ticks later (#spawnT), 3 failures cancel
# the fight without reward. The body holds rlk_zmob from tick 0, so the zone cannot clear early.
execute in minecraft:overworld unless loaded @CX@ @CY@ @CZ@ run return run function rlk:mboss/start_unloaded
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run scoreboard players set #spawnT room 10
execute unless data storage rlk:mboss cur run function rlk:mboss/roll
execute unless data storage rlk:mboss cur run return run function rlk:mboss/start_fail
scoreboard players set #mbLd mb 0
# From here on fight entities may exist: rlk:tick runs mboss/main (cleared when the body is gone).
scoreboard players set #mbLive mb 1
function rlk:mboss/cleanup_aux
function rlk:mboss/fight_vars
execute in minecraft:overworld run function rlk:mboss/arena/ensure
execute in minecraft:overworld run summon minecraft:marker @CX@ @CY@ @CZ@ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_arena"],Rotation:[180.0f,0.0f]}
execute in minecraft:overworld as @e[tag=rlk_mb_arena,limit=1] at @s rotated as @s run function rlk:mboss/d/spawn
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run function rlk:mboss/start_fail
scoreboard players set #mbFail mb 0
function rlk:mboss/ret_save
scoreboard players operation #mbLv mb = @e[tag=rlk_mb_body,limit=1] mlv
data modify storage rlk:mboss met append from storage rlk:mboss cur.id
scoreboard players set #mbOn mb 1
scoreboard players set #mbSt mb 0
scoreboard players set #mbT mb 0
execute as @a[tag=player,limit=1] run function rlk:mboss/tp_in
function rlk:mboss/bars_show
''')
w('start_unloaded', '''
# @s = zone marker. The arena chunks are not loaded (their forceload was released, e.g. room/remove then
# room/setup without a /reload): forceload them again and retry every 10 ticks; the 7th miss in a row (3 s) cancels
# the fight without reward like a failed spawn (the gate comes back).
execute in minecraft:overworld run forceload add @FL@
scoreboard players add #mbLd mb 1
execute if score #mbLd mb matches ..6 run return run scoreboard players set #spawnT room 10
function rlk:mboss/start_cancel
''')
w('start_fail', '''
# Spawn failed (no registry entry, no body after the spawn hook): retry twice, then cancel without reward.
function rlk:mboss/cleanup_aux
scoreboard players add #mbFail mb 1
execute if score #mbFail mb matches ..2 run return run scoreboard players set #spawnT room 10
function rlk:mboss/start_cancel
''')
w('start_cancel', T.join(['''
# @s = zone marker: give up this attempt (no reward); room/combat_clear -> mboss/won brings the gate back.
scoreboard players set #mbFail mb 0
scoreboard players set #mbLd mb 0
scoreboard players set #mbKilled mb 0
tellraw @a[tag=player] ''', gray('중간보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)') + ''']
function rlk:room/combat_clear
''']))
w('fight_vars', '''
# Per-fight constants from rlk:mboss cur (read by hurt, gold_drop, the shells and the libraries).
scoreboard players set #mbKilled mb 0
scoreboard players set #mbPause mb 0
scoreboard players set #mbNoLeash mb 0
execute store result score #mbId mb run data get storage rlk:mboss cur.n
execute store result score #mbDmgMul mb run data get storage rlk:mboss cur.dmgMul
execute store result score #mbGoldMul mb run data get storage rlk:mboss cur.goldMul
execute store result score #mbSap mb run data get storage rlk:mboss cur.sap
execute store result score #mbIntro mb run data get storage rlk:mboss cur.intro
execute store result score #mbDeath mb run data get storage rlk:mboss cur.death
execute store result score #mbEl mb run data get storage rlk:mboss cur.el
execute store result score #mbAtk mb run data get storage rlk:mboss cur.atk
data modify storage rlk:mboss sub set value []
data modify storage rlk:mboss extra set value []
data modify storage rlk:mboss aura set value []
scoreboard players set #mbAuraK mb -1
function rlk:mboss/player_reset
function rlk:mboss/opts_reset
''')
w('player_reset', '''
# Player-side fight modifiers back to neutral (fight start, cleanup_fight): healing received 100 %, no crit
# change, no pending heal events, no low gravity. The player's crit chance is recomputed every 2 t (items/stat_light).
scoreboard players set #mbHealPct mb 100
scoreboard players set #mbCritAdd mb 0
scoreboard players set #mbHealEv mb 0
# low gravity off (rlk:tick removes the modifiers on the next tick: mboss/lowg_off)
scoreboard players set #mbLowG mb 0
''')
w('player_heal', '''
# From items/hook/on_heal, its first line (@s = player, #heal tmp >= 1), only while a fight is live (#mbLive 1).
# Every heal attempt counts as one heal event (#mbHealEv mb +1; the running module reads and clears it in its
# tick, e.g. the butterfly's 달빛 고치 cure), and the healing received is x #mbHealPct % (set by the module,
# 100 = unchanged), at least 1. It runs before the character hooks (Clorinde's Night Vigil turns heals into
# Bond of Life), so a heal that a character converts still counts and is reduced first.
scoreboard players add #mbHealEv mb 1
execute if score #mbHealPct mb matches 100 run return 0
scoreboard players operation #heal tmp *= #mbHealPct mb
scoreboard players operation #heal tmp /= #c100 mb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
''')

w('lowg_on', '''
# From rlk:tick while #mbLowG mb is 1 (@s = a player; before view/tick, so this tick's jump already uses it): low
# gravity on the player and on the shoulder-view avatar (view/move reads the avatar's own jump_strength):
# gravity x0.5, jump strength x1.19 (apex about 3 b, 25 t airtime), safe fall distance +4, all modifier
# rlk:mb_lowg. Multiplicative on purpose: the shoulder-view camera player has gravity base 0 and stays put.
# Re-added every tick (an existing modifier is not changed), so a re-created avatar gets it at once. The swing
# hold (jump x0, player/swing/tick) and every other x0 jump lock still win. Tag rlk_lowg marks who carries it.
function rlk:mboss/lowg_add
execute as @e[type=minecraft:mannequin,tag=rlk_av] run function rlk:mboss/lowg_add
''')
w('lowg_add', '''
attribute @s minecraft:gravity modifier add rlk:mb_lowg -0.5 add_multiplied_base
attribute @s minecraft:jump_strength modifier add rlk:mb_lowg 0.19 add_multiplied_base
attribute @s minecraft:safe_fall_distance modifier add rlk:mb_lowg 4 add_value
tag @s add rlk_lowg
''')
w('lowg_off', '''
# From rlk:tick while #mbLowG mb is not 1 and something still carries low gravity (any player or avatar tagged
# rlk_lowg: a field that ended, broke or paused, a fight that is over, a relog or crash mid-field, a view switch).
execute as @e[tag=rlk_lowg] run function rlk:mboss/lowg_rem
''')
w('lowg_rem', '''
attribute @s minecraft:gravity modifier remove rlk:mb_lowg
attribute @s minecraft:jump_strength modifier remove rlk:mb_lowg
attribute @s minecraft:safe_fall_distance modifier remove rlk:mb_lowg
tag @s remove rlk_lowg
''')

w('body', '''
# The common hitbox body (call from the module's spawn hook, at the spawn point; context yaw = facing).
# Invisible NoAI husk: rlk_zmob holds the zone fight, boss gives stun/freeze/knockback immunity,
# miniboss switches the boss economy to #mbGoldMul / #mbSap. HP/XP/level come from rlk:mboss cur.
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_mboss","boss","miniboss","rlk_mb_body","rlk_mb_inv","rlk_mb_bnew"],PersistenceRequired:1b,NoAI:1b,NoGravity:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_mb_bnew,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_mb_bnew,limit=1] at @s run function rlk:mboss/body_setup
tag @e[tag=rlk_mb_bnew] remove rlk_mb_bnew
''')
w('body_setup', '''
function rlk:mboss/body_tag with storage rlk:mboss cur
function rlk:room/mob_init
execute store result score #t mb run data get storage rlk:mboss cur.lvAdd
execute unless score #t mb matches 0 run scoreboard players operation @s mlv += #t mb
execute unless score #t mb matches 0 run function rlk:mob/level_apply
attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
execute store result storage rlk:mboss a.s double 0.01 run data get storage rlk:mboss cur.scale 100
function rlk:mboss/body_scale with storage rlk:mboss a
scoreboard players set @s mres 0
''')
w('body_tag', '$tag @s add rlk_mb_$(id)')
w('body_scale', '$attribute @s minecraft:scale base set $(s)')
w('base_stats', '''
# From room/mob_init (rlk_m_mboss), with storage rlk:mboss cur: level-1 HP and kill XP.
$scoreboard players set #mhp tmp $(hp)
scoreboard players set #mad tmp 0
$scoreboard players set @s xpDrop $(xp)
''')
w('shield_size', '''
# From mob/shield_ensure on creation (with storage rlk:mboss cur.hit): click-shield size of the body.
$data merge entity @e[tag=rlk_mshield_new,limit=1] {width:$(w)f,height:$(h)f}
''')

w('ret_save', '''
# Return point = rlk_safe (last solid footing in the dungeon), else the body; facing from the player.
execute store result storage rlk:mboss ret.x double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result storage rlk:mboss ret.y double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[1] 100
execute store result storage rlk:mboss ret.z double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
execute if entity @e[tag=rlk_safe,limit=1] store result storage rlk:mboss ret.x double 0.01 run data get entity @e[tag=rlk_safe,limit=1] Pos[0] 100
execute if entity @e[tag=rlk_safe,limit=1] store result storage rlk:mboss ret.y double 0.01 run data get entity @e[tag=rlk_safe,limit=1] Pos[1] 100
execute if entity @e[tag=rlk_safe,limit=1] store result storage rlk:mboss ret.z double 0.01 run data get entity @e[tag=rlk_safe,limit=1] Pos[2] 100
execute store result storage rlk:mboss ret.yaw float 0.01 run data get entity @a[tag=player,limit=1] Rotation[0] 100
execute store result storage rlk:mboss ret.pitch float 0.01 run data get entity @a[tag=player,limit=1] Rotation[1] 100
data modify storage rlk:mboss ret.dim set value "minecraft:overworld"
data modify storage rlk:mboss ret.dim set from entity @a[tag=player,limit=1] Dimension
''')
w('ret_here', '''
# Fallback return point: this zone marker (@s).
execute store result storage rlk:mboss ret.x double 0.01 run data get entity @s Pos[0] 100
execute store result storage rlk:mboss ret.y double 0.01 run data get entity @s Pos[1] 100
execute store result storage rlk:mboss ret.z double 0.01 run data get entity @s Pos[2] 100
data modify storage rlk:mboss ret.yaw set value 0.0f
data modify storage rlk:mboss ret.pitch set value 0.0f
data modify storage rlk:mboss ret.dim set value "minecraft:overworld"
''')
w('tp_in', '''
# @s = player. Into the arena: short blindness hides the jump; avatar and fall marker follow.
effect give @s minecraft:blindness 1 0 true
function rlk:mboss/tp_start with storage rlk:mboss cur.start
function rlk:view/sync
function rlk:mboss/safe_start with storage rlk:mboss cur.start
execute at @s run playsound minecraft:entity.enderman.teleport hostile @s ~ ~ ~ 0.6 0.6
execute at @s run playsound minecraft:block.beacon.activate hostile @s ~ ~ ~ 0.6 0.7
''')
w('tp_start', '$execute in minecraft:overworld run tp @s $(x) $(y) $(z) $(yaw) $(pitch)')
w('safe_start', '$execute in minecraft:overworld run tp @e[tag=rlk_safe,limit=1] $(x) $(y) $(z)')
w('tp_out', '''
# @s = player. Back to the dungeon return point; the fall marker rlk_safe moves too, otherwise a pit
# right after the return would rescue the player into the arena.
function rlk:mboss/ret_go with storage rlk:mboss ret
function rlk:view/sync
function rlk:mboss/ret_safe with storage rlk:mboss ret
effect clear @s minecraft:blindness
''')
w('ret_go', '$execute in $(dim) run tp @s $(x) $(y) $(z) $(yaw) $(pitch)')
w('ret_safe', '$execute in $(dim) run tp @e[tag=rlk_safe,limit=1] $(x) $(y) $(z)')

# =============================================================================================
# Won / cancelled / cleanup
w('won', '''
# @s = the 중간보스 zone marker, at @s (from room/combat_clear: the body is gone, #combat is 0).
# #mbKilled 1 = killed through combat/apply (reward); anything else (/kill, failed spawn, a reload that
# lost the body) cancels: no reward, the gate comes back so the fight can be retried.
scoreboard players operation #mbWas mb = #mbOn mb
execute in minecraft:overworld positioned @BOX@ as @e[tag=rlk_gold,@BOXD@] run function rlk:combat/gold_absorb
function rlk:mboss/cleanup_fight
execute unless data storage rlk:mboss ret.x run function rlk:mboss/ret_here
execute if score #mbWas mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/tp_out
scoreboard players set #mbRegate mb 0
execute if score #mbKilled mb matches 1 run function rlk:mboss/reward
execute unless score #mbKilled mb matches 1 run function rlk:mboss/cancelled
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
execute if score #mbRegate mb matches 1 run function rlk:room/obj/k_mboss
''')
w('reward', '''
# @s = zone marker, at @s (the 중간보스 zone centre, where the gate stood); the player is back in the dungeon.
# No selection screen and no fanfare here: cur.picks item boxes fall onto the floor (mboss/box/*). Each box is
# a room object (oact 15, room/obj/k_mbox); its first click = one chapter-rarity, items-only pick (room/obj/do_mbox),
# and the box stays (opened) until that pick is used (lvup/act/resolve -> box/spend).
title @a[tag=player] times 8 50 14
title @a[tag=player] subtitle [{text:"아이템 상자 ",color:"#FFE08A"},{nbt:"cur.picks",storage:"rlk:mboss",color:"#FFE08A"},{text:"개 · 챕터 등급",color:"#FFE08A"}]
title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]
scoreboard players set @a[tag=player] vBig 72
scoreboard players set @a[tag=player] ttlT 72
execute store result score #mbPk mb run data get storage rlk:mboss cur.picks
execute if score #mbPk mb matches 1.. run function rlk:mboss/box/drop_all
''')

# ---------------------------------------------------------------------------------------------
# Reward item boxes. cur.picks vanilla chests (item_display) fall BOX_H blocks onto the zone centre in
# BOX_F ticks (stepped tp + teleport_duration 1, light acceleration, an ease-out quarter turn that lands
# square), one after the other, BOX_GAP apart in a row across the line from the zone centre to the player.
# On landing each becomes the clickable room object room/obj/k_mbox (hand-written, oact 15); the click is
# room/obj/do_mbox. Everything carries rlk_room, so room/clear (map change, run end), room/wipe and
# uninstall remove the boxes like any other room object. room/tick runs box/all while #mbBoxOn mb is 1.
# Opened boxes: the first click grants the box's pick and opens it (box/open: rlk_mb_boxopen on its whole group,
# gold outline, label "(열림)", oarg = open age); backing out of the screen leaves it there and a later click only
# reopens the screen. When a mid-boss pick is used (lvup/act/resolve on an mbSet), box/spend removes the oldest
# opened box (box/gone: the open sounds at the player, who is in the selection screen; the particles at the box;
# then its group). No global counter: the state lives on the box entities, so
# a map change (room/clear) leaves nothing behind and an unused pick simply stays pending (Shift+F).
BOX_S = 1.1            # display scale: the chest item model is 14/16 wide and tall, centred on the entity
BOX_REST = BOX_S / 2   # display centre above the floor at rest (chest bottom on the floor)
BOX_GAP = 1.5          # centre to centre
BOX_H = 6.0            # drop height (blocks)
BOX_F = 14             # fall ticks
BOX_SPIN = 90          # yaw turned while falling (degrees, ease-out)
BOX_STAGGER = 4        # ticks between consecutive boxes
BOX_NMAX = max([2] + [int(b.get('picks', 2)) for b in BOSSES])
BOX_GOLD = '{color:[1.0f,0.84f,0.36f],scale:%sf}'
BOX_SQ = (1.12, 0.82)  # landing squash (xz, y) relative to BOX_S
BOX_GLOW = 0xFFD24A    # outline of an opened box (the label's gold)
# Label of an opened box: three short lines like the closed one (room/obj/k_mbox), so two labels 1.5 b apart
# never overlap (a one-line "아이템 상자 (열림)" would be about 1.8 b wide at the label's 0.8 scale).
BOX_OPEN_TEXT = ('[{text:"아이템 상자",color:"#FFD24A",bold:true},{text:"\\n(열림)",color:"#FFE08A",bold:true},'
                 '{text:"\\n다시 눌러 선택",color:"#D0D0D0",bold:false}]')


def exact_steps(total, weights, nd=4):
    # Per-tick steps rounded to nd decimals whose sum is exactly `total`.
    steps, acc = [], 0.0
    for i, wt in enumerate(weights):
        v = round(total - acc, nd) if i == len(weights) - 1 else round(total * wt / sum(weights), nd)
        steps.append(v)
        acc = round(acc + v, nd)
    return steps


BOX_FALL = exact_steps(BOX_H, [0.25 / BOX_F + 0.75 * (2 * t - 1) / BOX_F ** 2 for t in range(1, BOX_F + 1)])
BOX_TURN = exact_steps(BOX_SPIN, [2 * BOX_F - 2 * t + 1 for t in range(1, BOX_F + 1)])
_bs = L.num(BOX_S)
_row = []
for n in range(1, BOX_NMAX + 1):
    for i in range(n):
        off = (i - (n - 1) / 2) * BOX_GAP
        at = f' positioned ^{L.num(off)} ^ ^' if abs(off) > 1e-9 else ''
        _row.append(f'execute if score #mbPk mb matches {n}{at} run function rlk:mboss/box/drop')
w('box/drop_all', '\n'.join([
    '# From mboss/reward (@s = zone marker, at @s; #mbPk mb = cur.picks >= 1). The row stands across the line from',
    '# the zone centre to the player, its yaw snapped to the room axes, so the player sees the boxes side by side.',
    'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_boxq"]}',
    'execute as @e[type=minecraft:marker,tag=rlk_mb_boxq,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0',
    'execute store result score #mbBoxY mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_boxq,limit=1] Rotation[0]',
    'kill @e[type=minecraft:marker,tag=rlk_mb_boxq]',
    '# quarter = (yaw + 225) / 90 mod 4: 0 player to the north (yaw 180), 1 east (-90), 2 south (0), 3 west (90)',
    'scoreboard players add #mbBoxY mb 225',
    'scoreboard players set #mbBoxQ mb 90',
    'scoreboard players operation #mbBoxY mb /= #mbBoxQ mb',
    'scoreboard players operation #mbBoxY mb %= #c4 mb',
    f'execute if score #mbPk mb matches {BOX_NMAX + 1}.. run scoreboard players set #mbPk mb {BOX_NMAX}',
    'scoreboard players set #mbBoxW mb 0',
    'execute if score #mbBoxY mb matches 0 rotated 180 0 run function rlk:mboss/box/row',
    'execute if score #mbBoxY mb matches 1 rotated -90 0 run function rlk:mboss/box/row',
    'execute if score #mbBoxY mb matches 2 rotated 0 0 run function rlk:mboss/box/row',
    'execute if score #mbBoxY mb matches 3 rotated 90 0 run function rlk:mboss/box/row',
    'scoreboard players set #mbBoxOn mb 1',
    f'playsound minecraft:block.amethyst_block.chime block @a[tag=player] ~ ~{L.num(BOX_H)} ~ 1 1.3',
    f'playsound minecraft:entity.firework_rocket.twinkle_far block @a[tag=player] ~ ~{L.num(BOX_H)} ~ 0.5 1.4',
]))
w('box/row', '\n'.join([
    '# @s = zone marker, positioned at the zone centre, rotated toward the player (snapped): one set of lines per',
    f'# row size (1..{BOX_NMAX}), boxes {L.num(BOX_GAP)} b apart, dropped from the player\'s left to right.',
] + _row))
w('box/drop', f'''
# @s = zone marker, positioned at this box's floor spot, rotated toward the player. item_display turns item
# models 180 degrees, so yaw = toward the player + 180 puts the chest's latch toward the player; {BOX_SPIN} more
# are turned back while falling. Boxes after the first wait {BOX_STAGGER} ticks each (mbT starts at 0, -{BOX_STAGGER}, ...).
summon minecraft:item_display ~ ~{L.num(BOX_REST + BOX_H)} ~ {{Tags:["rlk_room","rlk_mb_box","rlk_mb_boxfall","rlk_mb_boxnew"],teleport_duration:1,brightness:{{sky:15,block:15}},item:{{id:"minecraft:chest",count:1}},transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[{_bs}f,{_bs}f,{_bs}f]}}}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_boxnew] run tp @s ~ ~{L.num(BOX_REST + BOX_H)} ~ ~{180 + BOX_SPIN} 0
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_boxnew] mbT 0
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_boxnew] mbT -= #mbBoxW mb
tag @e[type=minecraft:item_display,tag=rlk_mb_boxnew] remove rlk_mb_boxnew
scoreboard players add #mbBoxW mb {BOX_STAGGER}
''')
w('box/all', '''
# From room/tick while #mbBoxOn mb is 1 (drop_all sets it, every box alive keeps it): fall and idle shimmer.
scoreboard players set #mbBoxOn mb 0
execute as @e[type=minecraft:item_display,tag=rlk_mb_box] at @s run function rlk:mboss/box/tick
''')
w('box/tick', '''
# @s = box display, at @s. mbT = the box's own clock.
scoreboard players set #mbBoxOn mb 1
scoreboard players add @s mbT 1
execute if entity @s[tag=rlk_mb_boxfall] run return run function rlk:mboss/box/fall
execute if score @s mbT matches 10.. run function rlk:mboss/box/shimmer
''')
_fall = ['# @s = falling box, at @s. mbT <= 0: waiting for its turn up in the air (sparkles).',
         'execute if score @s mbT matches ..0 run return run particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.01 1']
for t, (dy, dr) in enumerate(zip(BOX_FALL, BOX_TURN), 1):
    _fall.append(f'execute if score @s mbT matches {t} run tp @s ~ ~-{L.num(dy)} ~ ~-{L.num(dr)} ~')
_fall += [
    f'execute if score @s mbT matches 1..{BOX_F - 1} at @s run function rlk:mboss/box/trail',
    f'execute if score @s mbT matches {BOX_F} at @s run function rlk:mboss/box/land',
    f'execute if score @s mbT matches {BOX_F + 3} run data merge entity @s {{start_interpolation:0,interpolation_duration:4,'
    f'transformation:{{translation:[0f,0f,0f],scale:[{_bs}f,{_bs}f,{_bs}f]}}}}',
    f'execute if score @s mbT matches {BOX_F + 6}.. run function rlk:mboss/box/settle',
]
w('box/fall', '\n'.join(_fall))
w('box/trail', f'''
# Gold and white sparkles along the fall.
particle minecraft:dust{BOX_GOLD % '1.3'} ~ ~ ~ 0.25 0.25 0.25 0 3
particle minecraft:dust{{color:[1.0f,0.97f,0.86f],scale:0.8f}} ~ ~0.35 ~ 0.15 0.3 0.15 0 2
particle minecraft:end_rod ~ ~0.45 ~ 0.12 0.2 0.12 0.01 1
''')
_sx, _sy = BOX_S * BOX_SQ[0], BOX_S * BOX_SQ[1]
w('box/land', f'''
# @s = box display at rest, at @s (centre {L.num(BOX_REST)} b above the floor): thud, dust puff and gold burst, a short
# squash (bottom kept on the floor; it starts 1 t later, when the client has finished the last interpolated fall
# step, and box/fall springs it back at {BOX_F + 3}), then the clickable room object around it (the display joins its group).
particle minecraft:poof ~ ~-{L.num(BOX_REST - 0.05)} ~ 0.45 0.02 0.45 0.03 12
particle minecraft:dust{BOX_GOLD % '1.6'} ~ ~-{L.num(BOX_REST - 0.1)} ~ 0.6 0.03 0.6 0 16
particle minecraft:end_rod ~ ~0.1 ~ 0.1 0.1 0.1 0.08 8
playsound minecraft:block.chest.close block @a[tag=player] ~ ~ ~ 0.8 0.7
playsound minecraft:block.wood.fall block @a[tag=player] ~ ~ ~ 1 0.7
playsound minecraft:block.anvil.land block @a[tag=player] ~ ~ ~ 0.15 1.6
data merge entity @s {{start_interpolation:1,interpolation_duration:2,transformation:{{translation:[0f,-{L.num(0.5 * (BOX_S - _sy), 3)}f,0f],scale:[{L.num(_sx, 3)}f,{L.num(_sy, 3)}f,{L.num(_sx, 3)}f]}}}}
tag @s add rlk_new
execute positioned ~ ~-{L.num(BOX_REST)} ~ run function rlk:room/obj/k_mbox
''')
w('box/settle', '''
tag @s remove rlk_mb_boxfall
scoreboard players set @s mbT 0
''')
w('box/shimmer', f'''
# Resting box: a soft gold shimmer every 10 ticks.
scoreboard players set @s mbT 0
particle minecraft:dust{BOX_GOLD % '0.9'} ~ ~0.15 ~ 0.35 0.3 0.35 0 2
particle minecraft:end_rod ~ ~{L.num(BOX_REST)} ~ 0.25 0.1 0.25 0.004 1
''')
w('box/open', f'''
# From room/obj/do_mbox on the FIRST click of a box (@s = its object marker, at @s), after its pick was granted.
# The box stays where it is until a mid-boss pick is used (box/spend): backing out of the screen with Shift leaves
# it, and a later click only reopens the screen. oarg = open age (closed 0; the newest opened box 1, older ones
# count up), so box/spend takes the oldest. Every entity of its group gets rlk_mb_boxopen; the chest gets a gold
# outline, the label "(열림)". No global counter: room/clear and uninstall remove the tags with the entities.
scoreboard players add @e[type=minecraft:marker,tag=rlk_obj,tag=rlk_mb_boxopen] oarg 1
scoreboard players set @s oarg 1
scoreboard players operation #mbBoxG mb = @s ogid
execute as @e[tag=rlk_room] if score @s ogid = #mbBoxG mb run tag @s add rlk_mb_boxopen
execute as @e[type=minecraft:item_display,tag=rlk_mb_box,tag=rlk_mb_boxopen] if score @s ogid = #mbBoxG mb run data merge entity @s {{Glowing:1b,glow_color_override:{BOX_GLOW}}}
execute as @e[type=minecraft:text_display,tag=rlk_olbl,tag=rlk_mb_boxopen] if score @s ogid = #mbBoxG mb run data modify entity @s text set value {BOX_OPEN_TEXT}
''')
w('box/spend', '''
# From lvup/act/resolve (@s = player) when a mid-boss pick is used: an mbSet was chosen (or skipped) while pkMb >= 1,
# just before pkMb -1. Exactly one opened box goes: the oldest (highest oarg; box/gone). None opened (the room with
# the opened box was left and its pick stayed pending for Shift+F): nothing. Closed boxes are never removed here.
scoreboard players set #mbBoxA mb 0
execute as @e[type=minecraft:marker,tag=rlk_obj,tag=rlk_mb_boxopen] run scoreboard players operation #mbBoxA mb > @s oarg
execute as @e[type=minecraft:marker,tag=rlk_obj,tag=rlk_mb_boxopen] if score @s oarg = #mbBoxA mb at @s run return run function rlk:mboss/box/gone
''')
w('box/gone', f'''
# @s = an opened box's object marker, at @s (box centre): the open fx (chest opening, chime, gold burst, poof), then
# the whole group (marker, chest display, label, hint) via room/obj/kill_group. From box/spend, and from
# room/obj/do_mbox for an opened box whose pick no longer exists (guard only: pkMb < 1 with an opened box).
# The two sounds play at the player: a pick is used in the selection screen (overworld 104 195 4), at least 40 b
# from any box in the room (-64..63), where a sound at the box (heard up to 16 b) would never reach the player.
execute at @a[tag=player,limit=1] run playsound minecraft:block.chest.open block @a[tag=player] ~ ~ ~ 0.9 1
execute at @a[tag=player,limit=1] run playsound minecraft:block.amethyst_block.chime block @a[tag=player] ~ ~ ~ 1 1.2
particle minecraft:dust{BOX_GOLD % '1.4'} ~ ~ ~ 0.35 0.35 0.35 0 18
particle minecraft:end_rod ~ ~0.2 ~ 0.15 0.15 0.15 0.1 12
particle minecraft:poof ~ ~-{L.num(BOX_REST - 0.1)} ~ 0.35 0.25 0.35 0.02 12
function rlk:room/obj/kill_group
''')
w('cancelled', T.join(['''
tellraw @a[tag=player] ''', gray('중간보스 전투가 취소되었습니다. (보상 없음) 문 오브젝트를 다시 누르면 재도전합니다.') + ''']
scoreboard players set #mbRegate mb 1
''']))
w('forget', '''
data remove storage rlk:mboss cur
data remove storage rlk:mboss ret
scoreboard players set #mbId mb 0
scoreboard players set #mbKilled mb 0
''')
w('cleanup_aux', '''
# Every entity of the fight (body, rig, hazards, props, aux objects, arena marker).
kill @e[tag=rlk_mb_aux]
kill @e[tag=rlk_mb_body]
''')
w('cleanup_fight', '''
# End of a fight without forgetting cur/ret (won reads them afterwards).
execute if score #mbId mb matches 1.. run function rlk:mboss/d/cleanup
function rlk:mboss/cleanup_aux
function rlk:mboss/arena_sweep
function rlk:mboss/bars_hide
function rlk:mboss/line/clear
scoreboard players set #mbOn mb 0
scoreboard players set #mbSt mb 0
scoreboard players set #mbT mb 0
scoreboard players set #mbPause mb 0
scoreboard players set #mbFail mb 0
scoreboard players set #mbLd mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #mbLive mb 0
function rlk:mboss/player_reset
data modify storage rlk:mboss sub set value []
data modify storage rlk:mboss extra set value []
''')
w('cleanup', '''
# Idempotent full cleanup: room/clear (map change, run end, death), room/wipe, uninstall, test stop.
# Never teleports the player (callers that end a run move the player themselves).
function rlk:mboss/cleanup_fight
function rlk:mboss/forget
''')
w('arena_sweep', '''
# Loose entities in the arena box (room/clear only sweeps the dungeon square).
execute in minecraft:overworld positioned @BOX@ run kill @e[type=minecraft:arrow,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[type=minecraft:item,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[type=minecraft:experience_orb,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[tag=rlk_healorb,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[tag=rlk_gold,@BOXD@]
''')

# =============================================================================================
# World tick, pause, out of bounds, state shells, death
w('main', '''
# From rlk:tick, only while #mbLive mb is 1 (set by mboss/start and mboss/reload, cleared by cleanup_fight and
# here), so outside a fight the server never scans for mid-boss entities. No body any more (killed, /kill,
# lost): the fight's leftovers and the bars go, and the scans stop until the next mboss/start.
# Low gravity is a per-tick request: cleared here, set again by the running module's tick (#mbLowG mb 1), so a
# paused fight, a missing player or body, the intro, the death sequence and every exit path drop it at once.
scoreboard players set #mbLowG mb 0
execute if entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run return run function rlk:mboss/world
function rlk:mboss/cleanup_aux
function rlk:mboss/bars_hide
scoreboard players set #mbLive mb 0
''')
w('world', '''
# From mboss/main while a body exists. Pause (dead / revival / selection screen / no body entity / no tagged
# player) freezes AI, timers, hazards and projectiles; out-of-bounds puts the player back at the arrival spot.
# No tagged player (a disconnect, the tag gone) is a pause too, so the module's pause hook runs (its decals go and
# their redraw is queued for the resume) instead of the fight freezing silently.
# The libraries are scanned only while their activity flag is set (#mbMvOn #mbHzOn #mbPjOn #mbPlOn: set when
# one is created, kept by every live one in its tick, so the scan stops one tick after the last one ends).
execute unless entity @a[tag=player,limit=1] run return run function rlk:mboss/pause_tick
scoreboard players set #mbP mb 0
execute if entity @a[tag=player,scores={dead=1}] run scoreboard players set #mbP mb 1
execute if entity @a[tag=player,scores={rnDie=1..}] run scoreboard players set #mbP mb 1
execute if entity @a[tag=player,scores={pkMode=1..}] run scoreboard players set #mbP mb 1
execute unless entity @e[tag=rlk_body,limit=1] run scoreboard players set #mbP mb 1
execute if score #mbP mb matches 1 run return run function rlk:mboss/pause_tick
execute if score #mbPause mb matches 1 run function rlk:mboss/resume
execute if score #mbOn mb matches 1 unless entity @a[tag=player,scores={devMode=1}] as @e[tag=rlk_body,limit=1] at @s run function rlk:mboss/oob
execute if score #mbMvOn mb matches 1 run function rlk:mboss/mv/all
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/body_tick
execute if score #mbHzOn mb matches 1 run function rlk:mboss/hz/all
execute if score #mbPjOn mb matches 1 run function rlk:mboss/pj/all
execute if score #mbPlOn mb matches 1 run function rlk:mboss/pull/all
execute if score #mbSt mb matches 0..1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/bars
function rlk:mboss/line/tick
''')
w('mv/all', '''
scoreboard players set #mbMvOn mb 0
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/tick
''')
w('hz/all', '''
scoreboard players set #mbHzOn mb 0
# re-arm clock of #hzRearm hazards (advances only while hazards are scanned, so a paused fight freezes it too)
scoreboard players add #mbHzClk mb 1
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] at @s rotated as @s run function rlk:mboss/hz/tick
''')
w('pj/all', '''
scoreboard players set #mbPjOn mb 0
execute as @e[tag=rlk_mb_pj] at @s rotated as @s run function rlk:mboss/pj/tick
''')
w('pull/all', '''
scoreboard players set #mbPlOn mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_pullpt] at @s run function rlk:mboss/pull/tick
''')
w('pause_tick', '''
execute if score #mbPause mb matches 0 as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/d/pause
scoreboard players set #mbPause mb 1
# No boss bars on the death screen (the run, or the test, is lost).
execute if entity @a[tag=player,scores={dead=1}] run function rlk:mboss/bars_hide
''')
w('resume', '''
scoreboard players set #mbPause mb 0
execute as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/d/resume
''')
w('oob', T.join(['''
# @s = rlk_body (avatar or first-person player), at @s. Inside = between y 198 and 217 (wall 201..207,
# barrier cap above it; the volume box is taken at the body's own x/z) and within @OOB@ blocks of the axis.
execute if entity @s[y=198,dy=19] positioned @CX@ ~ @CZ@ if entity @s[distance=..@OOB@] run return 0
execute as @a[tag=player,limit=1] run function rlk:mboss/tp_start with storage rlk:mboss cur.start
execute as @a[tag=player,limit=1] run function rlk:view/sync
function rlk:mboss/safe_start with storage rlk:mboss cur.start
title @a[tag=player] actionbar ''', '{text:"경기장 밖으로 벗어나 처음 자리로 돌아왔습니다",color:"#FFB0A0",bold:false}]']))
w('body_tick', '''
# @s = body, at @s. #mbT = clock of the current state (0 intro, 1 fight, 2 dying).
data merge entity @s {Motion:[0d,0d,0d],Fire:-1s}
scoreboard players add #mbT mb 1
execute if score #mbSt mb matches 0 run return run function rlk:mboss/intro_shell
execute if score #mbSt mb matches 1 run return run function rlk:mboss/fight_tick
execute if score #mbSt mb matches 2 run function rlk:mboss/death_shell
''')
w('intro_shell', '''
# Untargetable intro (rlk_mb_inv). The module ends it with mboss/intro_end; cur.intro is the maximum.
function rlk:mboss/d/intro_tick
execute if score #mbSt mb matches 0 if score #mbT mb >= #mbIntro mb run function rlk:mboss/intro_end
''')
w('intro_end', '''
# Callable from anywhere (module intro hook, tests): the fight state starts, the body becomes targetable.
execute unless score #mbSt mb matches 0 run return 0
tag @e[tag=rlk_mb_body] remove rlk_mb_inv
scoreboard players set #mbSt mb 1
scoreboard players set #mbT mb 0
''')
w('fight_tick', '''
function rlk:mboss/d/tick
execute if score #mbSt mb matches 1 unless score #mbNoLeash mb matches 1 run function rlk:mboss/mv/leash
''')
w('death_start', '''
# @s = body whose HP reached 0 in combat/apply (heal orb, XP and gold of the lethal hit already paid).
# The body keeps rlk_zmob until death_finish, so the zone clears only after the death sequence.
execute if entity @s[tag=rlk_mb_dying] run return 0
tag @s add rlk_mb_dying
tag @s add rlk_mb_inv
scoreboard players set @s mhpC 0
scoreboard players set #mbKilled mb 1
scoreboard players set #mbSt mb 2
scoreboard players set #mbT mb 0
function rlk:mboss/lib_clear
function rlk:mboss/bars_hide
# Generic death roar unless the registry entry sets deathSnd false (the module plays its own death sound).
execute unless data storage rlk:mboss cur{deathSnd:0b} at @s run playsound minecraft:entity.wither.death hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
function rlk:mboss/d/death_start
''')
w('death_shell', '''
function rlk:mboss/d/death_tick
execute if score #mbT mb >= #mbDeath mb run function rlk:mboss/death_finish
''')
w('death_finish', '''
# @s = body. Removing the last rlk_zmob lets room/combat_tick clear the zone -> mboss/won.
execute at @s run particle minecraft:poof ~ ~1 ~ 0.6 1 0.6 0.02 30 force @a[tag=player]
kill @s
''')
w('lib_clear', '''
# Cancels every running library effect (death, tests). Module decals tagged rlk_mb_hzfx go with them.
kill @e[tag=rlk_mb_hz]
kill @e[tag=rlk_mb_hzfx]
kill @e[tag=rlk_mb_pj]
kill @e[tag=rlk_mb_pullpt]
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
''')

# =============================================================================================
# Damage to the player, true damage to mobs
w('hurt', '''
# Generic hit on the player. @s = the attacker (hazard marker, projectile, the body for a direct swing);
# it is the knockback source. Inputs: #mbHitPct mb (coefficient %, 100 = registry atk), #cmEl tmp
# (element), #mbKB mb (knockback steps, 0 none), #mbKBDir mb (0 away from @s, 1 along @s's yaw).
# Goes through cm/hit_pl2 -> player/take_damage: dash i-frames, defence, level scaling, element, shields.
# Output: #dodged tmp 1 when the dash i-frames ate the hit. #mbNoDodge mb 1 (set around the call by hz/hurt for a
# #hzNoDodge hazard): the dash i-frames are ignored for this one hit (the player keeps them for the next).
scoreboard players set #dodged tmp 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if score #mbSt mb matches 2 run return 0
scoreboard players operation #cmDmg tmp = #mbAtk mb
scoreboard players operation #cmDmg tmp *= #mbHitPct mb
scoreboard players operation #cmDmg tmp *= #mbDmgMul mb
scoreboard players operation #cmDmg tmp /= #c10000 mb
execute if score #cmDmg tmp matches ..0 run scoreboard players set #cmDmg tmp 1
scoreboard players operation #cmLv tmp = #mbLv mb
scoreboard players operation #cmKB tmp = #mbKB mb
kill @e[tag=rlk_plkb_source]
execute if score #cmKB tmp matches 1.. run function rlk:mboss/kb_src
execute unless score #mbNoDodge mb matches 1 as @a[tag=player,limit=1] run function rlk:cm/hit_pl2
# #mbNoDodge mb 1 (a #hzNoDodge hazard): dash i-frames do not help this hit
execute if score #mbNoDodge mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/hurt_nd
kill @e[tag=rlk_plkb_source]
scoreboard players set #mbKBDir mb 0
''')
w('hurt_nd', '''
# @s = player: one hit that dash i-frames cannot dodge (dashInvT is 0 during the call, then restored).
execute store result score #mbDI mb run scoreboard players get @s dashInvT
scoreboard players set @s dashInvT 0
function rlk:cm/hit_pl2
scoreboard players operation @s dashInvT = #mbDI mb
''')
w('kb_src', '''
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_plkb_source"]}
execute if score #mbKBDir mb matches 0 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 run tp @e[tag=rlk_plkb_source,limit=1] ~ ~ ~ ~ 0
execute if score #mbKBDir mb matches 1 at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_plkb_source,limit=1] ~ ~ ~ ~ 0
''')
w('true_hit', '''
# True damage to @s (any rlk_mob, normally the body) at @s: #mbTrue mb = damage, #mbTrueEl mb = colour
# of the number (#elem). Goes through combat/apply (kill, rewards, death_start) but skips elements,
# modifiers, RES and the module hooks (#trueDmg). Never call it from inside combat/apply.
# A lethal hit on the body runs mboss/death_start (and the module's death_start) BEFORE this returns: when
# called from the module's own tick, stop that tick right after it if #mbSt mb is 2 (hz/pj/pull refuse
# anyway while the boss is dying).
scoreboard players add #hitLanded tmp 0
scoreboard players operation #mbSaveHL mb = #hitLanded tmp
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = #mbTrue mb
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #basic itv 0
scoreboard players set #bowHit tmp 0
scoreboard players operation #elem tmp = #mbTrueEl mb
scoreboard players set #tfm tmp 1
scoreboard players set #trueDmg tmp 1
function rlk:combat/apply
scoreboard players set #trueDmg tmp 0
scoreboard players set #tfm tmp 0
scoreboard players operation #hitLanded tmp = #mbSaveHL mb
''')
w('true_pct', '''
# @s = target: true damage of $(pct) % of its max HP (mhpM / 100 x pct, overflow-safe). Colour = #mbTrueEl.
scoreboard players operation #mbTrue mb = @s mhpM
scoreboard players operation #mbTrue mb /= #c100 mb
$scoreboard players set #t mb $(pct)
scoreboard players operation #mbTrue mb *= #t mb
execute if score #mbTrue mb matches ..0 run scoreboard players set #mbTrue mb 1
function rlk:mboss/true_hit
''')

# =============================================================================================
# Aux objects (rlk_mb_hit): hit routing from combat/apply
w('aux_hit', '''
# From combat/apply after element/on_hit and combat/apply_mods (@s = aux with rlk_mb_hit; #dmg #elem #elU #rx
# #tfm #crit known). #dmg is already modified exactly like a hit on the body (engravings, items, level factor,
# Ronova, the aux's own mres), so a pool sized as a share of the boss's max HP (#auxHpPct) breaks in that share
# of the boss's kill time. The module hook may change #dmg or take over completely (#mbAuxDone mb 1); by
# default #dmg comes off the aux's mhpC with a number. Nothing here re-enters combat/apply; a broken aux gets
# rlk_mb_broken and the module acts on it in its tick.
scoreboard players set #hitLanded tmp 1
execute unless entity @s[tag=rlk_mb_broken] run function rlk:mboss/aux_hit2
# Like the end of combat/apply: a frost crit made for this target only does not spread to the next one.
execute if score #frostC eng matches 1 run scoreboard players set #crit tmp 0
execute if score #frostC eng matches 1 run scoreboard players set #frostC eng 0
''')
w('aux_hit2', '''
scoreboard players set #mbAuxDone mb 0
function rlk:mboss/d/aux_hit
execute if score #mbAuxDone mb matches 1 run return 0
function rlk:mboss/aux/take
''')
w('aux/take', '''
# @s = aux: #dmg off its own pool (mhpC/mhpM, shown by its overhead bar), number, flash.
execute if score #dmg tmp matches ..0 run return run function rlk:mboss/aux/immune
scoreboard players operation @s mhpC -= #dmg tmp
function rlk:mboss/aux/number
execute if score @s mhpC matches ..0 run function rlk:mboss/aux/broke
''')
w('aux/number', '''
# Damage number at @s (same look as combat/apply).
function rlk:element/color
execute store result storage rlk:combat dmg int 1 run scoreboard players get #dmg tmp
execute store result storage rlk:combat ox float 0.1 run random value -8..8
execute store result storage rlk:combat oz float 0.1 run random value -8..8
execute store result storage rlk:combat oy float 0.1 run random value 16..26
execute if score #crit tmp matches 1 run function rlk:combat/text_crit_macro with storage rlk:combat
execute unless score #crit tmp matches 1 run function rlk:combat/text_normal_macro with storage rlk:combat
particle minecraft:crit ~ ~1 ~ 0.25 0.35 0.25 0.12 8
''')
w('aux/immune', '''
# "면역" popup at @s (immune element or a zero-damage hit).
summon minecraft:text_display ~ ~1.9 ~ {billboard:"center",Tags:["dmgText"],background:0,brightness:{sky:15,block:15},shadow:true,alignment:"center",see_through:true,text:{text:"면역",color:"#D8D8D8"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.1f,1.1f,1.1f]}}
''')
w('aux/broke', '''
scoreboard players set @s mhpC 0
tag @s add rlk_mb_broken
scoreboard players add #mbAuxBroke mb 1
''')
w('aux/spawn', '''
# Helper object the player can hit (stars, cores ...), at the execution position. Options set before the
# call: #auxHpPct mb = HP pool in % of the body's max HP (scales with the boss level; preferred), else
# #auxHp mb = fixed HP pool; #auxRes mb = RES %. Invisible NoAI husk with the boss tag (no stun, freeze,
# knockback), rlk_mob + overhead HP bar, a click shield, the boss level; never rlk_zmob. Player hits on it
# take the same modifiers as hits on the body (combat/apply_mods). The new one carries rlk_mb_auxlast until
# the next aux/spawn: add the module's own tags/visuals to it.
tag @e[tag=rlk_mb_auxlast] remove rlk_mb_auxlast
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_hit","boss","rlk_mb_auxlast"],PersistenceRequired:1b,NoAI:1b,NoGravity:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_mb_auxlast,limit=1] at @s run function rlk:mboss/aux/setup
scoreboard players set #auxHp mb 100
scoreboard players set #auxHpPct mb 0
scoreboard players set #auxRes mb 0
''')
w('aux/setup', '''
attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
scoreboard players operation @s mlv = #mbLv mb
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
execute if score #auxHpPct mb matches 1.. run function rlk:mboss/aux/pool_pct
scoreboard players operation @s mhpM = #auxHp mb
execute unless score @s mhpM matches 1.. run scoreboard players set @s mhpM 1
scoreboard players operation @s mhpC = @s mhpM
scoreboard players operation @s mres = #auxRes mb
''')
w('aux/pool_pct', '''
# #auxHp mb = body max HP x #auxHpPct / 100 (1..100 %, overflow-safe; no body = #auxHp unchanged).
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run return 0
execute if score #auxHpPct mb matches 101.. run scoreboard players set #auxHpPct mb 100
scoreboard players operation #t mb = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] mhpM
execute if score #t mb matches 10000000.. run return run function rlk:mboss/aux/pool_big
scoreboard players operation #t mb *= #auxHpPct mb
scoreboard players operation #t mb /= #c100 mb
scoreboard players operation #auxHp mb = #t mb
''')
w('aux/pool_big', '''
scoreboard players operation #t mb /= #c100 mb
scoreboard players operation #t mb *= #auxHpPct mb
scoreboard players operation #auxHp mb = #t mb
''')

# =============================================================================================
# Bars
w('bars_show', '''
# Order matters: a bar made visible later is drawn below the others.
bossbar set rlk:mboss players @a[tag=player]
bossbar set rlk:mboss_state players @a[tag=player]
bossbar set rlk:mboss_sub players @a[tag=player]
bossbar set rlk:mboss visible true
bossbar set rlk:mboss_state visible true
bossbar set rlk:mboss_sub visible true
scoreboard players set #mbBar mb 1
''')
w('bars_hide', '''
bossbar set rlk:mboss visible false
bossbar set rlk:mboss_state visible false
bossbar set rlk:mboss_sub visible false
scoreboard players set #mbBar mb 0
''')
w('bars', '''
# @s = body. Line 1: Lv + name + element auras on the boss + rlk:mboss extra[]. Line 2: bossui HP bar
# with the under-bar the module fills in its bars hook (#buSub #buSubMax #buSubCol). Line 3: rlk:mboss sub[].
execute unless score #mbBar mb matches 1 run function rlk:mboss/bars_show
# A relogged player keeps the bars (player lists refresh every tick, order unchanged).
bossbar set rlk:mboss players @a[tag=player]
bossbar set rlk:mboss_state players @a[tag=player]
bossbar set rlk:mboss_sub players @a[tag=player]
function rlk:mboss/aura
bossbar set rlk:mboss name [{text:"Lv.",color:"#FFD86B",bold:true},{score:{name:"@s",objective:"mlv"},color:"#FFD86B",bold:true},{text:"  ",bold:false},{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{nbt:"aura[]",storage:"rlk:mboss",interpret:true,separator:""},{nbt:"extra[]",storage:"rlk:mboss",interpret:true,separator:""}]
scoreboard players operation #buHp bu = @s mhpC
scoreboard players operation #buMax bu = @s mhpM
execute if score #mbSt mb matches 0 if score #mbT mb matches ..29 run function rlk:mboss/bars_ramp
scoreboard players set #buSub bu 0
scoreboard players set #buSubMax bu 1
scoreboard players set #buSubCol bu 0
function rlk:mboss/d/bars
function rlk:bossui/draw
bossbar set rlk:mboss_state name {nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}
bossbar set rlk:mboss_sub name {nbt:"sub[]",storage:"rlk:mboss",interpret:true,separator:""}
''')
w('bars_ramp', '''
# Intro: the HP bar fills over 1.5 s.
scoreboard players operation #buHp bu *= #mbT mb
scoreboard players operation #buHp bu /= #c30 mb
''')
w('aura', '''
# @s = body. Element auras as glyphs on the name line (the body has no overhead bar). Rebuilt on change.
scoreboard players set #k mb 0
execute if score @s aFire matches 1.. run scoreboard players add #k mb 1
execute if score @s aWater matches 1.. run scoreboard players add #k mb 2
execute if score @s aThunder matches 1.. run scoreboard players add #k mb 4
execute if score @s aIce matches 1.. run scoreboard players add #k mb 8
execute if score @s aGrass matches 1.. run scoreboard players add #k mb 16
execute if score @s aVoid matches 1.. run scoreboard players add #k mb 32
execute if score @s frzT matches 1.. run scoreboard players add #k mb 64
execute if score #k mb = #mbAuraK mb run return 0
scoreboard players operation #mbAuraK mb = #k mb
data modify storage rlk:mboss aura set value []
execute if score @s aFire matches 1.. run data modify storage rlk:mboss aura append value {text:"  🔥",color:"#FF8A3D"}
execute if score @s aWater matches 1.. run data modify storage rlk:mboss aura append value {text:"  🌊",color:"#4FB8FF"}
execute if score @s aThunder matches 1.. run data modify storage rlk:mboss aura append value {text:"  ⚡",color:"#C58BFF"}
execute if score @s aIce matches 1.. run data modify storage rlk:mboss aura append value {text:"  ❄",color:"#9FE8F5"}
execute if score @s aGrass matches 1.. run data modify storage rlk:mboss aura append value {text:"  ♣",color:"#A5D94A"}
execute if score @s aVoid matches 1.. run data modify storage rlk:mboss aura append value {text:"  ◉",color:"#E0365F"}
execute if score @s frzT matches 1.. run data modify storage rlk:mboss aura append value {text:"  [빙결]",color:"#E6F7FF",bold:true}
''')
bu_lines = ['# #mbE mb (#elem numbering) -> #buSubCol bu (bossui colour codes).']
for e, c in L.ELEM_TO_BU.items():
    bu_lines.append(f'execute if score #mbE mb matches {e} run scoreboard players set #buSubCol bu {c}')
w('elem_to_bu', '\n'.join(bu_lines))

# =============================================================================================
# Typed subtitle lines
w('line/say', '''
# Typed subtitle: {t:"text",c:"#colour",gap:ticks per step,hold:ticks the full line stays,snd:0 none/1 soft/2 stern}.
# Grows two characters per step with a quiet tick; a new line replaces the running one.
$data modify storage rlk:mboss ln set value {t:"$(t)",c:"$(c)",n:0,stay:0}
$scoreboard players set #mbLnGap mb $(gap)
$scoreboard players set #mbLnHold mb $(hold)
$scoreboard players set #mbLnSnd mb $(snd)
execute if score #mbLnGap mb matches ..0 run scoreboard players set #mbLnGap mb 1
execute store result score #mbLnLen mb run data get storage rlk:mboss ln.t
scoreboard players set #mbLnN mb 0
scoreboard players set #mbLnT mb 0
scoreboard players set #mbLn mb 1
execute if score #mbLnSnd mb matches 1 as @a[tag=player] at @s run playsound minecraft:block.amethyst_block.resonate voice @s ~ ~ ~ 0.6 0.8
execute if score #mbLnSnd mb matches 2 as @a[tag=player] at @s run playsound minecraft:block.bell.resonate voice @s ~ ~ ~ 0.45 0.55
function rlk:mboss/line/step
''')
w('line/tick', '''
execute unless score #mbLn mb matches 1 run return 0
execute if entity @a[tag=player,scores={dead=1}] run return 0
scoreboard players add #mbLnT mb 1
execute if score #mbLnT mb >= #mbLnGap mb run function rlk:mboss/line/next
''')
w('line/next', '''
scoreboard players set #mbLnT mb 0
function rlk:mboss/line/step
''')
w('line/step', '''
scoreboard players add #mbLnN mb 2
execute if score #mbLnN mb > #mbLnLen mb run scoreboard players operation #mbLnN mb = #mbLnLen mb
execute store result storage rlk:mboss ln.n int 1 run scoreboard players get #mbLnN mb
function rlk:mboss/line/cut with storage rlk:mboss ln
scoreboard players operation #mbLnStay mb = #mbLnGap mb
scoreboard players add #mbLnStay mb 6
execute if score #mbLnN mb >= #mbLnLen mb run scoreboard players operation #mbLnStay mb = #mbLnHold mb
execute store result storage rlk:mboss ln.stay int 1 run scoreboard players get #mbLnStay mb
scoreboard players operation #mbLnTtl mb = #mbLnStay mb
scoreboard players add #mbLnTtl mb 12
function rlk:mboss/line/show with storage rlk:mboss ln
scoreboard players operation @a[tag=player] ttlT = #mbLnTtl mb
execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute if score #mbLnN mb >= #mbLnLen mb run scoreboard players set #mbLn mb 0
''')
w('line/cut', '$data modify storage rlk:mboss ln.cur set string storage rlk:mboss ln.t 0 $(n)')
w('line/show', '''
$title @a[tag=player] times 0 $(stay) 12
$title @a[tag=player] subtitle {nbt:"ln.cur",storage:"rlk:mboss",color:"$(c)",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
''')
w('line/clear', '''
execute unless score #mbLn mb matches 1 run return 0
scoreboard players set #mbLn mb 0
title @a[tag=player] subtitle ""
scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0
''')

# =============================================================================================
# Dispatchers
for hook in L.HOOKS:
    args = L.MACRO_HOOKS.get(hook)
    if hook in L.ALL_MODULE_HOOKS:
        lines = [f'# GENERATED dispatcher: rlk:mboss/<id>/{hook} of every enabled mid-boss module (none needs to be running).']
        lines += [f'function rlk:mboss/{b["id"]}/{hook}' for b in BOSSES]
        out.write('mboss/d/' + hook, '\n'.join(lines))
        continue
    lines = [f'# GENERATED dispatcher: rlk:mboss/<id>/{hook} of the running mid-boss (#mbId mb = registry n).']
    for b in BOSSES:
        if args:
            argtxt = '{' + ','.join(f'{a}:$({a})' for a in args) + '}'
            lines.append(f'$execute if score #mbId mb matches {b["n"]} run return run function rlk:mboss/{b["id"]}/{hook} {argtxt}')
        else:
            lines.append(f'execute if score #mbId mb matches {b["n"]} run return run function rlk:mboss/{b["id"]}/{hook}')
    if args:
        lines.append('$scoreboard players set #mbReqT mb $(' + args[0] + ')')
    out.write('mboss/d/' + hook, '\n'.join(lines))

# =============================================================================================
# Hazard library (hz)
for kind, keys, body in (
    ('disc', ['r', 'tell', 'dmg'], ['$scoreboard players set #hzR mb $(r)', 'scoreboard players set #hzK mb 1']),
    ('ring', ['r0', 'r', 'tell', 'dmg'], ['$scoreboard players set #hzR mb $(r)', '$scoreboard players set #hzR0 mb $(r0)',
                                          'scoreboard players set #hzK mb 2']),
    ('sector', ['r', 'a', 'tell', 'dmg'], ['$scoreboard players set #hzR mb $(r)', '$scoreboard players set #hzAng mb $(a)',
                                           '$execute store result score #hzC mb run data get storage rlk:mboss cos[$(a)]',
                                           'scoreboard players set #hzK mb 3']),
    ('line', ['len', 'w', 'tell', 'dmg'], ['$scoreboard players set #hzR mb $(len)', '$scoreboard players set #hzHW mb $(w)',
                                           'scoreboard players set #hzK mb 4']),
    ('full', ['tell', 'dmg'], [f'scoreboard players set #hzR mb {WALK * 10}', 'scoreboard players set #hzK mb 5']),
):
    doc = {
        'disc': 'Filled circle of radius r around the execution position.',
        'ring': 'Annulus r0..r (the hole is safe). For a jumpable wave set #hzY1 small (e.g. 7 = 0.7 b).',
        'sector': 'Sector/arc: radius r, half-angle a degrees (1..180, 180 = full 360 swing) around the aim;'
                  ' option #hzR0 makes it an arc (inner part safe).',
        'line': 'Rectangle: from the execution position forward len, total width w (option #hzBack starts it behind).',
        'full': 'The whole arena; option #hzR0 = safe circle (radius, tenths) around the execution position.',
    }[kind]
    w('hz/' + kind, '\n'.join([
        f'# {doc}',
        '# As anything, positioned on the floor point, rotated = aim (pitch ignored). tell = ticks of telegraph',
        '# until the hit is resolved, dmg = % of the boss base hit (0 = telegraph only). Units: tenths of a block.',
        '# Options: opts_reset (#hzGrp = volley group, see mboss/grp_new; #hzNoDodge 1 = dash i-frames do not help;',
        '# #hzRearm N = a hit disarms it for N ticks only, then it can hit again; live changes: hz/aim, hz/resize).',
        f'# Call: function rlk:mboss/hz/{kind} {{' + ','.join(f'{k}:..' for k in keys) + '}'] + body + [
        '$scoreboard players set #hzW mb $(tell)', '$scoreboard players set #hzD mb $(dmg)',
        'function rlk:mboss/hz/make']))

w('hz/make', '''
# In the caller's context (floor point, aim yaw). Summons the hazard marker, then resets the options.
# Refused while the boss is dying (#mbSt 2: a lethal true hit inside the module tick must not leave
# hazards behind lib_clear); #hzLast is then 0.
execute if score #mbSt mb matches 2 run scoreboard players set #hzLast mb 0
execute if score #mbSt mb matches 2 run function rlk:mboss/opts_reset
execute if score #mbSt mb matches 2 run return fail
scoreboard players set #mbHzOn mb 1
execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_hz","rlk_mb_aux","rlk_room","rlk_mb_hznew"]}
execute rotated ~ 0 as @e[tag=rlk_mb_hznew,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rlk_mb_hznew,limit=1] at @s rotated as @s run function rlk:mboss/hz/init
tag @e[tag=rlk_mb_hznew] remove rlk_mb_hznew
function rlk:mboss/opts_reset
''')
w('hz/init', '''
# @s = new hazard marker, at/rotated as @s. Scores from #hz* (tenths -> milliblocks).
scoreboard players operation @s mbHzK = #hzK mb
scoreboard players operation @s mbHzW = #hzW mb
scoreboard players operation @s mbHzD = #hzD mb
scoreboard players operation @s mbHzA = #hzAct mb
scoreboard players operation @s mbHzE = #mbEl mb
execute if score #hzEl mb matches 0.. run scoreboard players operation @s mbHzE = #hzEl mb
scoreboard players operation @s mbHzB = #hzKB mb
# Knockback direction: 0 away from the origin, 1 along the aim, -1 (default) = shape default (lines 1, else 0).
scoreboard players operation @s mbHzKD = #hzKBDir mb
execute unless score @s mbHzKD matches 0..1 run scoreboard players set @s mbHzKD 0
execute if score @s mbHzK matches 4 unless score #hzKBDir mb matches 0..1 run scoreboard players set @s mbHzKD 1
scoreboard players operation @s mbHzS = #hzSfx mb
scoreboard players operation @s mbHzV = #hzVis mb
scoreboard players operation @s mbHzG = #hzGrp mb
scoreboard players operation @s mbHzND = #hzNoDodge mb
scoreboard players operation @s mbHzRA = #hzRearm mb
scoreboard players set @s mbHzRT 0
scoreboard players operation @s mbHzCol = @s mbHzE
execute if score #hzCol mb matches 0.. run scoreboard players operation @s mbHzCol = #hzCol mb
execute if score #hzQuiet mb matches 1 run tag @s add rlk_mb_hzq
execute if score @s mbHzW matches ..0 run scoreboard players set @s mbHzW 1
execute if score @s mbHzA matches ..0 run scoreboard players set @s mbHzA 1
scoreboard players set @s mbHzT -1
scoreboard players set @s mbHzHit 0
scoreboard players operation @s mbHzL = @s mbHzW
scoreboard players operation @s mbHzL += @s mbHzA
scoreboard players operation @s mbHzL += #hzLinger mb
scoreboard players add #hzId mb 1
scoreboard players operation @s mbHzI = #hzId mb
scoreboard players operation #hzLast mb = #hzId mb
scoreboard players operation @s mbHzY0 = #hzY0 mb
scoreboard players operation @s mbHzY0 *= #c100 mb
scoreboard players operation @s mbHzY1 = #hzY1 mb
scoreboard players operation @s mbHzY1 *= #c100 mb
scoreboard players operation @s mbHzR = #hzR mb
scoreboard players operation @s mbHzR *= #c100 mb
scoreboard players operation @s mbHzR0 = #hzR0 mb
scoreboard players operation @s mbHzR0 *= #c100 mb
scoreboard players set @s mbHzAng 180
scoreboard players set @s mbHzC 0
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/init_sector
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/init_line
# Squared bounds with a 0.3-block body pad: outer grows, inner (safe hole) shrinks.
scoreboard players operation #t mb = @s mbHzR
scoreboard players add #t mb 300
scoreboard players operation @s mbHzRR = #t mb
scoreboard players operation @s mbHzRR *= #t mb
scoreboard players operation #t mb = @s mbHzR0
scoreboard players remove #t mb 300
execute if score #t mb matches ..-1 run scoreboard players set #t mb 0
scoreboard players operation @s mbHzRI = #t mb
scoreboard players operation @s mbHzRI *= #t mb
# full: the safe circle is exact (body centre inside = safe).
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI = @s mbHzR0
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI *= @s mbHzR0
# Local forward axis x1000 from a temporary marker (exact, no trigonometry at runtime).
execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_hzax"]}
execute store result score #ox mb run data get entity @s Pos[0] 1000
execute store result score #oz mb run data get entity @s Pos[2] 1000
execute store result score @s mbHzFX run data get entity @e[tag=rlk_mb_hzax,limit=1] Pos[0] 1000
execute store result score @s mbHzFZ run data get entity @e[tag=rlk_mb_hzax,limit=1] Pos[2] 1000
scoreboard players operation @s mbHzFX -= #ox mb
scoreboard players operation @s mbHzFZ -= #oz mb
kill @e[tag=rlk_mb_hzax]
function rlk:mboss/hz/init_draw
execute if score @s mbHzV matches 1.. run scoreboard players set #hzEv mb 0
execute if score @s mbHzV matches 1.. run function rlk:mboss/d/hz_vis
''')
w('hz/init_sector', '''
scoreboard players operation @s mbHzAng = #hzAng mb
execute if score @s mbHzAng matches ..0 run scoreboard players set @s mbHzAng 1
execute if score @s mbHzAng matches 181.. run scoreboard players set @s mbHzAng 180
scoreboard players operation @s mbHzC = #hzC mb
''')
w('hz/init_line', '''
# len = mbHzR, back = mbHzR0; half width (tenths of the full width x 50) with the body pad.
scoreboard players operation @s mbHzHW = #hzHW mb
scoreboard players operation @s mbHzHW *= #c100 mb
scoreboard players operation @s mbHzHW /= #c2 mb
scoreboard players operation @s mbHzC = @s mbHzHW
scoreboard players add @s mbHzHW 300
scoreboard players operation @s mbHzR0 = #hzBack mb
scoreboard players operation @s mbHzR0 *= #c100 mb
scoreboard players operation @s mbHzLo = @s mbHzR0
scoreboard players operation @s mbHzLo *= #cm1 mb
scoreboard players remove @s mbHzLo 300
scoreboard players operation @s mbHzHi = @s mbHzR
scoreboard players add @s mbHzHi 300
''')
w('hz/init_draw', '''
# Particle drawing parameters in the marker's data (read with "with storage rlk:mboss hzp"):
# k/k0 = outer/inner circle bucket (0.5 b, max 30 b), kr = ray bucket (max 45 b), kw = bar bucket.
scoreboard players operation #kraw mb = @s mbHzR
scoreboard players add #kraw mb 250
scoreboard players operation #kraw mb /= #c500 mb
scoreboard players operation #k0raw mb = @s mbHzR0
scoreboard players add #k0raw mb 250
scoreboard players operation #k0raw mb /= #c500 mb
scoreboard players operation #k mb = #kraw mb
execute if score #k mb matches ..0 run scoreboard players set #k mb 1
execute if score #k mb matches 61.. run scoreboard players set #k mb 60
execute store result entity @s data.k int 1 run scoreboard players get #k mb
scoreboard players operation #k0 mb = #k0raw mb
execute if score #k0 mb matches ..0 run scoreboard players set #k0 mb 1
execute if score #k0 mb matches 61.. run scoreboard players set #k0 mb 60
execute store result entity @s data.k0 int 1 run scoreboard players get #k0 mb
scoreboard players operation #kr mb = #kraw mb
execute unless score @s mbHzK matches 4 run scoreboard players operation #kr mb -= #k0raw mb
execute if score @s mbHzK matches 4 run scoreboard players operation #kr mb += #k0raw mb
execute if score #kr mb matches ..0 run scoreboard players set #kr mb 1
execute if score #kr mb matches 91.. run scoreboard players set #kr mb 90
execute store result entity @s data.kr int 1 run scoreboard players get #kr mb
execute store result entity @s data.a int 1 run scoreboard players get @s mbHzAng
execute store result entity @s data.r0b double 0.001 run scoreboard players get @s mbHzR0
execute store result entity @s data.nb double -0.001 run scoreboard players get @s mbHzR0
execute store result entity @s data.lenb double 0.001 run scoreboard players get @s mbHzR
execute store result entity @s data.hw double 0.001 run scoreboard players get @s mbHzC
execute store result entity @s data.nhw double -0.001 run scoreboard players get @s mbHzC
scoreboard players operation #kw mb = @s mbHzC
scoreboard players operation #kw mb /= #c500 mb
scoreboard players operation #kw mb *= #c2 mb
execute if score #kw mb matches ..0 run scoreboard players set #kw mb 1
execute if score #kw mb matches 41.. run scoreboard players set #kw mb 40
execute store result entity @s data.kw int 1 run scoreboard players get #kw mb
data modify entity @s data.sc set value "1.0"
''' + '\n'.join(f'execute if score @s mbHzCol matches {i} run data modify entity @s data.col set from storage rlk:mboss hzc[{i}]'
                for i in range(11)))

w('hz/tick', '''
# @s = hazard marker, at/rotated as @s (world tick; frozen while the fight is paused).
scoreboard players set #mbHzOn mb 1
scoreboard players add @s mbHzT 1
execute if score @s mbHzT >= @s mbHzL run return run function rlk:mboss/hz/expire
scoreboard players operation #t mb = @s mbHzT
scoreboard players operation #t mb %= #c4 mb
execute if score @s mbHzT < @s mbHzW if score #t mb matches 0 unless entity @s[tag=rlk_mb_hzq] run function rlk:mboss/hz/draw
execute if score @s mbHzT = @s mbHzW run function rlk:mboss/hz/strike
scoreboard players operation #hzEnd mb = @s mbHzW
scoreboard players operation #hzEnd mb += @s mbHzA
# #hzRearm: a hit (or a hit of its volley group) disarmed it until the re-arm clock reaches mbHzRT
execute if score @s mbHzHit matches 1 if score @s mbHzRA matches 1.. if score #mbHzClk mb >= @s mbHzRT run scoreboard players set @s mbHzHit 0
# dmg 0 = telegraph only (outline, strike flash and the module visuals; never a hit)
execute if score @s mbHzHit matches 0 if score @s mbHzD matches 1.. if score @s mbHzT >= @s mbHzW if score @s mbHzT < #hzEnd mb run function rlk:mboss/hz/hit
''')
w('hz/expire', '''
execute if score @s mbHzV matches 1.. run scoreboard players set #hzEv mb 2
execute if score @s mbHzV matches 1.. run function rlk:mboss/d/hz_vis
kill @s
''')
w('hz/draw', '''
# Telegraph: outline plus a progress outline that reaches the rim when the hit lands.
data modify storage rlk:mboss hzp set from entity @s data
scoreboard players operation #p mb = @s mbHzT
scoreboard players operation #p mb *= #c1000 mb
scoreboard players operation #p mb /= @s mbHzW
execute store result score #kp mb run data get storage rlk:mboss hzp.k
scoreboard players operation #kp mb *= #p mb
scoreboard players operation #kp mb /= #c1000 mb
execute if score #kp mb matches ..0 run scoreboard players set #kp mb 1
execute store result storage rlk:mboss hzp.kp int 1 run scoreboard players get #kp mb
scoreboard players operation #hzAng mb = @s mbHzAng
execute if score @s mbHzK matches 1 run function rlk:mboss/hz/d/disc with storage rlk:mboss hzp
execute if score @s mbHzK matches 2 run function rlk:mboss/hz/d/ring with storage rlk:mboss hzp
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/d/sector with storage rlk:mboss hzp
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/draw_line
execute if score @s mbHzK matches 5 run function rlk:mboss/hz/d/full with storage rlk:mboss hzp
''')
w('hz/draw_line', '''
# Progress bar position along the line: -back + (len + back) x progress.
scoreboard players operation #pz mb = @s mbHzR
scoreboard players operation #pz mb += @s mbHzR0
scoreboard players operation #pz mb *= #p mb
scoreboard players operation #pz mb /= #c1000 mb
scoreboard players operation #pz mb -= @s mbHzR0
execute store result storage rlk:mboss hzp.pz double 0.001 run scoreboard players get #pz mb
function rlk:mboss/hz/d/line with storage rlk:mboss hzp
''')
w('hz/d/disc', '''
$function rlk:mboss/hz/p/c/$(k) with storage rlk:mboss hzp
$function rlk:mboss/hz/p/c/$(kp) with storage rlk:mboss hzp
''')
w('hz/d/ring', '''
$function rlk:mboss/hz/p/c/$(k) with storage rlk:mboss hzp
$execute if score @s mbHzR0 matches 1.. run function rlk:mboss/hz/p/c/$(k0) with storage rlk:mboss hzp
$function rlk:mboss/hz/p/c/$(kp) with storage rlk:mboss hzp
''')
w('hz/d/sector', '''
$function rlk:mboss/hz/p/c/$(k) with storage rlk:mboss hzp
$execute if score @s mbHzR0 matches 1.. run function rlk:mboss/hz/p/c/$(k0) with storage rlk:mboss hzp
$function rlk:mboss/hz/p/c/$(kp) with storage rlk:mboss hzp
$execute if score @s mbHzAng matches ..179 rotated ~$(a) 0 positioned ^ ^ ^$(r0b) run function rlk:mboss/hz/p/r/$(kr) with storage rlk:mboss hzp
$execute if score @s mbHzAng matches ..179 rotated ~-$(a) 0 positioned ^ ^ ^$(r0b) run function rlk:mboss/hz/p/r/$(kr) with storage rlk:mboss hzp
''')
w('hz/d/line', '''
$execute positioned ^$(hw) ^ ^$(nb) run function rlk:mboss/hz/p/r/$(kr) with storage rlk:mboss hzp
$execute positioned ^$(nhw) ^ ^$(nb) run function rlk:mboss/hz/p/r/$(kr) with storage rlk:mboss hzp
$execute positioned ^ ^ ^$(nb) run function rlk:mboss/hz/p/b/$(kw) with storage rlk:mboss hzp
$execute positioned ^ ^ ^$(lenb) run function rlk:mboss/hz/p/b/$(kw) with storage rlk:mboss hzp
$execute positioned ^ ^ ^$(pz) run function rlk:mboss/hz/p/b/$(kw) with storage rlk:mboss hzp
''')
w('hz/d/full', '''
# Arena rim, the safe circle (green) and a ring growing from the centre.
execute positioned @CX@ ~ @CZ@ run function rlk:mboss/hz/p/c/@WALK2X@ with storage rlk:mboss hzp
$execute positioned @CX@ ~ @CZ@ run function rlk:mboss/hz/p/c/$(kp) with storage rlk:mboss hzp
execute if score @s mbHzR0 matches 1.. run function rlk:mboss/hz/d/full_safe
'''.replace('@WALK2X@', str(WALK * 2)))
w('hz/d/full_safe', '''
data modify storage rlk:mboss hzs set from storage rlk:mboss hzp
data modify storage rlk:mboss hzs.col set from storage rlk:mboss hzc[10]
data modify storage rlk:mboss hzs.sc set value "1.3"
function rlk:mboss/hz/d/full_safe2 with storage rlk:mboss hzs
''')
w('hz/d/full_safe2', '$function rlk:mboss/hz/p/c/$(k0) with storage rlk:mboss hzs')
w('hz/strike', '''
# Hit frame: bright outline + fill, sound, module visual event 1.
execute unless entity @s[tag=rlk_mb_hzq] run function rlk:mboss/hz/flash
execute if score @s mbHzS matches 1 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.55 1.5 0.18
execute if score @s mbHzS matches 1 run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.3 0.6 0.1
execute if score @s mbHzS matches 2 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute if score @s mbHzS matches 3 run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute if score @s mbHzS matches 4 run playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute if score @s mbHzS matches 4 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.23
execute if score @s mbHzV matches 1.. run scoreboard players set #hzEv mb 1
execute if score @s mbHzV matches 1.. run function rlk:mboss/d/hz_vis
''')
w('hz/flash', '''
data modify storage rlk:mboss hzp set from entity @s data
data modify storage rlk:mboss hzp.col set from storage rlk:mboss hzc[9]
data modify storage rlk:mboss hzp.sc set value "1.5"
scoreboard players operation #hzAng mb = @s mbHzAng
execute store result score #kp mb run data get storage rlk:mboss hzp.k
scoreboard players operation #kp mb *= #c2 mb
scoreboard players operation #kp mb /= #c4 mb
execute if score #kp mb matches ..0 run scoreboard players set #kp mb 1
execute store result storage rlk:mboss hzp.kp int 1 run scoreboard players get #kp mb
scoreboard players set #p mb 500
execute if score @s mbHzK matches 1 run function rlk:mboss/hz/d/disc with storage rlk:mboss hzp
execute if score @s mbHzK matches 2 run function rlk:mboss/hz/d/ring with storage rlk:mboss hzp
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/d/sector with storage rlk:mboss hzp
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/draw_line
execute if score @s mbHzK matches 1..3 run particle minecraft:explosion ~ ~0.3 ~ 0.6 0.1 0.6 0 2 force @a[tag=player]
execute if score @s mbHzK matches 5 run particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 force @a[tag=player]
''')
w('hz/hit', '''
# @s = hazard marker, at @s, inside its active window. Body feet only (never the camera).
scoreboard players set #hzHit mb 0
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute store result score #dy mb run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #t mb run data get entity @s Pos[1] 1000
scoreboard players operation #dy mb -= #t mb
execute if score #dy mb < @s mbHzY0 run return 0
execute if score #dy mb > @s mbHzY1 run return 0
execute if score @s mbHzK matches 5 run return run function rlk:mboss/hz/hit_full
execute unless entity @e[tag=rlk_body,distance=..48,limit=1] run return 0
execute store result score #dx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #dz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #dx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #dz mb -= #t mb
# Projections on the frozen forward axis (fwd) and its left normal (side), milliblocks.
scoreboard players operation #fwd mb = #dx mb
scoreboard players operation #fwd mb *= @s mbHzFX
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= @s mbHzFZ
scoreboard players operation #fwd mb += #t mb
scoreboard players operation #fwd mb /= #c1000 mb
execute if score @s mbHzK matches 4 run return run function rlk:mboss/hz/k4
# Radial shapes: distance squared (safe from overflow inside 32 blocks).
execute unless entity @e[tag=rlk_body,distance=..32,limit=1] run return 0
scoreboard players operation #r2 mb = #dx mb
scoreboard players operation #r2 mb *= #dx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #dz mb
scoreboard players operation #r2 mb += #t mb
execute if score #r2 mb > @s mbHzRR run return 0
execute if score #r2 mb < @s mbHzRI run return 0
execute if score @s mbHzK matches 1..2 run return run function rlk:mboss/hz/hurt
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/k3
''')
w('hz/k3', '''
# Sector angle test: angle(d, forward) <= a  <=>  fwd >= cos(a) |d|, squared without sqrt.
execute if score @s mbHzAng matches 180.. run return run function rlk:mboss/hz/hurt
scoreboard players operation #c mb = @s mbHzC
execute if score #c mb matches ..-1 run scoreboard players operation #c mb *= #cm1 mb
scoreboard players operation #q mb = #r2 mb
scoreboard players operation #q mb /= #c1000 mb
scoreboard players operation #q mb *= #c mb
scoreboard players operation #q mb /= #c1000 mb
scoreboard players operation #q mb *= #c mb
scoreboard players operation #f2 mb = #fwd mb
scoreboard players operation #f2 mb *= #fwd mb
execute if score @s mbHzC matches 0.. if score #fwd mb matches 0.. if score #f2 mb >= #q mb run return run function rlk:mboss/hz/hurt
execute if score @s mbHzC matches ..-1 if score #fwd mb matches 0.. run return run function rlk:mboss/hz/hurt
execute if score @s mbHzC matches ..-1 if score #fwd mb matches ..-1 if score #f2 mb <= #q mb run return run function rlk:mboss/hz/hurt
''')
w('hz/k4', '''
# Line: -back <= fwd <= len and |side| <= half width (both with the body pad).
execute if score #fwd mb < @s mbHzLo run return 0
execute if score #fwd mb > @s mbHzHi run return 0
scoreboard players operation #side mb = #dx mb
scoreboard players operation #side mb *= @s mbHzFZ
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= @s mbHzFX
scoreboard players operation #side mb -= #t mb
scoreboard players operation #side mb /= #c1000 mb
execute if score #side mb matches ..-1 run scoreboard players operation #side mb *= #cm1 mb
execute if score #side mb <= @s mbHzHW run function rlk:mboss/hz/hurt
''')
w('hz/hit_full', '''
# Whole arena: hit unless the body centre is inside the safe circle (radius mbHzR0) of the origin.
execute if score @s mbHzR0 matches ..0 run return run function rlk:mboss/hz/hurt
execute unless entity @e[tag=rlk_body,distance=..30,limit=1] run return run function rlk:mboss/hz/hurt
execute store result score #dx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #dz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #dx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #dz mb -= #t mb
scoreboard players operation #r2 mb = #dx mb
scoreboard players operation #r2 mb *= #dx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #dz mb
scoreboard players operation #r2 mb += #t mb
execute if score #r2 mb > @s mbHzRI run function rlk:mboss/hz/hurt
''')
w('hz/hurt', '''
# One hit per hazard: a dodge (dash i-frames) also consumes it. #hzRearm hazards arm again mbHzRA ticks later;
# #hzNoDodge hazards ignore the dash i-frames (mboss/hurt with #mbNoDodge 1).
scoreboard players set @s mbHzHit 1
execute if score @s mbHzRA matches 1.. run function rlk:mboss/hz/rearm_at
scoreboard players set #hzHit mb 1
scoreboard players operation #mbHitPct mb = @s mbHzD
scoreboard players operation #cmEl tmp = @s mbHzE
scoreboard players operation #mbKB mb = @s mbHzB
scoreboard players operation #mbKBDir mb = @s mbHzKD
scoreboard players operation #mbNoDodge mb = @s mbHzND
function rlk:mboss/hurt
scoreboard players set #mbNoDodge mb 0
scoreboard players operation #g mb = @s mbHzG
execute if score #dodged tmp matches 0 if score #g mb matches 1.. run function rlk:mboss/grp_mark
''')
w('hz/rearm_at', '''
# @s = a #hzRearm hazard that is disarmed now: armed again when the re-arm clock #mbHzClk reaches mbHzRT.
scoreboard players operation @s mbHzRT = #mbHzClk mb
scoreboard players operation @s mbHzRT += @s mbHzRA
''')
w('hz/aim', '''
# Re-aim a live hazard (@s = its marker): it moves to the execution position and turns to the execution yaw
# (pitch ignored); the frozen forward axis of the hit test is recomputed exactly as hz/init does. For sweeping
# lines (lasers): execute as <marker> at <body> rotated as @s rotated ~5 0 positioned ^ ^ ^2.8 run function
# rlk:mboss/hz/aim. Call it from the module tick (it runs before hz/all, so this tick's hit test uses the new aim).
tp @s ~ ~ ~ ~ 0
execute at @s rotated as @s positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_hzax"]}
execute store result score #ox mb run data get entity @s Pos[0] 1000
execute store result score #oz mb run data get entity @s Pos[2] 1000
execute store result score @s mbHzFX run data get entity @e[type=minecraft:marker,tag=rlk_mb_hzax,limit=1] Pos[0] 1000
execute store result score @s mbHzFZ run data get entity @e[type=minecraft:marker,tag=rlk_mb_hzax,limit=1] Pos[2] 1000
scoreboard players operation @s mbHzFX -= #ox mb
scoreboard players operation @s mbHzFZ -= #oz mb
kill @e[type=minecraft:marker,tag=rlk_mb_hzax]
''')
w('hz/resize', '''
# Change a live hazard's size (@s = its marker), tenths of a block: {r, r0} = outer / inner radius of a disc, ring,
# sector or full (r0 = the safe hole) or the length / back of a line, {w} = the width of a line (0 = keep). The
# hit bounds are recomputed with the 0.3 b body pad (as hz/init). Meant for #hzQuiet hazards whose visual the module
# draws (the framework outline of a loud one is redrawn too). Score form without a macro: set #hzSzR #hzSzR0
# #hzSzW mb and call hz/resize_s (an expanding wave front calls it every tick).
$scoreboard players set #hzSzR mb $(r)
$scoreboard players set #hzSzR0 mb $(r0)
$scoreboard players set #hzSzW mb $(w)
function rlk:mboss/hz/resize_s
''')
w('hz/resize_s', '''
# @s = live hazard marker; #hzSzR / #hzSzR0 / #hzSzW mb in tenths (see hz/resize). r is clamped to 0..40 b (the
# squared bounds stay inside 32 bits).
execute if score #hzSzR mb matches ..-1 run scoreboard players set #hzSzR mb 0
execute if score #hzSzR mb matches 401.. run scoreboard players set #hzSzR mb 400
scoreboard players operation @s mbHzR = #hzSzR mb
scoreboard players operation @s mbHzR *= #c100 mb
scoreboard players operation @s mbHzR0 = #hzSzR0 mb
scoreboard players operation @s mbHzR0 *= #c100 mb
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/resize_line
execute unless score @s mbHzK matches 4 run function rlk:mboss/hz/resize_rad
execute unless entity @s[tag=rlk_mb_hzq] run function rlk:mboss/hz/init_draw
''')
w('hz/resize_rad', '''
execute if score @s mbHzR0 matches ..-1 run scoreboard players set @s mbHzR0 0
scoreboard players operation #t mb = @s mbHzR
scoreboard players add #t mb 300
scoreboard players operation @s mbHzRR = #t mb
scoreboard players operation @s mbHzRR *= #t mb
scoreboard players operation #t mb = @s mbHzR0
scoreboard players remove #t mb 300
execute if score #t mb matches ..-1 run scoreboard players set #t mb 0
scoreboard players operation @s mbHzRI = #t mb
scoreboard players operation @s mbHzRI *= #t mb
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI = @s mbHzR0
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI *= @s mbHzR0
''')
w('hz/resize_line', '''
# len = mbHzR, back = mbHzR0, width #hzSzW (tenths, 0 = keep): as hz/init_line.
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzHW = #hzSzW mb
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzHW *= #c100 mb
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzHW /= #c2 mb
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzC = @s mbHzHW
execute if score #hzSzW mb matches 1.. run scoreboard players add @s mbHzHW 300
scoreboard players operation @s mbHzLo = @s mbHzR0
scoreboard players operation @s mbHzLo *= #cm1 mb
scoreboard players remove @s mbHzLo 300
scoreboard players operation @s mbHzHi = @s mbHzR
scoreboard players add @s mbHzHi 300
''')
w('hz/cancel', '''
# Cancels the hazard with id #hzLast mb (or any: set #hzLast mb before the call). Module visuals get event 2.
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb at @s rotated as @s run function rlk:mboss/hz/expire
''')

# Baked particle primitives (macro: col, sc). ^x = left, ^z = forward, relative to the caller.
def ppart(x, z, gate=None):
    line = f'$particle minecraft:dust{{color:$(col),scale:$(sc)}} ^{L.num(x, 3)} ^0.12 ^{L.num(z, 3)} 0 0 0 0 1 force @a[tag=player]'
    if gate is not None:
        line = f'$execute if score #hzAng mb matches {gate}.. run ' + line[1:]
    return line


for k in range(1, 61):
    r = k / 2
    n = max(12, math.ceil(2 * math.pi * r / (0.8 + 0.01 * r)))
    lines = [f'# Circle r {L.num(r)} ({n} points); a point at angle t from forward needs #hzAng >= |t|.']
    for i in range(n):
        t = -180 + 360 * i / n
        lines.append(ppart(r * math.sin(math.radians(t)), r * math.cos(math.radians(t)), math.ceil(abs(t) - 1e-6)))
    out.write(f'mboss/hz/p/c/{k}', '\n'.join(lines))
for k in range(1, 91):
    ln = k / 2
    n = max(2, math.ceil(ln / 0.7))
    out.write(f'mboss/hz/p/r/{k}', '\n'.join([f'# Ray forward 0..{L.num(ln)}'] + [ppart(0, ln * i / n) for i in range(n + 1)]))
for k in range(1, 41):
    wd = k / 2
    n = max(2, math.ceil(wd / 0.6))
    out.write(f'mboss/hz/p/b/{k}', '\n'.join([f'# Cross bar width {L.num(wd)}'] + [ppart(-wd / 2 + wd * i / n, 0) for i in range(n + 1)]))

# =============================================================================================
# Projectile props (pj)
w('pj/launch', '''
# @s = a prop entity the module summoned (item/block display, marker ...), positioned at the launch point,
# rotated = flight direction (pitch counts). {spd: tenths per tick, life: ticks, dmg: % of the base hit
# (0 = visual only), hr: hit radius in tenths}. Options: #pjEl, #pjKB, #pjRet (1 = fly back to the body's
# eyes at the end), #pjWall (0 = ignore walls), #pjShape (0 sphere of radius hr; 1 blade: a line hr wide on
# each side across the flight, see pj/b/*), #pjGrp (volley group id from mboss/grp_new: the first hit that lands
# makes every prop and hazard of the group harmless). Steering: mboss/pj/steer. Events go to the module hook pj_end with #pjEv 1 wall,
# 2 life over, 3 back at the body (or the return time ran out), 4 hit the player; #pjKeep mb is preset to
# the default and the hook may flip it: 1 = the prop lives on (4: keeps flying, it pierces; 1/2 of a
# returning prop: flies back; otherwise released as a plain entity), 0 = removed at once.
# Refused while the boss is dying (#mbSt 2): the prop is removed.
execute if score #mbSt mb matches 2 run function rlk:mboss/opts_reset
execute if score #mbSt mb matches 2 run return run kill @s
scoreboard players set #mbPjOn mb 1
tag @s add rlk_mb_pj
tag @s add rlk_mb_aux
tag @s add rlk_room
$scoreboard players set @s mbPjV $(spd)
$scoreboard players set @s mbPjL $(life)
$scoreboard players set @s mbPjD $(dmg)
$scoreboard players set @s mbPjR $(hr)
scoreboard players set @s mbPjT 0
scoreboard players set @s mbPjHit 0
scoreboard players operation @s mbPjE = #mbEl mb
execute if score #pjEl mb matches 0.. run scoreboard players operation @s mbPjE = #pjEl mb
scoreboard players operation @s mbPjB = #pjKB mb
scoreboard players operation @s mbPjRet = #pjRet mb
scoreboard players operation @s mbPjW = #pjWall mb
scoreboard players operation @s mbPjK = #pjShape mb
scoreboard players operation @s mbPjG = #pjGrp mb
execute if score @s mbPjR matches 41.. run scoreboard players set @s mbPjR 40
execute if score @s mbPjR matches ..0 run scoreboard players set @s mbPjR 1
tp @s ~ ~ ~ ~ ~
function rlk:mboss/opts_reset
''')
w('pj/tick', '''
# @s = prop, at/rotated as @s. Moves in 0.25-block sub-steps (speed rounded up to 0.25 b/t).
scoreboard players set #mbPjOn mb 1
scoreboard players add @s mbPjT 1
execute if score @s mbPjRet matches 2 run return run function rlk:mboss/pj/back
execute if score @s mbPjT > @s mbPjL run return run function rlk:mboss/pj/stop {ev:2}
scoreboard players operation #pjN mb = @s mbPjV
scoreboard players operation #pjN mb *= #c4 mb
scoreboard players add #pjN mb 9
scoreboard players operation #pjN mb /= #c10 mb
execute if score #pjN mb matches ..0 run scoreboard players set #pjN mb 1
scoreboard players set #pjStop mb 0
execute store result storage rlk:mboss pjp.hr int 1 run scoreboard players get @s mbPjR
function rlk:mboss/pj/step
execute if score #pjStop mb matches 1 run function rlk:mboss/pj/stop {ev:1}
# The hook ended the flight on a player hit (#pjKeep 0 at event 4).
execute if score #pjStop mb matches 2 run kill @s
''')
w('pj/step', '''
execute if score @s mbPjW matches 1 unless block ^ ^ ^0.25 #rlk:cm_pass run return run scoreboard players set #pjStop mb 1
tp @s ^ ^ ^0.25
execute if score @s mbPjHit matches 0 if score @s mbPjD matches 1.. if score @s mbPjK matches 1 at @s run function rlk:mboss/pj/br with storage rlk:mboss pjp
execute if score @s mbPjHit matches 0 if score @s mbPjD matches 1.. unless score @s mbPjK matches 1 at @s run function rlk:mboss/pj/hr with storage rlk:mboss pjp
execute if score #pjStop mb matches 2 run return 0
scoreboard players remove #pjN mb 1
execute if score #pjN mb matches 1.. at @s rotated as @s run function rlk:mboss/pj/step
''')
w('pj/hr', '$function rlk:mboss/pj/h/$(hr)')
for k in range(1, 41):
    out.write(f'mboss/pj/h/{k}', f'# Hit radius {L.num(k / 10)} b (+0.3 body), measured 0.9 b below the prop.\n'
              f'execute positioned ~ ~-0.9 ~ if entity @e[tag=rlk_body,distance=..{L.num(k / 10 + 0.3)},limit=1] run function rlk:mboss/pj/hit')
w('pj/br', '$function rlk:mboss/pj/b/$(hr)')
# Blade hit shape (#pjShape 1): a line across the flight direction, hr tenths on each side, sampled by points at
# most 0.8 b apart, in two rows (0.9 b below the prop = the sphere test's point, and 0.3 b above the prop, so a
# jumping player is caught too), each a 0.65 b sphere against the player's feet. Swept by the 0.25 b sub-steps.
BLADE_R = 0.65
for k in range(1, 41):
    hw = k / 10
    n = max(1, math.ceil(2 * hw / 0.8))
    xs = [-hw + 2 * hw * i / n for i in range(n + 1)]
    lines = [f'# Blade half width {L.num(hw)} b: {len(xs)} points x 2 rows, radius {L.num(BLADE_R)} b (@s = prop, at and rotated as it).']
    for dy in (-0.9, 0.3):
        for x in xs:
            lines.append(f'execute positioned ^{L.num(x, 3)} ^{L.num(dy)} ^ if entity @e[tag=rlk_body,distance=..{L.num(BLADE_R)},limit=1] '
                         'run return run function rlk:mboss/pj/hit')
    out.write(f'mboss/pj/b/{k}', '\n'.join(lines))
w('grp_new', '''
# A new volley group id in #mbGrp mb (never 0). Before each hz/pj create of the volley copy it into the one-shot
# option: scoreboard players operation #hzGrp mb = #mbGrp mb (or #pjGrp). The first hit of the group that lands
# (not dodged) makes every other live hazard and prop of the group harmless (mboss/grp_mark).
scoreboard players add #mbGrpN mb 1
execute if score #mbGrpN mb matches 1000000.. run scoreboard players set #mbGrpN mb 1
scoreboard players operation #mbGrp mb = #mbGrpN mb
''')
w('grp_mark', '''
# #g mb = a volley group that just landed a hit: its hazards and props stop testing for hits (the strike
# visuals and the flights go on).
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzG = #g mb run scoreboard players set @s mbHzHit 1
# #hzRearm members of the group re-arm together (one hit per re-arm period for the whole group)
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzG = #g mb if score @s mbHzRA matches 1.. run function rlk:mboss/hz/rearm_at
execute as @e[tag=rlk_mb_pj] if score @s mbPjG = #g mb run scoreboard players set @s mbPjHit 1
''')
w('pj/steer', '''
# Homing (@s = a live prop, at @s; from the module tick, which runs before pj/all moves the props): turn the
# flight direction toward the player's chest (body feet + 0.9 b, so the hit point 0.9 b below the prop meets the
# feet) by at most $(max) degrees in yaw and in pitch this tick; the pitch stays within +-60 degrees.
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute store result score #y0 mb run data get entity @s Rotation[0] 100
execute store result score #p0 mb run data get entity @s Rotation[1] 100
kill @e[type=minecraft:marker,tag=rlk_mb_help]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~0.9 ~ {Tags:["rlk_mb_help"]}
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] feet run tp @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] ~ ~ ~ ~ ~
execute store result score #y1 mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] Rotation[0] 100
execute store result score #p1 mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_help,limit=1] Rotation[1] 100
kill @e[type=minecraft:marker,tag=rlk_mb_help]
scoreboard players operation #y1 mb -= #y0 mb
scoreboard players add #y1 mb 90000
scoreboard players operation #y1 mb %= #c36000 mb
scoreboard players remove #y1 mb 18000
scoreboard players operation #p1 mb -= #p0 mb
$scoreboard players set #m mb $(max)
scoreboard players operation #m mb *= #c100 mb
scoreboard players operation #y1 mb < #m mb
scoreboard players operation #p1 mb < #m mb
scoreboard players operation #m mb *= #cm1 mb
scoreboard players operation #y1 mb > #m mb
scoreboard players operation #p1 mb > #m mb
scoreboard players operation #y0 mb += #y1 mb
scoreboard players operation #p0 mb += #p1 mb
scoreboard players set #m mb 6000
scoreboard players operation #p0 mb < #m mb
scoreboard players set #m mb -6000
scoreboard players operation #p0 mb > #m mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #y0 mb
execute store result entity @s Rotation[1] float 0.01 run scoreboard players get #p0 mb
''')
w('pj/hit', '''
# One hit per prop. Event 4 with #pjKeep 1 preset (the prop pierces and flies on, harmless from now);
# the hook sets #pjKeep mb 0 to end the flight here (pj/tick removes the prop after this sub-step).
scoreboard players set @s mbPjHit 1
scoreboard players operation #mbHitPct mb = @s mbPjD
scoreboard players operation #cmEl tmp = @s mbPjE
scoreboard players operation #mbKB mb = @s mbPjB
scoreboard players set #mbKBDir mb 1
function rlk:mboss/hurt
scoreboard players operation #g mb = @s mbPjG
execute if score #dodged tmp matches 0 if score #g mb matches 1.. run function rlk:mboss/grp_mark
scoreboard players set #pjEv mb 4
scoreboard players set #pjKeep mb 1
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 0 run scoreboard players set #pjStop mb 2
''')
w('pj/stop', '''
# End of the outward flight (ev 1 wall, 2 life over). A returning prop reports it and turns around.
$scoreboard players set #pjEv mb $(ev)
execute if score @s mbPjRet matches 1 run return run function rlk:mboss/pj/turn
function rlk:mboss/pj/finish
''')
w('pj/turn', '''
# Returning prop at the end of its outward flight: event 1/2 with #pjKeep 1 preset (fly back); 0 = removed.
# The return leg may last as long as the outward flight plus 2 s (mbPjL = 2 x elapsed + 40), then it
# ends with event 3 wherever the prop is (the body may have moved away faster than the prop flies).
scoreboard players set #pjKeep mb 1
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 0 run return run kill @s
scoreboard players set @s mbPjRet 2
scoreboard players operation @s mbPjL = @s mbPjT
scoreboard players operation @s mbPjL += @s mbPjT
scoreboard players add @s mbPjL 40
''')
w('pj/finish', '''
# Event 1/2 (non-returning) or 3 with #pjKeep 0 preset: removed unless the hook keeps it (released).
scoreboard players set #pjKeep mb 0
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 1 run return run function rlk:mboss/pj/release
kill @s
''')
w('pj/release', '''
# The module keeps the prop: it stops being a projectile.
tag @s remove rlk_mb_pj
scoreboard players reset @s mbPjV
scoreboard players reset @s mbPjRet
''')
w('pj/back', '''
# Return leg: steer at the body's eyes (facing entity .. eyes); arrived = the prop touches the body's hitbox
# (a 1-block cube around the prop intersects it; the eye point lies inside the hitbox at any scale). A
# moving body can outrun the prop, so the time cap from pj/turn ends the leg with event 3 anyway.
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run return run kill @s
execute if score @s mbPjT > @s mbPjL run return run function rlk:mboss/pj/returned
scoreboard players operation #pjN mb = @s mbPjV
scoreboard players operation #pjN mb *= #c4 mb
scoreboard players add #pjN mb 9
scoreboard players operation #pjN mb /= #c10 mb
execute if score #pjN mb matches ..0 run scoreboard players set #pjN mb 1
function rlk:mboss/pj/back_step
''')
w('pj/back_step', '''
execute at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes run tp @s ^ ^ ^0.25 ~ ~
# Not 'at <body> anchored eyes': that anchor uses the EXECUTOR's eye height (0 for a display or marker).
execute at @s positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[type=minecraft:husk,tag=rlk_mb_body,dx=0,dy=0,dz=0,limit=1] run return run function rlk:mboss/pj/returned
scoreboard players remove #pjN mb 1
execute if score #pjN mb matches 1.. run function rlk:mboss/pj/back_step
''')
w('pj/returned', '''
scoreboard players set #pjEv mb 3
function rlk:mboss/pj/finish
''')

# =============================================================================================
# Pull to a point (undodgeable, keeps the dead/revival/selection/map refusals)
w('pull/start', '''
# Pull the player's body to the execution position over t ticks (t 0 = at once), as anything, positioned at
# the destination (e.g. 1.2 b in front of the boss). Dash i-frames do not stop it; dead / revival / selection
# screen / map view / a dying boss refuse it (returns fail). Option #pullFace mb 1 (default): turn the player to
# the boss.
scoreboard players operation #plFace mb = #pullFace mb
scoreboard players set #pullFace mb 1
execute if score #mbSt mb matches 2 run return fail
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return fail
execute if entity @a[tag=player,scores={rnDie=1..}] run return fail
execute if entity @a[tag=player,scores={pkMode=1..}] run return fail
execute if entity @a[tag=player,scores={vMap=1}] run return fail
kill @e[tag=rlk_mb_pullpt]
kill @e[tag=rlk_plkb]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_pullpt","rlk_mb_aux","rlk_room"]}
scoreboard players set #mbPlOn mb 1
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_pullpt,limit=1] mbPlT $(t)
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_pullpt,limit=1] mbPlF = #plFace mb
execute as @a[tag=player,limit=1] run scoreboard players set @s stepT 0
execute if entity @e[tag=rlk_av,limit=1] as @a[tag=player,limit=1] run function rlk:view/stop_h
execute as @e[tag=rlk_mb_pullpt,limit=1] if score @s mbPlT matches ..0 at @s run function rlk:mboss/pull/finish
return 1
''')
w('pull/tick', '''
# @s = pull point, at @s. Glide: body += (point - body) / ticks left, collision-checked like knockback.
scoreboard players set #mbPlOn mb 1
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run kill @s
execute if entity @a[tag=player,scores={rnDie=1..}] run return run kill @s
execute if entity @a[tag=player,scores={pkMode=1..}] run return run kill @s
execute if entity @a[tag=player,scores={vMap=1}] run return run kill @s
execute unless entity @e[tag=rlk_body,limit=1] run return run kill @s
execute if score @s mbPlT matches ..1 run return run function rlk:mboss/pull/finish
execute store result score #bx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #by mb run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #bz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #px mb run data get entity @s Pos[0] 1000
execute store result score #py mb run data get entity @s Pos[1] 1000
execute store result score #pz mb run data get entity @s Pos[2] 1000
scoreboard players operation #px mb -= #bx mb
scoreboard players operation #px mb /= @s mbPlT
scoreboard players operation #px mb += #bx mb
scoreboard players operation #py mb -= #by mb
scoreboard players operation #py mb /= @s mbPlT
scoreboard players operation #py mb += #by mb
scoreboard players operation #pz mb -= #bz mb
scoreboard players operation #pz mb /= @s mbPlT
scoreboard players operation #pz mb += #bz mb
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[0] double 0.001 run scoreboard players get #px mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[1] double 0.001 run scoreboard players get #py mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[2] double 0.001 run scoreboard players get #pz mb
scoreboard players set #pkbBlocked tmp 0
execute at @e[tag=rlk_mb_help,limit=1] run function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 0 at @e[tag=rlk_mb_help,limit=1] run tp @e[tag=rlk_body,limit=1] ~ ~ ~
kill @e[tag=rlk_mb_help]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:reverse_portal ~ ~1 ~ 0.2 0.4 0.2 0.05 4 force @a[tag=player]
scoreboard players remove @s mbPlT 1
''')
w('pull/finish', '''
scoreboard players set #pkbBlocked tmp 0
function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 0 run tp @e[tag=rlk_body,limit=1] ~ ~ ~
execute if score @s mbPlF matches 1 if entity @e[tag=rlk_mb_body,limit=1] as @a[tag=player,limit=1] run rotate @s facing entity @e[tag=rlk_mb_body,limit=1] eyes
kill @s
''')

# =============================================================================================
# Movement (mv): per-entity glides/leaps, facing, steps with the arena clamp, leash, distance
w('mv/glide', '''
# @s = entity to move (body, prop, aux), positioned at the destination: straight glide over t ticks.
function rlk:mboss/mv/setup
$scoreboard players set @s mbMvN $(t)
scoreboard players set @s mbMvH 0
''')
w('mv/leap', '''
# Like glide, with a parabolic arc of apex h (tenths of a block above the straight path).
function rlk:mboss/mv/setup
$scoreboard players set @s mbMvN $(t)
$scoreboard players set @s mbMvH $(h)
scoreboard players operation @s mbMvH *= #c100 mb
''')
w('mv/setup', '''
scoreboard players set #mbMvOn mb 1
tag @s add rlk_mb_mv
scoreboard players set @s mbMvK 1
scoreboard players set @s mbMvT 0
execute store result score @s mbMvX0 run data get entity @s Pos[0] 1000
execute store result score @s mbMvY0 run data get entity @s Pos[1] 1000
execute store result score @s mbMvZ0 run data get entity @s Pos[2] 1000
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute store result score @s mbMvX1 run data get entity @e[tag=rlk_mb_help,limit=1] Pos[0] 1000
execute store result score @s mbMvY1 run data get entity @e[tag=rlk_mb_help,limit=1] Pos[1] 1000
execute store result score @s mbMvZ1 run data get entity @e[tag=rlk_mb_help,limit=1] Pos[2] 1000
kill @e[tag=rlk_mb_help]
''')
w('mv/tick', '''
# @s = moving entity (world tick, before the body tick so the module sees the new position).
scoreboard players set #mbMvOn mb 1
execute unless score @s mbMvN matches 1.. run return run function rlk:mboss/mv/stop
scoreboard players add @s mbMvT 1
scoreboard players operation #x mb = @s mbMvX1
scoreboard players operation #x mb -= @s mbMvX0
scoreboard players operation #x mb *= @s mbMvT
scoreboard players operation #x mb /= @s mbMvN
scoreboard players operation #x mb += @s mbMvX0
scoreboard players operation #y mb = @s mbMvY1
scoreboard players operation #y mb -= @s mbMvY0
scoreboard players operation #y mb *= @s mbMvT
scoreboard players operation #y mb /= @s mbMvN
scoreboard players operation #y mb += @s mbMvY0
scoreboard players operation #z mb = @s mbMvZ1
scoreboard players operation #z mb -= @s mbMvZ0
scoreboard players operation #z mb *= @s mbMvT
scoreboard players operation #z mb /= @s mbMvN
scoreboard players operation #z mb += @s mbMvZ0
execute if score @s mbMvH matches 1.. run function rlk:mboss/mv/arc
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[0] double 0.001 run scoreboard players get #x mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[1] double 0.001 run scoreboard players get #y mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[2] double 0.001 run scoreboard players get #z mb
execute at @e[tag=rlk_mb_help,limit=1] run tp @s ~ ~ ~
kill @e[tag=rlk_mb_help]
execute if score @s mbMvT >= @s mbMvN run function rlk:mboss/mv/stop
''')
w('mv/arc', '''
# y += 4 h t (n - t) / n^2
scoreboard players operation #a mb = @s mbMvN
scoreboard players operation #a mb -= @s mbMvT
scoreboard players operation #a mb *= @s mbMvT
scoreboard players operation #a mb *= #c4 mb
scoreboard players operation #n2 mb = @s mbMvN
scoreboard players operation #n2 mb *= @s mbMvN
scoreboard players operation #h mb = @s mbMvH
scoreboard players operation #h mb *= #a mb
scoreboard players operation #h mb /= #n2 mb
scoreboard players operation #y mb += #h mb
''')
w('mv/stop', '''
tag @s remove rlk_mb_mv
scoreboard players set @s mbMvK 0
scoreboard players set @s mbMvN 0
''')
w('mv/face', '''
# @s turns (yaw only) toward the player's body at once.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
''')
w('mv/turn', '''
# @s turns toward the player's body by at most {max} degrees this tick (smooth tracking).
execute store result score #y0 mb run data get entity @s Rotation[0] 100
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_mb_help,limit=1] ~ ~ ~ ~ 0
execute store result score #y1 mb run data get entity @e[tag=rlk_mb_help,limit=1] Rotation[0] 100
kill @e[tag=rlk_mb_help]
scoreboard players operation #y1 mb -= #y0 mb
scoreboard players add #y1 mb 90000
scoreboard players operation #y1 mb %= #c36000 mb
scoreboard players remove #y1 mb 18000
$scoreboard players set #m mb $(max)
scoreboard players operation #m mb *= #c100 mb
execute if score #y1 mb > #m mb run scoreboard players operation #y1 mb = #m mb
scoreboard players operation #m mb *= #cm1 mb
execute if score #y1 mb < #m mb run scoreboard players operation #y1 mb = #m mb
scoreboard players operation #y0 mb += #y1 mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #y0 mb
data modify entity @s Rotation[1] set value 0.0f
''')
w('mv/ok', '''
# At a proposed feet position: inside the safe disc (@SAFEP@ b from the axis) with free feet and head.
execute positioned ~ @CY@ ~ unless entity @e[tag=rlk_mb_arena,distance=..@SAFEP@,limit=1] run return fail
execute unless block ~ ~ ~ #rlk:dash_pass run return fail
execute unless block ~ ~1 ~ #rlk:dash_pass run return fail
return 1
''')
w('mv/step', '''
# @s steps {d} blocks forward (decimal, e.g. {d:0.4}) when the spot is free and inside the safe disc.
$execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/mv/ok run tp @s ~ ~ ~
''')
w('mv/toward', '''
# @s steps {d} blocks toward the player's body (no turn), same checks as step.
$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/mv/ok run tp @s ~ ~ ~
''')
w('mv/away', '''
$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^$(d) if function rlk:mboss/mv/ok run tp @s ~ ~ ~
''')
w('mv/leash', '''
# @s = body (automatic every fight tick unless #mbNoLeash mb 1). Beyond @SAFE1@ b from the axis: slide back
# 0.45 b/t; beyond @WALK2@ b: back to the centre at once.
execute at @s positioned ~ @CY@ ~ if entity @e[tag=rlk_mb_arena,distance=..@SAFE1@,limit=1] run return 0
execute at @s positioned ~ @CY@ ~ unless entity @e[tag=rlk_mb_arena,distance=..@WALK2@,limit=1] run return run function rlk:mboss/mv/home
execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
''')
w('mv/home', '''
execute at @e[tag=rlk_mb_arena,limit=1] run tp @s ~ ~ ~
execute at @s run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 12 force @a[tag=player]
''')
w('mv/clamp', '''
# @s (e.g. a destination marker) is pulled toward the arena axis until it is inside the safe disc.
scoreboard players set #cl mb 0
function rlk:mboss/mv/clamp_step
''')
w('mv/clamp_step', '''
execute at @s positioned ~ @CY@ ~ if entity @e[tag=rlk_mb_arena,distance=..@SAFEP@,limit=1] run return 0
scoreboard players add #cl mb 1
execute if score #cl mb matches 90.. run return 0
execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~
function rlk:mboss/mv/clamp_step
''')
isqrt = ['# #mbDist mb = horizontal distance @s -> player body in tenths of a block (integer Newton square root).',
         'execute store result score #dx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 10',
         'execute store result score #t mb run data get entity @s Pos[0] 10',
         'scoreboard players operation #dx mb -= #t mb',
         'execute store result score #dz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 10',
         'execute store result score #t mb run data get entity @s Pos[2] 10',
         'scoreboard players operation #dz mb -= #t mb',
         'scoreboard players operation #n mb = #dx mb', 'scoreboard players operation #n mb *= #dx mb',
         'scoreboard players operation #t mb = #dz mb', 'scoreboard players operation #t mb *= #dz mb',
         'scoreboard players operation #n mb += #t mb',
         'scoreboard players set #mbDist mb 0',
         'execute if score #n mb matches ..0 run return 0',
         'execute if score #n mb matches 4000001.. run return run scoreboard players set #mbDist mb 2000',
         'scoreboard players set #mbDist mb 2000']
for _ in range(14):
    isqrt += ['scoreboard players operation #t mb = #n mb', 'scoreboard players operation #t mb /= #mbDist mb',
              'scoreboard players operation #mbDist mb += #t mb', 'scoreboard players operation #mbDist mb /= #c2 mb',
              'execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1']
w('mv/dist', '\n'.join(isqrt))

# =============================================================================================
# Tests
HELP = (TT + gray('명령: ') + ',' + link("/function rlk:mboss/test/start {id:\"proto\"}", 'start {id}') + ',' + gray(' 시험 전투 · ') + ','
        + link("/function rlk:mboss/test/start_ch {id:\"proto\",ch:2}", 'start_ch {id,ch}') + ',' + gray(' 챕터 지정 · ') + ','
        + link('/function rlk:mboss/test/kill', 'kill') + ',' + gray(' 처치(보상) · ') + ','
        + link('/function rlk:mboss/test/abort', 'abort') + ',' + gray(' 취소(보상 없음) · ') + ','
        + link('/function rlk:mboss/test/pattern {id:1}', 'pattern {id}') + ',' + gray(' 다음 패턴 · ') + ','
        + link('/function rlk:mboss/test/lock {id:1}', 'lock {id}') + ',' + gray(' 패턴 고정(0 해제) · ') + ','
        + link('/function rlk:mboss/test/level {lv:10}', 'level {lv}') + ',' + gray(' 레벨 · ') + ','
        + link('/function rlk:mboss/test/stop', 'stop') + ',' + gray(' 종료 후 로비 · ') + ','
        + link('/function rlk:mboss/test/arena', 'arena') + ',' + gray(' 경기장 다시 짓고 보기') + ']')
w('test/help', 'tellraw @s ' + HELP)
w('test/start', '''
# /function rlk:mboss/test/start {id:"proto"}: a real node map (chapter 1, map 2) whose kind-15 zone holds
# that mid-boss; the gate is pressed at once. Exercises roll -> gate -> arena -> fight -> won -> reward.
$function rlk:mboss/test/start_ch {id:"$(id)",ch:1}
''')
w('test/start_ch', TT.join(['''
# /function rlk:mboss/test/start_ch {id:"proto",ch:2}
execute unless entity @s[tag=player] run return run tellraw @s {text:"[중간보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s ''', gray('던전 구역이 준비되지 않았습니다. 먼저 ') + ',' + link('/function rlk:room/setup') + ',' + gray(' 을 실행하세요.') + ''']
execute if score #active room matches 1 unless score #mbTest mb matches 1 run return run tellraw @s ''', gray('진행 중인 런이 있습니다. ') + ',' + link('/function rlk:run/stop') + ',' + gray(' 후 다시 실행하세요.') + ''']
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @s ''', gray("난이도가 '평화로움'이면 중간보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.") + ''']
execute if score @s dead matches 1 run return 0
$execute unless data storage rlk:mboss byid.$(id) run return run tellraw @s ''', gray('등록되지 않았거나 꺼진 중간보스입니다: $(id)') + ''']
$execute store result score #mbForce mb run data get storage rlk:mboss byid.$(id).n
# the boss of this test, for the replay links (test/defeat runs after test/end has forgotten cur)
$data modify storage rlk:mboss tlast set value {id:"$(id)"}
$scoreboard players set #mbReqCh mb $(ch)
execute unless score #mbReqCh mb matches 1.. run scoreboard players set #mbReqCh mb 1
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #mbTest mb 1
scoreboard players set #mbLock mb 0
scoreboard players set #active room 1
scoreboard players operation #chapter room = #mbReqCh mb
scoreboard players set #mapIdx room 2
scoreboard players set #mapType room 1
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
data modify storage rlk:room next set value [15]
data modify storage rlk:mboss met set value []
execute in minecraft:overworld run function rlk:room/gen
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=15,zst=0}] run function rlk:room/zone_build
execute in minecraft:overworld at @e[tag=rlk_zone,scores={zkind=15},limit=1] run tp @s ~ ~ ~ 180 0
function rlk:view/sync
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=15,zst=1}] at @s run function rlk:room/zone_enter
execute in minecraft:overworld as @e[tag=rlk_obj,scores={oact=14},limit=1] at @s run function rlk:mboss/gate
scoreboard players operation @s curHealth = @s maxHealth
tellraw @s ''', gray('중간보스 시험 전투를 시작합니다. 1.5초 뒤 경기장으로 이동합니다.') + ''']
function rlk:mboss/test/help
''']))
w('test/kill', TT.join(['''
# Lethal true hit through combat/apply: pays like a real kill (reward path).
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s ''', gray('진행 중인 중간보스가 없습니다.') + ''']
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
execute as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/test/kill_do
''']))
w('test/kill_do', '''
scoreboard players operation #mbTrue mb = @s mhpC
scoreboard players set #mbTrueEl mb 0
function rlk:mboss/true_hit
''')
w('test/abort', TT.join(['''
# Removes the body without a kill: the zone clears and mboss/won cancels (no reward, gate back).
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s ''', gray('진행 중인 중간보스가 없습니다.') + ''']
kill @e[tag=rlk_mb_body]
execute unless score #combat room matches 1.. run function rlk:mboss/cleanup
tellraw @s ''', gray('중간보스를 보상 없이 없앴습니다(취소 경로).') + ''']
''']))
w('test/pattern', TT.join(['''
# Module test hook (rlk:mboss/<id>/test {id:N}); the meaning of N belongs to the module.
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s ''', gray('진행 중인 중간보스가 없습니다.') + ''']
$function rlk:mboss/d/test {id:$(id)}
$tellraw @s ''', gray('다음 패턴 요청: $(id)') + ''']
''']))
w('test/lock', TT.join(['''
# #mbLock mb = N: the module repeats pattern N (0 unlocks). Modules read it in their pattern choice.
$scoreboard players set #mbLock mb $(id)
$tellraw @s ''', gray('패턴 고정: $(id) (0 = 해제)') + ''']
''']))
w('test/level', TT.join(['''
$scoreboard players set #mbReq mb $(lv)
execute unless score #mbReq mb matches 1..999 run return run tellraw @s ''', gray('레벨은 1 이상이어야 합니다.') + ''']
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s ''', gray('진행 중인 중간보스가 없습니다.') + ''']
execute as @e[tag=rlk_mb_body,limit=1] run scoreboard players operation @s mlv = #mbReq mb
execute as @e[tag=rlk_mb_body,limit=1] run function rlk:mob/level_apply
scoreboard players operation #mbLv mb = #mbReq mb
tellraw @s ''', gray('중간보스 레벨을 바꾸고 체력을 다시 채웠습니다.') + ''']
''']))
w('test/stop', TT.join(['''
execute unless score #mbTest mb matches 1 run return run tellraw @s ''', gray('진행 중인 중간보스 테스트가 없습니다.') + ''']
function rlk:mboss/test/end
tellraw @a[tag=player] ''', gray('중간보스 테스트를 끝내고 로비로 돌아왔습니다.') + ''']
''']))
w('test/end', '''
scoreboard players set #mbTest mb 0
scoreboard players set #mbForce mb 0
scoreboard players set #mbLock mb 0
function rlk:run/end
function rlk:mboss/cleanup
execute as @a[tag=player] run function rlk:lobby/go
''')
w('test/defeat', '''
# From player/hook_respawn during a test: never fails/resets the character. The replay link restarts the boss of
# this test (rlk:mboss tlast, saved by test/start_ch; cur is forgotten by test/end).
execute unless data storage rlk:mboss tlast.id run data modify storage rlk:mboss tlast set value {id:"proto"}
execute if data storage rlk:mboss cur.id run data modify storage rlk:mboss tlast.id set from storage rlk:mboss cur.id
function rlk:mboss/test/end
title @s times 10 40 15
title @s subtitle {text:"로비로 돌아왔습니다",color:"gray"}
title @s title {text:"중간보스 테스트 실패",color:"#E06A5A",bold:true}
scoreboard players set @s vBig 65
scoreboard players set @s ttlT 65
function rlk:mboss/test/defeat_msg with storage rlk:mboss tlast
''')
w('test/defeat_msg', '$tellraw @s ' + TT + gray('쓰러졌습니다. ') + ',' + link('/function rlk:mboss/test/start {id:"$(id)"}', '[다시 하기]') + ']')
WON_REPLAY = link('/function rlk:mboss/test/start {id:"$(id)"}', '[다시 하기]')
w('test/won', '\n'.join([
    '# From mboss/won during a test (with storage rlk:mboss cur).',
    '$execute if score #mbKilled mb matches 1 run tellraw @a[tag=player] ' + TT + gray('처치! 문 자리에 아이템 상자가 떨어졌습니다(누르면 아이템 선택). ') + ',' + WON_REPLAY
    + ',' + gray(' ') + ',' + link('/function rlk:mboss/test/stop', '[로비로]') + ']',
    'execute unless score #mbKilled mb matches 1 run tellraw @a[tag=player] ' + TT + gray('취소되었습니다(보상 없음). ') + ','
    + link('/function rlk:mboss/test/stop', '[로비로]') + ']']))
w('test/arena', TT.join(['''
# Rebuild the arena and look at it (outside a run). Back: /function rlk:lobby/go
execute if score #active room matches 1 run return run tellraw @s ''', gray('런 중에는 쓸 수 없습니다.') + ''']
execute in minecraft:overworld run function rlk:mboss/arena/rebuild
execute in minecraft:overworld run tp @s @CX@.5 @CY@ @CZ@.5 180 0
function rlk:view/sync
tellraw @s ''', gray('경기장을 다시 지었습니다. 돌아가기: ') + ',' + link('/function rlk:lobby/go') + ']']))

# Stale top-level framework files: every F:mboss/*.mcfunction belongs to this generator
# (modules live in F:mboss/<id>/, the arena in F:mboss/arena/).
for p in sorted(L.MB.glob('*.mcfunction')):
    if p.stem not in CORE_TOP:
        p.unlink()
removed = out.clean()
print(f'mboss core: {len(out.written)} functions, {len(BOSSES)} registered mid-bosses '
      f'({", ".join(b["id"] for b in BOSSES)}), {removed} stale removed.')
