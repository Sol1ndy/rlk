# Q pattern tick 60
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/core/cam_clear
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2537f,0.6805f,0.6125f],left_rotation:[0.1631f,0.0002f,0.0007f,0.9866f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_56] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_58] remove rlk_hr_trr
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^0.254 ^0.627 ^0.769 run function rlk:boss/scarlet/core/sw/rib
