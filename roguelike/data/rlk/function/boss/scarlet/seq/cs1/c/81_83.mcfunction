# cs1: the camera at #sq 81..83 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^-0.55 ^1.75 ^-1.3
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing ^0 ^1.4 ^9
