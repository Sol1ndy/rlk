function rlk:mboss/azhdaha/ai/cand
execute if score #azCn mb matches 0 run return run function rlk:mboss/azhdaha/ai/fallback
execute store result score #azR mb run random value 0..9999
scoreboard players operation #azR mb %= #azCn mb
function rlk:mboss/azhdaha/ai/draw
execute if score #azPick mb matches 0 run return run function rlk:mboss/azhdaha/ai/fallback
function rlk:mboss/azhdaha/ai/go
