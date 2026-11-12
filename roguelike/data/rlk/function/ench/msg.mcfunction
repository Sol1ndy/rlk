# macro: id → 강화 결과 안내
$data modify storage rlk:io src set from storage rlk:items registry.$(id)
$data modify storage rlk:io id set value "$(id)"
data remove storage rlk:io clickdrop
function rlk:items/build_display
title @s actionbar [{"text":"강화: ","color":"#B58BE8"},{"nbt":"name","storage":"rlk:io","interpret":true}]
scoreboard players set @s hudHold 20
