# 노드 선택지를 고름 (@s = 오브젝트 표식). 그 선택지의 노드 → rlk:room next, 노드 맵(종류 1)으로
execute store result storage rlk:room a.i int 1 run scoreboard players get @s oarg
function rlk:room/node/choose2 with storage rlk:room a
scoreboard players set #mapType room 1
function rlk:run/next_map
