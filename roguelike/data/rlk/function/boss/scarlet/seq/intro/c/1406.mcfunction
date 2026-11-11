# intro: the camera at #sq 1406 (@s = the body).
scoreboard players set #mbCamId mb 1
function rlk:mboss/cam/text
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^-0.3 ^2.9 ^0 facing ^0 ^1.5 ^6.5
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
