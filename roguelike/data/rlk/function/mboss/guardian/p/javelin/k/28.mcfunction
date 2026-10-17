# javelin clip tick 28
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"shard",pos:"^-0.9 ^ ^1.2",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:3.2,s1:3.6,move:"0f,0f,0f",life:3,fade:1}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.9 ^1.5 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:90,s0:0.5,s1:1.6,move:"0f,0f,0f",life:4,fade:2}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.2} ~ ~ ~ 0.05 1.3 0.05 0 24 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.04 1.4 0.04 0 12 force @a[tag=player]
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.7 1.8 0.3
