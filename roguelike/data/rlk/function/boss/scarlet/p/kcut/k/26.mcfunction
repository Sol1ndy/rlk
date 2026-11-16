# KCUT pattern tick 26
function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_18]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_20] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_22] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutw0w]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutw1w]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutw2w]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutw3w]
