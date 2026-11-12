# D4 pattern tick 33
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:42,a:35,tell:1,dmg:31}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/d4
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4033f,1.6592f,0.3881f],left_rotation:[0f,-0.3746f,-0.9272f,0f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_31] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_32,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3066f,1.28f,0.1551f],left_rotation:[0.0113f,-0.2044f,0.569f,0.7964f],scale:[0.5803f,0.3f,2.0497f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_32,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3311f,1.2883f,0.0814f],left_rotation:[-0.0672f,-0.0907f,0.5598f,0.8209f],scale:[0.5912f,0.3f,2.0884f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_d4_33","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3601f,1.2715f,-0.0124f],left_rotation:[-0.1089f,-0.0265f,0.613f,0.7822f],scale:[0f,0.3f,2.1722f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_d4_33","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3888f,1.2487f,-0.0427f],left_rotation:[-0.1045f,-0.0211f,0.6276f,0.7713f],scale:[0f,0.3f,2.1903f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
