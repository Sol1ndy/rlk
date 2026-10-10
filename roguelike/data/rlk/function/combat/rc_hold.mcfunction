# 우클릭을 누르고 있음(아이템 사용 중, @s = 플레이어): 처음 틱과 4틱마다 우클릭 처리(인터랙션 우클릭의 반복과 같은 간격)
scoreboard players add @s rcT 1
scoreboard players operation #t1 tmp = @s rcT
scoreboard players operation #t1 tmp %= #4 tmp
execute if score #t1 tmp matches 1 at @s run function rlk:combat/rclick_do
