#!/usr/bin/env python3
"""Placeholder mid-boss module "proto" (시험용 강적): proves the mid-boss framework end to end.

    python3 tools/build_mboss_proto.py

Registry entry: tools/mboss_registry.json id "proto", n 99, w 0 (never rolled; reachable through
/function rlk:mboss/test/start {id:"proto"}). Owns F:mboss/proto/** (deleted and rewritten).

What it exercises:
  hooks       every hook of the contract (README 중간보스 / scratchpad contract.md)
  rig         a husk-like body of 9 block_display parts, poses with interpolation (no RP needed)
  intro       drops from the sky onto a disc telegraph (mv/glide + hz/disc), typed line, intro_end
  patterns    1 slam (disc at the player)  2 thrust (line + lunge)  3 sweep (150-degree sector after
              closing in)  4 ripple (ring)  5 javelin (line + projectile prop that flies back)
              6 pull (pull/start) + 360-degree swing (sector 180)  7 whole arena with one safe circle (full)
  aux         test id 90: a breakable star (aux/spawn, mres 80, immune to pyro) whose break deals 10 %
              true damage (true_pct)
  bars        sub-line (pattern name) and under-bar (pattern progress)
  death       slump, line, sink
"""
import help_lib as H
import mboss_lib as L

ID = 'proto'
REG = L.load_registry()
A = REG['arena']
CY = A['cy']
B = next(b for b in REG['boss'] if b['id'] == ID)
P = f'rlk:mboss/{ID}/'
out = L.Out(owned_dirs=[f'mboss/{ID}'])


def w(name, text):
    out.write(f'mboss/{ID}/{name}', text if isinstance(text, list) else text.strip('\n'))


def fn(name):
    return 'function ' + P + name


# ---------------------------------------------------------------------------------------------
# Rig: parts in the body's local frame (+x left, +y up, +z forward), blocks. Each part: block,
# size, pivot (in the parent's rest frame), box min corner relative to the pivot, parent.
PARTS = {
    'leg_l': ('minecraft:blue_terracotta', (0.40, 1.15, 0.40), (0.22, 1.15, 0.0), (-0.20, -1.15, -0.20), 'root'),
    'leg_r': ('minecraft:blue_terracotta', (0.40, 1.15, 0.40), (-0.22, 1.15, 0.0), (-0.20, -1.15, -0.20), 'root'),
    'torso': ('minecraft:cyan_terracotta', (0.90, 0.95, 0.50), (0.0, 1.15, 0.0), (-0.45, 0.0, -0.25), 'root'),
    'head': ('minecraft:mud_bricks', (0.62, 0.62, 0.62), (0.0, 2.10, 0.0), (-0.31, 0.0, -0.31), 'torso'),
    'arm_l': ('minecraft:mud_bricks', (0.32, 1.05, 0.32), (0.61, 2.0, 0.0), (-0.16, -1.05, -0.16), 'torso'),
    'arm_r': ('minecraft:mud_bricks', (0.32, 1.05, 0.32), (-0.61, 2.0, 0.0), (-0.16, -1.05, -0.16), 'torso'),
    'shaft': ('minecraft:stripped_dark_oak_log', (0.18, 0.18, 1.75), (-0.61, 1.02, 0.0), (-0.09, -0.09, -0.25), 'arm_r'),
    'club': ('minecraft:chiseled_polished_blackstone', (0.46, 0.46, 0.58), (-0.61, 1.02, 0.0), (-0.23, -0.23, 1.35), 'arm_r'),
    'eye': ('minecraft:black_concrete', (0.44, 0.08, 0.02), (0.0, 2.10, 0.0), (-0.22, 0.36, 0.31), 'torso'),
}
ORDER = ['leg_l', 'leg_r', 'torso', 'head', 'eye', 'arm_l', 'arm_r', 'shaft', 'club']
# Poses: part -> (rx, ry, rz) degrees about the pivot; 'root' -> (dy, rx) for the whole body.
POSES = {
    'rest': {'arm_l': (-8, 0, 4), 'arm_r': (-14, 0, -4)},
    'raise': {'arm_r': (-165, 0, -8), 'arm_l': (-45, 0, 18), 'torso': (8, 0, 0), 'head': (-10, 0, 0), 'grip': (-10, 0, 0)},
    'strike': {'arm_r': (-62, 0, 0), 'arm_l': (-20, 0, 12), 'torso': (-16, 0, 0), 'grip': (78, 0, 0)},
    'thrust_wind': {'arm_r': (-70, 0, 0), 'arm_l': (-30, 0, 14), 'torso': (6, 28, 0), 'grip': (70, 0, 0)},
    'thrust': {'arm_r': (-96, 0, 0), 'arm_l': (-10, 0, 10), 'torso': (-12, -12, 0), 'grip': (90, 0, 0)},
    'sweep_wind': {'arm_r': (-92, 0, -10), 'arm_l': (-20, 0, 20), 'torso': (0, 62, 0), 'grip': (88, 0, 0)},
    'sweep': {'arm_r': (-92, 0, -10), 'arm_l': (-20, 0, 20), 'torso': (-6, -72, 0), 'grip': (88, 0, 0)},
    'both_up': {'arm_r': (-172, 0, -6), 'arm_l': (-172, 0, 6), 'torso': (6, 0, 0), 'head': (-14, 0, 0)},
    'both_down': {'arm_r': (-55, 0, -10), 'arm_l': (-55, 0, 10), 'torso': (-20, 0, 0), 'grip': (80, 0, 0)},
    'death': {'arm_r': (-12, 0, -18), 'arm_l': (-12, 0, 18), 'torso': (-34, 0, 0), 'head': (-24, 0, 0), 'root': (-0.35, 0), 'grip': (40, 0, 0)},
    'sink': {'arm_r': (-12, 0, -18), 'arm_l': (-12, 0, 18), 'torso': (-40, 0, 0), 'head': (-30, 0, 0), 'root': (-2.4, -6), 'grip': (40, 0, 0)},
}
# 'grip' = wrist angle of the club (shaft and head turn together about the hand).
for _p in POSES.values():
    if 'grip' in _p:
        _p['shaft'] = _p['club'] = _p.pop('grip')


