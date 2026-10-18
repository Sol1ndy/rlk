# release clock 96
# the landing in human form (the core: groggy next)
function rlk:mboss/butterfly/fx/p/land
function rlk:mboss/butterfly/fx/snd/land
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
particle minecraft:poof ~ ~0.15 ~ 0.6 0.05 0.6 0.03 8 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.7 0.05 0.7 0 10 force @a[tag=player]
function rlk:mboss/butterfly/p/end
