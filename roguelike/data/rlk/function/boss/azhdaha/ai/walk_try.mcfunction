# Far band: 25 % walk toward the player first (<= 40 t, 0.13 b/t, inside the body disc).
execute store result score #azR mb run random value 0..99
execute if score #azR mb matches ..24 run function rlk:boss/azhdaha/ai/walk_go
