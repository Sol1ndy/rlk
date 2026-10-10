# 초전도: 반경 4칸 얼음 피해 + 12초간 물리 피해 +40%
particle minecraft:snowflake ~ ~1 ~ 1.5 0.8 1.5 0.1 50
particle minecraft:electric_spark ~ ~1 ~ 1.2 0.8 1.2 0.3 25
execute unless score #k62 snd matches 1 run function rlk:snd/f65
execute unless score #k63 snd matches 1 run function rlk:snd/f66
scoreboard players set #qU tmp 0
scoreboard players set @e[tag=rlk_mob,distance=..4] scT 240
scoreboard players set @e[tag=rlk_mob,distance=..4] elAct 1
execute as @e[tag=rlk_mob,distance=..4] at @s run function rlk:element/aoe_hit
