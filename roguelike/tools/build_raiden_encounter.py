"""Narukami encounter controller. Original Minecraft adaptation, no recorded audio.

Generate controllers only; arena, hazards and articulated rig have separate builders.
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

objectives = ['rd','rdPhase','rdPat','rdTime','rdAnim','rdRage','rdShield','rdCycle','rdCool','rdPrev','rdTurns','rdHitCD','rdObjKind','rdObjId','rdObjHP','rdReal','rdOAge','rdPTime','rdShape','rdWind','rdHAge','rdHLife','rdDamage','rdHHit','rdFX','rdFZ','rdHId','rdVId','rdUltUsed','rdWalk','rdWalkDir','rdBlink','rdCam','rdDeath','rdDeathTime']
write('init',[f'scoreboard objectives add {v} dummy' for v in objectives]+[
    'bossbar add rlk:narukami {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple"}',
    'bossbar add rlk:narukami_state {text:"악연의 에너지",color:"light_purple"}',
    'bossbar set rlk:narukami color purple','bossbar set rlk:narukami_state color yellow',
    'bossbar set rlk:narukami visible false','bossbar set rlk:narukami_state visible false',
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
title @a[tag=player] times 8 60 16
title @a[tag=player] title {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple",bold:true}
title @a[tag=player] subtitle {text:"바닥의 보랏빛 예고를 보고 회피하세요",color:"white"}
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.7 0.62 0.3
''')
write('cleanup','''
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_raiden_aux]
bossbar set rlk:narukami visible false
bossbar set rlk:narukami_state visible false
''')
write('world','''
execute unless entity @e[tag=rlk_raiden,limit=1] run return run function rlk:boss/raiden/cleanup
execute as @e[tag=rlk_raiden,scores={rdDeath=1},limit=1] at @s run return run function rlk:boss/raiden/death/tick
execute unless entity @a[tag=player,limit=1] run return 0
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
write('pause','''
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/judgment_rig/cleanup
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
write('tick','''
# @s=real living boss; the invisible body owns damage, the displays own appearance.
execute if score @s rdDeath matches 1 run return run function rlk:boss/raiden/death/tick
data merge entity @s {Motion:[0d,0d,0d],Fire:-1s}
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
execute if score @s rdCool matches 1.. run scoreboard players remove @s rdCool 1
scoreboard players add @s rdTime 1
execute if score @s rdPhase matches 0 run scoreboard players add @s rdRage 1
execute if score @s rdPhase matches 0 if score @s rdRage matches 600.. run function rlk:boss/raiden/transform_start
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/transform_tick
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/armor_tick
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/exhausted_tick
execute if score @s rdPhase matches 0 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPhase matches 2 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPat matches 1..6 run function rlk:boss/raiden/normal_dispatch
execute if score @s rdPat matches 11..18 run function rlk:boss/raiden/armor_dispatch
execute if score @s rdPat matches 99 if score @s rdTime matches 60.. run function rlk:boss/raiden/finish
# Keep the body on the disc; all tracking uses the avatar, never the remote camera.
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..21] run tp @s ~ ~ ~
execute if score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_tick
execute unless score @s rdPat matches 5 unless score @s rdPat matches 15 unless score @s rdBlink matches 1.. at @s run function rlk:boss/raiden/rig/tick
# Hide the physical rig while illusions, scattering, or the aerial-arm ultimate are active.
execute if score @s rdPat matches 5 run tp @e[tag=rlk_raiden_part] ~ ~-60 ~
execute if score @s rdPat matches 15 run tp @e[tag=rlk_raiden_part] ~ ~-60 ~
execute if score @s rdBlink matches 1.. run tp @e[tag=rlk_raiden_part] ~ ~-60 ~
execute if score @s rdPat matches 15 run function rlk:boss/raiden/judgment_rig/tick
execute if score @s rdPat matches 15 if score @s rdTime matches 80..173 run function rlk:boss/raiden/camera/try_start
execute if score @s rdPat matches 15 if score @s rdTime matches 174 run function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/bars
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
execute rotated as @s positioned ^ ^ ^0.17 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ minecraft:air run tp @s ~ ~ ~
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
scoreboard players operation @s rdPrev = @s rdPat
scoreboard players set @s rdTime 0
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
''')
write('finish','''
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/judgment_rig/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players operation #rdWalkTurn rd = @s rdTurns
scoreboard players set #rd2 rd 2
scoreboard players operation #rdWalkTurn rd %= #rd2 rd
execute if score #rdWalkTurn rd matches 0 run function rlk:boss/raiden/movement/walk_start
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 0
scoreboard players set @s rdCool 12
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
''')
write('transform_start','''
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/judgment_rig/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
scoreboard players set @s rdPhase 1
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 9
scoreboard players add @s rdCycle 1
execute at @e[tag=rlk_raiden_arena,limit=1] run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
title @a[tag=player] times 8 55 16
execute at @s run function rlk:boss/raiden/vfx/transform
title @a[tag=player] title {text:"악요의 요구우 텐마",color:"light_purple",bold:true}
title @a[tag=player] subtitle {text:"번개 갑주를 파괴하면 잠시 무력화됩니다",color:"white"}
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.4
''')
write('transform_tick',[caption('악요의 요구우 텐마 · 변신'),
    at('1',haz(8,30,18,42)),at('15',sound('entity.lightning_bolt.thunder',.6,.7)),
    at('52',call('armor_start'))])
write('armor_start','''
attribute @s minecraft:scale base set 2.2
scoreboard players set @s rdPhase 2
scoreboard players set @s rdShield 300
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdPTime 0
scoreboard players set @s rdTurns 0
scoreboard players set @s rdHitCD 0
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 18
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
scoreboard players set @s rdCool 28
''')
write('bars','''
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
execute store result bossbar rlk:narukami max run scoreboard players get @s mhpM
execute store result bossbar rlk:narukami value run scoreboard players get @s mhpC
execute if score @s rdPhase matches 0 run bossbar set rlk:narukami_state max 600
execute if score @s rdPhase matches 0 store result bossbar rlk:narukami_state value run scoreboard players get @s rdRage
execute if score @s rdPhase matches 0..1 run bossbar set rlk:narukami_state name {text:"악연의 에너지",color:"light_purple"}
execute if score @s rdPhase matches 1 run bossbar set rlk:narukami_state max 52
execute if score @s rdPhase matches 1 store result bossbar rlk:narukami_state value run scoreboard players get @s rdTime
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami_state max 300
execute if score @s rdPhase matches 2 store result bossbar rlk:narukami_state value run scoreboard players get @s rdShield
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami_state name {text:"번개 갑주",color:"aqua"}
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami_state name {text:"갑주 파괴",color:"green"}
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
write('threshold','''
scoreboard players operation #dmg tmp = @s mhpC
scoreboard players operation #dmg tmp -= #rdFloor rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 0
scoreboard players set @s rdRage 600
''')
write('shield_hit','''
# Armor absorbs 80% body damage. Every character can break it; other elements work faster.
execute if score #dmg tmp matches ..0 run return 0
execute if score @s rdHitCD matches ..0 if score #dmg tmp matches 1.. run function rlk:boss/raiden/shield_drain
scoreboard players set #rdDiv rd 5
scoreboard players operation #dmg tmp /= #rdDiv rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
''')
write('shield_drain','''
scoreboard players set #rdDrain rd 2
execute if score #elem tmp matches 3 run scoreboard players set #rdDrain rd 1
execute if score #elem tmp matches 1 run scoreboard players set #rdDrain rd 6
execute if score #elem tmp matches 4 run scoreboard players set #rdDrain rd 6
execute if score #elem tmp matches 7 run scoreboard players set #rdDrain rd 4
execute if score #elem tmp matches 2 run scoreboard players set #rdDrain rd 3
execute if score #elem tmp matches 5..6 run scoreboard players set #rdDrain rd 3
execute if score #tfm tmp matches 1 run scoreboard players set #rdDrain rd 1
scoreboard players operation @s rdShield -= #rdDrain rd
scoreboard players set @s rdHitCD 4
''')
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

p=pattern(1,'태도 연격 · 옆이나 뒤로 회피')
for t,n in [(1,3),(25,4),(49,3)]:
    event(p,t,face,flat,anim(2),haz(1,18,9))
    event(p,t+18,anim(n),sound('entity.player.attack.sweep',1,.7))
event(p,74,anim(20),haz(8,20,14));event(p,94,anim(4));end(p,104)
p=pattern(2,'나기나타 · 전방 찌르기와 검파')
for t in [1,27,53]:
    event(p,t,face,flat,anim(5),haz(2,20,10));event(p,t+20,anim(6),sound('item.trident.throw',1,.72))
event(p,80,anim(7),haz(9,22,13));event(p,102,anim(8));end(p,112)
p=pattern(3,'뇌명 · 순간이동 후 발도')
event(p,1,anim(21),sound('entity.breeze.charge',.8,.7),call('movement/blink_start'))
event(p,12,face,flat,anim(2),haz(2,18,16));event(p,30,anim(6),sound('entity.player.attack.sweep',1.1,.65))
event(p,39,call('movement/blink_start'));event(p,50,face,flat,anim(2),haz(1,20,15));event(p,70,anim(4));end(p,80)
p=pattern(4,'마가츠의 뇌안 · 하나를 파괴하고 빈 원으로 이동')
event(p,1,anim(7),call('eyes_start'))
event(p,16,anim(8));event(p,60,call('eyes_arm'));event(p,96,anim(18));end(p,108)
p=pattern(5,'분신 · X자 검격을 내는 진짜를 공격')
event(p,1,call('illusions_start'),anim(7));event(p,18,call('illusions_cue'));event(p,55,call('illusions_cue'))
event(p,102,call('illusions_fail'));end(p,134)
p=pattern(6,'낙뢰 · 표시된 자리에서 벗어나세요')
for t in [1,26,51,76]:
    event(p,t,anim(7),target+haz(3,20,12));event(p,t+20,anim(8),sound('entity.lightning_bolt.impact',.7,.8))
end(p,106)
p=pattern(11,'거대 팔 연격 · 검의 궤적과 투척 낙뢰에 주의')
for t in [1,37]:
    event(p,t,face,flat,anim(10),haz(4,26,19));event(p,t+26,anim(11),sound('entity.player.attack.sweep',1.2,.62))
event(p,74,anim(7),target+haz(3,24,22));event(p,98,anim(8));end(p,110)
p=pattern(12,'인공팔 협격 · 양손 사이에서 벗어나세요')
event(p,1,face,flat,anim(12),haz(7,28,25));event(p,29,anim(13),sound('entity.iron_golem.attack',1,.65));end(p,40)
p=pattern(13,'인공팔 내려찍기 · 원 밖으로 회피')
for t in [1,43]:
    event(p,t,anim(14),target+haz(6,28,24),target+call('rig/target_slam_spawn'));event(p,t+28,anim(15),sound('entity.generic.explode',.65,.72))
end(p,83)
p=pattern(14,'천수의 속박 · 퍼지는 번개 고리를 점프로 회피')
event(p,1,anim(7),call('stakes_start'));event(p,15,anim(8))
for t,i in [(20,1),(54,2),(88,3)]:event(p,t,call('stakes_pulse_'+str(i)))
event(p,128,call('stakes_pulse'))
# Each ring keeps its full 32-tick travel; the final pulse ends before this finish.
end(p,178)
p=pattern(15,'최종 재앙 · 추억의 꽃을 공격한 뒤 보호막 안으로!')
event(p,1,call('judgment_start'),anim(16));event(p,30,sound('block.beacon.ambient',.6,.5));event(p,70,sound('block.portal.ambient',.45,.55))
# The flower retains the full six-second response window despite quicker recovery.
event(p,120,call('judgment_strike'));event(p,170,call('movement/arrive'));end(p,176)
p=pattern(16,'거검 내려베기 · 길게 표시된 직선에서 벗어나세요')
event(p,1,face,flat,anim(16),haz(5,28,30));event(p,29,anim(17),sound('entity.lightning_bolt.thunder',.8,.68));end(p,41)
p=pattern(17,'검파 연사 · 다섯 갈래 뒤 넓은 가로 검파')
event(p,1,face,flat,anim(7),haz(9,24,17));event(p,25,anim(8),sound('entity.breeze.shoot',.8,.72))
event(p,40,face,flat,anim(10),haz(10,24,21));event(p,64,anim(11));end(p,76)
p=pattern(18,'발도 돌진 · 고정된 직선 경로를 피하세요')
event(p,1,face,flat,anim(2),haz(5,24,22));event(p,25,anim(21),sound('item.trident.riptide_3',.7,.8))
p.append('execute if score @s rdTime matches 25..36 at @s rotated as @s positioned ^ ^ ^0.75 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~')
event(p,39,anim(10),haz(4,20,19));event(p,59,anim(11));end(p,71)
for i,p in patterns.items():write('patterns/'+str(i),p)
write('blink_relocate','''
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] positioned ^ ^ ^5 positioned ~ 201 ~ run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] run tp @s ~ ~ ~
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
execute if score @s rdObjKind matches 2 if score @s rdReal matches 1 as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/illusion_win
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
write('eyes_arm',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=1}] at @s run '+haz(12,35,34)])
write('illusions_start',[call('object/clear'),'execute store result score #rdReal rd run random value 1..4']+[
    center+f'execute positioned ~{x} ~ ~{z} run '+obj(2,'illusion',1,i,1)
    for i,(x,z) in enumerate([(-8,-8),(8,-8),(-8,8),(8,8)],1)]+[
    'execute as @e[tag=rlk_rd_object,scores={rdObjKind=2}] if score @s rdObjId = #rdReal rd run scoreboard players set @s rdReal 1'])
write('illusions_cue','''
execute as @e[tag=rlk_rd_object,scores={rdObjKind=2}] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute as @e[tag=rlk_rd_object,scores={rdObjKind=2}] at @s rotated as @s run function rlk:boss/raiden/illusion_cue
''')
write('illusion_cue',[call('object_vfx/illusion_cue'),haz(2,24,8)])
write('illusion_win','''
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
scoreboard players set @s rdPat 99
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 18
scoreboard players remove @s rdRage 120
execute if score @s rdRage matches ..0 run scoreboard players set @s rdRage 0
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ .8 .65 .3
''')
write('illusions_fail',[call('object/clear'),anim(8),target+haz(6,24,26),caption('분신 간파 실패 · 낙뢰 범위에서 벗어나세요')])
write('stakes_start',[call('object/clear')]+[
    center+f'execute positioned ~{x} ~ ~{z} run '+obj(4,'lightning_stake',1,i,0)
    for i,(x,z) in enumerate([(-8,-4),(8,-4),(0,9)],1)])
write('stakes_pulse',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=4}] at @s run '+haz(11,12,14,49),sound('block.beacon.power_select',.55,.7)])
for i in [1,2,3]:
    write('stakes_pulse_'+str(i),[f'execute as @e[tag=rlk_rd_object,scores={{rdObjKind=4,rdObjId={i}}}] at @s run '+haz(11,12,14,49),sound('block.beacon.power_select',.55,.7)])
write('judgment_start',[call('object/clear'),'scoreboard players set @s rdUltUsed 1','scoreboard players set @s rdWalk 0',call('movement/depart'),center+call('judgment_rig/start'),
    center+'execute positioned ~ ~ ~-8 run tp @s ~ ~ ~ 0 0',
    center+call('vfx/judgment_warning'),
    center+'execute positioned ~ ~ ~3 run '+obj(3,'remembrance_flower',4,1,.05),
    'title @a[tag=player] times 4 85 16',
    'title @a[tag=player] subtitle {text:"꽃을 공격 → 보호막 안으로! 번개 1타 / 다른 공격 4타",color:"aqua",bold:true}',
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
write('judgment_strike','''
scoreboard players set #rdSafe rd 0
execute as @e[tag=rlk_rd_dome,limit=1] at @s run function rlk:boss/raiden/dome_contains
execute if score #rdSafe rd matches 0 as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:boss/raiden/judgment_fatal
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/vfx/judgment_strike
execute if score #rdSafe rd matches 1 run scoreboard players remove @s rdShield 65
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
print('Generated Narukami encounter controllers and 14 attack timelines.')
