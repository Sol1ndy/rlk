# 개발자 모드(인벤 정렬 꺼짐): 실물 1개 제거 후 새 아이템 지급. macro: from, to
$data modify storage rlk:pinv obase set from storage rlk:items registry.$(from).item
$data modify storage rlk:pinv ocur set value "$(from)"
function rlk:items/order_replace_dev2 with storage rlk:pinv
$function rlk:items/give {id:"$(to)"}
