# 주변 6칸의 허계 균열을 모두 흡수 (@s = 플레이어, at 몸). 결과: #skAbs = 흡수한 개수, 1개당 뱀의 계략 +#skRiftGain
scoreboard players set #skAbs tmp 0
execute as @e[tag=rlk_rift,distance=..6] at @s run function rlk:char/skirk/rift_take
execute if score @s energy > #burstCost100 tmp run scoreboard players operation @s energy = #burstCost100 tmp
execute if score #skAbs tmp matches 1.. unless score #k312 snd matches 1 run function rlk:snd/f359
execute if score #skAbs tmp matches 1.. run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.5 0.3 0.15 30
