# thrust clip tick 14
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-3.934 ^2.851 ^0.751",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.3,s1:1.6,move:"0f,0f,0f",life:6,fade:3}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"glow",pos:"^-3.934 ^2.851 ^0.751",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.5,s1:1.3,move:"0f,0f,0f",life:5,fade:3}
execute at @s rotated as @s rotated ~ 0 positioned ^-3.934 ^2.851 ^0.751 run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.06 8 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 2 0.33
playsound minecraft:block.amethyst_cluster.hit hostile @a[tag=player] ~ ~ ~ 0.5 1.8 0.17
