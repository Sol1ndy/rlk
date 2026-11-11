# Q pattern tick 83
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_on
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/rig/anchor/head
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/star4
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_off
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/a9_star
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_swl]
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_swlh]
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_swn","rlk_hr_swl"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.24f,0.24f,1f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[14060543]}}}}
execute if score #q_hit hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_q","rlk_hr_swlh"],billboard:"center",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.62f,0.62f,0.62f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_head","minecraft:custom_model_data":{colors:[14060543]}}}}
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_body,limit=1] add rlk_hr_swt
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.4 ^3.856 ^-0.125 facing entity @e[tag=rlk_body,limit=1] feet run function rlk:boss/scarlet/core/sw/aim {dy:"0"}
execute if score #q_hit hr matches 1 run tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute if score #q_hit hr matches 1 store result storage rlk:hr core.sw.d double 0.0417 run scoreboard players get #sw_n hr
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
