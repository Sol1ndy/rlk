# 구역 전체의 바닥을 '들어가 본 구역' 블록으로 (@s = 구역 표식)
data modify storage rlk:room q set from entity @s data.cells
function rlk:room/floor_cells
