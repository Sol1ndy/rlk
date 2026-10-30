# groggy tick 280
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"^0.55 ^2.35 ^-0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.2,s1:0.7,move:"0f,0f,0f",life:4,fade:2,col:15072200}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"^-0.55 ^2.35 ^-0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.2,s1:0.7,move:"0f,0f,0f",life:4,fade:2,col:15072200}
playsound minecraft:entity.breeze.idle_air hostile @a[tag=player] ~ ~ ~ 0.3 1 0.1
