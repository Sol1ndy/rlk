# TRI pattern tick 64
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri60]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_tri60_60] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_tri60_62] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/ai/tail
