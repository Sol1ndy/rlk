# macro: id, n → "◆ 이름  n개" 한 줄
$data modify storage rlk:eng cur set from storage rlk:engravings registry.$(id)
$data modify storage rlk:eng cur.n set value $(n)
function rlk:engravings/info_head with storage rlk:eng cur
