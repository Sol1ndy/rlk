# 런 실패 (@s = 죽었다가 부활한 플레이어): 방을 치우고 캐릭터 초기화
function rlk:run/end
function rlk:player/reset_one
title @s times 10 50 20
scoreboard players set @s ttlT 80
title @s subtitle {"text":"처음부터 다시 시작합니다","color":"gray"}
title @s title {"text":"런 실패","color":"#E06A5A","bold":true}
tellraw @s [{"text":"[런] ","color":"red","bold":true},{"text":"쓰러졌습니다. ","color":"gray","bold":false},{"text":"/function rlk:run/start","color":"yellow","bold":false,"click_event":{"action":"suggest_command","command":"/function rlk:run/start"}},{"text":" 로 다시 도전하세요.","color":"gray","bold":false}]
