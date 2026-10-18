# Landing crouch: soft thud, moss dust, a mint ripple with drifting leaves (kit land).
function rlk:mboss/butterfly/fx/p/land
particle minecraft:poof ~ ~0.15 ~ 0.6 0.05 0.6 0.03 10 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.7 0.05 0.7 0 14 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/land
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
