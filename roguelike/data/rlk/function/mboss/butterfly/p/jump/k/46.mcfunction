# jump clock 46
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/p/land
function rlk:mboss/butterfly/fx/snd/land
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
particle minecraft:poof ~ ~0.1 ~ 0.4 0.05 0.4 0.02 6 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.5 0.05 0.5 0 8 force @a[tag=player]
