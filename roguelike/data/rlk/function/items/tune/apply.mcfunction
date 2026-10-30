# macro: id → 그 아이템의 조정 상수를 강화 단계(<id> enhL)에 맞춰 다시 계산하고, 설명 숫자 캐시(rlk:items disp.<id>)를 새로 만든다
$scoreboard players operation #enh tmp = $(id) enhL
function rlk:items/tune/fac
$data modify storage rlk:tune q set from storage rlk:tune t.$(id)
function rlk:items/tune/apply_loop
$function rlk:items/tune/disp_build {id:"$(id)"}
