# Q pattern tick 83
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_on
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/rig/anchor/head
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/star4
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_off
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/a9_star
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4012f,2.2488f,-0.0624f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
