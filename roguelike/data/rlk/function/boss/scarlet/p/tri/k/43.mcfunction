# TRI pattern tick 43
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri38_37]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_tri38_39] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_tri38_41] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_tri48,limit=1] ^1.858 ^2.181 ^0.978
