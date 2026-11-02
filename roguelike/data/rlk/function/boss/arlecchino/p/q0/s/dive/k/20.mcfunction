# Q0 stage dive tick 20
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run particle minecraft:explosion ~ ~ ~ 0.75 0.1 0.75 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.2 0.2 1.2 0 24 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.5 0.5 0.17
