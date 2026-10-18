# @s = an eruption disc (#hzEv 1 = it erupts): gold eruption 3.5 b tall, rock chunks.
execute unless score #hzEv mb matches 1 run return 0
particle minecraft:dust{color:[0.902f,0.698f,0.353f],scale:1.8} ~ ~1.5 ~ 1 1.4 1 0 14 force @a[tag=player]
particle minecraft:dust{color:[0.992f,0.984f,0.82f],scale:1.2} ~ ~0.5 ~ 1.4 0.3 1.4 0 8 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:tuff"} ~ ~0.5 ~ 1 0.5 1 0 16 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
playsound minecraft:block.basalt.break hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
