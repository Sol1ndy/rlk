# ending: the camera at #sq 211 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^3.5 ^3 ^2.8
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] facing ^0 ^5.583 ^2.817
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/camin
