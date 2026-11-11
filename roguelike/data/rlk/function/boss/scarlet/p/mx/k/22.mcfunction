# MX pattern tick 22
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx16_16]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx16_18] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_mx28,limit=1] ^0.718 ^0.804 ^1.549
