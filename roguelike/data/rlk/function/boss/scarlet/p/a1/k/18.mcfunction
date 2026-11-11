# A1 pattern tick 18
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a114]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a114_12]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a114_14] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a114_16] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/ai/tail
