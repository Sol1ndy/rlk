# jump clock 7
function rlk:mboss/butterfly/rig/face/track
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^ ^0.1 ^0.3",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1.2,s1:1.6,move:"0f,0f,0f",life:3,fade:1,col:12120160}
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
