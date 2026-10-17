# pull tick 49 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^2.7 ^3.26 ^-0.75",rot:"~ ~",bb:"center",roll:0,spin:60,s0:0.2,s1:1.4,move:"0f,0f,0f",life:8,fade:3}
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.7 0.17
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.35 1.8 0.12
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:0.8} ^1.89 ^2.771 ^-0.525 0.4 0.25 0.3 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^2.7 ^3.26 ^-0.75 0.2 0.2 0.2 0 1 force @a[tag=player]
