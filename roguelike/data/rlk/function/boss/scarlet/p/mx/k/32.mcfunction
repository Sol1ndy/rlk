# MX pattern tick 32
function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_mxb1]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_24]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_26] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_28] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_30] remove rlk_hr_trr
