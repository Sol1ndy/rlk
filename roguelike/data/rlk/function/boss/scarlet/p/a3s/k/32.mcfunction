# A3S pattern tick 32
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3sb1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3s_28] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a3s_30] remove rlk_hr_trr
