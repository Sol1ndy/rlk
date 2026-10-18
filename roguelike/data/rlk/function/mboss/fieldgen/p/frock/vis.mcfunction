# @s = a floor burst (#hzEv 1 = it strikes).
execute unless score #hzEv mb matches 1 run return 0
particle minecraft:block{block_state:"minecraft:tuff"} ~ ~0.3 ~ 0.8 0.3 0.8 0 14 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.698f,0.353f],scale:1.4} ~ ~0.4 ~ 0.6 0.2 0.6 0 6 force @a[tag=player]
playsound minecraft:block.tuff.break hostile @a[tag=player] ~ ~ ~ 1.2 0.5 0.4
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.6 1.1 0.2
