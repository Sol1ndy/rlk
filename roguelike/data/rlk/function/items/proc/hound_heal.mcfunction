scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #houndHeal tmp
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
