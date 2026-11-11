# ending: the camera at #sq 336 (@s = the body).
tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] 880.0 206 30.0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
rotate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] facing 889.0 218 -34.0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/camin
