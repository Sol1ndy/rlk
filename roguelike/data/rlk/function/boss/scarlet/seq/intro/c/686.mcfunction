# intro: the camera at #sq 686 (@s = the body).
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^0.35 ^1.45 ^1.5 facing ^0 ^1.35 ^0
