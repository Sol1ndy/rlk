# shell #azPT 44
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s5,limit=1] run data merge entity @s {teleport_duration:8}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s5,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @s ^0 ^7 ^9.5
function rlk:mboss/mv/turn {max:2}
