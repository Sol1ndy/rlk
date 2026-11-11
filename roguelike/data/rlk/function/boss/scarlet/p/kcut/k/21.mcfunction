# KCUT pattern tick 21
execute store result storage rlk:hr core.sw.d double 0.5 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m22,limit=1] ~ ~1.950 ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_kcut22_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_swn","rlk_hr_sw_kcut22_21"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.1327f,0.7306f,0.0738f],left_rotation:[0.6982f,-0.0785f,0.7109f,0.0305f],scale:[0.8236f,1f,2.1847f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_swn","rlk_hr_sw_kcut22_21"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.0852f,0.719f,0.0276f],left_rotation:[0.5548f,-0.0714f,0.8277f,0.0445f],scale:[0.8685f,1f,2.3044f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_swn","rlk_hr_sw_kcut22_21"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.123f,0.6779f,0.0045f],left_rotation:[0.3922f,-0.0618f,0.916f,0.0569f],scale:[0.8761f,1f,2.3246f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_swn","rlk_hr_sw_kcut22_21"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.0449f,0.6091f,0.1216f],left_rotation:[0.2161f,-0.0502f,0.9727f,0.0674f],scale:[0.8454f,1f,2.2427f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_arc_0","minecraft:custom_model_data":{colors:[14857471]}}}}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ 0
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line with storage rlk:hr core.dash
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/kcut
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated ~0 0 positioned ^ ^ ^-6 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:120,w:16,tell:1,dmg:61}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/kcut
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated ~55 0 positioned ^ ^ ^-6 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:120,w:16,tell:1,dmg:61}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/kcut
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated ~-55 0 positioned ^ ^ ^-6 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:120,w:16,tell:1,dmg:61}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/kcut
