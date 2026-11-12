scoreboard players operation #heal tmp = @s maxHealth
# 회복 = 최대 체력의 #talHeal‰
scoreboard players operation #heal tmp *= #talHeal tmp
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
