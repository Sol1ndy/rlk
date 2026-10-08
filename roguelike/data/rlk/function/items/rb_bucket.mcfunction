# cur 아이템의 등급을 읽어 해당 버킷에 추가 (macro: cur)
$data modify storage rlk:rb rar set from storage rlk:items registry.$(cur).rarity
function rlk:items/rb_put with storage rlk:rb
