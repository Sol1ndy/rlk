# intro: the camera at #sq 579 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^1.067 ^1.517 ^-1.4 facing ^-0.15 ^1.3 ^0.5
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
