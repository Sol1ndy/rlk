# Into the main slot (#apPick): the opener of a pattern that names one (R before P4 when the player is far: #apNext
# hands P4 over at the opener's end), then go_raw.
execute if score #apPick mb matches 4 if score #apDist mb matches 91.. run scoreboard players set #apNext mb 4
execute if score #apPick mb matches 4 if score #apNext mb matches 4 run scoreboard players set #apPick mb 7
function rlk:boss/apep/ai/go_raw
