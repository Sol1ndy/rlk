# @s = 풀 씨앗, at @s. 번개가 닿았으면 만개(12), 불이 닿았으면 발화(13), 수명이 다하면 개화 폭발
execute if score @s rxQ matches 12 run return run function rlk:element/core_hyper
execute if score @s rxQ matches 13 run return run function rlk:element/core_burgeon
scoreboard players remove @s life 1
particle minecraft:happy_villager ~ ~0.2 ~ 0.15 0.15 0.15 0 1
execute if score @s life matches ..0 run function rlk:element/core_bloom
