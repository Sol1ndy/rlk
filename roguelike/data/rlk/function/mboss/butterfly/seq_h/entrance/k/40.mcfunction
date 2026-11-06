# entrance tick 40
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^ ^2.0 ^",rot:"~244 0",bb:"fixed",roll:-3,spin:90,s0:1.5,s1:2.5,move:"0f,0f,0f",life:6,fade:2,col:15136504}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"ripple",pos:"^ ^0.05 ^",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:8,s1:8.2,move:"0f,0f,0f",life:20,fade:0,col:12377554}
execute positioned ~ ~2.0 ~ run function rlk:mboss/butterfly/fx/p/motes
playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
