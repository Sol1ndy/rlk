# Q pattern tick 57
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.4375 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_swn","rlk_hr_sw_q_air38_57"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0503f,1.7282f,0.4228f],left_rotation:[0.4094f,-0.4096f,0.5766f,0.5766f],scale:[0.4393f,1f,1.842f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #q_hit hr matches 1 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
