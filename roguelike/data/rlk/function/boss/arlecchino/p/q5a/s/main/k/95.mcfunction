# Q5A stage main tick 95
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 2.7 0.4 2.7 0 80 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] positioned ~ 201 ~ run particle minecraft:explosion ~ ~ ~ 2 0.3 2 0 4 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] run playsound minecraft:entity.wither.break_block hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
