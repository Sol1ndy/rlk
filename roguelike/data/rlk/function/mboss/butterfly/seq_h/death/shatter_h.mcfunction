# Human form: the crescent plates at her hands crack (navy shards).
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"^-1.05 ^2.92 ^-0.33",rot:"~-60 40",bb:"fixed",roll:0,spin:0,s0:0.4,s1:0.7,move:"0f,0.9f,0f",life:8,fade:4,col:3754869}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"^-1.05 ^2.92 ^-0.33",rot:"~-10 65",bb:"fixed",roll:20,spin:0,s0:0.4,s1:0.7,move:"0f,0.9f,0f",life:8,fade:4,col:3754869}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"^0.84 ^1.95 ^-0.01",rot:"~60 40",bb:"fixed",roll:0,spin:0,s0:0.4,s1:0.7,move:"0f,0.9f,0f",life:8,fade:4,col:3754869}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"^0.84 ^1.95 ^-0.01",rot:"~110 65",bb:"fixed",roll:20,spin:0,s0:0.4,s1:0.7,move:"0f,0.9f,0f",life:8,fade:4,col:3754869}
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
