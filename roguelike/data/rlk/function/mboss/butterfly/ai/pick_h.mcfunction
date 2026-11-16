# @s = body. Range-filtered, weighted shuffle bag of the human form, no immediate repeat:
# kick meleex2/mid, jump melee/mid, dash mid/farx2, vacuum farx2/mid (melee <= 4.0 b, far >= 8.0 b).
function rlk:mboss/mv/dist
scoreboard players operation #bfDist mb = #mbDist mb
scoreboard players set #bfBand mb 2
execute if score #bfDist mb matches ..40 run scoreboard players set #bfBand mb 1
execute if score #bfDist mb matches 80.. run scoreboard players set #bfBand mb 3
function rlk:mboss/butterfly/ai/cand_h
execute if score #bfCn mb matches 0 run function rlk:mboss/butterfly/ai/refill_h
execute if score #bfCn mb matches 0 run function rlk:mboss/butterfly/ai/cand_h
execute if score #bfCn mb matches 0 run function rlk:mboss/butterfly/ai/cand_any_h
execute if score #bfCn mb matches 0 run scoreboard players set #bfC1 mb 1
execute if score #bfCn mb matches 0 run scoreboard players set #bfCn mb 1
execute store result score #bfR mb run random value 0..999
scoreboard players operation #bfR mb %= #bfCn mb
function rlk:mboss/butterfly/ai/draw_h
execute if score #bfPick mb matches 0 run scoreboard players set #bfPick mb 1
scoreboard players operation #bfLast mb = #bfPick mb
function rlk:mboss/butterfly/ai/launch
