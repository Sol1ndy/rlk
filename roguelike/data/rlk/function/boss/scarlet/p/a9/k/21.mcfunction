# A9 pattern tick 21
function rlk:boss/scarlet/p/a9/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..9] rotated as @s rotated ~ 0 positioned ^ ^ ^9 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
tag @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] add rlk_hr_swt
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet positioned ~ ~1.0 ~ run function rlk:boss/scarlet/core/sw/aim {dy:"-1.0"}
tag @e[tag=rlk_hr_swt] remove rlk_hr_swt
execute store result storage rlk:hr core.sw.d double 0.25 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ ~1.95 ~ rotated 0 -90 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_swn","rlk_hr_sw_m28"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.14f,0.14f,2.4f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[14060543]}}}}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ ~1.95 ~ rotated 0 -90 run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ ~
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ ~4.35 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_swh","rlk_hr_sw_m28"],billboard:"center",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.36f,0.36f,0.36f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_head","minecraft:custom_model_data":{colors:[14060543]}}}}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m28,limit=1] ~ ~4.007 ~
