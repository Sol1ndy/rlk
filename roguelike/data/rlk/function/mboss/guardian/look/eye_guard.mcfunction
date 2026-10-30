# Guard aura: gold eye, or slot A's element when guard II re-records a remembered element (m2 B10-B17).
function rlk:mboss/guardian/rig/eye/gold
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 1 run function rlk:mboss/guardian/rig/eye/pyro
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 2 run function rlk:mboss/guardian/rig/eye/hydro
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 3 run function rlk:mboss/guardian/rig/eye/electro
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 4 run function rlk:mboss/guardian/rig/eye/cryo
