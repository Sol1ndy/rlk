# A3 pattern tick 50
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^ ^3.221 ^-0.048 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1054f,1.6821f,0.3626f],left_rotation:[-0.8241f,0f,0f,0.5664f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_42]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_46] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_48] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_49,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2507f,1.8345f,0.2383f],left_rotation:[-0.1323f,-0.8223f,-0.5465f,0.0879f],scale:[0.3135f,0.22f,1.435f],right_rotation:[0f,0f,0f,1f]}}
