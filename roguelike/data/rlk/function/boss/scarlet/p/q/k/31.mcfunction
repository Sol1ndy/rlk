# Q pattern tick 31
execute unless score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4141f,2.0015f,0.3975f],left_rotation:[-0.7553f,-0.2899f,0.2106f,0.5488f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_23]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_25] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_27] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_1"
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_29] remove rlk_hr_trr
