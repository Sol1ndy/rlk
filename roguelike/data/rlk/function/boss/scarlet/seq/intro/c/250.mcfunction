# intro: the camera at #sq 250 (@s = the body).
scoreboard players set #mbCamId mb 1
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^-1.1 ^1.45 ^0.25 facing ^0 ^1.6 ^0.05
