# slam tick 24 (@s = body, at the body).
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:wax_on ~ ~0.8 ~ 1.4 0.6 1.4 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:dust{color:[0.86f,0.78f,0.45f],scale:1.1} ~ ~0.4 ~ 1.92 0.3 1.92 0 4 force @a[tag=player]
execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^0.175 ^1.003 ^3.115",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.05,s1:0.5085,move:"0f,0f,0f",life:7,fade:3}
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:end_rod ~ ~0.8 ~ 0.25 0.6 0.25 0.01 2 force @a[tag=player]
