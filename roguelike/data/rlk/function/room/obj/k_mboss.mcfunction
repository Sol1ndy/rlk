# 중간보스 구역 오브젝트 (위치 = 실행 위치): 이번에 나올 중간보스를 미리 정해(mboss/roll) 이름을 표시.
# 누르면(oact 14 → mboss/gate) 구역 전투가 시작되고 1.5초 뒤 원형 경기장으로 이동한다
function rlk:mboss/roll
execute unless data storage rlk:mboss cur run return 0
scoreboard players set #oact tmp 14
scoreboard players set #oarg tmp 0
function rlk:room/obj/make_node with storage rlk:mboss cur.gate
