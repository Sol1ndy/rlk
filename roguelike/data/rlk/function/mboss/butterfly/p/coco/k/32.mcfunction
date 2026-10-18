# coco clock 32
function rlk:mboss/butterfly/rig_stub/face/track
execute unless entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.12}
execute rotated as @s rotated ~ 0 positioned ^0 ^3.24 ^0.23 run function rlk:mboss/butterfly/fx/p/orb_charge
function rlk:mboss/butterfly/fx/snd/orb_charge
