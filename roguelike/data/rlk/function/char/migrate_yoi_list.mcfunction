# macro: l = rlk:lvpick 의 문자열 목록 이름. 그 목록에서 "char_yoimiya" 를 뺀다(순서는 그대로)
$data modify storage rlk:mig q set from storage rlk:lvpick $(l)
data modify storage rlk:mig out set value []
function rlk:char/migrate_yoi_loop
$data modify storage rlk:lvpick $(l) set from storage rlk:mig out
data remove storage rlk:mig q
data remove storage rlk:mig out
data remove storage rlk:mig cmp
