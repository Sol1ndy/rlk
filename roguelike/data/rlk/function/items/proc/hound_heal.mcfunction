scoreboard players operation #heal tmp = @s maxHealth
# #houndHeal 은 ‰ (10 = 최대 체력의 1%)
scoreboard players operation #heal tmp *= #houndHeal tmp
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
