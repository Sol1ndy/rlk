# slam tick 7 (@s = body, at the body).
# Aim locked: disc r 6 centred 3.5 b ahead (K25 x1.2), ring lead 13 t -> hit on the impact (clip 20).
# Quiet (rule 10-20): the module ring (vis 31) is the only ground telegraph, as in the footage.
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzVis mb 31
scoreboard players set #hzKB mb 3
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:60,tell:13,dmg:160}
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.27
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.5 1.5 0.17
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-0.7 ^0.08 ^1.62 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.65 ^0.08 ^-0.99 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-0.41 ^0.08 ^0.05 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-0.91 ^0.08 ^-0.34 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1 ^0.08 ^1.44 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^0.96 ^0.08 ^1.76 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-1.45 ^0.08 ^-0.95 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.46 ^0.08 ^1.17 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-0.93 ^0.08 ^-0.38 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.6 ^0.08 ^-0.74 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-0.13 ^0.08 ^1.76 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-0.35 ^0.08 ^1.9 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^0.93 ^0.08 ^-1.59 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^0.35 ^0.08 ^-0.01 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^-1.39 ^0.08 ^0.23 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^0.72 ^0.08 ^0.59 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run particle minecraft:dust{color:[0.93f,0.7f,0.27f],scale:0.9} ^1.74 ^0.08 ^0.04 0 0 0 0 1 force @a[tag=player]
