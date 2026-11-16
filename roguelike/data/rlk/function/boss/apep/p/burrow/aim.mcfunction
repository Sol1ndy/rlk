# @s = body (hidden, t(23, 26, 29)): the shadow's next goal: the predictive lock (lead 10), its head (3.13 b
# ahead, the rig's burst anchor) on it, the anchor inside r 18; it faces the lock and glides there over $(t) t.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
function rlk:mboss/mv/lockv {lead:10}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p1g]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3.13 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p1","rlk_mb_ap_p1g"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3.13 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p1g,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p1g,limit=1] run function rlk:boss/apep/u/clamp_burst1
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
$execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p1g,limit=1] run function rlk:mboss/mv/glide {t:$(t)}
