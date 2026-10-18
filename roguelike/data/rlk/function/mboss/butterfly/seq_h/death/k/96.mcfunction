# death tick 96
particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.6 0.3 0.18 20 force @a[tag=player]
particle minecraft:dust{color:[0.929f,0.976f,0.855f],scale:1.6} ~ ~1.6 ~ 0.6 1 0.6 0 16 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"^ ^1.2 ^",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:2.5,move:"0f,0f,0f",life:6,fade:3,col:15072200}
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.8 2 0.27
