# 소각: 검붉은 불기둥
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.7 0.3 0.06 25
particle minecraft:flame ~ ~1 ~ 0.35 0.8 0.35 0.08 25
particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.6} ~ ~1.2 ~ 0.4 0.9 0.4 0 30
particle minecraft:large_smoke ~ ~1.5 ~ 0.3 0.6 0.3 0.03 10
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.8 0.5
playsound minecraft:item.firecharge.use master @a ~ ~ ~ 0.8 0.6
scoreboard players operation #dmg tmp = #qDmg tmp
scoreboard players set #elem tmp 1
function rlk:element/dot
