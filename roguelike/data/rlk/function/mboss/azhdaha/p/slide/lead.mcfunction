# T1 lead (@s = body): walk to <= 2 b of the arena centre (the glide length from the distance, GLIDE_SPD
# 0.3 b/t, 8-24 t, then walk_stop) or, already there, step-turn in place when
# the player is more than 20 degrees off the facing; the turn runs only until the clip starts (the landslide
# clip keeps its feet planted: no yaw schedule, R3a note).
scoreboard players set #aq20W mb 0
scoreboard players set #aq20S mb 0
scoreboard players set #aq20M mb 0
scoreboard players set #aq20G mb 24
execute positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..2,limit=1] run scoreboard players set #aq20W mb 1
execute positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..6.0,limit=1] run scoreboard players set #aq20G mb 20
execute positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..4.8,limit=1] run scoreboard players set #aq20G mb 16
execute positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..3.6,limit=1] run scoreboard players set #aq20G mb 12
execute positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..2.4,limit=1] run scoreboard players set #aq20G mb 8
execute store result storage rlk:mboss az.p20.t int 1 run scoreboard players get #aq20G mb
execute if score #aq20W mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/mv/glide with storage rlk:mboss az.p20
execute if score #aq20W mb matches 0 run function rlk:mboss/azhdaha/p/slide/yerr
execute if score #aq20W mb matches 0 if score #aq20Y mb matches 2001.. run scoreboard players set #aq20S mb 1
execute if score #aq20S mb matches 1 run scoreboard players set #aq20G mb 8
execute if score #aq20S mb matches 1 if score #aq20Y mb matches 3201.. run scoreboard players set #aq20G mb 16
execute if score #aq20S mb matches 1 if score #aq20Y mb matches 6401.. run scoreboard players set #aq20G mb 24
execute if score #aq20W mb matches 1 run scoreboard players set #aq20M mb 1
execute if score #aq20S mb matches 1 run scoreboard players set #aq20M mb 1
execute if score #aq20M mb matches 1 run function rlk:mboss/azhdaha/rig/play/walk
execute if score #aq20M mb matches 0 run function rlk:mboss/azhdaha/rig/play/idle
