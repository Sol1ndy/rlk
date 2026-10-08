execute unless data storage rlk:room cq[0] run return 0
data modify storage rlk:room ce set from storage rlk:room cq[0]
function rlk:room/gen_cell with storage rlk:room ce
data remove storage rlk:room cq[0]
function rlk:room/gen_cells
