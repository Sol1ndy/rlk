# H2 달빛 점프 (clip kick_jump; after the core's close-in to 3 b). Sweep r 3 (quiet) 0 -> 10
# (active 4 t, y <= 1.0 b: jumpable), the jump 22 -> 46, the disc r 2.5 locked under the
# player (walk disc) at 32 -> impact 42 (orb 34, kick 39); 0.45 / 0.7 Dendro, 2 hits.
function rlk:mboss/butterfly/rig/face/player
execute at @s rotated as @s rotated ~ 0 positioned ^0.84 ^1.918 ^0.113 run function rlk:mboss/butterfly/fx/p/shard_tell
function rlk:mboss/butterfly/fx/snd/shard_tell
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.722f,0.941f,0.376f],scale:0.9} ^0.84 ^1.918 ^0.113 0.1 0.25 0.1 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run particle minecraft:end_rod ^0.84 ^1.918 ^0.113 0.1 0.2 0.1 0.01 1 force @a[tag=player]
scoreboard players set #hzAct mb 4
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 10
execute positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:30,tell:10,dmg:45}
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.12
