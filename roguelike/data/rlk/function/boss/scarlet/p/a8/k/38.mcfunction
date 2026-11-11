# A8 pattern tick 38.
kill @e[type=minecraft:marker,tag=rlk_hr_gst]
function rlk:boss/scarlet/g/spot/side
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] add rlk_hr_gst
tag @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] remove rlk_hr_gsp
function rlk:boss/scarlet/g/cut/aim {s:48}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0697f,0.8201f,0.3034f],left_rotation:[-0.3799f,0.2126f,0.5964f,-0.6744f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_30]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_34] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_36] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_37,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2696f,0.8643f,-0.1258f],left_rotation:[0.1294f,-0.1313f,0.9827f,0.0173f],scale:[0.6119f,0.18f,1.797f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_37,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2873f,0.837f,0.0771f],left_rotation:[0.0432f,0.1324f,-0.9902f,0.0058f],scale:[0.5768f,0.18f,1.6929f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a8_38","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2925f,0.8692f,0.0583f],left_rotation:[0.1318f,0.1284f,-0.9822f,0.0366f],scale:[0f,0.18f,1.8287f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a8_38","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2138f,0.8563f,0.1817f],left_rotation:[0.1368f,0.1122f,-0.9815f,0.0725f],scale:[0f,0.18f,1.7529f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16771496]}}}}
