# kick clock 10
function rlk:mboss/mv/away {d:0.15}
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.757f,0.969f,0.533f],scale:1} ^ ^2.6 ^-0.4 0.15 0.2 0.15 0 2 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^0.3 ^2.1 ^-0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.4,move:"0f,-1.2f,0.4f",life:12,fade:6,col:11067252}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^0.55 ^2.1 ^-0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.4,move:"0f,-1.2f,0.4f",life:12,fade:6,col:11067252}
