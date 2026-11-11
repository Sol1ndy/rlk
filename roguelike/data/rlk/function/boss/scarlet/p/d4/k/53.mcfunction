# D4 pattern tick 53
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:36,a:60,tell:1,dmg:42}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/d4
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0473f,0.9591f,0.5688f],left_rotation:[-0.0616f,0f,0.7044f,-0.7071f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_45]
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_51] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_52,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0874f,0.9642f,0.1486f],left_rotation:[0.6584f,-0.0403f,0.7508f,0.0353f],scale:[0.8402f,0.26f,1.9059f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_52,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0905f,0.9709f,0.1498f],left_rotation:[0.4803f,-0.047f,0.8755f,0.0258f],scale:[0.8395f,0.26f,1.9042f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_d4_53","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.066f,0.9828f,0.125f],left_rotation:[0.3821f,-0.0492f,0.9226f,0.0189f],scale:[0f,0.26f,1.9959f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_d4_53","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.082f,0.9877f,0.1688f],left_rotation:[-0.3812f,0.0487f,-0.9232f,0.0023f],scale:[0f,0.26f,1.9725f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
