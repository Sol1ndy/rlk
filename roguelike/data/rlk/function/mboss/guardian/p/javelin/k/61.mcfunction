# javelin clip tick 61
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s,limit=1] at @s run particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:1.1} ~ ~ ~ 0.1 0.1 0.1 0 4 force @a[tag=player]
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s,limit=1] at @s run particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[tag=player]
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]}}
