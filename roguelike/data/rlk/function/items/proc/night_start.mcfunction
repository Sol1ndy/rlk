scoreboard players operation #amt tmp = @s maxHealth
scoreboard players operation #amt tmp *= #nightShield tmp
scoreboard players operation #amt tmp /= #100 tmp
execute if score #amt tmp matches ..0 run scoreboard players set #amt tmp 1
function rlk:element/shield_gain
scoreboard players operation #nightT itv = #nightDur tmp
scoreboard players set #stars itv 0
