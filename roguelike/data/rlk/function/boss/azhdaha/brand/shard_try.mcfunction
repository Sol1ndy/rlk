# @s = the player just branded without a shield: one 응결 결정 (cooldown 300 t, at most 1 alive, life 200 t).
execute if score #azClk mb < #azShCd mb run return 0
execute if entity @e[type=minecraft:item_display,tag=rlk_az_shard,limit=1] run return 0
kill @e[type=minecraft:marker,tag=rlk_mb_az_shp]
# away from the anchor when it is within 10 b, else a random bearing; 5 b out
execute at @s if entity @e[type=minecraft:husk,tag=rlk_mb_body,distance=..10,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^5 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_shp"]}
execute store result storage rlk:mboss az.sh.a int 1 run random value 0..359
execute at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] run function rlk:boss/azhdaha/brand/shard_rnd with storage rlk:mboss az.sh
execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] run function rlk:boss/azhdaha/u/clamp_w
# off a live hazard and the body: one swing of 60 degrees about the player, else give up
execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] at @s if entity @e[type=minecraft:marker,tag=rlk_mb_hz,distance=..4,limit=1] at @a[tag=player,limit=1] facing entity @s feet rotated ~60 0 positioned ^ ^ ^5 run tp @s ~ 201 ~
execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] at @s if entity @e[type=minecraft:husk,tag=rlk_mb_body,distance=..5,limit=1] at @a[tag=player,limit=1] facing entity @s feet rotated ~-120 0 positioned ^ ^ ^5 run tp @s ~ 201 ~
execute as @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] at @s if entity @e[type=minecraft:marker,tag=rlk_mb_hz,distance=..4,limit=1] run kill @s
execute at @e[type=minecraft:marker,tag=rlk_mb_az_shp,limit=1] run function rlk:boss/azhdaha/brand/shard_make
kill @e[type=minecraft:marker,tag=rlk_mb_az_shp]
