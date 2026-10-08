# cid가 이미 뽑힌 목록(picked) 또는 플레이어 보유 목록(pinv order)에 있으면 #dup=1 (macro: cid)
$execute if data storage rlk:pick {picked:["$(cid)"]} run scoreboard players set #dup tmp 1
$execute if data storage rlk:pinv {order:["$(cid)"]} run scoreboard players set #dup tmp 1
