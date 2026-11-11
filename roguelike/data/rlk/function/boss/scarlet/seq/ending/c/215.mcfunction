# ending: the camera at #sq 215 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^3.5 ^3 ^2.8
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing ^0 ^5.942 ^2.808
