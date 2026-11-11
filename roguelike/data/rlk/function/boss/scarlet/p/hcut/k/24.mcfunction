# HCUT pattern tick 24
execute store result storage rlk:hr core.sw.d double 0.4583 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m26,limit=1] ~ ~2.293 ~
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_hcut","rlk_hr_swn","rlk_hr_sw_hcut26_24"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.2727f,0.7106f,0.4406f],left_rotation:[0.874f,-0.0501f,0.4745f,0.0921f],scale:[0.4703f,1f,2.7138f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
function rlk:boss/scarlet/p/hcut/dash
execute at @s run function rlk:boss/scarlet/fx/snd/g_dash
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:160}
