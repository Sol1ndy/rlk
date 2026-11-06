# Small meteor 0 (hit t64): its target, then the hazard + the air halo + the prop high above it.
function rlk:mboss/mv/lockv {lead:10}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_p32
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_p32m0
tag @e[type=minecraft:marker,tag=rlk_mb_lock] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m0,limit=1] run function rlk:boss/azhdaha/p/meteor/s0_hz
