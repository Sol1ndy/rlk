# One try (recursive): a random cell, a random point inside its walls (>= 3 b from a wall face), the ground, the check.
scoreboard players add #riftTry room 1
execute if score #riftTry room matches 25.. run return 0
function rlk:room/mob_cell with entity @s data
function rlk:room/mob_cell2 with storage rlk:room a
function rlk:room/rift/spot/range
execute if score #riftRg room matches 1 run function rlk:room/rift/spot/at with storage rlk:room rsp
execute if score #riftWay room matches 1 run return 1
function rlk:room/rift/spot/try