def part_matrix(name, pose):
    chain = []
    n = name
    while n != 'root':
        chain.append(n)
        n = PARTS[n][4]
    root = pose.get('root', (0.0, 0.0))
    m = L.mat_chain(L.mat_t(0, root[0], 0), L.mat_rx(root[1]))
    for p in reversed(chain):
        _, size, pivot, mn, _ = PARTS[p]
        rx, ry, rz = pose.get(p, (0, 0, 0))
        m = L.mat_chain(m, L.mat_t(*pivot), L.mat_ry(ry), L.mat_rx(rx), L.mat_rz(rz), L.mat_t(*(-c for c in pivot)))
    _, size, pivot, mn, _ = PARTS[name]
    return L.mat_chain(m, L.mat_t(pivot[0] + mn[0], pivot[1] + mn[1], pivot[2] + mn[2]), L.mat_s(*size))


SEL = '@e[type=minecraft:block_display,tag=rlk_mbp_{},limit=1]'
spawn = ['# @s = body, at @s: summon the 9-part block-display rig (all rlk_mb_aux, so cleanup removes it).',
         f'kill @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part]']
for n in ORDER:
    blk = PARTS[n][0]
    spawn.append(f'summon minecraft:block_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_{ID}_part","rlk_mbp_{n}"],'
                 f'block_state:{{id:"{blk}"}},teleport_duration:1,interpolation_duration:0,'
                 f'transformation:{L.mat_nbt(part_matrix(n, POSES["rest"]))}}}')
spawn.append(f'execute rotated as @s rotated ~ 0 run tp @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part] ~ ~ ~ ~ 0')
w('rig/spawn', spawn)
w('rig/follow', [
    '# @s = body, at @s: parts follow the body position and yaw (teleport_duration 1 smooths it).',
    f'execute unless entity @e[type=minecraft:block_display,tag=rlk_mbp_torso,limit=1] run {fn("rig/spawn")}',
    f'execute rotated as @s rotated ~ 0 run tp @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part] ~ ~ ~ ~ 0'])
for pose, spec in POSES.items():
    lines = [f'# Pose "{pose}" over $(d) ticks (macro {{d:N}}).']
    for n in ORDER:
        lines.append(f'$data merge entity {SEL.format(n)} {{start_interpolation:0,interpolation_duration:$(d),'
                     f'transformation:{L.mat_nbt(part_matrix(n, spec))}}}')
    w(f'pose/{pose}', lines)
