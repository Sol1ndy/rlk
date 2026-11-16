# entrance tick 85
particle minecraft:wax_off ~ ~1.0 ~ 1.6 0.6 1.6 0 2 force @a[tag=player]
particle minecraft:end_rod ~ ~3.0 ~ 1 0.6 1 0.01 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^-0.4 ^3.6 ^0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.35,move:"0f,-2f,0f",life:14,fade:6,col:11067252}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^0.4 ^3.6 ^0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.35,move:"0f,-2f,0f",life:14,fade:6,col:11067252}
function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"~0.02 ~0.25 ~0.66",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.2,s1:0.6,move:"0f,0f,0f",life:4,fade:2,col:16777215}
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
