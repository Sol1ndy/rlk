# pull tick 53 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4ca10] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,1.9f,0f],left_rotation:[0f,-0.9903f,0f,-0.1392f],scale:[-13.7113f,13.7113f,13.7113f],right_rotation:[0f,0f,0f,1f]}}
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 0.85 0.2
