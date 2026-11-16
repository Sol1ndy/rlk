# A13 pattern tick 245.
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b225]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_239] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_241] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_243] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13r5r239] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_1"
