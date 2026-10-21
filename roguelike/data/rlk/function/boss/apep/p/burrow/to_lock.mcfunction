# @s = body: the burst point = the predictive lock (lead 6) clamped to r 18; the anchor jumps there.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
function rlk:mboss/mv/lockv {lead:6}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] remove rlk_mb_lock
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run function rlk:boss/apep/u/clamp_burst1
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run tp @s ~ 201 ~
