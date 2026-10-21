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
import json
import math
import mboss_lib as L

REG = L.load_registry()
A = REG['arena']
# Every enabled entry (hook dispatchers); mid-boss entries (reg[], the roll); chapter bosses (creg[], AZ-CM).
BOSSES = L.enabled_bosses(REG)
MIDS = L.mid_bosses(REG)
CHAPS = L.chapter_bosses(REG)
ARENAS = L.arenas(REG)                      # [(aid, arena)] plaza first (n 0), then arenas{} by n
PX_STATES = {}                              # proxy boss id -> [state set names] (filled from the rig manifests, px_build)
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
                        'mboss/line', 'mboss/test', 'mboss/box', 'mboss/cb', 'mboss/ar', 'mboss/px', 'mboss/music',
                        'mboss/push', 'mboss/cine'],
            owned_files=[])
CORE_TOP = set()


def w(name, text):
    if isinstance(text, list):
        text = '\n'.join(text)
    for k, v in TOK.items():
        text = text.replace(k, v)
    if '/' not in name:
        CORE_TOP.add(name)
    out.write('mboss/' + name, text)


T = '[{text:"[중간보스] ",color:"#E0703A",bold:true},'
TT = '[{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},'
CT = '[{text:"[챕터 보스] ",color:"#E0703A",bold:true},'
CTT = '[{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},'


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
    # chapter mode (AZ-CM, scratchpad az/contract/cm.md 4.2): per-element RES, hazard no-reaction / mask safe group,
    # projectile no-dodge / no-reaction, the hit-proxy index
    'mbRes0', 'mbRes1', 'mbRes2', 'mbRes3', 'mbRes4', 'mbRes5', 'mbRes6', 'mbRes7', 'mbRes8',
    'mbHzNR', 'mbHzSG', 'mbPjND', 'mbPjNR', 'mbPart',
    # AP-FW (cm.md 13.11): per-mille hazards (pl_dot per mille, lethal flag)
    'mbHzPm', 'mbHzPmL',
]
OBJECTIVES = ['mb', 'mres', 'pkMb'] + PER_ENTITY

# =============================================================================================
# Registry
def snbt_entry(b):
    ar = L.arena_of(b, REG)
    start = b.get('start', ar['start'])
    picks = int(b.get('picks', 2))
    shield = bool(b.get('shield', not b.get('px', False)))
    hit = b.get('hit', {'w': 1.0, 'h': 1.0})
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
        'hit:{w:%sf,h:%sf}' % (L.num(float(hit['w'])), L.num(float(hit['h']))),
        'start:{x:%sd,y:%sd,z:%sd,yaw:%sf,pitch:%sf}' % tuple(L.num(float(start[k])) for k in ('x', 'y', 'z', 'yaw', 'pitch')),
        f'title:{{text:{s(b["name"])},color:{s(b["color"])},bold:true}}',
        f'gate:{{item:{s(icon["item"])},model:{s(icon["model"])},name:{s(b["name"])},'
        f'desc:{s(("좌클릭으로 도전 · 처치 시 아이템 상자 %d개" % picks) if b.get("kind", "mid") == "mid" else "좌클릭으로 도전 · 챕터 보스")},color:{s(b["color"])}}}',
        # schema v2 (AZ-CM, scratchpad az/contract/cm.md 3.1): every entry, mid-boss defaults. Int lists are plain lists
        # ([1], not [I;1]): the same reads in game, and the offline harness (mcsim) parses SNBT records as JSON.
        f'kind:{s(b.get("kind", "mid"))}', 'ch:[' + ','.join(str(int(c)) for c in b.get('ch', [])) + ']',
        f'route:{1 if b.get("route", True) else 0}b', f'arena:{s(ar["aid"])}', f'ar:{ar["n"]}',
        f'px:{1 if b.get("px") else 0}b', f'pxBase:{int(b.get("pxBase", 65))}', f'shield:{1 if shield else 0}b',
        'phases:[' + ','.join(str(int(p)) for p in b.get('phases', [100])) + ']',
    ]
    if 'res' in b:
        r = b['res']
        parts.append('res:[' + ','.join(str(int(r.get(str(k), r.get('*', 0)))) for k in range(9)) + ']')
    if 'music' in b:
        parts.append('music:{' + ','.join(f'"{ph}":{{ev:{s(m["ev"])},len:{int(m["len"])}}}'
                                          for ph, m in sorted(b['music'].items())) + '}')
    return '{' + ','.join(parts) + '}'


reg_lines = ['# GENERATED by tools/build_mboss_core.py from tools/mboss_registry.json (enabled entries only).',
             '# reg[]: roll candidates and their stats (mid-boss entries only). byid.<id>.n: lookup for test commands.',
             'data modify storage rlk:mboss reg set value [' + ','.join(snbt_entry(b) for b in MIDS) + ']',
             'data modify storage rlk:mboss byid set value {' + ','.join(f'{b["id"]}:{{n:{b["n"]}}}' for b in MIDS) + '}',
             f'scoreboard players set #mbN mb {len(MIDS)}',
             '# Bosses the normal node roll can pick (w >= 1). 0 keeps the 중간보스 node out of the offers.',
             f'scoreboard players set #mbRoll mb {sum(1 for b in MIDS if b["w"] >= 1)}',
             '# Chapter bosses (kind chapter, AZ-CM): creg[] = their records, cbyid.<id> = the full record (cb/start copies it',
             '# into cur). The roll never sees them.',
             'data modify storage rlk:mboss creg set value [' + ','.join(snbt_entry(b) for b in CHAPS) + ']',
             'data modify storage rlk:mboss cbyid set value {' + ','.join(f'{b["id"]}:{snbt_entry(b)}' for b in CHAPS) + '}',
             f'scoreboard players set #mbCN mb {len(CHAPS)}']
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
       'execute unless score #mbCritDmgAdd mb matches -1000.. run scoreboard players set #mbCritDmgAdd mb 0',
       'execute unless score #mbHealEv mb matches 0.. run scoreboard players set #mbHealEv mb 0',
       'execute unless score #mbHealAmt mb matches 0.. run scoreboard players set #mbHealAmt mb 0',
       'execute unless score #mbGrpN mb matches 0.. run scoreboard players set #mbGrpN mb 0',
       'execute unless score #mbGrpL mb matches 0.. run scoreboard players set #mbGrpL mb 0',
       '# Low gravity requested by the running module (#mbLowG 1; mboss/main clears it every tick, the module tick sets it',
       '# again; rlk:tick syncs the attribute modifiers through mboss/lowg_on|off). Hazard re-arm clock (hz/all).',
       'execute unless score #mbLowG mb matches 0..1 run scoreboard players set #mbLowG mb 0',
       'execute unless score #mbHzClk mb matches 0.. run scoreboard players set #mbHzClk mb 0',
       'scoreboard players set #mbNoDodge mb 0',
       '# Chapter mode (AZ-CM): the fight arena (#mbAr = arena n, plaza 0) and its walk / safe radius in tenths, the',
       '# chapter flag, proxies, pools, floor, cine, music, the running arena job (re-armed after /reload).',
       'execute unless score #mbAr mb matches 0.. run scoreboard players set #mbAr mb 0',
       f'execute unless score #mbArW10 mb matches 1.. run scoreboard players set #mbArW10 mb {WALK * 10}',
       f'execute unless score #mbArS10 mb matches 1.. run scoreboard players set #mbArS10 mb {SAFE * 10}',
       'execute unless score #mbMode mb matches 0.. run scoreboard players set #mbMode mb 0',
       'execute unless score #mbPx mb matches 0.. run scoreboard players set #mbPx mb 0',
       'execute unless score #mbPoolPct mb matches 1.. run scoreboard players set #mbPoolPct mb 100',
       'execute unless score #mbRamp mb matches 0.. run scoreboard players set #mbRamp mb 0',
       'execute unless score #mbFloor mb matches 0.. run scoreboard players set #mbFloor mb 0',
       'execute unless score #mbFloorHit mb matches 0.. run scoreboard players set #mbFloorHit mb 0',
       'execute unless score #mbCine mb matches 0.. run scoreboard players set #mbCine mb 0',
       'execute unless score #mbLost mb matches 0.. run scoreboard players set #mbLost mb 0',
       'execute unless score #cbForce mb matches 0.. run scoreboard players set #cbForce mb 0',
       'execute unless score #cbAuto mb matches 0.. run scoreboard players set #cbAuto mb 0',
       'execute unless score #cbWait mb matches 0.. run scoreboard players set #cbWait mb 0',
       'execute unless score #mbMusPh mb matches 0.. run scoreboard players set #mbMusPh mb 0',
       'execute unless score #mbArBuild mb matches 0.. run scoreboard players set #mbArBuild mb 0',
       'execute unless score #mbHitEv mb matches 0.. run scoreboard players set #mbHitEv mb 0',
       'execute unless score #mbDodgeEv mb matches 0.. run scoreboard players set #mbDodgeEv mb 0',
       'execute unless score #mbDodgeOk mb matches 0.. run scoreboard players set #mbDodgeOk mb 0',
       'execute unless score #mbPart mb matches 0.. run scoreboard players set #mbPart mb 0',
       'execute unless score #atkSeq tmp matches -2147483648.. run scoreboard players set #atkSeq tmp 0',
       'scoreboard players set #mbPushOn mb 0',
       'scoreboard players set #mbNRNow mb 0',
       'scoreboard players set #mbNoRx mb 0',
       'scoreboard players set #pxIn mb 0',
       'scoreboard players set #c280 mb 280',
       'execute if score #mbArBuild mb matches 1.. run schedule function rlk:mboss/arena/job_tick 1t replace',
       '# Library activity flags (a set flag makes the world tick scan for that library\'s entities once).',
       'scoreboard players set #mbHzOn mb 1', 'scoreboard players set #mbPjOn mb 1',
       'scoreboard players set #mbPlOn mb 1', 'scoreboard players set #mbMvOn mb 1',
       'function rlk:mboss/opts_reset',
       'function rlk:mboss/bars_hide',
       'scoreboard players set #mbLn mb 0',
       '# Every helper entity dies on reload; a surviving body rebuilds its own (module reload hook).',
       'kill @e[tag=rlk_mb_aux]',
       'kill @e[tag=rlk_mb_arena_prop]',
       'execute as @e[tag=rlk_mb_body] at @s run function rlk:mboss/reload',
       '# The arena is built once the dungeon area is set up (room/setup) and its chunks are loaded.',
       f'execute if data storage rlk:room {{ready:1b}} in minecraft:overworld if loaded {CX} {CY} {CZ} run function rlk:mboss/arena/ensure']))

w('reload', '''
# @s = surviving body after /reload (objectives and the registry are fresh, aux entities are gone).
scoreboard players set #mbLive mb 1
execute if entity @s[tag=rlk_mb_dying] run return run function rlk:mboss/death_finish
execute in minecraft:overworld run function rlk:mboss/ar/marker
scoreboard players set #mbPause mb 0
scoreboard players set #mbNoLeash mb 0
execute unless score #mbId mb matches 1.. run return 0
# hit proxies (rlk_mb_aux: killed by init) come back in their current state set (rlk:mboss px.set)
execute if score #mbPx mb matches 1 run function rlk:mboss/px/spawn
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
# chapter mode: the running arena job, every arena's forceload, the music, chapter storage
function rlk:mboss/arena/abort
schedule clear rlk:mboss/arena/job_tick
function rlk:mboss/music/stop
''' + ''.join(f'execute in minecraft:overworld run function rlk:mboss/ar/{aid}/fl_off\n' for aid, _ in ARENAS if aid != 'plaza') + '''data remove storage rlk:mboss reg
data remove storage rlk:mboss byid
data remove storage rlk:mboss met
data remove storage rlk:mboss tlast
data remove storage rlk:mboss creg
data remove storage rlk:mboss cbyid
data remove storage rlk:mboss cprep
data remove storage rlk:mboss cbpeek
data remove storage rlk:mboss cbl
data remove storage rlk:mboss cbg
data remove storage rlk:mboss tch
data remove storage rlk:mboss pxq
data remove storage rlk:mboss arsw
data remove storage rlk:mboss plp
data remove storage rlk:mboss arjob
''' + ''.join(f'data remove storage rlk:mboss built_{aid}\ndata remove storage rlk:mboss look_{aid}\n' for aid, _ in ARENAS if aid != 'plaza')
  + '\n'.join(f'scoreboard objectives remove {o}' for o in OBJECTIVES))

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
# chapter mode (AZ-CM): no-reaction / mask safe group / projectile no-dodge / per-element aux RES (-1 = none)
scoreboard players set #hzNR mb 0
scoreboard players set #hzSafeG mb 0
scoreboard players set #pjNoDodge mb 0
scoreboard players set #pjNR mb 0
scoreboard players set #auxResEl mb -1
scoreboard players set #auxResElV mb 0
# AP-FW (cm.md 13.11): per-mille hazard option (#hzPmL is spent by hz/init_pm and reset by cleanup_fight)
scoreboard players reset #hzPm mb
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
# Mid-bosses always fight in the plaza (#mbAr 0); chapter bosses start through mboss/cb/start (AZ-CM).
scoreboard players set #mbAr mb 0
execute in minecraft:overworld unless function rlk:mboss/ar/loaded run return run function rlk:mboss/start_unloaded
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run scoreboard players set #spawnT room 10
execute unless data storage rlk:mboss cur run function rlk:mboss/roll
execute unless data storage rlk:mboss cur run return run function rlk:mboss/start_fail
function rlk:mboss/start_go
''')
w('start_go', '''
# The shared start body (@s = the zone marker, at @s; cur is set): mboss/start (mid-boss, plaza) and mboss/cb/start
# (chapter boss, its own arena, already built: arena ensure reported 1). fight_vars sets #mbMode and #mbAr from cur.
scoreboard players set #mbLd mb 0
# From here on fight entities may exist: rlk:tick runs mboss/main (cleared when the body is gone).
scoreboard players set #mbLive mb 1
function rlk:mboss/cleanup_aux
function rlk:mboss/fight_vars
execute if score #mbMode mb matches 0 in minecraft:overworld run function rlk:mboss/arena/ensure
execute in minecraft:overworld run function rlk:mboss/ar/marker
execute in minecraft:overworld as @e[tag=rlk_mb_arena,limit=1] at @s rotated as @s run function rlk:mboss/d/spawn
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run function rlk:mboss/start_fail
scoreboard players set #mbFail mb 0
scoreboard players set #cbWait mb 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/start_body
function rlk:mboss/ret_save
scoreboard players operation #mbLv mb = @e[tag=rlk_mb_body,limit=1] mlv
execute if score #mbMode mb matches 0 run data modify storage rlk:mboss met append from storage rlk:mboss cur.id
scoreboard players set #mbOn mb 1
scoreboard players set #mbSt mb 0
scoreboard players set #mbT mb 0
execute as @a[tag=player,limit=1] run function rlk:mboss/tp_in
function rlk:mboss/bars_show
''')
w('start_body', '''
# @s = the new body, at @s (start_go, right after the spawn hook): #mbTot = its full max HP; chapter bosses: the first
# pool split (cur.phases[0] < 100) and the hit proxies (state inv until the module's intro ends).
scoreboard players operation #mbTot mb = @s mhpM
scoreboard players set #mbPoolPct mb 100
execute unless score #mbMode mb matches 1 run return 0
execute store result score #t mb run data get storage rlk:mboss cur.phases[0]
execute if score #t mb matches 1..99 store result storage rlk:mboss a.pct int 1 run scoreboard players get #t mb
execute if score #t mb matches 1..99 run function rlk:mboss/repool with storage rlk:mboss a
execute if score #mbPx mb matches 1 run function rlk:mboss/px/spawn
''')
w('start_unloaded', '''
# @s = zone marker. The arena chunks are not loaded (their forceload was released, e.g. room/remove then
# room/setup without a /reload): forceload them again and retry every 10 ticks; the 7th miss in a row (3 s) cancels
# the fight without reward like a failed spawn (the gate comes back).
execute in minecraft:overworld run function rlk:mboss/ar/fl_on
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
# @s = zone marker: give up this attempt (no reward); room/combat_clear -> mboss/won (chapter: cb/clear -> cb/won)
# brings the gate back.
scoreboard players set #mbFail mb 0
scoreboard players set #mbLd mb 0
scoreboard players set #mbKilled mb 0
scoreboard players set #cbWait mb 0
execute unless data storage rlk:mboss cur{kind:"chapter"} run tellraw @a[tag=player] ''', gray('중간보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)') + ''']
execute if data storage rlk:mboss cur{kind:"chapter"} run tellraw @a[tag=player] ''', gray('보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)') + ''']
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
# chapter mode (AZ-CM): #mbMode from cur.kind, the fight arena and its radii, proxies; per-fight chapter state
scoreboard players set #mbMode mb 0
execute if data storage rlk:mboss cur{kind:"chapter"} run scoreboard players set #mbMode mb 1
execute store result score #mbAr mb run data get storage rlk:mboss cur.ar
''' + ''.join(f'execute if score #mbAr mb matches {a["n"]} run scoreboard players set #mbArW10 mb {int(round(a["walk"] * 10))}\n'
              f'execute if score #mbAr mb matches {a["n"]} run scoreboard players set #mbArS10 mb {int(round(a["safe"] * 10))}\n'
              for _, a in ARENAS) + '''execute store result score #mbPx mb run data get storage rlk:mboss cur.px
