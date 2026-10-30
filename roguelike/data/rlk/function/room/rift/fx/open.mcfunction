# @s = the anchor (every 2 t): electric sparks on two rim points, an end rod drifting, ink at the edge, reverse portal
# pulled in. The rim points are in the plane facing the player (rotated toward them, pitch 0).
scoreboard players operation #riftP room = @s riftT
scoreboard players operation #riftP room /= #riftC2 room
scoreboard players operation #riftP room %= #riftC4 room
execute facing entity @a[tag=player,limit=1] feet rotated ~ 0 run function rlk:room/rift/fx/rim
particle minecraft:end_rod ~ ~1.45 ~ 0.5 0.8 0.5 0.01 1
particle minecraft:reverse_portal ~ ~1.45 ~ 0.7 1.0 0.7 0.2 2
