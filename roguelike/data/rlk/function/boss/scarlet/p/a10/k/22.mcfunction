# A10 pattern tick 22
kill @e[type=minecraft:item_display,tag=rlk_hr_swlh]
execute as @e[type=minecraft:item_display,tag=rlk_hr_swl] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a1022_20] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a10","rlk_hr_swn","rlk_hr_sw_a1022_22"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0751f,1.0892f,-0.4982f],left_rotation:[0.011f,0.011f,-0.7066f,0.7075f],scale:[0.6316f,1f,3.1169f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a10","rlk_hr_swn","rlk_hr_sw_a1022_22"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.067f,1.0883f,-0.4917f],left_rotation:[0.0821f,0.0823f,-0.7019f,0.7027f],scale:[0.6309f,1f,3.1133f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run function rlk:boss/scarlet/fx/p/burst_radial {r:35}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:boss/scarlet/fx/snd/a10_impact
