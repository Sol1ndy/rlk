# Butterfly form: the wings shatter into lime / opal shards (kit wing_shatter at her back).
particle minecraft:block{block_state:"minecraft:lime_stained_glass"} ~ ~3.0 ~ 1.8 1 0.6 0 30 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:white_stained_glass"} ~ ~3.0 ~ 1.6 1 0.6 0 16 force @a[tag=player]
particle minecraft:dust{color:[0.831f,0.973f,0.776f],scale:1.4} ~ ~3.0 ~ 2 1.2 0.8 0 20 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^ ^2.8 ^-0.4 run function rlk:mboss/butterfly/fx/p/wing_shatter
function rlk:mboss/butterfly/fx/snd/wing_shatter
