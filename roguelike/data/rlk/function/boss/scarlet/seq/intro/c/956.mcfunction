# intro: the camera at #sq 956 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing ^0 ^1.7 ^0
function rlk:mboss/cam/spawn
tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] 878.0 204.5 2.0 facing 858.0 203 14.0
