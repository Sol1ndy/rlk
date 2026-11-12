# #gdPick = pattern id: start it; melee patterns close in first, a pattern with a hop back (P4) hops back
# first when the player is too near.
execute if score #gdPick mb matches 3 unless entity @e[tag=rlk_body,distance=..3,limit=1] run return run function rlk:mboss/guardian/ai/close_begin
execute if score #gdPick mb matches 4 if entity @e[tag=rlk_body,distance=..5,limit=1] run return run function rlk:mboss/guardian/ai/back_begin
function rlk:mboss/guardian/ai/go
