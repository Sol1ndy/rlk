# intro: the camera at #sq 1257 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] ^4.6 ^1.3 ^9.2
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^-0.719 ^-0.292 rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] facing ^0 ^1 ^0
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/cam/fix
function rlk:mboss/cam/spawn
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] {teleport_duration:0}
