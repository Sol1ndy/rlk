# A4 pattern tick 28
execute at @s positioned ~ 202 ~ run function rlk:mboss/mv/glide {t:2}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_a434] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_a434,limit=1] ^1.1 ^1.494 ^0.998
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a434] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_swn","rlk_hr_sw_a434_28"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.3973f,1.2046f,0.4083f],left_rotation:[-0.0161f,-0.7602f,-0.0106f,0.6493f],scale:[0.4713f,1f,1.3713f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_swn","rlk_hr_sw_a434_28"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.0685f,1.3561f,0.4079f],left_rotation:[-0.0138f,-0.6493f,-0.0128f,0.7602f],scale:[0.5238f,1f,1.5497f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
