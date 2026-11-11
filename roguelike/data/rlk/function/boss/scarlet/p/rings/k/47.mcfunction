# RINGS pattern tick 47
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_41]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_43] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_45] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_swn","rlk_hr_sw_rings44_47"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0035f,1.1633f,0.2484f],left_rotation:[0.4713f,0.0292f,-0.8812f,0.0239f],scale:[0.8216f,1f,2.0706f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_rings","rlk_hr_swn","rlk_hr_sw_rings44_47"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.0134f,1.1612f,0.2554f],left_rotation:[0.6337f,0.0333f,-0.7726f,0.0178f],scale:[0.8176f,1f,2.0606f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute if score #ph hr matches 7 run function rlk:mboss/mv/turn {max:10}
execute if score #ph hr matches 7 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #ph hr matches 7 run function rlk:boss/scarlet/fx/follow_on
execute if score #ph hr matches 7 run function rlk:boss/scarlet/rig/anchor/blade_mid
execute if score #ph hr matches 7 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
execute if score #ph hr matches 7 run function rlk:boss/scarlet/fx/follow_off
execute if score #ph hr matches 7 at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute if score #ph hr matches 7 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings54] ~ ~ ~ ~ 0
execute if score #ph hr matches 7 at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings54,limit=1] ^-0.289 ^1.033 ^1.761
