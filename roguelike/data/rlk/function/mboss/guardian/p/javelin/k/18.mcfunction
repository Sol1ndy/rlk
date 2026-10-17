# javelin clip tick 18
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:dust{color:[0.969f,0.918f,0.663f],scale:0.55} ~ ~ ~ 0.35 0.35 0.35 0 3 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.9 0.17
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p2bar] store result entity @s transformation.scale[2] float 0.1 run scoreboard players get #gp2Len mb
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p2bar] run data merge entity @s {start_interpolation:0,interpolation_duration:9}
