# @s = 플레이어. 최대 체력의 #gringHeal‰ 회복 (최소 1) + 주변에 적이 있으면 번개 피해
scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #gringHeal tmp
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute if entity @e[tag=rlk_mob,distance=..3.5,limit=1] run function rlk:items/proc/gring_hit
