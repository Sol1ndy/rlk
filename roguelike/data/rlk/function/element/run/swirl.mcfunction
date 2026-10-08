# 확산: 반경 4칸에 해당 원소 피해. 주변 몹에게는 그 원소가 묻어 연쇄 반응이 일어날 수 있음
particle minecraft:cloud ~ ~1 ~ 1.2 0.6 1.2 0.12 30
particle minecraft:sweep_attack ~ ~1 ~ 1 0.4 1 0 6
playsound minecraft:entity.breeze.wind_burst master @a ~ ~ ~ 0.7 1.2
scoreboard players set #qU tmp 0
function rlk:element/aoe_hit
scoreboard players set #qU tmp 1000
execute as @e[tag=rlk_mob,distance=0.01..4] at @s run function rlk:element/aoe_hit
