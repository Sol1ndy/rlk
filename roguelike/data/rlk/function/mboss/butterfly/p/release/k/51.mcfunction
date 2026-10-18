# release clock 51
execute rotated as @s rotated ~ 0 positioned ^0 ^4.811 ^0.415 as @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod] run tp @s ~ ~ ~ ~ ~
execute rotated as @s rotated ~ 0 positioned ^0 ^4.811 ^0.415 run function rlk:mboss/butterfly/fx/card {kind:"burst",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1.5,s1:2.5,move:"0f,0f,0f",life:4,fade:2,col:14678428}
