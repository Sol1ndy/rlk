# D4 pattern tick 37
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^ ^3.223 ^-0.069 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2525f,1.7396f,0.3615f],left_rotation:[-0.7914f,0f,0f,0.6114f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_35] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_36,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4096f,1.8796f,0.1395f],left_rotation:[-0.388f,-0.6733f,-0.5453f,0.3142f],scale:[0.3277f,0.18f,1.435f],right_rotation:[0f,0f,0f,1f]}}
