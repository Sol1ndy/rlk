# 런 중단 (@s = 플레이어). 사용: /function rlk:run/stop  — 방을 치우고 시작했던 자리로 돌아감
execute unless score #active room matches 1 run return run tellraw @s {"text":"[런] 진행 중인 런이 없습니다.","color":"gray"}
function rlk:run/end
function rlk:run/tp_back with storage rlk:room ret
tellraw @s [{"text":"[런] ","color":"gold","bold":true},{"text":"런을 중단했습니다.","color":"gray","bold":false}]
