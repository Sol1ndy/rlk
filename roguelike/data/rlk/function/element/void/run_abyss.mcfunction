# 심연: 주변 적에게 물 범위 피해
particle minecraft:bubble_pop ~ ~1 ~ 1.4 0.4 1.4 0.05 40
particle minecraft:splash ~ ~1 ~ 1.4 0.4 1.4 0.2 50
particle minecraft:dust{color:[0.25,0.35,0.95],scale:1.4} ~ ~0.6 ~ 1.5 0.2 1.5 0 30
particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.2} ~ ~0.6 ~ 0.8 0.2 0.8 0 15
execute unless score #k54 snd matches 1 run function rlk:snd/f56
execute unless score #k55 snd matches 1 run function rlk:snd/f57
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:element/aoe_hit
