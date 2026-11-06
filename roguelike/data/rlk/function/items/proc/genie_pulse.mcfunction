scoreboard players operation #enAdd tmp = #genieEnergy tmp
function rlk:char/energy_add
scoreboard players operation #heal tmp = @s maxHealth
# 회복 = 최대 체력의 #genieHeal‰ (최소 1)
scoreboard players operation #heal tmp *= #genieHeal tmp
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:wax_on ~ ~1.2 ~ 0.3 0.5 0.3 0 6
