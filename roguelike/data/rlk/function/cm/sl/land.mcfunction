# 착지: 반경 1.9 안의 몸에 12(번개)
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 6
particle minecraft:electric_spark ~ ~0.2 ~ 1.2 0.1 1.2 0.25 30 normal
particle minecraft:item_slime ~ ~0.3 ~ 0.8 0.2 0.8 0.1 16 normal
execute unless score #c2slland snd matches 1 run function rlk:cm/c2/snd/slland
execute unless score #c2slzap snd matches 1 run function rlk:cm/c2/snd/slzap
execute if entity @e[tag=rlk_body,distance=..1.9] run function rlk:cm/sl/hit
