# BLUE pattern tick 21
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line with storage rlk:hr core.dash
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/blue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blueb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2616f,1.0364f,1.0308f],left_rotation:[0f,0f,-0.7071f,0.7071f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_19] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_20,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2081f,1.1042f,-0.5011f],left_rotation:[-0.074f,-0.0176f,-0.9806f,0.1805f],scale:[0.4019f,0.3f,2.6931f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_blue","rlk_hr_trr","rlk_hr_trq","rlk_hr_tr_blue_21","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3367f,1.161f,1.0269f],left_rotation:[-0.0195f,0f,-0.8951f,0.4454f],scale:[0f,0.3f,1.435f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_quad_0","minecraft:custom_model_data":{colors:[11917567]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.262 ^1.036 ^1.196 run function rlk:boss/scarlet/core/sw/rib
