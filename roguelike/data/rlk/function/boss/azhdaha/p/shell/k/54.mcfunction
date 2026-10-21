# shell #azPT 54
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s7,limit=1] run data merge entity @s {teleport_duration:8}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s7,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @s ^0 ^9 ^4
function rlk:mboss/mv/turn {max:2}
