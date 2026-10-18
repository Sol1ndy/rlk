particle minecraft:explosion ~ ~ ~ 0.2 0.1 0.2 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.698f,0.353f],scale:1.3} ~ ~0.2 ~ 0.6 0.1 0.6 0 6 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.17
kill @s
