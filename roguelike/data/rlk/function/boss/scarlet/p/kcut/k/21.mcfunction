# KCUT pattern tick 21
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
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2787f,0.7198f,0.5266f],left_rotation:[-0.4156f,0.3954f,0.5721f,-0.5862f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_17] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_19] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_20,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1238f,0.7259f,0.0776f],left_rotation:[0.7011f,-0.0416f,0.7096f,0.0562f],scale:[0.7474f,0.26f,1.9768f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_20,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0654f,0.6954f,0.0404f],left_rotation:[0.5565f,-0.0466f,0.8282f,0.0464f],scale:[0.7827f,0.26f,2.0722f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_20,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.1098f,0.6545f,0.0132f],left_rotation:[0.3923f,-0.05f,0.9178f,0.0351f],scale:[0.7918f,0.26f,2.0981f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_20,tag=rlk_hr_tr_i3] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0547f,0.6054f,0.0922f],left_rotation:[0.2144f,-0.0517f,0.9751f,0.0225f],scale:[0.7736f,0.26f,2.0507f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_kcut_21","rlk_hr_tr_i0"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.0098f,0.5875f,0.3517f],left_rotation:[0.1221f,-0.0543f,0.9909f,0.017f],scale:[0f,0.26f,1.8477f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16773806]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_kcut_21","rlk_hr_tr_i1"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.0113f,0.6434f,0.3572f],left_rotation:[-0.1216f,-0.0469f,0.9914f,0.0115f],scale:[0f,0.26f,1.8454f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16773806]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_kcut","rlk_hr_trr","rlk_hr_trf","rlk_hr_tr_kcut_21","rlk_hr_tr_i2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.0657f,0.6967f,0.4472f],left_rotation:[-0.358f,-0.0374f,0.9329f,0.0053f],scale:[0f,0.26f,1.7856f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_fan_0","minecraft:custom_model_data":{colors:[16773806]}}}}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.434 ^0.714 ^0.583 run function rlk:boss/scarlet/core/sw/rib
