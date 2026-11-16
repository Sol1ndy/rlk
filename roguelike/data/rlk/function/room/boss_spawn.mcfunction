# 모든 스테이지의 임시 공통 보스: 나루카미. 위치 = 원형 필드 중앙.
# 챕터 보스 구역(data.cboss): 그 보스의 경기장 전투(mboss/cb/spawn_route), 나루카미로 넘어가지 않음
execute if data entity @s data.cboss run return run function rlk:mboss/cb/spawn_route
execute if entity @e[tag=rlk_raiden_arena,limit=1] at @e[tag=rlk_raiden_arena,limit=1] run return run function rlk:boss/raiden/spawn
function rlk:boss/raiden/spawn
