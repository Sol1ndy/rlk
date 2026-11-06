# #bfPick = pattern id: human melee patterns burst-run to their distance first, butterfly patterns switch
# the wing element look first (ai/prep); then the slot.
execute if score #bfPick mb matches 2 unless entity @e[tag=rlk_body,distance=..3,limit=1] run return run function rlk:mboss/butterfly/ai/close_begin
execute if score #bfPick mb matches 11 run return run function rlk:mboss/butterfly/ai/prep_begin
execute if score #bfPick mb matches 12 run return run function rlk:mboss/butterfly/ai/prep_begin
execute if score #bfPick mb matches 13 run return run function rlk:mboss/butterfly/ai/prep_begin
execute if score #bfPick mb matches 14 run return run function rlk:mboss/butterfly/ai/prep_begin
execute if score #bfPick mb matches 15 run return run function rlk:mboss/butterfly/ai/prep_begin
function rlk:mboss/butterfly/ai/go
