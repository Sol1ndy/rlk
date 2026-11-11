# repel: the camera at #sq 74 (@s = the body).
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^3.6 ^0.8 ^2.2
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing ^0 ^1.7 ^2.2
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/lift
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing ^0 ^1.7 ^2.2
