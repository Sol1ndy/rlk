# 로노바 원소전투 스킬 (@s = 플레이어, at 몸). 좌클릭 = 사형 선고(재사용 대기), 우클릭 = 재연(잔향 소모, 2초 간격)
execute if score #skBtn tmp matches 2 run return run function rlk:char/ronova/replay
execute if score @s skillCd matches 1.. run return run function rlk:char/deny {t:"원소전투 스킬 재사용 대기 중"}
function rlk:char/ronova/doom
