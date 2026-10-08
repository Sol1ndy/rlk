scoreboard players operation #dandT itv = #dandDur tmp
scoreboard players operation #heal tmp = @s atk
scoreboard players set #t1 itv 150
scoreboard players operation #heal tmp *= #t1 itv
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:cloud ~ ~1 ~ 0.4 0.6 0.4 0.05 15
execute at @e[tag=rlk_body,limit=1] run particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3
