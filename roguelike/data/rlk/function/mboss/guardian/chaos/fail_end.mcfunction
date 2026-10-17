# Spears done and she is on the floor: slots reset (K22), then the approach and 4-5 normal patterns.
execute if score #gdPat mb matches 1.. run function rlk:mboss/guardian/p/cancel
function rlk:mboss/guardian/chaos/reset
execute store result score #gdLeft mb run random value 4..5
function rlk:mboss/guardian/ai/approach_begin
