# Q pattern tick 96
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_92] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_94] remove rlk_hr_trr
