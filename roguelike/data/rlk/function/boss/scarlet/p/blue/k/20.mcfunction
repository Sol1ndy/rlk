# BLUE pattern tick 20
execute store result storage rlk:hr core.sw.d double 0.4583 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m22,limit=1] ~ ~2.293 ~
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_blue","rlk_hr_swn","rlk_hr_sw_blue22_20"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,transformation:{translation:[1.0939f,1.5477f,1.5129f],left_rotation:[0.1553f,-0.2904f,0.0478f,0.943f],scale:[0.36f,0.36f,0.6579f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
function rlk:boss/scarlet/p/blue/dash
execute at @s run function rlk:boss/scarlet/fx/snd/lunge
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:90}
