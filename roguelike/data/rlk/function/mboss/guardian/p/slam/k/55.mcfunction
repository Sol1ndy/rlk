# slam tick 55 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^-1.192 ^4.865 ^2.797 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^-0.905 ^4.86 ^2.755 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^-0.618 ^4.855 ^2.712 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^-0.33 ^4.85 ^2.67 0.04 0.04 0.04 0 1 force @a[tag=player]
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.35 1.4 0.3
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.45 0.7 0.3
