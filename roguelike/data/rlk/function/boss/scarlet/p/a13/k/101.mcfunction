# A13 pattern tick 101.
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.45 ~ run function rlk:boss/scarlet/fx/p/ghost_trail {len:65}
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:7}
execute at @s run function rlk:boss/scarlet/fx/snd/g_dash
function rlk:boss/scarlet/g/cut/aim {s:113}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b101] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1976f,0.6791f,0.3011f],left_rotation:[-0.6774f,-0.6495f,0.2844f,0.196f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_93]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_95] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a13_101","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.1805f,0.6824f,0.3318f],left_rotation:[0.659f,-0.6621f,-0.3067f,0.184f],scale:[0f,0.22f,1.6262f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.304 ^0.712 ^0.2 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_trt"]}
tag @e[type=minecraft:item_display,tag=rlk_hr_trg] remove rlk_hr_trg
execute at @s rotated as @s rotated ~ 0 positioned ^-0.304 ^0.712 ^0.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_tri","rlk_hr_trg","rlk_hr_tr_a13r3r101"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_rib_0","minecraft:custom_model_data":{colors:[16771496]}}}}
