# S2 transformation fx, clock 4 (@s = body, at it; the core's p/transform calls it).
# t4 the folded wings open partially: white sparks, a rim glint on each folded wing.
particle minecraft:end_rod ~ ~2.3 ~ 0.3 0.3 0.3 0.05 6 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^0.6 ^2.6 ^-0.3 run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.9,move:"0f,0f,0f",life:3,fade:1,col:15728034}
execute rotated as @s rotated ~ 0 positioned ^-0.6 ^2.6 ^-0.3 run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.9,move:"0f,0f,0f",life:3,fade:1,col:15728034}
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
