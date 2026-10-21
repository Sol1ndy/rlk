# @s = body (t32, hidden): the burst point L = the predictive lock (lead 10) clamped to r 16;
# the burst hazard r 4.2 (tell 12, 56 %) with its keep decal (the rosette ring,
# plan 14: the leaf ring the footage shows 12 t before the burst) and the airborne rosette.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
function rlk:mboss/mv/lockv {lead:10}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] remove rlk_mb_lock
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run function rlk:boss/apep/u/clamp_burst3
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p31l]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p31l
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p31l] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p31l] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] run function rlk:boss/apep/p/mstrike/burst_hz
