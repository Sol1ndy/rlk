# A3 pattern tick 73
function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_67] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_69] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_71] remove rlk_hr_trr
