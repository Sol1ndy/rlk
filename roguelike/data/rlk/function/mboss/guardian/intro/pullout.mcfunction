playsound minecraft:block.chain.break hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
playsound minecraft:block.stone.break hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run particle minecraft:block{block_state:"minecraft:gold_block"} ~ 201.2 ~ 0.3 0.1 0.3 0 10 force @a[tag=player]
