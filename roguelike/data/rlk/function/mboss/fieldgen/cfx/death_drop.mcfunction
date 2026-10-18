# Core fx death_drop (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
execute at @s run playsound minecraft:block.chain.break hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @s run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.5 ~ 2 0.2 2 0 20 force @a[tag=player]
