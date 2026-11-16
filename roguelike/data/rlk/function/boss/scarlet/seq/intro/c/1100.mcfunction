# intro: the camera at #sq 1100 (@s = the body).
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^-1.808 rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^0.45 ^1.65 ^1.75 facing ^0 ^1.65 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
