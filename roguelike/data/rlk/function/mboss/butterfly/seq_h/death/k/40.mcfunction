# death tick 40
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
execute positioned ~ ~1.5 ~ run function rlk:mboss/butterfly/fx/p/death_motes
