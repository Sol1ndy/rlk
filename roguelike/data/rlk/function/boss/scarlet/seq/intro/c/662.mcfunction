# intro: the camera at #sq 662 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^1.005 ^1.501 ^-1.307 facing ^-0.15 ^1.3 ^0.5
function rlk:mboss/cam/spawn
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] ^-0.45 ^1.75 ^-0.9 facing ^0 ^1.5 ^20.7
