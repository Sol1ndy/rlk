particle minecraft:electric_spark ~ ~1 ~ 0.6 1.2 0.6 0.5 40
particle minecraft:end_rod ~ ~2 ~ 0.1 1.5 0.1 0.02 12
execute unless score #k183 snd matches 1 run function rlk:snd/f198
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:120}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..3] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
