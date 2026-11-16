# @s = room zone marker (room/zone_build). Fixed absolute geometry inside the zone cells (zone 1 strips cover
# the dome). The foyer starts the sliced backdrop job; the arena builds the walk square at once.
execute if score @s zid matches 1 run function rlk:room/raiden/foyer
execute if score @s zkind matches 9 run function rlk:room/raiden/arena
