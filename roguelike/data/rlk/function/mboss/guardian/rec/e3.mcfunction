# One counted electro hit (at most one per 8 t of the fight clock #gdClk).
execute if score #gdClk mb < #gdRc3 mb run return 0
scoreboard players operation #gdRc3 mb = #gdClk mb
scoreboard players add #gdRc3 mb 8
scoreboard players add #gdN3 mb 1
execute if score #gdN3 mb >= #gdQ3 mb run scoreboard players set #gdRecNew mb 3
