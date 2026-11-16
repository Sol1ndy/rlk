# A8 pattern tick 85.
function rlk:boss/scarlet/rig/play/g_sweep
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b76] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.283f,0.7885f,0.2624f],left_rotation:[-0.6198f,-0.6937f,0.2943f,0.219f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_77]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_79] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a8_85","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.6575f,0.71f,-0.1991f],left_rotation:[0.6749f,-0.6341f,-0.3025f,0.2045f],scale:[0f,0.3f,0.9428f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8r2r76] remove rlk_hr_trg
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
