# waves clock 179
execute if score #fgWvK mb matches 2 run playsound minecraft:block.heavy_core.place hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute if score #fgWvK mb matches 2 run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
execute if score #fgWvK mb matches 2 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/dust_puff
