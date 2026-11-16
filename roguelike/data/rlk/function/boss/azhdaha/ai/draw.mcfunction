# #azR = 0..#azCn-1 -> the candidate whose weight range holds it.
scoreboard players set #azPick mb 0
execute if score #azPick mb matches 0 if score #azC1 mb matches 1.. if score #azR mb < #azC1 mb run scoreboard players set #azPick mb 1
scoreboard players operation #azR mb -= #azC1 mb
execute if score #azPick mb matches 0 if score #azC2 mb matches 1.. if score #azR mb < #azC2 mb run scoreboard players set #azPick mb 2
scoreboard players operation #azR mb -= #azC2 mb
execute if score #azPick mb matches 0 if score #azC3 mb matches 1.. if score #azR mb < #azC3 mb run scoreboard players set #azPick mb 3
scoreboard players operation #azR mb -= #azC3 mb
execute if score #azPick mb matches 0 if score #azC4 mb matches 1.. if score #azR mb < #azC4 mb run scoreboard players set #azPick mb 4
scoreboard players operation #azR mb -= #azC4 mb
execute if score #azPick mb matches 0 if score #azC5 mb matches 1.. if score #azR mb < #azC5 mb run scoreboard players set #azPick mb 5
scoreboard players operation #azR mb -= #azC5 mb
execute if score #azPick mb matches 0 if score #azC6 mb matches 1.. if score #azR mb < #azC6 mb run scoreboard players set #azPick mb 6
scoreboard players operation #azR mb -= #azC6 mb
execute if score #azPick mb matches 0 if score #azC7 mb matches 1.. if score #azR mb < #azC7 mb run scoreboard players set #azPick mb 7
scoreboard players operation #azR mb -= #azC7 mb
execute if score #azPick mb matches 0 if score #azC8 mb matches 1.. if score #azR mb < #azC8 mb run scoreboard players set #azPick mb 8
scoreboard players operation #azR mb -= #azC8 mb
execute if score #azPick mb matches 0 if score #azC9 mb matches 1.. if score #azR mb < #azC9 mb run scoreboard players set #azPick mb 9
scoreboard players operation #azR mb -= #azC9 mb
execute if score #azPick mb matches 0 if score #azC31 mb matches 1.. if score #azR mb < #azC31 mb run scoreboard players set #azPick mb 31
scoreboard players operation #azR mb -= #azC31 mb
execute if score #azPick mb matches 0 if score #azC32 mb matches 1.. if score #azR mb < #azC32 mb run scoreboard players set #azPick mb 32
scoreboard players operation #azR mb -= #azC32 mb
execute if score #azPick mb matches 0 if score #azC43 mb matches 1.. if score #azR mb < #azC43 mb run scoreboard players set #azPick mb 43
scoreboard players operation #azR mb -= #azC43 mb
execute if score #azPick mb matches 0 if score #azC44 mb matches 1.. if score #azR mb < #azC44 mb run scoreboard players set #azPick mb 44
scoreboard players operation #azR mb -= #azC44 mb
