# TRI pattern tick 12
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:60,w:16,tell:2,dmg:31}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/tri
function rlk:boss/scarlet/p/tri/lunge
execute at @s run function rlk:boss/scarlet/fx/snd/lunge
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:60}
execute store result storage rlk:hr core.sw.d double 0.4583 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[tag=rlk_body,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m14,limit=1] ~ ~2.293 ~
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_tri","rlk_hr_swn","rlk_hr_sw_tri14_12"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,transformation:{translation:[0.7439f,1.2334f,1.3474f],left_rotation:[0.184f,-0.2086f,0.04f,0.9597f],scale:[0.36f,0.36f,0.4208f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
