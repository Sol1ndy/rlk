# intro: the camera at #sq 1230 (@s = the body).
scoreboard players set #mbCamId mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^0.8 ^0.3 ^8.5
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes
