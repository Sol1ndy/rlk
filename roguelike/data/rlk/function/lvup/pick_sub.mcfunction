# 아이템 선택 안내 (@s = 플레이어, 매 틱): 고를 것이 있고 · 선택 공간 밖이고 · 살아 있을 때. 1초마다 다시 띄워 계속 보이게
scoreboard players set #ps tmp 0
execute if score @s pkPending matches 1.. unless score @s pkMode matches 1.. unless score @s dead matches 1 run scoreboard players set #ps tmp 1
# 다른 제목이 떠 있는 동안: 덮지 않고 기다림(끝나면 바로 다시 띄움)
execute if score @s ttlT matches 1.. run return run scoreboard players set @s pkSubT 0
# 보일 필요가 없어짐: 띄워 둔 것만 지운다
execute if score #ps tmp matches 0 if score @s pkSubT matches 1.. run title @s clear
execute if score #ps tmp matches 0 run return run scoreboard players set @s pkSubT 0
scoreboard players remove @s pkSubT 1
execute if score @s pkSubT matches 1.. run return 0
scoreboard players set @s pkSubT 20
title @s times 0 30 5
execute if score #on view matches 1 if score #vmode view matches 2 run title @s subtitle [{"text":"고를 아이템 ","color":"#FFE08A"},{"score":{"name":"@s","objective":"pkPending"},"color":"white","bold":true},{"text":"개  ·  ","color":"#FFE08A"},{"text":"웅크리기(Shift)","color":"white"},{"text":" 로 선택","color":"gray"}]
execute unless score #vmode view matches 2 run title @s subtitle [{"text":"고를 아이템 ","color":"#FFE08A"},{"score":{"name":"@s","objective":"pkPending"},"color":"white","bold":true},{"text":"개  ·  ","color":"#FFE08A"},{"text":"Shift + F","color":"white"},{"text":" 로 선택","color":"gray"}]
execute unless score #on view matches 1 if score #vmode view matches 2 run title @s subtitle [{"text":"고를 아이템 ","color":"#FFE08A"},{"score":{"name":"@s","objective":"pkPending"},"color":"white","bold":true},{"text":"개  ·  ","color":"#FFE08A"},{"text":"Shift + F","color":"white"},{"text":" 로 선택","color":"gray"}]
function rlk:view/ttl_blank
