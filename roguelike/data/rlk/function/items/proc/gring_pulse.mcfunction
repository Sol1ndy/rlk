scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #gringHeal tmp
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute if entity @e[tag=rlk_mob,distance=..3.5,limit=1] run function rlk:items/proc/gring_hit
