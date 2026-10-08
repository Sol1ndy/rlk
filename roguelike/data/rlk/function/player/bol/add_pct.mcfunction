# 생명의 계약 획득 (@s = 플레이어, 입력: #bolPct tmp = 최대 체력의 %)
scoreboard players operation #t1 tmp = @s maxHealth
scoreboard players operation #t1 tmp *= #bolPct tmp
scoreboard players operation #t1 tmp /= #100 tmp
execute if score #t1 tmp matches ..0 run scoreboard players set #t1 tmp 1
scoreboard players operation #bolAdd tmp = #t1 tmp
function rlk:player/bol/add
