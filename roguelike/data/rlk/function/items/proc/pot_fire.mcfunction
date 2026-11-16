scoreboard players remove @s pcVal 1
particle minecraft:flame ^ ^0.6 ^1.2 0.3 0.25 0.3 0.06 30
particle minecraft:flame ^ ^0.6 ^2.6 0.6 0.3 0.6 0.05 40
particle minecraft:flame ^ ^0.6 ^4.0 0.8 0.35 0.8 0.04 40
execute unless score #k140 snd matches 1 run function rlk:snd/f148
particle minecraft:lava ^ ^0.7 ^0.6 0.1 0.1 0.1 0 4
particle minecraft:small_flame ^ ^0.6 ^2 0.2 0.2 1.2 0.02 40
# 피해 계수 = #potCoef (강화 단계로 조정)
execute store result storage rlk:tune m_hot_pot.coef int 1 run scoreboard players get #potCoef tmp
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc with storage rlk:tune m_hot_pot
scoreboard players set #sub itv 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
execute positioned ^ ^ ^1.5 run tag @e[tag=rlk_mob,distance=..1.8] add rlk_hit
execute positioned ^ ^ ^3.2 run tag @e[tag=rlk_mob,distance=..2.2] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
scoreboard players set #sub itv 0
