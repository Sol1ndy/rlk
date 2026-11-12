# A9 pattern tick 21
function rlk:boss/scarlet/p/a9/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..9] rotated as @s rotated ~ 0 positioned ^ ^ ^9 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.286f,0.7285f,0.1269f],left_rotation:[-0.6645f,-0.6964f,0.2418f,0.1228f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
