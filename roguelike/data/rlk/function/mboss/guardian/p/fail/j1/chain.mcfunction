# A gold chain step from her chest toward the column top (recursive, <= 30 steps).
scoreboard players add #gp13D mb 1
particle minecraft:dust{color:[0.98f,0.91f,0.56f],scale:1.3} ~ ~ ~ 0.05 0.05 0.05 0 1 force @a[tag=player]
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1} ~ ~ ~ 0.08 0.08 0.08 0 1 force @a[tag=player]
execute if score #gp13D mb matches 30.. run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p13k1,distance=..0.9] run return 0
execute positioned ^ ^ ^0.75 run function rlk:mboss/guardian/p/fail/j1/chain
