# A3 pattern tick 23
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^1.044 ^2.081 ^-0.836 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5201f,1.5603f,-0.3507f],left_rotation:[-0.8184f,0.339f,-0.1776f,0.4287f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_15]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_17] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_21] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_22,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2673f,1.3009f,-0.0935f],left_rotation:[-0.3326f,0.803f,0.1892f,0.4569f],scale:[0.234f,0.22f,2.0404f],right_rotation:[0f,0f,0f,1f]}}
