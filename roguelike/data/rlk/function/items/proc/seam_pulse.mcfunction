# @s = 플레이어
scoreboard players operation #amt tmp = @s maxHealth
scoreboard players operation #amt tmp *= #seamShield tmp
scoreboard players operation #amt tmp /= #100 tmp
execute if score #amt tmp matches ..0 run scoreboard players set #amt tmp 1
function rlk:element/shield_gain
scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #seamHeal tmp
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:happy_villager ~ ~1 ~ 0.4 0.6 0.4 0 8
