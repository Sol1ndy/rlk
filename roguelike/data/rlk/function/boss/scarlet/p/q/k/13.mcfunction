# Q pattern tick 13
function rlk:boss/scarlet/p/q/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..15.6] rotated as @s rotated ~ 0 positioned ^ ^ ^15.6 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4048f,0.6665f,0.0278f],left_rotation:[-0.525f,0.6557f,-0.4741f,0.2638f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
