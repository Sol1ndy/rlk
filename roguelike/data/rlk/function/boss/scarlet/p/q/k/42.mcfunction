# Q pattern tick 42
execute if score #q_hit hr matches 1 run scoreboard players set #hzEl mb 3
execute if score #q_hit hr matches 1 run scoreboard players set #hzKB mb 0
execute if score #q_hit hr matches 1 run scoreboard players set #hzSfx mb 0
execute if score #q_hit hr matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #q_hit hr matches 1 run scoreboard players set #hzNoParry mb 0
execute if score #q_hit hr matches 1 at @s positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet rotated ~ 0 run function rlk:mboss/hz/line {len:140,w:26,tell:1,dmg:42}
execute if score #q_hit hr matches 1 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/q
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.5 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_swn","rlk_hr_sw_q_air22_42"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.5597f,1.8405f,0.4758f],left_rotation:[-0.3023f,-0.6789f,-0.2722f,0.6113f],scale:[0.852f,1f,2.0044f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_swn","rlk_hr_sw_q_air22_42"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.5204f,1.882f,0.4818f],left_rotation:[-0.2391f,-0.537f,-0.3291f,0.7391f],scale:[0.8387f,1f,1.9729f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #q_hit hr matches 1 at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
