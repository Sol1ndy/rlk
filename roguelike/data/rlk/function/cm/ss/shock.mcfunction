# 감전: 반경 1.5 안의 몸에 6(번개)
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 4
scoreboard players set @s c2T 14
execute as @e[tag=rlk_c2ring,distance=..4] if score @s cmId = #cid tmp run kill @s
particle minecraft:electric_spark ~ ~0.3 ~ 0.9 0.2 0.9 0.3 30 normal
particle minecraft:end_rod ~ ~0.3 ~ 0.6 0.1 0.6 0.05 8 normal
execute unless score #c2ssshock snd matches 1 run function rlk:cm/c2/snd/ssshock
execute unless score #c2sszap snd matches 1 run function rlk:cm/c2/snd/sszap
execute if entity @e[tag=rlk_body,distance=..1.5] run function rlk:cm/ss/hit
