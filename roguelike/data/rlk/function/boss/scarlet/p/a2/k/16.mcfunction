# A2 pattern tick 16
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a212]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a212_10]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a212_12] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a212_14] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/ai/tail