scoreboard players set #mbLost mb 0
scoreboard players set #mbFloor mb 0
scoreboard players set #mbFloorHit mb 0
scoreboard players set #mbCine mb 0
scoreboard players set #mbPoolPct mb 100
scoreboard players set #mbRamp mb 0
scoreboard players set #mbHitEv mb 0
scoreboard players set #mbDodgeEv mb 0
scoreboard players set #mbDodgeOk mb 0
scoreboard players set #mbPart mb 0
scoreboard players set #mbQi mb 0
data remove storage rlk:mboss lv
data remove storage rlk:mboss px
data remove storage rlk:mboss push
data modify storage rlk:mboss sub set value []
data modify storage rlk:mboss extra set value []
data modify storage rlk:mboss aura set value []
scoreboard players set #mbAuraK mb -1
function rlk:mboss/player_reset
function rlk:mboss/opts_reset
''')
w('player_reset', '''
# Player-side fight modifiers back to neutral (fight start, cleanup_fight): healing received 100 %, no crit
# chance / crit damage change, no pending heal events or amounts, no low gravity. The player's crit stats are
# recomputed every 2 t (items/stat_light -> items/hook/stat_buffs).
scoreboard players set #mbHealPct mb 100
scoreboard players set #mbCritAdd mb 0
scoreboard players set #mbCritDmgAdd mb 0
scoreboard players set #mbHealEv mb 0
scoreboard players set #mbHealAmt mb 0
# low gravity off (rlk:tick removes the modifiers on the next tick: mboss/lowg_off)
scoreboard players set #mbLowG mb 0
''')
w('player_heal', '''
# From items/hook/on_heal, its first line (@s = player, #heal tmp >= 1), only while a fight is live (#mbLive 1).
# Every heal attempt counts as one heal event (#mbHealEv mb +1; the running module reads and clears it in its
# tick, e.g. the butterfly's 달빛 고치 cure meter), and the healing received is x #mbHealPct % (set by the module,
# 100 = unchanged; rounded half up), at least 1. #mbHealAmt mb adds up the amount after that factor (overheal
# included: the cap to max HP comes later in player/heal), cleared by the module with the events. It runs before
# the character hooks (Clorinde's Night Vigil turns heals into Bond of Life), so a heal that a character converts
# still counts and is reduced first.
scoreboard players add #mbHealEv mb 1
execute unless score #mbHealPct mb matches 100 run scoreboard players operation #heal tmp *= #mbHealPct mb
execute unless score #mbHealPct mb matches 100 run scoreboard players add #heal tmp 50
execute unless score #mbHealPct mb matches 100 run scoreboard players operation #heal tmp /= #c100 mb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
scoreboard players operation #mbHealAmt mb += #heal tmp
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
# chapter mode (AZ-CM): per-element RES from the registry res (mbRes0..8, rlk_mb_resel); mid-bosses have none (mres 0)
execute if data storage rlk:mboss cur.res run function rlk:mboss/res_set
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
execute in minecraft:overworld run function rlk:mboss/ar/box_absorb
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
BOX_NMAX = max([2] + [int(b.get('picks', 2)) for b in MIDS])
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
# Every entity of the fight (body, rig, hazards, props, aux objects, arena marker; chapter arena props, cm.md 12).
kill @e[tag=rlk_mb_aux]
kill @e[tag=rlk_mb_arena_prop]
kill @e[tag=rlk_mb_body]
''')
w('cleanup_fight', '''
# End of a fight without forgetting cur/ret (won reads them afterwards).
execute if score #mbId mb matches 1.. run function rlk:mboss/d/cleanup
function rlk:mboss/cleanup_aux
function rlk:mboss/ar/sweep
function rlk:mboss/bars_hide
function rlk:mboss/line/clear
function rlk:mboss/music/stop
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
# chapter mode (AZ-CM): per-fight chapter state; #mbAr keeps its value until the next fight_vars (cb/won reads it)
scoreboard players set #mbMode mb 0
scoreboard players set #mbFloor mb 0
scoreboard players set #mbFloorHit mb 0
scoreboard players set #mbCine mb 0
scoreboard players set #mbPushOn mb 0
scoreboard players set #mbPoolPct mb 100
scoreboard players set #mbRamp mb 0
scoreboard players set #mbHitEv mb 0
scoreboard players set #mbDodgeEv mb 0
scoreboard players set #mbDodgeOk mb 0
scoreboard players set #mbPart mb 0
scoreboard players set #mbPx mb 0
scoreboard players set #mbLost mb 0
scoreboard players set #cbWait mb 0
scoreboard players set #mbNoRx mb 0
scoreboard players reset #hzPmL mb
data remove storage rlk:mboss px
data remove storage rlk:mboss push
data remove storage rlk:mboss lv
''')
w('cleanup', '''
# Idempotent full cleanup: room/clear (map change, run end, death), room/wipe, uninstall, test stop.
# Never teleports the player (callers that end a run move the player themselves).
function rlk:mboss/cleanup_fight
function rlk:mboss/forget
# chapter arenas (AZ-CM): their forceload goes (ar/<aid>/fl_off aborts a running job of that arena first; cb/pp/<id>
# adds the forceload again at the next entrance build); barrier bands
''' + ''.join(f'execute in minecraft:overworld run function rlk:mboss/ar/{aid}/fl_off\n' for aid, _ in ARENAS if aid != 'plaza')
  + ''.join(f'execute in minecraft:overworld run function rlk:mboss/arena/{aid}/sweep {{y0:{a["sweep"]["y0"]},y1:{a["sweep"]["y1"]}}}\n'
            for aid, a in ARENAS if aid != 'plaza' and 'sweep' in a))
SWEEP_PLAZA = '''
# Loose entities in the arena box (room/clear only sweeps the dungeon square).
execute in minecraft:overworld positioned @BOX@ run kill @e[type=minecraft:arrow,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[type=minecraft:item,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[type=minecraft:experience_orb,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[tag=rlk_healorb,@BOXD@]
execute in minecraft:overworld positioned @BOX@ run kill @e[tag=rlk_gold,@BOXD@]
'''
w('arena_sweep', '''
# Loose entities in the fight arena's box (F:mboss/ar/<aid>/sweep).
function rlk:mboss/ar/sweep
''')

# =============================================================================================
# World tick, pause, out of bounds, state shells, death
w('world_cm_pre', '''
# From mboss/world in a chapter fight (#mbMode 1), before the libraries and the module tick: out of bounds of the
# chapter arena (#mbAr >= 1; the plaza's is called by world directly), the body push request cleared (a per-tick
# request: set again by the module tick, cm.md 13.5), the lockv ring buffer (mv/lockv), proxy clicks polled.
execute if score #mbAr mb matches 1.. if score #mbOn mb matches 1 unless entity @a[tag=player,scores={devMode=1}] as @e[tag=rlk_body,limit=1] at @s run function rlk:mboss/ar/oob
scoreboard players set #mbPushOn mb 0
function rlk:mboss/mv/lv_sample
execute if score #mbPx mb matches 1 run function rlk:mboss/px/poll
''')
w('world_cm_post', '''
# From mboss/world in a chapter fight (#mbMode 1), after the module tick (and the rig tick inside it): the proxies
# follow the shown pose, the body push (#mbPushOn set by the module this tick), the music clock.
execute if score #mbPx mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/px/tick
execute if score #mbPushOn mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s rotated as @s run function rlk:mboss/push/capsule
execute if score #mbMusPh mb matches 1.. run function rlk:mboss/music/tick
''')
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
execute unless score #mbAr mb matches 1.. if score #mbOn mb matches 1 unless entity @a[tag=player,scores={devMode=1}] as @e[tag=rlk_body,limit=1] at @s run function rlk:mboss/ar/plaza/oob
# chapter fights only (AZ-CM, #mbMode 1; a mid-boss tick pays these two checks): the chapter arena's out of bounds,
# the per-tick push request cleared, the lockv ring buffer, proxy clicks (world_cm_pre); after the module tick the
# proxies follow the shown pose, the body push, the music clock (world_cm_post)
execute if score #mbMode mb matches 1 run function rlk:mboss/world_cm_pre
execute if score #mbMvOn mb matches 1 run function rlk:mboss/mv/all
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/body_tick
execute if score #mbMode mb matches 1 run function rlk:mboss/world_cm_post
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
# chapter mode (AZ-CM): the pause edge halts the music (resume restarts the phase track) and drops proxy clicks
execute if score #mbPause mb matches 0 if score #mbMusPh mb matches 1.. run function rlk:mboss/music/halt
execute if score #mbPx mb matches 1 run function rlk:mboss/px/clear_input
scoreboard players set #mbPause mb 1
# No boss bars on the death screen (the run, or the test, is lost).
execute if entity @a[tag=player,scores={dead=1}] run function rlk:mboss/bars_hide
''')
w('resume', '''
scoreboard players set #mbPause mb 0
execute if score #mbMusPh mb matches 1.. store result storage rlk:mboss a.ph int 1 run scoreboard players get #mbMusPh mb
execute if score #mbMusPh mb matches 1.. run function rlk:mboss/music/set with storage rlk:mboss a
execute as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/d/resume
''')
OOB_PLAZA = T.join(['''
# @s = rlk_body (avatar or first-person player), at @s. Inside = between y 198 and 217 (wall 201..207,
# barrier cap above it; the volume box is taken at the body's own x/z) and within @OOB@ blocks of the axis.
execute if entity @s[y=198,dy=19] positioned @CX@ ~ @CZ@ if entity @s[distance=..@OOB@] run return 0
execute as @a[tag=player,limit=1] run function rlk:mboss/tp_start with storage rlk:mboss cur.start
execute as @a[tag=player,limit=1] run function rlk:view/sync
function rlk:mboss/safe_start with storage rlk:mboss cur.start
title @a[tag=player] actionbar ''', '{text:"경기장 밖으로 벗어나 처음 자리로 돌아왔습니다",color:"#FFB0A0",bold:false}]'])
w('oob', '''
# @s = rlk_body, at @s: the out-of-bounds check of the fight arena (F:mboss/ar/<aid>/oob; the plaza's is the M0 text).
function rlk:mboss/ar/oob
''')
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
# chapter mode (AZ-CM): proxies to the dead set (inv: nothing targetable), the music stops (a sting is the module's)
execute if score #mbPx mb matches 1 run function rlk:mboss/px/state {set:"dead"}
function rlk:mboss/music/stop
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
# Chapter mode (AZ-CM, cm.md 13.3 / 13.4): one-shot inputs #mbNoRx (no player-side reaction: F:player/take_damage skips
# element/player_hit while #mbNRNow 1; hz/hurt and pj/hit copy their hazard's / prop's option into it) and #mbSrc
# (1 hazard, 2 projectile; 0 = a direct call); refused while #mbCine 1; after a call that reached the player the hit /
# dodge events #mbHitEv #mbHitEl #mbHitSh #mbHitRA #mbHitSrc / #mbDodgeEv #mbDodgeOk (read and cleared by the module).
scoreboard players set #dodged tmp 0
scoreboard players operation #mbNRIn mb = #mbNoRx mb
scoreboard players set #mbNoRx mb 0
scoreboard players operation #mbSrcIn mb = #mbSrc mb
scoreboard players set #mbSrc mb 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if score #mbSt mb matches 2 run return 0
execute if score #mbCine mb matches 1 run return 0
scoreboard players set #mbShIn mb 0
execute if entity @a[tag=player,scores={shieldHP=1..},limit=1] run scoreboard players set #mbShIn mb 1
execute if entity @a[tag=player,scores={gShield=1..},limit=1] run scoreboard players set #mbShIn mb 1
scoreboard players operation #mbNRNow mb = #mbNRIn mb
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
scoreboard players set #mbNRNow mb 0
kill @e[tag=rlk_plkb_source]
scoreboard players set #mbKBDir mb 0
function rlk:mboss/hurt_ev
''')
w('hurt_ev', '''
# @s = the attacker of a mboss/hurt call that reached the player (cm.md 13.3). Landed: #mbHitEv +1 with its element,
# shield-before-the-hit, re-arming / lingering source (#hzRearm hazard) and source kind (1 hazard, 2 projectile, 3 direct).
# Dodged: #mbDodgeEv +1; #mbDodgeOk 1 only for a one-shot strike hazard (no re-arm, tell >= 12 t, dodgeable) or a projectile.
execute if score #dodged tmp matches 1 run return run function rlk:mboss/hurt_dodge
scoreboard players add #mbHitEv mb 1
scoreboard players operation #mbHitEl mb = #cmEl tmp
scoreboard players operation #mbHitSh mb = #mbShIn mb
scoreboard players set #mbHitRA mb 0
execute if score #mbSrcIn mb matches 1 if score @s mbHzRA matches 1.. run scoreboard players set #mbHitRA mb 1
scoreboard players set #mbHitSrc mb 3
execute if score #mbSrcIn mb matches 1..2 run scoreboard players operation #mbHitSrc mb = #mbSrcIn mb
''')
w('hurt_dodge', '''
scoreboard players add #mbDodgeEv mb 1
execute if score #mbSrcIn mb matches 2 run return run scoreboard players set #mbDodgeOk mb 1
execute unless score #mbSrcIn mb matches 1 run return 0
execute if score @s mbHzRA matches 0 if score @s mbHzW matches 12.. if score @s mbHzND matches 0 run scoreboard players set #mbDodgeOk mb 1
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
scoreboard players set #auxResEl mb -1
scoreboard players set #auxResElV mb 0
scoreboard players reset #auxShW mb
scoreboard players reset #auxShH mb
scoreboard players reset #auxHbY mb
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
execute if score #auxResEl mb matches 0..8 run function rlk:mboss/aux/res_el
# AP-FW (cm.md 13.12): the click shield size and the HP-bar height of this aux (one-shot options of aux/spawn)
execute if score #auxShW mb matches 1.. run function rlk:mboss/aux/shield_pre
execute if score #auxHbY mb matches -100..100 run function rlk:mboss/aux/hb_y
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
# chapter fights (AZ-CM): the repool refill, the bossui options back to 0 before d/bars (bars_cm)
execute if score #mbMode mb matches 1 run function rlk:mboss/bars_cm
scoreboard players set #buSub bu 0
scoreboard players set #buSubMax bu 1
scoreboard players set #buSubCol bu 0
function rlk:mboss/d/bars
function rlk:bossui/draw
bossbar set rlk:mboss_state name {nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}
bossbar set rlk:mboss_sub name {nbt:"sub[]",storage:"rlk:mboss",interpret:true,separator:""}
''')
w('bars_cm', '''
# From mboss/bars in a chapter fight (#mbMode 1): after mboss/repool the new pool's bar refills over 30 t (#mbRamp);
# the bossui options (tools/build_bossbar.py), 0 = the default look, are reset before d/bars every call (cm.md 11):
# #buHpCol HP colour code, #buNoNum 1 = no numbers. (bossui/draw also resets both after every draw, so a mid-boss
# fight, which never sets them, and Raiden always draw the M0 line.)
execute if score #mbRamp mb matches 1.. run function rlk:mboss/bars_repool
scoreboard players set #buHpCol bu 0
scoreboard players set #buNoNum bu 0
''')
w('bars_ramp', '''
# Intro: the HP bar fills over 1.5 s.
scoreboard players operation #buHp bu *= #mbT mb
scoreboard players operation #buHp bu /= #c30 mb
''')
w('bars_repool', '''
# After mboss/repool (#mbRamp 30..1): the new pool's bar refills over 30 t (#buHp x (30 - ramp) / 30, overflow-safe).
scoreboard players remove #mbRamp mb 1
scoreboard players set #t mb 30
scoreboard players operation #t mb -= #mbRamp mb
scoreboard players operation #h mb = #buHp bu
execute if score #h mb matches 10000000.. run scoreboard players operation #buHp bu /= #c30 mb
scoreboard players operation #buHp bu *= #t mb
execute if score #h mb matches ..9999999 run scoreboard players operation #buHp bu /= #c30 mb
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
        elif hook == 'incoming' and b.get('kind', 'mid') == 'chapter':
            # chapter bosses: the module's incoming, then the framework floor (mboss/floor, cm.md 7.2)
            lines.append(f'execute if score #mbId mb matches {b["n"]} run return run function rlk:mboss/cb/inc/{b["id"]}')
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
    ('full', ['tell', 'dmg'], ['scoreboard players operation #hzR mb = #mbArW10 mb', 'scoreboard players set #hzK mb 5']),
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
# chapter mode (AZ-CM): no player-side reaction; the mask's safe group (0 = this hazard's own id, set below)
scoreboard players operation @s mbHzNR = #hzNR mb
scoreboard players operation @s mbHzSG = #hzSafeG mb
execute if score #hzPm mb matches 1.. run function rlk:mboss/hz/init_pm
scoreboard players operation @s mbHzCol = @s mbHzE
execute if score #hzCol mb matches 0.. run scoreboard players operation @s mbHzCol = #hzCol mb
execute if score #hzQuiet mb matches 1 run tag @s add rlk_mb_hzq
execute if score @s mbHzW matches ..0 run scoreboard players set @s mbHzW 1
execute if score @s mbHzA matches ..0 run scoreboard players set @s mbHzA 1
scoreboard players set @s mbHzT -1
scoreboard players set @s mbHzHit 0
# a member made after its volley group already landed its hit is harmless from the start (#mbGrpL, grp_mark)
execute if score @s mbHzG matches 1.. if score @s mbHzG = #mbGrpL mb run scoreboard players set @s mbHzHit 1
scoreboard players operation @s mbHzL = @s mbHzW
scoreboard players operation @s mbHzL += @s mbHzA
scoreboard players operation @s mbHzL += #hzLinger mb
scoreboard players add #hzId mb 1
scoreboard players operation @s mbHzI = #hzId mb
scoreboard players operation #hzLast mb = #hzId mb
execute if score @s mbHzSG matches 0 run scoreboard players operation @s mbHzSG = @s mbHzI
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
# mask (kind 6, AZ-CM): the safe distance (R0 + 0.3 b) squared
execute if score @s mbHzK matches 6 run function rlk:mboss/hz/init_mask
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
# a mask with its own safe group (#hzSafeG 0 at creation) takes its safe markers with it (AZ-CM)
execute if score @s mbHzK matches 6 if score @s mbHzSG = @s mbHzI run function rlk:mboss/hz/mask_end
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
# Arena rim, the safe circle (green) and a ring growing from the centre (the fight arena's: F:mboss/ar/<aid>/full_rim).
$function rlk:mboss/ar/full_rim {kp:$(kp)}
execute if score @s mbHzR0 matches 1.. run function rlk:mboss/hz/d/full_safe
''')
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
execute if score @s mbHzK matches 6 run return run function rlk:mboss/hz/hit_mask
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
# AP-FW (cm.md 13.7, 13.11): refused while #mbCine 1 without being consumed (it can still hit after the cine); a
# per-mille hazard (#hzPm) hits through mboss/pl_dot (hz/hurt_pm).
execute if score #mbCine mb matches 1 run return 0
scoreboard players set @s mbHzHit 1
execute if score @s mbHzRA matches 1.. run function rlk:mboss/hz/rearm_at
scoreboard players set #hzHit mb 1
execute if score @s mbHzPm matches 1.. run return run function rlk:mboss/hz/hurt_pm
scoreboard players operation #mbHitPct mb = @s mbHzD
scoreboard players operation #cmEl tmp = @s mbHzE
scoreboard players operation #mbKB mb = @s mbHzB
scoreboard players operation #mbKBDir mb = @s mbHzKD
scoreboard players operation #mbNoDodge mb = @s mbHzND
scoreboard players operation #mbNoRx mb = @s mbHzNR
scoreboard players set #mbSrc mb 1
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
# chapter mode (AZ-CM): no dash dodge / no player-side reaction
scoreboard players operation @s mbPjND = #pjNoDodge mb
scoreboard players operation @s mbPjNR = #pjNR mb
execute if score @s mbPjG matches 1.. if score @s mbPjG = #mbGrpL mb run scoreboard players set @s mbPjHit 1
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
# Blade hit shape (#pjShape 1): a line across the flight direction, hr tenths on each side. Its reach is hr + 0.3
# off the line (the same 0.3 body pad as every other shape and the telegraph): sample spheres of radius BLADE_R
# whose outer centres sit at +-(hr + 0.3 - BLADE_R), at most 0.6 b apart, in three rows 0.9 / 0.3 b below and 0.3 b
# above the prop (the prop flies 0.9 b over the floor: feet from the floor to floor + 1.65 are covered without a gap,
# a jump's apex is 1.25), each tested against the player's feet. Swept by the 0.25 b sub-steps. (Before the review
# fix FW-1 the outer points sat at +-hr with 0.65 b spheres in two rows: a reach of hr + 0.65 and a height gap.)
BLADE_R, BLADE_PAD, BLADE_GAP = 0.45, 0.3, 0.6
for k in range(1, 41):
    hw = k / 10
    reach = hw + BLADE_PAD
    if reach <= BLADE_R:
        xs, rad = [0.0], reach
    else:
        outer = reach - BLADE_R
        n = max(1, math.ceil(2 * outer / BLADE_GAP - 1e-9))
        xs, rad = [-outer + 2 * outer * i / n for i in range(n + 1)], BLADE_R
    lines = [f'# Blade half width {L.num(hw)} b (reach {L.num(reach)} b off the line): {len(xs)} points x 3 rows, radius {L.num(rad)} b '
             '(@s = prop, at and rotated as it).']
    for dy in (-0.9, -0.3, 0.3):
        for x in xs:
            lines.append(f'execute positioned ^{L.num(x, 3)} ^{L.num(dy)} ^ if entity @e[tag=rlk_body,distance=..{L.num(rad + 0.001, 3)},limit=1] '
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
# visuals and the flights go on). #mbGrpL remembers it, so a member made later (hz/init, pj/launch) starts harmless:
# one hit per group even when a member is created after the hit (e.g. a burst made at a prop's life end).
scoreboard players operation #mbGrpL mb = #g mb
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
# AP-FW (cm.md 13.7): refused while #mbCine 1 without being consumed (no event; the prop can still hit after the cine).
execute if score #mbCine mb matches 1 run return 0
scoreboard players set @s mbPjHit 1
scoreboard players operation #mbHitPct mb = @s mbPjD
scoreboard players operation #cmEl tmp = @s mbPjE
scoreboard players operation #mbKB mb = @s mbPjB
scoreboard players set #mbKBDir mb 1
scoreboard players operation #mbNoDodge mb = @s mbPjND
scoreboard players operation #mbNoRx mb = @s mbPjNR
scoreboard players set #mbSrc mb 2
function rlk:mboss/hurt
scoreboard players set #mbNoDodge mb 0
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
OK_PLAZA = '''
# At a proposed feet position: inside the safe disc (@SAFEP@ b from the axis) with free feet and head.
execute positioned ~ @CY@ ~ unless entity @e[tag=rlk_mb_arena,distance=..@SAFEP@,limit=1] run return fail
execute unless block ~ ~ ~ #rlk:dash_pass run return fail
execute unless block ~ ~1 ~ #rlk:dash_pass run return fail
return 1
'''
w('mv/ok', '''
# At a proposed feet position: inside the fight arena's safe disc (safe - 0.5 b from the axis) with free feet and head.
# A chapter arena (#mbAr >= 1) through F:mboss/ar/<aid>/ok; the plaza's lines (the M0 text, = ar/plaza/ok) follow inline.
execute if score #mbAr mb matches 1.. run return run function rlk:mboss/ar/ok''' + OK_PLAZA.split('head.', 1)[1])
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
LEASH_PLAZA = '''
# @s = body (automatic every fight tick unless #mbNoLeash mb 1). Beyond @SAFE1@ b from the axis: slide back
# 0.45 b/t; beyond @WALK2@ b: back to the centre at once.
execute at @s positioned ~ @CY@ ~ if entity @e[tag=rlk_mb_arena,distance=..@SAFE1@,limit=1] run return 0
execute at @s positioned ~ @CY@ ~ unless entity @e[tag=rlk_mb_arena,distance=..@WALK2@,limit=1] run return run function rlk:mboss/mv/home
execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
'''
w('mv/leash', '''
# @s = body (automatic every fight tick unless #mbNoLeash mb 1): the fight arena's leash. A chapter arena (#mbAr >= 1)
# through F:mboss/ar/<aid>/leash; the plaza's lines (the M0 text, = ar/plaza/leash) follow inline.
execute if score #mbAr mb matches 1.. run return run function rlk:mboss/ar/leash''' + LEASH_PLAZA.split('at once.', 1)[1])
w('mv/home', '''
execute at @e[tag=rlk_mb_arena,limit=1] run tp @s ~ ~ ~
execute at @s run particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 12 force @a[tag=player]
''')
w('mv/clamp', '''
# @s (e.g. a destination marker) is pulled toward the arena axis until it is inside the fight arena's safe disc.
# A chapter arena (#mbAr >= 1) through F:mboss/ar/<aid>/clamp; the plaza's lines (= ar/plaza/clamp) follow inline.
execute if score #mbAr mb matches 1.. run return run function rlk:mboss/ar/clamp
scoreboard players set #cl mb 0
function rlk:mboss/ar/plaza/clamp_step
''')
w('mv/clamp_step', '''
function rlk:mboss/ar/clamp_step
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
$data modify storage rlk:mboss tlast set value {id:"$(id)",ch:1}
$scoreboard players set #mbReqCh mb $(ch)
execute unless score #mbReqCh mb matches 1.. run scoreboard players set #mbReqCh mb 1
# ... and its chapter, so [다시 하기] replays the same chapter (test/defeat_msg, test/won_msg)
execute store result storage rlk:mboss tlast.ch int 1 run scoreboard players get #mbReqCh mb
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #mbTest mb 1
scoreboard players set #mbLock mb 0
# a chapter test's forced chapter boss and auto gate press end here (every boss map of this test is the run's)
scoreboard players set #cbForce mb 0
scoreboard players set #cbAuto mb 0
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
# chapter mode (AZ-CM): the new full pool is #mbTot; the current split (#mbPoolPct < 100) is applied again
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation #mbTot mb = @s mhpM
execute if score #mbPoolPct mb matches 1..99 store result storage rlk:mboss a.pct int 1 run scoreboard players get #mbPoolPct mb
execute if score #mbPoolPct mb matches 1..99 run function rlk:mboss/repool with storage rlk:mboss a
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
scoreboard players set #cbForce mb 0
scoreboard players set #cbAuto mb 0
function rlk:run/end
function rlk:mboss/cleanup
execute as @a[tag=player] run function rlk:lobby/go
''')
w('test/defeat', '''
# From player/hook_respawn during a test: never fails/resets the character. The replay link restarts the boss and
# the chapter of this test (rlk:mboss tlast {id, ch}, saved by test/start_ch; cur is forgotten by test/end).
execute unless data storage rlk:mboss tlast.id run data modify storage rlk:mboss tlast set value {id:"proto",ch:1}
execute if data storage rlk:mboss cur.id run data modify storage rlk:mboss tlast.id set from storage rlk:mboss cur.id
execute unless data storage rlk:mboss tlast.ch run data modify storage rlk:mboss tlast.ch set value 1
# the wording and the replay link follow the fight that just ended (a chapter session can reach a mid-boss and back)
execute if data storage rlk:mboss cur{kind:"chapter"} run data modify storage rlk:mboss tlast.cb set value 1b
execute if data storage rlk:mboss cur.id unless data storage rlk:mboss cur{kind:"chapter"} run data remove storage rlk:mboss tlast.cb
function rlk:mboss/test/end
title @s times 10 40 15
title @s subtitle {text:"로비로 돌아왔습니다",color:"gray"}
execute unless data storage rlk:mboss tlast{cb:1b} run title @s title {text:"중간보스 테스트 실패",color:"#E06A5A",bold:true}
execute if data storage rlk:mboss tlast{cb:1b} run title @s title {text:"챕터 보스 테스트 실패",color:"#E06A5A",bold:true}
scoreboard players set @s vBig 65
scoreboard players set @s ttlT 65
execute if data storage rlk:mboss tlast{cb:1b} run return run function rlk:mboss/test/cdefeat_msg with storage rlk:mboss tlast
function rlk:mboss/test/defeat_msg with storage rlk:mboss tlast
''')
# [다시 하기] replays the same boss AND chapter (review fix FW-3: it used to restart at chapter 1 through test/start).
REPLAY = link('/function rlk:mboss/test/start_ch {id:"$(id)",ch:$(ch)}', '[다시 하기]')
w('test/defeat_msg', '$tellraw @s ' + TT + gray('쓰러졌습니다. ') + ',' + REPLAY + ']')
w('test/won', '\n'.join([
    '# From mboss/won during a test (with storage rlk:mboss cur): the replay link comes from rlk:mboss tlast {id, ch}',
    '# (test/start_ch), with this fight\'s id.',
    '$data modify storage rlk:mboss tlast.id set value "$(id)"',
    'execute unless data storage rlk:mboss tlast.ch run data modify storage rlk:mboss tlast.ch set value 1',
    '# the wording follows this fight (cur.kind; cur is always there), not the session: a chapter test can go on to a',
    '# mid-boss of the next chapter and back (tlast.cb is kept for test/defeat)',
    'execute if data storage rlk:mboss cur{kind:"chapter"} run data modify storage rlk:mboss tlast.cb set value 1b',
    'execute unless data storage rlk:mboss cur{kind:"chapter"} run data remove storage rlk:mboss tlast.cb',
    'execute if data storage rlk:mboss cur{kind:"chapter"} run return run function rlk:mboss/test/cwon',
    'execute if score #mbKilled mb matches 1 run function rlk:mboss/test/won_msg with storage rlk:mboss tlast',
    'execute unless score #mbKilled mb matches 1 run tellraw @a[tag=player] ' + TT + gray('취소되었습니다(보상 없음). ') + ','
    + link('/function rlk:mboss/test/stop', '[로비로]') + ']']))
w('test/cwon', '\n'.join([
    '# From test/won after a chapter fight (killed or cancelled): the forced routing and the auto gate press end with the',
    '# fight (cm.md 4.1; a cancelled gate needs neither: cb/gate and cb/start never read #cbForce), so the rest of the',
    '# session (k_chapter -> the next chapter\'s boss map) routes as in a run. The chapter wording and replay link.',
    'scoreboard players set #cbForce mb 0',
    'scoreboard players set #cbAuto mb 0',
    'execute if score #mbKilled mb matches 1 run return run function rlk:mboss/test/cwon_msg with storage rlk:mboss tlast',
    'tellraw @a[tag=player] ' + CTT + gray('취소되었습니다(보상 없음). 문이 다시 나타났습니다. ') + ','
    + link('/function rlk:mboss/test/stop', '[로비로]') + ']']))
w('test/won_msg', '$tellraw @a[tag=player] ' + TT + gray('처치! 문 자리에 아이템 상자가 떨어졌습니다(누르면 아이템 선택). ') + ',' + REPLAY
  + ',' + gray(' ') + ',' + link('/function rlk:mboss/test/stop', '[로비로]') + ']')
w('test/arena', TT.join(['''
# Rebuild the arena and look at it (outside a run). Back: /function rlk:lobby/go
execute if score #active room matches 1 run return run tellraw @s ''', gray('런 중에는 쓸 수 없습니다.') + ''']
execute in minecraft:overworld run function rlk:mboss/arena/rebuild
execute in minecraft:overworld run tp @s @CX@.5 @CY@ @CZ@.5 180 0
function rlk:view/sync
tellraw @s ''', gray('경기장을 다시 지었습니다. 돌아가기: ') + ',' + link('/function rlk:lobby/go') + ']']))

# =============================================================================================
# Chapter mode (AZ-CM; scratchpad az/contract/cm.md). Everything below is generic: the chapter bosses, their arenas
# and their routing come from the registry (kind "chapter", arenas{}); Azhdaha and Apep plug in as data.
# ---------------------------------------------------------------------------------------------
# A. Per-arena functions F:mboss/ar/<aid>/<fn> behind one-line dispatchers F:mboss/ar/<fn> on #mbAr (cm.md 6.1, 6.2).
#    The plaza's functions hold exactly the M0 text of the function they replace (mid-boss fights behave as on M0).
AR_FNS = ['marker', 'oob', 'sweep', 'box_absorb', 'ok', 'clamp', 'clamp_step', 'clampw', 'clampw_step', 'leash',
          'full_rim', 'tp_in', 'fl_on', 'fl_off', 'loaded', 'ensure', 'test']
AR_MACRO = {'full_rim': '{kp:$(kp)}'}           # dispatchers that pass macro arguments on


def ar_box(a):
    b = a['box']
    return b['x0'], b['y0'], b['z0'], b['x1'], b['y1'], b['z1']


def ar_texts(aid, a):
    """{fn: text} of one arena's F:mboss/ar/<aid>/*."""
    x0, y0, z0, x1, y1, z1 = ar_box(a)
    cx, cy, cz = a['cx'], a['cy'], a['cz']
    walk, safe = a['walk'], a['safe']
    box, boxd = f'{x0} {y0} {z0}', f'dx={x1 - x0},dy={y1 - y0},dz={z1 - z0}'
    fl = f'{x0} {z0} {x1} {z1}'
    P = f'rlk:mboss/ar/{aid}/'
    oy0, oy1 = L.arena_oob(a)
    t = {}
    t['marker'] = (f'# The arena marker of {aid} (rlk_mb_arena, rotation 180 as the plaza; d/spawn runs rotated as it).\n'
                   f'execute in minecraft:overworld run summon minecraft:marker {cx} {cy} {cz} '
                   '{Tags:["rlk_room","rlk_mb_aux","rlk_mb_arena"],Rotation:[180.0f,0.0f]}')
    if aid == 'plaza':
        t['oob'] = OOB_PLAZA
        t['sweep'] = SWEEP_PLAZA
        t['ok'] = OK_PLAZA
        t['leash'] = LEASH_PLAZA
    else:
        t['oob'] = (f'# @s = rlk_body, at @s. Inside = feet in y {oy0}..{oy1} (the volume box taken at the body\'s own x/z) and within\n'
                    f'# {L.num(walk + 1.5)} b of the axis of {aid}; else back to the arrival spot.\n'
                    f'execute if entity @s[y={oy0},dy={oy1 - oy0}] positioned {cx} ~ {cz} if entity @s[distance=..{L.num(walk + 1.5)}] run return 0\n'
                    'execute as @a[tag=player,limit=1] run function ' + P + 'tp_in\n'
                    'title @a[tag=player] actionbar {text:"경기장 밖으로 벗어나 처음 자리로 돌아왔습니다",color:"#FFB0A0",bold:false}')
        t['sweep'] = (f'# Loose entities in the box of {aid}.\n' + ''.join(
            f'execute in minecraft:overworld positioned {box} run kill @e[{sel}{boxd}]\n'
            for sel in ('type=minecraft:arrow,', 'type=minecraft:item,', 'type=minecraft:experience_orb,', 'tag=rlk_healorb,', 'tag=rlk_gold,')).rstrip('\n'))
        t['ok'] = (f'# At a proposed feet position: inside the safe disc of {aid} ({L.num(safe - 0.5)} b from the axis) with free feet and head.\n'
                   f'execute positioned ~ {cy} ~ unless entity @e[tag=rlk_mb_arena,distance=..{L.num(safe - 0.5)},limit=1] run return fail\n'
                   'execute unless block ~ ~ ~ #rlk:dash_pass run return fail\n'
                   'execute unless block ~ ~1 ~ #rlk:dash_pass run return fail\n'
                   'return 1')
        t['leash'] = (f'# @s = body: beyond {L.num(safe + 1)} b from the axis of {aid} slide back 0.45 b/t; beyond {L.num(walk + 2)} b back home.\n'
                      f'execute at @s positioned ~ {cy} ~ if entity @e[tag=rlk_mb_arena,distance=..{L.num(safe + 1)},limit=1] run return 0\n'
                      f'execute at @s positioned ~ {cy} ~ unless entity @e[tag=rlk_mb_arena,distance=..{L.num(walk + 2)},limit=1] run return run function rlk:mboss/mv/home\n'
                      'execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~')
    t['box_absorb'] = (f'# Gold left in the box of {aid} goes to the player (cb/won, won).\n'
                       f'execute in minecraft:overworld positioned {box} as @e[tag=rlk_gold,{boxd}] run function rlk:combat/gold_absorb')
    for nm, rad, what in (('clamp', safe - 0.5, 'safe disc'), ('clampw', walk - 0.7, 'walk disc')):
        t[nm] = (f'# @s (a destination marker) is pulled toward the axis until it is inside the {what} of {aid} ({L.num(rad)} b).\n'
                 'scoreboard players set #cl mb 0\n'
                 f'function {P}{nm}_step')
        t[nm + '_step'] = (f'execute at @s positioned ~ {cy} ~ if entity @e[tag=rlk_mb_arena,distance=..{L.num(rad)},limit=1] run return 0\n'
                           'scoreboard players add #cl mb 1\n'
                           'execute if score #cl mb matches 90.. run return 0\n'
                           'execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~\n'
                           f'function {P}{nm}_step')
    k = int(round(walk * 2))
    assert 1 <= k <= 60, f'{aid}: walk {walk} beyond the 30 b circle buckets'
    t['full_rim'] = (f'# hz/d/full of {aid}: the rim circle (walk {L.num(walk)} b) and the ring growing from the centre (macro {{kp}}).\n'
                     f'execute positioned {cx} ~ {cz} run function rlk:mboss/hz/p/c/{k} with storage rlk:mboss hzp\n'
                     f'$execute positioned {cx} ~ {cz} run function rlk:mboss/hz/p/c/$(kp) with storage rlk:mboss hzp')
    t['tp_in'] = (f'# @s = player: back to the arrival spot (cur.start) of the fight in {aid}, the avatar and the fall marker follow.\n'
                  'function rlk:mboss/tp_start with storage rlk:mboss cur.start\n'
                  'function rlk:view/sync\n'
                  'function rlk:mboss/safe_start with storage rlk:mboss cur.start'
                  + ('' if aid == 'plaza' else '\n# the player moved: the per-tick body position cache (mv/plpos) reads again\n'
                     'scoreboard players set #mbPlG mb -1'))
    t['fl_on'] = f'# Forceload the box of {aid} (idempotent).\nexecute in minecraft:overworld run forceload add {fl}'
    if aid == 'plaza':
        t['fl_off'] = f'# Release the forceload of the box of {aid}.\nexecute in minecraft:overworld run forceload remove {fl}'
    else:   # CM-REVIEW PERF-2: a job of this arena never outlives its chunks (it would wait 200 t, then abort)
        t['fl_off'] = (f'# Release the forceload of the box of {aid}; a running job of {aid} is aborted first (without the chunks it\n'
                       '# would only wait 200 t, refuse every gate press, then abort and force a full rebuild; cm.md 12).\n'
                       f'execute if data storage rlk:mboss arjob{{aid:"{aid}"}} run function rlk:mboss/arena/abort\n'
                       f'execute in minecraft:overworld run forceload remove {fl}')
    if aid == 'plaza':      # M0 mboss/start's test (the centre; the plaza forceload covers the whole box), cm.md 6.2
        t['loaded'] = (f'# 1 when the centre of the plaza is loaded (the M0 test of mboss/start), else fail.\n'
                       f'execute in minecraft:overworld unless loaded {cx} {cy} {cz} run return fail\n'
                       'return 1')
    else:
        # every chunk of the box (forced chunks load in no fixed order: a job must not start on a half-loaded box)
        cols = [(cx, cz)] + [(max(x0, i * 16), max(z0, j * 16)) for i in range(x0 >> 4, (x1 >> 4) + 1)
                             for j in range(z0 >> 4, (z1 >> 4) + 1) if (i, j) != (cx >> 4, cz >> 4)]
        t['loaded'] = (f'# 1 when every chunk of the box of {aid} is loaded (the centre first), else fail.\n'
                       + ''.join(f'execute in minecraft:overworld unless loaded {x} {cy} {z} run return fail\n' for x, z in cols)
                       + 'return 1')
    if aid == 'plaza':
        t['ensure'] = '# The plaza (legacy arena generator: arena/ensure, stamp "plaza@2").\nexecute in minecraft:overworld run return run function rlk:mboss/arena/ensure'
        t['test'] = T.join([f'''
# Rebuild the plaza and look at it (outside a run). Back: /function rlk:lobby/go
execute if score #active room matches 1 run return run tellraw @s ''', gray('런 중에는 쓸 수 없습니다.') + f''']
execute in minecraft:overworld run function rlk:mboss/arena/rebuild
execute in minecraft:overworld run tp @s {cx}.5 {cy} {cz}.5 180 0
function rlk:view/sync
tellraw @s ''', gray('경기장을 다시 지었습니다. 돌아가기: ') + ',' + link('/function rlk:lobby/go') + ']'])
    else:
        st = a['start']
        t['ensure'] = (f'# 1 when {aid} is built in its default look and loaded; else fail and a sliced job runs (arena generator).\n'
                       f'execute in minecraft:overworld run return run function rlk:mboss/arena/{aid}/ensure')
        t['test'] = T.join([f'''
# Rebuild {aid} (a sliced job) and look at it from its arrival spot (outside a run; the job's done releases the
# forceload again, outside a run). Back: /function rlk:lobby/go
execute if score #active room matches 1 run return run tellraw @s ''', gray('런 중에는 쓸 수 없습니다.') + f''']
function {P}fl_on
execute in minecraft:overworld run function rlk:mboss/arena/{aid}/rebuild
execute in minecraft:overworld run tp @s {L.num(st['x'])} {L.num(st['y'])} {L.num(st['z'])} {L.num(st['yaw'])} {L.num(st['pitch'])}
function rlk:view/sync
tellraw @s ''', gray(f'경기장 {aid} 을(를) 다시 짓는 중입니다(여러 틱; 다 지으면 강제 로드를 풉니다). 돌아가기: ') + ',' + link('/function rlk:lobby/go') + ']'])
    return t


for aid, a in ARENAS:
    for fn_, text in ar_texts(aid, a).items():
        w(f'ar/{aid}/{fn_}', text)
for fn_ in AR_FNS:
    arg = AR_MACRO.get(fn_)
    lines = [f'# GENERATED dispatcher: rlk:mboss/ar/<aid>/{fn_} of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).']
    for aid, a in ARENAS:
        cond = 'unless score #mbAr mb matches 1..' if aid == 'plaza' else f'if score #mbAr mb matches {a["n"]}'
        if arg:
            lines.append(f'$execute {cond} run return run function rlk:mboss/ar/{aid}/{fn_} {arg}')
        else:
            lines.append(f'execute {cond} run return run function rlk:mboss/ar/{aid}/{fn_}')
    if fn_ in ('ok', 'loaded', 'ensure'):
        lines.append('return fail')
    w(f'ar/{fn_}', '\n'.join(lines))

# ---------------------------------------------------------------------------------------------
# B. Chapter lifecycle F:mboss/cb/** (cm.md 5): routing, entrance prep, gate, start, win / cancel, lose, run hooks.
ROUTED = sorted(((c, b['n'], b['id']) for b in CHAPS if b.get('route', True) for c in b.get('ch', [])), key=lambda x: (x[1], x[0]))


def b_arena(b):
    return L.arena_of(b, REG)


w('cb/route', '\n'.join(
    ['# GENERATED from the registry (kind chapter: ch + route). From room/pick/boss: the boss map\'s layout. A test forces a',
     '# chapter boss through #cbForce (honoured only while #mbTest 1); every other chapter not routed here is Raiden\'s.',
     'execute if score #mbTest mb matches 1 if score #cbForce mb matches 1.. run return run function rlk:mboss/cb/route_force']
    + [f'execute if score #chapter room matches {c} run return run function rlk:mboss/cb/layout {{id:"{bid}"}}' for c, _, bid in ROUTED]
    + ['function rlk:room/raiden/layout']))
w('cb/route_force', '\n'.join(
    ['# GENERATED: the boss map of the forced chapter boss (#cbForce mb = registry n, any route flag). Never sets #mbForce.']
    + [f'execute if score #cbForce mb matches {b["n"]} run return run function rlk:mboss/cb/layout {{id:"{b["id"]}"}}' for b in CHAPS]
    + ['function rlk:room/raiden/layout']))
w('cb/layout', '\n'.join(
    ['# {id}: the domain-entrance layout of chapter boss <id> (F:room/cboss/<id>/layout, tools/build_cboss_rooms.py) into',
     '# rlk:room cur; literal lines per boss (no $(id) in a function name). An unknown id falls back to Raiden\'s layout.',
     '$data modify storage rlk:mboss cbl set value "$(id)"']
    + [f'execute if data storage rlk:mboss {{cbl:"{b["id"]}"}} run return run function rlk:room/cboss/{b["id"]}/layout' for b in CHAPS]
    + ['function rlk:room/raiden/layout']))
w('cb/prep', '\n'.join(
    ['# @s = the kind-9 zone marker of a chapter entrance, at it (from F:room/cboss/<id>/build at zone build): the arena prep',
     '# and the module\'s prep of the boss named by the zone\'s data.boss_id (literal lines per boss).']
    + [f'execute if data entity @s data{{boss_id:"{b["id"]}"}} run return run function rlk:mboss/cb/pp/{b["id"]}' for b in CHAPS]))
for b in CHAPS:
    a = b_arena(b)
    w(f'cb/pp/{b["id"]}', f'''
# Entrance prep of {b["id"]} (@s = the zone marker, at it): a fresh rlk:mboss cprep.{b["id"]}, the arena forceloaded and its
# sliced build / look restore started (the result is not needed here), then the module's own prep (gate texts, roll).
data remove storage rlk:mboss cprep.{b["id"]}
execute in minecraft:overworld run function rlk:mboss/ar/{a["aid"]}/fl_on
execute in minecraft:overworld run function rlk:mboss/ar/{a["aid"]}/ensure
function rlk:mboss/{b["id"]}/prep
''')
    w(f'cb/inc/{b["id"]}', f'''
# @s = the body inside combat/apply_mods: the module's incoming hook, then the framework floor (#mbFloor, cm.md 7.2).
function rlk:mboss/{b["id"]}/incoming
function rlk:mboss/floor
''')
    w(f'cb/g/{b["id"]}', f'''
# The gate of {b["id"]} was pressed (@s = the object marker, at it; the zone tagged rlk_cbz): forceload again (a cancelled
# cb/won released it; the chunks load during the 30-t delay), the object goes, the zone fight starts, the gate texts.
# A press (by hand or by test/cwait) ends the test's auto press, so a gate that comes back is never pressed again for you.
scoreboard players set #cbWait mb 0
scoreboard players set #cbAuto mb 0
execute in minecraft:overworld run function rlk:mboss/ar/{a["aid"]}/fl_on
function rlk:room/obj/kill_group
execute as @e[tag=rlk_zone,tag=rlk_cbz,limit=1] at @s run function rlk:room/combat_start
tag @e[tag=rlk_cbz] remove rlk_cbz
scoreboard players set #spawnT room 30
title @a[tag=player] times 6 46 14
title @a[tag=player] subtitle {{nbt:"cprep.{b["id"]}.sub",storage:"rlk:mboss",interpret:true}}
title @a[tag=player] title {{nbt:"cprep.{b["id"]}.title",storage:"rlk:mboss",interpret:true}}
scoreboard players set @a[tag=player] vBig 66
scoreboard players set @a[tag=player] ttlT 66
execute as @a[tag=player] at @s run playsound minecraft:block.bell.resonate hostile @s ~ ~ ~ 0.7 0.6
execute as @a[tag=player] at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.7
''')
w('cb/enter', '''
# @s = the kind-9 chapter zone marker, at it (from room/zone_enter instead of combat_start): the zone is cleared for
# objects (zst 3) and the gate object stands at its centre (room/obj/k_cboss, oact 16, texts from cprep.<boss_id>.gate).
scoreboard players set @s zst 3
function rlk:room/obj/k_cboss
execute unless score #k10 snd matches 1 run function rlk:snd/f10
''')
w('cb/gate', CT.join(['''
# From room/obj/click (oact 16; @s = the gate object, at it; clicks during combat are refused there). The guards of
# mboss/gate, "준비 중" while an arena job runs (#mbArBuild >= 1: the object stays), then the boss's own gate (cb/g/<id>).
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @a[tag=player] ''', gray("난이도가 '평화로움'이면 보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 누르세요.") + ''']
tag @e[tag=rlk_cbz] remove rlk_cbz
execute as @e[tag=rlk_zone,scores={zkind=9,zst=3}] if data entity @s data.cboss run tag @s add rlk_cbz
execute unless entity @e[tag=rlk_cbz,limit=1] run return 0
execute if entity @e[tag=rlk_mb_body,limit=1] run return run tag @e[tag=rlk_cbz] remove rlk_cbz
execute if score #mbArBuild mb matches 1.. run tag @e[tag=rlk_cbz] remove rlk_cbz
execute if score #mbArBuild mb matches 1.. run return run tellraw @a[tag=player] ''', gray('경기장을 준비하는 중입니다. 잠시 뒤 다시 누르세요.') + ''']
data modify storage rlk:mboss cbg set value ""
data modify storage rlk:mboss cbg set from entity @e[tag=rlk_cbz,limit=1] data.boss_id
''']).rstrip('\n') + ''.join(
    f'\nexecute if data storage rlk:mboss {{cbg:"{b["id"]}"}} run return run function rlk:mboss/cb/g/{b["id"]}'
    for b in CHAPS) + '\ntag @e[tag=rlk_cbz] remove rlk_cbz')
w('cb/spawn_route', '\n'.join(
    ['# From room/boss_spawn (@s = a kind-9 zone marker with data.cboss, at it): the chapter boss named by data.boss_id.',
     '# No fall-through to Raiden: an unknown boss_id cancels the fight (the gate returns).']
    + [f'execute if data entity @s data{{boss_id:"{b["id"]}"}} run return run function rlk:mboss/cb/start {{id:"{b["id"]}"}}' for b in CHAPS]
    + ['function rlk:mboss/start_cancel']))
w('cb/start', '''
# {id} (@s = the zone marker, at it; from cb/spawn_route, #combat = its zid). cur = cbyid.<id> (no roll, no met append,
# never #mbForce), the boss's own arena (fight_vars sets #mbMode 1 and #mbAr from cur). The arena must report built
# (ensure 1): while it does not, cb/wait retries every 10 t (a running or waiting arena job never cancels; 60 retries do).
data remove storage rlk:mboss cur
$data modify storage rlk:mboss cur set from storage rlk:mboss cbyid.$(id)
execute unless data storage rlk:mboss cur run return run function rlk:mboss/start_cancel
execute store result score #mbAr mb run data get storage rlk:mboss cur.ar
execute in minecraft:overworld run function rlk:mboss/ar/fl_on
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run scoreboard players set #spawnT room 10
execute in minecraft:overworld unless function rlk:mboss/ar/ensure run return run function rlk:mboss/cb/wait
function rlk:mboss/start_go
''')
w('cb/wait', '''
# @s = zone marker: the arena is not ready yet (being built or restored, its chunks loading, or another arena's job
# running). Retry in 10 t; 7 misses in a row while no job runs (#mbArBuild 0) or 60 retries in all cancel (the gate
# returns with the same cprep).
scoreboard players add #cbWait mb 1
execute if score #cbWait mb matches 60.. run return run function rlk:mboss/start_cancel
execute if score #mbArBuild mb matches 1.. run return run scoreboard players set #spawnT room 10
scoreboard players add #mbLd mb 1
execute if score #mbLd mb matches ..6 run return run scoreboard players set #spawnT room 10
function rlk:mboss/start_cancel
''')
w('cb/body', '''
# The chapter boss's hitbox body (the module's spawn hook calls this instead of mboss/body; at the spawn point, context
# yaw = facing): as mboss/body WITHOUT miniboss (the boss economy: gold x15 x chapter, 2 sapphires, combat/gold_drop),
# rlk_mb_big when cur.px (proxy redirect, px/dup), rlk_mb_noshield when cur.shield is 0b (no click box in any state).
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_mboss","boss","rlk_mb_body","rlk_mb_inv","rlk_mb_bnew"],PersistenceRequired:1b,NoAI:1b,NoGravity:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_mb_bnew,limit=1] run tp @s ~ ~ ~ ~ 0
execute if data storage rlk:mboss cur{px:1b} run tag @e[tag=rlk_mb_bnew] add rlk_mb_big
execute if data storage rlk:mboss cur{shield:0b} run tag @e[tag=rlk_mb_bnew] add rlk_mb_noshield
execute as @e[tag=rlk_mb_bnew,limit=1] at @s run function rlk:mboss/body_setup
tag @e[tag=rlk_mb_bnew] remove rlk_mb_bnew
''')
w('cb/clear', '''
# @s = the chapter zone marker, at it (from room/combat_clear: the body is gone, #combat 0). Killed: the next-chapter
# object (room/obj/k_chapter); cancelled: cb/won put the gate back.
execute store result score #cbW mb run function rlk:mboss/cb/won
execute if score #cbW mb matches 1 run function rlk:room/obj/k_chapter
''')
w('cb/won', '\n'.join([
    '# @s = the chapter zone marker, at it. Gold left in the arena goes to the player, the fight ends, the player returns,',
    '# the arena forceload goes (and its barrier band, when the arena entry has sweep). No reward boxes (chapter rewards are',
    '# the kill\'s gold x15 x chapter and 2 sapphires). Returns 1 when killed (#mbKilled 1), 0 when cancelled (gate back).',
    'scoreboard players operation #mbWas mb = #mbOn mb',
    'execute in minecraft:overworld run function rlk:mboss/ar/box_absorb',
    'function rlk:mboss/cleanup_fight',
    'execute unless data storage rlk:mboss ret.x run function rlk:mboss/ret_here',
    'execute if score #mbWas mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/tp_out']
    + [f'execute if score #mbAr mb matches {a["n"]} in minecraft:overworld run function rlk:mboss/arena/{aid}/sweep {{y0:{a["sweep"]["y0"]},y1:{a["sweep"]["y1"]}}}'
       for aid, a in ARENAS if aid != 'plaza' and 'sweep' in a]
    + ['# the forceload goes; ar/<aid>/fl_off first aborts a running job of the fight arena (a module look swap, a rebuild:',
       '# without the chunks it would only wait and refuse every gate press for 200 t; cm.md 12); ensure restarts it at the',
       '# next press',
       'execute in minecraft:overworld run function rlk:mboss/ar/fl_off',
       'execute if score #mbKilled mb matches 1 run return run function rlk:mboss/cb/won_kill',
       'function rlk:mboss/cb/won_cancel',
       'return 0']))
w('cb/won_kill', '''
# The chapter boss was killed (@s = zone marker): title, the test replay links, forget. Returns 1.
title @a[tag=player] times 8 50 14
title @a[tag=player] subtitle {text:"다음 챕터로 가는 길이 열렸습니다",color:"#FFE08A"}
title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]
scoreboard players set @a[tag=player] vBig 72
scoreboard players set @a[tag=player] ttlT 72
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
return 1
''')
w('cb/won_cancel', CT.join(['''
# The fight was cancelled (no kill: /kill, a failed spawn, a reload that lost the body, test/abort): no reward, the gate
# comes back at the zone centre with the same cprep (same texts, same per-map state). Returns nothing (cb/won returns 0).
tellraw @a[tag=player] ''', gray('보스 전투가 취소되었습니다. (보상 없음) 문 오브젝트를 다시 누르면 재도전합니다.') + ''']
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
function rlk:room/obj/k_cboss
''']))
w('cb/lose', '''
# Objective loss (callable from anywhere, cm.md 5.8): the normal death path (run/fail, or test/defeat in a test; a Ronova
# revive applies as for any death). #mbLost stays 1 through a revive and is reset by the next fight_vars / cleanup_fight.
scoreboard players set #mbLost mb 1
scoreboard players set @a[tag=player] curHealth 0
''')
w('cb/run_reset', '''
# From run/start and run/end (also test end): no forced chapter boss, no auto gate press, no per-map chapter state.
scoreboard players set #cbForce mb 0
scoreboard players set #cbAuto mb 0
data remove storage rlk:mboss cprep
data remove storage rlk:mboss cbpeek
''')
w('cb/remove', '\n'.join(
    ['# From room/remove (in minecraft:overworld): every chapter arena cleared (when loaded), its forceload released; a',
     '# running arena job is aborted first.',
     'execute if score #mbArBuild mb matches 1.. run function rlk:mboss/arena/abort']
    + [f'function rlk:mboss/arena/{aid}/sweep {{y0:{a["sweep"]["y0"]},y1:{a["sweep"]["y1"]}}}' for aid, a in ARENAS if aid != 'plaza' and 'sweep' in a]
    + [ln for aid, _ in ARENAS if aid != 'plaza' for ln in (f'function rlk:mboss/arena/{aid}/clear', f'function rlk:mboss/ar/{aid}/fl_off')]))
w('cb/peek', '\n'.join(
    ['# Optional (cm.md 5.10): rlk:mboss cbpeek = the chapter boss the boss map of #chapter room routes to (none = Raiden).',
     'data remove storage rlk:mboss cbpeek']
    + [f'execute if score #chapter room matches {c} run return run data modify storage rlk:mboss cbpeek set value '
       f'{{id:"{bid}",name:{L.snbt_str(next(b for b in CHAPS if b["id"] == bid)["name"])},color:"{next(b for b in CHAPS if b["id"] == bid)["color"]}"}}'
       for c, _, bid in ROUTED]))

# ---------------------------------------------------------------------------------------------
# C. Pools, floor, title, RES, cine, music (cm.md 7, 8, 10, 13.7)
w('repool', '''
# {pct} (as anything; 1..100): the body's pool = #mbTot x pct / 100 (overflow-safe), full; the HP bar refills over 30 t
# (#mbRamp, mboss/bars). #mbPoolPct remembers the split (test/level re-applies it).
$scoreboard players set #mbPoolPct mb $(pct)
execute if score #mbPoolPct mb matches ..0 run scoreboard players set #mbPoolPct mb 1
execute if score #mbPoolPct mb matches 101.. run scoreboard players set #mbPoolPct mb 100
scoreboard players operation #t mb = #mbTot mb
execute if score #t mb matches 10000000.. run scoreboard players operation #t mb /= #c100 mb
scoreboard players operation #t mb *= #mbPoolPct mb
execute if score #mbTot mb matches ..9999999 run scoreboard players operation #t mb /= #c100 mb
execute if score #t mb matches ..0 run scoreboard players set #t mb 1
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation @s mhpM = #t mb
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation @s mhpC = #t mb
scoreboard players set #mbRamp mb 30
''')
w('title', '''
# {title,sub,color}: the fight's title (boss bar name line) and sub (gate subtitle); the bars pick it up next tick.
$data modify storage rlk:mboss cur.title set value {text:"$(title)",color:"$(color)",bold:true}
$data modify storage rlk:mboss cur.sub set value "$(sub)"
''')
w('floor', '''
# @s = the body inside combat/apply_mods, after the module's incoming hook (cb/inc/<id>; modules never call this).
# #mbFloor mb >= 1 (absolute HP, set by the module): #mbFloorRaw = the unclamped #dmg; a hit with mhpC - raw <= #mbFloor
# sets #mbFloorHit 1 (the module clears it); #dmg = max(0, min(#dmg, mhpC - #mbFloor)). True damage never gets here.
execute unless score #mbFloor mb matches 1.. run return 0
scoreboard players operation #mbFloorRaw mb = #dmg tmp
scoreboard players operation #t mb = @s mhpC
scoreboard players operation #t mb -= #dmg tmp
execute if score #t mb <= #mbFloor mb run scoreboard players set #mbFloorHit mb 1
scoreboard players operation #t mb = @s mhpC
scoreboard players operation #t mb -= #mbFloor mb
scoreboard players operation #dmg tmp < #t mb
execute if score #dmg tmp matches ..-1 run scoreboard players set #dmg tmp 0
''')
w('res_set', '\n'.join(
    ['# @s = a body (body_setup) with cur.res: per-element RES mbRes0..8 from the registry ("*" = the rest), tag',
     '# rlk_mb_resel (combat/apply runs mboss/res_pre for it), mres = the physical one until the first hit.']
    + [f'execute store result score @s mbRes{k} run data get storage rlk:mboss cur.res[{k}]' for k in range(9)]
    + ['tag @s add rlk_mb_resel', 'scoreboard players operation @s mres = @s mbRes0']))
w('res_pre', '\n'.join(
    ['# @s = a rlk_mb_resel entity inside combat/apply (not true damage), after element/on_hit and before the module on_hit:',
     '# mres = mbRes<#elem> (a module on_hit may override). Reactions, amplified hits and DoTs come back with their own #elem.']
    + [f'execute if score #elem tmp matches {k} run scoreboard players operation @s mres = @s mbRes{k}' for k in range(9)]))
w('aux/res_el', '\n'.join(
    ['# @s = a new aux (aux/setup) with #auxResEl mb 0..8: mbRes0..8 = #auxRes, mbRes<#auxResEl> = #auxResElV, rlk_mb_resel.']
    + [f'scoreboard players operation @s mbRes{k} = #auxRes mb' for k in range(9)]
    + [f'execute if score #auxResEl mb matches {k} run scoreboard players operation @s mbRes{k} = #auxResElV mb' for k in range(9)]
    + ['tag @s add rlk_mb_resel']))
w('cine/start', '''
# Cine on (cm.md 13.7): boss hits on the player (mboss/hurt, pl_dot) are refused; the bars stay; the module freezes its AI.
scoreboard players set #mbCine mb 1
''')
w('cine/end', '''
scoreboard players set #mbCine mb 0
''')
w('music/set', '''
# {ph} (int 0..9): play the registry track cur.music."<ph>" (record category, at each player, non-positional stereo
# event); 0 or no such phase stops the music. Looped by music/tick when len >= 1; vanilla music is stopped every 100 t.
$scoreboard players set #t mb $(ph)
execute unless score #t mb matches 1..9 run return run function rlk:mboss/music/stop
$execute unless data storage rlk:mboss cur.music."$(ph)".ev run return run function rlk:mboss/music/stop
execute if data storage rlk:mboss mus.ev run function rlk:mboss/music/off with storage rlk:mboss mus
$data modify storage rlk:mboss mus set value {ph:$(ph),ev:"",len:0}
$data modify storage rlk:mboss mus.ev set from storage rlk:mboss cur.music."$(ph)".ev
$data modify storage rlk:mboss mus.len set from storage rlk:mboss cur.music."$(ph)".len
$scoreboard players set #mbMusPh mb $(ph)
scoreboard players set #mbMusT mb 0
execute store result score #mbMusLen mb run data get storage rlk:mboss mus.len
function rlk:mboss/music/play with storage rlk:mboss mus
''')
w('music/play', '''
# (macro ev) the track from its start, at every player (record category, volume 1): vanilla background music stops.
stopsound @a[tag=player] music
$execute as @a[tag=player] at @s run playsound $(ev) record @s ~ ~ ~ 1 1 1
''')
w('music/off', '''
# (macro ev) stop the sound of the current track (no state change).
$stopsound @a[tag=player] record $(ev)
''')
w('music/stop', '''
# Stop the music (no fade; a sting is the caller's): the sound, #mbMusPh 0, rlk:mboss mus removed.
execute if data storage rlk:mboss mus.ev run function rlk:mboss/music/off with storage rlk:mboss mus
scoreboard players set #mbMusPh mb 0
scoreboard players set #mbMusT mb 0
data remove storage rlk:mboss mus
''')
w('music/halt', '''
# The pause edge: the sound stops, #mbMusPh and mus stay (mboss/resume restarts the phase track from its start).
execute if data storage rlk:mboss mus.ev run function rlk:mboss/music/off with storage rlk:mboss mus
''')
w('music/tick', '''
# From mboss/world (live, unpaused ticks) while #mbMusPh >= 1: the loop timer and the vanilla-music suppression.
scoreboard players add #mbMusT mb 1
execute if score #mbMusLen mb matches 1.. if score #mbMusT mb >= #mbMusLen mb run function rlk:mboss/music/loop
scoreboard players operation #t mb = #mbMusT mb
scoreboard players operation #t mb %= #c100 mb
execute if score #t mb matches 0 run stopsound @a[tag=player] music
''')
w('music/loop', '''
scoreboard players set #mbMusT mb 0
execute if data storage rlk:mboss mus.ev run function rlk:mboss/music/off with storage rlk:mboss mus
execute if data storage rlk:mboss mus.ev run function rlk:mboss/music/play with storage rlk:mboss mus
''')

# ---------------------------------------------------------------------------------------------
# D. Player-status and motion helpers (cm.md 13)
w('pl_dot', '''
# One player DoT tick (cm.md 13.4), as anything: #mbDotPct mb = per mille of the player's max HP, #mbDotEl mb = #elem for
# the shields (an element shield of the same element absorbs at 250 %), #mbDotLethal mb 0 = the player keeps >= 1 HP.
# Guard shield, then the element shield; no defence; dash i-frames do not block it; hurt fx. Output #mbDotDmg (HP lost).
# Refused (nothing, #mbDotDmg 0) while dead, reviving, on a selection screen, the boss dying (#mbSt 2) or #mbCine 1.
scoreboard players set #mbDotDmg mb 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run function rlk:mboss/pl_dot_end
execute if entity @a[tag=player,scores={rnDie=1..}] run return run function rlk:mboss/pl_dot_end
execute if entity @a[tag=player,scores={pkMode=1..}] run return run function rlk:mboss/pl_dot_end
execute if score #mbSt mb matches 2 run return run function rlk:mboss/pl_dot_end
execute if score #mbCine mb matches 1 run return run function rlk:mboss/pl_dot_end
execute as @a[tag=player,limit=1] at @s run function rlk:mboss/pl_dot2
function rlk:mboss/pl_dot_end
''')
w('pl_dot_end', '''
# Every pl_dot input is reset after the call, refused or not (a stale value never leaks into the next caller). A one-shot
# #mbNoRx the caller set for this tick is spent here too (pl_dot never runs a player reaction), so it cannot reach the
# next direct mboss/hurt.
scoreboard players set #mbDotPct mb 0
scoreboard players set #mbDotEl mb 0
scoreboard players set #mbDotLethal mb 0
scoreboard players set #mbNoRx mb 0
''')
w('pl_dot2', '''
# @s = player (modelled on F:player/hurt_elem).
scoreboard players operation #mbDI mb = @s dashInvT
scoreboard players set @s dashInvT 0
scoreboard players operation #dmgIn tmp = @s maxHealth
scoreboard players operation #dmgIn tmp *= #mbDotPct mb
scoreboard players operation #dmgIn tmp /= #c1000 mb
execute if score #dmgIn tmp matches ..0 run scoreboard players set #dmgIn tmp 1
scoreboard players operation #elem tmp = #mbDotEl mb
function rlk:engravings/guard/absorb
function rlk:element/shield_absorb
scoreboard players operation #t mb = @s curHealth
scoreboard players remove #t mb 1
execute if score #t mb matches ..-1 run scoreboard players set #t mb 0
execute if score #mbDotLethal mb matches 0 run scoreboard players operation #dmgIn tmp < #t mb
execute if score #dmgIn tmp matches 1.. run scoreboard players operation @s curHealth -= #dmgIn tmp
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 0
execute if score #dmgIn tmp matches 1.. run scoreboard players operation #mbDotDmg mb = #dmgIn tmp
scoreboard players operation #hurtDmg tmp = #mbDotDmg mb
execute if score #hurtDmg tmp matches 1.. at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/hurt_do
scoreboard players operation @s dashInvT = #mbDI mb
''')
w('hz/mask', '''
# Mask hazard (kind 6, cm.md 13.6): hits a player whose feet are not within R0 + 0.3 b (horizontal) of any rlk_mb_hzsafe
# marker of its safe group; no radius limit; volley groups, #hzNoDodge, #hzRearm, the height band and NoRx as the other
# kinds; never drawn by the framework (the module / kit draws it). Options: #hzR0 mb = R0 (tenths), #hzSafeG mb = the
# safe group (0 = this hazard's own id mbHzI = #hzLast after the call). Safe markers: rlk_room rlk_mb_aux rlk_mb_hzsafe
# with mbHzSG = the group, made by the module after the call. Call: function rlk:mboss/hz/mask {tell:..,dmg:..}
scoreboard players set #hzR mb 0
scoreboard players set #hzK mb 6
$scoreboard players set #hzW mb $(tell)
$scoreboard players set #hzD mb $(dmg)
function rlk:mboss/hz/make
''')
w('hz/init_mask', '''
# @s = a new mask hazard: the safe distance squared with the 0.3 b pad, milliblocks.
scoreboard players operation #t mb = @s mbHzR0
scoreboard players add #t mb 300
scoreboard players operation @s mbHzRI = #t mb
scoreboard players operation @s mbHzRI *= #t mb
''')
w('hz/hit_mask', '''
# @s = a mask hazard inside its active window (height band passed): safe when the body is near a safe marker of its group.
scoreboard players set #hzSafe mb 0
execute unless function rlk:mboss/mv/plpos run return 0
scoreboard players operation #bx mb = #mbPX mb
scoreboard players operation #bz mb = #mbPZ mb
scoreboard players operation #hzG2 mb = @s mbHzSG
scoreboard players operation #hzRI2 mb = @s mbHzRI
execute as @e[type=minecraft:marker,tag=rlk_mb_hzsafe] if score @s mbHzSG = #hzG2 mb run function rlk:mboss/hz/mask_one
execute if score #hzSafe mb matches 0 run function rlk:mboss/hz/hurt
''')
w('hz/mask_one', '''
# @s = a safe marker of the group: horizontal distance squared to the body (overflow-safe inside 32 b) <= (R0 + 0.3)^2.
execute if score #hzSafe mb matches 1 run return 0
execute store result score #dx mb run data get entity @s Pos[0] 1000
scoreboard players operation #dx mb -= #bx mb
execute store result score #dz mb run data get entity @s Pos[2] 1000
scoreboard players operation #dz mb -= #bz mb
execute unless score #dx mb matches -32000..32000 run return 0
execute unless score #dz mb matches -32000..32000 run return 0
scoreboard players operation #r2 mb = #dx mb
scoreboard players operation #r2 mb *= #dx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #dz mb
scoreboard players operation #r2 mb += #t mb
execute if score #r2 mb <= #hzRI2 mb run scoreboard players set #hzSafe mb 1
''')
w('hz/mask_end', '''
# @s = an expiring mask hazard with its own safe group (made with #hzSafeG 0): its safe markers go with it.
scoreboard players operation #hzG2 mb = @s mbHzSG
execute as @e[type=minecraft:marker,tag=rlk_mb_hzsafe] if score @s mbHzSG = #hzG2 mb run kill @s
''')
w('hz/extend', '''
# {n} (as a live hazard marker; cm.md 13.8): its active window and its life grow by n ticks (a lingering field refresh).
$scoreboard players add @s mbHzA $(n)
$scoreboard players add @s mbHzL $(n)
''')
# AP-FW (2026-10-21, cm.md 13.6, 13.11, 13.12): the framework gaps Apep's FN list left after AZ-CM.
w('hz/safe_new', '''
# A new mask safe group in #mbSafeG mb (cm.md 13.6, APEP-04): -1, -2, ... (back to -1 after -999 999), a number space of
# its own: hazard ids (mbHzI, also the default group of a mask made with #hzSafeG 0) are >= 1, so neither a mask of
# another group nor an expiring mask ever matches it. Copy it into #hzSafeG before each mask of the group
# (L.hz_opts(safe_g='cur')) and into mbHzSG of the group's safe markers; the module removes those markers itself.
scoreboard players remove #mbSafeN mb 1
execute unless score #mbSafeN mb matches -999999..-1 run scoreboard players set #mbSafeN mb -1
scoreboard players operation #mbSafeG mb = #mbSafeN mb
''')
w('hz/init_pm', '''
# @s = a new hazard made with #hzPm mb (cm.md 13.11): its hit takes mbHzPm per mille (1..1000) of the player's max HP
# through mboss/pl_dot; lethal unless #hzPmL mb 0 (unset = 1), which is spent here.
scoreboard players operation @s mbHzPm = #hzPm mb
execute if score @s mbHzPm matches 1001.. run scoreboard players set @s mbHzPm 1000
scoreboard players set @s mbHzPmL 1
execute if score #hzPmL mb matches 0 run scoreboard players set @s mbHzPmL 0
scoreboard players reset #hzPmL mb
''')
w('hz/hurt_pm', '''
# @s = a per-mille hazard (cm.md 13.11) that reached the player; hz/hurt has marked it hit (and re-armed it). The hit is a
# mboss/pl_dot of mbHzPm per mille of the player's max HP (the hazard's element for the shields, lethal per mbHzPmL; no
# defence, no level factor, no player-side reaction, no knockback) instead of mboss/hurt. Without #hzNoDodge the dash
# i-frames dodge it (#dodged 1, a dodge event; consumed as any hazard hit). Hit / dodge events and the volley group as
# mboss/hurt (source 1); refused while dead, reviving, selecting or with the boss dying (as mboss/hurt).
scoreboard players set #dodged tmp 0
scoreboard players set #mbSrcIn mb 1
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if score #mbSt mb matches 2 run return 0
execute if score @s mbHzND matches 0 as @a[tag=player,scores={dashInvT=1..},limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/dash_iframe
execute if score #dodged tmp matches 1 run return run function rlk:mboss/hurt_dodge
scoreboard players set #mbShIn mb 0
execute if entity @a[tag=player,scores={shieldHP=1..},limit=1] run scoreboard players set #mbShIn mb 1
execute if entity @a[tag=player,scores={gShield=1..},limit=1] run scoreboard players set #mbShIn mb 1
scoreboard players operation #mbDotPct mb = @s mbHzPm
scoreboard players operation #mbDotEl mb = @s mbHzE
scoreboard players operation #mbDotLethal mb = @s mbHzPmL
function rlk:mboss/pl_dot
scoreboard players operation #cmEl tmp = @s mbHzE
function rlk:mboss/hurt_ev
scoreboard players operation #g mb = @s mbHzG
execute if score #g mb matches 1.. run function rlk:mboss/grp_mark
''')
w('aux/shield_pre', '''
# @s = a new aux made with #auxShW mb (aux/setup, cm.md 13.12): its click shield made now, #auxShW x #auxShH tenths of a
# block (#auxShH unset = 22), linked by msid and marked synced, so mob/shield_ensure keeps it (no 1.2 x 2.2 default).
execute unless score @s msid matches 1.. run scoreboard players add #msidC tmp 1
execute unless score @s msid matches 1.. run scoreboard players operation @s msid = #msidC tmp
summon minecraft:interaction ~ ~ ~ {Tags:["rlk_mshield","rlk_msync","rlk_mb_shnew"],width:1.2f,height:2.2f,response:false}
scoreboard players operation @e[type=minecraft:interaction,tag=rlk_mb_shnew,limit=1] msid = @s msid
execute store result entity @e[type=minecraft:interaction,tag=rlk_mb_shnew,limit=1] width float 0.1 run scoreboard players get #auxShW mb
execute if score #auxShH mb matches 1.. store result entity @e[type=minecraft:interaction,tag=rlk_mb_shnew,limit=1] height float 0.1 run scoreboard players get #auxShH mb
tag @e[type=minecraft:interaction,tag=rlk_mb_shnew] remove rlk_mb_shnew
''')
w('aux/hb_y', '''
# @s = a new aux made with #auxHbY mb (aux/setup after mob/setup, cm.md 13.12): its HP-bar passengers (mob/hb_spawn: bar,
# fill, number at 0.25 b, level 0.43 b, icon 0.82 b) moved up by #auxHbY tenths of a block (negative = down).
scoreboard players operation #t mb = #auxHbY mb
scoreboard players operation #t mb *= #c10 mb
scoreboard players add #t mb 25
execute on passengers if entity @s[tag=rlk_hb_bg] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
execute on passengers if entity @s[tag=rlk_hb_fg] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
execute on passengers if entity @s[tag=rlk_hb_num] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
scoreboard players add #t mb 18
execute on passengers if entity @s[tag=rlk_hb_lv] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
scoreboard players add #t mb 39
execute on passengers if entity @s[tag=rlk_hb_icon] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
''')
w('mv/step_flat', '''
# {spd} (blocks per call, a decimal: L.step_flat; cm.md 13.12) as @s = a ground walker (an aux husk, a marker), rotated =
# its heading (the caller faces the target: execute as <e> at @s facing entity <target> feet run function
# rlk:mboss/mv/step_flat {spd:0.3}): turns to the heading (yaw only), steps forward, stands on the fight arena's floor
# (the y of its rlk_mb_arena marker), is pulled inside walk - 0.7 (ar/clampw). No collision test: the arena floor is flat.
$execute rotated ~ 0 positioned ^ ^ ^$(spd) run tp @s ~ ~ ~ ~ 0
execute store result entity @s Pos[1] double 0.001 run data get entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] Pos[1] 1000
function rlk:mboss/ar/clampw
''')
w('mv/lv_sample', '''
# From mboss/world (chapter fights, live and unpaused): the lockv ring buffer rlk:mboss lv[0..5] (oldest .. newest) of
# the player's body x / z in milliblocks; a tick while the player dashes (dashMoveT >= 1) is skipped (cm.md 13.1).
execute if entity @a[tag=player,scores={dashMoveT=1..},limit=1] run return 0
execute unless function rlk:mboss/mv/plpos run return 0
scoreboard players operation #lx mb = #mbPX mb
scoreboard players operation #lz mb = #mbPZ mb
execute unless data storage rlk:mboss lv[5] run function rlk:mboss/mv/lv_fill
data modify storage rlk:mboss lv append value {x:0,z:0}
data remove storage rlk:mboss lv[0]
execute store result storage rlk:mboss lv[5].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[5].z int 1 run scoreboard players get #lz mb
scoreboard players add #mbQi mb 1
execute if score #mbQi mb matches 6.. run scoreboard players set #mbQi mb 0
''')
w('mv/lv_fill', '''
# An empty (or short) buffer: six copies of this sample.
data modify storage rlk:mboss lv set value [{x:0,z:0},{x:0,z:0},{x:0,z:0},{x:0,z:0},{x:0,z:0},{x:0,z:0}]
''' + ''.join(f'execute store result storage rlk:mboss lv[{i}].x int 1 run scoreboard players get #lx mb\n'
              f'execute store result storage rlk:mboss lv[{i}].z int 1 run scoreboard players get #lz mb\n' for i in range(6)))
isq = []
for _ in range(12):
    isq += ['scoreboard players operation #t mb = #n mb', 'scoreboard players operation #t mb /= #mbV mb',
            'scoreboard players operation #mbV mb += #t mb', 'scoreboard players operation #mbV mb /= #c2 mb',
            'execute if score #mbV mb matches ..0 run scoreboard players set #mbV mb 1']
w('mv/lockv', '\n'.join([
    '# {lead} (as anything; cm.md 13.1): v = (newest - oldest) / 5 of the ring buffer in mb/t, |v| capped at 280 (sprint):',
    '# #mbVx #mbVz = v, #mbV = |v|; the old rlk_mb_lock marker dies and a new one (rlk_room rlk_mb_aux rlk_mb_lock) stands at',
    '# the player + v x lead, y = the arena centre, pulled inside walk - 0.7 (ar/clampw). A module that keeps the marker',
    '# removes rlk_mb_lock from it (the next lockv kills a tagged one).',
    'execute unless function rlk:mboss/mv/plpos run return fail',
    'scoreboard players operation #lx mb = #mbPX mb',
    'scoreboard players operation #lz mb = #mbPZ mb',
    'execute unless data storage rlk:mboss lv[5] run function rlk:mboss/mv/lv_fill',
    'execute store result score #mbVx mb run data get storage rlk:mboss lv[5].x',
    'execute store result score #t mb run data get storage rlk:mboss lv[0].x',
    'scoreboard players operation #mbVx mb -= #t mb',
    'scoreboard players set #t mb 5',
    'scoreboard players operation #mbVx mb /= #t mb',
    'execute store result score #mbVz mb run data get storage rlk:mboss lv[5].z',
    'execute store result score #t mb run data get storage rlk:mboss lv[0].z',
    'scoreboard players operation #mbVz mb -= #t mb',
    'scoreboard players set #t mb 5',
    'scoreboard players operation #mbVz mb /= #t mb',
    '# |v| (integer Newton square root; a teleport-sized jump is clamped before squaring)',
    'execute if score #mbVx mb matches 20001.. run scoreboard players set #mbVx mb 20000',
    'execute if score #mbVx mb matches ..-20001 run scoreboard players set #mbVx mb -20000',
    'execute if score #mbVz mb matches 20001.. run scoreboard players set #mbVz mb 20000',
    'execute if score #mbVz mb matches ..-20001 run scoreboard players set #mbVz mb -20000',
    'scoreboard players operation #n mb = #mbVx mb', 'scoreboard players operation #n mb *= #mbVx mb',
    'scoreboard players operation #t mb = #mbVz mb', 'scoreboard players operation #t mb *= #mbVz mb',
    'scoreboard players operation #n mb += #t mb',
    'scoreboard players set #mbV mb 0',
    'execute if score #n mb matches 1.. run function rlk:mboss/mv/lv_sqrt',
    'execute if score #mbV mb matches 281.. run function rlk:mboss/mv/lv_cap',
    '# lock point = the player + v x lead (milliblocks), y = the arena centre',
    '$scoreboard players set #t mb $(lead)',
    'scoreboard players operation #lx2 mb = #mbVx mb', 'scoreboard players operation #lx2 mb *= #t mb',
    'scoreboard players operation #lx2 mb += #lx mb',
    'scoreboard players operation #lz2 mb = #mbVz mb', 'scoreboard players operation #lz2 mb *= #t mb',
    'scoreboard players operation #lz2 mb += #lz mb',
    'kill @e[type=minecraft:marker,tag=rlk_mb_lock]',
    'execute at @e[tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_lock","rlk_mb_locknew"]}',
    'execute store result entity @e[type=minecraft:marker,tag=rlk_mb_locknew,limit=1] Pos[0] double 0.001 run scoreboard players get #lx2 mb',
    'execute store result entity @e[type=minecraft:marker,tag=rlk_mb_locknew,limit=1] Pos[2] double 0.001 run scoreboard players get #lz2 mb',
    'execute as @e[type=minecraft:marker,tag=rlk_mb_locknew,limit=1] run function rlk:mboss/ar/clampw',
    'tag @e[type=minecraft:marker,tag=rlk_mb_locknew] remove rlk_mb_locknew',
    'return 1']))
w('mv/lv_sqrt', '\n'.join(['# #mbV = isqrt(#n) (#n >= 1), 12 Newton steps from 1000.', 'scoreboard players set #mbV mb 1000'] + isq))
w('mv/lv_cap', '''
# |v| > 280 mb/t: v x 280 / |v|.
scoreboard players operation #mbVx mb *= #c280 mb
scoreboard players operation #mbVx mb /= #mbV mb
scoreboard players operation #mbVz mb *= #c280 mb
scoreboard players operation #mbVz mb /= #mbV mb
scoreboard players set #mbV mb 280
''')
w('mv/plpos', '''
# (anywhere; cm.md 13.2, CM-REVIEW PERF-4) #mbPX / #mbPZ mb = the player's body x / z in milliblocks, read from the body
# (a player: every entity NBT read saves the whole player) once per game tick, in one read (Pos -> rlk:mboss plp); later
# calls in the same tick reuse it. Fails when there is no body. A chapter-runtime teleport of the player in the tick
# (push/capsule, the chapter arena's tp_in) sets #mbPlG -1, so the next call reads again.
execute store result score #plG mb run time query gametime
execute if score #plG mb = #mbPlG mb run return 1
execute unless entity @e[tag=rlk_body,limit=1] run return fail
data modify storage rlk:mboss plp set from entity @e[tag=rlk_body,limit=1] Pos
execute store result score #mbPX mb run data get storage rlk:mboss plp[0] 1000
execute store result score #mbPZ mb run data get storage rlk:mboss plp[2] 1000
scoreboard players operation #mbPlG mb = #plG mb
return 1
''')
w('mv/local', '''
# As the anchor (the body; cm.md 13.2): #mbLf / #mbLs mb = the player's body in the anchor frame, milliblocks (f forward
# along the anchor yaw, s = the anchor's left), the hz/hit projection on an exact forward axis (no trigonometry).
scoreboard players set #mbLf mb 0
scoreboard players set #mbLs mb 0
execute unless function rlk:mboss/mv/plpos run return fail
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_lcax"]}
execute store result score #ox mb run data get entity @s Pos[0] 1000
execute store result score #oz mb run data get entity @s Pos[2] 1000
execute store result score #fx mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_lcax,limit=1] Pos[0] 1000
execute store result score #fz mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_lcax,limit=1] Pos[2] 1000
kill @e[type=minecraft:marker,tag=rlk_mb_lcax]
scoreboard players operation #fx mb -= #ox mb
scoreboard players operation #fz mb -= #oz mb
scoreboard players operation #dx mb = #mbPX mb
scoreboard players operation #dz mb = #mbPZ mb
scoreboard players operation #dx mb -= #ox mb
scoreboard players operation #dz mb -= #oz mb
scoreboard players operation #mbLf mb = #dx mb
scoreboard players operation #mbLf mb *= #fx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #fz mb
scoreboard players operation #mbLf mb += #t mb
scoreboard players operation #mbLf mb /= #c1000 mb
scoreboard players operation #mbLs mb = #dx mb
scoreboard players operation #mbLs mb *= #fz mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #fx mb
scoreboard players operation #mbLs mb -= #t mb
scoreboard players operation #mbLs mb /= #c1000 mb
return 1
''')

# ---------------------------------------------------------------------------------------------
# E. Hit proxies (cm.md 9): the shared redirect / de-dupe (px/hit, px/dup) and the per-boss runtime compiled from the
#    rig manifests (px_build below).
w('px/hit', '''
# From the top of combat/apply (@s = a hit proxy, at it). One attack event = one hit on the body (cm.md 9.6): a second
# hit in the same game tick with the same #atkSeq is swallowed (no number, no reaction); else the hit is re-run as the
# body at the proxy (the number shows here) with #pxIn 1, and #mbPart / #mbPartGT record the proxy.
execute store result score #pxG mb run time query gametime
execute if score #pxG mb = #pxGT mb if score #atkSeq tmp = #pxSeq mb run return 0
scoreboard players operation #pxGT mb = #pxG mb
scoreboard players operation #pxSeq mb = #atkSeq tmp
scoreboard players operation #mbPart mb = @s mbPart
scoreboard players operation #mbPartGT mb = #pxG mb
scoreboard players set #pxIn mb 1
execute at @s as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:combat/apply
scoreboard players set #pxIn mb 0
return 1
''')
w('px/dup', '''
# From combat/apply (@s = a rlk_mb_big body hit directly, #pxIn 0, not true damage): the same de-dupe as px/hit with
# #mbPart 0. Returns 1 = go on with the hit, fail = swallow it (the same attack already hit through a proxy).
execute store result score #pxG mb run time query gametime
execute if score #pxG mb = #pxGT mb if score #atkSeq tmp = #pxSeq mb run return fail
scoreboard players operation #pxGT mb = #pxG mb
scoreboard players operation #pxSeq mb = #atkSeq tmp
scoreboard players set #mbPart mb 0
scoreboard players operation #mbPartGT mb = #pxG mb
return 1
''')

# ---------------------------------------------------------------------------------------------
# F. Chapter test commands (cm.md 5.9)
w('test/chapter', '\n'.join(
    ['# /function rlk:mboss/test/chapter {id:"cproto"}: test/chapter_ch in the boss\'s first chapter (none: chapter 1).',
     '$data modify storage rlk:mboss tch set value "$(id)"']
    + [f'execute if data storage rlk:mboss {{tch:"{b["id"]}"}} run return run function rlk:mboss/test/chapter_ch {{id:"{b["id"]}",ch:{(b.get("ch") or [1])[0]}}}'
       for b in CHAPS]
    + ['$function rlk:mboss/test/chapter_ch {id:"$(id)",ch:1}']))
w('test/chapter_ch', CTT.join(['''
# /function rlk:mboss/test/chapter_ch {id:"cproto",ch:2}: a real boss map (#mapIdx 5, #mapType 8) of that chapter routed
# to the chapter boss (#cbForce, only under #mbTest 1): room/gen -> cb/route_force -> the entrance layout, the kind-9 zone
# built (-> cb/prep: cprep, forceload, the sliced arena job), the player in front of the gate (zone_enter -> k_cboss);
# test/cwait presses the gate as soon as no arena job runs (#cbAuto 1).
execute unless entity @s[tag=player] run return run tellraw @s {text:"[챕터 보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s ''', gray('던전 구역이 준비되지 않았습니다. 먼저 ') + ',' + link('/function rlk:room/setup') + ',' + gray(' 을 실행하세요.') + ''']
execute if score #active room matches 1 unless score #mbTest mb matches 1 run return run tellraw @s ''', gray('진행 중인 런이 있습니다. ') + ',' + link('/function rlk:run/stop') + ',' + gray(' 후 다시 실행하세요.') + ''']
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @s ''', gray("난이도가 '평화로움'이면 보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.") + ''']
execute if score @s dead matches 1 run return 0
$execute unless data storage rlk:mboss cbyid.$(id) run return run tellraw @s ''', gray('등록되지 않았거나 꺼진 챕터 보스입니다: $(id)') + ''']
$execute store result score #mbReqF mb run data get storage rlk:mboss cbyid.$(id).n
$data modify storage rlk:mboss tlast set value {id:"$(id)",ch:1,cb:1b}
$scoreboard players set #mbReqCh mb $(ch)
execute unless score #mbReqCh mb matches 1.. run scoreboard players set #mbReqCh mb 1
execute store result storage rlk:mboss tlast.ch int 1 run scoreboard players get #mbReqCh mb
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #mbTest mb 1
scoreboard players set #mbLock mb 0
scoreboard players set #mbForce mb 0
scoreboard players operation #cbForce mb = #mbReqF mb
scoreboard players set #cbAuto mb 1
scoreboard players set #active room 1
scoreboard players operation #chapter room = #mbReqCh mb
scoreboard players set #mapIdx room 5
scoreboard players set #mapType room 8
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
execute in minecraft:overworld run function rlk:room/gen
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=9,zst=0}] run function rlk:room/zone_build
execute in minecraft:overworld at @e[tag=rlk_zone,scores={zkind=9},limit=1] positioned ~ ~ ~4 run tp @s ~ ~ ~ 180 0
function rlk:view/sync
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zkind=9,zst=1}] at @s run function rlk:room/zone_enter
scoreboard players operation @s curHealth = @s maxHealth
tellraw @s ''', gray('챕터 보스 시험 전투를 시작합니다. 경기장이 준비되면 문을 자동으로 누릅니다.') + ''']
function rlk:mboss/test/chelp
scoreboard players set #cbWaitT mb 0
schedule function rlk:mboss/test/cwait 5t replace
''']))
w('test/cwait', '''
# Scheduled every 5 t after test/chapter_ch (at most 300 t): presses the gate once no arena job runs (#cbAuto 1).
execute unless score #cbAuto mb matches 1 run return 0
execute unless score #mbTest mb matches 1 run return run scoreboard players set #cbAuto mb 0
scoreboard players add #cbWaitT mb 5
execute if score #mbArBuild mb matches 0 if entity @e[tag=rlk_obj,scores={oact=16},limit=1] run return run function rlk:mboss/test/cpress
execute if score #cbWaitT mb matches 300.. run return run function rlk:mboss/test/ctimeout
schedule function rlk:mboss/test/cwait 5t replace
''')
w('test/cpress', '''
scoreboard players set #cbAuto mb 0
execute in minecraft:overworld as @e[tag=rlk_obj,scores={oact=16},limit=1] at @s run function rlk:mboss/cb/gate
''')
w('test/ctimeout', CTT.join(['''
scoreboard players set #cbAuto mb 0
tellraw @a[tag=player] ''', gray('경기장 준비 시간 초과 — 문을 직접 누르세요') + ''']
''']))
w('test/lose', CTT.join(['''
# The objective-loss path of the chapter mode (mboss/cb/lose): the normal death (test/defeat in a test).
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s ''', gray('진행 중인 보스가 없습니다.') + ''']
function rlk:mboss/cb/lose
''']))
CREPLAY = link('/function rlk:mboss/test/chapter_ch {id:"$(id)",ch:$(ch)}', '[다시 하기]')
w('test/cdefeat_msg', '$tellraw @s ' + CTT + gray('쓰러졌습니다. ') + ',' + CREPLAY + ']')
w('test/cwon_msg', '$tellraw @a[tag=player] ' + CTT + gray('처치! 다음 챕터 오브젝트가 나타났습니다. ') + ',' + CREPLAY
  + ',' + gray(' ') + ',' + link('/function rlk:mboss/test/stop', '[로비로]') + ']')
w('test/chelp', 'tellraw @s ' + CTT + gray('명령: ') + ',' + link('/function rlk:mboss/test/chapter {id:"cproto"}', 'chapter {id}') + ','
  + gray(' 챕터 보스 시험 · ') + ',' + link('/function rlk:mboss/test/chapter_ch {id:"cproto",ch:2}', 'chapter_ch {id,ch}') + ','
  + gray(' 챕터 지정 · ') + ',' + link('/function rlk:mboss/test/lose', 'lose') + ',' + gray(' 패배 경로 · kill / abort / pattern / lock / level / stop 공통') + ']')

# ---------------------------------------------------------------------------------------------
# Hit proxies (cm.md 9): the runtime of every proxy boss (registry px:true) compiled from its rig manifest (schema v1):
# the real T:mboss_<id>_rig_manifest.json ("source": "rig") merged per clip with the stub T:mboss_<id>/stub_rig_manifest.json
# (a static "source": "stub" file at the real path counts as the stub: cproto). Interactions with fixed UUIDs follow the
# anchor (the body) every tick at ^x ^ ^z of the pose the rig shows (clip_obj / tick_obj of the anchor).
PXB = [b for b in CHAPS if b.get('px')]
PX_MOVE = 0.15                  # a key is written when a sampled column moved more than this (x, z or top)
PX_UP = 0.3                     # a column at or below this is parked (hidden bone, sunk part)
PX_PARK = -8.0                  # parked proxies stand this far under the floor


def px_manifest(b):
    tools = L.ROOT / 'tools'
    real_p, stub_p = tools / f'mboss_{b["id"]}_rig_manifest.json', tools / f'mboss_{b["id"]}' / 'stub_rig_manifest.json'
    real = stub = None
    if real_p.exists():
        m = json.loads(real_p.read_text(encoding='utf-8'))
        if m.get('schema') == 1 and m.get('source') == 'rig':
            real = m
        elif m.get('schema') == 1 and m.get('source') == 'stub':
            stub = m
    if stub_p.exists():
        m = json.loads(stub_p.read_text(encoding='utf-8'))
        if m.get('schema') == 1:
            stub = m
    assert real or stub, f'px boss {b["id"]}: no schema-v1 rig manifest ({real_p.name} / {stub_p.relative_to(tools)})'
    G = ('proxies', 'uuids', 'states', 'capsules', 'runtime', 'functions')
    if real:
        merged = {k: real[k] for k in G if k in real}
        for k in G:
            if k not in merged and stub and k in stub:
                merged[k] = stub[k]
        have = {c['name'] for c in real['clips']}
        clips = list(real['clips']) + ([c for c in stub['clips'] if c['name'] not in have] if stub else [])
    else:
        merged = {k: stub[k] for k in G if k in stub}
        clips = list(stub['clips'])
    merged['clips'] = [c for c in clips if not c['name'].startswith('dbg_')]
    # AP-FW (APEP-09, manifest.md 1): a stub clip that falls back beside a real rig manifest carries an id >= 1000 (never a
    # rig id, so the rig's clip_obj can never select it by accident); the build fails otherwise
    if real and stub:
        low = sorted(c['name'] for c in merged['clips'] if c['name'] not in have and int(c['id']) < 1000)
        assert not low, (f'{b["id"]}: stub fallback clip(s) {low} merged beside the real rig manifest need ids >= 1000 '
                         '(manifest.md 1: stub ids are 1000 + k, never a rig id)')
    # a stub fallback clip merged beside the real clips must not reuse a real clip id (the px dispatch is keyed by id)
    cids = [c['id'] for c in merged['clips']]
    dup = sorted({i for i in cids if cids.count(i) > 1})
    assert not dup, f'{b["id"]}: clip id(s) {dup} used by two clips of the merged manifest (real + stub fallback clips need distinct ids)'
    lay = merged['proxies']['layout']
    assert 1 <= len(lay) <= 16, f'{b["id"]}: {len(lay)} proxies (at most 16)'
    pxb = int(b.get('pxBase', 65))
    for k, p in enumerate(lay):
        want = pxb + k
        assert p.get('idx', want) == want, f'{b["id"]}: proxy {p["name"]} idx {p.get("idx")} != pxBase + {k}'
        assert merged['uuids'].get('proxies', {}).get(p['name'], want) == want, f'{b["id"]}: uuids.proxies.{p["name"]}'
    for st in ('inv', 'dead'):
        assert st in merged['states'], f'{b["id"]}: state set {st} missing from the manifest'
    names = [p['name'] for p in lay]
    for st, sd in merged['states'].items():
        assert set(sd['px']) <= set(names), f'{b["id"]}: state {st} names unknown proxies'
        for c in sd.get('capsules', []):
            assert c in merged.get('capsules', {}), f'{b["id"]}: state {st} capsule {c}'
    return merged


def px_sample(clip, names):
    """[(t, {name: (x, z, top)})] for t = 0 .. len-1, linear between the clip's px keys (missing proxies: rest)."""
    keys = sorted((int(t), v) for t, v in clip.get('px', {}).get('keys', {}).items())
    out = []
    for t in range(int(clip['len'])):
        lo = max((k for k in keys if k[0] <= t), default=keys[0], key=lambda k: k[0])
        hi = min((k for k in keys if k[0] >= t), default=keys[-1], key=lambda k: k[0])
        f = 0.0 if hi[0] == lo[0] else (t - lo[0]) / (hi[0] - lo[0])
        row = {}
        for n in names:
            a, c = lo[1].get(n), hi[1].get(n)
            if a is None or c is None:
                continue
            row[n] = tuple(a[i] + (c[i] - a[i]) * f for i in range(3))
        out.append((t, row))
    return out


PX = {b['id']: px_manifest(b) for b in PXB}
for b in PXB:
    PX_STATES[b['id']] = list(PX[b['id']]['states'])


def px_build(b):
    bid, m = b['id'], PX[b['id']]
    P, F = f'px/{bid}/', f'rlk:mboss/px/{bid}/'
    lay = m['proxies']['layout']
    names = [p['name'] for p in lay]
    ints = m['uuids']['ints']
    block = m['uuids']['block']
    pxb = int(b.get('pxBase', 65))
    uu = [f'{block}{pxb + k:02x}' for k in range(len(lay))]
    rest = m['proxies'].get('rest', {})
    co, to = m['runtime']['clip_obj'], m['runtime']['tick_obj']
    tag_n = lambda n: f'rlk_mb_px_{n}'
    o0 = ','.join(f'{n}_x:{L.num(float(rest.get(n, [0, 0, 0])[0]))}d,{n}_y:{L.num(PX_PARK)}d,{n}_z:{L.num(float(rest.get(n, [0, 0, 0])[1]))}d' for n in names)
    t0 = ','.join(f'{n}:{L.num(float(rest.get(n, [0, 0, 1.0])[2]))}f' for n in names)
    sp = [f'# @s = the body of {bid} (anchor), at it: its {len(lay)} hit proxies (interactions, UUID block {block}.., low byte',
          f'# pxBase {pxb} + k) summoned parked, then the current state set (px.set; inv at a fight start) applied. A /reload',
          '# respawns them from rlk:mboss px (the offsets and tops of the last pose written).']
    sp += [f'kill {u}' for u in uu]
    sp += [f'execute unless data storage rlk:mboss px.o run data modify storage rlk:mboss px.o set value {{{o0}}}',
           f'execute unless data storage rlk:mboss px.top run data modify storage rlk:mboss px.top set value {{{t0}}}',
           'execute unless data storage rlk:mboss px.set run data modify storage rlk:mboss px.set set value "inv"']
    for k, p in enumerate(lay):
        ui = '[I;' + ','.join(str(i) for i in ints + [pxb + k]) + ']'
        sp += [f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^{L.num(PX_PARK)} ^ run summon minecraft:interaction ~ ~ ~ '
               f'{{UUID:{ui},Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","{tag_n(p["name"])}"],width:{L.num(float(p["w"]))}f,height:1.0f,response:false}}',
               f'scoreboard players set {uu[k]} mbPart {k + 1}',
               f'execute store result score #t mb run data get storage rlk:mboss px.top.{p["name"]} 100',
               f'scoreboard players set #pxU{k + 1} mb 0',
               f'execute if score #t mb matches {int(PX_UP * 100) + 1}.. run scoreboard players set #pxU{k + 1} mb 1',
               'execute if score #t mb matches ..10 run scoreboard players set #t mb 10',
               f'execute store result entity {uu[k]} height float 0.01 run scoreboard players get #t mb']
    sp += ['function rlk:mboss/px/state with storage rlk:mboss px']
    w(P + 'spawn', '\n'.join(sp))
    for k, p in enumerate(lay):
        n = p['name']
        w(P + f'on/{k + 1}', f'# Proxy {n} live: on the anchor floor, rlk_mob (targetable).\n'
          f'data modify storage rlk:mboss px.o.{n}_y set value 0.0d\ntag {uu[k]} add rlk_mob')
        w(P + f'off/{k + 1}', f'# Proxy {n} parked: {L.num(-PX_PARK)} b under the floor, no rlk_mob.\n'
          f'data modify storage rlk:mboss px.o.{n}_y set value {L.num(PX_PARK)}d\ntag {uu[k]} remove rlk_mob')
        w(P + f'ev/{k + 1}', f'# Proxy {n}: live iff in the current state set (#pxS{k + 1}) and its column top > {PX_UP} b (#pxU{k + 1}).\n'
          f'scoreboard players operation #t mb = #pxS{k + 1} mb\nscoreboard players operation #t mb *= #pxU{k + 1} mb\n'
          f'execute if score #t mb matches 1 run return run function {F}on/{k + 1}\nfunction {F}off/{k + 1}')
    fns = m.get('functions') or {}
    for st, sd in m['states'].items():
        caps = []
        for c in sd.get('capsules', []):
            cd = m['capsules'][c]
            caps.append('{f0:%d,f1:%d,hw:%d,px:%s,top:%d}' % (round(cd['f0'] * 10), round(cd['f1'] * 10), round(cd['hw'] * 10),
                                                            L.snbt_str(cd.get('px', '')), round(cd.get('top_max', 0) * 10)))
        lines = [f'# State set "{st}" of {bid}: membership, live / parked, the push capsules (tenths, anchor frame), the rig',
                 '# visibility, the inv rule (rlk_mb_inv only through rlk_mb_pxinv: an inv the body already has is never touched).',
                 f'data modify storage rlk:mboss px.set set value "{st}"']
        lines += [f'scoreboard players set #pxS{k + 1} mb {1 if n in sd["px"] else 0}' for k, n in enumerate(names)]
        lines += [f'function {F}ev/{k + 1}' for k in range(len(names))]
        lines.append('data modify storage rlk:mboss push set value [' + ','.join(caps) + ']')
        vis = sd.get('vis')
        if vis:
            st_fns = fns.get('state') if isinstance(fns, dict) else None
            vfn = (st_fns.get(vis) if isinstance(st_fns, dict) else None) or (m['runtime'].get('ns', f'rlk:mboss/{bid}/rig/') + 'state/' + vis)
            # always the literal call (the output never depends on which generator ran first): the rig / the module's
            # stand-in rig provides it (manifest.md 8), check_mboss_pack reports it when it is missing
            lines.append(f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function {vfn}')
        if sd.get('inv'):
            lines.append('execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] unless entity @s[tag=rlk_mb_inv] run function rlk:mboss/px/inv_on')
        else:
            lines.append('execute as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_pxinv,limit=1] run function rlk:mboss/px/inv_off')
        w(P + f's/{st}', '\n'.join(lines))
    # keys: per clip, the ticks where a sampled column moved > PX_MOVE since the last write (t 0 writes all)
    kd = {}
    for c in m['clips']:
        if not c.get('px', {}).get('keys'):
            continue
        last, ticks = {}, []
        for t, row in px_sample(c, names):
            lines = []
            for k, n in enumerate(names):
                if n not in row:
                    continue
                x, z, top = row[n]
                prev = last.get(n)
                if prev is not None and max(abs(x - prev[0]), abs(z - prev[1]), abs(top - prev[2])) <= PX_MOVE:
                    continue
                lines += [f'data modify storage rlk:mboss px.o.{n}_x set value {L.num(x, 3)}d',
                          f'data modify storage rlk:mboss px.o.{n}_z set value {L.num(z, 3)}d',
                          f'data modify storage rlk:mboss px.top.{n} set value {L.num(top, 3)}f',
                          f'data merge entity {uu[k]} {{height:{L.num(max(top, 0.1), 3)}f}}']
                up = 1 if top > PX_UP else 0
                if prev is None or (1 if prev[2] > PX_UP else 0) != up:
                    lines += [f'scoreboard players set #pxU{k + 1} mb {up}', f'function {F}ev/{k + 1}']
                last[n] = (x, z, top)
            if lines:
                w(P + f'k/{c["id"]}/{t}', [f'# Clip {c["name"]} (id {c["id"]}) tick {t}: the proxy columns that moved.'] + lines)
                ticks.append(t)
        kd[c['id']] = (c['name'], ticks)

    def tree(cid, ts):
        if len(ts) <= 8:
            return [f'execute if score #pxT mb matches {t} run return run function {F}k/{cid}/{t}' for t in ts]
        h = len(ts) // 2
        a, bb = ts[:h], ts[h:]
        for part in (a, bb):
            w(P + f't/{cid}_{part[0]}_{part[-1]}', tree(cid, part))
        return [f'execute if score #pxT mb matches {a[0]}..{a[-1]} run return run function {F}t/{cid}_{a[0]}_{a[-1]}',
                f'execute if score #pxT mb matches {bb[0]}..{bb[-1]} run return run function {F}t/{cid}_{bb[0]}_{bb[-1]}']
    for cid, (cname, ts) in kd.items():
        if ts:
            w(P + f'c/{cid}', [f'# Clip {cname}: the key of tick #pxT (binary tree over the {len(ts)} key ticks).'] + tree(cid, ts))
    w(P + 'c', [f'# The clip shown this tick (#pxC = the anchor\'s {co}).']
      + [f'execute if score #pxC mb matches {cid} run return run function {F}c/{cid}' for cid, (_, ts) in kd.items() if ts])
    w(P + 'tick', f'''
# @s = the body of {bid} (the anchor), at it, after the module and rig ticks: the key of the shown clip tick (the anchor's
# {to}; negative = queued: the offsets stay), then every proxy follows the anchor.
execute unless score @s {to} matches 0.. run return run function {F}follow with storage rlk:mboss px.o
execute store result score #pxC mb run scoreboard players get @s {co}
scoreboard players operation #pxT mb = @s {to}
function {F}c
function {F}follow with storage rlk:mboss px.o
''')
    w(P + 'follow', '\n'.join(
        [f'# (macro px.o) @s = the anchor: one tp per proxy to ^x ^y ^z from the anchor (yaw only; y 0 live, {L.num(PX_PARK)} parked).']
        + [f'$execute at @s rotated as @s rotated ~ 0 as {uu[k]} run tp @s ^$({n}_x) ^$({n}_y) ^$({n}_z)' for k, n in enumerate(names)]))
    w(P + 'park', '\n'.join([f'# Every proxy of {bid} parked (the state set is kept; the next px/state or key re-evaluates).']
                            + [f'function {F}off/{k + 1}' for k in range(len(names))]))
    w(P + 'poll', '\n'.join([f'# Clicks on the proxies of {bid} (interaction attack / interaction data) go through the normal click input, every',
                             '# live tick (the click shield path of combat/mshield_tick).']
                            + [ln for u in uu for ln in (f'execute as {u} if data entity @s attack at @s run function rlk:combat/input/poll_attack',
                                                         f'execute as {u} if data entity @s interaction at @s run function rlk:combat/input/poll_right')]))
    w(P + 'clear_input', '\n'.join([f'# Paused: drop the stored clicks of the proxies of {bid}.']
                                   + [ln for u in uu for ln in (f'data remove entity {u} attack', f'data remove entity {u} interaction')]))
    return len(lay), sum(len(ts) for _, ts in kd.values())


PX_INFO = {b['id']: px_build(b) for b in PXB}
w('px/inv_on', '''
# @s = the body: an inv:true proxy state made it untargetable (rlk_mb_pxinv marks that px added the inv).
tag @s add rlk_mb_inv
tag @s add rlk_mb_pxinv
''')
w('px/inv_off', '''
# @s = the body with rlk_mb_pxinv: leaving the inv set removes the inv px added (and only that one).
tag @s remove rlk_mb_inv
tag @s remove rlk_mb_pxinv
''')
# Target-side state that M0 code writes with distance / rlk_hit selectors outside combat/apply lands on the proxies
# (cm.md 9.6 audit, README "챕터 보스" audit table); combat/apply reads it on the body. px/db (every px tick, before the
# key) moves it to the body: countdown timers (element/tick counts them down on the body, elAct 1) and game-time ends
# (max). Proxies are interactions: mob/tick never runs on them, so a value left there would never decay.
PX_DB = (('scT', 'superconduct (element/run/supercond)', True),
         ('rnNoE', "Ronova's echo window (char/ronova/echo_boom)", True),
         ('mirEnd', 'the mirror item (items/proc/mirror)', False),
         ('aurEnd', "Yoimiya's aura (char/yoimiya/rocket_boom, aur_move)", False))
w('px/db', ['# @s = the body (px/tick): proxy-held target state moves to the body (cm.md 9.6 audit).']
  + [f'execute as @e[type=minecraft:interaction,tag=rlk_mb_px,scores={{{o}=1..}}] run function rlk:mboss/px/db/{o.lower()}' for o, _, _ in PX_DB])
for o, what, timer in PX_DB:
    w(f'px/db/{o.lower()}', [f'# @s = a proxy holding {o} ({what}): the body takes the larger value, the proxy drops it.',
                     f'scoreboard players operation @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] {o} > @s {o}']
      + (['scoreboard players set @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] elAct 1'] if timer else [])
      + [f'scoreboard players set @s {o} 0'])
w('px/to_body', '''
# @s = a proxy tagged rlk_hit (a §16 line in char/arlecchino/skill_hit, after the damage): the rest of that skill's
# target-side writes (arDir, the blood-debt mark) go to the body, once per boss, not to each proxy that was in range.
tag @s remove rlk_hit
tag @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] add rlk_hit
''')
for fn_, ctx in (('spawn', 'as the body, at it'), ('tick', 'as the body, at it (mboss/world after body_tick)'),
                 ('park', 'anywhere'), ('poll', 'anywhere (mboss/world, live ticks)'), ('clear_input', 'anywhere (pause_tick)')):
    w(f'px/{fn_}', '\n'.join([f'# GENERATED dispatcher ({ctx}): rlk:mboss/px/<id>/{fn_} of the running proxy boss (#mbId).']
                              + (['function rlk:mboss/px/db'] if fn_ == 'tick' else [])
                              + [f'execute if score #mbId mb matches {b["n"]} run return run function rlk:mboss/px/{b["id"]}/{fn_}' for b in PXB]))
w('px/state', '\n'.join(
    ['# {set} (anywhere): the proxy state set of the running proxy boss (a key of its manifest states). Literal lines per',
     '# boss and set (no $(..) function names); an unknown set name changes nothing and warns.',
     '$data modify storage rlk:mboss pxq set value "$(set)"']
    + [f'execute if score #mbId mb matches {b["n"]} if data storage rlk:mboss {{pxq:"{st}"}} run return run function rlk:mboss/px/{b["id"]}/s/{st}'
       for b in PXB for st in PX_STATES.get(b['id'], [])]
    + ['execute if score #mbPx mb matches 1 run tellraw @a[tag=player] ' + CT + gray('알 수 없는 판정 상태: ') + ',{nbt:"pxq",storage:"rlk:mboss",color:"gray"}]']))

w('push/capsule', '''
# @s = the body (the anchor), at it, rotated as it: mboss/world after body_tick while #mbPushOn 1 (a per-tick request of
# the module; cm.md 13.5). Capsules = rlk:mboss push[] {f0,f1,hw,px,top} in tenths in the anchor frame (f0 <= f <= f1,
# |s| < hw; an entry with px is active only while that proxy's current top <= top). A player inside is moved toward the
# nearest exit (side, front end, back end) whose end point is not inside a live disc / ring / line hazard, by at most
# 0.6 b this tick in 0.1-b player/knockback/check steps (no velocity, no FOV). Refused while dead, reviving, selecting,
# in the map view or dashing.
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if entity @a[tag=player,scores={vMap=1}] run return 0
execute if entity @a[tag=player,scores={dashMoveT=1..}] run return 0
execute unless data storage rlk:mboss push[0] run return 0
execute unless function rlk:mboss/mv/local run return 0
scoreboard players operation #pbx mb = #mbPX mb
scoreboard players operation #pbz mb = #mbPZ mb
scoreboard players set #puDone mb 0
data modify storage rlk:mboss pq set from storage rlk:mboss push
function rlk:mboss/push/cap_loop
execute if score #puDone mb matches 1 run scoreboard players set #mbPlG mb -1
''')
w('push/cap_loop', '''
execute if score #puDone mb matches 1 run return 0
execute unless data storage rlk:mboss pq[0] run return 0
function rlk:mboss/push/cap_one
data remove storage rlk:mboss pq[0]
function rlk:mboss/push/cap_loop
''')
w('push/cap_one', '''
# @s = the anchor: the capsule pq[0] (tenths -> mb); the player's anchor-frame position is #mbLf / #mbLs (mb).
execute store result score #pF0 mb run data get storage rlk:mboss pq[0].f0 100
execute store result score #pF1 mb run data get storage rlk:mboss pq[0].f1 100
execute store result score #pHW mb run data get storage rlk:mboss pq[0].hw 100
execute store result score #pTop mb run data get storage rlk:mboss pq[0].top
scoreboard players set #pAct mb 1
data modify storage rlk:mboss pc set from storage rlk:mboss pq[0]
execute unless data storage rlk:mboss pc{px:""} run function rlk:mboss/push/cap_top with storage rlk:mboss pc
execute if score #pAct mb matches 0 run return 0
execute if score #mbLf mb < #pF0 mb run return 0
execute if score #mbLf mb > #pF1 mb run return 0
scoreboard players operation #pAs mb = #mbLs mb
execute if score #pAs mb matches ..-1 run scoreboard players operation #pAs mb *= #cm1 mb
execute if score #pAs mb >= #pHW mb run return 0
# inside: the three exits (distance to the edge, mb) tried nearest first
scoreboard players operation #pdS mb = #pHW mb
scoreboard players operation #pdS mb -= #pAs mb
scoreboard players operation #pdF mb = #pF1 mb
scoreboard players operation #pdF mb -= #mbLf mb
scoreboard players operation #pdB mb = #mbLf mb
scoreboard players operation #pdB mb -= #pF0 mb
scoreboard players set #pU1 mb 0
scoreboard players set #pU2 mb 0
scoreboard players set #pU3 mb 0
scoreboard players set #pEx mb 0
function rlk:mboss/push/pick
execute if score #pEx mb matches 0 run function rlk:mboss/push/pick
execute if score #pEx mb matches 0 run function rlk:mboss/push/pick
execute if score #pEx mb matches 0 run return 0
scoreboard players set #puDone mb 1
function rlk:mboss/push/move
''')
w('push/cap_top', '''
# (macro px) a capsule bound to a proxy is active only while that proxy's current column top <= top (tenths).
$execute store result score #t mb run data get storage rlk:mboss px.top.$(px) 10
execute if score #t mb > #pTop mb run scoreboard players set #pAct mb 0
''')
w('push/pick', '''
# The nearest exit not tried yet (#pU1 side, #pU2 front end, #pU3 back end); #pEx = 1 left 2 right 3 front 4 back when
# its end point (the edge + 0.3 b) is clear of live disc / ring / line hazards.
scoreboard players set #pBest mb 0
scoreboard players set #pBd mb 2147483647
execute if score #pU1 mb matches 0 if score #pdS mb < #pBd mb run scoreboard players set #pBest mb 1
execute if score #pBest mb matches 1 run scoreboard players operation #pBd mb = #pdS mb
execute if score #pU2 mb matches 0 if score #pdF mb < #pBd mb run scoreboard players set #pBest mb 2
execute if score #pBest mb matches 2 run scoreboard players operation #pBd mb = #pdF mb
execute if score #pU3 mb matches 0 if score #pdB mb < #pBd mb run scoreboard players set #pBest mb 3
execute if score #pBest mb matches 3 run scoreboard players operation #pBd mb = #pdB mb
execute if score #pBest mb matches 0 run return 0
execute if score #pBest mb matches 1 run scoreboard players set #pU1 mb 1
execute if score #pBest mb matches 2 run scoreboard players set #pU2 mb 1
execute if score #pBest mb matches 3 run scoreboard players set #pU3 mb 1
# unit direction x1000 in the world (#fx #fz = the anchor forward from mv/local; left = (fz, -fx))
execute if score #pBest mb matches 1 if score #mbLs mb matches 0.. run function rlk:mboss/push/dir_left
execute if score #pBest mb matches 1 if score #mbLs mb matches ..-1 run function rlk:mboss/push/dir_right
execute if score #pBest mb matches 2 run function rlk:mboss/push/dir_front
execute if score #pBest mb matches 3 run function rlk:mboss/push/dir_back
scoreboard players operation #pDist mb = #pBd mb
scoreboard players add #pDist mb 300
scoreboard players operation #peX mb = #pux mb
scoreboard players operation #peX mb *= #pDist mb
scoreboard players operation #peX mb /= #c1000 mb
scoreboard players operation #peX mb += #pbx mb
scoreboard players operation #peZ mb = #puz mb
scoreboard players operation #peZ mb *= #pDist mb
scoreboard players operation #peZ mb /= #c1000 mb
scoreboard players operation #peZ mb += #pbz mb
function rlk:mboss/push/end_ok
execute if score #pOK mb matches 1 run scoreboard players operation #pEx mb = #pDir mb
''')
for nm, d, ux, uz in (('left', 1, '#fz', '#fx'), ('right', 2, '#fz', '#fx'), ('front', 3, '#fx', '#fz'), ('back', 4, '#fx', '#fz')):
    sx = {'left': '', 'right': ' *= #cm1 mb', 'front': '', 'back': ' *= #cm1 mb'}[nm]
    sz = {'left': ' *= #cm1 mb', 'right': '', 'front': '', 'back': ' *= #cm1 mb'}[nm]
    lines = [f'scoreboard players set #pDir mb {d}', f'scoreboard players operation #pux mb = {ux} mb', f'scoreboard players operation #puz mb = {uz} mb']
    if sx:
        lines.append('scoreboard players operation #pux mb' + sx)
    if sz:
        lines.append('scoreboard players operation #puz mb' + sz)
    w(f'push/dir_{nm}', '\n'.join([f'# exit {nm}: the unit direction x1000 of the anchor frame in the world.'] + lines))
w('push/end_ok', '''
# #peX / #peZ mb = a proposed end point (the player's y): #pOK 1 unless it lies inside a live disc / ring (kind 1-2) or
# line (kind 4) hazard (their own bounds with the body pad).
scoreboard players set #pOK mb 1
execute as @e[type=minecraft:marker,tag=rlk_mb_hz,scores={mbHzK=1..2}] run function rlk:mboss/push/end_disc
execute as @e[type=minecraft:marker,tag=rlk_mb_hz,scores={mbHzK=4}] run function rlk:mboss/push/end_line
''')
w('push/end_disc', '''
execute if score #pOK mb matches 0 run return 0
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #qx mb = #peX mb
scoreboard players operation #qx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #qz mb = #peZ mb
scoreboard players operation #qz mb -= #t mb
execute unless score #qx mb matches -32000..32000 run return 0
execute unless score #qz mb matches -32000..32000 run return 0
scoreboard players operation #q2 mb = #qx mb
scoreboard players operation #q2 mb *= #qx mb
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= #qz mb
scoreboard players operation #q2 mb += #t mb
execute if score #q2 mb <= @s mbHzRR if score #q2 mb >= @s mbHzRI run scoreboard players set #pOK mb 0
''')
w('push/end_line', '''
execute if score #pOK mb matches 0 run return 0
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #qx mb = #peX mb
scoreboard players operation #qx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #qz mb = #peZ mb
scoreboard players operation #qz mb -= #t mb
execute unless score #qx mb matches -48000..48000 run return 0
execute unless score #qz mb matches -48000..48000 run return 0
scoreboard players operation #q2 mb = #qx mb
scoreboard players operation #q2 mb *= @s mbHzFX
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= @s mbHzFZ
scoreboard players operation #q2 mb += #t mb
scoreboard players operation #q2 mb /= #c1000 mb
execute if score #q2 mb < @s mbHzLo run return 0
execute if score #q2 mb > @s mbHzHi run return 0
scoreboard players operation #qs mb = #qx mb
scoreboard players operation #qs mb *= @s mbHzFZ
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= @s mbHzFX
scoreboard players operation #qs mb -= #t mb
scoreboard players operation #qs mb /= #c1000 mb
execute if score #qs mb matches ..-1 run scoreboard players operation #qs mb *= #cm1 mb
execute if score #qs mb <= @s mbHzHW run scoreboard players set #pOK mb 0
''')
w('push/move', '\n'.join(
    ['# @s = the anchor: up to 6 steps of 0.1 b toward exit #pEx (collision-checked like knockback); the distance needed is',
     '# the edge distance #pBd + 0.1 b.',
     'scoreboard players operation #pN mb = #pBd mb',
     'scoreboard players add #pN mb 199',
     'scoreboard players operation #pN mb /= #c100 mb',
     'execute if score #pN mb matches 7.. run scoreboard players set #pN mb 6']
    + [f'execute if score #pEx mb matches {d} run function rlk:mboss/push/step_{nm}' for d, nm in ((1, 'left'), (2, 'right'), (3, 'front'), (4, 'back'))]))
for nm, off in (('left', '^0.1 ^ ^'), ('right', '^-0.1 ^ ^'), ('front', '^ ^ ^0.1'), ('back', '^ ^ ^-0.1')):
    w(f'push/step_{nm}', f'''
# @s = the anchor: one 0.1-b step of the player's body toward the {nm} exit, while #pN steps are left.
execute unless score #pN mb matches 1.. run return 0
scoreboard players remove #pN mb 1
scoreboard players set #pkbBlocked tmp 0
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned {off} run function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 1 run return 0
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned {off} run tp @e[tag=rlk_body,limit=1] ~ ~ ~
function rlk:mboss/push/step_{nm}
''')
pisq = []
for _ in range(14):
    pisq += ['scoreboard players operation #t mb = #n mb', 'scoreboard players operation #t mb /= #pd mb',
             'scoreboard players operation #pd mb += #t mb', 'scoreboard players operation #pd mb /= #c2 mb',
             'execute if score #pd mb matches ..0 run scoreboard players set #pd mb 1']
w('push/sqrt', '\n'.join(['# #pd = isqrt(#n) (#n >= 1).', 'scoreboard players set #pd mb 10000'] + pisq))
w('push/ring', '''
# {r,to,kb} (as anything, at the centre; cm.md 13.5 / N18): a push-only ring. A player whose body is within r (tenths,
# horizontal) is moved radially outward to the distance to (tenths, to >= r) on its bearing over kb ticks (1..10; the
# collision-checked pull glide, no facing turn); a player at the centre goes toward the arena start. Skipped when the
# landing point is inside a live disc / ring / line hazard. No damage, no hit event, not dodgeable. r <= 320 and to <= 600
# (larger values are clamped: the squared distances stay inside int32, every offset beyond 32 b is outside the ring).
$scoreboard players set #prR mb $(r)
$scoreboard players set #prTo mb $(to)
$scoreboard players set #prKb mb $(kb)
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute if score #prR mb matches 321.. run scoreboard players set #prR mb 320
execute if score #prTo mb matches 601.. run scoreboard players set #prTo mb 600
execute if score #prTo mb < #prR mb run scoreboard players operation #prTo mb = #prR mb
execute if score #prKb mb matches ..0 run scoreboard players set #prKb mb 1
execute if score #prKb mb matches 11.. run scoreboard players set #prKb mb 10
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_prc"]}
execute store result score #qcx mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_prc,limit=1] Pos[0] 1000
execute store result score #qcz mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_prc,limit=1] Pos[2] 1000
kill @e[type=minecraft:marker,tag=rlk_mb_prc]
execute unless function rlk:mboss/mv/plpos run return 0
scoreboard players operation #pbx mb = #mbPX mb
scoreboard players operation #pbz mb = #mbPZ mb
scoreboard players operation #qx mb = #pbx mb
scoreboard players operation #qx mb -= #qcx mb
scoreboard players operation #qz mb = #pbz mb
scoreboard players operation #qz mb -= #qcz mb
execute unless score #qx mb matches -32000..32000 run return 0
execute unless score #qz mb matches -32000..32000 run return 0
scoreboard players operation #n mb = #qx mb
scoreboard players operation #n mb *= #qx mb
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= #qz mb
scoreboard players operation #n mb += #t mb
scoreboard players operation #t mb = #prR mb
scoreboard players operation #t mb *= #c100 mb
scoreboard players operation #t mb *= #t mb
execute if score #n mb > #t mb run return 0
scoreboard players set #pd mb 0
execute if score #n mb matches 1.. run function rlk:mboss/push/sqrt
execute if score #pd mb matches ..49 run function rlk:mboss/push/ring_start
execute if score #pd mb matches ..49 run return 0
function rlk:mboss/push/ring_land
''')
w('push/ring_start', '''
# A player at the centre: the bearing toward the arena arrival spot (cur.start) instead. Only the bearing counts
# (ring_land divides by the length), so the offset is taken in units of 4 mb: up to 128 b on x / z without overflow.
execute store result score #qx mb run data get storage rlk:mboss cur.start.x 1000
execute store result score #qz mb run data get storage rlk:mboss cur.start.z 1000
scoreboard players operation #qx mb -= #qcx mb
scoreboard players operation #qz mb -= #qcz mb
scoreboard players set #t mb 4
scoreboard players operation #qx mb /= #t mb
scoreboard players operation #qz mb /= #t mb
execute unless score #qx mb matches -32000..32000 run return 0
execute unless score #qz mb matches -32000..32000 run return 0
scoreboard players operation #n mb = #qx mb
scoreboard players operation #n mb *= #qx mb
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= #qz mb
scoreboard players operation #n mb += #t mb
execute if score #n mb matches ..0 run return 0
function rlk:mboss/push/sqrt
function rlk:mboss/push/ring_land
''')
w('push/ring_land', '''
# The landing point = centre + (#qx, #qz) / #pd x to (mb); then the glide unless it lands inside a live hazard.
scoreboard players operation #t mb = #prTo mb
scoreboard players operation #t mb *= #c100 mb
scoreboard players operation #peX mb = #qx mb
scoreboard players operation #peX mb *= #t mb
scoreboard players operation #peX mb /= #pd mb
scoreboard players operation #peX mb += #qcx mb
scoreboard players operation #peZ mb = #qz mb
scoreboard players operation #peZ mb *= #t mb
scoreboard players operation #peZ mb /= #pd mb
scoreboard players operation #peZ mb += #qcz mb
function rlk:mboss/push/end_ok
execute if score #pOK mb matches 0 run return 0
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_prl"]}
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_prl,limit=1] Pos[0] double 0.001 run scoreboard players get #peX mb
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_prl,limit=1] Pos[2] double 0.001 run scoreboard players get #peZ mb
execute store result storage rlk:mboss a.t int 1 run scoreboard players get #prKb mb
scoreboard players set #pullFace mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_prl,limit=1] run function rlk:mboss/push/ring_go with storage rlk:mboss a
kill @e[type=minecraft:marker,tag=rlk_mb_prl]
''')
w('push/ring_go', '''
# (macro t) at the landing point: the undodgeable, collision-checked glide (mboss/pull/start) without the facing turn.
$function rlk:mboss/pull/start {t:$(t)}
''')

# Stale top-level framework files: every F:mboss/*.mcfunction belongs to this generator
# (modules live in F:mboss/<id>/, the arena in F:mboss/arena/).
for p in sorted(L.MB.glob('*.mcfunction')):
    if p.stem not in CORE_TOP:
        p.unlink()
removed = out.clean()
print(f'mboss core: {len(out.written)} functions, {len(MIDS)} registered mid-bosses '
      f'({", ".join(b["id"] for b in MIDS)}), {len(CHAPS)} chapter bosses ({", ".join(b["id"] for b in CHAPS) or "none"}), '
      f'{len(ARENAS)} arenas, {removed} stale removed.')
