# ending: the camera at #sq 554 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^-0.4 ^1.5 ^1.7
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run rotate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] facing ^0 ^1.45 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/camin
