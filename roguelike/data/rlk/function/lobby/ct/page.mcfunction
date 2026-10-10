# 캐릭터 튜토리얼 한 쪽 준비 (@s = 플레이어, #tutS 21~26)
data modify storage rlk:lobby ct set value {}
data modify storage rlk:lobby ct.name set from storage rlk:chars cur.info.name
data modify storage rlk:lobby ct.color set from storage rlk:chars cur.info.color
# 더미 셋(앞 · 양옆)
execute if score #tutS lob matches 21..25 positioned 120.5 193 24.0 run function rlk:lobby/try/dummy_at
execute if score #tutS lob matches 21..25 positioned 122.5 193 23.0 run function rlk:lobby/try/dummy_at
execute if score #tutS lob matches 21..25 positioned 124.5 193 24.0 run function rlk:lobby/try/dummy_at
execute if score #tutS lob matches 21..25 run tag @e[tag=rlk_dummy,x=122.5,y=193,z=23.5,distance=..2.5] add rlk_tutE
execute if score #tutS lob matches 21 run data modify storage rlk:lobby ct.h set value "1. 기본 공격"
execute if score #tutS lob matches 21 run data modify storage rlk:lobby ct.q set from storage rlk:chars cur.weapon.lore
execute if score #tutS lob matches 21 run scoreboard players set #tutNeed lob 6
execute if score #tutS lob matches 21 run data modify storage rlk:lobby tg set value "더미를 기본 공격으로 6번 공격하기"
execute if score #tutS lob matches 22 run data modify storage rlk:lobby ct.h set value "2. 원소전투 스킬"
execute if score #tutS lob matches 22 run data modify storage rlk:lobby ct.q set from storage rlk:chars cur.skill.lore
execute if score #tutS lob matches 22 run scoreboard players set #tutNeed lob 2
execute if score #tutS lob matches 22 run data modify storage rlk:lobby tg set value "원소전투 스킬 2번 쓰기"
execute if score #tutS lob matches 23 run data modify storage rlk:lobby ct.h set value "3. 원소폭발"
execute if score #tutS lob matches 23 run data modify storage rlk:lobby ct.q set from storage rlk:chars cur.burst.lore
execute if score #tutS lob matches 23 run scoreboard players set #tutNeed lob 1
execute if score #tutS lob matches 23 run data modify storage rlk:lobby tg set value "원소폭발 쓰기"
execute if score #tutS lob matches 24 run data modify storage rlk:lobby ct.h set value "4. 고유 특성"
execute if score #tutS lob matches 24 run data modify storage rlk:lobby ct.q set from storage rlk:chars cur.info.passive
execute if score #tutS lob matches 24 run scoreboard players set #tutNeed lob 0
execute if score #tutS lob matches 24 run data modify storage rlk:lobby tg set value ""
execute if score #tutS lob matches 25 run data modify storage rlk:lobby ct.h set value "5. 추가 설명"
execute if score #tutS lob matches 25 run data modify storage rlk:lobby ct.q set from storage rlk:chars cur.info.extra.lore
execute if score #tutS lob matches 25 run scoreboard players set #tutNeed lob 0
execute if score #tutS lob matches 25 run data modify storage rlk:lobby tg set value ""
execute if score #tutS lob matches 25 run data modify storage rlk:lobby ct.h set from storage rlk:chars cur.info.extra.name
execute if score #tutS lob matches 23 run scoreboard players operation @s energy = #burstCost100 tmp
execute if score #tutS lob matches 23 run scoreboard players set @s burstCd 0
execute if score #tutS lob matches 26 run data modify storage rlk:lobby ct.h set value "완료!"
execute if score #tutS lob matches 26 run scoreboard players set #tutNeed lob 0
execute if score #tutS lob matches 26 run data modify storage rlk:lobby ct.q set value [{text:"수고했어요! 이 캐릭터의 기본 공격 · 스킬 · 원소폭발 · 고유 특성을 모두 봤습니다.",color:"#E6E6E6"},{text:"「캐릭터 바꾸기」로 다른 캐릭터를 고른 뒤 「캐릭터 튜토리얼」을 다시 누르면 그 캐릭터를 배울 수 있어요.",color:"#E6E6E6"},{text:"「캐릭터 · 아이템 체험」 방에서는 더미로 DPS 를 재 볼 수 있습니다.",color:"#E6E6E6"}]
function rlk:lobby/ct/head with storage rlk:lobby ct
function rlk:lobby/ct/loop
# 길이에 따라 글자 크기 · 줄 폭 · 높이
execute store result score #t lob run data get storage rlk:lobby ct.list
execute if score #t lob matches ..19 run data merge entity @e[tag=rlk_tutp,limit=1] {line_width:320,transformation:{translation:[0f,0f,0f],scale:[1.6f,1.6f,1.6f]}}
execute if score #t lob matches 20..33 run data merge entity @e[tag=rlk_tutp,limit=1] {line_width:400,transformation:{translation:[0f,0f,0f],scale:[1.2f,1.2f,1.2f]}}
execute if score #t lob matches 34.. run data merge entity @e[tag=rlk_tutp,limit=1] {line_width:500,transformation:{translation:[0f,0f,0f],scale:[0.95f,0.95f,0.95f]}}
function rlk:lobby/ct/show with storage rlk:lobby ct
