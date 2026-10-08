scoreboard players operation #maidCd itv = #maidCdT tmp
scoreboard players operation #heal tmp = @s def
scoreboard players set #t1 itv 6
scoreboard players operation #heal tmp *= #t1 itv
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:heart ~ ~1.8 ~ 0.2 0.1 0.2 0 1
