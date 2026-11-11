# ULT pattern tick 49
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_43]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_45] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_47] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
