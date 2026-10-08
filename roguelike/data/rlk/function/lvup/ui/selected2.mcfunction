$execute unless data storage rlk:lvpick choices[$(i)] run return 0
$data modify storage rlk:io id set from storage rlk:lvpick choices[$(i)]
function rlk:lvup/ui/item_load with storage rlk:io
# 고른 것이 캐릭터인가(확인 창의 문구가 달라짐)
execute store success score #pkIsChar tmp if data storage rlk:io src.char
function rlk:lvup/ui/item_big with storage rlk:io
