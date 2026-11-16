# #bfR = 0..#bfCn-1 (sum of the weights) -> the candidate whose weight range holds it.
scoreboard players set #bfPick mb 0
execute if score #bfPick mb matches 0 if score #bfC1 mb matches 1.. if score #bfR mb < #bfC1 mb run scoreboard players set #bfPick mb 1
scoreboard players operation #bfR mb -= #bfC1 mb
execute if score #bfPick mb matches 0 if score #bfC2 mb matches 1.. if score #bfR mb < #bfC2 mb run scoreboard players set #bfPick mb 2
scoreboard players operation #bfR mb -= #bfC2 mb
execute if score #bfPick mb matches 0 if score #bfC3 mb matches 1.. if score #bfR mb < #bfC3 mb run scoreboard players set #bfPick mb 3
scoreboard players operation #bfR mb -= #bfC3 mb
execute if score #bfPick mb matches 0 if score #bfC4 mb matches 1.. if score #bfR mb < #bfC4 mb run scoreboard players set #bfPick mb 4
scoreboard players operation #bfR mb -= #bfC4 mb
execute if score #bfPick mb matches 1 run scoreboard players set #bfBag1 mb 0
execute if score #bfPick mb matches 2 run scoreboard players set #bfBag2 mb 0
execute if score #bfPick mb matches 3 run scoreboard players set #bfBag3 mb 0
execute if score #bfPick mb matches 4 run scoreboard players set #bfBag4 mb 0
