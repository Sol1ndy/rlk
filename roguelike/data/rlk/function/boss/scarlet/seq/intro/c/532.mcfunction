# intro: the camera at #sq 532 (@s = the body).
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^1.2 ^1.55 ^-1.6 facing ^-0.15 ^1.3 ^0.5
