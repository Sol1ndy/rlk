# Q pattern tick 46
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_swl]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air22_42] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air22_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
