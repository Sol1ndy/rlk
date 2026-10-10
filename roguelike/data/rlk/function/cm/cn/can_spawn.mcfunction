# Run at the block center. A complete flat 3x3 full-block floor and 3 blocks of clear headroom are mandatory.
scoreboard players set #cnSpawnOk tmp 0
# Keep the three-by-three emplacement separate from nearby artillery.
execute positioned ~-2.5 ~ ~-2.5 if entity @e[tag=rlk_cm_cn,dx=4,dy=2,dz=4] run return 0
execute unless block ~-1 ~-1 ~-1 #rlk:cannon_floor run return 0
execute unless block ~-1 ~ ~-1 #rlk:cannon_clear run return 0
execute unless block ~-1 ~1 ~-1 #rlk:cannon_clear run return 0
execute unless block ~-1 ~2 ~-1 #rlk:cannon_clear run return 0
execute unless block ~-1 ~-1 ~ #rlk:cannon_floor run return 0
execute unless block ~-1 ~ ~ #rlk:cannon_clear run return 0
execute unless block ~-1 ~1 ~ #rlk:cannon_clear run return 0
execute unless block ~-1 ~2 ~ #rlk:cannon_clear run return 0
execute unless block ~-1 ~-1 ~1 #rlk:cannon_floor run return 0
execute unless block ~-1 ~ ~1 #rlk:cannon_clear run return 0
execute unless block ~-1 ~1 ~1 #rlk:cannon_clear run return 0
execute unless block ~-1 ~2 ~1 #rlk:cannon_clear run return 0
execute unless block ~ ~-1 ~-1 #rlk:cannon_floor run return 0
execute unless block ~ ~ ~-1 #rlk:cannon_clear run return 0
execute unless block ~ ~1 ~-1 #rlk:cannon_clear run return 0
execute unless block ~ ~2 ~-1 #rlk:cannon_clear run return 0
execute unless block ~ ~-1 ~ #rlk:cannon_floor run return 0
execute unless block ~ ~ ~ #rlk:cannon_clear run return 0
execute unless block ~ ~1 ~ #rlk:cannon_clear run return 0
execute unless block ~ ~2 ~ #rlk:cannon_clear run return 0
execute unless block ~ ~-1 ~1 #rlk:cannon_floor run return 0
execute unless block ~ ~ ~1 #rlk:cannon_clear run return 0
execute unless block ~ ~1 ~1 #rlk:cannon_clear run return 0
execute unless block ~ ~2 ~1 #rlk:cannon_clear run return 0
execute unless block ~1 ~-1 ~-1 #rlk:cannon_floor run return 0
execute unless block ~1 ~ ~-1 #rlk:cannon_clear run return 0
execute unless block ~1 ~1 ~-1 #rlk:cannon_clear run return 0
execute unless block ~1 ~2 ~-1 #rlk:cannon_clear run return 0
execute unless block ~1 ~-1 ~ #rlk:cannon_floor run return 0
execute unless block ~1 ~ ~ #rlk:cannon_clear run return 0
execute unless block ~1 ~1 ~ #rlk:cannon_clear run return 0
execute unless block ~1 ~2 ~ #rlk:cannon_clear run return 0
execute unless block ~1 ~-1 ~1 #rlk:cannon_floor run return 0
execute unless block ~1 ~ ~1 #rlk:cannon_clear run return 0
execute unless block ~1 ~1 ~1 #rlk:cannon_clear run return 0
execute unless block ~1 ~2 ~1 #rlk:cannon_clear run return 0
scoreboard players set #cnSpawnOk tmp 1
return 1
