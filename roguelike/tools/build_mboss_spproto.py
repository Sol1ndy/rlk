#!/usr/bin/env python3
"""The stand-in special boss "spproto" (시험용 균열 수호자): proves the special-boss framework and the rift end to end
(Tachy S1; scratchpad tk/PLAN.md §7, §9.1).

    python3 tools/build_mboss_spproto.py

Registry entry: tools/mboss_registry.json id "spproto", n 97, kind special, w 0 (never rolled by a natural rift: only
/function rlk:boss/test/rift (when it is the only special), rift_id {id:"spproto"}, special {id:"spproto"}), arena cp_test,
picks 3, lvup 1, goldMul 6, sap 1, RES 10 % for every element, one music phase. Owns F:mboss/spproto/** (deleted and
rewritten). Needs the core (tools/build_mboss_core.py) and the arena generator for cp_test.

What it exercises:
  spawn       mboss/body (the mid-boss body: miniboss tag = gold x goldMul, sapphire sap through combat/gold_drop),
              husk scale 1.25, click shield 1.1 x 2.6, the per-element RES of the registry; two block displays follow it
  intro       20 t (untargetable), then the fight: music phase 1, no floor
  patterns    every 60 t: 1 a 3 b disc at the player (electro), 2 a 5 b ring around the body; lock {id:1|2}
  test {id}   1 / 2 the patterns now, 3 music off, 4 music phase 1 again
  death       40 t: the displays sink, a sound, then the framework's death_finish (the zone clears -> sp/clear)
"""
import help_lib as H
import mboss_lib as L

ID = 'spproto'
REG = L.load_registry()
B = next(b for b in REG['boss'] if b['id'] == ID)
assert B.get('kind') == 'special', 'spproto must be a special entry'
AR = L.arena_of(B, REG)
CY = AR['cy']
ROOT = L.fn_root(B)                  # mboss/spproto
P = f'rlk:{ROOT}/'
out = L.Out(owned_dirs=[ROOT])
TH = L.theme_module(AR['theme'])     # tools/mboss_arena_cp_test.py
SPAWN = TH.POINTS['spawn'] if TH is not None and hasattr(TH, 'POINTS') else (AR['cx'], AR['cy'], AR['cz'], 0.0)


def w(name, text):
    out.write(f'{ROOT}/{name}', text if isinstance(text, list) else text.strip('\n'))


def fn(name):
    return 'function ' + P + name


PART = f'rlk_mb_{ID}_part'
w('rig/spawn', f'''
# @s = body, at it: two block displays (a pillar and a crown; rlk_mb_aux: cleanup and /reload remove them).
kill @e[type=minecraft:block_display,tag={PART}]
summon minecraft:block_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","{PART}"],block_state:{{id:"minecraft:obsidian"}},teleport_duration:1,transformation:{{translation:[-0.45f,0f,-0.45f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,2.2f,0.9f]}}}}
summon minecraft:block_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","{PART}","rlk_mb_{ID}_crown"],block_state:{{id:"minecraft:sea_lantern"}},brightness:{{sky:15,block:15}},teleport_duration:1,transformation:{{translation:[-0.3f,2.3f,-0.3f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f]}}}}
{fn("rig/follow")}
''')
w('rig/follow', f'''
execute unless entity @e[type=minecraft:block_display,tag={PART},limit=1] run return run {fn("rig/spawn")}
execute rotated as @s rotated ~ 0 run tp @e[type=minecraft:block_display,tag={PART}] ~ ~ ~ ~ 0
''')
w('rig/glow', [f'execute as @e[type=minecraft:block_display,tag={PART}] run data merge entity @s {{Glowing:1b,glow_color_override:9426175}}'])
w('rig/unglow', [f'execute as @e[type=minecraft:block_display,tag={PART}] run data merge entity @s {{Glowing:0b}}'])
w('rig/sink', [f'execute as @e[type=minecraft:block_display,tag={PART}] run data merge entity @s {{start_interpolation:0,interpolation_duration:30,'
               'transformation:{translation:[-0.45f,-2.4f,-0.45f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,2.2f,0.9f]}}'])

# ---------------------------------------------------------------------------------------------
# Patterns (#spT = the pattern clock, #spPat = the running pattern, #spCool = the idle clock)
w('choose', '''
scoreboard players add #spNext mb 1
execute if score #spNext mb matches 3.. run scoreboard players set #spNext mb 1
scoreboard players operation #spPat mb = #spNext mb
execute if score #mbLock mb matches 1..2 run scoreboard players operation #spPat mb = #mbLock mb
scoreboard players set #spT mb 0
''')
w('p/1', f'''
# 1: a 3 b electro disc at the player (tell 24 t).
execute if score #spT mb matches 1 run {L.hz_opts(el=3)[0]}
execute if score #spT mb matches 1 at @e[tag=rlk_body,limit=1] positioned ~ {CY} ~ run {L.hz_disc(3.0, 24, 100)}
execute if score #spT mb matches 1 at @s run {L.sound('block.respawn_anchor.charge', 0.6, 1.4)}
execute if score #spT mb matches 40.. run scoreboard players set #spPat mb 0
''')
w('p/2', f'''
# 2: a ring 2.5 .. 5 b around the body (tell 28 t).
execute if score #spT mb matches 1 at @s positioned ~ {CY} ~ run {L.hz_ring(2.5, 5.0, 28, 110)}
execute if score #spT mb matches 1 at @s run {L.sound('entity.lightning_bolt.impact', 0.4, 1.6)}
execute if score #spT mb matches 44.. run scoreboard players set #spPat mb 0
''')
w('pattern', ['# @s = body: the running pattern (#spT = its clock).', 'scoreboard players add #spT mb 1']
  + [f'execute if score #spPat mb matches {k} run {fn(f"p/{k}")}' for k in (1, 2)])

