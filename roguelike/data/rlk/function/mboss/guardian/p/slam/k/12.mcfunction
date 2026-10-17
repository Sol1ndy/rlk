# slam tick 12 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.26 ^6.82 ^0.3",rot:"~ ~",bb:"center",roll:0,spin:90,s0:0.1,s1:1.1,move:"0f,0f,0f",life:6,fade:3}
execute rotated as @s rotated ~ 0 run particle minecraft:end_rod ^-0.26 ^6.82 ^0.3 0.1 0.1 0.1 0.04 3 force @a[tag=player]
