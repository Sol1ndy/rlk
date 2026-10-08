# @s = 회복구슬, at @s. 파티클 + 근접 흡수
particle minecraft:happy_villager ~ ~0.3 ~ 0.15 0.15 0.15 0 1
particle minecraft:end_rod ~ ~0.3 ~ 0.08 0.08 0.08 0.01 1
execute if entity @e[tag=rlk_body,distance=..1.6] run function rlk:combat/healorb_absorb
