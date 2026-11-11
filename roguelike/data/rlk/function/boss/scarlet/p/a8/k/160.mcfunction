# A8 pattern tick 160.
function rlk:boss/scarlet/rig/play/g_wrap
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.6875f,1.2735f,-0.2615f],left_rotation:[-0.7094f,0.4967f,-0.2868f,0.4096f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_158] remove rlk_hr_trr
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a8_160","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2827f,1.1321f,-0.0139f],left_rotation:[-0.9254f,-0.1632f,-0.3366f,0.06f],scale:[0f,0.26f,2.0984f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.822 ^1.322 ^-0.344 run function rlk:boss/scarlet/core/sw/rib
