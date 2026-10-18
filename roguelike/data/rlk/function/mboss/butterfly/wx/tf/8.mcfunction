# S2 transformation fx, clock 8 (@s = body, at it; the core's p/transform calls it).
# t8 the sphere bursts into ripple rings (kit tf_ripples: a floor ring, two vertical arcs, radial
# speed lines) and a floor dust ring r 3.
execute rotated as @s rotated ~ 0 positioned ~ ~1.6 ~ run function rlk:mboss/butterfly/fx/p/tf_ripples
playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~0 ~0.15 ~3 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~1.15 ~0.15 ~2.77 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~2.12 ~0.15 ~2.12 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~2.77 ~0.15 ~1.15 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~3 ~0.15 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~2.77 ~0.15 ~-1.15 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~2.12 ~0.15 ~-2.12 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~1.15 ~0.15 ~-2.77 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~0 ~0.15 ~-3 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~-1.15 ~0.15 ~-2.77 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~-2.12 ~0.15 ~-2.12 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~-2.77 ~0.15 ~-1.15 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~-3 ~0.15 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~-2.77 ~0.15 ~1.15 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~-2.12 ~0.15 ~2.12 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.741f,0.898f,0.573f],scale:1.2} ~-1.15 ~0.15 ~2.77 0 0 0 0 1 force @a[tag=player]
