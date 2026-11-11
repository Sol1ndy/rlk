# A13 pattern tick 242.
function rlk:boss/scarlet/shield/judge
function rlk:boss/scarlet/fx/hud/warn {on:0}
execute if score #gres hr matches 2 run function rlk:boss/scarlet/p/a13/fail
execute if score #gres hr matches 1 run scoreboard players set #done hr 1
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b225] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1538f,1.3795f,0.293f],left_rotation:[-0.4287f,-0.0962f,-0.0478f,-0.897f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_238] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_240] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_241,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1196f,1.3003f,0.4847f],left_rotation:[0.3474f,0.2481f,-0.5228f,0.7379f],scale:[0.2243f,0.26f,1.435f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a13","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a13_242","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1535f,1.3806f,0.2922f],left_rotation:[0.4311f,0.0026f,0.0014f,0.9023f],scale:[0f,0.26f,1.6014f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[15584255]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.189 ^1.254 ^0.394 run function rlk:boss/scarlet/core/sw/rib
