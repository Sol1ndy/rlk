# gs 의 아이템 중 보유 목록(rlk:pinv order)에 없는 것만 gq2 로
execute unless data storage rlk:room gs[0] run return 0
data modify storage rlk:room gx.x set from storage rlk:room gs[0]
function rlk:root/give_filter1 with storage rlk:room gx
data remove storage rlk:room gs[0]
function rlk:root/give_filter
