# Q3 stage whip tick 20
scoreboard players set #q3_k kn 2
execute at @s if entity @e[tag=rlk_body,limit=1,distance=..6] run scoreboard players set #q3_k kn 1
