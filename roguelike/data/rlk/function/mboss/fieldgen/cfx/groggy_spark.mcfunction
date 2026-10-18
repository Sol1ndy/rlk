# Core fx groggy_spark (vanilla particles / sounds; @s = body unless noted).
execute at @s run particle minecraft:electric_spark ~ ~2.6 ~ 0.8 0.6 0.8 0.05 4 force @a[tag=player]
execute at @s run playsound minecraft:block.chain.hit hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
