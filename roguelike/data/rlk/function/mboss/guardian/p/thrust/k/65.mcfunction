# thrust clip tick 65
playsound minecraft:block.amethyst_block.fall hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.3
execute at @s rotated as @s rotated ~ 0 run particle minecraft:block{block_state:"minecraft:calcite"} ^ ^0.1 ^0.6 0.5 0.05 0.5 0 8 force @a[tag=player]
