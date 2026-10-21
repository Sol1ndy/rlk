execute if entity @s[tag=!rlk_mb_ap_rng] if entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,distance=..3.4,limit=1] run return run function rlk:mboss/apep/org/b_arrive
execute if entity @s[tag=rlk_mb_ap_rng] if entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,distance=..8,limit=1] run return run function rlk:mboss/apep/org/b_arrive
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run function rlk:mboss/mv/step_flat {spd:0.12}
