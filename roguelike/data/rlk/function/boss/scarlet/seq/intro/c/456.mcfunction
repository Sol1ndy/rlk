# intro: the camera at #sq 456 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing ^-0.45 ^0.28 ^0
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^-0.75 ^1 ^-0.9
rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] facing 889.0 218 -34.0
