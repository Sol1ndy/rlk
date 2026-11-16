# S1 at the spawn (@s = the new body, at it, facing the arriving player): the glowing lime floor disc under the
# cocoon until the burst (kit cocoon_disc), its pale rim (refreshed every 20 t), the faint hum, the first hover.
execute positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/p/cocoon_disc {life:80}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"ripple",pos:"^ ^0.05 ^",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:8,s1:8.2,move:"0f,0f,0f",life:20,fade:0,col:12377554}
playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~0 ~0.15 ~1.6 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~0.69 ~0.15 ~1.44 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~1.25 ~0.15 ~1 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~1.56 ~0.15 ~0.36 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~1.56 ~0.15 ~-0.36 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~1.25 ~0.15 ~-1 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~0.69 ~0.15 ~-1.44 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~0 ~0.15 ~-1.6 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~-0.69 ~0.15 ~-1.44 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~-1.25 ~0.15 ~-1 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~-1.56 ~0.15 ~-0.36 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~-1.56 ~0.15 ~0.36 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~-1.25 ~0.15 ~1 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.2} ~-0.69 ~0.15 ~1.44 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:1} ~ ~0.12 ~ 0.7 0.02 0.7 0 4 force @a[tag=player]
particle minecraft:dust_color_transition{from_color:[1f,1f,1f],to_color:[0.553f,0.918f,0.941f],scale:0.8} ~ ~2.2 ~ 1 1.4 1 0 2 force @a[tag=player]
particle minecraft:end_rod ~ ~2.0 ~ 0.9 1.3 0.9 0.01 1 force @a[tag=player]
