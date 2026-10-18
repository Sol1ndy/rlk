# Core fx groggy (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
execute at @s run particle minecraft:smoke ~ ~2 ~ 0.8 0.5 0.8 0.01 10 force @a[tag=player]
