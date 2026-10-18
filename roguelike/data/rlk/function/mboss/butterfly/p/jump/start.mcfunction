# H2 달빛 점프 (clip kick_jump; after the core's close-in to 3 b). Sweep r 3 decal 3 -> 13
# (active 4 t, y <= 1.0 b: jumpable), the jump 33 -> 55, the disc r 2.5 locked under the
# player (walk disc) at 38 -> impact 50 (orb 40, kick 47); 0.9 / 1.4 Dendro, 2 hits.
function rlk:mboss/butterfly/rig_stub/face/player
execute at @s rotated as @s rotated ~ 0 positioned ^0.62 ^2.6 ^0.1 run function rlk:mboss/butterfly/fx/p/shard_tell
function rlk:mboss/butterfly/fx/snd/shard_tell
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.722f,0.941f,0.376f],scale:0.9} ^0.62 ^2.6 ^0.1 0.1 0.25 0.1 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run particle minecraft:end_rod ^0.62 ^2.6 ^0.1 0.1 0.2 0.1 0.01 1 force @a[tag=player]
