# D4 pattern tick 34
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_d434] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_d434,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d434_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_swn","rlk_hr_sw_d434_34"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.3616f,1.2716f,-0.0106f],left_rotation:[-0.1585f,0.0389f,0.6101f,0.7754f],scale:[0.7801f,1f,2.3905f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_d4","rlk_hr_swn","rlk_hr_sw_d434_34"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.3907f,1.2473f,-0.0438f],left_rotation:[-0.2546f,0.1632f,0.5766f,0.759f],scale:[0.7878f,1f,2.4141f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute at @s run function rlk:boss/scarlet/fx/snd/a3_h2
