# ending: the camera at #sq 310 (@s = the body).
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^16 ^3 ^2
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/over
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes
