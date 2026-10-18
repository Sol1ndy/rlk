# kick clock 44
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust{color:[0.682f,0.878f,0.545f],scale:1.2} ^ ^0.2 ^3 0.3 0.1 2.5 0 6 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust{color:[0.718f,0.847f,0.686f],scale:1} ^ ^0.2 ^3 0.3 0.1 2.5 0 8 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/p/land
function rlk:mboss/butterfly/fx/snd/land
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.6 0.9 0.2
particle minecraft:poof ~ ~0.1 ~ 0.4 0.05 0.4 0.02 6 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.5 0.05 0.5 0 8 force @a[tag=player]
