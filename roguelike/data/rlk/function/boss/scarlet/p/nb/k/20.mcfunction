# NB pattern tick 20
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb20] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb20,limit=1]
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_nb20_20"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.5696f,1.7341f,0.5373f],left_rotation:[-0.2696f,-0.1515f,-0.3255f,0.8935f],scale:[0.8568f,1f,2.0584f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_nb20_20"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.578f,1.7036f,0.4463f],left_rotation:[-0.1976f,0.0336f,-0.3736f,0.9057f],scale:[0.8782f,1f,2.1099f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_n0] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~-30 0 positioned ~ ~0.6 ~ run function rlk:boss/scarlet/fx/p/qi_beam {len:160}
execute at @s run function rlk:boss/scarlet/fx/snd/g_sweep
