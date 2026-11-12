# macro: it = 캐릭터 아이템 id -> 그 캐릭터 id 로 한 줄
$data modify storage rlk:help r.id set from storage rlk:items registry.$(it).char
function rlk:help/row with storage rlk:help r
