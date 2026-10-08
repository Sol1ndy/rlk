particle minecraft:flame ~ ~1 ~ 1.6 0.3 1.6 0.05 40
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.4 1.3
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:50}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
scoreboard players set #aqE eng 1
execute positioned ~ ~1 ~ as @e[tag=rlk_mob,distance=..3.5] run function rlk:items/fx/to_me
tag @e[tag=rlk_mob,distance=..3.5] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
