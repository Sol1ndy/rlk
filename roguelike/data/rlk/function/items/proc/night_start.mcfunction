scoreboard players operation #amt tmp = @s maxHealth
# #nightShield 는 ‰ (80 = 최대 체력의 8%)
scoreboard players operation #amt tmp *= #nightShield tmp
scoreboard players operation #amt tmp /= #1000 tmp
execute if score #amt tmp matches ..0 run scoreboard players set #amt tmp 1
function rlk:element/shield_gain
scoreboard players operation #nightT itv = #nightDur tmp
scoreboard players set #stars itv 0
