# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Every wall (pause, reload, cleanup, death, the CS, a failure strike, the phase jumps; idempotent, any executor):
# the recorded blocks first, then the blades, groups and locks; then the arena's barrier safety sweep (FN-26;
# its spans stay inside walk - 0.5, the rim barrier is never touched).
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wallb] at @s run function rlk:boss/apep/wall/unput
function rlk:boss/apep/om/wall/kill_all
kill @e[type=minecraft:marker,tag=rlk_mb_ap_wall]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_wlock]
function rlk:mboss/arena/ap_oasis/sweep {y0:201,y1:202}
