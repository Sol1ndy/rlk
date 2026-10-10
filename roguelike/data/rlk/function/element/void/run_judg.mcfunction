# 단죄: 붉은 낙뢰
particle minecraft:dust{color:[0.85,0.10,0.30],scale:1.6} ~ ~4 ~ 0.04 3 0.04 0 50
particle minecraft:electric_spark ~ ~1 ~ 0.3 0.8 0.3 0.4 30
particle minecraft:end_rod ~ ~1 ~ 0.2 0.6 0.2 0.1 10
execute unless score #k48 snd matches 1 run function rlk:snd/f50
execute unless score #k49 snd matches 1 run function rlk:snd/f51
scoreboard players operation #dmg tmp = #qDmg tmp
scoreboard players set #elem tmp 3
function rlk:element/dot
function rlk:char/particles {n:1,el:8}
