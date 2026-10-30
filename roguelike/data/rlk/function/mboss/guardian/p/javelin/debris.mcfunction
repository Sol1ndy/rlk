# @s = body, on the floor under the lane: rock and gold debris every 2 b.
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.1 ~ 0.4 0.05 0.4 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:polished_blackstone"} ~ ~0.1 ~ 0.4 0.05 0.4 0 2 force @a[tag=player]
scoreboard players add #gp2S mb 20
execute if score #gp2S mb < #gp2Len mb positioned ^ ^ ^2 run function rlk:mboss/guardian/p/javelin/debris
