scoreboard players set #lionQ itv 0
particle minecraft:flame ~ ~1 ~ 1.5 0.5 1.5 0.06 40
particle minecraft:lava ~ ~1 ~ 1.2 0.4 1.2 0 8
execute unless score #k140 snd matches 1 run function rlk:snd/f148
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:150}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..4] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
