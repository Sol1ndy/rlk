# cs1: the camera at #sq 338 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^0.7 ^1.5 ^2.1
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] facing ^0 ^1.45 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/camin
