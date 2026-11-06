# Q2 stage main tick 40
scoreboard players set #q2_sl kn 0
execute at @e[type=minecraft:marker,tag=rlk_kn_q2e,limit=1] if entity @e[tag=rlk_body,limit=1,distance=..6] run scoreboard players set #q2_sl kn 1
