# intro: the camera at #sq 240 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^-0.9 ^0.75 ^0.9 facing ^-0.092 ^1.319 ^0.031
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
