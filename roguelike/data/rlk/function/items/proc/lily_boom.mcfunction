scoreboard players set #lilyHit itv 0
scoreboard players operation #lilyCd itv = #lilyCdT tmp
particle minecraft:splash ~ ~0.5 ~ 1.5 0.3 1.5 0.2 40
particle minecraft:bubble_pop ~ ~1 ~ 1.5 0.5 1.5 0.02 20
playsound minecraft:entity.generic.splash master @a ~ ~ ~ 0.5 1.5
execute as @a[tag=player,limit=1] run function rlk:items/calc_stat {obj:"maxHealth",pm:40}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 2
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..4] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
