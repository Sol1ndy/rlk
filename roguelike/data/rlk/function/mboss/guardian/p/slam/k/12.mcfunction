# slam tick 12 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.26 ^6.82 ^0.3",rot:"~ ~",bb:"center",roll:0,spin:90,s0:0.2,s1:1.8,move:"0f,0f,0f",life:9,fade:3}
execute rotated as @s rotated ~ 0 run particle minecraft:end_rod ^-0.26 ^6.82 ^0.3 0.1 0.1 0.1 0.04 3 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 2 0.3
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:0.8} ^-0.26 ^6.22 ^0.3 0.12 0.4 0.12 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-0.26 ^6.82 ^0.3 0.2 0.3 0.2 0 1 force @a[tag=player]
