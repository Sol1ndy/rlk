# A13 pattern tick 103.
function rlk:boss/scarlet/g/cut/aim {s:113}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b101] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1192f,0.6232f,0.2798f],left_rotation:[-0.5909f,-0.6634f,0.4146f,0.1972f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_95]
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_101] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_102,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.028f,0.7157f,0.5392f],left_rotation:[0.7238f,-0.5958f,-0.1891f,0.2922f],scale:[0.3686f,0.18f,1.9143f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a13_103","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.2079f,0.5913f,0.2121f],left_rotation:[0.1239f,-0.9265f,0.1102f,0.338f],scale:[0f,0.18f,1.4897f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.243 ^0.571 ^0.184 run function rlk:boss/scarlet/core/sw/rib
