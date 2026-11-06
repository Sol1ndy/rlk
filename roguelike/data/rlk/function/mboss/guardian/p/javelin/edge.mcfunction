# Positioned on the floor, rotated = the lane: #gp2Len += 0.5 b while the next point is inside the walk disc.
scoreboard players add #gp2Len mb 5
execute if score #gp2Len mb matches 440.. run return 0
execute positioned ^ ^ ^0.5 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..21] run function rlk:mboss/guardian/p/javelin/edge