w('rig/glow', [
    '# Short hit flash (from on_hit via #prFlash): glowing outline on every part.',
    f'execute as @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part] run data merge entity @s {{Glowing:1b,glow_color_override:16757606}}'])
w('rig/unglow', [f'execute as @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part] run data merge entity @s {{Glowing:0b}}'])

# ---------------------------------------------------------------------------------------------
# Patterns
NAMES = {1: '강타', 2: '찌르기', 3: '휘두르기', 4: '파문', 5: '투창', 6: '끌어당겨 회전베기', 7: '전역 강타'}
LENGTH = {1: 44, 2: 38, 3: 34, 4: 40, 5: 42, 6: 66, 7: 60}
FLOOR = f'positioned ~ {CY} ~'


def at(t, cmd):
    return f'execute if score #prT mb matches {t} run {cmd}'


def at_body(t, sub):
    """sub = the rest of an execute chain (e.g. 'positioned ~ 201 ~ run function ...'), body yaw as rotation."""
    return f'execute if score #prT mb matches {t} at @s rotated as @s rotated ~ 0 {sub}'


PAT = {
    1: [at(1, 'function rlk:mboss/mv/face'),
        at(1, fn('pose/raise') + ' {d:8}'),
        at(1, 'scoreboard players set #hzSfx mb 1'),
        at(1, f'execute at @e[tag=rlk_body,limit=1] {FLOOR} run function rlk:mboss/hz/disc {{r:35,tell:24,dmg:150}}'),
        at(1, L.sound('entity.ravager.roar', 0.5, 1.4)),
        at(20, fn('pose/strike') + ' {d:4}'),
        at(25, 'particle minecraft:explosion ~ ~1 ~ 0.4 0.2 0.4 0 2 force @a[tag=player]'),
        at(LENGTH[1], fn('finish'))],
    2: [at(1, 'function rlk:mboss/mv/face'),
        at(1, fn('pose/thrust_wind') + ' {d:10}'),
        at(1, 'scoreboard players set #hzKB mb 4'),
        at(1, 'scoreboard players set #hzSfx mb 3'),
        at_body(1, f'{FLOOR} run function rlk:mboss/hz/line {{len:120,w:22,tell:18,dmg:120}}'),
        at(16, fn('pose/thrust') + ' {d:3}'),
        'execute if score #prT mb matches 16..20 run function rlk:mboss/mv/step {d:0.8}',
        at(LENGTH[2], fn('finish'))],
    3: [at(1, 'function rlk:mboss/mv/face'),
        at(1, fn('pose/sweep_wind') + ' {d:10}'),
        at(1, 'scoreboard players set #hzSfx mb 2'),
        at_body(1, f'{FLOOR} run function rlk:mboss/hz/sector {{r:55,a:75,tell:16,dmg:130}}'),
        at(15, fn('pose/sweep') + ' {d:3}'),
        at(LENGTH[3], fn('finish'))],
    4: [at(1, fn('pose/both_up') + ' {d:10}'),
        at(1, 'scoreboard players set #hzSfx mb 4'),
        at(1, f'execute {FLOOR} run function rlk:mboss/hz/ring {{r0:35,r:95,tell:22,dmg:110}}'),
        at(1, L.sound('block.respawn_anchor.charge', 0.7, 0.7)),
        at(20, fn('pose/both_down') + ' {d:3}'),
        at(LENGTH[4], fn('finish'))],
    5: [at(1, 'function rlk:mboss/mv/face'),
        at(1, fn('pose/raise') + ' {d:10}'),
        at(1, 'scoreboard players set #hzSfx mb 3'),
        at(1, 'scoreboard players set #hzY1 mb 22'),
        at_body(1, f'{FLOOR} run function rlk:mboss/hz/line {{len:300,w:14,tell:18,dmg:130}}'),
        at(17, fn('pose/strike') + ' {d:3}'),
        at(17, fn('javelin')),
        at(LENGTH[5], fn('finish'))],
    6: [at(1, fn('pose/both_up') + ' {d:12}'),
        at(1, L.say('이리 오너라.', '#E8C890', 2, 26, 2)),
        'execute if score #prT mb matches 1..27 run ' + fn('pull_tell'),
        at_body(28, f'positioned ^ ^ ^1.6 {FLOOR} run function rlk:mboss/pull/start {{t:6}}'),
        at(28, L.sound('entity.evoker.prepare_wololo', 0.8, 1.2)),
        at(36, fn('pose/sweep_wind') + ' {d:5}'),
        at(36, 'scoreboard players set #hzSfx mb 2'),
        at(36, f'execute {FLOOR} run function rlk:mboss/hz/sector {{r:55,a:180,tell:14,dmg:120}}'),
        at(49, fn('pose/sweep') + ' {d:3}'),
        at(LENGTH[6], fn('finish'))],
    7: [at(1, fn('pose/both_up') + ' {d:12}'),
        at(1, L.say('피할 곳은 한 곳뿐.', '#E8C890', 2, 30, 2)),
        at(1, fn('safe_spot')),
        at(44, fn('pose/both_down') + ' {d:3}'),
        at(46, f'kill @e[tag=rlk_mb_{ID}_safe]'),
        at(LENGTH[7], fn('finish'))],
}
for k, lines in PAT.items():
    w(f'p/{k}', [f'# Pattern {k} "{NAMES[k]}" (@s = body, at @s; #prT = 1.. pattern clock).'] + lines)
