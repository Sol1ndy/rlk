# A thrown slab ends: 1 floor / wall, 2 life -> it shatters (slab_impact on the floor under it); 4 = it hit the
# player: one more slab hit toward the cap (2); the slab flies on, harmless (its group struck).
execute if score #pjEv mb matches 4 run scoreboard players add #fq12SH mb 1
execute if score #pjEv mb matches 1..2 at @s positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/slab_impact
execute if score #pjEv mb matches 1..2 at @s run function rlk:mboss/fieldgen/fx/snd/slab_impact
execute if score #pjEv mb matches 1..2 run scoreboard players set #pjKeep mb 0
