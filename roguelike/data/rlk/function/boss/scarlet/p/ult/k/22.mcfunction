# ULT pattern tick 22
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_ult24] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_ult24,limit=1] ^0.106 ^0.949 ^2.077
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_ult24] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_ult","rlk_hr_swn","rlk_hr_sw_ult24_22"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.1805f,0.8045f,0.2215f],left_rotation:[-0.1122f,-0.919f,0.2089f,0.3151f],scale:[0.7602f,1f,1.9094f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
