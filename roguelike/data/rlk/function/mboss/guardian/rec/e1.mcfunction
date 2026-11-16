# One counted pyro hit (at most one per 8 t of the fight clock #gdClk).
execute if score #gdClk mb < #gdRc1 mb run return 0
scoreboard players operation #gdRc1 mb = #gdClk mb
scoreboard players add #gdRc1 mb 8
scoreboard players add #gdN1 mb 1
execute if score #gdN1 mb >= #gdQ1 mb run scoreboard players set #gdRecNew mb 1
