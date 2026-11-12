# jump clock 34
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"sphere",pos:"^-0.415 ^4.419 ^1.092",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.6,s1:1.3,move:"0f,0f,0f",life:8,fade:2,col:16777215}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"ripple",pos:"^-0.415 ^4.419 ^1.092",rot:"~ ~",bb:"center",roll:0,spin:120,s0:1.2,s1:1.8,move:"0f,0f,0f",life:8,fade:2,col:13957318}
playsound minecraft:block.conduit.activate hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
