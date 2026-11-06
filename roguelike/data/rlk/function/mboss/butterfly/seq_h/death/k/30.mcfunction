# death tick 30
particle minecraft:poof ~ ~0.2 ~ 0.5 0.05 0.5 0.02 8 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.6 0.05 0.6 0 10 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0 ~0.15 ~1 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0.5 ~0.15 ~0.87 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0.87 ~0.15 ~0.5 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~1 ~0.15 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0.87 ~0.15 ~-0.5 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0.5 ~0.15 ~-0.87 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~0 ~0.15 ~-1 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-0.5 ~0.15 ~-0.87 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-0.87 ~0.15 ~-0.5 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-1 ~0.15 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-0.87 ~0.15 ~0.5 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.9} ~-0.5 ~0.15 ~0.87 0 0 0 0 1 force @a[tag=player]
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.27
playsound minecraft:entity.iron_golem.step hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
