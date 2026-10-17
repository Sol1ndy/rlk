# flyslam clip tick 17
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c10_1]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5b62,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.31f,0f,-0.31f],left_rotation:[0f,0f,0f,1f],scale:[0.62f,11f,0.62f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5b16,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.08f,0f,-0.08f],left_rotation:[0f,0f,0f,1f],scale:[0.16f,11f,0.16f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^ ^2.1 ^",rot:"~ ~",bb:"fixed",roll:180,spin:-160,s0:2.6,s1:3.4,move:"0f,0f,0f",life:5,fade:2}
particle minecraft:end_rod ~ ~4 ~ 0.15 2.5 0.15 0.05 14 force @a[tag=player]
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.9 1.3 0.3
playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
