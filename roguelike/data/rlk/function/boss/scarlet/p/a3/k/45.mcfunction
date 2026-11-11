# A3 pattern tick 45
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_a345] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_a345,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a345_43] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a3","rlk_hr_swn","rlk_hr_sw_a345_45"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.3409f,1.3009f,0.0497f],left_rotation:[-0.1109f,-0.0452f,0.592f,0.797f],scale:[0.9391f,1f,2.3024f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a3","rlk_hr_swn","rlk_hr_sw_a345_45"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.3436f,1.2841f,-0.0074f],left_rotation:[-0.227f,0.115f,0.5579f,0.7899f],scale:[0.9524f,1f,2.3349f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute at @s run function rlk:boss/scarlet/fx/snd/a3_h3
