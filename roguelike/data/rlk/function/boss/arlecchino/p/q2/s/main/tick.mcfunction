# Q2 stage main: one tick (#q2_c 1..).
execute if score #q2_c kn matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #q2_c kn matches 21..31 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1,distance=..0.8] at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/p/q2/burst
execute if score #q2_c kn matches 6 run function rlk:boss/arlecchino/p/q2/s/main/k/6
execute if score #q2_c kn matches 14 run function rlk:boss/arlecchino/p/q2/s/main/k/14
execute if score #q2_c kn matches 20 run function rlk:boss/arlecchino/p/q2/s/main/k/20
execute if score #q2_c kn matches 21 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #q2_c kn matches 23 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #q2_c kn matches 25 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #q2_c kn matches 27 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #q2_c kn matches 29 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #q2_c kn matches 31 as @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #q2_c kn matches 33 run function rlk:boss/arlecchino/p/q2/s/main/k/33
execute if score #q2_c kn matches 34 run function rlk:boss/arlecchino/p/q2/s/main/k/34
execute if score #q2_c kn matches 35 at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
execute if score #q2_c kn matches 36 at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
execute if score #q2_c kn matches 37 at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
execute if score #q2_c kn matches 38 at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
execute if score #q2_c kn matches 39 at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
execute if score #q2_c kn matches 40 run function rlk:boss/arlecchino/p/q2/s/main/k/40
execute if score #q2_c kn matches 41 run function rlk:boss/arlecchino/p/q2/s/main/k/41
execute if score #q2_c kn matches 42 if score #q2_sl kn matches 1 run function rlk:boss/arlecchino/p/q2/f/slash_fx
execute if score #q2_c kn matches 48 run return run function rlk:boss/arlecchino/p/q2/s/main/k/48
execute if score #q2_c kn matches 70 run return run function rlk:boss/arlecchino/p/q2/s/main/k/70
