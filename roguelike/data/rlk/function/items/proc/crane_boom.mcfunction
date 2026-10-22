particle minecraft:cloud ~ ~0.6 ~ 1.8 0.3 1.8 0.08 40
particle minecraft:sweep_attack ~ ~1 ~ 2 0.3 2 0 8
execute unless score #k137 snd matches 1 run function rlk:snd/f145
# 피해 계수 = #craneCoef (강화 단계로 조정)
execute store result storage rlk:tune m_crane_feather.coef int 1 run scoreboard players get #craneCoef tmp
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc with storage rlk:tune m_crane_feather
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 6
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..4.5] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
