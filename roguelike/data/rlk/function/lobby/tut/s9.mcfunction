# 튜토리얼 9단계 준비 (@s = 플레이어)
data modify entity @e[tag=rlk_tutp,limit=1] text set value [{"text": "9. 레벨 · 아이템 · 각인\n", "color": "#7FD3FF", "bold": true}, {"text": "\n적을 쓰러뜨리면 경험치를 얻고, 레벨이 오르면 체력 · 공격력 · 방어력이 오릅니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n레벨이 오를 때마다 아이템을 고를 기회가 생깁니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n무기를 든 채 웅크리기(Shift) 키로 선택 공간에 들어가 셋 중 하나를 고르세요.", "color": "#E6E6E6", "bold": false}, {"text": "\n아이템은 등급(커먼 ~ 신화)이 있고, 저마다 「각인」을 가집니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n같은 각인을 여러 개 모으면 세트 효과가 켜집니다.", "color": "#E6E6E6", "bold": false}, {"text": "\n인벤토리(E)의 「인벤토리 상세」 상자를 누르면 가진 아이템과 각인을 정리할 수 있어요.", "color": "#E6E6E6", "bold": false}]
data merge entity @e[tag=rlk_tutp,limit=1] {line_width:300,transformation:{translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}
scoreboard players set #tutNeed lob 0
data modify storage rlk:lobby tg set value ""
