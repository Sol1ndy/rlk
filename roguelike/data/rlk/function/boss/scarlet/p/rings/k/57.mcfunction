# RINGS pattern tick 57
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1b48] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3588f,1.0446f,0.3365f],left_rotation:[-0.4056f,-0.2988f,-0.5792f,-0.6409f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_49]
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_51] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_53] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #ph hr matches 7 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_55] remove rlk_hr_trr
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings1_56,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0712f,1.1049f,0.1766f],left_rotation:[0.0499f,0.371f,-0.0741f,0.9243f],scale:[0.6665f,0.3f,1.901f],right_rotation:[0f,0f,0f,1f]}}
