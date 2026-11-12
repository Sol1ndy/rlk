# intro: the camera at #sq 978 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^-0.7 ^2 ^1.5 facing ^0 ^1.95 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
