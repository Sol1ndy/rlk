# death tick 12
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/p/death_flicker
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
