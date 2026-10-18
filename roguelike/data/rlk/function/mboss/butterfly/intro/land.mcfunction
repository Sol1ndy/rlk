# Landing crouch: soft thud, moss dust, a lime floor ring.
particle minecraft:poof ~ ~0.15 ~ 0.6 0.05 0.6 0.03 10 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.7 0.05 0.7 0 14 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0 ~0.15 ~1.3 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0.65 ~0.15 ~1.13 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~1.13 ~0.15 ~0.65 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~1.3 ~0.15 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~1.13 ~0.15 ~-0.65 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0.65 ~0.15 ~-1.13 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0 ~0.15 ~-1.3 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-0.65 ~0.15 ~-1.13 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-1.13 ~0.15 ~-0.65 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-1.3 ~0.15 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-1.13 ~0.15 ~0.65 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-0.65 ~0.15 ~1.13 0 0 0 0 1 force @a[tag=player]
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
playsound minecraft:entity.iron_golem.step hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
