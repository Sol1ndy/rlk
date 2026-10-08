# macro: i = 고른 선택지, j = 내려놓을 보유 아이템. 왼쪽 = 내려놓을 것, 오른쪽 = 얻을 것
$execute unless data storage rlk:pinv order[$(j)] run return 0
$execute unless data storage rlk:lvpick choices[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:pinv order[$(j)]
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/swapconf_old with storage rlk:io
$data modify storage rlk:io id set from storage rlk:lvpick choices[$(i)]
function rlk:lvup/ui/item_load with storage rlk:io
function rlk:lvup/ui/swapconf_new with storage rlk:io
