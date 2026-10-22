# 노드 선택지를 고름 (@s = 오브젝트 표식). 그 선택지의 노드 → rlk:room next, 노드 맵(종류 1)으로
execute store result storage rlk:room a.i int 1 run scoreboard players get @s oarg
function rlk:room/node/choose2 with storage rlk:room a
# 고른 사이에 쓸모가 없어진 노드는 뺀다(이 맵에서 기적을 받음 · 보유 칸이 18칸이 됨). 다 빠지면 골드
function rlk:room/node/validate
# 이번 챕터에 고른 노드는 다음 선택지에 나오지 않는다
data modify storage rlk:room sq set from storage rlk:room next
function rlk:room/node/seen_loop
scoreboard players set #mapType room 1
function rlk:run/next_map
