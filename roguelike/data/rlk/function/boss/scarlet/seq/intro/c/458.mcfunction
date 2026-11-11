# intro: the camera at #sq 458 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^-0.75 ^1 ^-0.9
rotate @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] facing 889.0 218 -34.0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
