# A4 pattern tick 19
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:26,tell:1,dmg:54}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/a4
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2504f,0.754f,0.6305f],left_rotation:[0.192f,0.0001f,0.0002f,0.9814f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_13] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_15] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_17] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_18,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3996f,1.4423f,0.3023f],left_rotation:[-0.4545f,-0.4546f,-0.5417f,0.5417f],scale:[0.663f,0.26f,1.8791f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_18,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3802f,1.3425f,0.2659f],left_rotation:[-0.3536f,-0.3536f,-0.6124f,0.6124f],scale:[0.6814f,0.26f,1.9314f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_18,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3608f,1.328f,0.2537f],left_rotation:[-0.2418f,-0.2418f,-0.6645f,0.6645f],scale:[0.6847f,0.26f,1.9408f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a4_19","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3343f,1.0953f,-0.1493f],left_rotation:[-0.183f,-0.1805f,-0.683f,0.683f],scale:[0f,0.26f,2.4039f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a4_19","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3007f,1.0781f,-0.2259f],left_rotation:[-0.183f,-0.1806f,-0.6829f,0.6831f],scale:[0f,0.26f,2.4431f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a4_19","rlk_hr_tr_i2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2671f,1.0719f,-0.1507f],left_rotation:[0.0293f,0.0319f,-0.7064f,0.7066f],scale:[0f,0.26f,2.4053f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.25 ^0.692 ^0.783 run function rlk:boss/scarlet/core/sw/rib
