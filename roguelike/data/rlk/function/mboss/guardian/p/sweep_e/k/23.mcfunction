# sweep_e clip tick 23
execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p12h,scores={mbHzHit=1..}] run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_gd_p12h] mbHzHit 1
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w2]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w6] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.984f,0.01f,0.04f]}}
