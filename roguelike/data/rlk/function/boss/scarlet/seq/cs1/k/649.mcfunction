# cs1: the timeline at #sq 649 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_a,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:15,transformation:{left_rotation:{angle:-1.1f,axis:[0f,0f,1f]}}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_b,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:15,transformation:{left_rotation:{angle:0.8f,axis:[0f,0f,1f]}}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_a,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1.1 ^0.884 ^1.09 run tp @s ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_b,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.956 ^0.792 ^1.174 run tp @s ~ ~ ~
