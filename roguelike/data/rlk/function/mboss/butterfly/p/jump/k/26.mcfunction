# jump clock 26
function rlk:mboss/butterfly/rig/face/track
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~-0.48 ~1.7 ~-1.32 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~0.48 ~1.7 ~1.32 0 0 0 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"ripple",pos:"^ ^2.4 ^",rot:"~ ~",bb:"center",roll:0,spin:170,s0:1.5,s1:3,move:"0f,0f,0f",life:8,fade:3,col:11197316}
