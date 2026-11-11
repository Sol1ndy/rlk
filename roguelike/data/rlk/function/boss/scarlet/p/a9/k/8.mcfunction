# A9 pattern tick 8
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a9f3_4] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a9f3_6] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_swn","rlk_hr_sw_a9f3_8"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.2589f,1.1612f,0.0802f],left_rotation:[0.0524f,-0.9476f,0.0638f,0.3085f],scale:[0.7418f,1f,1.9594f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_swn","rlk_hr_sw_a9f3_8"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.0794f,1.1839f,0.2491f],left_rotation:[0.0396f,-0.8737f,0.0724f,0.4793f],scale:[0.7931f,1f,2.095f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_swn","rlk_hr_sw_a9f3_8"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0297f,1.1854f,0.2929f],left_rotation:[0.0255f,-0.7694f,0.0784f,0.6334f],scale:[0.8173f,1f,2.1588f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/chest
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/yellow_tell {t:6}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/yellow_chime
