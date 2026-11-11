# ULT pattern tick 50
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_44]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_46] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_48] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/ai/tail
