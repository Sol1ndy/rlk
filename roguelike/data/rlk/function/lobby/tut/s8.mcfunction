# 튜토리얼 8단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "8. 원소 에너지와 원소폭발\n", "color": "#7FD3FF", "bold": true}, {"text": "\n원소 에너지(액션바 가운데 게이지)가 가득 차면 원소폭발을 쓸 수 있습니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n핫바 3번 칸(원소폭발)을 들고 클릭하면 발동!", "color": "#E6E6E6", "bold": false}, {"text": "\n에너지는 주로 스킬로 만든 원소 입자로 채웁니다. 내 캐릭터와 같은 원소의 입자일수록 많이 찹니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n이번에는 에너지를 가득 채워 두었습니다.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 1
data modify storage rlk:lobby tg set value "원소폭발 1번 쓰기"
execute positioned 122.5 193 23.5 run function rlk:lobby/try/dummy_at
tag @e[tag=rlk_dummy,x=122.5,y=193,z=23.5,distance=..0.5] add rlk_tutE
scoreboard players operation @s energy = #burstCost100 tmp
scoreboard players set @s burstCd 0
