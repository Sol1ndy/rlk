# MX pattern tick 32
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_26]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_28] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/ai/tail
