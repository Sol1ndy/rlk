# ending: the camera at #sq 338 (@s = the body).
scoreboard players set #mbCamId mb 1
tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] 880.0 206 30.0
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing 889.0 218 -34.0
