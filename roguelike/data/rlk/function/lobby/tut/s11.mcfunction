# 튜토리얼 11단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "튜토리얼 완료!\n", "color": "#7FD3FF", "bold": true}, {"text": "\n수고했어요! 로비에서 캐릭터를 고르고 「게임 시작」을 누르면 런이 시작됩니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n캐릭터마다 따로 배울 수 있어요: 「캐릭터 튜토리얼」 (캐릭터는 「캐릭터 바꾸기」로)", "color": "#E6E6E6", "bold": false}, {"text": "\n「캐릭터 · 아이템 체험」 방에서는 모든 캐릭터와 아이템을 미리 써 볼 수 있습니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n「시작 전 설정」 방에서 숄더뷰 · 카메라를 바꿀 수 있어요.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 0
data modify storage rlk:lobby tg set value ""
