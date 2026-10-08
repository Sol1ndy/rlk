scoreboard players remove @s pcVal 1
particle minecraft:flame ^ ^0.6 ^1.2 0.3 0.25 0.3 0.06 30
particle minecraft:flame ^ ^0.6 ^2.6 0.6 0.3 0.6 0.05 40
particle minecraft:flame ^ ^0.6 ^4.0 0.8 0.35 0.8 0.04 40
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.7 0.8
particle minecraft:lava ^ ^0.7 ^0.6 0.1 0.1 0.1 0 4
particle minecraft:small_flame ^ ^0.6 ^2 0.2 0.2 1.2 0.02 40
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:45}
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
