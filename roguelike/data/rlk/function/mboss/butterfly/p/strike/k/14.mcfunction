# strike clock 14
execute rotated as @s rotated ~ 0 positioned ^4.669 ^3.847 ^-0.822 run particle minecraft:dust{color:[0.906f,0.992f,0.667f],scale:0.8} ~ ~ ~ 0.2 0.2 0.2 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^1.131 ^7.776 ^-0.822 run particle minecraft:dust{color:[0.906f,0.992f,0.667f],scale:0.8} ~ ~ ~ 0.2 0.2 0.2 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^ ^0.8 ^-1.0",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:2.5,s1:3,move:"0f,0f,0f",life:3,fade:1,col:15203754}
