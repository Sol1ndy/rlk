# 선택지 #slot 의 오브젝트 (위치 = 놓을 자리). 노드가 둘이면 아이콘 둘 + 이름 "A + B"
execute store result storage rlk:room a.i int 1 run scoreboard players get #slot tmp
function rlk:room/node/spawn2 with storage rlk:room a
