# MX pattern tick 30
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_24]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_26] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_28] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_mx","rlk_hr_swn","rlk_hr_sw_mx28_30"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.1391f,1.0958f,0.24f],left_rotation:[0.0465f,-0.75f,0.0529f,0.6577f],scale:[0.4825f,1f,1.8342f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
