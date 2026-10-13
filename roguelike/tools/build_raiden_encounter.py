"""Narukami encounter controller. Original Minecraft adaptation, no recorded audio.

Generate controllers only; arena, hazards and articulated rig have separate builders.
The illusion challenge (pattern 5) lives in build_raiden_illusions.py; this file only
dispatches to illusion/tick and calls illusion/on_break and illusion/cleanup.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'data/rlk/function/boss/raiden'
def write(name, lines):
    p = BASE/(name+'.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text((lines.strip() if isinstance(lines,str) else '\n'.join(lines))+'\n',encoding='utf-8')
def call(name): return 'function rlk:boss/raiden/'+name
def at(t,cmd): return cmd if cmd.startswith('#') else f'execute if score @s rdTime matches {t} at @s rotated as @s run {cmd}'
def anim(n): return f'scoreboard players set @s rdAnim {n}'
def haz(shape,tell,dmg,life=None):
    return call('hazard/create')+f' {{shape:{shape},tell:{tell},damage:{dmg},life:{life or tell+10}}}'
def sound(event,vol=1,pitch=.8):
    return f'playsound minecraft:{event} hostile @a[tag=player] ~ ~ ~ {vol} {pitch} 0.3'
def caption(text):
    return '# Pattern names intentionally stay out of the boss bar.'
def obj(kind,model,hp,oid,y=0):
    return call('object/create')+f' {{kind:{kind},model:"{model}",hp:{hp},id:{oid},y:{y}}}'

# ---- Lightning armor tuning --------------------------------------------------
# A continuously attacking player lands at most one armor drain per SHIELD_CD ticks
# (20/5 = 4 drains per second, multi-hit and DoT spam included); the armor also decays
# by 1 every 4 ticks (5 per second) except during the flower ultimate.
#   passive only      750 / 5            = 150 s
#   physical/thunder  750 / (5 + 4*2)    = 57.7 s
#   water/rock/wind   750 / (5 + 4*3)    = 44.1 s
#   grass             750 / (5 + 4*4)    = 35.7 s
#   fire/ice          750 / (5 + 4*6)    = 25.9 s
# A successful flower defence removes 190 (25% of the armor).
SHIELD_MAX = 750
SHIELD_CD = 5
FLOWER_BREAK = 190
# #elem: 0 physical 1 fire 2 water 3 thunder 4 ice 5 rock 6 wind 7 grass 8 void.
DRAIN_DEFAULT = 2
DRAIN = {1:6, 4:6, 2:3, 5:3, 6:3, 7:4}
DRAIN_REACTION = 1
# Malice energy: normal-phase ticks before the transformation (45 s, was 30 s).
RAGE_MAX = 900
# Like the original, every hit the boss lands also feeds the malice gauge (+3 s).
RAGE_HIT = 60
# Armour-break stun (original: about 15 s of collapse before she recovers).
EXHAUST = 300
# Transformation: scatter to the centre, then the transformation burst/clip.
TRANSFORM_FX = 1
TRANSFORM_LEN = 52
# Final calamity entry (pattern 15): she gathers lightning, rises inside a lightning
# pillar while bolts rake the arena, and dissolves at the top (rig hidden from then on).
ASCEND_END, ASCEND_STEP = 26, 0.32
CLAP_LOCK, CLAP_TELL = 17, 14   # pattern 12: hands follow until 17, clap lands 14 later
SHADOW_LOCK = 37                 # pattern 13: the shadow chases for 36 ticks
# Close-range patterns and their reach: chosen farther than `start` blocks from the
# player, she dashes at them (or scatter-blinks in front of them beyond CLOSE_BLINK)
# until within `stop`, and only then starts; a dash pinned on the arena rim or timing out
# scatter-blinks beside the player instead. Ranged patterns (3 뇌명, 4, 6, 7, 12-15) start
# where she stands; 18 발도 돌진 reaches about 20 blocks (its line, or dash + sweep).
REACH = {1: (5.5, 4), 2: (16, 13), 11: (10, 8), 16: (11, 9), 17: (14, 12), 18: (20, 17)}
CLOSE_BLINK, CLOSE_MAX, CLOSE_STEP = 18, 45, (0.55, 0.65)
# 금강괴멸파 (pattern 14): three stakes spread around the centre; each pulse is a ring that
# travels from radius 2 to the far wall (RING_END over RING_FRAMES ticks, jump it).
from build_raiden_fx_textures import RING_END, RING_FRAMES
STAKES = [(0, -9), (7.8, 4.5), (-7.8, 4.5)]
STAKE_TELL = 12

objectives = ['rd','rdPhase','rdPat','rdTime','rdAnim','rdRage','rdShield','rdCycle','rdCool','rdPrev','rdTurns','rdHitCD','rdObjKind','rdObjId','rdObjHP','rdReal','rdOAge','rdPTime','rdShape','rdWind','rdHAge','rdHLife','rdDamage','rdHHit','rdFX','rdFZ','rdHId','rdVId','rdUltUsed','rdWalk','rdWalkDir','rdBlink','rdCam','rdDeath','rdDeathTime','rdHidden','rdGo','rdNext']
write('init',[f'scoreboard objectives add {v} dummy' for v in objectives]+[
    'bossbar add rlk:narukami {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple"}',
    'bossbar add rlk:narukami_state {text:"악연의 에너지",color:"light_purple"}',
    '# Resource-pack boss bar (tools/build_bossbar.py): white bars are transparent, the',
    '# names carry the level/name line and the drawn HP bar with its under bar.',
    'bossbar set rlk:narukami color white','bossbar set rlk:narukami_state color white',
    'bossbar set rlk:narukami style progress','bossbar set rlk:narukami_state style progress',
    call('bars_hide'),
    'scoreboard players set #rd100 rd 100','scoreboard players set #rd4 rd 4',
    call('camera/release_all'), call('rig/init'), call('vfx/init'), call('object_vfx/init'), call('movement/init'), 'kill @e[tag=rlk_raiden_aux]',
    'execute as @e[tag=rlk_raiden] at @s run '+call('reload')])
write('reload','''
# A reload cancels pending danger volumes; it never refills boss health.
execute if score @s rdDeath matches 1 run return run kill @s
scoreboard players set @s rdDeath 0
scoreboard players set @s rdDeathTime 0
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdHidden 0
kill @e[tag=rlk_rd_blink_dest]
function rlk:boss/raiden/illusion/cleanup
attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 0
scoreboard players set @s rdPat 0
scoreboard players set @s rdGo 0
scoreboard players set @s rdNext 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdRage 0
scoreboard players set @s rdCool 40
scoreboard players set @s rdAnim 0
scoreboard players set @s rdHitCD 0
function rlk:boss/raiden/rig/spawn
''')
write('spawn','''
# Room boss spawn, position = arena center. One encounter is active at a time.
function rlk:boss/raiden/cleanup
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_boss","boss","rlk_raiden","rlk_rd_newboss"],PersistenceRequired:1b,NoAI:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",CustomName:{text:"마가츠 미타케 나루카미노 미코토",color:"light_purple"},active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_rd_newboss] at @s run function rlk:boss/raiden/setup
tag @e[tag=rlk_rd_newboss] remove rlk_rd_newboss
''')
write('setup','''
function rlk:room/mob_init
attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
scoreboard players set @s rdCycle 0
scoreboard players set @s rdPrev 0
scoreboard players set @s rdTurns 0
function rlk:boss/raiden/reload
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
title @a[tag=player] times 8 60 16
title @a[tag=player] subtitle {text:"바닥의 보랏빛 예고를 보고 회피하세요",color:"white"}
title @a[tag=player] title {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 84
scoreboard players set @a[tag=player] ttlT 84
scoreboard players set #rdCap rd 1
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.7 0.62 0.3
''')
write('cleanup','''
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/illusion/cleanup
kill @e[tag=rlk_raiden_aux]
function rlk:boss/raiden/bars_hide
''')
write('bars_hide','''
# Boss bars are server-global: hide them whenever no fight is shown (also from rlk:tick).
bossbar set rlk:narukami visible false
bossbar set rlk:narukami_state visible false
scoreboard players set #rdBar rd 0
''')
write('world','''
execute unless entity @e[tag=rlk_raiden,limit=1] run return run function rlk:boss/raiden/cleanup
execute as @e[tag=rlk_raiden,scores={rdDeath=1},limit=1] at @s run return run function rlk:boss/raiden/death/tick
execute unless entity @a[tag=player,limit=1] run return 0
# A dead player means the run (or boss test) is lost: no bars on the death screen.
execute if entity @a[tag=player,scores={dead=1}] run function rlk:boss/raiden/bars_hide
execute if entity @a[tag=player,scores={dead=1}] run return run function rlk:boss/raiden/pause
execute if entity @a[tag=player,scores={rnDie=1..}] run return run function rlk:boss/raiden/pause
execute if entity @a[tag=player,scores={pkMode=1..}] run return run function rlk:boss/raiden/pause
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/tick
execute as @e[tag=rlk_rd_object] at @s run function rlk:boss/raiden/object/tick
execute as @e[tag=rlk_rd_hazard] at @s run function rlk:boss/raiden/hazard/tick
function rlk:boss/raiden/hazard/vfx_world
execute as @e[tag=rlk_rd_dome] at @s run function rlk:boss/raiden/dome_tick
execute as @e[tag=rlk_rd_slam_hand] at @s run function rlk:boss/raiden/rig/target_slam_tick
function rlk:boss/raiden/vfx/world
function rlk:boss/raiden/object_vfx/world
function rlk:boss/raiden/orb/world
function rlk:boss/raiden/movement/world
''')
# Boss captions ride on the HUD title timer: ttlT (subtitle lifetime, view/ride_tick
# blanks the subtitle when it runs out so the 0.5 s crosshair title cannot replay it)
# and vBig (pauses the crosshair while a big title is up). #rdCap marks a boss caption,
# #rdCapPat one that belongs to the running pattern and ends with it.
write('caption/expire','''
scoreboard players set #rdCap rd 0
scoreboard players set #rdCapPat rd 0
''')
write('caption/clear','''
scoreboard players set #rdLine rd 0
execute unless score #rdCap rd matches 1 run return 0
function rlk:boss/raiden/caption/expire
title @a[tag=player] subtitle ""
scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0
scoreboard players set @a[tag=player,scores={vBig=1..}] vBig 0
''')
def typed(text):
    # Typewriter steps: each word grows at most two syllables at a time; punctuation
    # stays on its syllable, except the closing punctuation, which lands as the last step.
    PUNCT = '.,!?…'
    body = text.rstrip(PUNCT)
    tail = text[len(body):]
    steps, done = [], ''
    for w, word in enumerate(body.split(' ')):
        sylls = []
        for ch in word:
            if ch in PUNCT and sylls:
                sylls[-1] += ch
            else:
                sylls.append(ch)
        for k in range(0, len(sylls), 2):
            steps.append(done + ''.join(sylls[:k+2]))
        done = steps[-1] + ' '
    if tail:
        steps.append(text)
    return steps
# Boss lines from the original fight (나무위키 「마가츠 미타케 나루카미노 미코토」 3.2 패턴):
# key: (text or explicit steps, ticks per step, colour, hold of the full line)
VOICE, VOICE2 = '#d7b4ff', '#e6a3ff'
LINES = {
    'mangeop': (['그', '그 끝은', '그 끝은 만겁', '그 끝은 만겁일지니', '그 끝은 만겁일지니...'], 5, VOICE, 24),
    'eternal': ('이 몸이 곧 영원이다', 3, VOICE, 26),
    'nothing': ('그 무엇도 영원한 것은 없다.', 2, VOICE, 40),
    'eyes': ('뇌광이 영원의 땅을 비추는구나.', 2, VOICE, 24),
    'pohyeong': ('찰나의... 포영!', 3, VOICE, 22),
    'ganpa': ('간파했군.', 4, '#bfe4ff', 34),
    'noemyeong': ('뇌명.', 4, VOICE, 20),
    'will': ('뇌전은 인간의 의지 따위로 변하지 않아', 2, VOICE, 22),
    'command': ('번개여, 나의 호령을 따르라.', 2, VOICE, 22),
    'calm': ('무념 무상, 천하가 고요하리.', 2, VOICE, 12),
    'sever_one': ('무념 무상, 일도 단절.', 1, VOICE2, 16),
    'cleave_all': ('방해는 모두 베겠노라', 2, VOICE2, 22),
    'prison': ('감옥으로 만들어 주지', 2, VOICE2, 22),
    'cheonsu': ('천수의 속박!', 3, VOICE2, 30),
    'sever': ('단절!', 2, VOICE2, 20),
    'goemyeol': ('궤멸하라!', 3, VOICE2, 24),
    'pierce': ('뚫려라!', 2, VOICE2, 20),
}
LINE_IDS = {k: i for i, k in enumerate(LINES, 1)}
tick_lines = ['# Advances the boss line in progress (#rdLine id, #rdLineT age); called from tick.',
              'execute unless score #rdLine rd matches 1.. run return 0',
              'scoreboard players add #rdLineT rd 1']
for key, (steps, gap, colour, hold) in LINES.items():
    steps = typed(steps) if isinstance(steps, str) else steps
    lid = LINE_IDS[key]
    write('line/'+key, [f'scoreboard players set #rdLine rd {lid}', 'scoreboard players set #rdLineT rd -1'])
    for k, text in enumerate(steps):
        last = k == len(steps)-1
        stay = hold if last else gap+6
        # One plain, quiet tick per step (same sound and pitch every time).
        frame = [f'title @a[tag=player] times 0 {stay} {12 if last else 0}',
                 'title @a[tag=player] subtitle {text:"'+text+'",color:"'+colour+'",bold:true}',
                 'execute as @a[tag=player] run function rlk:view/ttl_blank',
                 f'scoreboard players set @a[tag=player] ttlT {stay+(12 if last else 0)}',
                 'scoreboard players set #rdCap rd 1', 'scoreboard players set #rdCapPat rd 1',
                 'execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ .3 1 0']
        if last:
            frame.append('scoreboard players set #rdLine rd 0')
        write(f'line/{key}_{k}', frame)
        tick_lines.append(f'execute if score #rdLine rd matches {lid} if score #rdLineT rd matches {k*gap} run function rlk:boss/raiden/line/{key}_{k}')
write('line/tick', tick_lines)
write('caption/pattern_end','''
execute if score #rdCapPat rd matches 1 run function rlk:boss/raiden/caption/clear
''')
write('pause','''
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @e[tag=rlk_raiden] rdBlink 0
scoreboard players set @e[tag=rlk_raiden] rdWalk 0
scoreboard players set @e[tag=rlk_raiden] rdGo 0
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_slam_hand]
kill @e[tag=rlk_rd_sfx]
function rlk:boss/raiden/object_vfx/clear
function rlk:boss/raiden/hazard/vfx_world
scoreboard players set @e[tag=rlk_raiden] rdPat 0
scoreboard players set @e[tag=rlk_raiden] rdTime 0
scoreboard players set @e[tag=rlk_raiden] rdCool 60
scoreboard players set @e[tag=rlk_raiden] rdAnim 0
''')
write('tick',f'''
# @s=real living boss; the invisible body owns damage, the displays own appearance.
execute if score @s rdDeath matches 1 run return run function rlk:boss/raiden/death/tick
data merge entity @s {{Motion:[0d,0d,0d],Fire:-1s}}
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
execute if score @s rdCool matches 1.. run scoreboard players remove @s rdCool 1
scoreboard players add @s rdTime 1
execute if score @s rdPhase matches 0 run scoreboard players add @s rdRage 1
# A full gauge waits for the running pattern (and any blink) to finish, then the
# boss transforms where it stands.
execute if score @s rdPhase matches 0 if score @s rdRage matches {RAGE_MAX}.. if score @s rdPat matches 0 unless score @s rdBlink matches 1.. run function rlk:boss/raiden/transform_start
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/transform_tick
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/armor_tick
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/exhausted_tick
execute if score @s rdPhase matches 0 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPhase matches 2 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
# Close-range patterns first close the distance (rdGo); their clock waits at 0 meanwhile.
execute if score @s rdGo matches 1.. if score @s rdPat matches 1..18 run function rlk:boss/raiden/close_in
# Timelines start on the tick after choose: rdTime 1 is every pattern's first frame.
execute if score @s rdPat matches 1..7 if score @s rdTime matches 1.. run function rlk:boss/raiden/normal_dispatch
execute if score @s rdPat matches 11..18 if score @s rdTime matches 1.. run function rlk:boss/raiden/armor_dispatch
execute if score @s rdPat matches 99 if score @s rdTime matches 60.. run function rlk:boss/raiden/finish
# Found the real illusion: a 10 s stun owned by the illusion generator.
execute if score @s rdPat matches 98 run function rlk:boss/raiden/illusion/stun_tick
# Keep the body on the disc without snapping: slide back toward the centre, and only
# scatter-blink home if it is somehow far outside. Tracking uses the avatar, never the camera.
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..21] at @s facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..26] unless score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_to
execute if score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_tick
# Hide the physical rig while illusions, scattering, or the aerial-arm ultimate are active.
scoreboard players set #rdHide rd 0
execute if score @s rdBlink matches 1.. run scoreboard players set #rdHide rd 1
execute if score @s rdPat matches 5 if score @s rdTime matches 1.. run scoreboard players set #rdHide rd 1
execute if score @s rdPat matches 15 if score @s rdTime matches {ASCEND_END}.. run scoreboard players set #rdHide rd 1
execute if score #rdHide rd matches 0 at @s run function rlk:boss/raiden/rig/tick
execute if score #rdHide rd matches 1 run function rlk:boss/raiden/rig_hide
execute if score #rdHide rd matches 0 if score @s rdHidden matches 1.. run function rlk:boss/raiden/rig_shown
execute if score @s rdPat matches 15 run function rlk:boss/raiden/judgment_rig/tick
execute if score @s rdPat matches 15 if score @s rdTime matches 80..173 run function rlk:boss/raiden/camera/try_start
execute if score @s rdPat matches 15 if score @s rdTime matches 174 run function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/bars
''')
write('rig_hide','''
# As boss, at its position before any relocation this tick. Parts wait under the floor
# with teleport_duration 0, so the reappearance frame snaps instead of sliding up/across.
execute unless score @s rdHidden matches 1 as @e[tag=rlk_raiden_part] run data merge entity @s {teleport_duration:0}
scoreboard players set @s rdHidden 1
tp @e[tag=rlk_raiden_part] ~ ~-60 ~
''')
write('rig_shown','''
# 1 = first visible frame (rig/tick already snapped the parts); 2 = restore 1-tick smoothing.
execute if score @s rdHidden matches 2.. as @e[tag=rlk_raiden_part] run data merge entity @s {teleport_duration:1}
execute if score @s rdHidden matches 2.. run return run scoreboard players set @s rdHidden 0
scoreboard players set @s rdHidden 2
''')
write('idle','''
execute if score @s rdWalk matches 1.. run return run function rlk:boss/raiden/movement/walk_tick
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rdAnim 0
execute if score @s rdPhase matches 0 at @s unless entity @e[tag=rlk_body,distance=..5] rotated as @s run function rlk:boss/raiden/approach
execute if score @s rdCool matches ..0 at @s run function rlk:boss/raiden/choose
''')
write('approach','''
scoreboard players set @s rdAnim 1
execute rotated as @s positioned ^ ^ ^0.17 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] run tp @s ~ ~ ~
''')
# Shuffle bag per phase: every move appears once before any repeats, in random order;
# a refilled bag never starts with the move just used. The ultimate (15) is not in the
# bag: it comes on the fourth armoured move (below), at most once per transformation.
BAGS = {0: [1, 2, 3, 4, 5, 6, 7], 2: [11, 12, 13, 14, 16, 17, 18]}
for ph, moves in BAGS.items():
    write(f'bag/count_{ph}', ['scoreboard players set #rdCnt rd 0'] +
          [f'execute if score #rdB{i} rd matches 1 run scoreboard players add #rdCnt rd 1' for i in moves])
    write(f'bag/fill_{ph}', [f'scoreboard players set #rdB{i} rd 1' for i in moves] +
          [f'execute if score @s rdPrev matches {i} run scoreboard players set #rdB{i} rd 0' for i in moves] +
          [call(f'bag/count_{ph}')])
    write(f'bag/draw_{ph}', ['# As the boss: draw one move from the bag into rdPat.', call(f'bag/count_{ph}'),
          f'execute if score #rdCnt rd matches 0 run '+call(f'bag/fill_{ph}'),
          'execute store result score #rdR rd run random value 0..9999',
          'scoreboard players operation #rdR rd %= #rdCnt rd',
          'scoreboard players add #rdR rd 1',
          'scoreboard players set #rdPick rd 0'] +
          sum(([f'execute if score #rdPick rd matches 0 if score #rdB{i} rd matches 1 run scoreboard players remove #rdR rd 1',
                f'execute if score #rdPick rd matches 0 if score #rdB{i} rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd {i}']
               for i in moves), []) +
          ['scoreboard players operation @s rdPat = #rdPick rd'])
write('choose','''
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/bag/draw_0
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/bag/draw_2
# 몽상의 일심 always follows an illusion round that was not broken (illusion/fail_end).
execute if score @s rdPhase matches 0 if score @s rdNext matches 1..7 run scoreboard players operation @s rdPat = @s rdNext
scoreboard players set @s rdNext 0
scoreboard players add @s rdTurns 1
scoreboard players operation #rdTurn rd = @s rdTurns
scoreboard players operation #rdTurn rd %= #rd4 rd
# At most one ultimate in each transformation, guaranteed by the fourth move.
execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 1 if score @s rdPat matches 15 run scoreboard players set @s rdPat 18
execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 0 if score #rdTurn rd matches 0 run scoreboard players set @s rdPat 15
# Boss test hooks (test/lock repeats, test/pattern once) only apply to the current phase.
execute if score @s rdPhase matches 0 if score #rdLock rd matches 1..7 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 2 if score #rdLock rd matches 11..18 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 0 if score #rdForce rd matches 1..7 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPhase matches 2 if score #rdForce rd matches 11..18 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPat = #rdForce rd run scoreboard players set #rdForce rd 0
# Whatever finally runs (bag, forced follow-up, ultimate, test hook) leaves the bag.
'''+'\n'.join(f'execute if score @s rdPat matches {i} run scoreboard players set #rdB{i} rd 0' for i in BAGS[0]+BAGS[2])+'''
scoreboard players operation @s rdPrev = @s rdPat
scoreboard players set @s rdTime 0
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
# A close-range pattern chosen while the player is out of its reach: close in first.
scoreboard players set @s rdGo 0
'''+'\n'.join(f'execute if score @s rdPat matches {i} at @s unless entity @e[tag=rlk_body,distance=..{start}] run scoreboard players set @s rdGo 1' for i,(start,stop) in REACH.items())+'''
''')
# Close-in: dash at the player; scatter-blink in front of them when far away.
write('close_in',[
    '# As the boss with a chosen close-range pattern (rdGo 1..): the clock stays at 0.',
    'scoreboard players set @s rdTime 0',
    'scoreboard players add @s rdGo 1',
    'execute if score @s rdBlink matches 1.. run return 0',
    '# A blink taken because the dash was pinned or timed out: start where she landed.',
    'execute if score @s rdGo matches 100.. run return run function rlk:boss/raiden/close_done',
    'execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet',
    'execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0',
    f'execute if score @s rdGo matches 2 at @s unless entity @e[tag=rlk_body,distance=..{CLOSE_BLINK}] run return run function rlk:boss/raiden/movement/blink_start',
    'scoreboard players set #rdNear rd 0']+[
    f'execute if score @s rdPat matches {i} at @s if entity @e[tag=rlk_body,distance=..{stop}] run scoreboard players set #rdNear rd 1' for i,(start,stop) in REACH.items()]+[
    'execute if score #rdNear rd matches 1 run return run function rlk:boss/raiden/close_done',
    f'execute if score @s rdGo matches {CLOSE_MAX}.. run return run function rlk:boss/raiden/close_blink',
    'scoreboard players set @s rdAnim 21',
    'scoreboard players set #rdStep rd 0',
    f'execute if score @s rdPhase matches 0 at @s rotated as @s positioned ^ ^ ^{CLOSE_STEP[0]} if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] store success score #rdStep rd run tp @s ~ ~ ~',
    f'execute if score @s rdPhase matches 2 at @s rotated as @s positioned ^ ^ ^{CLOSE_STEP[1]} if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] store success score #rdStep rd run tp @s ~ ~ ~',
    '# Pinned (the straight line to the player leaves the arena disc, or a block is in the way).',
    'execute if score #rdStep rd matches 0 run return run function rlk:boss/raiden/close_blink',
    'execute if score @s rdGo matches 3 at @s run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.2',
])
write('close_blink',[
    '# Dash pinned on the rim or timed out: scatter-blink beside the player, then start.',
    'scoreboard players set @s rdGo 100',
    'function rlk:boss/raiden/movement/blink_start',
])
write('close_done',[
    'scoreboard players set @s rdGo 0',
    'scoreboard players set @s rdAnim 0',
    'execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet',
    'execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0',
])
write('finish','''
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/caption/pattern_end
function rlk:boss/raiden/judgment_rig/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdGo 0
kill @e[tag=rlk_rd_blink_dest]
scoreboard players operation #rdWalkTurn rd = @s rdTurns
scoreboard players set #rd2 rd 2
scoreboard players operation #rdWalkTurn rd %= #rd2 rd
execute if score #rdWalkTurn rd matches 0 run function rlk:boss/raiden/movement/walk_start
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 0
scoreboard players set @s rdCool 10
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
''')
write('transform_start','''
function rlk:boss/raiden/camera/release_all
scoreboard players set @s rdGo 0
scoreboard players set @s rdNext 0
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
scoreboard players set @s rdWalk 0
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
scoreboard players set @s rdPhase 1
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players add @s rdCycle 1
# Transforms where it stands (normally only after its pattern ended). A test/forced
# start can land mid-blink: let that blink finish in place without a destination.
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set @s rdAnim 9
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
function rlk:boss/raiden/line/eternal
scoreboard players set #rdCapPat rd 0
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.4
''')
# The burst and its danger circle start at the boss on TRANSFORM_FX; the transform
# clip (46) ends before armor_start at TRANSFORM_LEN.
write('transform_title',['# After her line: the form name and the armour hint.']+'''title @a[tag=player] times 8 55 16
title @a[tag=player] subtitle {text:"번개 갑주를 파괴하면 잠시 무력화됩니다",color:"white"}
title @a[tag=player] title {text:"악요의 요고우 텐마",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 79
scoreboard players set @a[tag=player] ttlT 79
scoreboard players set #rdCap rd 1
# Not a pattern caption: an interrupted illusion caption must not let armor_start\'s
# finish (rdTime 56) cut this one short.
'''.strip().split('\n')+['scoreboard players set #rdCapPat rd 0'])
write('transform_tick',[caption('악요의 요고우 텐마 · 변신'),at('30',call('transform_title')),
    at(str(TRANSFORM_FX),call('vfx/transform')),at(str(TRANSFORM_FX),haz(8,30,18,42)),
    at(str(TRANSFORM_FX+14),sound('entity.lightning_bolt.thunder',.6,.7)),
    at(str(TRANSFORM_LEN),call('armor_start'))])
write('armor_start',f'''
attribute @s minecraft:scale base set 2.2
scoreboard players set @s rdPhase 2
scoreboard players set @s rdShield {SHIELD_MAX}
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdPTime 0
scoreboard players set @s rdTurns 0
scoreboard players set @s rdHitCD 0
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 14
''')
write('armor_tick','''
scoreboard players add @s rdPTime 1
scoreboard players operation #rdMod rd = @s rdPTime
scoreboard players operation #rdMod rd %= #rd4 rd
execute unless score @s rdPat matches 15 if score #rdMod rd matches 0 run scoreboard players remove @s rdShield 1
scoreboard players operation #rdEnergyTick rd = @s rdPTime
scoreboard players set #rd20 rd 20
scoreboard players operation #rdEnergyTick rd %= #rd20 rd
execute if score #rdEnergyTick rd matches 0 unless score #charN tmp matches 3 run scoreboard players remove @a[tag=player,limit=1] energy 100
execute as @a[tag=player,scores={energy=..-1}] run scoreboard players set @s energy 0
execute unless score @s rdPat matches 15 if score @s rdShield matches ..0 run function rlk:boss/raiden/exhausted_start
''')
write('exhausted_start','''
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
attribute @s minecraft:scale base set 1.2
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
scoreboard players set @s rdPhase 3
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 23
scoreboard players set @s rdShield 0
scoreboard players operation @a[tag=player,limit=1] energy = #burstCost100 tmp
title @a[tag=player] times 5 45 15
title @a[tag=player] subtitle {text:"갑주 파괴 · 지금 공격하세요!",color:"green",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 65
scoreboard players set #rdCap rd 1
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3
execute at @s run function rlk:boss/raiden/vfx/armor_break
''')
write('exhausted_tick',[at('46',anim(22)),at(str(EXHAUST-28),anim(24)),at(str(EXHAUST),call('normal_return'))])
write('normal_return','''
attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 0
scoreboard players set @s rdRage 0
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 20
''')
write('bars',f'''
function rlk:boss/raiden/line/tick
execute if score #rdCap rd matches 1 unless entity @a[tag=player,scores={{ttlT=1..}}] run function rlk:boss/raiden/caption/expire
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
# Line 1: level and name (and the armour state). Line 2: the drawn HP bar, numbers on it,
# the white recent-damage trail, and under it the malice gauge / armour / recovery.
execute unless score @s rdPhase matches 2..3 run bossbar set rlk:narukami name [{{text:"Lv.",color:"#FFD86B",bold:true}},{{score:{{name:"@s",objective:"mlv"}},color:"#FFD86B",bold:true}},{{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"}}]
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami name [{{text:"Lv.",color:"#FFD86B",bold:true}},{{score:{{name:"@s",objective:"mlv"}},color:"#FFD86B",bold:true}},{{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"}},{{text:"  · 번개 갑주",color:"#C58BFF"}}]
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami name [{{text:"Lv.",color:"#FFD86B",bold:true}},{{score:{{name:"@s",objective:"mlv"}},color:"#FFD86B",bold:true}},{{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"}},{{text:"  · 갑주 파괴",color:"#7BD88F"}}]
scoreboard players operation #buHp bu = @s mhpC
scoreboard players operation #buMax bu = @s mhpM
scoreboard players set #buSubCol bu 0
execute if score @s rdPhase matches 0 run scoreboard players operation #buSub bu = @s rdRage
execute if score @s rdPhase matches 0 run scoreboard players set #buSubMax bu {RAGE_MAX}
execute if score @s rdPhase matches 0 run scoreboard players set #buSubCol bu 8
execute if score @s rdPhase matches 1 run scoreboard players operation #buSub bu = @s rdTime
execute if score @s rdPhase matches 1 run scoreboard players set #buSubMax bu {TRANSFORM_LEN}
execute if score @s rdPhase matches 1 run scoreboard players set #buSubCol bu 1
execute if score @s rdPhase matches 2 run scoreboard players operation #buSub bu = @s rdShield
execute if score @s rdPhase matches 2 run scoreboard players set #buSubMax bu {SHIELD_MAX}
execute if score @s rdPhase matches 2 run scoreboard players set #buSubCol bu 1
execute if score @s rdPhase matches 3 run scoreboard players operation #buSub bu = @s rdTime
execute if score @s rdPhase matches 3 run scoreboard players set #buSubMax bu {EXHAUST}
execute if score @s rdPhase matches 3 run scoreboard players set #buSubCol bu 9
function rlk:bossui/draw
bossbar set rlk:narukami_state name {{nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}}
''')
write('incoming','''
# Called after normal damage/defense modifiers, before damage is deducted.
execute if score #dmg tmp matches ..0 run return 0
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/shield_hit
execute if score @s rdPhase matches 3 run scoreboard players operation #dmg tmp += #dmg tmp
# Guarantee the first transformation cannot be skipped by one enormous hit.
scoreboard players operation #rdFloor rd = @s mhpM
scoreboard players set #rdPct rd 55
scoreboard players operation #rdFloor rd *= #rdPct rd
scoreboard players operation #rdFloor rd /= #rd100 rd
scoreboard players operation #rdAfter rd = @s mhpC
scoreboard players operation #rdAfter rd -= #dmg tmp
execute if score @s rdPhase matches 0 if score @s rdCycle matches 0 if score #rdAfter rd <= #rdFloor rd run function rlk:boss/raiden/threshold
execute if score #dmg tmp matches 1.. run function rlk:boss/raiden/rig/flash
''')
write('threshold',f'''
scoreboard players operation #dmg tmp = @s mhpC
scoreboard players operation #dmg tmp -= #rdFloor rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 0
scoreboard players set @s rdRage {RAGE_MAX}
''')
write('shield_hit','''
# Armor absorbs 80% body damage. Every character can break it; fire and ice work fastest.
execute if score #dmg tmp matches ..0 run return 0
execute if score @s rdHitCD matches ..0 if score #dmg tmp matches 1.. run function rlk:boss/raiden/shield_drain
scoreboard players set #rdDiv rd 5
scoreboard players operation #dmg tmp /= #rdDiv rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
''')
write('shield_drain',[
    f'# One drain per {SHIELD_CD} ticks however many hits/DoT ticks land. #elem: 0 physical 1 fire 2 water',
    '# 3 thunder 4 ice 5 rock 6 wind 7 grass 8 void; reaction/DoT damage (#tfm) drains least.',
    f'scoreboard players set #rdDrain rd {DRAIN_DEFAULT}']+[
    f'execute if score #elem tmp matches {e} run scoreboard players set #rdDrain rd {v}' for e,v in DRAIN.items()]+[
    f'execute if score #tfm tmp matches 1 run scoreboard players set #rdDrain rd {DRAIN_REACTION}',
    'scoreboard players operation @s rdShield -= #rdDrain rd',
    f'scoreboard players set @s rdHitCD {SHIELD_CD}'])
write('hurt','''
# Hazard origin is the knockback source; cm handles avatar, defense and dash invulnerability.
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
# Boss damage multiplier (load: #bossDmgMul %), on top of the mob level scaling. Every
# hazard and the shadow bites set #cmDmg fresh before calling this.
scoreboard players operation #cmDmg tmp *= #bossDmgMul tmp
scoreboard players operation #cmDmg tmp /= #100 tmp
function rlk:cm/hit_pl
# A hit that lands (not dodged) feeds the malice gauge, like the original.
execute unless score #dodged tmp matches 1 as @e[tag=rlk_raiden,scores={rdPhase=0,rdDeath=0},limit=1] run scoreboard players add @s rdRage '''+str(RAGE_HIT)+'''
''')

write('normal_dispatch',[f'execute if score @s rdPat matches {i} run '+call('patterns/'+str(i)) for i in range(1,8)])
write('armor_dispatch',[f'execute if score @s rdPat matches {i} run '+call('patterns/'+str(i)) for i in range(11,19)])

patterns={}
def pattern(i,title):
    lines=[at('1',caption(title))];patterns[i]=lines;return lines
def event(lines,t,*commands):
    # Fast strike keys reach contact after 2 ticks (heavy 3) + interpolation 1.
    # Begin each clip just before the danger volume lands, not on the damage tick.
    for cmd in commands:
        n=int(cmd.rsplit(' ',1)[1]) if cmd.startswith('scoreboard players set @s rdAnim ') else -1
        lead=4 if n in (15,17) else 3 if n in (3,4,6,8,11,13) else 0
        lines.append(at(str(max(1,t-lead)),cmd))
def end(lines,t):event(lines,t,call('finish'))
face='execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet'
flat='execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0'
target='execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run '
center='execute at @e[tag=rlk_raiden_arena,limit=1] run '
# Tells: every telegraphed strike gets W extra ticks over the old 8-13 (so at least
# 12 ticks = 0.6 s; eyes 18), then 4-7 ticks of recovery before the next wind-up.
# Every wind clip (slash/thrust 6, cast 10, sweep/clap/slam 8, judgment 14) reaches its
# hold pose and simply holds it longer before the strike clip starts 3-4 ticks ahead.
W=4
def tell(t): return max(t+W,12)

def gated(lines,t,cond,*commands):
    # event() with an extra score condition (e.g. a random follow-up).
    for cmd in commands:
        n=int(cmd.rsplit(' ',1)[1]) if cmd.startswith('scoreboard players set @s rdAnim ') else -1
        lead=4 if n in (15,17) else 3 if n in (3,4,6,8,11,13) else 0
        lines.append(f'execute if score @s rdTime matches {max(1,t-lead)} {cond} at @s rotated as @s run {cmd}')
p=pattern(1,'4연격 · 가로 베기 세 번, 나기나타 내려찍기, 이어지는 검기')
t=1
for n in (3,4,3):
    event(p,t,face,flat,anim(2),haz(1,tell(8),9))
    event(p,t+tell(8),anim(n),sound('entity.player.attack.sweep',1,.7))
    t+=tell(8)+5
# Fourth hit: the naginata is driven into the floor; lightning bursts around her and
# falls where the player stands.
hit=t+tell(10)
event(p,t,face,flat,anim(5),haz(8,tell(10),15),target+haz(3,tell(10),12))
event(p,hit,anim(6),sound('entity.lightning_bolt.impact',.9,.75),sound('item.trident.hit_ground',1,.6))
# Half the time a flying sword wave follows (watch her to the end).
p.append(f'execute if score @s rdTime matches {hit+2} store result score #rdFollow rd run random value 0..1')
gated(p,hit+6,'if score #rdFollow rd matches 1',face,flat,anim(2),haz(13,tell(8),12))
gated(p,hit+6+tell(8),'if score #rdFollow rd matches 1',anim(3),call('object_vfx/slash'),sound('entity.player.attack.sweep',1.1,.9))
gated(p,hit+8,'if score #rdFollow rd matches 0',call('finish'))
gated(p,hit+12+tell(8),'if score #rdFollow rd matches 1',call('finish'))
p=pattern(2,'회전 참격 · 빠른 번개 칼날 세 개와 큰 초승달 검기')
event(p,1,call('line/will'))
# She spins in place throwing three fast blades at the player, then a big crescent.
event(p,1,face,flat,anim(20),sound('entity.breeze.charge',.8,.8))
# Blades leave every 6 ticks; each is marked tell(6) ticks before it flies.
for t in [4,10,16]:
    event(p,t,face,flat,haz(13,tell(6),10))
    # Blades overlap; launch each wave from its own hazard marker (yaw locked at its tell).
    event(p,t+tell(6),f'execute as @e[tag=rlk_rd_hazard,scores={{rdShape=13,rdHAge={tell(6)-1}}},limit=1] at @s run '+call('object_vfx/slash'),sound('entity.breeze.shoot',.8,1.25))
t=16+tell(6)+4
event(p,t,face,flat,anim(2),haz(10,tell(10),18))
event(p,t+tell(10),anim(3),call('object_vfx/slash'),sound('entity.player.attack.sweep',1.2,.6))
end(p,t+tell(10)+8)
p=pattern(3,'뇌명 · 순간이동 후 발도')
event(p,1,call('line/noemyeong'))
# Each scatter blink keeps the rig hidden for 8 ticks (reforms on blink start + 8).
event(p,1,anim(21),sound('entity.breeze.charge',.8,.7),call('movement/blink_start'))
t=10+tell(8)
event(p,10,face,flat,anim(2),haz(2,tell(8),16));event(p,t,anim(6),sound('entity.player.attack.sweep',1.1,.65))
event(p,t+6,call('movement/blink_start'));event(p,t+15,face,flat,anim(2),haz(1,tell(8),15))
event(p,t+15+tell(8),anim(4));end(p,t+22+tell(8))
p=pattern(4,'마가츠의 뇌안 · 하나를 파괴하고 빈 원으로 이동')
event(p,1,anim(7),call('eyes_start'),call('line/eyes'))
event(p,16,anim(8));event(p,40,call('eyes_arm'));event(p,59,anim(18));end(p,70)
# Pattern 5 (분신 · 진짜 찾기) belongs to build_raiden_illusions.py; it ends itself.
patterns[5]=[call('illusion/tick')]
p=pattern(6,'낙뢰 · 표시된 자리에서 벗어나세요')
event(p,1,call('line/command'))
for k in range(4):
    t=1+k*(tell(9)+4)
    event(p,t,anim(7),target+haz(3,tell(9),12));event(p,t+tell(9),anim(8),sound('entity.lightning_bolt.impact',.7,.8))
end(p,t+tell(9)+5)
p=pattern(7,'몽상의 일심 · 가장자리의 번개 구슬 사이로 피하세요')
# As in the original: she blinks to the centre, electro orbs fall along the outer edge,
# then time stops and one cut covers nearly the whole arena (radius 19). The orbs burst
# at the same moment, so the only cover is between them at the very edge.
HIT=42
event(p,1,call('line/calm'),center+call('movement/blink_to'),sound('entity.warden.sonic_charge',.6,1.4))
event(p,10,anim(7))
event(p,12,center+haz(14,HIT-12,30))
for k in range(8):
    t=10+2*k
    event(p,t,center+f'execute rotated {45*k} 0 positioned ^ ^ ^21 run '+haz(3,HIT-t,10),
          center+f'execute rotated {45*k} 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2')
event(p,HIT-4,call('line/sever_one'))
event(p,HIT-2,sound('block.beacon.deactivate',.9,.5))
event(p,HIT,anim(8),sound('entity.lightning_bolt.thunder',.9,.85))
end(p,HIT+10)
p=pattern(11,'거대 팔 연격 · 검의 궤적과 투척 낙뢰에 주의')
event(p,1,call('line/cleave_all'))
for t in [1,6+tell(11)]:
    event(p,t,face,flat,anim(10),haz(4,tell(11),19));event(p,t+tell(11),anim(11),sound('entity.player.attack.sweep',1.2,.62))
t+=tell(11)+5
event(p,t,anim(7),target+haz(3,tell(10),22));event(p,t+tell(10),anim(8));end(p,t+tell(10)+7)
p=pattern(12,'인공팔 협격 · 따라오는 두 손이 박수치기 전에 빠져나오세요')
# Two hands appear at the player's sides and follow them, then lock and clap shut.
event(p,1,face,flat,anim(12),call('clap/spawn'),call('line/prison'))
p.append('execute if score @s rdTime matches 1..'+str(CLAP_LOCK-1)+' run '+call('clap/follow'))
event(p,CLAP_LOCK,call('clap/lock'))
event(p,CLAP_LOCK+CLAP_TELL-3,call('clap/shut'))
event(p,CLAP_LOCK+CLAP_TELL,anim(13),sound('entity.iron_golem.attack',1,.65),sound('entity.zombie.attack_iron_door',.7,.6))
event(p,CLAP_LOCK+CLAP_TELL+3,call('clap/fade'))
event(p,CLAP_LOCK+CLAP_TELL+9,call('clap/clear'))
end(p,CLAP_LOCK+CLAP_TELL+10)
p=pattern(13,'그림자 손 · 따라오는 그림자에서 계속 달아나세요')
# A shadow chases the player (repeated small damage while it covers them), then a hand
# slams down where it stops. Contract with build_raiden_rig.mjs: the floating hand lands
# at hazard age 12 (SLAM_CONTACT); the finish 12 ticks after landing lets it fade.
event(p,1,anim(14),call('shadow/spawn'),sound('entity.warden.dig',.6,1.4),call('line/prison'))
p.append('execute if score @s rdTime matches 1..'+str(SHADOW_LOCK-1)+' run '+call('shadow/follow'))
event(p,SHADOW_LOCK,call('shadow/lock'))
event(p,SHADOW_LOCK+12,anim(15),sound('entity.generic.explode',.65,.72))
end(p,SHADOW_LOCK+24)
p=pattern(14,'금강괴멸파 · 퍼지는 번개 고리를 점프로 회피')
event(p,1,anim(7),call('stakes_start'),call('line/cheonsu'));event(p,15,anim(8))
# As in the original: each stake fires once in turn, twice round, then all three at once.
# Rings overlap in time (each travels RING_FRAMES ticks to the far wall).
for k,i in enumerate([1,2,3,1,2,3]):
    event(p,20+28*k,call('stakes_pulse_'+str(i)))
LAST=20+28*6+4
event(p,LAST,call('stakes_pulse'))
end(p,LAST+STAKE_TELL+RING_FRAMES+4)
p=pattern(15,'최종 재앙 · 추억의 꽃을 공격한 뒤 보호막 안으로!')
event(p,1,call('judgment_start'),anim(16));
p.append(f'execute if score @s rdTime matches 2..{ASCEND_END-1} at @s run tp @s ~ ~{ASCEND_STEP} ~')
for t,(bx,bz) in zip([3,7,11,15,19,23],[(9,-6),(-11,4),(5,12),(-7,-12),(13,6),(-14,-3)]):
    event(p,t,center+f'execute positioned ~{bx} ~ ~{bz} run '+call('vfx/judgment_bolt'),center+f'execute positioned ~{bx} ~ ~{bz} run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4')
event(p,ASCEND_END,call('movement/depart'),sound('entity.lightning_bolt.thunder',1,.6),center+'execute positioned ~ ~ ~-8 run tp @s ~ ~ ~ 0 0')
# The gameplay hint follows once the line has been spoken (line ends ~tick 46).
event(p,ASCEND_END+21,call('judgment_hint'));event(p,30,sound('block.beacon.ambient',.6,.5));event(p,70,sound('block.portal.ambient',.45,.55))
# The flower retains the full six-second response window despite quicker recovery.
# The hidden body already waits at centre-8; it reforms there facing the player.
event(p,120,call('judgment_strike'));event(p,170,face,flat,call('movement/arrive'));end(p,176)
p=pattern(16,'신속한 발도 / 몽상 · 단절')
# Two moves of the original, picked at random:
#  0 신속한 발도: a charged horizontal iai around her; a white flash marks the dodge.
#  1 몽상·단절: the giant sword rises while a straight line lights up on the floor, she
#    calls "단절!" and brings it straight down along the line; a weak field rings her.
p.append('execute if score @s rdTime matches 1 store result score #rdVar rd run random value 0..1')
IAI='if score #rdVar rd matches 0'
hit=1+tell(14)
gated(p,1,IAI,face,flat,anim(10),haz(4,tell(14),30),haz(10,tell(14),26))
gated(p,hit-4,IAI,'execute positioned ^ ^2.4 ^1.2 run '+call('object_vfx/object_break'),sound('block.amethyst_block.resonate',1,1.9))
gated(p,hit,IAI,anim(11),sound('entity.lightning_bolt.thunder',.8,.68))
gated(p,hit+11,IAI,call('finish'))
CUT='if score #rdVar rd matches 1'
hit=1+tell(16)
gated(p,1,CUT,face,flat,anim(16),haz(5,tell(16),34),haz(8,12,5),sound('block.beacon.power_select',.7,.6))
gated(p,hit-5,CUT,call('line/sever'))
gated(p,hit,CUT,anim(17),sound('entity.lightning_bolt.thunder',.9,.6),sound('entity.generic.explode',.6,.8))
gated(p,hit+12,CUT,call('finish'))
p=pattern(17,'검파 연사 · 다섯 갈래 뒤 넓은 가로 검파')
event(p,1,call('line/goemyeol'))
t=1+tell(10)
event(p,1,face,flat,anim(7),haz(9,tell(10),17));event(p,t,anim(8),sound('entity.breeze.shoot',.8,.72))
event(p,t+5,face,flat,anim(10),haz(10,tell(10),21));event(p,t+5+tell(10),anim(11));end(p,t+12+tell(10))
p=pattern(18,'발도 돌진 · 고정된 직선 경로를 피하세요')
event(p,1,call('line/pierce'))
t=1+tell(10)
event(p,1,face,flat,anim(2),haz(5,tell(10),22));event(p,t,anim(21),sound('item.trident.riptide_3',.7,.8))
p.append(f'execute if score @s rdTime matches {t}..{t+11} at @s rotated as @s positioned ^ ^ ^0.75 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] run tp @s ~ ~ ~')
# After the dash she keeps cutting: two wide sweeps in a row.
t+=14
event(p,t,face,flat,anim(10),haz(4,tell(9),19));event(p,t+tell(9),anim(11),sound('entity.player.attack.sweep',1.2,.62))
t+=tell(9)+4
event(p,t,face,flat,anim(10),haz(4,tell(8),19));event(p,t+tell(8),anim(11),sound('entity.player.attack.sweep',1.2,.7));end(p,t+tell(8)+7)
for i,p in patterns.items():write('patterns/'+str(i),p)

# Following clap hands (pattern 12). Display-only hands owned by the boss; the hazard is
# created on lock at the hands' midpoint, facing along the boss -> player line.
HAND='{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/support_hand_%s"}}'
def hand_tf(side,gap):
    # Fingers up, palm facing the other hand (half turns about the (1,0,+-1) diagonals of
    # the support-hand model: fingers -Y, palm -Z), hand centred gap blocks to the side.
    x=gap if side=='l' else -gap
    q='[0.7071068f,0f,0.7071068f,0f]' if side=='l' else '[0.7071068f,0f,-0.7071068f,0f]'
    return '{translation:[%.3ff,1.6f,0f],left_rotation:%s,scale:[3.6f,3.6f,3.6f],right_rotation:[0f,0f,0f,1f]}'%(x,q)
write('clap/spawn',[
    '# As the boss. Two hands appear beside the player, facing along the boss -> player line.',
    'kill @e[tag=rlk_rd_clap]',
    'execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @s feet rotated ~180 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_clap","rlk_rd_clap_l"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:2,interpolation_duration:4,view_range:3f,width:12f,height:8f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:'+hand_tf('l',4.2).replace('3.6f,3.6f,3.6f','0.2f,0.2f,0.2f')+',item:'+HAND%'l'+'}',
    'execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @s feet rotated ~180 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_clap","rlk_rd_clap_r"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:2,interpolation_duration:4,view_range:3f,width:12f,height:8f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:'+hand_tf('r',4.2).replace('3.6f,3.6f,3.6f','0.2f,0.2f,0.2f')+',item:'+HAND%'r'+'}',
    'execute as @e[tag=rlk_rd_clap] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_raiden,limit=1] feet',
    'execute as @e[tag=rlk_rd_clap] at @s rotated ~180 0 run tp @s ~ ~ ~ ~ 0',
    'data merge entity @e[tag=rlk_rd_clap_l,limit=1] {start_interpolation:0,transformation:'+hand_tf('l',4.2)+'}',
    'data merge entity @e[tag=rlk_rd_clap_r,limit=1] {start_interpolation:0,transformation:'+hand_tf('r',4.2)+'}',
])
write('clap/follow',[
    '# As the boss: the hands drift after the player (slower than a sprint).',
    'execute as @e[tag=rlk_rd_clap] at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^ ^0.3 unless entity @e[tag=rlk_body,distance=..0.4] run tp @s ~ 201 ~',
    'execute as @e[tag=rlk_rd_clap] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_raiden,limit=1] feet',
    'execute as @e[tag=rlk_rd_clap] at @s rotated ~180 0 run tp @s ~ ~ ~ ~ 0',
])
write('clap/lock',[
    '# As the boss: the hands stop; the clap zone (8 x 8) is centred between them.',
    'execute as @e[tag=rlk_rd_clap_l,limit=1] at @s rotated as @s positioned ^ ^ ^-4 run '+haz(7,CLAP_TELL,25),
    'execute as @e[tag=rlk_rd_clap] run data merge entity @s {teleport_duration:0}',
])
write('clap/shut',[
    '# Three ticks before the hit: the palms slam together over the zone.',
    'data merge entity @e[tag=rlk_rd_clap_l,limit=1] {interpolation_duration:3,start_interpolation:0,transformation:'+hand_tf('l',.7)+'}',
    'data merge entity @e[tag=rlk_rd_clap_r,limit=1] {interpolation_duration:3,start_interpolation:0,transformation:'+hand_tf('r',.7)+'}',
])
write('clap/fade',[
    'execute as @e[tag=rlk_rd_clap] run data merge entity @s {interpolation_duration:5,start_interpolation:0,transformation:{translation:[0f,2.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}',
])
write('clap/clear',['kill @e[tag=rlk_rd_clap]'])

# Chasing shadow (pattern 13): a dark decal follows the player more slowly than a sprint,
# nibbling them while it covers them, then the floating hand slams where it stopped.
write('shadow/spawn',[
    'kill @e[tag=rlk_rd_shadow]',
    'execute at @e[tag=rlk_body,limit=1] positioned ~ 201.03 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_shadow"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:5,view_range:3f,width:6f,height:2f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/after_3"}}}',
    'data merge entity @e[tag=rlk_rd_shadow,limit=1] {start_interpolation:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[19f,19f,19f],right_rotation:[0f,1f,0f,0f]}}',
    'scoreboard players set #rdShadowT rd 0',
])
write('shadow/follow',[
    '# As the boss. 0.26 block/tick: walking cannot outrun it, sprinting/dashing can.',
    f'execute as @e[tag=rlk_rd_shadow,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^ ^0.26 unless entity @e[tag=rlk_body,distance=..0.3] run tp @s ~ 201.03 ~',
    'scoreboard players add #rdShadowT rd 1',
    'execute if score #rdShadowT rd matches 8.. run '+call('shadow/bite'),
])
write('shadow/bite',[
    'scoreboard players set #rdShadowT rd 0',
    'execute as @e[tag=rlk_rd_shadow,limit=1] at @s if entity @e[tag=rlk_body,distance=..1.8] run '+call('shadow/hurt'),
])
write('shadow/hurt',[
    '# As the shadow (knockback source).',
    'scoreboard players set #cmDmg tmp 6',
    'scoreboard players operation #cmLv tmp = @e[tag=rlk_raiden,limit=1] mlv',
    'scoreboard players set #cmEl tmp 3',
    call('hurt'),
])
write('shadow/lock',[
    '# As the boss: the shadow becomes the slam target (hand + 12-tick disk, radius 5).',
    'execute at @e[tag=rlk_rd_shadow,limit=1] positioned ~ 201 ~ run '+haz(6,12,24),
    'execute at @e[tag=rlk_rd_shadow,limit=1] positioned ~ 201 ~ run '+call('rig/target_slam_spawn'),
    'kill @e[tag=rlk_rd_shadow]',
])

write('blink_relocate','''
# Hidden middle of a scatter blink. A movement/blink_to marker wins; otherwise reform
# 5 blocks ahead of the player, or 5 blocks from the player toward the centre.
execute if entity @e[tag=rlk_rd_blink_dest,limit=1] run return run function rlk:boss/raiden/blink_dest
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^ ^5 positioned ~ 201 ~ run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^5 positioned ~ 201 ~ run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] run tp @s ~ ~ ~
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
''')
write('blink_dest','''
execute at @e[tag=rlk_rd_blink_dest,limit=1] run tp @s ~ ~ ~
kill @e[tag=rlk_rd_blink_dest]
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
''')
write('blink',[call('movement/blink_start')])

write('object/create','''
# At the desired ground point, as boss; kinds: 1 eye,2 illusion,3 flower,4 stake.
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_object","rlk_rd_objnew","rlk_mob","rlk_mapv"],NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,CanPickUpLoot:0b,IsBaby:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjKind $(kind)
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjId $(id)
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjHP $(hp)
scoreboard players set @e[tag=rlk_rd_objnew] rdHitCD 0
scoreboard players set @e[tag=rlk_rd_objnew] rdOAge 0
scoreboard players set @e[tag=rlk_rd_objnew] rdReal 0
scoreboard players set @e[tag=rlk_rd_objnew] mhpC 1000000
scoreboard players set @e[tag=rlk_rd_objnew] mhpM 1000000
scoreboard players set @e[tag=rlk_rd_objnew] mhp0 1000000
scoreboard players set @e[tag=rlk_rd_objnew] xpDrop 0
scoreboard players operation @e[tag=rlk_rd_objnew] mlv = @e[tag=rlk_raiden,limit=1] mlv
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:max_health base set 1024
execute as @e[tag=rlk_rd_objnew] run data modify entity @s Health set value 1024f
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:attack_damage base set 0
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:knockback_resistance base set 1
team join rlk_cam @e[tag=rlk_rd_objnew]
$summon minecraft:item_display ~ ~$(y) ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_objvisual","rlk_rd_visnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/$(model)"}},item_display:"none",brightness:{sky:15,block:15},view_range:2f,transformation:{translation:[0f,0f,0f],scale:[1f,1f,1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
$scoreboard players set @e[tag=rlk_rd_visnew] rdObjId $(id)
tag @e[tag=rlk_rd_visnew] remove rlk_rd_visnew
execute as @e[tag=rlk_rd_objnew,scores={rdObjKind=4}] run tag @s remove rlk_mob
execute as @e[tag=rlk_rd_objnew] at @s run function rlk:boss/raiden/object_vfx/create
execute as @e[tag=rlk_rd_objnew,scores={rdObjKind=3}] at @s run function rlk:boss/raiden/orb/create
tag @e[tag=rlk_rd_objnew] remove rlk_rd_objnew
''')
write('object/tick','''
scoreboard players add @s rdOAge 1
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
data modify entity @s Health set value 1024f
data merge entity @s {Fire:-1s,Motion:[0d,0d,0d]}
execute unless score @s rdObjKind matches 4 run function rlk:mob/shield_ensure
execute if score @s rdObjKind matches 3 at @s run function rlk:boss/raiden/orb/tick
''')
write('object/on_hit','''
# Gameplay objects count landed attacks, never award mob loot or proc an infinite HP pool.
scoreboard players set #hitLanded tmp 1
execute if score @s rdHitCD matches 1.. run return 0
execute if score @s rdObjKind matches 4 run return 0
scoreboard players set @s rdHitCD 4
scoreboard players set #rdObjectDrain rd 1
execute if score @s rdObjKind matches 3 if score #elem tmp matches 3 run scoreboard players set #rdObjectDrain rd 4
scoreboard players operation @s rdObjHP -= #rdObjectDrain rd
execute if score @s rdObjHP matches 1.. at @s run function rlk:boss/raiden/object_vfx/hit
playsound minecraft:entity.player.attack.knockback player @a[tag=player] ~ ~ ~ .65 .7 .2
execute if score @s rdObjHP matches ..0 run function rlk:boss/raiden/object/break
''')
write('object/break','''
execute if score @s rdObjKind matches 3 run function rlk:boss/raiden/orb/remove
execute at @s run function rlk:boss/raiden/object_vfx/break
scoreboard players operation #rdObjectId rd = @s rdObjId
execute as @e[tag=rlk_rd_objvisual] if score @s rdObjId = #rdObjectId rd run kill @s
# An eye's armed danger circle disappears as soon as the eye is destroyed.
execute if score @s rdObjKind matches 1 at @s run kill @e[tag=rlk_rd_hazard,distance=..0.2]
execute if score @s rdObjKind matches 1 run scoreboard players remove @e[tag=rlk_raiden] rdRage 50
execute as @e[tag=rlk_raiden,scores={rdRage=..-1}] run scoreboard players set @s rdRage 0
execute if score @s rdObjKind matches 3 at @s run function rlk:boss/raiden/dome_create
# As the broken illusion object, before it is removed (build_raiden_illusions.py).
execute if score @s rdObjKind matches 2 at @s run function rlk:boss/raiden/illusion/on_break
kill @s
''')
write('object/clear','''
function rlk:boss/raiden/orb/clear
kill @e[tag=rlk_rd_object]
kill @e[tag=rlk_rd_objvisual]
''')
write('eyes_start',[call('object/clear'),
    center+'execute positioned ~-10 ~ ~-6 run '+obj(1,'electro_orb',3,1,.3),
    center+'execute positioned ~10 ~ ~-6 run '+obj(1,'electro_orb',3,2,.3),
    center+'execute positioned ~ ~ ~11 run '+obj(1,'electro_orb',3,3,.3),
    sound('block.beacon.activate',.7,.7)])
write('eyes_arm',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=1}] at @s run '+haz(12,18,34)])
write('stakes_start',[call('object/clear')]+[
    center+f'execute positioned ~{x} ~ ~{z} run '+obj(4,'lightning_stake',1,i,0)
    for i,(x,z) in enumerate(STAKES,1)])
RING=haz(11,STAKE_TELL,14,STAKE_TELL+RING_FRAMES+5)
write('stakes_pulse',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=4}] at @s run '+RING,sound('block.beacon.power_select',.55,.7)])
for i in [1,2,3]:
    write('stakes_pulse_'+str(i),[f'execute as @e[tag=rlk_rd_object,scores={{rdObjKind=4,rdObjId={i}}}] at @s run '+RING,
        f'execute as @e[tag=rlk_rd_object,scores={{rdObjKind=4,rdObjId={i}}}] at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3'])
write('judgment_start',[call('object/clear'),'scoreboard players set @s rdUltUsed 1','scoreboard players set @s rdWalk 0',
    center+call('judgment_rig/start'),
    center+call('vfx/judgment_warning'),
    center+'execute positioned ~ ~ ~3 run '+obj(3,'remembrance_flower',4,1,.05),
    '# She stays in view: lightning gathers around her and she rises (patterns/15 lifts her).',
    call('vfx/judgment_ascend'),
    call('line/mangeop'),
    sound('entity.wither.ambient',.7,.5),sound('block.beacon.activate',.9,.5)])
write('judgment_hint',[
    'title @a[tag=player] times 4 85 16',
    'title @a[tag=player] subtitle {text:"꽃을 공격 → 보호막 안으로! 번개 1타 / 다른 공격 4타",color:"aqua",bold:true}',
    'execute as @a[tag=player] run function rlk:view/ttl_blank',
    'scoreboard players set @a[tag=player] ttlT 105',
    'scoreboard players set #rdCap rd 1',
    'scoreboard players set #rdCapPat rd 1',
])
write('dome_create','''
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_dome"]}
scoreboard players set @e[tag=rlk_rd_dome] rdTime 0
function rlk:boss/raiden/vfx/dome_create
playsound minecraft:block.beacon.activate player @a[tag=player] ~ ~ ~ .85 1.25 .4
''')
# A persistent wire dome marks the exact safe radius. Keep the old entry point
# harmless for callers retained across reloads; no particle-only replacement.
write('dome_draw',['# Safe dome is rendered by vfx/dome_create.'])
write('dome_tick','''
scoreboard players add @s rdTime 1
execute if score @s rdTime matches 180.. run kill @s
''')
write('judgment_strike',f'''
scoreboard players set #rdSafe rd 0
execute as @e[tag=rlk_rd_dome,limit=1] at @s run function rlk:boss/raiden/dome_contains
execute if score #rdSafe rd matches 0 as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:boss/raiden/judgment_fatal
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/vfx/judgment_strike
# A successful defence cracks a quarter of the armor.
execute if score #rdSafe rd matches 1 run scoreboard players remove @s rdShield {FLOWER_BREAK}
''')
write('judgment_fatal','''
# This announced encounter mechanic requires the flower dome, not a timed dash.
# Setting custom HP to zero preserves the existing death / Ronova revival flow.
execute if score @s dead matches 1 run return 0
execute if score @s rnDie matches 1.. run return 0
scoreboard players operation #hurtDmg tmp = @s curHealth
scoreboard players set #elem tmp 3
function rlk:player/hurt_do
scoreboard players set @s curHealth 0
function rlk:player/die
''')
write('dome_contains','''
# The entire marked ground circle is safe, including a player jumping inside it.
execute unless entity @e[tag=rlk_body,distance=..7,limit=1] run return 0
execute store result score #rdSafeX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #rdSafeZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
execute store result score #rdDomeX rd run data get entity @s Pos[0] 100
execute store result score #rdDomeZ rd run data get entity @s Pos[2] 100
scoreboard players operation #rdSafeX rd -= #rdDomeX rd
scoreboard players operation #rdSafeZ rd -= #rdDomeZ rd
scoreboard players operation #rdSafeX rd *= #rdSafeX rd
scoreboard players operation #rdSafeZ rd *= #rdSafeZ rd
scoreboard players operation #rdSafeX rd += #rdSafeZ rd
execute if score #rdSafeX rd matches ..160000 run scoreboard players set #rdSafe rd 1
''')

# ---- Boss test: fight only Narukami in the real boss room, no run needed ----------
T='[{text:"[보스 테스트] ",color:"light_purple",bold:true},'
def cmd_link(command,label=None,color='yellow'):
    return f'{{text:"{label or command}",color:"{color}",bold:false,click_event:{{action:"suggest_command",command:"{command}"}}}}'
TEST='/function rlk:boss/raiden/test/'
HELP=(T+'{text:"명령: ",color:"gray",bold:false},'
      +cmd_link(TEST+'start','start')+',{text:" 처음부터 · ",color:"gray",bold:false},'
      +cmd_link(TEST+'armored','armored')+',{text:" 갑주 단계 · ",color:"gray",bold:false},'
      +cmd_link(TEST+'pattern {id:11}','pattern {id:N}')+',{text:" 다음 패턴(1~7, 11~18) · ",color:"gray",bold:false},'
      +cmd_link(TEST+'lock {id:11}','lock {id:N}')+',{text:" 패턴 고정(0 해제) · ",color:"gray",bold:false},'
      +cmd_link(TEST+'level {lv:12}','level {lv:N}')+',{text:" 보스 레벨 · ",color:"gray",bold:false},'
      +cmd_link(TEST+'stop','stop')+',{text:" 종료 후 로비",color:"gray",bold:false}]')
write('test/start','''
# /function rlk:boss/raiden/test/start (@s = 'player'): fight only Narukami, normal phase.
# Uses the real boss room (room/raiden layout in the forceloaded dungeon area) and the
# run flags (#active room 1) so room tick, death and cleanup flows all behave as in a run.
# Re-running restarts the fight. Player death or test/stop returns to the lobby.
execute unless entity @s[tag=player] run return run tellraw @s {text:"[보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s '''+T+'{text:"던전 구역이 준비되지 않았습니다. 먼저 ",color:"gray",bold:false},'+cmd_link('/function rlk:room/setup')+''',{text:" 을 실행하세요.",color:"gray",bold:false}]
execute if score #active room matches 1 unless score #rdTest rd matches 1 run return run tellraw @s '''+T+'{text:"진행 중인 런이 있습니다. ",color:"gray",bold:false},'+cmd_link('/function rlk:run/stop')+''',{text:" 후 다시 실행하세요.",color:"gray",bold:false}]
# Peaceful discards the husk body at once, which would read as an instant win.
execute store result score #rdDiff rd run difficulty
execute if score #rdDiff rd matches 0 run return run tellraw @s '''+T+'''{text:"난이도가 '평화로움'이면 나루카미가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.",color:"gray",bold:false}]
execute if score @s dead matches 1 run return 0
# The map screen restores its saved position/game mode on close: close it before moving.
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #rdTest rd 1
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
# Stage-2 boss slot (Narukami's planned stage): level = (chapter-1)*6 + mapIdx + 1 = 12
# (test/level changes it).
scoreboard players set #active room 1
scoreboard players set #chapter room 2
scoreboard players set #mapIdx room 5
scoreboard players set #mapType room 8
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
execute in minecraft:overworld run function rlk:room/gen
# Open the arena at once, put the player inside facing the centre, start the fight now.
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2,zst=0}] run function rlk:room/zone_build
execute in minecraft:overworld run tp @s 0.5 201 14.5 180 0
function rlk:view/sync
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2,zst=1}] at @s run function rlk:room/zone_enter
scoreboard players set #spawnT room 0
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2}] at @s run function rlk:room/mob_wave
scoreboard players operation @s curHealth = @s maxHealth
tellraw @s '''+T+'''{text:"나루카미 단독 전투를 시작합니다.",color:"white",bold:false}]
tellraw @s '''+HELP)
write('test/armored','''
# /function rlk:boss/raiden/test/armored: fresh test fight, transformed straight away.
function rlk:boss/raiden/test/start
execute unless score #rdTest rd matches 1 run return 0
execute as @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] at @s run function rlk:boss/raiden/transform_start
tellraw @s '''+T+'{text:"바로 악요의 요고우 텐마(갑주 단계)로 변신합니다.",color:"white",bold:false}]')
write('test/pattern','''
# /function rlk:boss/raiden/test/pattern {id:N}: N = 1~7 (normal) or 11~18 (armored), once.
$scoreboard players set #rdReq rd $(id)
execute store result score #rdOk rd run function rlk:boss/raiden/test/request
execute if score #rdOk rd matches 1 run scoreboard players operation #rdForce rd = #rdReq rd
execute if score #rdOk rd matches 1 run tellraw @s '''+T+'''{text:"다음 패턴: ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false}]''')
write('test/lock','''
# /function rlk:boss/raiden/test/lock {id:N}: repeat pattern N whenever its phase allows; {id:0} unlocks.
$scoreboard players set #rdReq rd $(id)
execute if score #rdReq rd matches 0 run scoreboard players set #rdLock rd 0
execute if score #rdReq rd matches 0 run scoreboard players set #rdForce rd 0
execute if score #rdReq rd matches 0 run return run tellraw @s '''+T+'''{text:"패턴 고정을 해제했습니다.",color:"gray",bold:false}]
execute store result score #rdOk rd run function rlk:boss/raiden/test/request
execute if score #rdOk rd matches 1 run scoreboard players operation #rdLock rd = #rdReq rd
execute if score #rdOk rd matches 1 run tellraw @s '''+T+'''{text:"패턴 고정: ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false},{text:" (해제: lock {id:0})",color:"gray",bold:false}]''')
write('test/request','''
# #rdReq = requested id. Starts a test if needed, aborts the current attack and switches
# phase so the request can run next. Returns 1 when accepted.
scoreboard players set #rdOk rd 0
execute if score #rdReq rd matches 1..7 run scoreboard players set #rdOk rd 1
execute if score #rdReq rd matches 11..18 run scoreboard players set #rdOk rd 1
execute if score #rdOk rd matches 0 run tellraw @s '''+T+'''{text:"패턴 번호는 1~7(일반) 또는 11~18(갑주)입니다.",color:"red",bold:false}]
execute if score #rdOk rd matches 0 run return 0
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run function rlk:boss/raiden/test/start
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/test/apply
return 1
''')
write('test/apply','''
# @s = boss. Abort the running attack (same reset as a pause), then enter the right phase.
execute unless score @s rdPat matches 0 run function rlk:boss/raiden/pause
execute if score #rdReq rd matches 11..18 if score @s rdPhase matches 0 run function rlk:boss/raiden/transform_start
execute if score #rdReq rd matches 11..18 if score @s rdPhase matches 3 run function rlk:boss/raiden/transform_start
execute if score #rdReq rd matches 1..7 if score @s rdPhase matches 1.. run function rlk:boss/raiden/test/to_normal
scoreboard players set @s rdWalk 0
execute unless score @s rdPhase matches 1 run scoreboard players set @s rdCool 2
''')
write('test/to_normal','''
# @s = boss in phase 1/2/3: drop the armor state without the exhausted break.
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/hazard/vfx_world
function rlk:boss/raiden/normal_return
''')
write('test/level','''
# /function rlk:boss/raiden/test/level {lv:N}: set the boss level and refill its scaled HP.
$scoreboard players set #rdReq rd $(lv)
execute unless score #rdReq rd matches 1..999 run return run tellraw @s '''+T+'''{text:"레벨은 1 이상이어야 합니다.",color:"red",bold:false}]
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run function rlk:boss/raiden/test/start
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] run scoreboard players operation @s mlv = #rdReq rd
execute as @e[tag=rlk_raiden,limit=1] run function rlk:mob/level_apply
tellraw @s '''+T+'''{text:"보스 레벨 ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false},{text:" · 체력을 다시 채웠습니다.",color:"gray",bold:false}]''')
write('test/stop','''
# /function rlk:boss/raiden/test/stop: remove the fight (bars included) and return to the lobby.
execute unless score #rdTest rd matches 1 run return run tellraw @s '''+T+'''{text:"진행 중인 보스 테스트가 없습니다.",color:"gray",bold:false}]
function rlk:boss/raiden/test/end
tellraw @a[tag=player] '''+T+'''{text:"보스 테스트를 끝내고 로비로 돌아왔습니다.",color:"gray",bold:false}]''')
write('test/end','''
# Shared teardown: run flags off, room cleared (bars hidden by boss cleanup), lobby spawn.
scoreboard players set #rdTest rd 0
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
function rlk:run/end
function rlk:boss/raiden/cleanup
execute as @a[tag=player] run function rlk:lobby/go
''')
write('test/defeat','''
# From player/hook_respawn (@s = respawned player): a lost test never fails/resets the run.
function rlk:boss/raiden/test/end
title @s times 10 40 15
title @s subtitle {text:"로비로 돌아왔습니다",color:"gray"}
title @s title {text:"보스 테스트 실패",color:"#E06A5A",bold:true}
scoreboard players set @s vBig 65
scoreboard players set @s ttlT 65
tellraw @s '''+T+'{text:"쓰러졌습니다. 다시 도전: ",color:"gray",bold:false},'+cmd_link(TEST+'start')+']')
write('test/won','''
# From room/combat_clear (boss zone cleared) during a test: no next-chapter object.
tellraw @a[tag=player] '''+T+'{text:"나루카미 처치! ",color:"green",bold:false},'+cmd_link(TEST+'start','[다시 하기]')+',{text:" ",bold:false},'+cmd_link(TEST+'stop','[로비로]')+']')
print('Generated Narukami encounter controllers, 13 attack timelines + illusion hook, and boss test commands.')
