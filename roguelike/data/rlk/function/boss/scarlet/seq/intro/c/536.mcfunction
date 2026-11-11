# intro: the camera at #sq 536 (@s = the body).
scoreboard players set #mbCamId mb 1
function rlk:mboss/cam/text
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^1.133 ^1.533 ^-1.5 facing ^-0.15 ^1.3 ^0.5
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
