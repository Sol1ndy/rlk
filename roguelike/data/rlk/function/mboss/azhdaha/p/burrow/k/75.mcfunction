# burrow #azPT 75
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
function rlk:mboss/mv/lockv {lead:6}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_az_p9r2]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_kept
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p9r2
tag @e[type=minecraft:marker,tag=rlk_mb_az_p9r2] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p9r2] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p9r2,limit=1] run function rlk:mboss/azhdaha/p/burrow/ring_at
