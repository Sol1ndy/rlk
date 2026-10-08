scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #gourdHeal tmp
scoreboard players operation #heal tmp *= @s it_life_gourd
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
