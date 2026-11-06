scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp /= #c100 mb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/apep/fx/p/spark
