# @s = body. Range-filtered shuffle bag with no immediate repeat (K2/K3):
# P1 melee/mid, P2 mid/far, P3 melee, P4 far, P5 far (melee <= 4.0 b, far >= 8.0 b).
function rlk:mboss/mv/dist
scoreboard players operation #gdDist mb = #mbDist mb
scoreboard players set #gdBand mb 2
execute if score #gdDist mb matches ..40 run scoreboard players set #gdBand mb 1
execute if score #gdDist mb matches 80.. run scoreboard players set #gdBand mb 3
function rlk:mboss/guardian/ai/cand
execute if score #gdCn mb matches 0 run function rlk:mboss/guardian/ai/refill
execute if score #gdCn mb matches 0 run function rlk:mboss/guardian/ai/cand
execute if score #gdCn mb matches 0 run function rlk:mboss/guardian/ai/cand_any
execute if score #gdCn mb matches 0 run scoreboard players set #gdC1 mb 1
execute if score #gdCn mb matches 0 run scoreboard players set #gdCn mb 1
execute store result score #gdR mb run random value 0..999
scoreboard players operation #gdR mb %= #gdCn mb
function rlk:mboss/guardian/ai/draw
execute if score #gdPick mb matches 0 run scoreboard players set #gdPick mb 1
scoreboard players operation #gdLast mb = #gdPick mb
function rlk:mboss/guardian/ai/launch
