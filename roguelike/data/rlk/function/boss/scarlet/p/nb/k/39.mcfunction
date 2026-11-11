# NB pattern tick 39
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~0 0 positioned ^ ^ ^-8 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:160,w:30,tell:1,dmg:54}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/nb
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1357f,1.3104f,0.8151f],left_rotation:[0.0175f,0f,0f,0.9998f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_31]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_38,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.091f,1.5087f,0.6754f],left_rotation:[-0.4491f,-0.3451f,-0.5257f,0.6348f],scale:[0.5869f,0.26f,1.8047f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_38,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0911f,1.449f,0.6439f],left_rotation:[-0.4286f,-0.1294f,-0.4294f,0.7844f],scale:[0.5982f,0.26f,1.8403f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_nb_39","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1026f,1.4017f,0.6234f],left_rotation:[-0.2993f,-0.2599f,-0.8019f,0.4449f],scale:[0f,0.26f,1.8531f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_nb_39","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1288f,1.323f,0.4795f],left_rotation:[-0.1515f,-0.13f,-0.7389f,0.6438f],scale:[0f,0.26f,1.9521f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
