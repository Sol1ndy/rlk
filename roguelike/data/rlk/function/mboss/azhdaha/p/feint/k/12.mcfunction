# feint #azPT 12
function rlk:mboss/azhdaha/fx/snd/feint_sway
execute positioned ^3.4 ^0 ^0 positioned ~ ~1.6 ~ run function rlk:mboss/azhdaha/fx/p/dust
execute positioned ^-3.4 ^0 ^0 positioned ~ ~1.6 ~ run function rlk:mboss/azhdaha/fx/p/dust
execute positioned ^3 ^0 ^-1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
execute positioned ^3 ^0 ^1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
execute positioned ^-3 ^0 ^-1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
execute positioned ^-3 ^0 ^1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
