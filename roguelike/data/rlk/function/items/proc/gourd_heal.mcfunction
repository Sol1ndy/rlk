# 회복량 = 최대 체력 × #gourdHeal‰ × 개수
scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #gourdHeal tmp
scoreboard players operation #heal tmp *= @s it_life_gourd
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
