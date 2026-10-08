playsound minecraft:entity.sheep.shear master @a ~ ~ ~ 0.7 1.4
execute as @a[tag=player,limit=1] run function rlk:items/calc_stat {obj:"def",pm:1000}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 5
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
tag @e[tag=rlk_hit,limit=1] add rlk_abt
scoreboard players set #aqE eng 5
scoreboard players set #bi eng 0
execute positioned ~ ~0.8 ~ facing entity @e[tag=rlk_abt,limit=1] eyes run function rlk:items/fx/shot
tag @e[tag=rlk_abt] remove rlk_abt
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..10,sort=nearest,limit=1] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
