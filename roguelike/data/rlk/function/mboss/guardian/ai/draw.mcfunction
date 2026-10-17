# #gdR = 0..#gdCn-1 (sum of the weights) -> the candidate whose weight range holds it.
scoreboard players set #gdPick mb 0
execute if score #gdPick mb matches 0 if score #gdC1 mb matches 1.. if score #gdR mb < #gdC1 mb run scoreboard players set #gdPick mb 1
scoreboard players operation #gdR mb -= #gdC1 mb
execute if score #gdPick mb matches 0 if score #gdC2 mb matches 1.. if score #gdR mb < #gdC2 mb run scoreboard players set #gdPick mb 2
scoreboard players operation #gdR mb -= #gdC2 mb
execute if score #gdPick mb matches 0 if score #gdC3 mb matches 1.. if score #gdR mb < #gdC3 mb run scoreboard players set #gdPick mb 3
scoreboard players operation #gdR mb -= #gdC3 mb
execute if score #gdPick mb matches 0 if score #gdC4 mb matches 1.. if score #gdR mb < #gdC4 mb run scoreboard players set #gdPick mb 4
scoreboard players operation #gdR mb -= #gdC4 mb
execute if score #gdPick mb matches 0 if score #gdC5 mb matches 1.. if score #gdR mb < #gdC5 mb run scoreboard players set #gdPick mb 5
scoreboard players operation #gdR mb -= #gdC5 mb
execute if score #gdPick mb matches 1 run scoreboard players set #gdBag1 mb 0
execute if score #gdPick mb matches 2 run scoreboard players set #gdBag2 mb 0
execute if score #gdPick mb matches 3 run scoreboard players set #gdBag3 mb 0
execute if score #gdPick mb matches 4 run scoreboard players set #gdBag4 mb 0
execute if score #gdPick mb matches 5 run scoreboard players set #gdBag5 mb 0