w('javelin', f'''
# Visual javelin: a block-display prop that flies 0.25 b sub-steps forward, then back to the body (pj/launch,
# #pjRet 1). The damage belongs to the line hazard created at the start of the pattern (K23 style).
execute rotated as @s rotated ~ 0 positioned ^-0.6 ^1.5 ^0.8 run summon minecraft:block_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_{ID}_jav"],block_state:{{id:"minecraft:stripped_dark_oak_log"}},teleport_duration:1,transformation:{{translation:[-0.08f,-0.08f,-1.0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.16f,0.16f,2.0f]}}}}
scoreboard players set #pjRet mb 1
execute rotated as @s rotated ~ 0 positioned ^-0.6 ^1.5 ^0.8 as @e[tag=rlk_mb_{ID}_jav,tag=!rlk_mb_pj,limit=1] run function rlk:mboss/pj/launch {{spd:30,life:9,dmg:0,hr:6}}
{L.sound('item.trident.throw', 1, 0.7)}
''')
w('pull_tell', '''
# Pull tell (27 ticks): a red cage around the player, every 3rd tick.
scoreboard players operation #t mb = #prT mb
scoreboard players operation #t mb %= #c3 mb
execute if score #t mb matches 0 at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.9f,0.1f,0.15f],scale:1.4f} ~ ~1 ~ 0.7 0.9 0.7 0 14 force @a[tag=player]
''')
w('safe_spot', f'''
# Whole-arena blast with one safe circle (r 4.5) at a random spot within 12 blocks of the centre.
kill @e[tag=rlk_mb_{ID}_safe]
execute at @e[tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_{ID}_safe"]}}
execute store result score #t mb run random value -120..120
execute store result score #t2 mb run data get entity @e[tag=rlk_mb_arena,limit=1] Pos[0] 10
scoreboard players operation #t mb += #t2 mb
execute store result entity @e[tag=rlk_mb_{ID}_safe,limit=1] Pos[0] double 0.1 run scoreboard players get #t mb
execute store result score #t mb run random value -120..120
execute store result score #t2 mb run data get entity @e[tag=rlk_mb_arena,limit=1] Pos[2] 10
scoreboard players operation #t mb += #t2 mb
execute store result entity @e[tag=rlk_mb_{ID}_safe,limit=1] Pos[2] double 0.1 run scoreboard players get #t mb
scoreboard players set #hzR0 mb 45
scoreboard players set #hzSfx mb 4
execute at @e[tag=rlk_mb_{ID}_safe,limit=1] run function rlk:mboss/hz/full {{tell:44,dmg:140}}
''')

