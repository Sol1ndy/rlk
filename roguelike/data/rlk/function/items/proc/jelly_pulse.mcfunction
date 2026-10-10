particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~4.00 ~0.2 ~0.00 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~3.80 ~0.2 ~1.24 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~3.24 ~0.2 ~2.35 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~2.35 ~0.2 ~3.24 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~1.24 ~0.2 ~3.80 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~0.00 ~0.2 ~4.00 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-1.24 ~0.2 ~3.80 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-2.35 ~0.2 ~3.24 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-3.24 ~0.2 ~2.35 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-3.80 ~0.2 ~1.24 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-4.00 ~0.2 ~0.00 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-3.80 ~0.2 ~-1.24 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-3.24 ~0.2 ~-2.35 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-2.35 ~0.2 ~-3.24 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-1.24 ~0.2 ~-3.80 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~-0.00 ~0.2 ~-4.00 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~1.24 ~0.2 ~-3.80 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~2.35 ~0.2 ~-3.24 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~3.24 ~0.2 ~-2.35 0 0 0 0 1
particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.0f} ~3.80 ~0.2 ~-1.24 0 0 0 0 1
particle minecraft:splash ~ ~0.4 ~ 1.8 0.2 1.8 0.1 30
execute unless score #k117 snd matches 1 run function rlk:snd/f125
execute as @a[tag=player,limit=1] run function rlk:items/calc_stat {obj:"maxHealth",pm:50}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 2
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
scoreboard players set #aqE eng 2
execute positioned ~ ~1.6 ~ as @e[tag=rlk_mob,distance=..4] run function rlk:items/fx/to_me
tag @e[tag=rlk_mob,distance=..4] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute if entity @e[tag=rlk_body,distance=..4] as @a[tag=player,limit=1] run function rlk:items/proc/jelly_heal
