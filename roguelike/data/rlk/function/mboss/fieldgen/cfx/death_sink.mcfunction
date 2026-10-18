# Core fx death_sink (vanilla particles / sounds; @s = body unless noted).
execute at @s run playsound minecraft:block.anvil.place hostile @a[tag=player] ~ ~ ~ 0.9 0.4 0.3
execute at @s run playsound minecraft:entity.iron_golem.damage hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
execute at @s run particle minecraft:poof ~ ~0.5 ~ 2 0.2 2 0.02 16 force @a[tag=player]
