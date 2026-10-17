# @s = body. Range-filtered, weighted shuffle bag with no immediate repeat (K2/K3):
# P1 meleex2/mid, P2 mid/far, P3 meleex2, P4 melee/mid/farx3, P5 farx3 (melee <= 4.0 b, far >= 8.0 b).
# Pull guarantee: P4 has not run in this stretch of normals (#gdP4N 0) and this is the stretch's last
# pick (#gdLeft 0) -> P4 now, at any distance (from melee range she hops back first, ai/back), so it
# shows up in every stretch of normals.
function rlk:mboss/mv/dist
scoreboard players operation #gdDist mb = #mbDist mb
scoreboard players set #gdBand mb 2
execute if score #gdDist mb matches ..40 run scoreboard players set #gdBand mb 1
execute if score #gdDist mb matches 80.. run scoreboard players set #gdBand mb 3
execute if score #gdP4N mb matches 0 if score #gdLeft mb matches ..0 unless score #gdLast mb matches 4 run return run function rlk:mboss/guardian/ai/pity
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
