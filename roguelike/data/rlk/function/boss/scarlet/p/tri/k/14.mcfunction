# TRI pattern tick 14
kill @e[type=minecraft:item_display,tag=rlk_hr_swlh]
execute as @e[type=minecraft:item_display,tag=rlk_hr_swl] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_tri14_12] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_tri","rlk_hr_swn","rlk_hr_sw_tri14_14"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,transformation:{translation:[0.3411f,1.0167f,2.0632f],left_rotation:[-0.0317f,-0.1118f,-0.0036f,0.9932f],scale:[0.36f,0.36f,0.3619f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[14857471]}}}}
tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute at @s run function rlk:boss/scarlet/fx/snd/a2_hit
