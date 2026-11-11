# D4 pattern tick 52
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d444_46]
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_d454] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_d454,limit=1] ^0.445 ^0.795 ^2.036
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d454] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_swn","rlk_hr_sw_d454_52"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.117f,0.969f,0.1372f],left_rotation:[0.8535f,-0.0339f,0.5183f,0.0423f],scale:[0.5667f,1f,2.1648f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_swn","rlk_hr_sw_d454_52"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0859f,0.966f,0.1486f],left_rotation:[0.779f,-0.0281f,0.6247f,0.0463f],scale:[0.5715f,1f,2.1829f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
