scoreboard players operation #maidCd itv = #maidCdT tmp
scoreboard players operation #heal tmp = @s def
# 회복량 = 방어력 × #maidHeal ‰ (60 = 6%)
scoreboard players operation #heal tmp *= #maidHeal tmp
scoreboard players operation #heal tmp /= #1000 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:heart ~ ~1.8 ~ 0.2 0.1 0.2 0 1
