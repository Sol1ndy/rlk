# 공허 반응 (공허 + 다른 원소 n). macro: e(소모할 부착 원소), n(다른 원소 번호). 반응 번호 #rx = 16 + n
$function rlk:element/use {e:"$(e)",m:100}
$scoreboard players set #rvN tmp $(n)
scoreboard players operation #rx tmp = #rvN tmp
scoreboard players add #rx tmp 16
$function rlk:element/void/rx_$(n)
function rlk:element/void/echo_rx
