# #fgR = 0..#fgCn-1 (sum of the weights) -> the candidate whose weight range holds it.
scoreboard players set #fgPick mb 0
execute if score #fgPick mb matches 0 if score #fgC1 mb matches 1.. if score #fgR mb < #fgC1 mb run scoreboard players set #fgPick mb 1
scoreboard players operation #fgR mb -= #fgC1 mb
execute if score #fgPick mb matches 0 if score #fgC2 mb matches 1.. if score #fgR mb < #fgC2 mb run scoreboard players set #fgPick mb 2
scoreboard players operation #fgR mb -= #fgC2 mb
execute if score #fgPick mb matches 0 if score #fgC3 mb matches 1.. if score #fgR mb < #fgC3 mb run scoreboard players set #fgPick mb 3
scoreboard players operation #fgR mb -= #fgC3 mb
execute if score #fgPick mb matches 0 if score #fgC4 mb matches 1.. if score #fgR mb < #fgC4 mb run scoreboard players set #fgPick mb 4
scoreboard players operation #fgR mb -= #fgC4 mb
execute if score #fgPick mb matches 0 if score #fgC5 mb matches 1.. if score #fgR mb < #fgC5 mb run scoreboard players set #fgPick mb 5
scoreboard players operation #fgR mb -= #fgC5 mb
execute if score #fgPick mb matches 0 if score #fgC6 mb matches 1.. if score #fgR mb < #fgC6 mb run scoreboard players set #fgPick mb 6
scoreboard players operation #fgR mb -= #fgC6 mb
execute if score #fgPick mb matches 1 run scoreboard players set #fgBag1 mb 0
execute if score #fgPick mb matches 2 run scoreboard players set #fgBag2 mb 0
execute if score #fgPick mb matches 3 run scoreboard players set #fgBag3 mb 0
execute if score #fgPick mb matches 4 run scoreboard players set #fgBag4 mb 0
execute if score #fgPick mb matches 5 run scoreboard players set #fgBag5 mb 0
execute if score #fgPick mb matches 6 run scoreboard players set #fgBag6 mb 0
