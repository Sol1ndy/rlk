# Chaos now with preset slots (30 = keep, 31 = electro x2, 32 = inert x2, 33 = pyro + cryo).
scoreboard players operation #gdX mb = #gdSlotA mb
scoreboard players operation #gdY mb = #gdSlotB mb
function rlk:mboss/guardian/test/cut
scoreboard players operation #gdSlotA mb = #gdX mb
scoreboard players operation #gdSlotB mb = #gdY mb
execute if score #gdTst mb matches 31 run scoreboard players set #gdSlotA mb 3
execute if score #gdTst mb matches 31 run scoreboard players set #gdSlotB mb 3
execute if score #gdTst mb matches 32 run scoreboard players set #gdSlotA mb 0
execute if score #gdTst mb matches 32 run scoreboard players set #gdSlotB mb 0
execute if score #gdTst mb matches 33 run scoreboard players set #gdSlotA mb 1
execute if score #gdTst mb matches 33 run scoreboard players set #gdSlotB mb 4
function rlk:mboss/guardian/chaos/begin
