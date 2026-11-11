# A10 pattern tick 21
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 1
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:35,tell:1,dmg:54}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/a10
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0636f,0.6901f,0.6556f],left_rotation:[0.1662f,0.0001f,0.0006f,0.9861f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_19] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_20,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0132f,1.2984f,0.6867f],left_rotation:[-0.3118f,-0.3117f,-0.6346f,0.6346f],scale:[0.5796f,0.26f,1.6995f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_20,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0396f,1.1985f,0.5784f],left_rotation:[-0.2008f,-0.2008f,-0.678f,0.678f],scale:[0.6043f,0.26f,1.7721f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_20,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.066f,1.1579f,0.4841f],left_rotation:[-0.0841f,-0.0841f,-0.7021f,0.7021f],scale:[0.6215f,0.26f,1.8227f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a10","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a10_21","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.0752f,1.0892f,-0.4982f],left_rotation:[-0.0247f,-0.0242f,-0.7064f,0.707f],scale:[0f,0.26f,2.8037f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16773806]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a10","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_a10_21","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.0671f,1.0883f,-0.4917f],left_rotation:[-0.0247f,-0.0242f,-0.7062f,0.7072f],scale:[0f,0.26f,2.8004f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16773806]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.064 ^0.636 ^0.811 run function rlk:boss/scarlet/core/sw/rib
