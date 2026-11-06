# recover tick 30
function rlk:mboss/butterfly/fx/snd/chain_reform
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.1} ^0.7 ^1.8 ^ 0.3 0.5 0.3 0 10 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"^0.84 ^1.98 ^0.1",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.4,s1:1,move:"0f,0f,0f",life:6,fade:2,col:12771724}
