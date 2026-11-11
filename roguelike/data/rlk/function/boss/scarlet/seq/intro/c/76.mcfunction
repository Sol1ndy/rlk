# intro: the camera at #sq 76 (@s = the body).
scoreboard players set #mbCamId mb 2
function rlk:mboss/cam/text
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^7 ^1.2 ^-0.2
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
