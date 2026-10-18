# Core fx clank (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.anvil.place hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.23
execute at @s run playsound minecraft:block.chain.place hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @s run playsound minecraft:block.piston.extend hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.27
execute at @s run particle minecraft:crit ~ ~2 ~ 1 0.4 1 0.1 8 force @a[tag=player]
