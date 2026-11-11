# Q pattern tick 63
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air38_57]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air38_59] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
