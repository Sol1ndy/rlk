# 만개: 가장 가까운 적(12칸) 하나에게 풀 피해 300%
scoreboard players set #rx tmp 12
function rlk:engravings/on_rx
execute positioned ~ ~-1.5 ~ run function rlk:element/rx_text
particle minecraft:electric_spark ~ ~0.5 ~ 0.4 0.4 0.4 0.4 25
execute unless score #k45 snd matches 1 run function rlk:snd/f47
scoreboard players operation #qDmg tmp = @s rxDmg3
scoreboard players set #qEl tmp 7
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,distance=..12,sort=nearest,limit=1] at @s run function rlk:element/aoe_hit
kill @s
