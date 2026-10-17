# slam tick 45 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.216 ^0.912 ^3.592",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.05,s1:0.6327,move:"0f,0f,0f",life:7,fade:3}
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:end_rod ~ ~0.8 ~ 0.25 0.6 0.25 0.01 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.4 2 0.13
