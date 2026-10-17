# flyslam clip tick 33
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_0]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_5]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_6]
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1.3} ~ ~9.866 ~ 0.25 0.35 0.25 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~9.466 ~ 0.2 0.3 0.2 0 2 force @a[tag=player]
particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~10.666 ~ 0.3 0.3 0.3 0 2 force @a[tag=player]
