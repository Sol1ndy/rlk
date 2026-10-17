# flyslam clip tick 36
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_2]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_8]
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1.3} ~ ~9.88 ~ 0.25 0.35 0.25 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~9.48 ~ 0.2 0.3 0.2 0 2 force @a[tag=player]
particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~10.68 ~ 0.3 0.3 0.3 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5t,limit=1] run function rlk:fx/nv/card {kind:"star",pos:"~0.456 ~7.762 ~-0.951",rot:"~ ~",bb:"center",roll:0,spin:90,s0:0.32,s1:0.55,move:"0f,-7.3619f,0f",life:9,fade:2}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5t,limit=1] run particle minecraft:falling_dust{block_state:"minecraft:gold_block"} ~ ~7 ~ 1.6 0.8 1.6 0 4 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5t,limit=1] run particle minecraft:end_rod ~ ~5 ~ 0.8 1.5 0.8 0 1 force @a[tag=player]
