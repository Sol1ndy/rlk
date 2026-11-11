# ULT pattern tick 46
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46] ~ ~ ~ ~ 0
kill @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_ult46,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_ult","rlk_hr_swn","rlk_hr_sw_ult46_46"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0345f,0.9552f,0.2988f],left_rotation:[0.0701f,0.011f,-0.9955f,0.062f],scale:[1.0045f,1f,2.006f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_ult","rlk_hr_swn","rlk_hr_sw_ult46_46"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.0322f,0.9358f,0.3101f],left_rotation:[0.3097f,0.0257f,-0.9487f,0.0575f],scale:[1.0011f,1f,1.9993f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
scoreboard players set #gau hr 0
function rlk:boss/scarlet/fx/hud/ovl {g:"white",in:0,hold:3,out:6}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/ult_burst
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/burst_radial {r:60}
execute at @s run function rlk:boss/scarlet/fx/snd/ult_cut2
