# ending: the camera at #sq 878 (@s = the body).
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^2.2 ^1.6 ^-2.6
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing ^-1.2 ^1.2 ^9
