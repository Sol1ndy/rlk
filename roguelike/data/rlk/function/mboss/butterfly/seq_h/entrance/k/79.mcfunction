# entrance tick 79
execute rotated as @s rotated ~ 0 positioned ~ ~2.2 ~ run function rlk:mboss/butterfly/fx/p/cocoon_burst
function rlk:mboss/butterfly/fx/snd/cocoon_burst
particle minecraft:block{block_state:"minecraft:white_stained_glass"} ~ ~2.2 ~ 1.2 1.5 1.2 0 36 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:light_blue_stained_glass"} ~ ~2.2 ~ 1 1.3 1 0 22 force @a[tag=player]
particle minecraft:dust{color:[0.224f,0.706f,0.757f],scale:1.2} ~ ~2.2 ~ 1.2 1.2 1.2 0 12 force @a[tag=player]
