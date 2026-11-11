# D4 pattern tick 17
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_d414] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_d414_11]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d414_13] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d414_15] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_swn","rlk_hr_sw_d414_17"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0657f,1.1245f,0.1961f],left_rotation:[0.0856f,0.1599f,-0.1152f,0.9766f],scale:[0.9285f,1f,2.0951f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
