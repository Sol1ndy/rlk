# @s = a missile decal (#hzEv 1 = its impact).
execute unless score #hzEv mb matches 1 run return 0
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.2 ~ 0.5 0.1 0.5 0 8 force @a[tag=player]
