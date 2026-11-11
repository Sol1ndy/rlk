# intro: the camera at #sq 786 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing ^-0.2 ^1.02 ^0.12
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^-0.5 ^1.45 ^1.7 facing ^0 ^1.6 ^0
