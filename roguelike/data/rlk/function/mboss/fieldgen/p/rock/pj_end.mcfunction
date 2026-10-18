# A thrown slab ends (#pjEv 1 floor / wall, 2 life): it shatters. A hit (4) lets it fly on (default, harmless).
execute if score #pjEv mb matches 1..2 at @s run particle minecraft:block{block_state:"minecraft:tuff"} ~ ~ ~ 0.6 0.3 0.6 0 16 force @a[tag=player]
execute if score #pjEv mb matches 1..2 at @s run playsound minecraft:block.tuff.break hostile @a[tag=player] ~ ~ ~ 1.2 0.6 0.4
execute if score #pjEv mb matches 1..2 run scoreboard players set #pjKeep mb 0
