# The emergence spot under lockv lead 8 (re-tagged rlk_mb_az_p9e)
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
function rlk:mboss/mv/lockv {lead:8}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_az_p9e]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_kept
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p9e
tag @e[type=minecraft:marker,tag=rlk_mb_az_p9e] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p9e] remove rlk_mb_lock
tag @e[tag=rlk_mb_az_p9e] add rlk_mb_az_p9m
