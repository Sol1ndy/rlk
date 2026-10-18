# -> Dendro: the kit's lime pulse (1 card, 10 dust), pale glows at the forewing tips, two leaf puffs.
execute rotated as @s rotated ~ 0 positioned ~ ~2.8 ~ run function rlk:mboss/butterfly/fx/p/dendro_switch
execute rotated as @s rotated ~ 0 positioned ^3.129 ^5.99 ^-1.327 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:2.5,move:"0f,0f,0f",life:5,fade:2,col:15072200}
execute rotated as @s rotated ~ 0 positioned ^-3.129 ^5.99 ^-1.327 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:2.5,move:"0f,0f,0f",life:5,fade:2,col:15072200}
execute rotated as @s rotated ~ 0 positioned ^3.129 ^5.99 ^-1.327 run particle minecraft:composter ~ ~ ~ 0.2 0.2 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.129 ^5.99 ^-1.327 run particle minecraft:composter ~ ~ ~ 0.2 0.2 0.2 0 1 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/dendro_switch
