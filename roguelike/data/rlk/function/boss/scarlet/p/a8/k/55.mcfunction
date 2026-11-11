# A8 pattern tick 55.
function rlk:boss/scarlet/g/cut/aim {s:64}
function rlk:boss/scarlet/rig/play/g_leap
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5133f,1.6194f,-0.3365f],left_rotation:[-0.6989f,-0.4542f,-0.5504f,-0.0489f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_47]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_49] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_51] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a8_55","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3236f,1.5102f,-0.2248f],left_rotation:[-0.6321f,0.4767f,-0.0858f,0.6044f],scale:[0f,0.18f,1.9002f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
