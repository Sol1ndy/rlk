# flyslam clip tick 21
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5t,limit=1] run function rlk:fx/nv/card {kind:"glow",pos:"~ ~0.04 ~",rot:"0 90",bb:"fixed",roll:0,spin:0,s0:11,s1:11,move:"0f,0f,0f",life:10,fade:0}
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1.3} ~ ~9.812 ~ 0.25 0.35 0.25 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~9.412 ~ 0.2 0.3 0.2 0 2 force @a[tag=player]
particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~10.612 ~ 0.3 0.3 0.3 0 2 force @a[tag=player]
