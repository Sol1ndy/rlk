# 튜토리얼 10단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "10. 던전 진행\n", "color": "#7FD3FF", "bold": true}, {"text": "\n던전은 여러 구역으로 나뉜 맵입니다. 구역에 들어가면 문이 닫히고 적이 나오며,", "color": "#E6E6E6", "bold": false}, {"text": "\n모두 쓰러뜨리면 문이 열립니다. 왼손의 지도에 구역과 문(흰 점)이 보입니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n구멍(낙사 구간)에 떨어지면 체력이 깎이고 떨어지기 전 자리로 돌아옵니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n마지막 구역에서는 다음 맵(전투 · 상점 · 보물 등)을 고릅니다. 챕터 끝에는 보스가 있어요.", "color": "#E6E6E6", "bold": false}, {"text": "\n쓰러지면 런이 끝나고 처음부터 다시 시작합니다. 사파이어는 런이 끝나도 남습니다.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 0
data modify storage rlk:lobby tg set value ""
