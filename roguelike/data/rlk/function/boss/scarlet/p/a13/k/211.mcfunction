# A13 pattern tick 211.
function rlk:boss/scarlet/g/cut/aim {s:220}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b140] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0929f,1.3994f,0.3909f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_203]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_205] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_207] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_209] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_210,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1762f,1.0695f,0.2275f],left_rotation:[-0.5004f,-0.3169f,0.2992f,0.7481f],scale:[0.7349f,0.18f,1.9766f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a13_211","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.065f,1.1827f,0.3056f],left_rotation:[-0.5409f,-0.2099f,0.3048f,0.7552f],scale:[0f,0.18f,1.8696f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
