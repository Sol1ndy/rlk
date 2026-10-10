# 소각: 검붉은 불기둥
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.7 0.3 0.06 25
particle minecraft:flame ~ ~1 ~ 0.35 0.8 0.35 0.08 25
particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.6} ~ ~1.2 ~ 0.4 0.9 0.4 0 30
particle minecraft:large_smoke ~ ~1.5 ~ 0.3 0.6 0.3 0.03 10
execute unless score #k52 snd matches 1 run function rlk:snd/f54
execute unless score #k53 snd matches 1 run function rlk:snd/f55
scoreboard players operation #dmg tmp = #qDmg tmp
scoreboard players set #elem tmp 1
function rlk:element/dot
