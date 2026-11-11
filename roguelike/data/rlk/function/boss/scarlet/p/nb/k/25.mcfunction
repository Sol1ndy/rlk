# NB pattern tick 25
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20_19]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20_21] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20_23] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb30,limit=1] ^0.949 ^3.108 ^1.541
