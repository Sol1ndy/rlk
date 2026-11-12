# [c_rocks] A thrown slab (mbId 6): an undodged hit (#pjEv 4) counts toward the cap of 2 (it then flies on,
# harmless); on the floor or a wall (1) or at its life end (2) it shatters.
execute if score #pjEv mb matches 4 unless score #dodged tmp matches 1 run scoreboard players add #fq6SH mb 1
execute if score #pjEv mb matches 1..2 at @s positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/slab_impact
execute if score #pjEv mb matches 1..2 at @s run function rlk:mboss/fieldgen/fx/snd/slab_impact
execute if score #pjEv mb matches 1..2 run scoreboard players set #pjKeep mb 0
