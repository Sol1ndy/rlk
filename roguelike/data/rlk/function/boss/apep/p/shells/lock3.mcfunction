# t82: lock 3 (lockp); shell 3 r 3.0 (tell 14, 130 %), quiet (none row);
# the hovering shell moves over its point (10 b up) and stays there to the streak.
function rlk:boss/apep/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p33c]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p33c
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p33c] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p33c] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33c,limit=1] run function rlk:boss/apep/p/shells/hz3
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s3] run data merge entity @s {teleport_duration:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33c,limit=1] positioned ~ ~10 ~ as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s3] run tp @s ~ ~ ~
