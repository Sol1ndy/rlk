# Q pattern tick 59
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_swlh]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_swl] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air38_57] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_swn","rlk_hr_sw_q_air38_59"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.179f,0.6358f,1.1815f],left_rotation:[0.2304f,-0.2326f,0.6667f,0.6705f],scale:[0.2523f,1f,0.9092f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #q_hit hr matches 1 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run function rlk:boss/scarlet/fx/p/dive_impact {r:26}
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:boss/scarlet/fx/snd/a4_impact
