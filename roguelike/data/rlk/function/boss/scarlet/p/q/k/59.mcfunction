# Q pattern tick 59
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run function rlk:boss/scarlet/fx/p/dive_impact {r:26}
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:boss/scarlet/fx/snd/a4_impact
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.244f,0.8765f,0.601f],left_rotation:[-0.2315f,-0.046f,0.1898f,-0.953f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[14060543]}}}}
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_55] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_57] remove rlk_hr_trr
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_58,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.179f,0.6358f,1.1816f],left_rotation:[0.2304f,-0.2326f,0.6667f,0.6705f],scale:[0.2256f,0.3f,0.8132f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.244 ^0.801 ^0.748 run function rlk:boss/scarlet/core/sw/rib
