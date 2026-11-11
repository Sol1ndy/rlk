# intro: the camera at #sq 248 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^-1.1 ^1.45 ^0.25 facing ^0 ^1.6 ^0.05
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
