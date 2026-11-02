# Q5B stage main tick 96
scoreboard players set #bolw kn 1
execute at @s positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 3.38 0.6 3.38 0 200 force @a[tag=player]
execute at @s positioned ~ 201 ~ run particle minecraft:explosion ~ ~ ~ 3 0.4 3 0 6 force @a[tag=player]
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s run playsound minecraft:entity.wither.break_block hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
