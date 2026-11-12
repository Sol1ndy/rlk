scoreboard players set #nurseQ itv 0
scoreboard players operation #enAdd tmp = #nurseEnergy tmp
function rlk:char/energy_add
scoreboard players operation #heal tmp = @s maxHealth
# 회복 = 최대 체력의 #nurseHeal‰
scoreboard players operation #heal tmp *= #nurseHeal tmp
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3
