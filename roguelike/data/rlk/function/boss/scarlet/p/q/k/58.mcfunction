# Q pattern tick 58
execute if score #q_hit hr matches 1 run scoreboard players set #hzEl mb 3
execute if score #q_hit hr matches 1 run scoreboard players set #hzKB mb 0
execute if score #q_hit hr matches 1 run scoreboard players set #hzSfx mb 0
execute if score #q_hit hr matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #q_hit hr matches 1 run scoreboard players set #hzNoParry mb 0
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:26,tell:1,dmg:54}
execute if score #q_hit hr matches 1 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/q
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2228f,0.9797f,0.6028f],left_rotation:[-0.256f,-0.0685f,0.2499f,-0.9313f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_50]
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_56] remove rlk_hr_trr
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_57,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1054f,1.314f,0.6072f],left_rotation:[0.3809f,-0.2561f,0.4949f,0.7379f],scale:[0.1628f,0.3f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_q1_58","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.179f,0.6358f,1.1816f],left_rotation:[0.2718f,-0.2949f,0.6504f,0.6543f],scale:[0f,0.3f,0.821f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16774616]}}}}
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.223 ^0.895 ^0.745 run function rlk:boss/scarlet/core/sw/rib
