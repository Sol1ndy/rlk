# A1 pattern tick 18
function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a1b1]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_10]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_12] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_14] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_16] remove rlk_hr_trr
