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
# Transformation: scatter to the centre, then the transformation burst/clip.
TRANSFORM_FX = 6
TRANSFORM_LEN = 56

objectives = ['rd','rdPhase','rdPat','rdTime','rdAnim','rdRage','rdShield','rdCycle','rdCool','rdPrev','rdTurns','rdHitCD','rdObjKind','rdObjId','rdObjHP','rdReal','rdOAge','rdPTime','rdShape','rdWind','rdHAge','rdHLife','rdDamage','rdHHit','rdFX','rdFZ','rdHId','rdVId','rdUltUsed','rdWalk','rdWalkDir','rdBlink','rdCam','rdDeath','rdDeathTime','rdHidden']
write('init',[f'scoreboard objectives add {v} dummy' for v in objectives]+[
    'bossbar add rlk:narukami {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple"}',
    'bossbar add rlk:narukami_state {text:"악연의 에너지",color:"light_purple"}',
    'bossbar set rlk:narukami color purple','bossbar set rlk:narukami_state color yellow',
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
execute unless score #rdCap rd matches 1 run return 0
function rlk:boss/raiden/caption/expire
title @a[tag=player] subtitle ""
scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0
scoreboard players set @a[tag=player,scores={vBig=1..}] vBig 0
''')
write('caption/pattern_end','''
execute if score #rdCapPat rd matches 1 run function rlk:boss/raiden/caption/clear
''')
write('pause','''
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @e[tag=rlk_raiden] rdBlink 0
scoreboard players set @e[tag=rlk_raiden] rdWalk 0
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
execute if score @s rdPhase matches 0 if score @s rdRage matches {RAGE_MAX}.. run function rlk:boss/raiden/transform_start
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/transform_tick
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/armor_tick
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/exhausted_tick
execute if score @s rdPhase matches 0 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPhase matches 2 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
# Timelines start on the tick after choose: rdTime 1 is every pattern's first frame.
execute if score @s rdPat matches 1..6 if score @s rdTime matches 1.. run function rlk:boss/raiden/normal_dispatch
execute if score @s rdPat matches 11..18 if score @s rdTime matches 1.. run function rlk:boss/raiden/armor_dispatch
execute if score @s rdPat matches 99 if score @s rdTime matches 60.. run function rlk:boss/raiden/finish
# Keep the body on the disc without snapping: slide back toward the centre, and only
# scatter-blink home if it is somehow far outside. Tracking uses the avatar, never the camera.
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..21] at @s facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..26] unless score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_to
execute if score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_tick
# Hide the physical rig while illusions, scattering, or the aerial-arm ultimate are active.
scoreboard players set #rdHide rd 0
execute if score @s rdBlink matches 1.. run scoreboard players set #rdHide rd 1
execute if score @s rdPat matches 5 if score @s rdTime matches 1.. run scoreboard players set #rdHide rd 1
execute if score @s rdPat matches 15 if score @s rdTime matches 1.. run scoreboard players set #rdHide rd 1
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
write('choose','''
execute if score @s rdPhase matches 0 store result score @s rdPat run random value 1..6
execute if score @s rdPhase matches 2 store result score @s rdPat run random value 11..18
execute if score @s rdPat = @s rdPrev run scoreboard players add @s rdPat 1
execute if score @s rdPhase matches 0 if score @s rdPat matches 7 run scoreboard players set @s rdPat 1
execute if score @s rdPhase matches 2 if score @s rdPat matches 19 run scoreboard players set @s rdPat 11
scoreboard players add @s rdTurns 1
scoreboard players operation #rdTurn rd = @s rdTurns
scoreboard players operation #rdTurn rd %= #rd4 rd
# At most one ultimate in each transformation, guaranteed by the fourth move.
execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 1 if score @s rdPat matches 15 run scoreboard players set @s rdPat 18
execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 0 if score #rdTurn rd matches 0 run scoreboard players set @s rdPat 15
# Boss test hooks (test/lock repeats, test/pattern once) only apply to the current phase.
execute if score @s rdPhase matches 0 if score #rdLock rd matches 1..6 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 2 if score #rdLock rd matches 11..18 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 0 if score #rdForce rd matches 1..6 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPhase matches 2 if score #rdForce rd matches 11..18 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPat = #rdForce rd run scoreboard players set #rdForce rd 0
scoreboard players operation @s rdPrev = @s rdPat
scoreboard players set @s rdTime 0
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
''')
write('finish','''
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/caption/pattern_end
function rlk:boss/raiden/judgment_rig/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
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
# Scatter to the arena centre (depart here, reform there) instead of snapping to it;
# an unfinished blink is redirected there. Relocation lands by rdTime 4 at the latest.
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set #rdGo rd 0
execute if score @s rdBlink matches 1.. run scoreboard players set #rdGo rd 1
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..1.5] run scoreboard players set #rdGo rd 1
execute if score #rdGo rd matches 1 at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/movement/blink_to
scoreboard players set @s rdAnim 9
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
title @a[tag=player] times 8 55 16
title @a[tag=player] subtitle {text:"번개 갑주를 파괴하면 잠시 무력화됩니다",color:"white"}
title @a[tag=player] title {text:"악요의 요구우 텐마",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 79
scoreboard players set @a[tag=player] ttlT 79
scoreboard players set #rdCap rd 1
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.4
''')
# The blink relocates by rdTime 3-4 and the rig reforms on 7-8, so the burst and its
# danger circle start at the centre on TRANSFORM_FX; the transform clip (46) ends ~54.
write('transform_tick',[caption('악요의 요구우 텐마 · 변신'),
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
bossbar set rlk:narukami_state color blue
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
bossbar set rlk:narukami_state color green
title @a[tag=player] times 5 45 15
title @a[tag=player] subtitle {text:"갑주 파괴 · 지금 공격하세요!",color:"green",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 65
scoreboard players set #rdCap rd 1
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3
execute at @s run function rlk:boss/raiden/vfx/armor_break
''')
write('exhausted_tick',[at('46',anim(22)),at('132',anim(24)),at('160',call('normal_return'))])
write('normal_return','''
attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 0
scoreboard players set @s rdRage 0
bossbar set rlk:narukami_state color yellow
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 20
''')
write('bars',f'''
execute if score #rdCap rd matches 1 unless entity @a[tag=player,scores={{ttlT=1..}}] run function rlk:boss/raiden/caption/expire
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
execute store result bossbar rlk:narukami max run scoreboard players get @s mhpM
execute store result bossbar rlk:narukami value run scoreboard players get @s mhpC
execute if score @s rdPhase matches 0 run bossbar set rlk:narukami_state max {RAGE_MAX}
execute if score @s rdPhase matches 0 store result bossbar rlk:narukami_state value run scoreboard players get @s rdRage
execute if score @s rdPhase matches 0..1 run bossbar set rlk:narukami_state name {{text:"악연의 에너지",color:"light_purple"}}
execute if score @s rdPhase matches 1 run bossbar set rlk:narukami_state max {TRANSFORM_LEN}
execute if score @s rdPhase matches 1 store result bossbar rlk:narukami_state value run scoreboard players get @s rdTime
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami_state max {SHIELD_MAX}
execute if score @s rdPhase matches 2 store result bossbar rlk:narukami_state value run scoreboard players get @s rdShield
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami_state name {{text:"번개 갑주",color:"aqua"}}
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami_state name {{text:"갑주 파괴",color:"green"}}
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami_state max 160
execute if score @s rdPhase matches 3 store result bossbar rlk:narukami_state value run scoreboard players get @s rdTime
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
function rlk:cm/hit_pl
''')

write('normal_dispatch',[f'execute if score @s rdPat matches {i} run '+call('patterns/'+str(i)) for i in range(1,7)])
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
# Short tells (12-19 ticks), then 6-8 ticks of recovery before the next wind-up.
# Every wind clip (slash/thrust 6, cast 10, sweep/clap/slam 8, judgment 14) still
# reaches its hold pose before the strike clip starts 3-4 ticks ahead of contact.

p=pattern(1,'태도 연격 · 옆이나 뒤로 회피')
for t,n in [(1,3),(19,4),(37,3)]:
    event(p,t,face,flat,anim(2),haz(1,12,9))
    event(p,t+12,anim(n),sound('entity.player.attack.sweep',1,.7))
event(p,55,anim(20),haz(8,13,14));event(p,68,anim(4));end(p,76)
p=pattern(2,'나기나타 · 전방 찌르기와 검파')
for t in [1,20,39]:
    event(p,t,face,flat,anim(5),haz(2,13,10));event(p,t+13,anim(6),sound('item.trident.throw',1,.72))
event(p,58,anim(7),haz(9,14,13));event(p,72,anim(8));end(p,80)
p=pattern(3,'뇌명 · 순간이동 후 발도')
# Each scatter blink keeps the rig hidden for 8 ticks (reforms on blink start + 8).
event(p,1,anim(21),sound('entity.breeze.charge',.8,.7),call('movement/blink_start'))
event(p,10,face,flat,anim(2),haz(2,12,16));event(p,22,anim(6),sound('entity.player.attack.sweep',1.1,.65))
event(p,28,call('movement/blink_start'));event(p,37,face,flat,anim(2),haz(1,13,15));event(p,50,anim(4));end(p,58)
p=pattern(4,'마가츠의 뇌안 · 하나를 파괴하고 빈 원으로 이동')
event(p,1,anim(7),call('eyes_start'))
event(p,16,anim(8));event(p,46,call('eyes_arm'));event(p,73,anim(18));end(p,84)
# Pattern 5 (분신 · 진짜 찾기) belongs to build_raiden_illusions.py; it ends itself.
patterns[5]=[call('illusion/tick')]
p=pattern(6,'낙뢰 · 표시된 자리에서 벗어나세요')
for t in [1,20,39,58]:
    event(p,t,anim(7),target+haz(3,14,12));event(p,t+14,anim(8),sound('entity.lightning_bolt.impact',.7,.8))
end(p,80)
p=pattern(11,'거대 팔 연격 · 검의 궤적과 투척 낙뢰에 주의')
for t in [1,25]:
    event(p,t,face,flat,anim(10),haz(4,17,19));event(p,t+17,anim(11),sound('entity.player.attack.sweep',1.2,.62))
event(p,49,anim(7),target+haz(3,16,22));event(p,65,anim(8));end(p,73)
p=pattern(12,'인공팔 협격 · 양손 사이에서 벗어나세요')
event(p,1,face,flat,anim(12),haz(7,18,25));event(p,19,anim(13),sound('entity.iron_golem.attack',1,.65));end(p,28)
p=pattern(13,'인공팔 내려찍기 · 원 밖으로 회피')
# Contract with build_raiden_rig.mjs: the floating hand lands at hazard age 18; the
# finish 12 ticks after the second landing leaves its lift-and-fade on screen.
for t in [1,26]:
    event(p,t,anim(14),target+haz(6,18,24),target+call('rig/target_slam_spawn'));event(p,t+18,anim(15),sound('entity.generic.explode',.65,.72))
end(p,56)
p=pattern(14,'천수의 속박 · 퍼지는 번개 고리를 점프로 회피')
event(p,1,anim(7),call('stakes_start'));event(p,15,anim(8))
for t,i in [(20,1),(54,2),(88,3)]:event(p,t,call('stakes_pulse_'+str(i)))
event(p,128,call('stakes_pulse'))
# Each ring keeps its full 32-tick travel; the final pulse ends before this finish.
end(p,178)
p=pattern(15,'최종 재앙 · 추억의 꽃을 공격한 뒤 보호막 안으로!')
event(p,1,call('judgment_start'),anim(16));event(p,30,sound('block.beacon.ambient',.6,.5));event(p,70,sound('block.portal.ambient',.45,.55))
# The flower retains the full six-second response window despite quicker recovery.
# The hidden body already waits at centre-8; it reforms there facing the player.
event(p,120,call('judgment_strike'));event(p,170,face,flat,call('movement/arrive'));end(p,176)
p=pattern(16,'거검 내려베기 · 길게 표시된 직선에서 벗어나세요')
event(p,1,face,flat,anim(16),haz(5,19,30));event(p,20,anim(17),sound('entity.lightning_bolt.thunder',.8,.68));end(p,32)
p=pattern(17,'검파 연사 · 다섯 갈래 뒤 넓은 가로 검파')
event(p,1,face,flat,anim(7),haz(9,16,17));event(p,17,anim(8),sound('entity.breeze.shoot',.8,.72))
event(p,23,face,flat,anim(10),haz(10,16,21));event(p,39,anim(11));end(p,47)
p=pattern(18,'발도 돌진 · 고정된 직선 경로를 피하세요')
event(p,1,face,flat,anim(2),haz(5,16,22));event(p,17,anim(21),sound('item.trident.riptide_3',.7,.8))
p.append('execute if score @s rdTime matches 17..28 at @s rotated as @s positioned ^ ^ ^0.75 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] run tp @s ~ ~ ~')
event(p,31,anim(10),haz(4,13,19));event(p,44,anim(11));end(p,52)
for i,p in patterns.items():write('patterns/'+str(i),p)
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
write('eyes_arm',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=1}] at @s run '+haz(12,26,34)])
write('stakes_start',[call('object/clear')]+[
    center+f'execute positioned ~{x} ~ ~{z} run '+obj(4,'lightning_stake',1,i,0)
    for i,(x,z) in enumerate([(-8,-4),(8,-4),(0,9)],1)])
write('stakes_pulse',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=4}] at @s run '+haz(11,12,14,49),sound('block.beacon.power_select',.55,.7)])
for i in [1,2,3]:
    write('stakes_pulse_'+str(i),[f'execute as @e[tag=rlk_rd_object,scores={{rdObjKind=4,rdObjId={i}}}] at @s run '+haz(11,12,14,49),sound('block.beacon.power_select',.55,.7)])
write('judgment_start',[call('object/clear'),'scoreboard players set @s rdUltUsed 1','scoreboard players set @s rdWalk 0',call('movement/depart'),center+call('judgment_rig/start'),
    '# The body is hidden from this frame (tick hides rdPat 15), so this move is never seen.',
    center+'execute positioned ~ ~ ~-8 run tp @s ~ ~ ~ 0 0',
    center+call('vfx/judgment_warning'),
    center+'execute positioned ~ ~ ~3 run '+obj(3,'remembrance_flower',4,1,.05),
    'title @a[tag=player] times 4 85 16',
    'title @a[tag=player] subtitle {text:"꽃을 공격 → 보호막 안으로! 번개 1타 / 다른 공격 4타",color:"aqua",bold:true}',
    'execute as @a[tag=player] run function rlk:view/ttl_blank',
    'scoreboard players set @a[tag=player] ttlT 105',
    'scoreboard players set #rdCap rd 1',
    'scoreboard players set #rdCapPat rd 1',
    sound('entity.wither.ambient',.7,.5)])
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
      +cmd_link(TEST+'pattern {id:11}','pattern {id:N}')+',{text:" 다음 패턴(1~6, 11~18) · ",color:"gray",bold:false},'
      +cmd_link(TEST+'lock {id:11}','lock {id:N}')+',{text:" 패턴 고정(0 해제) · ",color:"gray",bold:false},'
      +cmd_link(TEST+'level {lv:6}','level {lv:N}')+',{text:" 보스 레벨 · ",color:"gray",bold:false},'
      +cmd_link(TEST+'stop','stop')+',{text:" 종료 후 로비",color:"gray",bold:false}]')
write('test/start','''
# /function rlk:boss/raiden/test/start (@s = 'player'): fight only Narukami, normal phase.
# Uses the real boss room (room/raiden layout in the forceloaded dungeon area) and the
# run flags (#active room 1) so room tick, death and cleanup flows all behave as in a run.
# Re-running restarts the fight. Player death or test/stop returns to the lobby.
execute unless entity @s[tag=player] run return run tellraw @s {text:"[보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s '''+T+'{text:"던전 구역이 준비되지 않았습니다. 먼저 ",color:"gray",bold:false},'+cmd_link('/function rlk:room/setup')+''',{text:" 을 실행하세요.",color:"gray",bold:false}]
execute if score #active room matches 1 unless score #rdTest rd matches 1 run return run tellraw @s '''+T+'{text:"진행 중인 런이 있습니다. ",color:"gray",bold:false},'+cmd_link('/function rlk:run/stop')+''',{text:" 후 다시 실행하세요.",color:"gray",bold:false}]
execute if score @s dead matches 1 run return 0
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #rdTest rd 1
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
# Chapter-1 boss slot: level = (chapter-1)*6 + mapIdx + 1 = 6 (test/level changes it).
scoreboard players set #active room 1
scoreboard players set #chapter room 1
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
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/transform_start
tellraw @s '''+T+'{text:"바로 악요의 요구우 텐마(갑주 단계)로 변신합니다.",color:"white",bold:false}]')
write('test/pattern','''
# /function rlk:boss/raiden/test/pattern {id:N}: N = 1~6 (normal) or 11~18 (armored), once.
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
execute if score #rdReq rd matches 1..6 run scoreboard players set #rdOk rd 1
execute if score #rdReq rd matches 11..18 run scoreboard players set #rdOk rd 1
execute if score #rdOk rd matches 0 run tellraw @s '''+T+'''{text:"패턴 번호는 1~6(일반) 또는 11~18(갑주)입니다.",color:"red",bold:false}]
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
execute if score #rdReq rd matches 1..6 if score @s rdPhase matches 1.. run function rlk:boss/raiden/test/to_normal
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
