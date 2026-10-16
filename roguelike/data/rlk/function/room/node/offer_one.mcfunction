# 선택지 #slot 하나의 노드 정하기 → rlk:room cur_nodes → offers[#slot].nodes
# 세 선택지에 같은 노드가 두 번 나오지 않는다(used = 이번 선택지들에 이미 나온 노드). 이번 챕터에 고른 노드(seen)도 빼되, 후보가 없을 때만 다시 허용
data modify storage rlk:room cur_nodes set value []
# 노드 개수: #node2Pct % 확률로 2개
scoreboard players set #nCnt tmp 1
execute store result score #r tmp run random value 0..99
execute if score #r tmp < #node2Pct tmp run scoreboard players set #nCnt tmp 2
# 첫 노드
function rlk:room/node/draw_fresh
execute if score #nk tmp matches ..0 run return 0
function rlk:room/node/take
# 상점은 혼자 나오지 않는다
execute if score #nk tmp matches 4 run scoreboard players set #nCnt tmp 2
# 둘째 노드
execute if score #nCnt tmp matches 2 run function rlk:room/node/offer_two
execute store result storage rlk:room a.i int 1 run scoreboard players get #slot tmp
function rlk:room/node/offer_set with storage rlk:room a
