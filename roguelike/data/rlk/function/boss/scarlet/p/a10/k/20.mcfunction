# A10 pattern tick 20
execute store result storage rlk:hr core.sw.d double 0.4583 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a10","rlk_hr_swn","rlk_hr_sw_a1022_20"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0049f,1.5356f,0.722f],left_rotation:[-0.4856f,-0.4856f,-0.514f,0.514f],scale:[0.5557f,1f,1.9162f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a10","rlk_hr_swn","rlk_hr_sw_a1022_20"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0016f,1.2589f,0.6657f],left_rotation:[-0.4068f,-0.4069f,-0.5783f,0.5783f],scale:[0.601f,1f,2.0724f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
function rlk:boss/scarlet/core/near {d:1.4,t:2}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 203 ~ run function rlk:boss/scarlet/fx/p/claw_streaks {r:15}
execute at @s run function rlk:boss/scarlet/fx/snd/a10_dive
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
