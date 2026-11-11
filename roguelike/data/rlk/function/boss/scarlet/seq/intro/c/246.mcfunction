# intro: the camera at #sq 246 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^-0.9 ^0.75 ^0.9 facing ^-0.069 ^1.377 ^0.023
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^-1.1 ^1.45 ^0.25 facing ^0 ^1.6 ^0.05
