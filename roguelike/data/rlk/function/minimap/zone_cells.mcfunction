# As a zone marker: mark every cell of its record.
scoreboard players operation #zid mm = @s zid
data modify storage rlk:mm q set from entity @s data.cells
function rlk:minimap/cells_loop
