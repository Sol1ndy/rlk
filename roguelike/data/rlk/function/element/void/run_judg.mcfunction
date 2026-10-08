# 단죄: 붉은 낙뢰
particle minecraft:dust{color:[0.85,0.10,0.30],scale:1.6} ~ ~4 ~ 0.04 3 0.04 0 50
particle minecraft:electric_spark ~ ~1 ~ 0.3 0.8 0.3 0.4 30
particle minecraft:end_rod ~ ~1 ~ 0.2 0.6 0.2 0.1 10
playsound minecraft:item.trident.thunder master @a ~ ~ ~ 0.5 1.4
playsound minecraft:entity.lightning_bolt.impact master @a ~ ~ ~ 0.6 1.2
scoreboard players operation #dmg tmp = #qDmg tmp
scoreboard players set #elem tmp 3
function rlk:element/dot
function rlk:char/particles {n:1,el:8}
