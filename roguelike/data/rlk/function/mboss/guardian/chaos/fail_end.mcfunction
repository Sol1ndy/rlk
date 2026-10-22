# The last spear has struck (the pattern's release, 10 t after it; m4: she leaves at +90 while the giant spear
# still stands) and she is on the floor: slots reset (K22), then the approach and 4-5 normal patterns. The
# fail pattern finishes its tail (planted spear dissolving) in the slot; the next decision waits for it.
execute if score #gdF mb matches 170.. if score #gdPat mb matches 1.. run function rlk:mboss/guardian/p/cancel
function rlk:mboss/guardian/chaos/reset
execute store result score #gdLeft mb run random value 4..5
function rlk:mboss/guardian/ai/approach_begin
