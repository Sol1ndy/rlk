# macro: id → 그 아이템을 팔아 더는 가진 것이 없으면 강화 단계를 지운다(다시 얻으면 ☆☆☆부터). 바닥에 떨군 것은 지우지 않음
$execute if data storage rlk:pinv {order:["$(id)"]} run return 0
$execute unless data storage rlk:pinv enh.$(id) run return 0
$data remove storage rlk:pinv enh.$(id)
$scoreboard players reset $(id) enhL
$execute if data storage rlk:tune t.$(id) run function rlk:items/tune/apply {id:"$(id)"}
