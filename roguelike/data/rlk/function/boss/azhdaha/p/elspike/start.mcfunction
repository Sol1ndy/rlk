# 46 천동만상 – 번개 가시 (Electro, replaces P4 in phase 3): the back glows t0-22, spikes up at t14; the hexagram
# (keep: a zone marker, plan Change note 1) at lockv (lead 10) at t26, redrawn under a player > 8 b away
# before a lump; 6 lumps at [44, 59, 74, 89, 104, 122]: each locks the player's feet 13 t before (the lump hovers
# over the lock, falls in the last 5 t, a bolt at -3), disc r 3.0, 0.7 + brand, groups (1,2) (3,4) 5 6.
function rlk:boss/azhdaha/rig/glow/gold_on
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^4 ^-0.2 run particle minecraft:electric_spark ~ ~ ~ 1.2 0.6 1.2 0.1 10 force @a[tag=player]
