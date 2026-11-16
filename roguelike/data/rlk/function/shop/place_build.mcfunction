# macro: id. 드롭과 동일한 표시(색이름+lore) + 펼침 텍스트(dfull) 구성
data remove storage rlk:io clickdrop
$data modify storage rlk:io src set from storage rlk:items registry.$(id)
$data modify storage rlk:io id set value "$(id)"
function rlk:items/build_display
data modify storage rlk:io dfull set value []
data modify storage rlk:io dfull append from storage rlk:io name
data modify storage rlk:io lj set from storage rlk:io lore
function rlk:items/drop_lj_loop
function rlk:shop/place_spawn2
