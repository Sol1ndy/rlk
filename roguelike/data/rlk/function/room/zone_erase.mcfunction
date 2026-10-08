# 구역 지우기 (@s = 구역 표식): 칸마다 구덩이(y 186~198) · 바닥판 복구 · 방(y 200~210)
execute unless data entity @s data.cells run return run function rlk:room/zone_erase_old with entity @s data
data modify storage rlk:room q set from entity @s data.cells
function rlk:room/erase_cells
