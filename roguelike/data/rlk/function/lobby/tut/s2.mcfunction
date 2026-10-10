# 튜토리얼 2단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "2. 기본 공격\n", "color": "#7FD3FF", "bold": true}, {"text": "\n무기를 든 채 좌클릭하면 기본 공격입니다. 캐릭터마다 여러 타로 이어집니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n적 머리 위의 체력 바와 피해 숫자를 보세요. 치명타는 크게 뜹니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n적을 쓰러뜨리면 경험치와 골드를 얻습니다.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 1
data modify storage rlk:lobby tg set value "앞의 허수아비 쓰러뜨리기"
execute positioned 122.5 193 23.5 run function rlk:lobby/tut/target
