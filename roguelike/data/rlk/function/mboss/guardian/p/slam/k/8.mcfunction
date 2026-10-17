# slam tick 8 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p3ring] run data merge entity @s {start_interpolation:0,interpolation_duration:11,transformation:{translation:[0f,0f,0f],left_rotation:[-0.4056f,0.5792f,0.5792f,0.4056f],scale:[13.9535f,13.9535f,13.9535f],right_rotation:[0f,0f,0f,1f]}}
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.7 1.5 0.23
