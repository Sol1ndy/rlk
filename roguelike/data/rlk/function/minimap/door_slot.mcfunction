# As a door marker on a cell border: which border slot, and how to draw it
# (1 closed / unexplored = grey, 2 open = white; hidden doors are not drawn).
execute unless score @s dst matches 1.. run return 0
scoreboard players operation #ds mm = @s dst
execute if score #ds mm matches 3.. run scoreboard players set #ds mm 2
execute store result score #cx mm run data get entity @s Pos[0]
execute store result score #cz mm run data get entity @s Pos[2]
scoreboard players set #c20 mm 20
scoreboard players operation #mx mm = #cx mm
scoreboard players add #mx mm 60
scoreboard players operation #mx mm %= #c20 mm
# On an x border (a wall between two columns): the slot is the left cell's right side.
execute if score #mx mm matches 0 run scoreboard players remove #cx mm 1
execute unless score #mx mm matches 0 run scoreboard players remove #cz mm 1
function rlk:minimap/cell_index
execute if score #idx mm matches 0.. if score #mx mm matches 0 run function rlk:minimap/set_hd
execute if score #idx mm matches 0.. unless score #mx mm matches 0 run function rlk:minimap/set_vd
