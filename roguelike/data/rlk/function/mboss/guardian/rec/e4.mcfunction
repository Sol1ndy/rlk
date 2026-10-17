# One counted cryo hit (at most one per 8 t of the fight clock #gdClk).
execute if score #gdClk mb < #gdRc4 mb run return 0
scoreboard players operation #gdRc4 mb = #gdClk mb
scoreboard players add #gdRc4 mb 8
scoreboard players add #gdN4 mb 1
execute if score #gdN4 mb >= #gdQ4 mb run scoreboard players set #gdRecNew mb 4
