# 선택지 하나 (위치 = 실행 위치, macro: i = choices 의 순번)
$execute unless data storage rlk:lvpick choices[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:lvpick choices[$(i)]
$scoreboard players set #pkIdx tmp $(i)
scoreboard players set #pkKind tmp 1
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io
