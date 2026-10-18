# S2 transformation fx, clock 5 (@s = body, at it; the core's p/transform calls it).
# t5 the core flash: a yellow-white flare at her chest.
execute rotated as @s rotated ~ 0 positioned ^0 ^2.2 ^0 run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.4,s1:2,move:"0f,0f,0f",life:3,fade:1,col:16448724}
particle minecraft:dust{color:[0.98f,0.988f,0.831f],scale:1.6} ~ ~2.2 ~ 0.15 0.15 0.15 0 12 force @a[tag=player]
