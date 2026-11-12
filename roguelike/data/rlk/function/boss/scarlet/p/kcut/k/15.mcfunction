# KCUT pattern tick 15
function rlk:boss/scarlet/p/kcut/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..7] rotated as @s rotated ~ 0 positioned ^ ^ ^7 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2742f,0.7812f,-0.139f],left_rotation:[-0.954f,0.0204f,0.0667f,0.2917f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