# ---------------------------------------------------------------------------------------------
# Hooks
w('spawn', f'''
# Hook spawn (@s = the arena marker of {AR["aid"]}): the body (mboss/body: miniboss, the registry's scale / shield / RES) at
# the arena's spawn point, facing the arrival.
execute positioned {L.num(SPAWN[0])} {L.num(SPAWN[1])} {L.num(SPAWN[2])} rotated {L.num(SPAWN[3])} 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {fn("reload")}
''')
w('reload', f'''
# Hook reload (@s = body): the displays and the module clocks (HP is kept by the framework).
scoreboard players set #spPat mb 0
scoreboard players set #spT mb 0
scoreboard players set #spCool mb 40
scoreboard players set #spFlash mb 0
{fn("rig/spawn")}
data modify storage rlk:mboss sub set value [{{text:"균열 수호",color:"#8FD8FF"}}]
''')
w('intro_tick', f'''
# Hook intro_tick (@s = body; untargetable): 20 t, then the fight (music phase 1).
{fn("rig/follow")}
execute if score #mbT mb matches 1 run {L.say('균열 너머를 지킨다.', '#8FD8FF', 2, 24, 1)}
execute if score #mbT mb matches 20.. run {fn("start_fight")}
''')
w('start_fight', f'''
function rlk:mboss/intro_end
{L.music(1)}
''')
w('tick', f'''
# Hook tick (@s = body, at it): displays, flash, then idle / pattern.
{fn("rig/follow")}
execute if score #spFlash mb matches 1.. run scoreboard players remove #spFlash mb 1
execute if score #spFlash mb matches 0 run {fn("rig/unglow")}
execute if score #spFlash mb matches 0 run scoreboard players set #spFlash mb -1
execute unless score #mbSt mb matches 1 run return 0
execute if score #spPat mb matches 1.. run return run {fn("pattern")}
execute if score #spCool mb matches 1.. run scoreboard players remove #spCool mb 1
function rlk:mboss/mv/turn {{max:8}}
execute if score #spCool mb matches ..0 run scoreboard players set #spCool mb 60
execute if score #spCool mb matches 60 run {fn("choose")}
''')
w('on_hit', f'''
# Hook on_hit (@s = body inside combat/apply): a short flash.
execute unless score #spFlash mb matches 1.. run {fn("rig/glow")}
scoreboard players set #spFlash mb 3
''')
w('aux_hit', '# Hook aux_hit: none (no aux objects).')
w('incoming', '# Hook incoming (@s = body inside apply_mods; the framework floor runs after it): no extra modifiers.')
w('pause', [fn('rig/unglow')])
w('resume', '# Hook resume: nothing to restore (the framework restarts the music).')
w('death_start', f'''
# Hook death_start (@s = body; hazards cleared, bars hidden, music stopped).
scoreboard players set #spPat mb 0
{fn("rig/unglow")}
{fn("rig/sink")}
{L.say('균열이... 닫힌다.', '#8FD8FF', 2, 30, 2)}
{L.sound('block.beacon.deactivate', 0.8, 0.8)}
''')
w('death_tick', f'''
execute if score #mbT mb matches 5.. run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.6 0.4 0.02 4 force @a[tag=player]
''')
w('cleanup', '''
# Hook cleanup (no executor; idempotent).
scoreboard players set #spPat mb 0
scoreboard players set #spT mb 0
scoreboard players set #spFlash mb 0
''')
w('uninstall', '# Hook uninstall: nothing of its own outside the fight (fake players in mb go with the objective).')
w('bars', '''
# Hook bars (@s = body): the sub-line.
data modify storage rlk:mboss sub set value [{text:"균열 수호",color:"#8FD8FF"}]
''')
w('hz_vis', '# Hook hz_vis: the framework particle telegraphs only.')
w('pj_end', '# Hook pj_end: no projectiles.')
TESTS = {1: (fn('p/1'), '원판 (번개)'), 2: (fn('p/2'), '고리'), 3: (L.music(0), '음악 끄기'), 4: (L.music(1), '음악 1단계')}
test = ['# Hook test {id:N} (as the player, from /function rlk:mboss/test/pattern).', '$scoreboard players set #spReq mb $(id)']
for k, (line, _) in TESTS.items():
    if k in (1, 2):
        test.append(f'execute if score #spReq mb matches {k} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run '
                    f'scoreboard players set #spPat mb {k}')
        test.append(f'execute if score #spReq mb matches {k} run scoreboard players set #spT mb 0')
    else:
        test.append(f'execute if score #spReq mb matches {k} run {line}')
test.append('scoreboard players set #spReq mb 0')
w('test', test)
w('test/help', [H.head('/function rlk:mboss/test/pattern {id:…}', f'{B["name"]} 시험 번호')]
  + [H.row(f'/function rlk:mboss/test/pattern {{id:{k}}}', k, v) for k, (_, v) in TESTS.items()]
  + [H.note('lock {id:1~2}: 그 패턴만 반복 · {id:0} 해제')])

missing = [h for h in L.HOOKS + L.HELP_HOOKS + L.SPECIAL_HOOKS if not (L.FN / f'{ROOT}/{h}.mcfunction').exists()]
assert not missing, missing
removed = out.clean()
print(f'mboss {ID}: {len(out.written)} functions, {removed} stale removed.')
