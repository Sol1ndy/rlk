# The warning glint of an unparriable attack (@s = body; the patterns call it at the tell tick of such a hit: Q4 beam,
# Q5a, Q5b's finisher, Q6's landing, and the full-arena hits of F / G): at the rig's chest anchor of the running
# clip tick - she may be in the air - or 2 b over her feet without the rig (framework gate: mboss/np_glint_here).
function rlk:boss/arlecchino/rig/anchor/chest
execute if entity @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] at @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] run return run function rlk:mboss/np_glint_here
execute at @s positioned ~ ~2 ~ run function rlk:mboss/np_glint_here
