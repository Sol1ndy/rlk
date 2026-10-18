# Core fx eye (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute at @s run particle minecraft:end_rod ~ ~3.2 ~ 0.3 0.3 0.3 0.02 6 force @a[tag=player]
