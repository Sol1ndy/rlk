# The player touched it (@s = orb, at it): heal, sparkle, gone.
execute as @a[tag=player,limit=1] run function rlk:mboss/butterfly/dew/heal
particle minecraft:dust{color:[0.929f,0.976f,0.855f],scale:1.4} ~ ~ ~ 0.4 0.4 0.4 0 16 force @a[tag=player]
particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.12 10 force @a[tag=player]
particle minecraft:happy_villager ~ ~ ~ 0.4 0.4 0.4 0 6 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 1.9 0.33
playsound minecraft:block.amethyst_cluster.hit hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
scoreboard players remove #bfDewN mb 1
kill @s
