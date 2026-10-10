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
