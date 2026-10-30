# The plant (clip tick 14): gold pillar, ground ring, radial crystal blades, the start line.
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ run function rlk:fx/nv/card {kind:"burst",pos:"^ ^1.2 ^",rot:"~ ~",bb:"center",roll:0,spin:20,s0:0.8,s1:3.2,move:"0f,0f,0f",life:6,fade:3}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ run function rlk:fx/nv/card {kind:"ring",pos:"^ ^0.1 ^",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:0.8,s1:7.68,move:"0f,0f,0f",life:9,fade:4}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.6} ^ ^1.5 ^ 0.15 1.6 0.15 0 24 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ run particle minecraft:block{block_state:"minecraft:gold_block"} ^ ^0.3 ^ 1.68 0.2 1.68 0 24 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~0 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -25",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~45 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -40",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~90 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -25",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~135 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -40",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~180 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -25",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~225 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -40",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~270 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -25",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ rotated ~315 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^ ^1.68",rot:"~ -40",bb:"fixed",roll:0,spin:0,s0:0.2,s1:1.1,move:"0f,0f,0f",life:12,fade:5}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.27
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run playsound minecraft:item.trident.thunder hostile @a[tag=player] ~ ~ ~ 0.3 1.2 0.1
function rlk:mboss/guardian/voice/start
