# release clock 53
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
playsound minecraft:entity.warden.sonic_boom hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:2} ~ ~2 ~ 3 1.5 3 0 40 force @a[tag=player]
