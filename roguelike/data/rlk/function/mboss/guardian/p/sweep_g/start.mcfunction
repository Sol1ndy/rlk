# Gold sweep (guard timeout) start (@s = body): sweep clip (39 t). See p56.py for the timeline.
kill @e[tag=rlk_mb_gd_p11]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/guardian/rig/play/sweep
function rlk:mboss/guardian/p/sweep_g/slices
