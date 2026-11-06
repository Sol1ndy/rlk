# K stage pl tick 20
kill @e[type=minecraft:marker,tag=rlk_tk_klock]
execute if score #ph tk matches 7 if score #k_2 tk matches 0 run return run function rlk:boss/tachy/p/k/k2
scoreboard players set #done tk 1
