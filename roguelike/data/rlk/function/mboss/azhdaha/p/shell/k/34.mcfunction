# shell #azPT 34
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s3,limit=1] run data merge entity @s {teleport_duration:8}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s3,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @s ^3.6 ^8.5 ^5
function rlk:mboss/azhdaha/rig/play/idle
function rlk:mboss/mv/turn {max:2}
