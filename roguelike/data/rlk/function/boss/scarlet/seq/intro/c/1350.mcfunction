# intro: the camera at #sq 1350 (@s = the body).
scoreboard players set #mbCamId mb 2
function rlk:mboss/cam/text
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^-0.6 ^1.3 ^3.2 facing ^0 ^1.3 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
