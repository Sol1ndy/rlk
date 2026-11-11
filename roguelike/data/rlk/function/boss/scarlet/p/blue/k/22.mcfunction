# BLUE pattern tick 22
execute at @s run function rlk:boss/scarlet/fx/snd/a2_hit
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blueb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2562f,1.0384f,1.0281f],left_rotation:[0f,0f,-0.7071f,0.7071f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_20] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_21,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2838f,1.091f,1.03f],left_rotation:[-0.0195f,0f,-0.8951f,0.4454f],scale:[0.1756f,0.3f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.256 ^1.038 ^1.193 run function rlk:boss/scarlet/core/sw/rib
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ 202 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_blue","rlk_hr_tri","rlk_hr_trn","rlk_hr_tr_bluew0w"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_rib_0","minecraft:custom_model_data":{colors:[5941503]}}}}
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ 202 ~ run tp @e[type=minecraft:item_display,tag=rlk_hr_trn] ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_trn] store result entity @s transformation.scale[2] float 0.5 run scoreboard players get #blue_n hr
tag @e[type=minecraft:item_display,tag=rlk_hr_trn] remove rlk_hr_trn
