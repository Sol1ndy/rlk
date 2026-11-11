# MX pattern tick 23
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx16_17]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx16_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_mx28,limit=1] ^1.523 ^0.796 ^0.74
