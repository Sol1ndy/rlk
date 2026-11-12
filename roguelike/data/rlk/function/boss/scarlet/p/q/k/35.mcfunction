# Q pattern tick 35
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.383f,2.0646f,0.588f],left_rotation:[-0.7553f,-0.2899f,0.2106f,0.5488f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_27]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_29] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_2"
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_34,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2872f,2.1518f,0.4168f],left_rotation:[-0.3988f,-0.7039f,-0.1862f,0.5575f],scale:[0.2427f,0.22f,1.435f],right_rotation:[0f,0f,0f,1f]}}
