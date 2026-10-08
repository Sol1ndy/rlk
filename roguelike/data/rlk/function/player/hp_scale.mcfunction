# 최대 체력 변경 시 현재 체력을 같은 비율로 (@s = 플레이어)
execute unless score @s hpMaxPrev matches 1.. run scoreboard players operation @s hpMaxPrev = @s maxHealth
scoreboard players operation #cur tmp = @s curHealth
scoreboard players operation #cur tmp *= @s maxHealth
scoreboard players operation #cur tmp /= @s hpMaxPrev
execute if score @s curHealth matches 1.. if score #cur tmp matches ..0 run scoreboard players set #cur tmp 1
scoreboard players operation @s curHealth = #cur tmp
scoreboard players operation @s hpMaxPrev = @s maxHealth
