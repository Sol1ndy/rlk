# 인벤 칸 하나 (macro: i = 보유 목록의 순번). 비어 있으면 아무것도 두지 않음
$execute unless data storage rlk:pinv order[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:pinv order[$(i)]
$scoreboard players set #pkIdx tmp $(i)
scoreboard players set #pkKind tmp 2
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/item_el with storage rlk:io
