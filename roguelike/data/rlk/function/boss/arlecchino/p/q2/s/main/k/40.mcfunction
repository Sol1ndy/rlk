# Q2 stage main tick 40
execute at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
scoreboard players set #q2_sl kn 0
execute at @e[type=minecraft:marker,tag=rlk_kn_q2e,limit=1] if entity @e[tag=rlk_body,limit=1,distance=..6] run scoreboard players set #q2_sl kn 1
