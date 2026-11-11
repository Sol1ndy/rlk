# D4 pattern tick 58
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d454]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d454_52]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d454_54] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d454_56] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/ai/tail
