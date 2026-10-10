# 튜토리얼 3단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "3. 원소전투 스킬\n", "color": "#7FD3FF", "bold": true}, {"text": "\n핫바 2번 칸(스킬)을 들고 클릭하면 원소전투 스킬을 씁니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n쓰고 나면 재사용 대기 시간이 생깁니다. (칸의 숫자)", "color": "#E6E6E6", "bold": false}, {"text": "\n스킬로 적을 맞히면 원소 입자가 나와 원소 에너지를 채웁니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n캐릭터마다 스킬이 다릅니다. 「캐릭터 튜토리얼」에서 자세히 배울 수 있어요.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 1
data modify storage rlk:lobby tg set value "스킬 1번 쓰기"
execute positioned 122.5 193 23.5 run function rlk:lobby/try/dummy_at
tag @e[tag=rlk_dummy,x=122.5,y=193,z=23.5,distance=..0.5] add rlk_tutE
