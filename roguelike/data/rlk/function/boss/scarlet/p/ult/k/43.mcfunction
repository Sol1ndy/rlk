# ULT pattern tick 43
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_ult46,limit=1] ^-0.567 ^0.849 ^2.006
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_ult","rlk_hr_swn","rlk_hr_sw_ult46_43"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.1621f,0.9792f,0.1279f],left_rotation:[-0.8156f,0.1278f,-0.5157f,0.2294f],scale:[0.3751f,1f,2.4577f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
