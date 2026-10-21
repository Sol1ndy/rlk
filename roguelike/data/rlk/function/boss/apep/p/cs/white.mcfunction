# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# t24 the white-out: the lush arena + props, the dressing gone, the stage markers gone, the body unparked
# at the centre (hidden), the phase-3 pool, the p3 look UPRIGHT, the push ring (8 -> 12 b).
function rlk:boss/apep/fx/hud/whiteout {hold:28}
function rlk:boss/apep/fx/dress/clear
function rlk:boss/apep/svc/arena_lush
function rlk:boss/apep/org/marks_kill
function rlk:boss/apep/svc/unpark
function rlk:boss/apep/svc/repool_p3
function rlk:boss/apep/svc/look_p3
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/apep/rig/stance/upright
function rlk:boss/apep/svc/push_ring_cs
