# One counted hydro hit (at most one per 8 t of the fight clock #gdClk).
execute if score #gdClk mb < #gdRc2 mb run return 0
scoreboard players operation #gdRc2 mb = #gdClk mb
scoreboard players add #gdRc2 mb 8
scoreboard players add #gdN2 mb 1
execute if score #gdN2 mb >= #gdQ2 mb run scoreboard players set #gdRecNew mb 2
