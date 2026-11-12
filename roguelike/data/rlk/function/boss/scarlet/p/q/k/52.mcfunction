# Q pattern tick 52
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/p/q/lockp
execute if score #q_hit hr matches 1 at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_on
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^-0.001 ^3.953 ^0.472 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_off
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0324f,1.7973f,0.4117f],left_rotation:[-0.4639f,-0.4639f,0.5337f,-0.5337f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_44]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_46] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_48] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_50] remove rlk_hr_trr
