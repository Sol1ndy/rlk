# 튜토리얼 1단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "1. 이동과 대쉬\n", "color": "#7FD3FF", "bold": true}, {"text": "\nWASD 로 걷고, 달리기 · 점프는 평소와 같습니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n무기(핫바 1번 칸)를 든 채 우클릭하면 대쉬! 대쉬하는 동안은 무적입니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n대쉬는 2번까지 모아 둘 수 있고 1초마다 1번씩 다시 찹니다. (액션바의 청록 칸)", "color": "#E6E6E6", "bold": false}, {"text": "\n숄더뷰에서는 화면 가운데 조준선 쪽으로 공격 · 스킬이 나갑니다.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 3
data modify storage rlk:lobby tg set value "대쉬 3번 하기"