w('choose', [
    '# Next pattern: fixed rotation 1..7, overridden by the test lock (#mbLock) or a test request (#prReq).',
    'scoreboard players add #prNext mb 1',
    'execute if score #prNext mb matches 8.. run scoreboard players set #prNext mb 1',
    'scoreboard players operation #prPat mb = #prNext mb',
    'execute if score #mbLock mb matches 1..7 run scoreboard players operation #prPat mb = #mbLock mb',
    'execute if score #prReq mb matches 1..7 run scoreboard players operation #prPat mb = #prReq mb',
    'scoreboard players set #prReq mb 0',
    'scoreboard players set #prT mb 0',
    'scoreboard players set #prGoT mb 0',
    'scoreboard players set #prGo mb 0',
    '# Melee patterns close in first (sweep).',
    'execute if score #prPat mb matches 3 unless entity @e[tag=rlk_body,distance=..3.6,limit=1] run scoreboard players set #prGo mb 1',
] + [f'execute if score #prPat mb matches {k} run data modify storage rlk:mboss sub set value [{{text:"패턴  ",color:"#A8A8A8"}},{{text:"{v}",color:"#FFD86B"}}]'
     for k, v in NAMES.items()]
    + [f'execute if score #prPat mb matches {k} run scoreboard players set #prLen mb {v}' for k, v in LENGTH.items()])
w('finish', f'''
scoreboard players set #prPat mb 0
scoreboard players set #prT mb 0
scoreboard players set #prCool mb 24
scoreboard players set #prGo mb 0
{fn("pose/rest")} {{d:6}}
data modify storage rlk:mboss sub set value [{{text:"대기",color:"#8A8A8A"}}]
''')
w('close_in', '''
# Melee pattern chosen from afar: dash toward the player (0.45 b/t) up to 30 ticks, then start.
scoreboard players add #prGoT mb 1
function rlk:mboss/mv/turn {max:30}
function rlk:mboss/mv/toward {d:0.45}
execute if entity @e[tag=rlk_body,distance=..3.6,limit=1] run scoreboard players set #prGo mb 0
execute if score #prGoT mb matches 30.. run scoreboard players set #prGo mb 0
''')
w('idle', '''
execute if score #prCool mb matches 1.. run scoreboard players remove #prCool mb 1
function rlk:mboss/mv/turn {max:12}
execute unless entity @e[tag=rlk_body,distance=..6,limit=1] run function rlk:mboss/mv/toward {d:0.16}
execute if score #prCool mb matches ..0 run function rlk:mboss/proto/choose
''')
w('pattern', [
    '# @s = body: the running pattern (#prGo = still closing in; the clock waits at 0).',
    'execute if score #prGo mb matches 1 run return run ' + fn('close_in'),
    'scoreboard players add #prT mb 1'] + [f'execute if score #prPat mb matches {k} run ' + fn(f'p/{k}') for k in PAT])

# ---------------------------------------------------------------------------------------------
# Stars (aux route + true damage)
w('star', f'''
# Test (pattern id 90): a breakable star 4 b in front of the boss. Pool 3 % of the boss's max HP (#auxHpPct,
# scales with the level; hits on it are modified like hits on the body), RES 80 % (x0.238), immune to Pyro
# (aux_hit); breaking it deals 10 % of the boss's max HP as true damage.
kill @e[tag=rlk_mb_{ID}_star]
kill @e[tag=rlk_mb_{ID}_starv]
scoreboard players set #auxHpPct mb 3
scoreboard players set #auxRes mb 80
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4 {FLOOR} run function rlk:mboss/aux/spawn
tag @e[tag=rlk_mb_auxlast,limit=1] add rlk_mb_{ID}_star
execute at @e[tag=rlk_mb_{ID}_star,limit=1] run summon minecraft:block_display ~ ~1.1 ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_{ID}_starv"],block_state:{{id:"minecraft:amethyst_block"}},teleport_duration:1,brightness:{{sky:15,block:15}},transformation:{{translation:[-0.35f,-0.35f,-0.35f],left_rotation:[0.3647f,0.2798f,0.1159f,0.8806f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}}}
{L.say('별을 부숴 보아라.', '#C9A8FF', 2, 24, 1)}
''')
w('star_tick', f'''
# @s = body. Spin the star visual; a broken star (rlk_mb_broken from aux/take) is removed and hurts the boss.
execute as @e[tag=rlk_mb_{ID}_starv] at @s run tp @s ~ ~ ~ ~6 0
execute if entity @e[tag=rlk_mb_{ID}_star,tag=rlk_mb_broken,limit=1] run {fn("star_break")}
''')
w('star_break', f'''
execute at @e[tag=rlk_mb_{ID}_star,limit=1] run particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.3 0.3 0.15 30 force @a[tag=player]
execute at @e[tag=rlk_mb_{ID}_star,limit=1] run {L.sound('block.amethyst_block.break', 1, 0.8)}
kill @e[tag=rlk_mb_{ID}_star]
kill @e[tag=rlk_mb_{ID}_starv]
scoreboard players set #mbTrueEl mb 3
function rlk:mboss/true_pct {{pct:10}}
''')

