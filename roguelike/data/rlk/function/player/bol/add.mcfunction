# 생명의 계약 획득 (@s = 플레이어, 입력: #bolAdd tmp = 양). 상한 = 최대 체력의 #bolMax%
execute unless score @s bol matches 0.. run scoreboard players set @s bol 0
scoreboard players operation #bolPrev tmp = @s bol
scoreboard players operation @s bol += #bolAdd tmp
scoreboard players operation #t1 tmp = @s maxHealth
scoreboard players operation #t1 tmp *= #bolMax tmp
scoreboard players operation #t1 tmp /= #100 tmp
execute if score @s bol > #t1 tmp run scoreboard players operation @s bol = #t1 tmp
execute unless score @s bol = #bolPrev tmp run function rlk:player/bol/on_change
