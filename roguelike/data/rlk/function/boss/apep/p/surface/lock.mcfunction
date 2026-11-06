# @s = body (t26, hidden): the surfacing point = 9.0 b from the player toward the boss (lockb, clamp r 14);
# the surfacing splash r 3.6 (tell 10, 32 %) with its keep decal (the leaf ring
# the footage shows at the surfacing spot) and the circling leaves.
function rlk:boss/apep/u/lockb {d:9}
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p36u]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p36u
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p36u] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p36u] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p36u,limit=1] run function rlk:boss/apep/p/surface/splash_hz
