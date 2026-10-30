# slam tick 54 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^0.74 ^1.693 ^2.33 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^0.58 ^1.555 ^2.33 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^0.42 ^1.417 ^2.33 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.87f,0.74f,0.47f],scale:0.7} ^0.26 ^1.28 ^2.33 0.04 0.04 0.04 0 1 force @a[tag=player]
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.35 1.4 0.12
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.45 0.7 0.15
