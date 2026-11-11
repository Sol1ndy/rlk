# RINGS pattern tick 57
execute if score #ph hr matches 7 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54] ~ ~ ~ ~ 0
execute if score #ph hr matches 7 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_51]
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_53] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_55] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #ph hr matches 7 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_swn","rlk_hr_sw_rings54_57"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0712f,1.1049f,0.1767f],left_rotation:[0.0498f,0.371f,-0.0741f,0.9243f],scale:[0.7451f,1f,2.1254f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #ph hr matches 7 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
execute if score #ph hr matches 7 run tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
