# Q6 stage main tick 30
execute at @s positioned ~ ~4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.6 1.6 1.6 0 60 force @a[tag=player]
execute at @s run playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
