execute unless data storage rlk:mm q[0] run return 0
execute store result score #cx mm run data get storage rlk:mm q[0].x0
execute store result score #cz mm run data get storage rlk:mm q[0].z0
function rlk:minimap/cell_index
function rlk:minimap/set_g
data remove storage rlk:mm q[0]
function rlk:minimap/cells_loop
