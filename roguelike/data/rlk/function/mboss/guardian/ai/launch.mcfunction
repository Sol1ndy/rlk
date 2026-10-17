# #gdPick = pattern id: start it, melee patterns close in first.
execute if score #gdPick mb matches 3 unless entity @e[tag=rlk_body,distance=..3,limit=1] run return run function rlk:mboss/guardian/ai/close_begin
function rlk:mboss/guardian/ai/go
