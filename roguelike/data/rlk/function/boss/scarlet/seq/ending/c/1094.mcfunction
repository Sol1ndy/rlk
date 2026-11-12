# ending: the camera at #sq 1094 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] ^-0.4 ^1.6 ^2.75
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] positioned ^0 ^0 ^-4.425 rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] facing ^0 ^1.6 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:mboss/cam/fix
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/camin
