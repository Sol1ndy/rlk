# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# t32: the body unparked at the centre, the p3 look UPRIGHT and the rig revival clip in the same tick
# (the clip hides every part from its key 0, so the unparked pose is never shown; AP-FIX RV-07).
function rlk:boss/apep/svc/unpark
function rlk:boss/apep/svc/look_p3
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/apep/rig/stance/upright
function rlk:boss/apep/play/revival
