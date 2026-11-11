# TRI pattern tick 12
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:60,w:16,tell:2,dmg:31}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/tri
function rlk:boss/scarlet/p/tri/lunge
execute at @s run function rlk:boss/scarlet/fx/snd/lunge
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:60}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2853f,0.9609f,0.4651f],left_rotation:[-0.0175f,0.0174f,0.0003f,0.9997f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_11,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3709f,0.9064f,0.1461f],left_rotation:[-0.1267f,-0.0475f,-0.9315f,0.3377f],scale:[0.1721f,0.26f,1.435f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_tri","rlk_hr_trr","rlk_hr_trq","rlk_hr_tr_tri_12","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.4345f,0.9643f,0.4487f],left_rotation:[-0.0464f,-0.031f,-0.9945f,0.0882f],scale:[0f,0.26f,1.435f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_quad_0","minecraft:custom_model_data":{colors:[16774616]}}}}
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute at @s rotated as @s rotated ~ 0 positioned ^0.383 ^0.928 ^0.29 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_tri","rlk_hr_trt"]}
tag @e[type=minecraft:item_display,tag=rlk_hr_trg] remove rlk_hr_trg
execute at @s rotated as @s rotated ~ 0 positioned ^0.383 ^0.928 ^0.29 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_tri","rlk_hr_tri","rlk_hr_trg","rlk_hr_tr_trir0r12"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_rib_0","minecraft:custom_model_data":{colors:[16771496]}}}}