# ---------------------------------------------------------------------------------------------
# Hooks
w('spawn', f'''
# Hook spawn (@s = arena marker at the centre, facing north). The body starts 10 b above the centre star
# and drops in during the intro; it faces the arriving player (south).
execute positioned ~ ~10 ~ rotated 0 0 run function rlk:mboss/body
execute as @e[tag=rlk_mb_body,limit=1] at @s run {fn("reload")}
''')
w('reload', f'''
# Hook reload (@s = body): AI to idle, rig rebuilt; HP kept.
scoreboard players set #prPat mb 0
scoreboard players set #prT mb 0
scoreboard players set #prGo mb 0
scoreboard players set #prReq mb 0
scoreboard players set #prCool mb 30
scoreboard players set #prFlash mb 0
scoreboard players set #c3 mb 3
{fn("rig/spawn")}
data modify storage rlk:mboss sub set value [{{text:"대기",color:"#8A8A8A"}}]
''')
w('intro_tick', f'''
# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end).
{fn("rig/follow")}
execute if score #mbT mb matches 1 run {fn("pose/both_up")} {{d:4}}
execute if score #mbT mb matches 1 positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:24}}
execute if score #mbT mb matches 1 run scoreboard players set #hzSfx mb 1
execute if score #mbT mb matches 1 positioned ~ {CY} ~ run function rlk:mboss/hz/disc {{r:30,tell:24,dmg:100}}
execute if score #mbT mb matches 21 run {fn("pose/both_down")} {{d:3}}
execute if score #mbT mb matches 25 run particle minecraft:explosion ~ ~0.5 ~ 0.8 0.1 0.8 0 3 force @a[tag=player]
execute if score #mbT mb matches 28 run {L.say('시험을 시작하지.', '#E8C890', 2, 30, 1)}
execute if score #mbT mb matches 32 run {fn("pose/rest")} {{d:8}}
execute if score #mbT mb matches 50.. run function rlk:mboss/intro_end
''')
w('tick', f'''
# Hook tick (@s = body, at @s, fight state): rig, hit flash, stars, then idle or the running pattern.
{fn("rig/follow")}
execute if score #prFlash mb matches 1.. run scoreboard players remove #prFlash mb 1
execute if score #prFlash mb matches 0 run {fn("rig/unglow")}
execute if score #prFlash mb matches 0 run scoreboard players set #prFlash mb -1
execute if entity @e[tag=rlk_mb_{ID}_starv,limit=1] run {fn("star_tick")}
# A star break can be lethal (true_pct runs death_start before it returns): no fight logic on a dying body.
execute unless score #mbSt mb matches 1 run return 0
execute if score #prPat mb matches 0 run return run {fn("idle")}
{fn("pattern")}
''')
w('on_hit', f'''
# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg known). Flags only: start a short flash.
execute unless score #prFlash mb matches 1.. run {fn("rig/glow")}
scoreboard players set #prFlash mb 3
''')
w('aux_hit', f'''
# Hook aux_hit (@s = a star inside combat/apply, all modifiers and RES already applied to #dmg). Pyro does nothing (immune);
# everything else falls through to the framework default (pool, number, broken tag).
execute if entity @s[tag=rlk_mb_{ID}_star] if score #elem tmp matches 1 run scoreboard players set #dmg tmp 0
''')
w('incoming', '''
# Hook incoming (@s = body inside combat/apply_mods, after level and RES): no extra modifiers for proto.
''')
w('pause', f'''
# Hook pause (player dead / reviving / on a selection screen): the framework freezes everything; drop the flash.
{fn("rig/unglow")}
''')
w('resume', '''
# Hook resume: nothing to restore (timers simply continue).
''')
w('death_start', f'''
# Hook death_start (@s = body, hazards already cleared, bars hidden).
scoreboard players set #prPat mb 0
kill @e[tag=rlk_mb_{ID}_star]
kill @e[tag=rlk_mb_{ID}_starv]
kill @e[tag=rlk_mb_{ID}_jav]
{fn("rig/unglow")}
{fn("pose/death")} {{d:14}}
{L.say('...여기까지인가.', '#E8C890', 2, 36, 2)}
''')
w('death_tick', f'''
# Hook death_tick (@s = body, #mbT = 1.. until cur.death).
{fn("rig/follow")}
execute if score #mbT mb matches 20 run {fn("pose/sink")} {{d:18}}
execute if score #mbT mb matches 20.. run particle minecraft:smoke ~ ~0.6 ~ 0.4 0.3 0.4 0.01 4 force @a[tag=player]
''')
w('cleanup', '''
# Hook cleanup (no executor; idempotent): reset proto's fake players. Its entities are rlk_mb_aux.
scoreboard players set #prPat mb 0
scoreboard players set #prT mb 0
scoreboard players set #prGo mb 0
scoreboard players set #prReq mb 0
scoreboard players set #prFlash mb 0
''')
w('uninstall', '''
# Hook uninstall (no executor; from rlk:mboss/uninstall for every module): proto creates no objectives or
# entities of its own beyond the framework's (rlk_mb_aux, mb), so there is nothing extra to remove.
''')
w('bars', '''
# Hook bars (@s = body): under-bar = progress of the running pattern (gold); the sub-line is set by choose.
execute unless score #prPat mb matches 1.. run return 0
scoreboard players operation #buSub bu = #prT mb
scoreboard players operation #buSubMax bu = #prLen mb
scoreboard players set #buSubCol bu 8
''')
w('hz_vis', '''
# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end, @s mbHzV = visual id): proto keeps the
# framework particle telegraphs, so it never sets #hzVis.
''')
w('pj_end', f'''
# Hook pj_end (@s = projectile prop, #pjEv 1 wall / 2 life / 3 back at the body / 4 hit the player; #pjKeep
# preset to the default: the javelin returns after 1/2 and is removed after 3).
execute if score #pjEv mb matches 3 at @s run particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.1 6 force @a[tag=player]
''')
w('test', [
    '# Hook test {id:N} (as the player, from /function rlk:mboss/test/pattern): 1..7 = run that pattern next',
    '# (the running one is cut), 90 = spawn a breakable star.',
    '$scoreboard players set #prReq mb $(id)',
    f'execute if score #prReq mb matches 90 as @e[tag=rlk_mb_body,limit=1] at @s run {fn("star")}',
    'execute if score #prReq mb matches 90 run return run scoreboard players set #prReq mb 0',
    'execute unless score #prReq mb matches 1..7 run return run scoreboard players set #prReq mb 0',
    'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
    'execute if score #prPat mb matches 1.. run function rlk:mboss/lib_clear',
    'execute if score #prPat mb matches 1.. as @e[tag=rlk_mb_body,limit=1] at @s run ' + fn('finish'),
    'scoreboard players set #prCool mb 1'])

# Contract test/help (L.HELP_HOOKS): /function rlk:mboss/test/pattern {id:"help"} while this boss runs.
w('test/help', [H.head('/function rlk:mboss/test/pattern {id:…}', f'{B["name"]} 시험 번호')]
  + [H.row(f'/function rlk:mboss/test/pattern {{id:{k}}}', k, f'{v} (다음 패턴)') for k, v in NAMES.items()]
  + [H.row('/function rlk:mboss/test/pattern {id:90}', 90, '부술 수 있는 별 소환'),
     H.note('lock {id:1~7}: 그 패턴만 반복 · {id:0} 해제')])


missing = [h for h in L.HOOKS + L.HELP_HOOKS if not (L.FN / f'mboss/{ID}/{h}.mcfunction').exists()]
assert not missing, missing
removed = out.clean()
print(f'mboss {ID}: {len(out.written)} functions ({len(PARTS)} rig parts, {len(POSES)} poses, {len(PAT)} patterns), {removed} stale removed.')
