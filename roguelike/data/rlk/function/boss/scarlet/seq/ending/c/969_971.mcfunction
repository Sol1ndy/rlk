# ending: the camera at #sq 969..971 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^-1.3 ^1.5 ^-2.2
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing 889.0 218 -34.0
