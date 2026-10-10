# 칸마다: 바닥 바꾸기
execute unless data storage rlk:room q[0] run return 0
data modify storage rlk:room it set from storage rlk:room q[0]
data modify storage rlk:room it merge from storage rlk:room th
function rlk:room/wave_fill with storage rlk:room it
execute if data storage rlk:room it.u2 run function rlk:room/wave_fill2 with storage rlk:room it
data remove storage rlk:room q[0]
function rlk:room/floor_cells
