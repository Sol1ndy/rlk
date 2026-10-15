# macro: id = 아이템 id. 그 아이템의 각인마다 byeng.<각인> 에 id 추가
$data modify storage rlk:engravings beq set from storage rlk:items registry.$(id).engravings
function rlk:engravings/byeng_eng_loop
