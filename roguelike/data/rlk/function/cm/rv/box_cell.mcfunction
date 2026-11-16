execute unless data storage rlk:c2e bc[0] run return 0
execute store result score #t1 tmp run data get storage rlk:c2e bc[0].ix0
scoreboard players operation #bx0 tmp < #t1 tmp
execute store result score #t1 tmp run data get storage rlk:c2e bc[0].ix1
scoreboard players operation #bx1 tmp > #t1 tmp
execute store result score #t1 tmp run data get storage rlk:c2e bc[0].iz0
scoreboard players operation #bz0 tmp < #t1 tmp
execute store result score #t1 tmp run data get storage rlk:c2e bc[0].iz1
scoreboard players operation #bz1 tmp > #t1 tmp
data remove storage rlk:c2e bc[0]
function rlk:cm/rv/box_cell
