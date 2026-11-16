# 우클릭을 누르고 있음(아이템 사용 중, @s = 플레이어): 처음 틱과 4틱마다 우클릭 처리(인터랙션 우클릭의 반복과 같은 간격)
scoreboard players add @s rcT 1
scoreboard players operation #t1 tmp = @s rcT
scoreboard players operation #t1 tmp %= #4 tmp
# round W: 누르고 있어 반복되는 우클릭(rcT 2 이상: 5 · 9 · 13 …틱)은 #rcRep tmp 1 — 더블 닷지의 두 번째 누름으로 치지 않는다(player/dodge/again)
execute if score #t1 tmp matches 1 if score @s rcT matches 2.. run scoreboard players set #rcRep tmp 1
execute if score #t1 tmp matches 1 at @s run function rlk:combat/rclick_do
scoreboard players set #rcRep tmp 0
