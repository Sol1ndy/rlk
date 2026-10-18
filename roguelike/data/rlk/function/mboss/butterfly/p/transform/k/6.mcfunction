# transform clock 6
execute rotated as @s rotated ~ 0 positioned ~ ~1.6 ~ run function rlk:mboss/butterfly/fx/p/tf_sphere
function rlk:mboss/butterfly/fx/snd/transform_swell
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~0 ~1.6 ~2.5 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~1.25 ~1.6 ~2.17 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~2.17 ~1.6 ~1.25 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~2.5 ~1.6 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~2.17 ~1.6 ~-1.25 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~1.25 ~1.6 ~-2.17 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~0 ~1.6 ~-2.5 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~-1.25 ~1.6 ~-2.17 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~-2.17 ~1.6 ~-1.25 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~-2.5 ~1.6 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~-2.17 ~1.6 ~1.25 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.973f,0.992f,0.733f],scale:1.4} ~-1.25 ~1.6 ~2.17 0 0 0 0 1 force @a[tag=player]
