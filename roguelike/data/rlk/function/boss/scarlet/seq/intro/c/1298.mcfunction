# intro: the camera at #sq 1298 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^-0.15 ^1.93 ^1.801 facing ^0 ^1.55 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
