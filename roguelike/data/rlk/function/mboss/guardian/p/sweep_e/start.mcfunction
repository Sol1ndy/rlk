# Enchanted sweep (record complete; the core already turned the spear) start (@s = body): sweep_e clip (45 t). See p56.py for the timeline.
kill @e[tag=rlk_mb_gd_p12]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/guardian/rig/play/sweep_e
function rlk:mboss/guardian/p/sweep_e/slices
