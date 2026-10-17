# slam tick 9 (@s = body, at the body).
# Aim locked: disc r 5 centred 3.5 b ahead (K25), ring lead 17 t -> hit on the impact (clip 26).
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 31
scoreboard players set #hzKB mb 3
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:50,tell:17,dmg:160}
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.27
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.5 1.5 0.17
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.92 ^0.08 ^-3.29 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^0.72 ^0.08 ^-0.02 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-2.87 ^0.08 ^0.48 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.49 ^0.08 ^1.21 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^3.59 ^0.08 ^0.08 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-2.16 ^0.08 ^-3.16 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-1.36 ^0.08 ^2.99 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-2.31 ^0.08 ^-2.83 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.52 ^0.08 ^-0.53 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-1.63 ^0.08 ^2.19 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.62 ^0.08 ^0.32 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^0.29 ^0.08 ^2.65 0 0 0 0 1 force @a[tag=player]
