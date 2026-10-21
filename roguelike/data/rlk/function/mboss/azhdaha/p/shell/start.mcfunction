# 44 번개의 가루 (Electro shells): tail_cast with the spark column (the tell), 8 shells from the tail tip every 5 t from
# fire into a hover cloud 7-9 b up over the front; each shell locks the player's feet 4 t before its dive
# (a flash + a sound on the shell), dives in 8 t: disc r 2.4, tell 12, 0.6 + brand, groups of 4; no ground
# decal (plan Change note 1). The body idles and tracks <= 2 deg/t until the last dive.
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^10.362 ^-1.445 run function rlk:mboss/azhdaha/fx/p/spark_column {h:60}
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^10.362 ^-1.445 run playsound minecraft:entity.evoker.prepare_attack hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
