# P8 ends with turn180 when the player is still behind the rump (plan 5 P8).
function rlk:boss/azhdaha/ai/sample
execute unless score #azZone mb matches 6..7 run return 0
scoreboard players set #azTurnK mb 5
execute if score #azS mb matches ..-1 run scoreboard players set #azTurnK mb 6
scoreboard players set #azPick mb 27
function rlk:boss/azhdaha/ai/go
