# ULT pattern tick 50
function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_42]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_46] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
