# cs1: the camera at #sq 11 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^2.492 ^1.308 ^0.8
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing ^0 ^1.45 ^0.75
