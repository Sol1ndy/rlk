# @s = zone marker, positioned at the zone centre, rotated toward the player (snapped): one set of lines per
# row size (1..3), boxes 1.5 b apart, dropped from the player's left to right.
execute if score #mbPk mb matches 1 run function rlk:mboss/box/drop
execute if score #mbPk mb matches 2 positioned ^-0.75 ^ ^ run function rlk:mboss/box/drop
execute if score #mbPk mb matches 2 positioned ^0.75 ^ ^ run function rlk:mboss/box/drop
execute if score #mbPk mb matches 3 positioned ^-1.5 ^ ^ run function rlk:mboss/box/drop
execute if score #mbPk mb matches 3 run function rlk:mboss/box/drop
execute if score #mbPk mb matches 3 positioned ^1.5 ^ ^ run function rlk:mboss/box/drop
