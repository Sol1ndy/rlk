"""Camera lifecycle and delayed collapse/death for the Narukami encounter."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/rlk/function/boss/raiden'
def write(name,content):
    p=BASE/(name+'.mcfunction');p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content.strip()+'\n',encoding='utf-8')

write('camera/try_start','''
# Only lock the camera after the player has actually reached the safe dome.
execute if entity @a[tag=player,scores={rdCam=1},limit=1] run return 0
execute unless entity @e[tag=rlk_rd_dome,limit=1] run return 0
scoreboard players set #rdSafe rd 0
execute as @e[tag=rlk_rd_dome,limit=1] at @s run function rlk:boss/raiden/dome_contains
execute if score #rdSafe rd matches 1 as @a[tag=player,limit=1] at @s run function rlk:boss/raiden/camera/start
''')
write('camera/start','''
execute if score @s rdCam matches 1 run return 0
execute if score @s dead matches 1 run return 0
execute if score @s rnDie matches 1.. run return 0
execute if score @s pkMode matches 1.. run return 0
data modify storage rlk:rdcam rotation set from entity @s Rotation
execute store result storage rlk:rdcam yaw float 0.01 run data get entity @s Rotation[0] 100
execute store result storage rlk:rdcam pitch float 0.01 run data get entity @s Rotation[1] 100
scoreboard players operation #rdCamPrevOn rd = #on view
scoreboard players operation #rdCamPrevMode rd = #vmode view
scoreboard players set #rdCamHadAv rd 0
execute if entity @e[tag=rlk_av,limit=1] run scoreboard players set #rdCamHadAv rd 1
kill @e[tag=rlk_rd_cam_anchor]
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_cam_anchor"]}
execute rotated as @e[tag=rlk_body,limit=1] as @e[tag=rlk_rd_cam_anchor] run rotate @s ~ ~
function rlk:view/ride_off
execute unless entity @e[tag=rlk_av,limit=1] at @e[tag=rlk_rd_cam_anchor,limit=1] run function rlk:view/spawn
tag @s remove rlk_body
scoreboard players set #on view 1
scoreboard players set #vmode view 1
scoreboard players set @s rdCam 1
execute if score @s skDash matches 1.. run function rlk:char/skirk/dash_end
function rlk:char/motion/release
execute if score @s buT matches 1.. run function rlk:char/burst_wind_end
execute if score @s bowT matches 1.. run function rlk:char/bow/cancel
scoreboard players set @s naQ 0
scoreboard players set @s fxT 0
scoreboard players set @s dashMoveT 0
scoreboard players set @s stepT 0
kill @e[tag=rlk_plkb]
data merge entity @e[tag=rlk_camv,limit=1] {teleport_duration:0}
function rlk:boss/raiden/camera/hold
''')
write('camera/hold','''
# Separate cinematic camera; never use the camera position for boss target/damage.
execute unless entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=80..173},limit=1] run return run function rlk:boss/raiden/camera/end
execute unless entity @e[tag=rlk_rd_cam_anchor,limit=1] run return run function rlk:boss/raiden/camera/end
execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:boss/raiden/camera/end
execute if score @s dead matches 1 run return run function rlk:boss/raiden/camera/end
execute if score @s rnDie matches 1.. run return run function rlk:boss/raiden/camera/end
execute if score @s pkMode matches 1.. run return run function rlk:boss/raiden/camera/end
scoreboard players set @s dashMoveT 0
scoreboard players set @s stepT 0
scoreboard players set @s rcU 0
scoreboard players set @s rcT 0
scoreboard players set @s pmAtkPending 0
kill @e[tag=rlk_plkb]
execute at @e[tag=rlk_rd_cam_anchor,limit=1] rotated as @e[tag=rlk_rd_cam_anchor,limit=1] run tp @e[tag=rlk_av,limit=1] ~ ~ ~ ~ ~
data merge entity @e[tag=rlk_av,limit=1] {Motion:[0d,0d,0d]}
# Eye at (0,204,13), aimed above the orb toward the rift and sword.
tp @e[tag=rlk_camv,limit=1] 0 202.98 13 180 -10
rotate @s 180 -10
execute if predicate rlk:in_sneak run tp @s 0 202.73 13 180 -10
execute unless predicate rlk:in_sneak run ride @s mount @e[tag=rlk_camv,limit=1]
function rlk:view/hand_wrap
''')
write('camera/end','''
execute unless score @s rdCam matches 1 run return 0
scoreboard players set @s rdCam 0
function rlk:view/ride_off
scoreboard players operation #on view = #rdCamPrevOn rd
scoreboard players operation #vmode view = #rdCamPrevMode rd
execute if score #rdCamHadAv rd matches 0 run function rlk:view/teardown
execute if score #rdCamHadAv rd matches 1 run data merge entity @e[tag=rlk_camv,limit=1] {teleport_duration:1}
execute if data storage rlk:rdcam yaw run function rlk:boss/raiden/camera/restore_rotation with storage rlk:rdcam
execute store result score @s vYaw run data get entity @s Rotation[0] 100
execute store result score @s vPitch run data get entity @s Rotation[1] 100
scoreboard players set @s vDy 0
scoreboard players set @s vDp 0
scoreboard players set #bcStep view 0
scoreboard players set #durNow view -1
scoreboard players set @s uiCd 6
scoreboard players set @s rcU 0
scoreboard players set @s rcT 0
kill @e[tag=rlk_rd_cam_anchor]
data remove storage rlk:rdcam rotation
data remove storage rlk:rdcam yaw
data remove storage rlk:rdcam pitch
''')
write('camera/restore_rotation','''
$rotate @s $(yaw) $(pitch)
''')
write('camera/release_all','''
execute as @a[scores={rdCam=1}] at @s run function rlk:boss/raiden/camera/end
kill @e[tag=rlk_rd_cam_anchor]
''')
write('death/start','''
# The first lethal hit already awarded loot. Keep the brain alive only for the visual.
execute if score @s rdDeath matches 1 run return 0
scoreboard players set @s rdDeath 1
scoreboard players set @s rdDeathTime 0
scoreboard players set @s mhpC 0
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 19
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/movement/cleanup
function rlk:boss/raiden/object/clear
function rlk:boss/raiden/object_vfx/clear
kill @e[tag=rlk_rd_hazard]
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_sfx]
kill @e[tag=rlk_rd_slam_hand]
function rlk:boss/raiden/hazard/vfx_world
execute on passengers run kill @s
bossbar set rlk:narukami value 0
bossbar set rlk:narukami_state visible false
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ .7 .7 .3
function rlk:boss/raiden/rig/tick
''')
write('death/tick','''
scoreboard players add @s rdDeathTime 1
data merge entity @s {Motion:[0d,0d,0d],Health:1024f,Fire:-1s}
execute if score @s rdDeathTime matches 48.. run return run function rlk:boss/raiden/death/finish
function rlk:boss/raiden/rig/tick
''')
write('death/finish','''
function rlk:boss/raiden/cleanup
kill @s
''')
print('Generated camera and collapse lifecycle functions.')
