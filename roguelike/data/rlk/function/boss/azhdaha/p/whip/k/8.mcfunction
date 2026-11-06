# whip #azPT 8
execute unless score #aq7S mb matches -1 at @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] run function rlk:boss/azhdaha/p/whip/l/8
execute if score #aq7S mb matches -1 at @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] run function rlk:boss/azhdaha/p/whip/r/8
execute unless score #aq7S mb matches -1 positioned ^3.6 ^0 ^-3 positioned ~ ~0.6 ~ run function rlk:boss/azhdaha/fx/p/dust
execute unless score #aq7S mb matches -1 positioned ^1.2 ^0 ^-4.6 positioned ~ ~3.0 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.6 0.4 0.6 0 10 force @a[tag=player]
execute if score #aq7S mb matches -1 positioned ^-3.6 ^0 ^-3 positioned ~ ~0.6 ~ run function rlk:boss/azhdaha/fx/p/dust
execute if score #aq7S mb matches -1 positioned ^-1.2 ^0 ^-4.6 positioned ~ ~3.0 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.6 0.4 0.6 0 10 force @a[tag=player]
