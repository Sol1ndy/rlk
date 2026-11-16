scoreboard players operation #heal tmp = @s maxHealth
# 회복 = 최대 체력의 #jellyHeal‰ (20 = 2%)
scoreboard players operation #heal tmp *= #jellyHeal tmp
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:heart ~ ~2.1 ~ 0.2 0.1 0.2 0 1
