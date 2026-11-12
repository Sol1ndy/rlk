# dash clock 4
particle minecraft:dust{color:[0.78f,0.859f,0.459f],scale:0.6} ~ ~1.0 ~ 0.9 0.9 0.9 0 3 force @a[tag=player]
particle minecraft:end_rod ~ ~1.0 ~ 0.8 0.6 0.8 0.02 1 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.965f,0.973f],scale:0.5} ~0 ~1.2 ~1.3 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.965f,0.973f],scale:0.5} ~1.13 ~1.2 ~0.65 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.965f,0.973f],scale:0.5} ~1.13 ~1.2 ~-0.65 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.965f,0.973f],scale:0.5} ~0 ~1.2 ~-1.3 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.965f,0.973f],scale:0.5} ~-1.13 ~1.2 ~-0.65 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.902f,0.965f,0.973f],scale:0.5} ~-1.13 ~1.2 ~0.65 0 0 0 0 1 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.3 1.9 0.1
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"^-0.396 ^1.259 ^0.495",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:1,move:"0f,0f,0f",life:4,fade:2,col:15793910}
