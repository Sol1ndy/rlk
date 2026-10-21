# Every dome (safe markers + org models), the Q2 mask hazards and the footprint rims (idempotent, any executor;
# the core calls it from cleanup, the phase jumps, death and a cancelled Q2).
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p32h] at @s run function rlk:mboss/hz/expire
kill @e[type=minecraft:marker,tag=rlk_mb_ap_dome]
function rlk:boss/apep/om/dome/kill_all
kill @e[tag=rlk_mb_ap_domed]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_aft]
function rlk:boss/apep/fx/tele/safe_end {id:0}
function rlk:boss/apep/fx/tele/safe_end {id:1}
function rlk:boss/apep/fx/tele/safe_end {id:2}
