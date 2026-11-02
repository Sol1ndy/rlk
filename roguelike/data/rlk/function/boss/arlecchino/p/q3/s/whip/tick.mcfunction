# Q3 stage whip: one tick (#q3_c 1..).
execute if score #q3_c kn matches 1..10 run function rlk:mboss/mv/turn {max:30}
execute if score #q3_c kn matches 15..20 run function rlk:mboss/mv/turn {max:20}
execute if score #q3_c kn matches 13 run function rlk:boss/arlecchino/p/q3/s/whip/k/13
execute if score #q3_c kn matches 14 run function rlk:boss/arlecchino/p/q3/s/whip/k/14
execute if score #q3_c kn matches 20 run function rlk:boss/arlecchino/p/q3/s/whip/k/20
execute if score #q3_c kn matches 26 if score #q3_k kn matches 2 run function rlk:boss/arlecchino/p/q3/f/far
execute if score #q3_c kn matches 27 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 29 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 31 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 33 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 35 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 36 run return run function rlk:boss/arlecchino/p/q3/s/whip/k/36
execute if score #q3_c kn matches 37 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 39 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 41 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 43 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 45 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 47 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
