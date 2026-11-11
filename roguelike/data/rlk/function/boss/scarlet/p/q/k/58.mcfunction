# Q pattern tick 58
execute if score #q_hit hr matches 1 run scoreboard players set #hzEl mb 3
execute if score #q_hit hr matches 1 run scoreboard players set #hzKB mb 0
execute if score #q_hit hr matches 1 run scoreboard players set #hzSfx mb 0
execute if score #q_hit hr matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #q_hit hr matches 1 run scoreboard players set #hzNoParry mb 0
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:26,tell:1,dmg:54}
execute if score #q_hit hr matches 1 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/q
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.5 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_swn","rlk_hr_sw_q_air38_58"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.1053f,1.0851f,0.7367f],left_rotation:[0.3234f,-0.3272f,0.6298f,0.6267f],scale:[0.4349f,1f,1.3012f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute if score #q_hit hr matches 1 run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
