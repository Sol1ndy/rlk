# intro: the camera at #sq 24 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^-0.6 ^1.7 ^-4.5 facing ^0 ^1.4 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
