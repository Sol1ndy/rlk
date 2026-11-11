# A3 pattern tick 43
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_a345] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_a345,limit=1] ^0.221 ^2.366 ^1.779
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a345] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a3","rlk_hr_swn","rlk_hr_sw_a345_43"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.2506f,1.2511f,0.2595f],left_rotation:[0.0701f,-0.3069f,0.5697f,0.7592f],scale:[0.4515f,1f,2.2287f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
