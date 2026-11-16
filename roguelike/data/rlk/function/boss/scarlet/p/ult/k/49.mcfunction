# ULT pattern tick 49
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_43] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_45] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_47] remove rlk_hr_trr
