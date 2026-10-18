# Core fx flip (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.crafter.craft hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
execute at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
execute at @s run particle minecraft:end_rod ~ ~4.6 ~ 0.4 0.3 0.4 0.02 6 force @a[tag=player]
