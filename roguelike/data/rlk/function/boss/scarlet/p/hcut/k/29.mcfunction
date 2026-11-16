# HCUT pattern tick 29
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_23] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_25] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_27] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutr0r24] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_1"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutw0w] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_2"
