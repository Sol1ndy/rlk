# 튜토리얼 7단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "7. 원소 반응 실습\n", "color": "#7FD3FF", "bold": true}, {"text": "\n앞의 더미에는 내 캐릭터의 원소와 반응하는 원소가 붙어 있습니다. (2초마다 다시 붙음)", "color": "#E6E6E6", "bold": false}, {"text": "\n기본 공격이나 스킬로 때려서 반응을 일으켜 보세요!", "color": "#E6E6E6", "bold": false}, {"text": "\n바람 캐릭터면 확산, 바위 캐릭터면 결정이 일어납니다.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 1
data modify storage rlk:lobby tg set value "원소 반응 일으키기"
execute positioned 122.5 193 23.5 run function rlk:lobby/try/dummy_at
tag @e[tag=rlk_dummy,x=122.5,y=193,z=23.5,distance=..0.5] add rlk_tutE
function rlk:lobby/tut/aura
