# ending: the camera at #sq 1011 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^-0.958 ^1.461 ^1.284
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/ar/clampw
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] facing ^0 ^1.62 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/camin
