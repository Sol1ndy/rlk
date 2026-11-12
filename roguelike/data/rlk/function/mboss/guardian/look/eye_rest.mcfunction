# Outside guard/chaos: the gems keep the latest recorded element of this cycle, else the painted Geo eye.
function rlk:mboss/guardian/rig/eye/geo
execute if score #gdSlotA mb matches 1 run function rlk:mboss/guardian/rig/eye/pyro
execute if score #gdSlotA mb matches 2 run function rlk:mboss/guardian/rig/eye/hydro
execute if score #gdSlotA mb matches 3 run function rlk:mboss/guardian/rig/eye/electro
execute if score #gdSlotA mb matches 4 run function rlk:mboss/guardian/rig/eye/cryo
execute if score #gdSlotB mb matches 1 run function rlk:mboss/guardian/rig/eye/pyro
execute if score #gdSlotB mb matches 2 run function rlk:mboss/guardian/rig/eye/hydro
execute if score #gdSlotB mb matches 3 run function rlk:mboss/guardian/rig/eye/electro
execute if score #gdSlotB mb matches 4 run function rlk:mboss/guardian/rig/eye/cryo
