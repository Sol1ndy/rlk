# 칸마다: 바닥·벽
execute unless data storage rlk:room q[0] run return 0
data modify storage rlk:room it set from storage rlk:room q[0]
data modify storage rlk:room it merge from storage rlk:room th
function rlk:room/zb_cell with storage rlk:room it
data remove storage rlk:room q[0]
function rlk:room/zb_cells
