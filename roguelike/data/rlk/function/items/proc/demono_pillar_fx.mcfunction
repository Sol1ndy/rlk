# @s = 플레이어, at = 불기둥 위치. 불기둥 이펙트 + 주변(2.5) 몹 타격
particle minecraft:flame ~ ~1 ~ 0.2 1.5 0.2 0.02 40
particle minecraft:lava ~ ~0.5 ~ 0.3 0.8 0.3 0 8
particle minecraft:large_smoke ~ ~2 ~ 0.3 1 0.3 0.02 15
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.7 0.7
execute as @e[tag=rlk_mob,distance=..2.5] at @s run function rlk:combat/apply
