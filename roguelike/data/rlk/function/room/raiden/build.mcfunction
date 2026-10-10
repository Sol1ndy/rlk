# @s = room zone marker. Fixed absolute geometry stays inside normal wipe bounds.
execute if score @s zid matches 1 run function rlk:room/raiden/foyer
execute if score @s zkind matches 9 run function rlk:room/raiden/arena
