# macro: id → t.<id> 의 항목마다 b = 지금 상수 값 (load 가 막 넣은 너프 전 값)
$data modify storage rlk:tune q set from storage rlk:tune t.$(id)
data modify storage rlk:tune qo set value []
function rlk:items/tune/capture_loop
$data modify storage rlk:tune t.$(id) set from storage rlk:tune qo
