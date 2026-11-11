# NB pattern tick 24
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20_20] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20_22] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb30,limit=1] ^1.162 ^3.18 ^1.2
