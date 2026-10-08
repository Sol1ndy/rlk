# macro: h = 보유 목록의 순번
$execute unless data storage rlk:pinv order[$(h)] run return 0
$data modify storage rlk:lvpick b.id set from storage rlk:pinv order[$(h)]
function rlk:invd/tip2_engs with storage rlk:lvpick b
