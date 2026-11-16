# kick clock 16
function rlk:mboss/mv/away {d:0.15}
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.757f,0.969f,0.533f],scale:1} ^0 ^2.756 ^-0.445 0.15 0.2 0.15 0 2 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/p/land
particle minecraft:poof ~ ~0.1 ~ 0.4 0.05 0.4 0.02 6 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.5 0.05 0.5 0 8 force @a[tag=player]
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
