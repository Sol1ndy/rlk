# 튜토리얼 1단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "1. 이동 · 닷지 · 패링\n", "color": "#7FD3FF", "bold": true}, {"text": "\nWASD 로 걷고, 달리기 · 점프는 평소와 같습니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n무기(핫바 1번 칸)를 든 채 우클릭하면 닷지: 이동 방향으로 빠르게 몸을 피합니다. (재사용 대기 0.9초, 공격을 피하면 0.6초)", "color": "#E6E6E6", "bold": false}, {"text": "\n맞기 직전에 피하면 퍼펙트 닷지: 붉은 잔상과 함께 피하고 원소 에너지를 10pt 얻습니다.", "color": "#E6E6E6", "bold": false}, {"text": "\nF 키 = 패링: 공격이 닿기 직전에 누르면 막아 냅니다. 닿기 직전일수록 높은 단계(3단계 = 퍼펙트 패링).", "color": "#E6E6E6", "bold": false}, {"text": "\n공격 · 스킬은 화면 가운데 조준선 쪽으로 나갑니다.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 3
data modify storage rlk:lobby tg set value "닷지 · 패링 3번 하기"
