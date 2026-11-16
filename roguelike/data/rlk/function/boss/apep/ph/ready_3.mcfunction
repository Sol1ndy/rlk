# @s = body: phase 3 ready (reload mid-CS; tests): the stage gone, the lush look, pool 47 %, the p3 title, the rig in
# p3 UPRIGHT at the centre, unparked, targetable.
function rlk:boss/apep/ph/cut
function rlk:boss/apep/rev/clear
function rlk:boss/apep/org/clear
function rlk:boss/apep/wall/clear
function rlk:boss/apep/heart/clear
execute if score #apPark mb matches 1 run function rlk:boss/apep/svc/unpark
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s 440 201 8 0 0
function rlk:boss/apep/svc/arena_lush
execute unless score #mbPoolPct mb matches 47 run function rlk:boss/apep/svc/repool_p3
function rlk:boss/apep/svc/look_p3
function rlk:boss/apep/rig/stance/upright
function rlk:boss/apep/play/idle_p3
function rlk:boss/apep/svc/title_p3
execute unless score #mbMusPh mb matches 3 run function rlk:boss/apep/svc/music_3
function rlk:boss/apep/svc/phase_3
function rlk:boss/apep/px/p3u
