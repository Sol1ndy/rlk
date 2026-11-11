# RINGS pattern tick 28
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings24]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings24_22]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings24_24] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings24_26] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings34] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings34,limit=1] ^1.254 ^1.065 ^1.375
