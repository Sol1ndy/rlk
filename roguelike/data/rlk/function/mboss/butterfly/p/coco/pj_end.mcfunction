# An orb event (@s = orb, at it): a hit pops it at once (one hit per orb, no burst left behind), a wall pops
# it, its life end (40 t) keeps it as a still prop for the burst (p/coco/orb).
execute if score #pjEv mb matches 2 run return run scoreboard players set #pjKeep mb 1
scoreboard players set #pjKeep mb 0
execute if score #pjEv mb matches 1 run return run function rlk:mboss/butterfly/p/coco/pop
execute if score #pjEv mb matches 4 run return run function rlk:mboss/butterfly/p/coco/pop
