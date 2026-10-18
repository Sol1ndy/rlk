# An orb event (@s = orb): a hit pops it at once; its life end (or a wall) bursts it.
execute if score #pjEv mb matches 4 run scoreboard players set #pjKeep mb 0
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.6} ~ ~ ~ 0.8 0.8 0.8 0 18 force @a[tag=player]
particle minecraft:end_rod ~ ~ ~ 0.3 0.3 0.3 0.1 8 force @a[tag=player]
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
