# ending: the camera at #sq 843..845 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing ^0 ^1.4 ^0
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^0.4 ^1.5 ^1.6
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing ^0 ^1.45 ^0
