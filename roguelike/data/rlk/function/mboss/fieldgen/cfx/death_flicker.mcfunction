# Core fx death_flicker (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
execute at @s run particle minecraft:electric_spark ~ ~4 ~ 1.5 0.4 1.5 0.1 8 force @a[tag=player]
