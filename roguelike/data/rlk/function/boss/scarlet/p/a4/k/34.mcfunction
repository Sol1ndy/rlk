# A4 pattern tick 34
tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_a434,limit=1]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a434_28]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a434_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a434_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_swn","rlk_hr_sw_a434_34"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.9214f,1.4526f,0.2475f],left_rotation:[-0.0101f,-0.7489f,-0.0131f,0.6625f],scale:[0.0924f,1f,0.5223f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:4}
