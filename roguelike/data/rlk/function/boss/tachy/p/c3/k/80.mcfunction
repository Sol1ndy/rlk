# C3 pattern tick 80
function rlk:mboss/mv/face
function rlk:boss/tachy/rig_stub/look/edge/glint
execute at @s rotated as @s rotated ~ 0 positioned ^-0.4 ^1.6 ^1.4 run particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.02 6 force @a[tag=player]
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.8 1.6 0.27
playsound minecraft:item.trident.return hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
