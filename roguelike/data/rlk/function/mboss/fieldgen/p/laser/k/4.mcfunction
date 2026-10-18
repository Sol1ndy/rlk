# laser clock 4
execute at @s rotated as @s run particle minecraft:electric_spark ^2.8 ^2.2 ^ 0.2 0.2 0.2 0.05 3 force @a[tag=player]
execute at @s rotated as @s run particle minecraft:electric_spark ^-2.8 ^2.2 ^ 0.2 0.2 0.2 0.05 3 force @a[tag=player]
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.7 1.8 0.23
