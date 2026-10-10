execute unless score #k192 snd matches 1 run function rlk:snd/f207
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:20}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 6
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
scoreboard players set #aqE eng 6
execute positioned ~ ~1 ~ as @e[tag=rlk_mob,distance=..5] run function rlk:items/fx/to_me
tag @e[tag=rlk_mob,distance=..5] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
