# @s = a follower that reached the landed lead: red/black shards and an ember.
particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~ ~ 0.15 0.15 0.15 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~ ~ 0.15 0.15 0.15 0 2 force @a[tag=player]
particle minecraft:dust{color:[0.99f,0.33f,0.33f],scale:0.9} ~ ~ ~ 0.1 0.1 0.1 0 2 force @a[tag=player]
kill @s
