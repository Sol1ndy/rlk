# NB pattern tick 35
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_29]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb40] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb40,limit=1] ^0.509 ^2.517 ^2.021
