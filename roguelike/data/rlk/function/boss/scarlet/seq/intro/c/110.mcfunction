# intro: the camera at #sq 110 (@s = the body).
scoreboard players set #mbCamId mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^3 ^1.5 ^14
rotate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] facing 889.0 218 -34.0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
