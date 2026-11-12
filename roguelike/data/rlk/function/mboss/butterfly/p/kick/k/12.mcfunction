# kick clock 12
function rlk:mboss/mv/away {d:0.15}
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.757f,0.969f,0.533f],scale:1} ^0 ^2.756 ^-0.445 0.15 0.2 0.15 0 2 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"cres_lime",pos:"^ ^1.4 ^",rot:"~ -90",bb:"fixed",roll:90,spin:-150,s0:1.6,s1:2.4,move:"0f,0f,0f",life:4,fade:2,col:12579217}
