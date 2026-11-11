# RINGS pattern tick 53
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_47]
execute if score #ph hr matches 7 run scoreboard players set #hzEl mb 3
execute if score #ph hr matches 7 run scoreboard players set #hzKB mb 3
execute if score #ph hr matches 7 run scoreboard players set #hzSfx mb 0
execute if score #ph hr matches 7 run scoreboard players set #hzQuiet mb 1
execute if score #ph hr matches 7 run scoreboard players set #hzNoParry mb 0
execute if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:26,tell:1,dmg:42}
execute if score #ph hr matches 7 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/rings
execute if score #ph hr matches 7 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54] ~ ~ ~ ~ 0
execute if score #ph hr matches 7 at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings54,limit=1] ^-2.002 ^1.03 ^0.533
execute if score #ph hr matches 7 as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54_51] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #ph hr matches 7 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_swn","rlk_hr_sw_rings54_53"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.0626f,1.199f,-0.2435f],left_rotation:[-0.0026f,0.9175f,-0.0455f,0.3951f],scale:[0.9261f,1f,1.9596f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #ph hr matches 7 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_swn","rlk_hr_sw_rings54_53"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.2089f,1.211f,-0.0208f],left_rotation:[0.0079f,0.9838f,-0.0448f,0.1735f],scale:[0.9947f,1f,2.1046f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #ph hr matches 7 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_swn","rlk_hr_sw_rings54_53"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.2156f,1.2044f,0.0349f],left_rotation:[-0.018f,-0.9973f,0.0418f,0.0574f],scale:[1.0089f,1f,2.1347f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #ph hr matches 7 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
execute if score #ph hr matches 7 run tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
