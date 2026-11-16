# 아이템 선택 안내 (@s = 플레이어, 매 틱): 고를 것이 있고 · 선택 공간 밖이고 · 살아 있고 · 전투 중이 아닐 때. 1초마다 다시 띄워 계속 보이게
scoreboard players set #ps tmp 0
execute if score @s pkPending matches 1.. unless score @s pkMode matches 1.. unless score @s dead matches 1 run scoreboard players set #ps tmp 1
# 전투 중에는 띄우지 않는다(사용자 11-06): 방 전투(#active room 1 · #combat room = 구역 번호; 나루카미 · 중간 · 챕터 · 특수 보스도 이 흐름)
# 또는 보스 엔진이 돌고 있음(#mbLive mb 1, 등장 연출부터 정리까지). 끝나면 「구역 정리」 제목(ttlT) 뒤에 다시 뜬다
execute if score #active room matches 1 if score #combat room matches 1.. run scoreboard players set #ps tmp 0
execute if score #mbLive mb matches 1 run scoreboard players set #ps tmp 0
# 다른 제목이 떠 있는 동안: 덮지 않고 기다림(끝나면 바로 다시 띄움)
execute if score @s ttlT matches 1.. run return run scoreboard players set @s pkSubT 0
# 보일 필요가 없어짐: 띄워 둔 아랫줄만 지운다(제목 줄은 F5 조준점이라 그대로 둠: title clear 면 조준점이 다음 재전송까지 사라짐)
execute if score #ps tmp matches 0 if score @s pkSubT matches 1.. run title @s subtitle ""
execute if score #ps tmp matches 0 run return run scoreboard players set @s pkSubT 0
scoreboard players remove @s pkSubT 1
execute if score @s pkSubT matches 1.. run return 0
scoreboard players set @s pkSubT 20
title @s times 0 30 5
title @s subtitle [{"text":"고를 아이템 ","color":"#FFE08A"},{"score":{"name":"@s","objective":"pkPending"},"color":"white","bold":true},{"text":"개  ·  ","color":"#FFE08A"},{"text":"웅크리기(Shift)","color":"white"},{"text":" 로 선택","color":"gray"}]
function rlk:view/ttl_blank
