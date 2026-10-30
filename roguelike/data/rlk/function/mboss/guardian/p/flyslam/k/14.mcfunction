# flyslam clip tick 14
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c8_1]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5b62,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[-0.077f,9f,-0.077f],left_rotation:[0f,0f,0f,1f],scale:[0.155f,6f,0.155f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5b16,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[-0.02f,9f,-0.02f],left_rotation:[0f,0f,0f,1f],scale:[0.04f,6f,0.04f],right_rotation:[0f,0f,0f,1f]}}
particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:1.4} ~ ~5 ~ 0.2 3.5 0.2 0 20 force @a[tag=player]
function rlk:mboss/guardian/voice/attack
scoreboard players set #mbNoLeash mb 1
particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~1.2 ~ 0.5 0.4 0.5 0 12 force @a[tag=player]
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1.5} ~ ~1.56 ~ 0.3 0.6 0.3 0 5 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~1.36 ~ 0.25 0.4 0.25 0 3 force @a[tag=player]
