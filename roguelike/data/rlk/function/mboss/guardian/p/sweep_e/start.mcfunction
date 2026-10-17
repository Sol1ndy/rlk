# Enchanted sweep (record complete; the core already turned the spear) start (@s = body): sweep_e clip (50 t). See p56.py for the timeline.
kill @e[tag=rlk_mb_gd_p12]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/guardian/rig/play/sweep_e
function rlk:mboss/guardian/p/sweep_e/slices
execute if score #gdSwEl mb matches 1 at @s rotated as @s rotated ~ 0 run function rlk:mboss/guardian/p/sweep_e/rim1
execute if score #gdSwEl mb matches 2 at @s rotated as @s rotated ~ 0 run function rlk:mboss/guardian/p/sweep_e/rim2
execute if score #gdSwEl mb matches 3 at @s rotated as @s rotated ~ 0 run function rlk:mboss/guardian/p/sweep_e/rim3
execute if score #gdSwEl mb matches 4 at @s rotated as @s rotated ~ 0 run function rlk:mboss/guardian/p/sweep_e/rim4
