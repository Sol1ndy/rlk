# kick clock 2
function rlk:mboss/butterfly/rig/face/track
particle minecraft:poof ~ ~0.1 ~ 0.25 0.02 0.25 0.02 2 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"^-0.342 ^0.407 ^-0.166",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.2,s1:0.6,move:"0f,0f,0f",life:4,fade:2,col:15072200}
