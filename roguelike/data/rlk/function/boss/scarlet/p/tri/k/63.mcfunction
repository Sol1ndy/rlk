# TRI pattern tick 63
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_57] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_59] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_61] remove rlk_hr_trr
