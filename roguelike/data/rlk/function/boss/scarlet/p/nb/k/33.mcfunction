# NB pattern tick 33
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30] ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_29] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_nb30_33"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.1632f,1.347f,0.5853f],left_rotation:[0.3134f,-0.6324f,0.2541f,0.6613f],scale:[0.6752f,1f,1.8055f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_nb30_33"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.2947f,1.5296f,0.545f],left_rotation:[0.2614f,-0.5002f,0.3073f,0.7662f],scale:[0.7219f,1f,1.9305f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_nb30_33"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.3536f,1.6376f,0.473f],left_rotation:[0.2006f,-0.3509f,0.3501f,0.845f],scale:[0.7508f,1f,2.0077f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_n1]
function rlk:boss/scarlet/p/nb/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^-0.067 ^3.256 ^0.948 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb40] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb40,limit=1] ^0.38 ^3.003 ^1.602
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~0 0 positioned ^ ^1.2 ^-8 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_n2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.24f,0.24f,16f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[16771496]}}}}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~0 0 positioned ^ ^1.2 ^-8 run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ ~
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
