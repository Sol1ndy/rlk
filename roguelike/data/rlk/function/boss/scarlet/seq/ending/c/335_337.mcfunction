# ending: the camera at #sq 335..337 (@s = the body).
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes
tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] 880.0 206 30.0
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing 889.0 218 -34.0
