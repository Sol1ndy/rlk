# kick clock 6
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated ~ 0 positioned ^ ^0.5 ^1.0 run function rlk:mboss/butterfly/fx/p/glint
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.9 0.17
