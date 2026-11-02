# Q5A stage main tick 121
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 6 0.5 6 0 160 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] run playsound minecraft:entity.evoker_fangs.attack hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
