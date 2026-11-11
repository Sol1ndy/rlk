# TRI pattern tick 44
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri38_38]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_tri38_40] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_tri48] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_tri48,limit=1] ^1.573 ^1.981 ^1.378
