# @s = 플레이어, at = 촉수 위치. 촉수 이펙트 + 주변(3) 몹 타격
particle minecraft:sculk_charge_pop ~ ~0.5 ~ 0.3 1 0.3 0.05 30
particle minecraft:squid_ink ~ ~1.5 ~ 0.3 1 0.3 0.02 20
particle minecraft:sculk_soul ~ ~2 ~ 0.2 0.5 0.2 0.02 12
execute unless score #k174 snd matches 1 run function rlk:snd/f185
execute as @e[tag=rlk_mob,distance=..3] at @s run function rlk:combat/apply
