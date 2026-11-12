# intro: the camera at #sq 1348 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^-0.4 ^1.4 ^1.6 facing ^0 ^1.3 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
