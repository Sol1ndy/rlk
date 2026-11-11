# NB pattern tick 33
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30] ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_29] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_nb30_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_nb30_33"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.2593f,1.455f,0.5719f],left_rotation:[0.3678f,-0.5803f,0.2363f,0.6872f],scale:[0.9014f,1f,1.8725f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_nb30_33"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.3734f,1.6633f,0.5099f],left_rotation:[0.3024f,-0.4034f,0.3158f,0.8038f],scale:[0.965f,1f,2.005f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_n1]
function rlk:boss/scarlet/p/nb/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_nb40] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_nb40,limit=1] ^0.093 ^2.92 ^1.724
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~0 0 positioned ^ ^1.2 ^-8 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_swn","rlk_hr_sw_n2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.24f,0.24f,16f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[16771496]}}}}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~0 0 positioned ^ ^1.2 ^-8 run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ ~
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
