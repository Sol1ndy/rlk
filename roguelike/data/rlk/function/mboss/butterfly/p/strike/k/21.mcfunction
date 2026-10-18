# strike clock 21
function rlk:mboss/butterfly/wx/u/fwd {d:0.12}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^1.2 ^3.5 ^-0.5",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.25,move:"0f,-2f,0f",life:16,fade:6,col:13957768}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^-1.5 ^3.0 ^0.4",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.25,move:"0f,-2f,0f",life:16,fade:6,col:13957768}
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.7} ~ ~ ~ 0.3 0.3 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.7} ~ ~ ~ 0.3 0.3 0.3 0 1 force @a[tag=player]
