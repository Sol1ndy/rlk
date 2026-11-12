# 바닥에 특수 아이템 드롭 (실행 위치에). 사용: function rlk:items/drop {id:"sealed_sword"}  ({id:"help"}: 아이템 id 목록)
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:items/help {cmd:"drop"}
# 드롭된 아이템은 조준하면 설명이 펼쳐지고, [회수]/[판매] 버튼을 좌클릭해 처리한다 (ditem/)
data remove storage rlk:io src
$data modify storage rlk:io src set from storage rlk:items registry.$(id)
$data modify storage rlk:io id set value "$(id)"
execute if data storage rlk:io src.item run function rlk:items/drop_do
