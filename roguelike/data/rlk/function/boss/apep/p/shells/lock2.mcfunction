# t79: lock 2 (lockv lead 8); shell 2 r 3.0 (tell 14, 130 %), quiet (none row);
# the hovering shell moves over its point (10 b up) and stays there to the streak.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
function rlk:mboss/mv/lockv {lead:8}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p33b]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p33b
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p33b] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p33b] remove rlk_mb_lock
function rlk:mboss/grp_new
scoreboard players operation #apq33G mb = #mbGrp mb
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33b,limit=1] run function rlk:boss/apep/p/shells/hz2
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s2] run data merge entity @s {teleport_duration:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33b,limit=1] positioned ~ ~10 ~ as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s2] run tp @s ~ ~ ~
