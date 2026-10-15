# 선택지 #slot 하나의 노드 정하기 → rlk:room cur_nodes → offers[#slot].nodes
data modify storage rlk:room cur_nodes set value []
# 노드 개수: #node2Pct % 확률로 2개
scoreboard players set #nCnt tmp 1
execute store result score #r tmp run random value 0..99
execute if score #r tmp < #node2Pct tmp run scoreboard players set #nCnt tmp 2
# 첫 노드: 앞 선택지들의 첫 노드는 뺀다
data modify storage rlk:room excl set from storage rlk:room used
function rlk:room/node/draw
execute if score #nk tmp matches ..0 run return 0
data modify storage rlk:room used append value 0
execute store result storage rlk:room used[-1] int 1 run scoreboard players get #nk tmp
data modify storage rlk:room cur_nodes append value 0
execute store result storage rlk:room cur_nodes[-1] int 1 run scoreboard players get #nk tmp
# 상점은 혼자 나오지 않는다
execute if score #nk tmp matches 4 run scoreboard players set #nCnt tmp 2
# 둘째 노드: 첫 노드와 다른 것
execute if score #nCnt tmp matches 2 run function rlk:room/node/offer_two
execute store result storage rlk:room a.i int 1 run scoreboard players get #slot tmp
function rlk:room/node/offer_set with storage rlk:room a
