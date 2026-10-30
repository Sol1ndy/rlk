# 챕터 보스 문 오브젝트 (위치 = 실행 위치 = 입구 구역 한가운데, @s = 그 구역 표식, data.boss_id 보유)
# 표시 내용은 보스 모듈의 prep(입구를 지을 때)이 rlk:mboss cprep.<boss_id>.gate 에 적어 둔 것: 아이콘 두 개 + 세 줄.
# 누르면(oact 16 → mboss/cb/gate) 구역 전투가 시작되고 1.5초 뒤 그 보스의 경기장으로 이동한다. 저장 내용이 없으면 아무것도 없음
function rlk:room/obj/k_cboss2 with entity @s data
