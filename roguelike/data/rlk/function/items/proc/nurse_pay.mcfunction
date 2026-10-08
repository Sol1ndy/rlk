scoreboard players set #nurseQ itv 0
scoreboard players operation #enAdd tmp = #nurseEnergy tmp
function rlk:char/energy_add
scoreboard players operation #heal tmp = @s maxHealth
scoreboard players set #t1 itv 8
scoreboard players operation #heal tmp *= #t1 itv
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3
