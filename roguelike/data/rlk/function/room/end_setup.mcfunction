# 마지막 구역 (@s = 구역 표식, at @s): 다음 맵 선택 오브젝트. 4번째 맵까지는 노드가 붙은 선택지 3개(room/node/offers), 그 다음은 보스전
execute if score #mapIdx room matches 4.. run return run function rlk:room/end_boss
function rlk:room/node/offers
