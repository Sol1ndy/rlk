# entrance tick 82
particle minecraft:dust_color_transition{from_color:[1f,1f,1f],to_color:[0.224f,0.706f,0.757f],scale:1} ~ ~4.5 ~ 1.5 1 1.5 0 6 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/cocoon_tail
particle minecraft:wax_off ~ ~1.0 ~ 1.6 0.6 1.6 0 2 force @a[tag=player]
particle minecraft:end_rod ~ ~3.0 ~ 1 0.6 1 0.01 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^-0.4 ^3.6 ^0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.35,move:"0f,-2f,0f",life:14,fade:6,col:11067252}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^0.4 ^3.6 ^0.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.35,move:"0f,-2f,0f",life:14,fade:6,col:11067252}
function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"~-0.37 ~0.25 ~0.51",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.2,s1:0.6,move:"0f,0f,0f",life:4,fade:2,col:16777215}
