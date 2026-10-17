# slam tick 42 (@s = body, at the body).
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p3cb]
execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^0.226 ^1.223 ^3.049",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.05,s1:0.6885,move:"0f,0f,0f",life:7,fade:3}
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:end_rod ~ ~0.8 ~ 0.25 0.6 0.25 0.01 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.9 0.3
