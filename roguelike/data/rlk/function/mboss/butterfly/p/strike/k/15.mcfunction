# strike clock 15
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
playsound minecraft:block.cherry_leaves.break hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.3} ^ ^1.5 ^1.5 1.5 0.6 0.6 0 16 force @a[tag=player]
