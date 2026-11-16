# D4 pattern tick 58
function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_52] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_54] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_56] remove rlk_hr_trr
