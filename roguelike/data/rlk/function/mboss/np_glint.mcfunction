# The unparriable-attack warning (combat overhaul C; the original's yellow flash, video_notes 1.6): a gold sphere-ring with a
# long horizontal flare, bright then fading (player/def/fx/glint), and a chime: "this attack cannot be parried: dodge it".
# Drawn on the visible body: the running boss's glint point (mboss/d/np_at: the chest / head of its rig above the body
# anchor, registry "glint"; never the hit-box husk's eyes - a px boss's husk is 0.2 b tall - and never under the floor).
# Called by hz/np_auto (a hazard whose wind-up is the tell) and by the modules at the tell tick of an attack whose hazard
# is made at the strike frame (mboss_lib.np_warn). Any executor. Gate: np_gate.
function rlk:mboss/np_gate
execute if score #npOk mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s rotated ~ 0 run function rlk:mboss/d/np_at
