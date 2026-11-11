# A3 pattern tick 62
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^0.177 ^3.027 ^0.424 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5711f,1.0281f,-0.3185f],left_rotation:[0.3508f,-0.8468f,0.3694f,-0.153f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_54]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_56] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_58] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_60] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_61,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.261f,1.3152f,0.0767f],left_rotation:[0.2061f,0.8822f,-0.2177f,0.3632f],scale:[0.173f,0.18f,2.1663f],right_rotation:[0f,0f,0f,1f]}}
