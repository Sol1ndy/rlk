# intro: the camera at #sq 664 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^-0.45 ^1.75 ^-0.9 facing ^0 ^1.5 ^20.7
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
