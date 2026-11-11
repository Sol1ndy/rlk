# KCUT pattern tick 25
kill @e[type=minecraft:item_display,tag=rlk_hr_swl]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_kcut22_19]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_kcut22_21] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_kcut22_23] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_k0]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_k1]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_k2]
