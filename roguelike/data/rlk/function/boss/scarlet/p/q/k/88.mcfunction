# Q pattern tick 88
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/p/q/lockp
execute if score #q_hit hr matches 1 at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:boss/scarlet/fx/p/sky_mark
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4001f,2.259f,-0.0675f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
