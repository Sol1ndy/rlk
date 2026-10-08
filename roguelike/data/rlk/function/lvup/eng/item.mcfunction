# 아이템(id)의 각인마다 obj 스코어 +1 (macro: id, obj)
$data modify storage rlk:lvpick xq set from storage rlk:items registry.$(id).engravings
function rlk:lvup/eng/item_loop
