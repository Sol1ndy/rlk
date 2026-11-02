scoreboard players operation #t kn = #stun_t kn
scoreboard players operation #t kn %= #c10 kn
execute if score #t kn matches 0 run execute at @s positioned ~ ~2.9 ~ run particle minecraft:crit ~ ~ ~ 0.4 0.2 0.4 0.1 6 force @a[tag=player]
