# E at the spawn (@s = the new body, at it, facing the arriving player; entrance clip tick 0): the folded device
# on the floor, a little tuff dust, the low mechanical hum.
execute positioned ~ 201 ~ run particle minecraft:block{block_state:"minecraft:tuff"} ~ ~0.3 ~ 1.2 0.1 1.2 0 10 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~2.132 ~ run playsound minecraft:block.respawn_anchor.ambient hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
