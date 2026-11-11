# NB pattern tick 34
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb40] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb40,limit=1] ^0.088 ^2.71 ^1.927
