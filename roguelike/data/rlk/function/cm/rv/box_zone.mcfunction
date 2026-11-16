# @s = the fight zone marker: bounding box of its cells' interiors (block coords)
data modify storage rlk:c2e bc set from entity @s data.cells
scoreboard players set #bx0 tmp 2147483647
scoreboard players set #bz0 tmp 2147483647
scoreboard players set #bx1 tmp -2147483648
scoreboard players set #bz1 tmp -2147483648
function rlk:cm/rv/box_cell
# usable only when the spawn spot lies inside that box
scoreboard players set #t1 tmp 100
scoreboard players operation #bx0 tmp *= #t1 tmp
scoreboard players operation #bz0 tmp *= #t1 tmp
scoreboard players operation #bx1 tmp *= #t1 tmp
scoreboard players operation #bz1 tmp *= #t1 tmp
scoreboard players add #bx1 tmp 100
scoreboard players add #bz1 tmp 100
execute if score #px tmp >= #bx0 tmp if score #px tmp < #bx1 tmp if score #pz tmp >= #bz0 tmp if score #pz tmp < #bz1 tmp run scoreboard players set #bOk tmp 1
