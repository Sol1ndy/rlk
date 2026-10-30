# coco clock 3
function rlk:mboss/butterfly/rig/face/track
execute unless entity @e[tag=rlk_body,distance=..6.5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.3}
# the wing wrap: the lime core grows at her chest with converging streaks (14 t)
execute rotated as @s rotated ~ 0 positioned ^0 ^3.276 ^0.306 run function rlk:mboss/butterfly/fx/p/orb_charge
function rlk:mboss/butterfly/fx/snd/orb_charge
