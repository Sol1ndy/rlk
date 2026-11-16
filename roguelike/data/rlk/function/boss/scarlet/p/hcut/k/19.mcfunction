# HCUT pattern tick 19
function rlk:boss/scarlet/p/hcut/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..13] rotated as @s rotated ~ 0 positioned ^ ^ ^13 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.402f,0.5095f,-0.0203f],left_rotation:[-0.5643f,0.6491f,-0.4262f,0.2805f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
