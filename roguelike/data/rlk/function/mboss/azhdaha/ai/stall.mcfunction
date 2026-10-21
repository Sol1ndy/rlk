# Anti-stall: the player stayed on the tail lane for 3 decisions without a tail pattern -> turn180, then a
# front pattern (#azFront 1: the next pick uses the HEAD near column).
scoreboard players set #azTailN mb 0
scoreboard players set #azFront mb 1
scoreboard players set #azTurnK mb 5
execute if score #azS mb matches ..-1 run scoreboard players set #azTurnK mb 6
scoreboard players set #azPick mb 27
function rlk:mboss/azhdaha/ai/go
