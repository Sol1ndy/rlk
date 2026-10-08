# 치유를 받음 (@s = 플레이어, #heal tmp = 치유량): 생명의 계약을 먼저 깎고, 남은 만큼만 #heal 에 남긴다
scoreboard players operation #t1 tmp = @s bol
scoreboard players operation @s bol -= #heal tmp
scoreboard players operation #heal tmp -= #t1 tmp
execute if score #heal tmp matches ..-1 run scoreboard players set #heal tmp 0
execute if score @s bol matches ..0 run scoreboard players set @s bol 0
function rlk:player/bol/on_change
execute if score @s bol matches 0 run function rlk:player/bol/on_clear
