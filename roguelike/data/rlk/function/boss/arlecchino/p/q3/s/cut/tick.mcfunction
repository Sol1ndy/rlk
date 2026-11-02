# Q3 stage cut: one tick (#q3_c 1..).
execute if score #q3_c kn matches 1..12 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.2}
execute if score #q3_c kn matches 1..6 run function rlk:mboss/mv/turn {max:12}
execute if score #q3_c kn matches 16..28 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #q3_c kn matches 15..24 run function rlk:mboss/mv/turn {max:14}
execute if score #q3_c kn matches 31..40 run function rlk:mboss/mv/turn {max:14}
execute if score #q3_c kn matches 13 run function rlk:boss/arlecchino/p/q3/s/cut/k/13
execute if score #q3_c kn matches 14 run function rlk:boss/arlecchino/p/q3/s/cut/k/14
execute if score #q3_c kn matches 29 run function rlk:boss/arlecchino/p/q3/s/cut/k/29
execute if score #q3_c kn matches 30 run function rlk:boss/arlecchino/p/q3/s/cut/k/30
execute if score #q3_c kn matches 46 run function rlk:boss/arlecchino/p/q3/s/cut/k/46
execute if score #q3_c kn matches 47 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 49 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 51 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 52 run return run function rlk:boss/arlecchino/p/q3/s/cut/k/52
execute if score #q3_c kn matches 53 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 55 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 57 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 59 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 61 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 63 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 65 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
execute if score #q3_c kn matches 67 as @e[tag=rlk_kn_p_q3,tag=rlk_kn_cres] at @s run particle minecraft:flame ~ ~ ~ 0.6 0.15 0.6 0.02 5 force @a[tag=player]
