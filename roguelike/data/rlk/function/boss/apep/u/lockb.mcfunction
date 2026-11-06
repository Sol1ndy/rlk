# Macro {d}: the lock d b in front of the player on the boss -> player line (as the body), clamped to
# the idle disc r 14 (R's re-emergence point, plan 8.1 R).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
$execute at @e[tag=rlk_body,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_lock"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run function rlk:boss/apep/u/clamp_idle
