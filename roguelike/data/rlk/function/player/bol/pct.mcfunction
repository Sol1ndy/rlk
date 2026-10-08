# 생명의 계약이 최대 체력의 몇 % 인가 → #bolNow tmp (@s = 플레이어)
scoreboard players set #bolNow tmp 0
execute unless score @s bol matches 1.. run return 0
scoreboard players operation #bolNow tmp = @s bol
scoreboard players operation #bolNow tmp *= #100 tmp
scoreboard players operation #bolNow tmp /= @s maxHealth
