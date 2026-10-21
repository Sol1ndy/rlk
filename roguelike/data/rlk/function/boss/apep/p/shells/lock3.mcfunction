# t82: lock 3 (lockp); shell 3 r 3.0 (tell 14, 130 %), quiet (none row);
# the q3_lock sound at the point; the hovering shell slides to 5 b over it (4 t), then falls onto it
# (AP-FIX RV-02: the readable cue 14 t before the hit, no floor decal).
function rlk:boss/apep/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p33c]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p33c
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p33c] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p33c] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33c,limit=1] run function rlk:boss/apep/fx/snd/q3_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33c,limit=1] run function rlk:boss/apep/p/shells/hz3
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s3] run data merge entity @s {teleport_duration:4}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33c,limit=1] positioned ~ ~5 ~ as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s3] run tp @s ~ ~ ~
