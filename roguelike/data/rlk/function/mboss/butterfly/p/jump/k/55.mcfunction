# jump clock 55
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust{color:[0.659f,0.875f,0.455f],scale:3} ~ ~1 ~ 1.2 0.8 1.2 0 4 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust{color:[0.553f,0.753f,0.494f],scale:3.5} ~ ~1 ~ 1.2 0.8 1.2 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/p/land
function rlk:mboss/butterfly/fx/snd/land
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
particle minecraft:poof ~ ~0.1 ~ 0.4 0.05 0.4 0.02 6 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.5 0.05 0.5 0 8 force @a[tag=player]
