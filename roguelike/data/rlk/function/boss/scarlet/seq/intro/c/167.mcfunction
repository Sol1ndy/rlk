# intro: the camera at #sq 167 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^3 ^1.5 ^14
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing 888.797 218 -34.0
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^-0.9 ^0.75 ^0.9 facing ^-0.25 ^0.62 ^0.35
