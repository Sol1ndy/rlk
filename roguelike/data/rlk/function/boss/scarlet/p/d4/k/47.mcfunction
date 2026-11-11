# D4 pattern tick 47
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^0.153 ^3.076 ^0.246 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4236f,0.9486f,-0.074f],left_rotation:[-0.6093f,0.6434f,-0.3589f,0.2932f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_41] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_43] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_45] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_46,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.068f,1.0513f,0.1967f],left_rotation:[0.1914f,0.5643f,0.0029f,0.8031f],scale:[0.7493f,0.26f,2.0054f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_46,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0459f,1.0254f,0.1943f],left_rotation:[0.1594f,0.7107f,-0.0018f,0.6852f],scale:[0.7449f,0.26f,1.9946f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_46,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0934f,0.995f,0.158f],left_rotation:[0.1217f,0.8313f,-0.0065f,0.5423f],scale:[0.718f,0.26f,1.9229f],right_rotation:[0f,0f,0f,1f]}}
