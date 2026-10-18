# kick clock 40
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.4} ^ ^0.3 ^3 0.8 0.2 2.5 0 18 force @a[tag=player]
