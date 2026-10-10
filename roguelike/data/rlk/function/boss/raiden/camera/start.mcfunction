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
