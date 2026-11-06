# whip #azPT 14
execute unless score #aq7S mb matches -1 positioned ^3.6 ^0 ^-3 positioned ~ ~0.6 ~ run function rlk:boss/azhdaha/fx/p/dust
execute unless score #aq7S mb matches -1 positioned ^1.2 ^0 ^-4.6 positioned ~ ~3.0 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.6 0.4 0.6 0 10 force @a[tag=player]
execute if score #aq7S mb matches -1 positioned ^-3.6 ^0 ^-3 positioned ~ ~0.6 ~ run function rlk:boss/azhdaha/fx/p/dust
execute if score #aq7S mb matches -1 positioned ^-1.2 ^0 ^-4.6 positioned ~ ~3.0 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.6 0.4 0.6 0 10 force @a[tag=player]
